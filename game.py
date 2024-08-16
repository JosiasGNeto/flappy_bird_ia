# Imports #
import random
import pygame
import neat
import os

AI_Play = True     # True: AI's gonna play | False: Player's gonna play     
generation = 0

# Screen Size #
WIDTH  = 500
HEIGHT = 800

# Images #
IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'back.png')))
IMG_FLOOR      = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'base.png')))
IMG_PIPE       = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))
IMG_BIRD       = [
                    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),        
                    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))), 
                    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png'))), 
                 ]

# Game Font #
pygame.font.init()
FONT = pygame.font.SysFont('arial', 50)


class Bird:
    IMAGES = IMG_BIRD

    # Animating the rotation #

    ANIMATION_TIME = 5
    ROTATION_SPEED = 20
    ROTATION_MAX   = 25

    # Constructor Method #
    def __init__(self, x, y):
        self.x      = x
        self.y      = y
        self.time   = 0
        self.angle  = 0
        self.speed  = 0
        self.frames = 0
        self.height = self.y
        self.image  = self.IMAGES[0]

    # Jump Method #
    def jump(self):
        self.time   = 0
        self.speed  = -25.5
        self.height = self.y

    # Movement Method #
    def move(self):
        self.time += 1
        self.aceleration = 1.5

        movement = self.aceleration * (self.time**2) + self.speed

        # Limit Movement #
        if movement > 16:
            movement = 16
        elif movement < 0:
            movement -= 2

        self.y += movement

        # Angle #
        if movement < 0 or self.y < (self.height + 50):
            if self.angle < self.ROTATION_MAX:
                self.angle = self.ROTATION_MAX
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_SPEED

    def draw(self, screen):
        # set what image we are gonna use 
        self.frames  += 1

        if self.frames < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.frames < self.ANIMATION_TIME*2:
            self.image = self.IMAGES[1]
        elif self.frames < self.ANIMATION_TIME*3:
            self.image = self.IMAGES[2]
        elif self.frames < self.ANIMATION_TIME*4:
            self.image = self.IMAGES[1]
        elif self.frames < self.ANIMATION_TIME*4 + 1:
            self.image = self.IMAGES[0]

        # if bird is falling don't use the wings 
        if self.angle <= -80:
            self.image  = self.IMAGES[1]
            self.frames = self.ANIMATION_TIME*2

        # draw image 
        center_position = self.image.get_rect(topleft = (self.x, self.y)).center
        rotate_image    = pygame.transform.rotate(self.image, self.angle)
        hitbox          = rotate_image.get_rect(center = center_position)

        screen.blit(rotate_image, hitbox.topleft)

    def mask(self):
        return pygame.mask.from_surface(self.image)

class Pipe:
    SPEED    = 5
    DISTANCE = 200

    def __init__(self, x):
        self.x               = x
        self.height          = 0
        self.position_top    = 0
        self.position_bottom = 0
        self.passed          = False

        self.PIPE_BOTTOM = IMG_PIPE
        self.PIPE_TOP    = pygame.transform.flip(IMG_PIPE, False, True)

        self.set_height()

    def set_height(self):
        self.height          = random.randrange(50, 450)
        self.position_top    = self.height - self.PIPE_TOP.get_height()
        self.position_bottom = self.height + self.DISTANCE

    def move(self):
        self.x -= self.SPEED
    
    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.position_top))
        screen.blit(self.PIPE_BOTTOM, (self.x, self.position_bottom))

    def collision(self, bird):
        bird_mask    = bird.mask()
        mask_top     = pygame.mask.from_surface(self.PIPE_TOP)
        mask_bottom  = pygame.mask.from_surface(self.PIPE_BOTTOM)

        distance_top    = (self.x - bird.x, self.position_top - round(bird.y))
        distance_bottom = (self.x - bird.x, self.position_bottom - round(bird.y))

        point_top    = bird_mask.overlap(mask_top, distance_top)
        point_bottom = bird_mask.overlap(mask_bottom, distance_bottom)

        if point_bottom or point_top:
            return True
        else:
            return False

class Floor:
    SPEED = 5
    WIDTH = IMG_FLOOR.get_width()
    IMAGE = IMG_FLOOR

    def __init__(self, y):
        self.y  = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))

def draw_screen(screen, birds, pipes, floor, points):

    screen.blit(IMG_BACKGROUND, (0, 0))

    for bird in birds:
        bird.draw(screen)

    for pipe in pipes:
        pipe.draw(screen)

    text = FONT.render(f"Score: {points}", 1, (255, 255, 255))
    screen.blit(text, (WIDTH - 10 - text.get_width(), 10))

    if AI_Play:
        text = FONT.render(f"Gen: {generation}", 1, (255, 255, 255))
        screen.blit(text, (10, 10))

    floor.draw(screen)
    pygame.display.update()

def main(genomes, config):
    global generation
    generation += 1

    if AI_Play:
        networks = []
        birds = []
        genomes_list = []

        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            networks.append(network)
            genome.fitness = 0
            genomes_list.append(genome)
            birds.append(Bird(230, 350))
    else:
        birds = [Bird(230, 350)]
        networks = None
        genomes_list = None

    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    points = 0
    clock = pygame.time.Clock()

    is_running = True

    while is_running:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                quit()
            if not AI_Play:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for bird in birds:
                            bird.jump()

        pip_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > (pipes[0].x + pipes[0].PIPE_TOP.get_width()):
                pip_index = 1
        else:
            is_running = False
            break

        for i, bird in enumerate(birds):
            bird.move()
            if AI_Play:
                genomes_list[i].fitness += 0.1
                output = networks[i].activate(
                    (bird.y, abs(bird.y - pipes[pip_index].height), abs(bird.y - pipes[pip_index].position_bottom))
                )
                if output[0] > 0.5:
                    bird.jump()

        floor.move()

        create_pipe = False
        remove_pipe = []

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collision(bird):
                    birds.pop(i)
                    if AI_Play:
                        genomes_list[i].fitness -= 1
                        genomes_list.pop(i)
                        networks.pop(i)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    create_pipe = True
                pipe.move()

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    remove_pipe.append(pipe)

        for pipe in remove_pipe:
            if pipe in pipes:
                pipes.remove(pipe)

        if create_pipe:
            points += 1
            pipes.append(Pipe(600))
            if AI_Play:
                for genome in genomes_list:
                    genome.fitness += 5  

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)
                if AI_Play:
                    genomes_list.pop(i)
                    networks.pop(i)

        draw_screen(screen, birds, pipes, floor, points)


def run(path_config):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        path_config
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    if AI_Play:
        population.run(main)
    else:
        main(None, None)

if __name__ == '__main__':
    path = os.path.dirname(__file__)
    path_config = os.path.join(path, 'config.txt')
    run(path_config)