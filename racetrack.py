import random

class Racetrack:
    def __init__(self):  # size = (rows, columns)
        # Values for the grid: 0 = outside, 1 = start, 2 = inside, 3 = finish
        self.grid = None
        self.max_height = None
        self.start_positions = []

    def create_empty_grid(self, size):
        self.grid = [[0 for x in range(size[1])] for y in range(size[0])]
        # initialize an empty nxm grid

    def right_walk(self, x_start, min_space=5, min_width=5):
        # set 'padding' to the max velocity
        n = len(self.grid)
        m = len(self.grid[0])
        x = x_start
        self.grid[n - 2][x] = 2
        # force to go U on the first step
        y = n - 2

        while x < m - min_width - 1:
            # leave space to account for velocity at finish line
            self.grid[y][x] = 2
            if y - min_space - min_width == 0:
                # no space to go U anymore
                x += 1
            else:
                step = random.choice([0, 1])
                # randomly decide to go U or R
                if step == 0:
                    y -= 1
                else:
                    x += 1
        self.grid[y][x] = 3
        # we stop at the finish line
        self.max_height = y

    def left_walk(self, x_start, min_space=5, min_width=5):
        n = len(self.grid)
        m = len(self.grid[0])
        y = n-1
        x = x_start
        self.grid[n - 2][x] = 2
        self.grid[n - 3][x] = 2
        # Force to go U on the first two steps
        y = n - 3

        while x < m - min_width - 1:
            self.grid[y][x] = 2
            if y - min_space == 0:
                # no space to go U anymore
                x += 1
            elif (y < self.max_height) & (self.max_height - y < 5):
                # make sure the road is wide enough to turn
                y -= 1
            elif self.grid[y][x + min_width] == 2:
                # make sure road is wide enough
                y -= 1
            elif self.max_height - y > 2*min_width:
                # so the finish line is not too wide
                x += 1
            else:
                step = random.choice([0, 1])
                # randomly decide to go U or R
                if step == 0:
                    y -= 1
                else:
                    x += 1
        self.grid[y][x] = 3

        for i in range(y, self.max_height):
            self.grid[i][m - min_width - 1] = 3
            # paint the finish line

    def draw_grid_edges(self, min_space=5, min_width=5):
        start_r = (min_space + min_width*2 - 1)
        start_l = (min_space - 1)
        self.right_walk(start_r)
        self.left_walk(start_l)
        for j in range(start_l, start_r+1):
            self.start_positions.append((len(self.grid) - 1, j))
            self.grid[len(self.grid) - 1][j] = 1

        x_start_fill = start_l+1
        self.fill_grid(len(self.grid)-2, x_start_fill)

    def fill_grid(self, y, x):
        # converts all the interior 0's to 2's
        if self.grid[y][x] == 0:
            self.grid[y][x] = 2
            self.fill_grid(y, x + 1)
            self.fill_grid(y - 1, x)


    def has_finished(self, position, velocity):
        # check if the car has reached the finish line
        x = position[1]
        y = position[0]
        if self.grid[y][x] == 3:
            return True
        else:
            return False

    def check_for_crash(self, position, velocity):
        # check if the car will crash
        x = position[0]
        y = position[1]
        vx = velocity[0]
        vy = velocity[1]
        if (x + vx < 0) or (x + vx >= len(self.grid)) or (y + vy < 0) or (y + vy >= len(self.grid)) or (self.grid[y + vy][x + vx] == 0):
            return True
        return False

    def print(self):
        for x in self.grid:
            print(x, '\n')

    # Methood to get the finish line
    def get_finish_line(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 3:
                    return (i, j)
