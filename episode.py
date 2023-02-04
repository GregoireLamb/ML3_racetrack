from racetrack import Racetrack

class Episode:
    def __init__(self, racetrack: Racetrack, epsilon, state_values):
        self.racetrack = racetrack
        self.epsilon = epsilon
        self.state_values = state_values
        self._path = []

        self._current_pos = None  # (x, y) pairs of integers
        self._current_velocity = None  # (vx, vy) pairs of integers

    def get_possible_actions(self):
        # Velocity should be positive, <= 5
        # Compute based on self._current_velocity, self._current_pos
        return []

    def choose_action(self, possible_actions, epsilon, state_values):
        # Choose action based on epsilon-greedy policy. Return (position, speed, action)
        return None, None, None

    def go_back_to_start(self):
        # Go back to the start position
        return None, None

    def simulate(self):
        while not self.racetrack.has_finished(self._current_pos, self._current_velocity):
            possible_actions = self.get_possible_actions()
            self._current_pos, self._current_velocity, action = self.choose_action(possible_actions, self.epsilon,
                                                                                self.state_values)
            self._path.append((self._current_pos, action))
            if self.racetrack.check_for_crash(self._current_pos, self._current_velocity):
                self._current_pos, self._current_velocity = self.go_back_to_start()

        return self._path
