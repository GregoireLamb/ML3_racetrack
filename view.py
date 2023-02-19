from racetrack import Racetrack
import random
import pygame

class View:
    def __init__(self):
        self.map = None
        self.height = 800
        self.width = self.height*0.8
        self.map_height = None
        self.episodes = None

    def load_path(self, path):
        with open(path, 'r') as f:
            episodes = []
            lines = f.readlines()
            for line in lines:
                if line[0] == 'E': # New episode
                    path = []
                    episodes.append(path)
                    continue
                else:
                    row = line.split(',')
                    try:
                        row.remove('\n')
                    except:
                        pass
                    row = [int(x) for x in row]
                    path.append([(row[0],row[1]),(row[2],row[3])]) #append velocity
            episodes.append(path)

            #print(len(episodes))
            #for i in range(len(episodes)):
            #    print(episodes[i])
            self.episodes = episodes


    def load_map(self, path):
        # parse map
        with open(path, 'r') as f:
            map = []
            lines = f.readlines()
            for line in lines:
                row = line.split(',')
                try:
                    row.remove('\n')
                except:
                    pass
                row = [int(x) for x in row]
                map.append(row)
            self.map_height = len(map[0])
            self.map = map

    def set_path(self, path):
        self.path = path

    def create_screen(self):
        screen = pygame.display.set_mode((self.height, self.width), pygame.RESIZABLE)
        screen.fill('white')
        pygame.display.set_caption('ML3 Racetrack')
        return screen

    def create_title(self):
        title_font = pygame.font.Font(None, 50)
        title_surface = title_font.render('ML3: Racetrack group 31', True, 'Black')
        return title_surface

    def create_background(self):
        back_surf = pygame.Surface((self.height, self.width))
        back_surf.fill('white')
        return back_surf

    def map_background(self):
        map_surf = pygame.Surface((self.width*3/4, self.width*3/4))
        map_surf.fill('black')
        return map_surf

    def draw_path(self, map_surf, path, n_frames):
        for i in range(n_frames-1):
            pygame.draw.line(map_surf, 'blue', (path[i][0][0]*self.width*3/4/self.map_height, path[i][0][1]*self.width*3/4/self.map_height), (path[i+1][0][0]*self.width*3/4/self.map_height, path[i+1][0][1]*self.width*3/4/self.map_height), 3)
            #pygame.draw.circle(map_surf, 'blue', (path[i][0][0]*self.width*3/4/self.map_height, path[i][0][1]*self.width*3/4/self.map_height), 5)

    def draw_episodes(self, map_surf, lim):
        episode = 0
        total_frames = len(self.episodes[episode])-1
        frame = 0

        # Draw path
        while lim > total_frames and episode <= len(self.episodes)-2:  # lim is to create frames
            #print('Total frames: ', total_frames)
            episode += 1
            total_frames += len(self.episodes[episode]) - 1

        n_frames = lim - total_frames + len(self.episodes[episode]) -1
        if n_frames > len(self.episodes[episode]):
            n_frames = len(self.episodes[episode])
        path = self.episodes[episode]

        print('Episode: ', episode, 'Frame: ', n_frames)
        self.draw_path(map_surf, path, n_frames)


    def draw_grid(self, map_surf):

        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if self.map[i][j] == 0:
                    color = 'black'
                elif self.map[i][j] == 1:
                    color = 'green'
                elif self.map[i][j] == 2:
                    color = 'grey'
                elif self.map[i][j] == 3:
                    color = 'red'
                else:
                    raise ValueError('Unknown value in map')

                pygame.draw.rect(map_surf, color, (j*self.width*3/4/self.map_height, i*self.width*3/4/self.map_height, self.width*3/4/self.map_height, self.width*3/4/self.map_height))

        for i in range(len(self.map)):
            vertical = (1 + i) * self.width * 3 / 4 / len(self.map)
            pygame.draw.line(map_surf, 'black', (vertical, 0), (vertical, self.width * 3 / 4), 1)

            horizontal = (1 + i) * self.width * 3 / 4 / len(self.map)
            pygame.draw.line(map_surf, 'black', (0, horizontal), (self.width * 3 / 4, horizontal), 1)



    def show(self):
        pygame.init()
        clock = pygame.time.Clock()

        screen = self.create_screen()
        back_surf = self.create_background()
        map_surf = self.map_background()
        title = self.create_title()
        self.draw_grid(map_surf)

        run = 1
        step = 0
        while run:

            for event in pygame.event.get():  # get all event
                if event.type == pygame.QUIT:  # Check for exit
                    run = 0  # Exit

            #map_surf = self.map_background()
            screen.blit(back_surf, (0, 0))  # Add surface
            screen.blit(map_surf, (self.height/25, self.width/8))  # Add surface
            screen.blit(title, (self.height/25, self.width/25))  # Add font

            self.draw_grid(map_surf)
            self.draw_episodes(map_surf, step)

            step += 1
            pygame.display.update()
            pygame.time.delay(1)
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':

    state1 = [(15, 35), (0, 0)]
    state2 = [(14, 34), (1, 1)]
    state3 = [(12, 32), (2, 2)]
    state4 = [(10, 30), (2, 2)]
    state5 = [(9, 27), (3, 1)]
    state6 = [(10, 23), (4, 1)]
    state7 = [(11, 18), (5, 1)]
    state8 = [(11, 13), (4, 0)]
    state9 = [(11, 8), (5, 0)]
    state10 = [(12, 3), (5, 1)]

    path = [state1, state2, state3, state4, state5, state6, state7, state8, state9, state10]
    path2 = [state1, state10]

    map = {(x, y): random.randint(0, 3) for x in range(0, 35) for y in range(0, 35)}

    for x in range(0, 10):
        for y in range(0, 35):
            map[x, y] = 0
        map[x, 1] = 0
    for x in range(10, 22):
        for y in range(0, 35):
            map[x, y] = 2
    for x in range(22, 35):
        for y in range(0, 35):
            map[x, y] = 0
    for x in range(10, 22):
        map[x, 34] = 1
    for x in range(10, 22):
        map[x, 0] = 3

    view = View()
    view.set_path(path)
    view.show()