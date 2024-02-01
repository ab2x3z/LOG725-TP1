"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
# snake_pos = [100, 50]
# snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

# food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]

class Entity:
    def __init__(self, type, color, position):
        self.type = type
        self.color = color
        self.position = position

entities = [
    Entity("head", blue, [100, 50]),
    Entity("food", white, [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]),  
    Entity("body", green, [100, 50]), 
    Entity("body", green, [100-10, 50]), 
    Entity("body", green, [100-20, 50])
    ]


food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()



# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    game_window.fill(black)
    for entity in entities:

        # Moving the snake
        if entity.type == "head":          
            if direction == 'UP':
                entity.position[1] -= 10
            if direction == 'DOWN':
                entity.position[1] += 10
            if direction == 'LEFT':
                entity.position[0] -= 10
            if direction == 'RIGHT':
                entity.position[0] += 10

            test = [entity.position[0], entity.position[1]]
            # Snake body growing mechanism
            entities.insert(2, Entity("body", green, [entity.position[0], entity.position[1]]))
            for food in entities:
                if food.type == "food": 
                    if entity.position[0] == food.position[0] and entity.position[1] == food.position[1]:
                        score += 1
                        food_spawn = False
                    else:
                        entities.pop()

                # Spawning food on the screen
                if not food_spawn:
                    food.position = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
                food_spawn = True

        # GFX
        pygame.draw.rect(game_window, entity.color, pygame.Rect(entity.position[0], entity.position[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if entity.type == "head":
            if entity.position[0] < 0 or entity.position[0] > frame_size_x-10:
                game_over()
            if entity.position[1] < 0 or entity.position[1] > frame_size_y-10:
                game_over()
            # Touching the snake body
            for body in entities[3:]:
                if entity.position[0] == body.position[0] and entity.position[1] == body.position[1]:
                    game_over()
    
    show_score(1, white, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)