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


plt.figure(figsize=(25, 15))
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
    df = df[df['strategy'].isin(['events_count', 'possible_events', 'reverse_possible_events', 'tree_edit_distance'])]
    df['app'] = app
   
    concat = pd.concat([concat, df])

bp = sns.boxplot(x='app', y='states', hue='strategy', data=concat)
bp.legend(title='Стратегия', fontsize=30, title_fontsize=30, shadow=True)
bp.legend_.texts[0].set_text('Обратная частота нажатий')
bp.legend_.texts[1].set_text('Кол-во инт. элементов')
bp.legend_.texts[2].set_text('Обратное кол-во инт. элементов')
bp.legend_.texts[3].set_text('Расстояние между состояниями')

plt.title('Зависимые от приложения стратегии', fontsize=40)
plt.ylabel('Уникальные состояния', fontsize=35)
plt.xlabel('Приложения', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.grid()
plt.savefig('states_app_based.jpg')
