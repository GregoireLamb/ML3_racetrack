from racetrack import Racetrack

from itertools import product
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import yaml, time

from rl_racetrack import RLRacetrack
from utils import mov_avg


class MultipleRL:
    def __init__(self, params_to_try, how='one_vs_base'):
        self._base_config = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
        self._params_to_try = params_to_try
        self._how = how  # 'one_vs_base' or 'cross'

        self._results = {}
        self._runtimes = {}

    def run(self):
        if self._how == 'one_vs_base':
            self._run_one_vs_base()
        if self._how == 'cross':
            self._run_cross()

    def _run_one_vs_base(self):
        for param_name, param_values in self._params_to_try.items():
            for param_value in param_values:
                print(f'Running with {param_name} = {param_value}')
                config = self._base_config.copy()
                config[param_name] = param_value
                results, runtime = self.run_with_config(config, report=False)
                self._results[f'{param_name} = {param_value}'] = results
                self._runtimes[f'{param_name} = {param_value}'] = runtime
        self._final_report()

    def _run_cross(self):
        configurations = list(product(*self._params_to_try.values()))
        for settings in configurations:
            print(f'Running with {self._params_to_try.keys()} = {settings}')
            config = self._base_config.copy()
            for i, param_name in enumerate(self._params_to_try.keys()):
                config[param_name] = settings[i]
            results, runtime = self.run_with_config(config, report=False)
            exec_name = ', '.join([f'{param_name} = {param_value}'
                                   for param_name, param_value in zip(self._params_to_try.keys(), settings)])
            self._results[exec_name] = results
            self._runtimes[exec_name] = runtime
        self._final_report()

    def _final_report(self):
        for name, results in self._results.items():
            print(f'\nExecution: {name}')
            print(f'    Number of episodes: {len(results)}')
            print(f'    Average return: {sum(results) / len(results)}')
            print(f'    Last 100 average return: {sum(results[-100:]) / 100 if len(results) >= 100 else "N/A"}')
            print(f'    Runtime: {self._runtimes[name]}')

        # make all results lists the same length
        max_episodes = max([len(results) for results in self._results.values()])
        mov_avg_window = 100
        for execution in self._results.keys():
            # Compute 100 moving average using numpy convolve
            self._results[execution] = mov_avg(self._results[execution], mov_avg_window)
            self._results[execution] += [np.nan] * (max_episodes - len(self._results[execution]))

        df = pd.DataFrame(self._results)
        df['episode'] = df.index
        sns.lineplot(data=df.melt(id_vars='episode', var_name='settings'), x='episode', y='value',
                     hue='settings').set(title=f'Episode returns by execution (MA = {mov_avg_window})', xlabel='Episode',
                                         ylabel='Episode return')
        plt.show()

    @staticmethod
    def run_with_config(config, report=True):
        start_time = time.time()

        track = Racetrack(config)
        grid_file = track.create_grid()

        rl_racetrack = RLRacetrack(config, track)

        logs = 'runs_' + grid_file.lstrip('grid_')
        rl_racetrack.run('runs/' + logs)

        if report:
            rl_racetrack.report()

        return rl_racetrack.episode_returns, time.time() - start_time


if __name__ == '__main__':
    config = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)

    params_to_try = {
        'epsilon': [0.05, 0.1, 0.2, 0.3],
    }

    multipleRL = MultipleRL(params_to_try, how='cross')
    multipleRL.run()
