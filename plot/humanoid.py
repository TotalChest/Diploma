import argparse
import json
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import matplotlib as mpl


plt.figure(figsize=(15, 10))
sns.set_palette("deep")

humanoid = [117, 39, 66, 41, 51, 77]
qlearning = [128, 72, 114, 41, 72, 138]

plt.plot(qlearning, 's:', markersize=15, label='Qlearning')
plt.plot(humanoid, 's:', markersize=15, label='Humanoid')

plt.xticks(range(6), ['BOOKING', 'EBAY', 'NYTIMES', 'APPLEBEES', 'FACEAPP', 'WSJ'])
plt.legend(loc=9, prop={'size': 20})
plt.title('Сравнение с Humanoid', fontsize=40)
plt.ylabel('Состояния', fontsize=30)
plt.xlabel('', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=25)
plt.savefig('humanoid.jpg')
