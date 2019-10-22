import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import iqr

import src.constants as constants
import src.plotting as plotting
import src.printout as printout
import src.util as util
from src.dataparser import DataParser


class Analyze(DataParser):

    def __init__(self, raw_button, config, idx_file, idx_cbpm):
        self.raw_button = raw_button
        self.config = config
        self.button_sum = []
        self.button = []
        self.std_button = []
        self.mean_button = []
        self.idx_file = idx_file
        self.idx_cbpm = idx_cbpm

    def raw_button_information(self):
        # extract individual buttons information
        # button 0 (or 3) is inner top
        # botton 1 (or 1) is inner bottom
        # bottom 2 (or 2) is outter bottom
        # button 3 (or 4)is outter top
        if (self.config.verbose > 0):
            print('\n   ---------------------')
            print('   | Raw button values |')
            print('   ---------------------\n')

        if self.config.analysis_type == 'pedestal':
            file_object = open('data/' + self.config.cbpm[self.idx_cbpm] + '_pedestal.txt', 'w')
            file_object.write('b0\tb1\tb2\tb3\n')

        if self.config.pedestal_correction:
            pedestal = []
            file_object = open('data/' + self.config.cbpm[self.idx_cbpm] + '_pedestal.txt', 'r')
            line_no = 0
            for line in file_object:
                if line_no == 1:
                    line = line.split()
                    for i in range(4):
                        pedestal.append(int(line[i]))
                line_no += 1
            print(pedestal)

        for i in range(4):

            if self.config.pedestal_correction:
                self.button.append(self.raw_button.data[:,i]-pedestal[i])
            else:
                self.button.append(self.raw_button.data[:,i])

            if (self.config.verbose > 0):
                print('   Button #', i, '--', end='')

