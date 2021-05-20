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

humanoid = [17, 7, 17, 6, 1, 10, 2, 9, 11, 8]
qlearning = [16, 8, 15, 5, 1, 9, 2, 10, 14, 8]

plt.plot(qlearning, 's:', markersize=18, label='Qlearning', linewidth=2)
plt.plot(humanoid, 's:', markersize=18, label='Humanoid', linewidth=2)

plt.xticks(range(10), ['ALIEXPRESS', 'APPLEBEES', 'BOOKING', 'COLORNOTE', 'DOMINOS', 'EBAY', 'FACEAPP', 'NYTIMES', 'WIKIPEDIA', 'WSJ'])

plt.legend(loc=9, prop={'size': 25}, shadow=True)
plt.title('Сравнение с Humanoid', fontsize=40)
plt.ylabel('Уникальные Активности', fontsize=35)
plt.xlabel('Приложения', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.grid()
plt.savefig('activities_humanoid.jpg')
