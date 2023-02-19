from racetrack import Racetrack

from itertools import product
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from rl_racetrack import RLRacetrack


class MultipleRL:
    def __init__(self, base_config, params_to_try, how='one_vs_base'):
        self._base_config = base_config
        self._params_to_try = params_to_try
        self._how = how  # 'one_vs_base' or 'cross'

        self._results = {}

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
                results = self.run_with_config(config, report=False)
                self._results[f'{param_name} = {param_value}'] = results
        self._final_report()

    def _run_cross(self):
        configurations = list(product(*self._params_to_try.values()))
        for settings in configurations:
            print(f'Running with {self._params_to_try.keys()} = {settings}')
            for i, param_name in enumerate(self._params_to_try.keys()):
                config = self._base_config.copy()
                config[param_name] = settings[i]
                results = self.run_with_config(config, report=False)
                exec_name = ', '.join([f'{param_name} = {param_value}'
                                       for param_name, param_value in zip(self._params_to_try.keys(), settings)])
                self._results[exec_name] = results
        self._final_report()

    def _final_report(self):
        for name, results in self._results.items():
            print(f'\nExecution: {name}')
            print(f'    Number of episodes: {len(results)}')
            print(f'    Average return: {sum(results) / len(results)}')
            print(f'    Last 100 average return: {sum(results[-100:]) / 100 if len(results) >= 100 else "N/A"}')

        # make all results lists the same length
        max_episodes = max([len(results) for results in self._results.values()])
        for execution in self._results.keys():
            self._results[execution] += [0] * (max_episodes - len(self._results[execution]))


        df = pd.DataFrame(self._results)
        df['episode'] = df.index
        sns.lineplot(data=df.melt(id_vars='episode', var_name='settings'), x='episode', y='value',
                     hue='settings').set(title='Episode returns by execution', xlabel='Episode',
                                          ylabel='Episode return')
        plt.show()

    @staticmethod
    def run_with_config(config, report=True):
        track = Racetrack(config)
        track.create_grid()

        track.print()

        rl_racetrack = RLRacetrack(config, track)

        rl_racetrack.run()

        if report:
            rl_racetrack.report()

        # visualization = View(config, rl_racetrack)
        # visualization.show()
        # visualization.save()

        return rl_racetrack.episode_returns


if __name__ == '__main__':
    base_config = {
        'grid_shape': (30, 30),
        'episodes': int(1e2),
        'epsilon': 0.1,  # probability of choosing random action
        'delta': 0.1,  # prob to not update velocity (not take action)
        'timestep_reward': -1,  # reward for each timestep. Actually has no impact
        'update_state_values_rule': 'every_visit',  # 'first_visit' or 'every_visit'
        'min_speed_x': 0,
        'max_speed_x': 5,
        'min_speed_y': -5,
        'max_speed_y': 0,
        'max_episode_length': 100,
    }

    params_to_try = {
        'epsilon': [0.1, 0.2],
        'delta': [0.1, 0.2],
    }

    multipleRL = MultipleRL(base_config, params_to_try, how='cross')
    multipleRL.run()
