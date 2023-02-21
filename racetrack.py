import random
from utils import closed_segment_intersect
import datetime
from bresenham import bresenham


class Racetrack:
    def __init__(self, config):
        # Values for the grid: 0 = outside, 1 = start, 2 = inside, 3 = finish
        self.shape = config['grid_shape']
        self.grid = None
        self.max_height = None
        self.start_positions = []
        self.seed = config['seed']
        self.end_positions = []
        self.finish_line_endpoints = None
        self.max_x = None

    def create_grid(self):
        self.create_empty_grid()
        self.draw_grid_edges()
        grid_file = self.store_grid()
        self.compute_finish_line_endpoints()
        return grid_file

    def compute_finish_line_endpoints(self):
        max_y = max([y for x, y in self.end_positions])
        min_y = min([y for x, y in self.end_positions])
        x = self.end_positions[0][0]
        self.finish_line_endpoints = (x, min_y), (x, max_y)

    def create_empty_grid(self):
        self.grid = [[0 for _ in range(self.shape[1])] for _ in range(self.shape[0])]
        # initialize an empty nxm grid

    def right_walk(self, x_start, min_space=5, min_width=5):
        random.seed(self.seed)
        # set 'padding' to the max velocity
        n = len(self.grid)
        m = len(self.grid[0])
        x = x_start
        self.grid[n - 2][x] = 2
        # force to go U on the first step
        y = n - 2
        self.max_x = x - min_width - 1

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
        self.end_positions.append((x, y))
        # we stop at the finish line
        self.max_height = y

    def left_walk(self, x_start, min_space=5, min_width=5):
        random.seed(self.seed)
        n = len(self.grid)
        m = len(self.grid[0])
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
            elif self.max_height - y > 2 * min_width:
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
        self.end_positions.append((x, y))

        # paint the finish line
        for i in range(y, self.max_height):
            self.grid[i][m - min_width - 1] = 3
            self.end_positions.append((m - min_width - 1, i))

    def draw_grid_edges(self, min_space=5, min_width=5):
        start_r = (min_space + min_width * 2 - 1)
        start_l = (min_space - 1)
        self.right_walk(start_r)
        self.left_walk(start_l)
        for j in range(start_l, start_r + 1):
            self.start_positions.append((len(self.grid) - 1, j))
            self.grid[len(self.grid) - 1][j] = 1

        x_start_fill = start_l + 1
        self.fill_grid(len(self.grid) - 2, x_start_fill)

    def fill_grid(self, y, x):
        # converts all the interior 0's to 2's
        if self.grid[y][x] == 0:
            self.grid[y][x] = 2
            self.fill_grid(y, x + 1)
            self.fill_grid(y - 1, x)

    def has_finished(self, position, velocity):
        # Compute whether the segments:
        # 1. previous position to current position, and
        # 2. finish line; are intersecting
        # If they are, then the car has finished
        x, y = position
        vx, vy = velocity
        x_prev = x - vx
        y_prev = y - vy
        return closed_segment_intersect((x_prev, y_prev), (x, y), *self.finish_line_endpoints)

    def has_finished_old(self, position, velocity):
        # check if the car has reached the finish line
        x, y = position
        vx, vy = velocity

        # assert self.grid[y][x] != 0, "the has_finished method cannot be used outside the road"

        dist_to_finish = abs(self.max_x - x)

        if dist_to_finish <= vx:
            # check if we can reach the finish line
            if vy > 0:
                y_u = y
                while self.grid[y_u][x] == 2:
                    # calculate the distance to the edge of the road from above
                    y_u -= 1
                dist_to_side = abs(y_u - y)

                if dist_to_finish - vx < dist_to_side - abs(vy):
                    # check if we reach finish line before side of the road
                    return True
                else:
                    return False

            elif vy < 0:
                y_d = y
                while self.grid[y_d][x] == 2:
                    # calculate the distance to the edge of the road from below
                    y_d += 1
                dist_to_side = abs(y_d - y)

                if dist_to_finish - vx < dist_to_side - abs(vy):
                    # check if we reach finish line before side of the road
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    def jumped_over_wall(self, position, velocity):
        x1, y1 = position
        vx, vy = velocity
        if (y1, x1) in self.start_positions:
            return False
        x0 = x1 - vx
        y0 = y1 - vy
        for x, y in bresenham(x0, y0, x1, y1):
            if self.grid[y][x] == 0:
                #print("jumped_over_wall: ", x, y, self.grid[y][x])
                return True
        return False

    def check_for_crash(self, position, velocity):
        # check if the car will crash
        x, y = position
        return self.grid[y][x] == 0 or self.jumped_over_wall(position, velocity)

    def store_grid(self):
        # get the current time to name the file
        time = datetime.datetime.now()
        filename = 'grid_'+str(time).replace('-', '_').split('.', 1)[0].replace(':', '_').replace(' ', 'h')+'.txt'
        # store the grid in a file
        with open('runs/'+filename, 'w') as f:
            for x in self.grid:
                for y in x:
                    if y != '[' or y != ']':
                        f.write(str(y)+',')
                f.write('\n')
        return filename

    def print(self):
        values_map = {0: u"█", 1: "X", 2: " ", 3: "X"}
        for i in range(len(self.grid)):
            print(''.join([values_map[self.grid[i][j]] for j in range(len(self.grid[i]))]))


#
#       Test function to delete in the final version
#

    def test_crash(self):
        for x, y in bresenham(0, 0, 2, 1):
            print(x, y)

        position = (15, 15)
        velocity = (2, 2)
        #print(self.check_for_crash(self, position, velocity))
