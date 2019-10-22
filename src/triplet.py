import math
from typing import List

from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

import src.plotting as plotting
import src.util as util

CBPM_12W2_LOCATION = 75.626
CBPM_12W3_LOCATION = 75.931
CBPM_12W_LOCATION = 76.236

positions = [CBPM_12W2_LOCATION, CBPM_12W3_LOCATION, CBPM_12W_LOCATION]


def resolution(analyze, idx_file):
    print('\n <<<<----------------------------->>>>')
    print(' <<<< Performing triplet analysis >>>>')
    print(' <<<<----------------------------->>>>\n')

    '''
    will define a centroid native Python list
    that has 3 layers [x][y][z]
    [x] will be vertical or horizontal
    [y] is the CBPM
    [z] is the turn-by-turn data

    index [x=0] is vertical centroid
    index [x=0][y=0] is first CBPM (should be 12W2)
    index [x=0][y=1] is second CBPM (should be 12W3)
    index [x=0][y=2] is  third CBPM (should be 12W)

    index [x=1] is horizontal centroid
    index [x=1][y=0] is first CBPM (should be 12W2)
    index [x=1][y=1] is second CBPM (should be 12W3)
    index [x=1][y=2]is  third CBPM (should be 12W)
    '''

    centroid = []
    for i in range(2):
        centroid.append([])  # add [x=0, 1]
        for j in range(3):
            centroid[i].append([])  # add [y=0,1,2]
            if i == 0:
                centroid[i][j] = analyze[j][idx_file].vertical_centroid  # add the vertical data
            if i == 1:
                centroid[i][j] = analyze[j][idx_file].horizontal_centroid  # add the horizontal data

    res_xaxis_label = []
    res_xaxis_label.append('pair-fitting 12W2 residuals [mm]')
    res_xaxis_label.append('pair-fitting 12W3 residuals [mm]')
    res_xaxis_label.append('pair-fitting 12W residuals [mm]')
    res_xaxis_label.append('triplet-fitting 12W2 residuals [mm]')
    res_xaxis_label.append('triplet-fitting 12W2 residuals [mm]')
    res_xaxis_label.append('triplet-fitting 12W2 residuals [mm]')
    res_xaxis_label.append('triplet-fitting all residuals [mm]')

    res_axis_centroid_tag = []
    res_axis_centroid_tag.append('Vertical ')
    res_axis_centroid_tag.append('Horizontal ')
    
    plot_name: List[str] = ['vertical', 'horizontal']

    analyze[0][idx_file].triplet_resolution = []

    for idx_centroid in range(2):

        residuals = []
        for i in range(6):
            residuals.append([])

        # pair analysis
        # fit first and third, look at second's residuals
        # fit first and second, look at third's residuals
        # fit second and third, look at first's residuals
        pairs = [[1, 2, 0], [0, 2, 1], [0, 1, 2], ['12W2', '12W3', '12W ']]

        cents = [-999, -999, -999]
        cnt = 0
        for cents[0], cents[1], cents[2] in zip(centroid[idx_centroid][0], centroid[idx_centroid][1],
                                                centroid[idx_centroid][2]):
            # if cnt > 1024:
            #     cnt = 0
            #     break
            # cnt += 1

            # pair-fitting analysis
            for idx_pair in range(3):
                x = [positions[pairs[idx_pair][0]], positions[pairs[idx_pair][1]]]
                y = [cents[pairs[idx_pair][0]], cents[pairs[idx_pair][1]]]
                fit = np.polyfit(x, y, 1)
                fit_func = np.poly1d(fit)
                #plt.figure(idx_pair)
                # plt.plot(x, y, 'ro')
                #x = [pos for pos in positions]
                # plt.plot(x, fit_func(x), c='red')
                # plt.plot(positions[pairs[idx_pair][2]], cents[pairs[idx_pair][2]], 'bo')
                residuals[pairs[idx_pair][2]].append(
                    cents[pairs[idx_pair][2]] - fit_func(positions[pairs[idx_pair][2]]))

            # triplet-fitting analysis
            x = [pos for pos in positions]
            y = [cent for cent in cents]
            fit = np.polyfit(x, y, 1)
            fit_func = np.poly1d(fit)
            # plt.plot(x, y, 'ro')
            # plt.plot(x, fit_func(x), c='red')
            # plt.savefig('test.eps')
            for i in range(3):
                residuals[3 + i].append(cents[i] - fit_func(positions[i]))

        for i in range(6):
            residuals[i] -= np.mean(residuals[i])
        triplet = np.concatenate((residuals[3], residuals[4], residuals[5]), axis=None)

        # print uncorrected residuals
        #for i in range(3):
        #    print('   pair-ffiting residuals (uncorrected)', pairs[3][i], ' ', np.std(residuals[i]))
        #print('   triplet-fitting residuals (uncorrected)    ', np.std(triplet))

        # print corrected residuals
        #print('\n   pair-ffiting residuals (corrected)', pairs[3][0], ' ', np.std(residuals[0]) / math.sqrt(6))
        #print('   pair-ffiting residuals (corrected)', pairs[3][1], ' ', np.std(residuals[1]) / math.sqrt(1.5))
        #print('   pair-ffiting residuals (corrected)', pairs[3][2], ' ', np.std(residuals[2]) / math.sqrt(6))
        print('   ' + plot_name[idx_centroid] + ' triplet-fitting residuals (corrected)    {0:.5f} mm\n'.format(np.std(triplet) * math.sqrt(3)))

        analyze[0][idx_file].triplet_resolution.append(np.std(triplet) * math.sqrt(3))

        # plt.figure(0)
        # plt.savefig('fits1.png')
        # plt.figure(1)
        # plt.savefig('fits2.png')
        # plt.figure(2)
        # plt.savefig('fits3.png')
        # plt.figure(3)
        # plt.savefig('fits4.png')
        # plt.close()

        for i in range(6):
            plotting.create_figure(1, 'triplet\n', res_axis_centroid_tag[idx_centroid] + res_xaxis_label[i], '#', '', '')
            plt.hist(residuals[i], bins=int(math.sqrt(len(residuals[i]))))
            plt.savefig('results/' + analyze[0][0].config.data_file_tag[idx_file] + '_' + plot_name[idx_centroid] + '_residuals' + str(i) + '.eps')
            plt.close()

        plotting.create_figure(1, 'triplet\n', res_axis_centroid_tag[idx_centroid] + res_xaxis_label[6], '#', '', '')
        intensity, bin_edge, _ = plt.hist(triplet, bins=int(math.sqrt(len(triplet))))
        try:
            bin_center = (bin_edge[:-1] + bin_edge[1:]) / 2.
            popt, pcov = curve_fit(util.triple_gauss_func, bin_center, intensity, maxfev = 50000,
                               p0=[max(intensity), np.mean(triplet), np.std(triplet),
                                   max(intensity), np.mean(triplet) + np.std(triplet)/2, np.std(triplet)/2,
                                   max(intensity), np.mean(triplet) - np.std(triplet)/2, np.std(triplet)/2],
                               bounds=([0, -np.inf, 0, 0, -np.inf, 0, 0, -np.inf, 0,], np.inf))
            plt.plot(bin_center, util.triple_gauss_func(bin_center, *popt), color='red', linewidth=2.5)
            plt.plot(bin_center, util.gauss_func(bin_center, *popt[0:3]), ls='--', color='darkorange', linewidth=2)
            plt.plot(bin_center, util.gauss_func(bin_center, *popt[3:6]), ls='--', color='darkorange', linewidth=2)
            plt.plot(bin_center, util.gauss_func(bin_center, *popt[6:9]), ls='--', color='darkorange', linewidth=2)
        except:
            print('   RUNNING WARNING -- could not fit the residual distribution')

        plt.savefig('results/' + analyze[0][0].config.data_file_tag[idx_file] + '_' + plot_name[idx_centroid] + '_residuals6.eps')
        plt.close()
