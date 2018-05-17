"""
This code takes the un-altered green's functions and slip, multiplies each slip value to the
appropriate subfault number to get the correct amount of slip per subfault and then sums each
waveform for each site (gauge location) and passes one array rather than 200 back to the
rest of the program.
"""

import numpy as np
import h5py


# create a dictionary to store the completed array
mongo_dict = {}

# initialize the array
max_array = np.zeros(shape=(145, 2))

def get_array_size():
    """
    Defines the size of the array based on the number of tide gauges tracked and the number of subfaults

    Returns
    -------
    tg_nbr = the number of tide gauges tracked

    """

    tg_file = 'Coast_points.txt'
    lines = open(tg_file).readlines()
    tg_nbr = len(lines)
    return tg_nbr


def calc_tsunami(slip_result):
    """
    This function calculates the tsunami sized from slip

    Parameters
    ----------
    slip_result: The slip array obtained from RabbitMQ for each model

    Returns:
    -------
    waveheight_per_site: the new tGF array for each location
    time array:  time array

   """
    gf = h5py.File('tsunamis.hdf5', 'r')
    time_array = np.array(gf['time/timedata'])

    # dictionary for holding slip calculations
    new_sf = []

    # declare empty array with max size
    ar_len = len(time_array)
    ar_width = get_array_size()

    waveheight_per_site = np.zeros(shape=(ar_len, ar_width))

    # loop over index adn slip value from slip array
    for i, slip in enumerate(slip_result):
        # print(i)
        # make sure slip is a float not string
        s = float(slip)

        # multiply slip by each subfault
        new_sf.append(s * gf['GF/{:03}'.format(i)][:])

    # iterate over all the subfaults and add all subfaults together per site
    for sf in new_sf:
        waveheight_per_site += sf

    # return the slip_at_site array and the time array
    return (waveheight_per_site, time_array)

