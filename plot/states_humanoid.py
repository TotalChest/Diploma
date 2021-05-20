import argparse
import json
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib as mpl

plt.figure(figsize=(25, 10))
sns.set_palette("deep")
sns.set(style="ticks")

humanoid = [59, 27, 97, 91, 28, 34, 51, 53, 91, 76]
qlearning = [80, 68, 107, 189, 39, 40, 79, 53, 139, 117]

plt.plot(qlearning, 's:', markersize=18, label='Qlearning', linewidth=2)
plt.plot(humanoid, 's:', markersize=18, label='Humanoid', linewidth=2)

plt.xticks(range(10), ['ALIEXPRESS', 'APPLEBEES', 'BOOKING', 'COLORNOTE', 'DOMINOS', 'EBAY', 'FACEAPP', 'NYTIMES', 'WIKIPEDIA', 'WSJ'])

plt.legend(loc=9, prop={'size': 25}, shadow=True)
plt.title('Сравнение с Humanoid', fontsize=40)
plt.ylabel('Уникальные cocтояния', fontsize=35)
plt.xlabel('Приложения', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.grid()
plt.savefig('states_humanoid.jpg')
