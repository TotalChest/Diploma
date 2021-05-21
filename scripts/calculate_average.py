import argparse
import json
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib as mpl


parser = argparse.ArgumentParser(description='Calculate average statistic.')
parser.add_argument('input', type=Path, help='Input file with statistics.')
parser.add_argument('strategy', type=str, help='Testing strategy.')
options = parser.parse_args()

strategy = options.strategy
app = str(options.input).split('/')[-1]
with open(options.input) as f:
    statistics = json.load(f)

df = pd.DataFrame(statistics).T
df['time'] = df.index.map(lambda x: int(x.split('/')[-1].split('_')[-2]))
df['strategy'] = df.index.map(lambda x: '_'.join(x.split('/')[-1].split('_')[:-2]))

print(df['strategy'].value_counts())
states = df[(df['time'] == 12) & (df['strategy'] == strategy)]['states']
activities = df[(df['time'] == 12) & (df['strategy'] == strategy)]['activities']

print(states)
print('MEAN: ', states.mean())
result = np.array(states)
result.sort()
plt.plot(result)
plt.show()

print(activities)
print('MEAN: ', activities.mean())
result = np.array(activities)
result.sort()
plt.plot(result)
plt.show()


