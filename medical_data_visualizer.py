import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data from CSV file
data = pd.read_csv('medical_examination.csv')

# Create 'overweight' column based on BMI
data['overweight'] = (data['weight'] / ((data['height'] / 100) ** 2) > 25).astype(int)
data['cholesterol'] = (data['cholesterol'] > 1).astype(int)
data['gluc'] = (data['gluc'] > 1).astype(int)
def draw_cat_plot():





    datac = pd.melt(data, id_vars=['cardio'], 
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    



    # Group and reorganize data
    datac = pd.DataFrame(datac.groupby(['cardio', 'variable', 'value'])['value'].count()).rename(columns={'value': 'total'}).reset_index()
    fig = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=datac, kind='bar')
    fig.set_axis_labels("variable", "total")
    fig.set_titles("Cardio - {col_name}")
    
    # Adjust the figure for output
    fig = fig.fig
    fig.savefig('catplot.png')
    return fig



#  Function to draw the heat map
def draw_heat_map():
    # Filter data
    data_heat = data[
        (data['ap_lo'] <= data['ap_hi']) & 
        (data['height'] >= data['height'].quantile(0.025)) &
        (data['height'] <= data['height'].quantile(0.975)) &
        (data['weight'] >= data['weight'].quantile(0.025)) &
        (data['weight'] <= data['weight'].quantile(0.975))
    ]
    corr = data_heat.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # 14. Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 9))

    # 15. Draw the heat map
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', square=True, linewidths=.5, ax=ax, cbar_kws={"shrink": .5})
    fig.savefig('heatmap.png')
    return fig