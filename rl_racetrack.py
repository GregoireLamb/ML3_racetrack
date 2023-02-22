from episode import Episode
from racetrack import Racetrack

from typing import List, Tuple

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import time
from utils import mov_avg


class RLRacetrack:
    def __init__(self, config: dict, racetrack: Racetrack):
        self.racetrack = racetrack
        self.inf = 1e5

        self.n_episodes = config['episodes']
        self.epsilon = config['epsilon']
        self.delta = config['delta']
        self.timestep_reward = config['timestep_reward']
        self.update_state_values_rule = config['update_state_values_rule']
        self.max_speed_x = config['max_speed_x']
        self.max_speed_y = config['max_speed_y']
        self.min_speed_x = config['min_speed_x']
        self.min_speed_y = config['min_speed_y']
        self.max_episode_length = config['max_episode_length']

        self.map_racetrack_values = {0: 'outside', 1: 'start', 2: 'inside', 3: 'finish'}

        assert self.update_state_values_rule in ['first_visit', 'every_visit', 'last_visit', 'last_visit_best'], \
            'Invalid update state values rule'
        self.episode_returns = []
        self.start_time = time.time()

        self.state_values = self.define_state_values()  # (pos, vel) -> (estimated return, count)

    def define_state_values(self):
        # Define the state values for all possible states
        # (position, velocity) -> (estimated return, count)

        possible_velocities = {(vx, vy) for vx in range(self.min_speed_x, self.max_speed_x + 1)
                               for vy in range(self.min_speed_y, self.max_speed_y + 1)}
        possible_positions = {(x, y) for x in range(len(self.racetrack.grid)) for y in
                              range(len(self.racetrack.grid))}

        state_values = {(pos, vel): (-self.inf, 0) for pos in possible_positions for vel in possible_velocities}

        return state_values

    def run(self, filename):
        # create log file
        # print('Running episode simulations...')
        f = open(filename, 'w')

        for episode in range(self.n_episodes):
            # print progress in percents.
            if episode % (self.n_episodes // 10) == 0:
                print(f'{episode // (self.n_episodes // 10) * 10}%')
            f.write(f'Episode {episode + 1}\n')
            ep = Episode(self.racetrack, self.epsilon, self.state_values,
                         self.min_speed_x, self.max_speed_x, self.min_speed_y, self.max_speed_y, self.delta,
                         self.max_episode_length)
            path, reached_end = ep.simulate(f)
            ep_return = self.update_state_values(path) if reached_end else - self.inf
            self.episode_returns.append(ep_return)

    def update_state_values(self, path: List[Tuple[Tuple[int, int], Tuple[int, int], int]]):
        g = 0
        visited = set()
        if self.update_state_values_rule in ['last_visit', 'last_visit_best']:
            for pos, vel, _ in reversed(path):
                g += self.timestep_reward
                if (pos, vel) not in visited:
                    estimated_return, count = self.state_values[pos, vel]
                    if self.update_state_values_rule == 'last_visit_best':
                        self.state_values[pos, vel] = (max(estimated_return, g), count + 1)
                    else:
                        self.state_values[pos, vel] = \
                            ((count * estimated_return + g) / (count + 1), count + 1) if count > 0 else (g, 1)
                    visited.add((pos, vel))

        else:
            for pos, vel, _ in path:
                g += self.timestep_reward
                if self.update_state_values_rule == 'every_visit' or \
                        (self.update_state_values_rule == 'first_visit' and (pos, vel) not in visited):
                    estimated_return, count = self.state_values[pos, vel]
                    self.state_values[pos, vel] = \
                        ((count * estimated_return + g) / (count + 1), count + 1) if count > 0 else (g, 1)
                    visited.add((pos, vel))
        return g

    def report(self):
        # 1. Plot the state values map (project into position space)
        # 2. Plot the convergence curve: return vs iteration
        # 3. Plot path following learnt policy (use follow_policy method)
        self.print_stats()

        base_grid = np.array(self.racetrack.grid).astype('float')
        self.state_values_map(base_grid, how='sum')
        self.state_values_map(base_grid, how='max')
        self.learnt_policy_path(base_grid)
        self.convergence_curve()

    def print_stats(self):
        print('\n-- Execution stats --')
        print('Number of episodes:', self.n_episodes)
        print('Average return:', np.mean(self.episode_returns))
        print('Last 100 episodes average return:',
              np.mean(self.episode_returns[-100:] if len(self.episode_returns) >= 100 else 'N/A'))
        print('Total runtime:', round(time.time() - self.start_time, 2), 'seconds')

    def state_values_map(self, base_grid: np.ndarray, how='sum'):
        # Plot the state values map (project into position space)
        # Use seaborn heatmap
        grid = base_grid.copy()

        cmap = {'outside': np.nan}
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                grid[i][j] = cmap.get(self.map_racetrack_values[base_grid[i][j]], -self.inf)
                if grid[i][j] < 0:
                    proj_func = max if how == 'max' else sum
                    state_values = [self.state_values[(j, i), (vx, vy)][0] for vx in
                                    range(self.min_speed_x, self.max_speed_x + 1)
                                    for vy in range(self.min_speed_y, self.max_speed_y + 1)]

                    grid[i][j] = proj_func(state_values)

        sns.heatmap(grid, annot=False, fmt=".1f").set(title=f'State values map - {how} projection')
        plt.show()

    def convergence_curve(self):
        # Plot the convergence curve: return vs iteration
        # For smoothing purposes, we actually plot return vs 100-episode moving average of returns
        smoothing_ma_window = 100
        moving_average = mov_avg(self.episode_returns, smoothing_ma_window)
        sns.lineplot(x=range(self.n_episodes), y=moving_average). \
            set(xlabel='Episode', ylabel='Return', title=f'Convergence curve (MA = {smoothing_ma_window})')
        plt.show()

    def learnt_policy_path(self, base_grid: np.ndarray):
        # Plot path following learnt policy
        # Run the policy and print the path
        ep = Episode(self.racetrack, 0, self.state_values, self.min_speed_x, self.max_speed_x, self.min_speed_y,
                     self.max_speed_y, 0, self.max_episode_length)
        f = open(r'runs\policy_path.txt', 'w')
        f.write('Episode 0:\n')
        path, _ = ep.simulate(f)

        grid = base_grid.copy()
        cmap = {'outside': np.nan, 'start': self.inf, 'finish': self.inf, 'inside': -self.inf}

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                grid[i][j] = cmap[self.map_racetrack_values[base_grid[i][j]]]

        for pos, _, _ in path:
            grid[pos[1]][pos[0]] = 1
        sns.heatmap(grid, annot=False, fmt=".1f").set(title='Path following learnt policy')
        plt.show()
