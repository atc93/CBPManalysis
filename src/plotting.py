import matplotlib.pyplot as plt

def create_figure(fig_id, title, xaxis_label, yaxis_label, run_label, timestamp):

    # rcParams need to be changed before calling the rest
    plt.rcParams['figure.figsize'] = [9, 6]
    plt.rcParams.update({'font.size': 17})

    fig = plt.figure(fig_id,)

    ax = fig.add_subplot(111)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    ax.tick_params(axis="y",direction="in", labelleft=True)
    ax.tick_params(axis="x",direction="in", labelleft=True)
    ax.text(-0.215, 0.9725, title, transform=ax.transAxes, fontsize=15)
    run_label = run_label + ' ' + timestamp
    ax.text(0.55, 1.016, run_label, transform=ax.transAxes, fontsize=15)


    plt.subplots_adjust(left=0.175, bottom=0.125, right=0.975, top=0.95, wspace=0, hspace=0)
    plt.xlabel(xaxis_label)
    plt.ylabel(yaxis_label)

    return fig, ax