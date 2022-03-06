import numpy as np
import matplotlib.pyplot as plt
import columnplots as clp
import glob

def obtain_avg_data(path, pattern="simu_*.vac.txt"):
    filenames = glob.glob("%s/%s" %(path, pattern))
    print("Averaging over %d trajectories under %s" %(len(filenames), path))
    data = np.loadtxt(filenames[0])
    for filename in filenames[1:]:
        data += np.loadtxt(filename)
    data /= float(len(filenames))
    return data

def obtain_IR(path):
    data = obtain_avg_data(path=path, pattern="simu_*.dac.txt")
    freq = data[:,5]
    sp = (data[:,6] + data[:,7]) / 2e28
    # truncate spectrum to a small window
    #df = freq[1] - freq[0]
    #nstart, nend = int(2500/df), int(4500/df)
    #freq, sp = freq[nstart:nend], sp[nstart:nend]
    sp /= np.max(sp)
    return freq, sp

def subfigure(ax, path_incav, path_outcav, cavfreq=3550.0, showlegend=True, xlabel=None):
    freq_in, sp_in = obtain_IR(path=path_incav)
    freq_out, sp_out = obtain_IR(path=path_outcav)

    colors = [clp.black, clp.red]
    labels = ["cavity off", "cavity on"]
    xs = [freq_out, freq_in]
    ys = [sp_out, sp_in]
    clp.plotone(xs, ys, ax, colors=colors, labels=labels, lw=1,
        xlim=[3000, 4400], showlegend=showlegend,
        ylabel="$n(\omega)\\alpha(\omega)$ [arb. units]",
        xlabel=xlabel)
    ax.axvline(x=cavfreq, color=clp.sky_blue, ls="--")

fig, axes = clp.initialize(2, 1, width=4.3, height=4.3*0.618*1.5, sharex=True, sharey=True,
    LaTeX=True, return_fig_args=True, fontsize=12, labelsize=12,
    labelthem=True, labelthemPosition=[0.1, 0.95])

path_incav = "../h2o_incav_classical/IR_calculation/Freq_3550/"
path_outcav = "../h2o_incav_classical/IR_calculation/Freq_outcav/"
subfigure(axes[0], path_incav=path_incav, path_outcav=path_outcav, cavfreq=3550)

axes[0].legend(loc="center left", fancybox=True, edgecolor="inherit", facecolor="inherit")

path_incav = "../h2o_incav_quantum/IR_calculation/Freq_3450/"
path_outcav = "../h2o_incav_quantum/IR_calculation/Freq_outcav/"
subfigure(axes[1], path_incav=path_incav, path_outcav=path_outcav, cavfreq=3450,
    showlegend=False, xlabel="frequency [cm$^{-1}$]")

axes[0].text(0.12, 0.87, "classical", fontsize=12, transform=axes[0].transAxes)
axes[1].text(0.12, 0.87, "quantum", fontsize=12, transform=axes[1].transAxes)

clp.adjust(tight_layout=True, savefile="IR.pdf")
