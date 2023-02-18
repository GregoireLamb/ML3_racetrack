from episode import Episode
from racetrack import Racetrack

from typing import List, Tuple

import seaborn as sns


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

        assert self.update_state_values_rule in ['first_visit', 'every_visit'], 'Invalid update state values rule'
        self.episode_returns = []

        self.state_values = self.define_state_values() # (pos, vel) -> (estimated return, count)

    def define_state_values(self):
        # Define the state values for all possible states
        # (position, velocity) -> (estimated return, count)

        possible_velocities = {(vx, vy) for vx in range(self.min_speed_x, self.max_speed_x + 1)
                               for vy in range(self.min_speed_y, self.max_speed_y + 1)}
        possible_positions = {(x, y) for x in range(self.racetrack.size[0]) for y in
                              range(self.racetrack.size[1])}

        state_values = {(pos, vel): (-self.inf, 0) for pos in possible_positions for vel in possible_velocities}

        return state_values

    def run(self):
        for episode in range(self.n_episodes):
            print(f'Episode {episode + 1}/{self.n_episodes}')
            ep = Episode(self.racetrack, self.epsilon, self.state_values,
                         self.min_speed_x, self.max_speed_x, self.min_speed_y, self.max_speed_y, self.delta)
            path = ep.simulate()
            ep_return = self.update_state_values(path)
            self.episode_returns.append(ep_return)

    def update_state_values(self, path: List[Tuple[Tuple[int, int], Tuple[int, int], int]]):
        g = 0
        visited = set()
        for (pos, vel), action in reversed(path):
            g += self.timestep_reward
            if self.update_state_values_rule == 'every_visit' or \
                    (self.update_state_values_rule == 'first_visit' and (pos, vel) not in visited):
                estimated_return, count = self.state_values[pos, vel]
                self.state_values[pos, vel] = (estimated_return + g) / (count + 1), count + 1
                visited.add((pos, vel))
        return g

    def report(self):
        # 1. Plot the state values map (project into position space)
        # 2. Plot the convergence curve: return vs iteration
        # 3. Plot path following learnt policy (use follow_policy method)
        max_x = max([pos[0] for pos, _ in self.state_values.keys()])
        max_y = max([pos[1] for pos, _ in self.state_values.keys()])
        base_grid = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        self.state_values_map(base_grid)
        self.learnt_policy_path(base_grid)
        self.convergence_curve()

    def state_values_map(self, base_grid: List[List[int]]):
        # Plot the state values map (project into position space)
        # Use seaborn heatmap
        grid = base_grid.copy()
        for pos, vel in self.state_values.keys():
            grid[pos[1]][pos[0]] += self.state_values[pos, vel][0]      # Project into position space with sum

        sns.heatmap(grid, annot=True, fmt=".1f").set(title='State values map')

    def convergence_curve(self):
        # Plot the convergence curve: return vs iteration
        sns.lineplot(x=range(self.n_episodes), y=self.episode_returns).\
            set(xlabel='Episode', ylabel='Return').set(title='Convergence curve')

    def learnt_policy_path(self, base_grid: List[List[int]]):
        # Plot path following learnt policy (use follow_policy method)
        # Run the policy and print the path
        ep = Episode(self.racetrack, epsilon=0, state_values=self.state_values)
        path = ep.simulate()
        grid = base_grid.copy()
        for pos, vel in path:
            grid[pos[1]][pos[0]] = 1
        sns.heatmap(grid, annot=True, fmt=".1f").set(title='Path following learnt policy')
