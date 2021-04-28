import argparse
import json
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib as mpl


#parser = argparse.ArgumentParser(description='Plot statistics.')
#parser.add_argument('input', nargs='+', type=Path, help='Input files with statistics.')
#options = parser.parse_args()

plt.figure(figsize=(15, 10))
sns.set_palette("deep")

humanoid = [7, 17, 11, 2, 9, 8]
qlearning = [8, 15, 9, 2, 10, 8]
#concat = pd.DataFrame()
#for result_file in options.input: 
#    app = str(result_file).split('/')[-1]
#    print(app)
#    with open(result_file) as f:
#        statistics = json.load(f)
#
#    df = pd.DataFrame(statistics).T
#    df['time'] = df.index.map(lambda x: int(x.split('/')[-1].split('_')[-2]))
#    df['strategy'] = df.index.map(lambda x: '_'.join(x.split('/')[-1].split('_')[:-2]))
#
#    df = df[(df['time'] == 12) & (df['strategy'].isin(['epsilon_greedy', 'humanoid']))]
#
#    df['compare'] = df['strategy'].map({'humanoid': #'Humanoid'}).fillna('Qlearning')
#    df['app'] = app
#   
#    concat = pd.concat([concat, df])

plt.plot(qlearning, 's:', markersize=15, label='Qlearning')
plt.plot(humanoid, 's:', markersize=15, label='Humanoid')

plt.xticks(range(6), ['APPLEBEES', 'BOOKING', 'EBAY', 'FACEAPP', 'NYTIMES', 'WSJ'])
#sns.boxplot(x='app', y='states', hue='compare', data=concat)
#sns.lineplot(x='app', y='states', hue='compare', data=concat)

plt.legend(loc=9, prop={'size': 20})
plt.title('Сравнение с Humanoid', fontsize=40)
plt.ylabel('Уникальные Активности', fontsize=30)
plt.xlabel('', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.savefig('activities_humanoid.jpg')
