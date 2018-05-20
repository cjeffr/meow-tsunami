"""
This program connects several scripts together to get slip from a GPS earthquake characterization system
multiplies the slip to tsunamis generated on multiple subfaults using GeoClaw, then adds the waveforms together
to get a new waveform for all tracked tide gauges, and reports the max height and arrival time of that max to a
database for display in GPSCockpit
"""


from queue import Queue
import configparser
import slip_queue
from calc_tsunami import calc_tsunami
from import_gauge_array import coastal_points_tracking_array
from create_dict import create_dictionary
from find_max import MaxHeight
# from RunCascadia.load_tsunamis_memory import load_tsunamis
from mongo_dict import SendToMongoDB
"""comment out load_tsunamis 9/21/17 to test loading on demand from binary file
# get the green's functions loaded from memory
gf = load_tsunamis()
"""

cfg = configparser.ConfigParser
rmq = cfg['rmq']
mdb = cfg['mdb']
model = cfg['NA_CAS'] ####CHECK HERE!!!!!!
def main():

    # initialize queue for holding slip values
    q = Queue(maxsize=1)

    # pull slip from the RabbitMQ
    get_slip = slip_queue.RabbitMQInterface(q, rmq)
    get_slip.start()

    # get maximum waveheight
    maxes = MaxHeight()

    # initialize the output dictionary
    output_dict = {}

    # variable set to module for sending to the MongoDB
    send_to_mongo = SendToMongoDB()

    # always run
    while True:
        # get the earthquake origin time, slip, and  model name from RabbitMQ
        time, slip, model = q.get()
        print(time, model, slip)

        # get my 1 tsunami array by passing slip and the green's functions
        waves, t = calc_tsunami(slip)
        # print(waves, t)

        # get the maxes
        max_a, max_t = maxes.get_max_waveheight(waves, t)
        print(max_a)

        # load all the sites into an array
        sites = coastal_points_tracking_array()

        # bind up all output variables into a dictionary
        output = create_dictionary(model, time, max_t, max_a, sites)
        print(output)

        # send everything on to the MongoDB for display in the cockpit
        send_to_mongo.store(output, mdb)


if __name__ == "__main__":
    main()
