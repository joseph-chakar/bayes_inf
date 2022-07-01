import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def bpe_results(bpe, param_ranges, params, labels, units, top=5, posterior=False):
    nb_params = len(param_ranges)

    fig = plt.figure(constrained_layout=True)
    gs = GridSpec(nb_params, nb_params, figure=fig)
    # plot the posterior/error distribution of each parameter
    for i, param_range in enumerate(param_ranges):
        ax = fig.add_subplot(gs[i, i])
        if posterior == True:
            if i == 0:
                print('Likelihood-based results')
                best_comb = bpe['Posterior'].idxmax()
                print('Best parameter combination:' + str(best_comb))

                top_predictions = bpe.sort_values(by=['Posterior'], ascending=False).head(top)
                print('Top 5 predictions:')
                print(top_predictions[['Posterior']])

            ax.plot(param_range, [bpe.iloc[bpe.index.get_loc_level(param_value, level=params[i])[0]]['Posterior'].sum() for param_value in param_range])
            ax.scatter(best_comb[i], bpe.iloc[bpe.index.get_loc_level(best_comb[i], level=params[i])[0]]['Posterior'].sum(), s=80, marker='*', c='yellow', linewidths=0.5, edgecolors= 'black')
            ax.yaxis.tick_right()
            ax.yaxis.set_label_position('right')
            ax.set_ylabel('Probability')
            ax.set_ylim([0, 1])

        else:
            if i == 0:
                print('Error-based results')
                best_comb = bpe['Error'].idxmin()
                print('Best parameter combination:' + str(best_comb))

                top_predictions = bpe.sort_values(by=['Error'], ascending=True).head(top)
                print('Top 5 predictions:')
                print(top_predictions[['Error']])

            ax.plot(param_range, [bpe.iloc[bpe.index.get_loc_level(param_value, level=params[i])[0]]['Error'].min() for param_value in param_range])
            ax.scatter(best_comb[i], bpe.iloc[bpe.index.get_loc_level(best_comb[i], level=params[i])[0]]['Error'].min(), s=80, marker='*', c='yellow', linewidths=0.5, edgecolors= 'black')
            ax.yaxis.set_label_position('right')
            ax.set_ylabel('Minimum Error')

        if i==nb_params-1:
            ax.set_xlabel(labels[i])

    # plot the relationship between any two parameters
    for cb in list(itertools.combinations(range(nb_params), 2)):
        x, y = cb[0], cb[1]
        ax = fig.add_subplot(gs[y, x])
        coupled_ranges = [param_ranges[x], param_ranges[y]]
        levels = [params[x], params[y]]
        coupled_combs = list(itertools.product(*coupled_ranges))
        if x==0:
            ax.set_ylabel(f'{labels[y]} [{units[y]}]')
        if y==nb_params-1:
            ax.set_xlabel(f'{labels[x]} [{units[x]}]')
        x = [coupled_comb[0] for coupled_comb in coupled_combs]
        y = [coupled_comb[1] for coupled_comb in coupled_combs]

        if posterior == True:
            sc = ax.scatter(x, y, c=[bpe.iloc[bpe.index.get_loc_level(coupled_comb, level=levels)[0]]['Posterior'].sum() for coupled_comb in coupled_combs], cmap='Blues')

        else:
            sc = ax.scatter(x, y, c=[bpe.iloc[bpe.index.get_loc_level(coupled_comb, level=levels)[0]]['Error'].min() for coupled_comb in coupled_combs], cmap='Blues_r')

    return best_comb, top_predictions
