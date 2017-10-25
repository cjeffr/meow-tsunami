# -*- coding: utf-8 -*-
"""
Reads in a dictionary of points along the West US Coast, and writes out the 
lat/lon to a text file that can be looped over in geoclaw
"""
import os
import numpy as np

def coastal_points_tracking_array():
    """
    Loads a file that keeps all of the points along the coast that correspond
    to tide gauges data we're performing calculations on. This is so the indexes of
    each array can be tied together for posting in the GPSCockpit
    """

    #declare the original file path and open the file as an array
    path = '/Users/jeffriesc/Research_Stuff/tsunami_files'
    coastal_points_file = os.path.join(path, 'Coast_points1.txt')
    coastal_points_array = np.loadtxt(coastal_points_file)
    return (coastal_points_array)

