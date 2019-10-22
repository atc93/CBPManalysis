import matplotlib.pyplot as plt
import math

import src.plotting as plotting

def single_cbpm_vs_runo(cbpm, idx_cbpm):

    run_no = []
    data = []
    data.append([])
    data.append([])
    data.append([])
    data.append([])
    vertical_mean = []
    vertical_std = []
    horizontal_mean = []
    horizontal_std = []

    for i in range(len(cbpm[idx_cbpm])):
        run_no.append(cbpm[idx_cbpm][i].config.data_file[i][9:len(cbpm[idx_cbpm][i].config.data_file[i]) - 4])
        data[0].append(cbpm[idx_cbpm][i].mean_vertical_centroid)
        data[1].append(cbpm[idx_cbpm][i].mean_horizontal_centroid)
        data[2].append(cbpm[idx_cbpm][i].std_vertical_centroid)
        data[2].append(cbpm[idx_cbpm][i].std_horizontal_centroid)
        vertical_mean.append(cbpm[idx_cbpm][i].mean_vertical_centroid)
        horizontal_mean.append(cbpm[idx_cbpm][i].mean_horizontal_centroid)
        vertical_std.append(cbpm[idx_cbpm][i].std_vertical_centroid)
        horizontal_std.append(cbpm[idx_cbpm][i].std_horizontal_centroid)

    button_mean = []
    button_std = []
    for i in range(4):
        button_mean.append([])
        button_std.append([])
        for j in range(len(cbpm[idx_cbpm])):
            button_mean[i].append(cbpm[idx_cbpm][j].mean_button[i])
            button_std[i].append(cbpm[idx_cbpm][j].std_button[i])

    # plot button mean versus run #
    for i in range(4):
        fig, ax = plotting.create_figure(1, cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '\n', 'Run #', 'Mean button readings [ADU] (w/ SE)', '', '')
        plt.xticks(rotation=45)
        plt.errorbar(run_no, button_mean[i], yerr=[x / math.sqrt(cbpm[idx_cbpm][0].config.n_turns) for x in button_std[i]], marker='o', ms=5, ls='')
        plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'Button' + str(i) + '_mean_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')
        plt.close()

    # plot button std versus run #
    for i in range(4):
        fig, ax = plotting.create_figure(1, cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '\n', 'Run #', 'Mean button std [ADU] (w/ SE)', '', '')
        plt.xticks(rotation=45)
        plt.errorbar(run_no, button_std[i], yerr=[x / math.sqrt(cbpm[idx_cbpm][0].config.n_turns) for x in button_std[i]], marker='o', ms=5, ls='')
        plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'Button' + str(i) + '_std_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')
        plt.close()


    for i in range(4):

        fig, ax = plotting.create_figure(1, cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '\n', 'Run #', 'Vertical centroid [mm] (w/ SE)', '', '')
        plt.xticks(rotation=45)

        if i == 0: # plot vertical centroid versus run #
            plt.errorbar(run_no, vertical_mean, yerr=[x / math.sqrt(cbpm[idx_cbpm][0].config.n_turns) for x in vertical_std], marker='o', ms=5, ls='')
            plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'VerticalCentroid_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')
        if i == 1: # plot vertical standard deviation versus run #
            plt.errorbar(run_no, vertical_std, yerr=[x / math.sqrt(2 * cbpm[idx_cbpm][0].config.n_turns - 2) for x in vertical_std], marker='o', ms=5, ls='')
            plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'VerticalSTD_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')

        plt.close()

    # plot horizontal centroid versus run #
    fig, ax = plotting.create_figure(1, cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '\n', 'Run #', 'Horizontal centroid [mm] (w/ SE)', '', '')
    plt.xticks(rotation=45)
    plt.errorbar(run_no, horizontal_mean, yerr=[x / math.sqrt(cbpm[idx_cbpm][0].config.n_turns) for x in horizontal_std], marker='o', ms=5, ls='')
    plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'Horizontalentroid_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')
    plt.close()

    # plot horizontal standard deviation versus run #
    fig, ax = plotting.create_figure(1, cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '\n', 'Run #', 'Horizontal standard deviation [mm] (w/ SE)', '', '')
    plt.xticks(rotation=45)
    plt.errorbar(run_no, horizontal_std, yerr=[x / math.sqrt(2*cbpm[idx_cbpm][0].config.n_turns-2) for x in horizontal_std], marker='o', ms=5, ls='')
    plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'HorizontalSTD_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')
    plt.close()


def results_to_text_file(cbpm):

    #print(cbpm[0][0].config.n_data_file)

    file_object = open('results/results.txt', 'w')
    for i in range(cbpm[0][0].config.n_data_file):
        file_object.write(cbpm[0][0].config.data_file[i])
        file_object.write('\n\t<x>\t\tsig_x\t\t<y>\t\tsig_y')
        for j in range(cbpm[0][i].config.n_cbpm):
            file_object.write('\n%s\t%f\t%f\t%f\t%f' % (cbpm[j][i].config.cbpm[j],
                                                    cbpm[j][i].mean_horizontal_centroid,
                                                    cbpm[j][i].std_horizontal_centroid,
                                                    cbpm[j][i].mean_vertical_centroid,
                                                    cbpm[j][i].std_vertical_centroid))

        if cbpm[0][0].config.analysis_type == 'triplet':
            average_resolution_x = math.sqrt((cbpm[0][i].std_horizontal_centroid**2
                                              +cbpm[1][i].std_horizontal_centroid**2
                                              +cbpm[2][i].std_horizontal_centroid**2)/3)
            average_resolution_y = math.sqrt((cbpm[0][i].std_vertical_centroid**2
                                              +cbpm[1][i].std_vertical_centroid**2
                                              +cbpm[2][i].std_vertical_centroid**2)/3)

            file_object.write('\naverage\t\t\t%f\t\t\t%f' % (average_resolution_x, average_resolution_y))
            file_object.write('\ntriplet\t\t\t%f\t\t\t%f' % (cbpm[0][i].triplet_resolution[1], cbpm[0][i].triplet_resolution[0]))

        file_object.write('\n\n')