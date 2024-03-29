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
sns.set(style="ticks")

plot = []
labels = []
for result_file in options.input: 
    app = str(result_file).split('/')[-1]
    print(app)
    with open(result_file) as f:
        statistics = json.load(f)

    df = pd.DataFrame(statistics).T
    df['time'] = df.index.map(lambda x: int(x.split('/')[-1].split('_')[-2]))
    df['strategy'] = df.index.map(lambda x: '_'.join(x.split('/')[-1].split('_')[:-2]))

    plot.append(df[(df['time'] == 12) & ((df['strategy'] == '') | (df['strategy'] == 'events_count')) ]['states'])
    labels.append(app)

sns.boxplot(x=labels, y=plot)
plt.title('Недетерменированность тестирования', fontsize=40)
plt.xlabel('Приложения', fontsize=30)
plt.ylabel('Уникальные состояния', fontsize=35)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid()
plt.savefig('states_indeterminacy.jpg')
