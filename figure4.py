# Importing necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pygam import LinearGAM, s
from matplotlib.ticker import FormatStrFormatter

# Reading the data
data = pd.read_excel('fig2.xlsx')

# Filtering dataRate
data = data[data['dataRate'] >= 2.5]

# Defining attributes and corresponding columns and labels
attributes_labels = [
    ("BLA", "Black Demographic %"),
    ("MIC", "Median Income"),
    ("EDU", "Low-Edu Demographic %"),
    ("NOC", "Childless Households %"),
    ("AGE", "Elderly Demographic %"),
    ("IMM", "Immigrant Demographic %")
]

# Creating subplots
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 35), gridspec_kw={'hspace': 0.4, 'wspace': 0.3})

labels = ['a', 'b', 'c', 'd', 'e', 'f']

# Setting style and colors
scatter_kws = {'s': 10, 'color': '#808080'}
line_kws = {'color': 'black'}

for i, (column, ylabel) in enumerate(attributes_labels):
    ax = axes[i // 2, i % 2]

    # Adding labels to the subplots
    ax.text(-0.23, 1.05, labels[i], transform=ax.transAxes, fontsize=10, va='top', ha='left', weight='bold')

    # Creating bins for RateHasCooling
    bins = np.arange(0, 1.1, 0.1)
    data['RateHasCooling_bins'] = pd.cut(data['RateHasCooling'], bins=bins, right=False,
                                         labels=(bins[:-1] + bins[1:]) / 2)

    # Calculating the proportion or average for each attribute
    if column == 'MIC':
        # Calculate the average income for each bin
        grouped_data = data.groupby('RateHasCooling_bins').apply(
            lambda x: pd.Series({
                'Total_Income': x['MedianIncome'].sum(),
                'Count': len(x)
            })).reset_index()
        grouped_data['AverageIncome'] = grouped_data['Total_Income'] / grouped_data['Count']
        y = grouped_data['AverageIncome'].values
    elif column == 'NOC':
        # Calculate the total number of households without children in each bin
        grouped_data = data.groupby('RateHasCooling_bins').apply(
            lambda x: pd.Series({
                'NoChildren_Total': (x['NoChildren'] * x['hushu'] / 100).sum(),
                'Household_Total': x['hushu'].sum()
            })).reset_index()
        grouped_data['NoChildren_Proportion'] = grouped_data['NoChildren_Total'] / grouped_data['Household_Total']
        y = grouped_data['NoChildren_Proportion'].values
    else:
        # Calculate the proportion of target population for other attributes
        grouped_data = data.groupby('RateHasCooling_bins').apply(
            lambda x: pd.Series({
                'Target_Total': x[column].sum(),
                'Population_Total': x['POP'].sum()
            })).reset_index()
        grouped_data['Proportion'] = grouped_data['Target_Total'] / grouped_data['Population_Total']
        y = grouped_data['Proportion'].values

    # Fitting a GAM model
    X = grouped_data['RateHasCooling_bins'].astype(float).values
    gam = LinearGAM(s(0, n_splines=9)).fit(X, y)

    # Plotting the GAM model and confidence intervals
    XX = np.linspace(X.min(), X.max(), 1000)
    ax.plot(XX, gam.predict(XX), color=line_kws['color'])
    confidence_width = 0.95
    ci_lower, ci_upper = gam.confidence_intervals(XX, width=confidence_width).T
    ax.fill_between(XX, ci_lower, ci_upper, color='lightgray', alpha=0.5)

    # Plotting original data points
    sns.scatterplot(x='RateHasCooling_bins', y=y, data=grouped_data, ax=ax, **scatter_kws)

    # Setting labels and title
    ax.set_xlabel('Prevalence of RCI Across Census Tracts', fontsize=8)
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.set_ylabel(ylabel, fontsize=8, labelpad=20)
    ax.yaxis.set_label_coords(-0.13, 0.5)

plt.tight_layout(pad=3.0)
plt.subplots_adjust(top=0.95, bottom=0.1, left=0.1, right=0.95, hspace=0.8, wspace=0.8)

plt.show()
