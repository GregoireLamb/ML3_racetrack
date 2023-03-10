from racetrack import Racetrack

import random


class Episode:
    def __init__(self, racetrack: Racetrack, epsilon, state_values, min_speed_x, max_speed_x, min_speed_y, max_speed_y,
                 delta, max_episode_length, random_start=True):
        self.racetrack = racetrack
        self.epsilon = epsilon
        self.state_values = state_values
        self.min_speed_x = min_speed_x
        self.max_speed_x = max_speed_x
        self.min_speed_y = min_speed_y
        self.max_speed_y = max_speed_y
        self.delta = delta
        self.max_episode_length = max_episode_length

        self._random_start = random_start
        start_point = racetrack.start_positions[int(len(racetrack.start_positions) / 2)]
        self._fixed_start = start_point[1], start_point[0]

        self._path = []

        self._current_pos = None  # (x, y) pairs of integers
        self._current_velocity = None  # (vx, vy) pair of integers

    def get_possible_actions(self):
        # Velocity should be positive, <= 5
        # Compute based on self._current_velocity, self._current_pos
        vx, vy = self._current_velocity

        deltas_vx = [-1, 0, 1]
        deltas_vy = [-1, 0, 1]

        if vx == self.min_speed_x:
            deltas_vx.remove(-1)
        if vx == self.max_speed_x:
            deltas_vx.remove(1)

        if vy == self.min_speed_y:
            deltas_vy.remove(-1)
        if vy == self.max_speed_y:
            deltas_vy.remove(1)

        # remove action that leads to (vx, vy) = (0, 0)
        possible_actions = [(delta_vx, delta_vy) for delta_vx in deltas_vx for delta_vy in deltas_vy if
                            ((delta_vx + vx != 0) or (delta_vy + vy != 0))]
        random.shuffle(possible_actions)
        return possible_actions

    def choose_action(self, possible_actions):
        # Choose action based on epsilon-greedy policy. Return (position, speed, action)
        if random.random() < self.delta:
            action = (0, 0)
        elif random.random() < self.epsilon:
            action = random.choice(possible_actions)
        else:
            action = max(possible_actions, key=lambda a: self.state_values[
                (self._current_pos, (self._current_velocity[0] + a[0], self._current_velocity[1] + a[1]))])

        new_velocity = (self._current_velocity[0] + action[0], self._current_velocity[1] + action[1])
        new_position = (self._current_pos[0] + new_velocity[0], self._current_pos[1] + new_velocity[1])
        return new_position, new_velocity, action

    def go_to_start(self):
        # Go back to the start position
        y, x = random.choice(self.racetrack.start_positions)
        return (x, y), self.random_velocity()

    def random_velocity(self):
        return 0, random.choice(range(self.min_speed_y, self.max_speed_y + 1))

    def write_to_file(self, file):
        file.write(f'{self._current_pos[0]}, {self._current_pos[1]}, '
                   f'{self._current_velocity[0]}, {self._current_velocity[1]},\n')

    def simulate(self, file):
        if self._random_start:
            self._current_pos, self._current_velocity = self.go_to_start()
        else:
            self._current_pos, self._current_velocity = \
                self._fixed_start, self.random_velocity()
        self._current_pos, self._current_velocity = self.go_to_start()
        self._path.append((self._current_pos, self._current_velocity, None))
        duration = 0
        self.write_to_file(file)

        while not self.racetrack.has_finished(self._current_pos, self._current_velocity) and \
                duration < self.max_episode_length:
            if self.racetrack.check_for_crash(self._current_pos, self._current_velocity):
                self._current_pos, self._current_velocity = self.go_to_start()
                self._path.append((self._current_pos, self._current_velocity, None))
                self.write_to_file(file)

            possible_actions = self.get_possible_actions()
            self._current_pos, self._current_velocity, action = self.choose_action(possible_actions)
            self._path.append((self._current_pos, self._current_velocity, action))

            self.write_to_file(file)
            duration += 1
        return self._path, duration < self.max_episode_length
