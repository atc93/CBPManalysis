import os
import shutil

import numpy as np
import math

# create results directory
def create_output_directory(dir_path):

    if os.path.isdir(dir_path) and not os.listdir(dir_path):
        print(
            '   Output directoy already exists and is empty --> will save results there')
    elif os.path.isdir(dir_path) and os.listdir(dir_path):
        print('   Output directoy already exists and is NOT empty --> deleting/recreating directory (previous results will be lost)')
        shutil.rmtree(dir_path)
        os.mkdir(dir_path)
    else:
        print('   Output directory does not exist --> creating it')
        os      .mkdir(dir_path)

# definie Gauss function
def gauss_func(x, amp, mean, std):
    return amp * np.exp(-(x - mean) ** 2 / (2. * std ** 2))

# define double Gauss function
def double_gauss_func(x, amp1, mean1, std1, amp2, mean2, std2):
    return amp1 * np.exp(-(x - mean1) ** 2 / (2. * std1 ** 2)) + amp2 * np.exp(-(x - mean2) ** 2 / (2. * std2 ** 2))