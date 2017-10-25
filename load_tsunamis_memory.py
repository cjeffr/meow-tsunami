import os
import numpy as np

# Path of the tide gauge files
path = "/Users/jeffriesc/Desktop/GF"



def load_tsunamis():
    """
    This function opens up all of the tide gauge text files, reads them in and writes the values
    to a dictionary. This dictionary is then saved in memory to be passed along to all modules for
    the tsunami early warning program.
    :return: returns dictionary of tsunamis
    """
    # Opens one file and loads the time column, and max length of the array
    data = np.loadtxt(os.path.join(path, '000_00000.txt'))

    # number of columns for each subfault's array (needs to be softcoded)
    sitecount = 145

    # Opens a text file with a list of the subfaults, array indices are the subfault numbers
    fault_numbers = np.loadtxt("/Users/jeffriesc/Research_Stuff/Cascadia20x10.d")

    # Pre declare the dictionaries
    tsunami_dict = {}
    runup_sites_dict = {}

    # create a new dictionary key for each fault and assign the time column to its own key called 'epoch'
    for fault in range(0, len(fault_numbers)):
        tsunami_dict[fault] = np.zeros(shape=(len(data), sitecount))
        tsunami_dict['epoch']= data[:,0]


    # Iterate over all files in the directory
    for (root, dirs, filenames) in os.walk(path):
        for fname in filenames:
            print(fname)

            # exclude files that start with .
            if not fname[0] == ".":

                # separate the file name from the file extension for each gauge file
                filename, file_extension = os.path.splitext(fname)

                # create an array to hold the subfault number and site number from the filename
                number = os.path.basename(filename).split('_')

                # assign the subfault number
                subfault = int(number[0])

                # assign the site number
                site = int(number[1])

                # set an index for the tsunami array for the current subfault to none
                array_index = None

                # see if array index is a key in runup_sites_dict, if it isn't make array_index
                # the length of the dictionary and set the current value to the site id
                try:
                    array_index = runup_sites_dict[site]
                except:
                    array_index = len(runup_sites_dict)
                    runup_sites_dict[site] = array_index

                # open the current file, load it into a numpy array, paste the waveheight into
                # the appropriate column of the subfault array.
                with open (os.path.join(root, fname)) as f:

                    data_from_file = np.loadtxt(f)
                    tsunami_dict[subfault][:, array_index] = data_from_file[:, 1]

    # return the entire dictionary
    return(tsunami_dict)

