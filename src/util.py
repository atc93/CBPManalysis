import os
import shutil

import numpy as np
import math

# create results directory
def create_output_directory(dir_path, opt):

    if os.path.isdir(dir_path) and not os.listdir(dir_path):
        print(
            '   Output directoy already exists and is empty --> will save results there')
    elif os.path.isdir(dir_path) and os.listdir(dir_path):
        if opt == 'ovwt':
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

def triple_gauss_func(x, amp1, mean1, std1, amp2, mean2, std2, amp3, mean3, std3):
    return amp1 * np.exp(-(x - mean1) ** 2 / (2. * std1 ** 2)) + amp2 * np.exp(-(x - mean2) ** 2 / (2. * std2 ** 2)) + amp3 * np.exp(-(x - mean3) ** 2 / (2. * std3 ** 2))

# define double Gauss function
def multiple_gauss_func(x, param, n,):
    func = 0
    for i in range(n):
        func += param[0+i*3] * np.exp(-(x - param[1+i*3]) ** 2 / (2. * param[2+i*3] ** 2))
    return func