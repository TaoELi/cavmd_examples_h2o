import numpy as np
import matplotlib.pyplot as plt
import columnplots as clp
import glob

simulation_box_length_au = 35.233
Kelvin2AU = 315777.09
kT = 300.0 / Kelvin2AU

def translate_data(filename):
    data = np.loadtxt(filename)
    # record the mean/meansquare of dipole moments for each 20 ps
    idx, mux, muy, muz = data[:,0], data[:,1], data[:,2], data[:,3]
    n = len(idx)
    t_ns = np.linspace(0, (n-1)*20, n) * 1e-3
    # calculate the moving average
    mux_ma, muy_ma, muz_ma = np.zeros(n), np.zeros(n), np.zeros(n)
    for i in range(n):
        mux_ma[i] = np.mean(mux[0:i+1])
        muy_ma[i] = np.mean(muy[0:i+1])
        muz_ma[i] = np.mean(muz[0:i+1])
    return t_ns, mux_ma, muy_ma, muz_ma

def prepare_plotting_data(path):
    f_mu_average = path + "/mean_dipole.txt"
    f_musq_average = path + "/meansquare_dipole.txt"
    t_ns, mux_ma, muy_ma, muz_ma = translate_data(filename=f_mu_average)
    t_ns, musqx_ma, musqy_ma, musqz_ma = translate_data(filename=f_musq_average)
    musq_avg = musqx_ma + musqy_ma + musqz_ma
    muavg_sq = mux_ma**2 + muy_ma**2 + muz_ma**2
    dmu2 = musq_avg - muavg_sq # in atomic units
    # calculate dielectric constant from <M^2> - <M>^2
    '''
    epsilon = 1 + 4pi/3Vk_bT(<M^2> - <M>^2)
    '''
    V = simulation_box_length_au**3
    epsilon = 1.0 + np.pi * 4.0 / 3.0 / V / kT * dmu2
    # we further calculate the mean value and std of epsilon from 10 to 20 ns
    epsilon_convg = epsilon[int(len(epsilon))//2:]
    mean_epsilon = np.mean(epsilon_convg)
    std_epsilon = np.std(epsilon_convg)
    print("for path = %s" %path)
    print("mean_epsilon = %.3f and std_epsilon %.3f" %(mean_epsilon, std_epsilon))
    return t_ns, epsilon

def subfigure(ax, path_incav, path_outcav, showlegend=True, xlabel=None):
    t_ns_in, y_in = prepare_plotting_data(path=path_incav)
    t_ns_out, y_out = prepare_plotting_data(path=path_outcav)
    xs = [t_ns_out, t_ns_in]
    ys = [y_out, y_in]
    labels = ["cavity off", "cavity on"]
    colors = [clp.black, clp.red]
    clp.plotone(xs, ys, ax, colors=colors, labels=labels, lw=1,
        showlegend=showlegend,
        ylim=[45, 70], xlim=[0,20], ylabel="$\epsilon_r$", xlabel=xlabel)

fig, axes = clp.initialize(2, 1, width=4.3, height=4.3*0.618*1.5, sharex=True, sharey=True,
    LaTeX=True, return_fig_args=True, fontsize=12, labelsize=12,
    labelthem=True, labelthemPosition=[0.1, 0.95])

path_incav = "../h2o_incav_classical/dielectric_constant/Freq_3550/"
path_outcav = "../h2o_incav_classical/dielectric_constant/Freq_outcav/"
subfigure(axes[0], path_incav=path_incav, path_outcav=path_outcav)

path_incav = "../h2o_incav_quantum/dielectric_constant/Freq_3450/"
path_outcav = "../h2o_incav_quantum/dielectric_constant/Freq_outcav/"
subfigure(axes[1], path_incav=path_incav, path_outcav=path_outcav,
    showlegend=False, xlabel="time [ns]")

axes[0].text(0.12, 0.87, "classical", fontsize=12, transform=axes[0].transAxes)
axes[1].text(0.12, 0.87, "quantum", fontsize=12, transform=axes[1].transAxes)

clp.adjust(tight_layout=True, savefile="dielectric.pdf")
