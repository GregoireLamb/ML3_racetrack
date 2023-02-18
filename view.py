from racetrack import Racetrack
import random
import pygame

class View:
    def __init__(self, racetrack: Racetrack):
        self.map = map
        self.height = 800
        self.width = self.height*0.8

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

    def draw_path(self, map_surf, path, lim):
        LENGHT = 35
        # Draw path
        if lim > len(path)-1:
            lim = len(path)-1

        for i in range(lim):
            pygame.draw.line(map_surf, 'blue', (path[i][0][0]*self.width*3/4/LENGHT, path[i][0][1]*self.width*3/4/LENGHT), (path[i+1][0][0]*self.width*3/4/LENGHT, path[i+1][0][1]*self.width*3/4/LENGHT), 3)
            pygame.draw.circle(map_surf, 'blue', (path[i][0][0]*self.width*3/4/LENGHT, path[i][0][1]*self.width*3/4/LENGHT), 5)


    def draw_grid(self, map_surf):
        LENGHT = 35

        # for each value in self.map draw a rectangle
        for key, value in self.map.items():
            if value == 0:
                color = 'black'
            elif value == 1:
                color = 'green'
            elif value == 2:
                color = 'grey'
            elif value == 3:
                color = 'red'
            else:
                raise ValueError('Unknown value in map')

            pygame.draw.rect(map_surf, color, (key[0]*self.width*3/4/LENGHT, key[1]*self.width*3/4/LENGHT, self.width*3/4/LENGHT, self.width*3/4/LENGHT))

        for i in range(LENGHT):
            vertical = (1 + i) * self.width * 3 / 4 / LENGHT
            pygame.draw.line(map_surf, 'black', (vertical, 0), (vertical, self.width * 3 / 4), 1)

            horizontal = (1 + i) * self.width * 3 / 4 / LENGHT
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

            screen.blit(back_surf, (0, 0))  # Add surface
            screen.blit(map_surf, (self.height/25, self.width/8))  # Add surface
            screen.blit(title, (self.height/25, self.width/25))  # Add font

            pygame.time.delay(300)
            self.draw_path(map_surf, self.path, step)

            step += 1
            pygame.time.delay(100)
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

    view = View(map)
    view.set_path(path)
    view.show()