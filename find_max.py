import numpy as np

class MaxHeight(object):
    """
    Find the maximum value in an array and its associated time and return it to another program.
    This will take the maximum waveheight per site location and return that value and its time
    """
    def __init__(self):
        self.waveheights = []
        self.times = []
        self.name = None

    def get_max_waveheight(self, tsunami_array, time_array):

        # grab the index of the hightest value for that array
        max_index = np.argmax(tsunami_array, axis=0)

        # get the max value from the waveheight
        max_amp = np.max(tsunami_array, axis=0)

        # use the index from the maximum waveheight to get the time
        max_time = time_array[max_index]

        #return max time and max waveheight to be sent to the MongoDB
        return(max_amp, max_time)


