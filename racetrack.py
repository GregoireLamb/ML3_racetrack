class Racetrack:
    def __init__(self):
        # Values for the grid: 0 = outside, 1 = start, 2 = inside, 3 = finish

        self.grid = {}

    def has_finished(self, position, velocity):
        # Check if the car has reached the finish line
        return True

    def check_for_crash(self, position, velocity):
        # Check if the car has crashed into a wall
        pass
