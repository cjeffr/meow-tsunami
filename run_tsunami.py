"""
This program connects several scripts together to get slip from a GPS earthquake characterization system
multiplies the slip to tsunamis generated on multiple subfaults using GeoClaw, then adds the waveforms together
to get a new waveform for all tracked tide gauges, and reports the max height and arrival time of that max to a
database for display in GPSCockpit
"""

import queue
import configparser
import slip_queue
from calc_tsunami import SlipCalc
from import_gauge_array import coastal_points_tracking_array
from create_dict import create_dictionary
from find_max import MaxHeight
# from RunCascadia.load_tsunamis_memory import load_tsunamis
from mongo_dict import SendToMongoDB
import argparse
import time
import h5py

"""comment out load_tsunamis 9/21/17 to test loading on demand from binary file
# get the green's functions loaded from memory
gf = load_tsunamis()
"""
epoch = time


#model = cfg['NA_CAS'] ####CHECK HERE!!!!!!

def main(name, cfg):
    rmq = cfg['rmq']
    mdb = cfg['mdb']
    model = cfg[name]
    print(model['gauges'])
    # initialize queue for holding slip values
    try:
        in_q = queue.Queue()
        out_q = queue.Queue()
    except Exception as EE:
        print('Exception! {}: {}',format(type(EE), str(EE)))

    tgfs = h5py.File(model['catalog'], 'r')


    # load all the sites into an array
    sites = coastal_points_tracking_array()


    # get maximum waveheight
    maxes = MaxHeight()

    # initialize the output dictionary
    output_dict = {}
    #calc = SlipCalc(model)
   # calc.start()

    # variable set to module for sending to the MongoDB

    send_to_mongo = SendToMongoDB(mdb, out_q)
    send_to_mongo.start()

    # pull slip from the RabbitMQ
    get_slip = slip_queue.RabbitMQInterface(in_q, rmq)
    get_slip.start()


    calc_input_q = queue.Queue()
    calc_output_q = queue.Queue()
    for x in range(4):
        slip_calc = SlipCalc(model, calc_input_q, calc_output_q, tgfs)
        slip_calc.start()
    # always run
    while True:
        # get the earthquake origin time, slip, and  model name from RabbitMQ
        time, slip, model = in_q.get()
        print(time)  # , model, slip)
        current = epoch.time()
        diff = current - time
        print(diff)
        # get my 1 tsunami array by passing slip and the green's functions
        calc_input_q.put(slip)

        #calc.calc_tsunami(slip, tgfs)
        # print(waves, t)
        try:

            waves, t = calc_output_q.get(False)
            # get the maxes
            max_a, max_t = maxes.get_max_waveheight(waves, t)
            # print(max_a)


            # bind up all output variables into a dictionary
            output = create_dictionary(name, time, max_t, max_a, sites)
            out_q.put_nowait(output)
            # print(output)
        except queue.Empty:
            pass


        # send everything on to the MongoDB for display in the cockpit
        #send_to_mongo(out_q)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Model Name')
    parser.add_argument('name', help = 'model name you are using')
    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    cfg.read('tsunami_config.ini')

    main(args.name, cfg)