#            tmp = [self.button[i][j] for j in range(4096)]
#            self.button[i] = np.array(tmp)

            if self.config.apply_boxcar_avg:
                self.button[i] = self.boxcar_averaging(np.array(self.button[i]), self.config.boxcar_avg)

            self.mean_button.append(np.mean(self.button[i]))
            self.std_button.append(np.std(self.button[i]))

            printout.print_stat(self.button[i])

            # plot raw button reading distribution
            boxcar_title = str(self.config.cbpm[self.idx_cbpm]) + ' button ' + str(i) + '\nboxcar ' + str(self.config.boxcar_avg)
            label = 'button' + str(i)
            fig, ax = plotting.create_figure(1, boxcar_title, 'Button raw readings [ADU]', '#', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            n_bins = int((max(self.button[i])-min(self.button[i]))/ 2*iqr(self.button[i], axis=None)/len(self.button[i])**(1/3))
            intensity, bin_edge, _ = plt.hist(self.button[i], bins=int(math.sqrt(len(self.button[i]))))
            try:
                bin_center = (bin_edge[:-1]+bin_edge[1:])/2.
                popt, pcov = curve_fit(util.double_gauss_func, bin_center, intensity,
                                   p0=[max(intensity), np.mean(self.button[i])+np.std(self.button[i])/2, np.std(self.button[i])/2,
                                       max(intensity)/2, np.mean(self.button[i])-np.std(self.button[i])/2, np.std(self.button[i])/2],
                                   bounds=(0, np.inf))
                plt.plot(bin_center, util.double_gauss_func(bin_center, *popt), color='red', linewidth=2.5)
                plt.plot(bin_center, util.gauss_func(bin_center, *popt[0:3]), ls='--', color='darkorange', linewidth=2)
                plt.plot(bin_center, util.gauss_func(bin_center, *popt[3:6]), ls='--', color='darkorange', linewidth=2)
                #print(math.sqrt(popt[2]**2+popt[5]**2), (popt[0]*popt[1]+popt[3]*popt[4])/(popt[0]+popt[3]))
            except:
                print('   RUNNING WARNING -- could not fit the centroid distribution')

            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + label + '_boxcar' + str(
                self.config.boxcar_avg) + '_rawADU.eps')
            plt.close()

            # plot raw button reading as a function of turn #
            fig, ax = plotting.create_figure(1, boxcar_title, 'Turn #', 'Button reading [ADU]', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            plt.plot([i for i in range(len(self.button[i]))], self.button[i])
            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + label + '_boxcar' + str(
                self.config.boxcar_avg) + '_rawADUtrend.eps')
            plt.close()

            # plot mean subtracted raw button reading as a function of turn #
            fig, ax = plotting.create_figure(1, boxcar_title, 'Turn #', 'Button reading [ADU]', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            plt.plot([i for i in range(len(self.button[i]))], self.button[i]-np.mean(self.button[i]))
            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + label + '_boxcar' + str(
                self.config.boxcar_avg) + '_rawADUtrendAvgSubtracted.eps')
            plt.close()

            self.perform_fft(np.array(self.button[i]), 'button ' + str(i), 'button_' + str(i))

            if self.config.analysis_type == 'pedestal':
                if self.config.verbose > 0:
                    print('   Saving pedestal information')
                file_object.write('%d\t' % (self.mean_button[i]))


        self.button_sum = self.button[0]+self.button[1]+self.button[2]+self.button[3]

        self.button_cross = ((self.button[0]+self.button[2]) - (self.button[1]+self.button[3]))/self.button_sum
        # plot button cross reading distribution
        fig, ax = plotting.create_figure(1, boxcar_title, 'Button cross reading [ADU]', '#',
                                         self.config.data_file_tag[self.idx_file], self.config.timestamp)
        plt.hist(self.button_cross, bins=int(math.sqrt(len(self.button_cross))))
        plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + 'Button_cross.eps')
        plt.close()

    @staticmethod
    def boxcar_averaging(data, averaging_window):
        
        n_steps = int(len(data)/averaging_window)
        boxcar_data = np.zeros((n_steps))
        for i in range(n_steps):
            boxcar_data[i] = np.mean(data[i*averaging_window:(i+1)*averaging_window], axis=0)

        return boxcar_data
            

    def perform_fft(self, data, title, label):

        fft = np.abs(np.fft.fft(data))
        fft = fft[range(1, int(len(fft)/2))] # exclude the 0 Hz bin and the mirror symmetry data points

        freq_step = 1/(len(data)*constants.ring_revolution_period*self.config.boxcar_avg) # keep sample period to revolution
        frequencies = [int(i)*freq_step/1000 for i in range(0, len(fft))] # in from Hz to kHz

        boxcar_title = title +'\nboxcar ' + str(self.config.boxcar_avg)
        fig, ax = plotting.create_figure(1, boxcar_title, 'Frequency [kHz]', 'FFT magnitude (log base 10)', self.config.data_file_tag[self.idx_file], self.config.timestamp)
        ax.set_yscale('log')
        ax.set_xlim(frequencies[0], frequencies[len(frequencies)-1])

        plt.grid(color='black', linestyle=':', linewidth=0.5, alpha=0.1)
        plt.grid(True)
        plt.plot(frequencies, fft)
        plt.savefig('results/'+ self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + label + '_boxcar' + str(self.config.boxcar_avg) + '_fft.eps')
        plt.close()
        

    def centroid(self):

        axis_label: List[str] = ['Vertical', 'Horizontal']
        plot_label: List[str] = ['vertical', 'horizontal']

        self.vertical_centroid = []
        self.horizontal_centroid = []

        for idx_centroid in range(2):

            boxcar_title = plot_label[idx_centroid] + ' centroid\nboxcar ' + str(self.config.boxcar_avg)

            if (self.config.verbose > 0 ):
                print('\n   ---------------------')
                print('   | ' + plot_label[idx_centroid] + ' centroid |')
                print('   ---------------------\n')

            if idx_centroid == 0:
                for i in range(len(self.button[0])):
                    self.vertical_centroid.append(self.config.ky*(self.button[0][i]+self.button[3][i]-(self.button[1][i]+self.button[2][i]))/self.button_sum[i])
                centroid = self.vertical_centroid
                self.mean_vertical_centroid = np.mean(self.vertical_centroid)
                self.std_vertical_centroid = np.std(self.vertical_centroid)
                self.perform_fft(centroid, plot_label[idx_centroid] + ' centroid', plot_label[idx_centroid] + '_centroid')

            elif idx_centroid == 1:
                for i in range(len(self.button[0])):
                    self.horizontal_centroid.append(self.config.kx*(self.button[2][i] + self.button[3][i]-(self.button[1][i] + self.button[0][i]))/self.button_sum[i])
                centroid = self.horizontal_centroid
                self.mean_horizontal_centroid = np.mean(self.vertical_centroid)
                self.std_horizontal_centroid = np.std(self.vertical_centroid)
                self.perform_fft(centroid, plot_label[idx_centroid] + ' centroid', plot_label[idx_centroid] + '_centroid')

            if (self.config.verbose > 0):
                printout.print_stat(centroid)

            # plot average subtracted raw button reading as a function of turn
            plotting.create_figure(1, boxcar_title, 'Turn #', axis_label[idx_centroid] + ' centroid [mm] (mean subtracted)', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            plt.plot([i for i in range(len(centroid))], centroid - np.mean(centroid))
            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + plot_label[idx_centroid] + 'Centroid_boxcar' +
                        str(self.config.boxcar_avg) + '_trendAvgSubtracted.eps')
            plt.close()

            # plot raw button reading as a function of turn with a linear fit
            _, ax = plotting.create_figure(1, boxcar_title, 'Turn #', axis_label[idx_centroid] + ' centroid [mm]', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            plt.plot([i for i in range(len(centroid))], centroid)
            try:
                fit = np.polyfit([i for i in range(len(centroid))], centroid, 1)
                fit_func = np.poly1d(fit)
                ax.text(0.025, 0.925, 'drift = {0:.5f}'.format(fit_func(len(centroid)-1)-fit_func(0)) + ' mm', transform=ax.transAxes, fontsize=15)
                plt.plot([i for i in range(len(centroid))], fit_func([i for i in range(len(centroid))]), c='red')
            except:
                print('   RUNNING WARNING -- could not fit the centroid trend')
            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + plot_label[idx_centroid] + 'Centroid_boxcar' +
                        str(self.config.boxcar_avg) + '_trend.eps')
            plt.close()

            # plot raw button reading distribution with a 3-Gaussian fit
            plotting.create_figure(1, boxcar_title, axis_label[idx_centroid] + ' centroid [mm]', '#', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            intensity, bin_edge, _ = plt.hist(centroid, bins=int(math.sqrt(len(centroid))))
            bin_center = (bin_edge[:-1] + bin_edge[1:]) / 2.

            try:
                popt, pcov = curve_fit(util.triple_gauss_func, bin_center, intensity, maxfev = 5000,
                                   p0=[max(intensity), np.mean(centroid), np.std(centroid),
                                       max(intensity), np.mean(centroid) + np.std(centroid)/2, np.std(centroid)/2,
                                       max(intensity), np.mean(centroid) - np.std(centroid)/2, np.std(centroid)/2],
                                   bounds=([0, -np.inf, 0, 0, -np.inf, 0, 0, -np.inf, 0,], np.inf))
                plt.plot(bin_center, util.triple_gauss_func(bin_center, *popt), color='red', linewidth=2.5)
                plt.plot(bin_center, util.gauss_func(bin_center, *popt[0:3]), ls='--', color='darkorange', linewidth=2)
                plt.plot(bin_center, util.gauss_func(bin_center, *popt[3:6]), ls='--', color='darkorange', linewidth=2)
                plt.plot(bin_center, util.gauss_func(bin_center, *popt[6:9]), ls='--', color='darkorange', linewidth=2)
            except:
                print('   RUNNING WARNING -- could not fit the centroid distribution')

            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + plot_label[idx_centroid] + 'Centroid_boxcar' +
                        str(self.config.boxcar_avg) + '_dist.eps')
            plt.close()