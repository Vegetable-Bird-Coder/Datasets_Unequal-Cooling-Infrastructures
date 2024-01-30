import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data = pd.read_excel('fig3.xlsx')

# Check if 'dataRate' column exists and filter accordingly
if 'dataRate' in data.columns:
    data = data[data['dataRate'] >= 2.5]

# Define the category edges based on the specified requirements
cooling_edges = [0, 0.6, 0.9, 1.0]  # Edges for the 'RateHasCooling' categories
temperature_edges = data['mean59'].quantile([0.2, 0.8]).values
temperature_edges = [data['mean59'].min(), temperature_edges[0], temperature_edges[1], data['mean59'].max()]

# Create a single scatter plot
fig, ax = plt.subplots(figsize=(10, 8))

# Plot all the data points with 'x' markers
ax.scatter(data['RateHasCooling'], data['mean59'], alpha=0.5, s=10, marker='x')

# Draw vertical and horizontal lines to divide the plot into categories
# for edge in cooling_edges[1:-1]:
#     ax.axvline(x=edge, color='grey', linestyle='--')
# for edge in temperature_edges[1:-1]:
#     ax.axhline(y=edge, color='grey', linestyle='--', lw=0.3)

# Set the axis labels
ax.set_xlabel('The Prevalence of RCI Across Census Tracts')
ax.set_ylabel('Summer Average temperature (May-September in 2021)')

# Fit a polynomial trend line
coefficients = np.polyfit(data['RateHasCooling'], data['mean59'], deg=2)  # 'deg' specifies the degree of the polynomial
polynomial = np.poly1d(coefficients)
x_poly = np.linspace(0, 1, 100)  # Generate 100 x values between 0 and 1 for plotting
y_poly = polynomial(x_poly)  # Calculate the y values from the polynomial


ax.plot(x_poly, y_poly, color='red', linestyle='-', lw=1.3, label='Trend Line')


# Set the axis limits to include all data points and the [0, 1] range for RateHasCooling
ax.set_xlim(0, 1)
ax.set_ylim(data['mean59'].min(), data['mean59'].max())

# Move the legend to the upper left corner
ax.legend(loc='upper left')

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()
