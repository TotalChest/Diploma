import argparse
import os
from pathlib import Path


def init_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', type=int, required=True,
                        help='How many episodes for testing')
    parser.add_argument('--timeout', type=int, required=True,
                        help='Tesing time for episode')
    parser.add_argument('--epsilon', type=float, default=0.9,
                        help='Init value for epsilon')
    return parser.parse_args()


if __name__ == '__main__':
    options = init_options()
    
    EPISODES = options.episodes
    TIMEOUT = options.timeout

    # Second Epsilon Greedy strategy
    # Where epsilon decrease from 0.9 to 0 and only changes after episode
    EPSILON_DECAY = 0.6

    APKS = '/home/sfomin/Documents/apks_core'
    Q_TABLE_PATH = 'q-table.txt'
    LEANING_RATE = 0.5

    for apk_file in Path(APKS).iterdir():

        for timeout in [12]:

            for strategy in ['abstract_states', 'dqn', 'events_count',
                             'possible_events', 'reverse_possible_events',
                             'tree_edit_distance', 'epsilon_greedy']:

                epsilon = options.epsilon

                for episode in range(EPISODES):

                    print(f'\n\nAPK: {apk_file.name} \nESISODE: {episode} '
                          f'\nTIMEOUT: {timeout} \nepsilon={epsilon} '
                          f'\nstrategy: {strategy}\n\n')

                    OUTPUT = f'/home/sfomin/RLoutput/{apk_file.name}/'
                             f'{strategy}_{timeout}_{episode}'
                    Q_TABLE_PATH = f'/home/sfomin/RLtables/{apk_file.name}/'
                                   f'{stage}_qtable_{timeout}.txt'
                    
                    
                    os.system(f'poetry run python {Path(__file__).parents[0] / "../main.py"} '
                        f'-p qlearning --q-learning-strategy {strategy} '
                        f'-d emulator-5554 '
                        f'-a {apk_file} '
                        f'-o {OUTPUT} '
                        f'--timeout {timeout} '
                        f'--save-q-table-path {Q_TABLE_PATH} '
                        f'--q-table-path {Q_TABLE_PATH} '
                        f'--epsilon {epsilon} '
                        f'--learning-rate {LEANING_RATE} '
                    )
                    
                    epsilon = epsilon * EPSILON_DECAY
