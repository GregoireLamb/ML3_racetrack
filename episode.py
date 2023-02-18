from racetrack import Racetrack

import random


class Episode:
    def __init__(self, racetrack: Racetrack, epsilon, state_values, min_speed_x, max_speed_x, min_speed_y, max_speed_y,
                 delta):
        self.racetrack = racetrack
        self.epsilon = epsilon
        self.state_values = state_values
        self.min_speed_x = min_speed_x
        self.max_speed_x = max_speed_x
        self.min_speed_y = min_speed_y
        self.max_speed_y = max_speed_y
        self.delta = delta

        self._path = []

        self._current_pos = None  # (x, y) pairs of integers
        self._current_velocity = None  # (vx, vy) pair of integers

    def get_possible_actions(self):
        # Velocity should be positive, <= 5
        # Compute based on self._current_velocity, self._current_pos
        vx = self._current_velocity[0]
        vy = self._current_velocity[1]

        deltas_vx = range(-vx - self.min_speed_x, -vx + self.max_speed_x + 1)
        deltas_vy = range(-vy - self.min_speed_y, -vy + self.max_speed_y + 1)

        return [(delta_vx, delta_vy) for delta_vx in deltas_vx for delta_vy in deltas_vy]

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

    def go_back_to_start(self):
        # Go back to the start position
        print(f'--- Going back to start ---')
        return random.choice(self.racetrack.start_positions), (0, 0)

    def simulate(self):
        self._current_pos, self._current_velocity = self.go_back_to_start()
        while not self.racetrack.has_finished(self._current_pos, self._current_velocity):
            # print(self._current_pos, self._current_velocity)
            possible_actions = self.get_possible_actions()
            self._current_pos, self._current_velocity, action = self.choose_action(possible_actions)
            print(self._current_pos, self._current_velocity, action)
            self._path.append((self._current_pos, action))
            if self.racetrack.check_for_crash(self._current_pos, self._current_velocity):
                self._current_pos, self._current_velocity = self.go_back_to_start()

        return self._path
