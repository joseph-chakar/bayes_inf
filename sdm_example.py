from utils import *
import itertools
import pandas as pd
import numpy as np
from pvlib import pvsystem, singlediode
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_percentage_error as mape
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

''' This example shows how to extract the Single-Diode Model (SDM) parameters (specifically, the two resistances) from "observed" IV curve data. 
In this case, the "observed" data consists of one IV curve that is simulated using pre-defined SDM parameters, just to demonstrate that the approach works! '''

# 1. Get (generate in this case) the "observed" data
IL_obs, Io_obs, Rs_obs, Rsh_obs, a_obs = 11.26, 4.72e-11, 0.18, 69.97, 1.56

iv_obs = pvsystem.singlediode(photocurrent=IL_obs, saturation_current=Io_obs, resistance_series=Rs_obs, resistance_shunt=Rsh_obs, nNsVth=a_obs, ivcurve_pnts=100)
v_obs, i_obs = iv_obs['v'], iv_obs['i']

fig, ax = plt.subplots()
ax.plot(v_obs, i_obs)
plt.xlabel('Voltage [V]')
plt.ylabel('Current [A]')

# 2. Define the fitting parameters
params = ['Rs', 'Rsh']
labels = ['R$_s$', 'R$_{sh}$']
units = ['Ω', 'Ω']

Rs_range = np.arange(0.2, 0.4, 0.01)
Rsh_range = np.arange(400, 600, 1)

param_ranges = [Rs_range, Rsh_range]

combinations = list(itertools.product(*param_ranges)) #get all the possible parameter combinations

# define the Prior distribution and compute the Likelihood
bpe = pd.DataFrame(index=pd.MultiIndex.from_tuples(combinations, names=params))
bpe['Prior'] = 1/len(bpe)
bpe['Error'] = np.nan

for cb in combinations:
    i_model = singlediode.bishop88_i_from_v(v_obs, photocurrent=IL_ref, saturation_current=Io_ref, resistance_series=cb[0], resistance_shunt=cb[1], nNsVth=a_ref)

    # bpe.loc[cb, 'Error'] = mse(i_obs.round(2), i_model.round(2))
    bpe.loc[cb, 'Error'] = mape(i_obs.round(2), i_model.round(2))*100

# calculate the posterior distribution
bpe['Likelihood'] = np.exp(-bpe['Error'])
bpe['Posterior'] = bpe['Prior']*bpe['Likelihood']/np.sum(bpe['Prior']*bpe['Likelihood'])

best_comb_err, top_predictions_err = bpe_results(bpe, param_ranges, params, labels, units, top=5, posterior=False)

best_comb_lkl, top_predictions_lkl = bpe_results(bpe, param_ranges, params, labels, units, top=5, posterior=True)

fig, ax = plt.subplots()
ax.plot(v_obs, i_obs, label='Observed Data')
for i, top in enumerate(top_predictions_err.index[:5]):
    i_best = singlediode.bishop88_i_from_v(v_obs, photocurrent=IL_ref, saturation_current=Io_ref, resistance_series=top[0], resistance_shunt=top[1], nNsVth=a_ref)
    ax.plot(v_obs, i_best, label=f'BPE Fit #{i+1}')
plt.legend()

