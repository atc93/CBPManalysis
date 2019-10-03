import matplotlib.pyplot as plt
import math

import src.plotting as plotting

def single_cbpm(cbpm, idx_cbpm):

    run_no = []
    vertical_mean = []
    vertical_std = []
    horizontal_mean = []
    horizontal_std = []

    for i in range(len(cbpm[idx_cbpm])):
        run_no.append(cbpm[idx_cbpm][i].config.data_file[i][9:len(cbpm[idx_cbpm][i].config.data_file[i]) - 4])
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
        fig, ax = plotting.create_figure(cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '\n', 'Run #', 'Mean button readings [ADU] (w/ SE)', '', '')
        plt.xticks(rotation=45)
        plt.errorbar(run_no, button_mean[i], yerr=[x / math.sqrt(cbpm[idx_cbpm][0].config.n_turns) for x in button_std[i]], marker='o', ms=5, ls='')
        plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'Button' + str(i) + '_mean_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')
        plt.close()

    # plot button std versus run #
    for i in range(4):
        fig, ax = plotting.create_figure(cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '\n', 'Run #', 'Mean button std [ADU] (w/ SE)', '', '')
        plt.xticks(rotation=45)
        plt.errorbar(run_no, button_std[i], yerr=[x / math.sqrt(cbpm[idx_cbpm][0].config.n_turns) for x in button_std[i]], marker='o', ms=5, ls='')
        plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'Button' + str(i) + '_std_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')
        plt.close()

    # plot vertical centroid versus run #
    fig, ax = plotting.create_figure(cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '\n', 'Run #', 'Vertical centroid [mm] (w/ SE)', '', '')
    plt.xticks(rotation=45)
    plt.errorbar(run_no, vertical_mean, yerr=[x / math.sqrt(cbpm[idx_cbpm][0].config.n_turns) for x in vertical_std], marker='o', ms=5, ls='')
    plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'VerticalCentroid_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')
    plt.close()

    # plot vertical standard deviation versus run #
    fig, ax = plotting.create_figure(cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '\n', 'Run #', 'Vertical standard deviation [mm] (w/ SE)', '', '')
    plt.xticks(rotation=45)
    plt.errorbar(run_no, vertical_std, yerr=[x / math.sqrt(2*cbpm[idx_cbpm][0].config.n_turns-2) for x in vertical_std], marker='o', ms=5, ls='')
    plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'VerticalSTD_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')
    plt.close()

    # plot horizontal centroid versus run #
    fig, ax = plotting.create_figure(cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '\n', 'Run #', 'Horizontal centroid [mm] (w/ SE)', '', '')
    plt.xticks(rotation=45)
    plt.errorbar(run_no, horizontal_mean, yerr=[x / math.sqrt(cbpm[idx_cbpm][0].config.n_turns) for x in horizontal_std], marker='o', ms=5, ls='')
    plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'Horizontalentroid_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')
    plt.close()

    # plot horizontal standard deviation versus run #
    fig, ax = plotting.create_figure(cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '\n', 'Run #', 'Horizontal standard deviation [mm] (w/ SE)', '', '')
    plt.xticks(rotation=45)
    plt.errorbar(run_no, horizontal_std, yerr=[x / math.sqrt(2*cbpm[idx_cbpm][0].config.n_turns-2) for x in horizontal_std], marker='o', ms=5, ls='')
    plt.savefig('results/' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '/' + 'HorizontalSTD_' + cbpm[idx_cbpm][0].config.cbpm[idx_cbpm] + '.eps')
    plt.close()


