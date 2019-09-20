import src.dataparser as dataparser
import numpy as np

class Button(dataparser.DataParser):

    def __init__(self, data):
        self.data = data
        self.button_sum = 0
        self.button = []
        self.std_button = []
        self.mean_button = []

    def extract_button_information(self):
        # extract individual buttons information
        # button 0 (or 3) is inner top
        # botton 1 (or 1) is inner bottom
        # bottom 0 (or 2) is outter bottom
        # button 3 (or 4)is outter top
        if (self.data.config.verbose > 0):
            print('\n ---------------------')
            print(' | Raw button values |')
            print(' ---------------------\n')
        for i in range(4):
            self.button.append(self.data.raw_data[:,i])
            self.std_button.append(np.std(self.button[i]))
            self.mean_button.append(np.mean(self.button[i]))
            self.button_sum += self.data.raw_data[:,i]
            if (self.data.config.verbose > 0):
                print(' Button #', i, ' -- mean: {0:0.2f} ADU'.format(self.mean_button[i]), ', std: {0:0.2f} ADU'.format(self.std_button[i])
                    , ', std/mean: {0:0.5f}'.format(self.std_button[i]/self.mean_button[i]))

    def calculate_vertical_centroid(self):
        self.vertical_centroid = []
        self.vertical_centroid.append([self.data.config.ky*(self.button[0][i]+self.button[3][i]-(self.button[1][i]+self.button[2][i]))/self.button_sum[i] for i in range(self.data.n_turns[0])])
        self.mean_vertical_centroid =  np.mean(self.vertical_centroid)
        self.std_vertical_centroid =  np.std(self.vertical_centroid)
        if (self.data.config.verbose > 0 ):
            print('\n ---------------------')
            print(' | Vertical centroid |')
            print(' ---------------------\n')        
            print(' y = {0:0.2f}'.format(self.mean_vertical_centroid), ' +- {0:0.2f}'.format(self.std_vertical_centroid), '(std) mm')
