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


plt.figure(figsize=(25, 10))
sns.set_palette("deep")
sns.set(style="ticks")

concat = pd.DataFrame()
for result_file in options.input: 
    app = str(result_file).split('/')[-1]
    print(app)
    with open(result_file) as f:
        statistics = json.load(f)

    df = pd.DataFrame(statistics).T
    df['time'] = df.index.map(lambda x: int(x.split('/')[-1].split('_')[-2]))
    df['strategy'] = df.index.map(lambda x: '_'.join(x.split('/')[-1].split('_')[:-2]))
    df = df[df['strategy'].isin(['abstract_states', 'dqn'])]
    df['app'] = app
   
    concat = pd.concat([concat, df])

bp = sns.boxplot(x='app', y='activities', hue='strategy', data=concat)
bp.legend(title='Стратегия', fontsize=30, title_fontsize=30, shadow=True)
bp.legend_.texts[0].set_text('Абстрактные состояния')
bp.legend_.texts[1].set_text('Нейронная сеть')

plt.title('Независимые от приложения стратегии', fontsize=40)
plt.ylabel('Уникальные Активности', fontsize=35)
plt.xlabel('Приложения', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.grid()
plt.savefig('activities_app_free.jpg')
