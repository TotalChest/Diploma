import argparse
import json
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib as mpl


parser = argparse.ArgumentParser(description='Plot statistics.')
parser.add_argument('input', nargs='+', type=Path, help='Input files with statistics.')
options = parser.parse_args()


plt.figure(figsize=(15, 10))
sns.set_palette("deep")

concat = pd.DataFrame()
for result_file in options.input: 
    app = str(result_file).split('/')[-1]
    print(app)
    with open(result_file) as f:
        statistics = json.load(f)

    df = pd.DataFrame(statistics).T
    df['time'] = df.index.map(lambda x: int(x.split('/')[-1].split('_')[-2]))
    df['strategy'] = df.index.map(lambda x: '_'.join(x.split('/')[-1].split('_')[:-2]))
    df = df[df['strategy'].isin(['events_count', 'possible_events', 'reverse_possible_events', 'tree_edit_distance'])]
    df['app'] = app
   
    concat = pd.concat([concat, df])

sns.boxplot(x='app', y='states', hue='strategy', data=concat)
plt.legend(prop={'size': 20})
plt.title('Зависимые от приложения стратегии', fontsize=40)
plt.ylabel('Уникальные состояния', fontsize=30)
plt.xlabel('', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.savefig('states_app_based.jpg')
