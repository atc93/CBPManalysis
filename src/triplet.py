import numpy as np
import src.plotting as plotting
import matplotlib.pyplot as plt
import math

CBPM_12W2_LOCATION = 75.626
CBPM_12W3_LOCATION = 75.931
CBPM_12W_LOCATION = 76.236

def resolution(analyze, idx_file):

    print('\n <<<<----------------------------->>>>')
    print(' <<<< Performing triplet analysis >>>>')
    print(' <<<<----------------------------->>>>\n')

    centroid = [] # will contain the vertical and horizontal centroid for the triplet CBPMs
    centroid.append([])
    centroid.append([])

    # index 0 is vertical centroid
    centroid[0].append([]) # 12W2
    centroid[0][0] = analyze[0][idx_file].vertical_centroid
    centroid[0].append([]) # 12W3
    centroid[0][1] = analyze[1][idx_file].vertical_centroid
    centroid[0].append([]) # 12W
    centroid[0][2] = analyze[2][idx_file].vertical_centroid

    # index 1 is horizontal centroid
    centroid[1].append([]) # 12W2
    centroid[1][0] = analyze[0][idx_file].horizontal_centroid
    centroid[1].append([]) # 12W3
    centroid[1][1] = analyze[1][idx_file].horizontal_centroid
    centroid[1].append([]) # 12W
    centroid[1][2] = analyze[2][idx_file].horizontal_centroid

    fig, ax = plotting.create_figure('triplet\n', 'CBPM position', 'Vertical centroid [mm]', '', '')

    for idx_centroid in range(2):

        residuals_12W2 = []
        residuals_12W3 = []
        residuals_12W = []
        residuals_all_12W3 = []
        cnt = 0

        for y1, y2, y3 in zip(centroid[idx_centroid][0], centroid[idx_centroid][1], centroid[idx_centroid][2]):

            # fit first and third (12W2 and 12W)
            position = [CBPM_12W2_LOCATION, CBPM_12W_LOCATION]
            x = [y1, y3]
            fit = np.polyfit(position, x, 1)
            fit_func = np.poly1d(fit)
            residuals_12W3.append(fit_func(CBPM_12W3_LOCATION)-analyze[1][idx_file].vertical_centroid[cnt])

            # fit first and second (12W2 and 12W3)
            position = [CBPM_12W2_LOCATION, CBPM_12W3_LOCATION]
            x = [y1, y2]
            fit = np.polyfit(position, x, 1)
            fit_func = np.poly1d(fit)
            residuals_12W.append(fit_func(CBPM_12W_LOCATION)-analyze[2][idx_file].vertical_centroid[cnt])

            # fit second and third (12W3 and 12W)
            position = [CBPM_12W3_LOCATION, CBPM_12W_LOCATION]
            x = [y2, y3]
            fit = np.polyfit(position, x, 1)
            fit_func = np.poly1d(fit)
            residuals_12W2.append(fit_func(CBPM_12W2_LOCATION) - analyze[0][idx_file].vertical_centroid[cnt])

            # fit all of them
            position = [CBPM_12W2_LOCATION, CBPM_12W3_LOCATION, CBPM_12W_LOCATION]
            x = [y1, y2, y3]
            fit = np.polyfit(position, x, 1)
            fit_func = np.poly1d(fit)
            #residuals_all.append(fit_func(CBPM_12W2_LOCATION) - analyze[0][idx_file].vertical_centroid[cnt])
            residuals_all_12W3.append(fit_func(CBPM_12W3_LOCATION) - analyze[1][idx_file].vertical_centroid[cnt])
            #residuals_all.append(fit_func(CBPM_12W_LOCATION) - analyze[2][idx_file].vertical_centroid[cnt])


            #print(x[0], x[1], y1, y2, p[0], p[1], analyze[1][0].vertical_centroid[cnt], ' ', p(75.931), '\n')
            #plt.plot(x, y, 'ro')
            #plt.plot(x, p(x), c='red')
            #x = 75.931
            #y = analyze[1][idx_file].vertical_centroid[cnt]
            #plt.plot(x, y, 'bo')
            cnt += 1

        print(np.std(np.array(residuals_12W2)))
        print(np.std(np.array(residuals_12W3)))
        print(np.std(np.array(residuals_12W)))
        print(np.std(np.array(residuals_all_12W3)))


    #plt.savefig('test.eps')

    plt.close()

    fig, ax = plotting.create_figure('triplet\n', 'Fit residuals [mm]', '#', '', '')
    plt.hist(residuals_all_12W3, bins=int(math.sqrt(len(residuals_all_12W3))))
    plt.savefig('residuals.eps')

    #for i in range(len(analyze[0][0].config.n_turns)):


