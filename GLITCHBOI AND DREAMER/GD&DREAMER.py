import pygame, sys, random, time
from pygame.fastevent import wait

clock = pygame.time.Clock()

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)

pygame.init() # initiates pygame

pygame.display.set_caption('GLITCHBOI AND DREAMER')

WINDOW_SIZE = (1920,1000)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((384,202))

grassimg = pygame.image.load('GLITCHBOI AND DREAMER\images\sblocks\grass.png')
dirtimg = pygame.image.load('GLITCHBOI AND DREAMER\images\sblocks\dirt.png')
metalimg1 = pygame.image.load(r'GLITCHBOI AND DREAMER\images\sblocks\lessfancyblockofmetal.png')
metalimg2 = pygame.image.load(r'GLITCHBOI AND DREAMER\images\sblocks\blockofmetal.png')
brickimg = pygame.image.load(r"GLITCHBOI AND DREAMER\images\sblocks\brick.png")
balcony_left_img = pygame.image.load(r"GLITCHBOI AND DREAMER\images\sblocks\balcony_left_end.png")
balcony_middle_img = pygame.image.load(r"GLITCHBOI AND DREAMER\images\sblocks\balcony_middle.png")
balcony_right_img = pygame.image.load(r"GLITCHBOI AND DREAMER\images\sblocks\balcony_right_end.png")
lamp_left_img = pygame.image.load(r"GLITCHBOI AND DREAMER\images\sblocks\lamp.png")
lamp_right_img = pygame.image.load(r"GLITCHBOI AND DREAMER\images\sblocks\lamp_2.png")
background_image = pygame.image.load(r"GLITCHBOI AND DREAMER\images\stestfiles\bg.png")
glassimg = pygame.image.load(r"GLITCHBOI AND DREAMER\images\sblocks\glass.png")
coinimg = pygame.image.load(r"GLITCHBOI AND DREAMER\images\interactives\coin.png")
diamondimg = pygame.image.load(r"GLITCHBOI AND DREAMER\images\interactives\diamond.png")
bg = background_image
transparent = (0, 0, 0, 0)

jump_sound = pygame.mixer.Sound(r'GLITCHBOI AND DREAMER\sounds\jump.wav')
walk_sound = [pygame.mixer.Sound(r'GLITCHBOI AND DREAMER\sounds\grass_0.wav'), pygame.mixer.Sound(r'GLITCHBOI AND DREAMER\sounds\grass_1.wav'), pygame.mixer.Sound('GLITCHBOI AND DREAMER\sounds\grass_2.wav'),pygame.mixer.Sound(r'GLITCHBOI AND DREAMER\sounds\grass_3.wav')]
win_sound = pygame.mixer.Sound(r"GLITCHBOI AND DREAMER\sounds\win.wav")
coin_sound = pygame.mixer.Sound(r"GLITCHBOI AND DREAMER\sounds\mixkit-winning-a-coin-video-game-2069.wav")
diamond_sound = pygame.mixer.Sound(r"GLITCHBOI AND DREAMER\sounds\mixkit-space-coin-win-notification-271.wav")
coin_sound.set_volume(0.2)
diamond_sound.set_volume(0.2)
walk_sound[0].set_volume(0.2)
walk_sound[1].set_volume(0.2)
walk_sound[2].set_volume(0.2)
walk_sound[3].set_volume(0.2)
win_sound.set_volume(0.2)

pygame.mixer.music.load('GLITCHBOI AND DREAMER\sounds\music.mp3')
pygame.mixer.music.play(-1)

walk_sound_timer = 0
TILE_SIZE = grassimg.get_width()

i = 0

def loadmap(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
global animation_frames
animation_frames = {}

def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split(r'/') [-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255, 0, 0))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame

animation_database = {}
animation_database['run'] = load_animation('GLITCHBOI AND DREAMER/images/GD/duxey/run',[8,8,8,8])
animation_database['idle'] = load_animation('GLITCHBOI AND DREAMER/images/GD/duxey/idle',[4])

player_action = 'idle'
player_frame = 0
player_flip = False

game_map = loadmap(r'GLITCHBOI AND DREAMER\map\map.txt')
game_map_2 = loadmap(r"GLITCHBOI AND DREAMER\map\map2.txt")
game_map_3 = loadmap(r"GLITCHBOI AND DREAMER\map\map3.txt")

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

font_style = pygame.font.SysFont("bahnschrift", 25)
def message(msg, color, coords):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, coords)

leftmove = False
rightmove = False
upmove = False

player_y_momentum = 0
air_timer = 0
true_scroll = [0, 0]

background_objects = [[0.25,[120, 10, 70, 400]], [0.25,[280, 30, 40, 400]], [0.5,[30, 40, 40, 400]], [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

player_rect = pygame.Rect(69, 69, 10, 22)

next_level = 0

score = 0

d = 0
e = 0

interactive_rects = []
while next_level == 0: # game loop

    display.blit(background_image, (0, 0))

    if walk_sound_timer > 0:
        walk_sound_timer -= 1

    collide_left = False
    collide_right = False
    upmove = False

    true_scroll[0] += (player_rect.x - true_scroll[0] - 145)/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 89)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # for background_object in background_objects:
    #     obj_rect = pygame.Rect(background_objects[1][0] - scroll[0]*background_object[0], background_object[1][1] - scroll[1]*background_object[0], background_object[1][2], background_object[1][3])
    #     if background_object[0] == 0.5:
    #         pygame.draw.rect(display, (255, 255, 0), obj_rect)
    #     else:
    #         pygame.draw.rect(display, (255, 0, 0), obj_rect)

    # message('x coordinate ' + str(player_rect.x), 'white', [5, 5])
    # message('y coordinate ' + str(player_rect.y), 'white', [5, 25])

    tile_rects = []

    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirtimg, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
                tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile == '2':
                display.blit(grassimg, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
                tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile == '3' and d == 0:
                interactive_rects.append([pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 'coin'])
            if tile == '4' and d == 0:
                interactive_rects.append([pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 'diamond'])
            x += 1
        y += 1
    d = 1

    for interactive in interactive_rects:
        if interactive[1] == 'coin':
            display.blit(coinimg, (interactive[0][0] - scroll[0], interactive[0][1] - scroll[1]))
        if interactive[1] == 'diamond':
            display.blit(diamondimg, (interactive[0][0] - scroll[0], interactive[0][1] - scroll[1]))
        if player_rect.colliderect(interactive[0]) == True:
            if interactive[1] == 'coin':
                score += 1
                coin_sound.play()
                index = interactive_rects.index(interactive)
                interactive_rects.pop(index)
            if interactive[1] == 'diamond':
                diamond_sound.play()
                score += 5
                index = interactive_rects.index(interactive)
                interactive_rects.pop(index)

    player_movement = [0, 0]
    if rightmove:
        player_movement[0] += 2 
    if leftmove:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    if player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False
    if player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True
    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    # for interactive in interactive_rects:
    #     if player_rect.colliderect(interactive[0]):
    #         if interactive[1] == 'coin':
    #             score += 1
    #
    #             interactive_rects.remove(interactive)
    #         if interactive[1] == 'diamond':
    #             interactive_rects.remove(interactive)
    #             score += 5

    message('score: ' + str(score), 'violet', [5, 5])

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
        if player_movement[0] != 0:
            if walk_sound_timer == 0:
                walk_sound_timer = 30
                random.choice(walk_sound).play()
    else:
        air_timer += 1

    if collisions['top']:
        player_y_momentum = -player_y_momentum * 0.75

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_image_id = animation_database[player_action][player_frame]
    player_image = animation_frames[player_image_id]
    display.blit(pygame.transform.flip(player_image, player_flip, False), (player_rect.x - scroll[0], player_rect.y - scroll[1])) # render player

    if player_rect.y > 400:
        display.blit(background_image, (0, 0))
        message('GAME OVER', 'yellow', [130, 40])
        message('Press R to restart, or Q to quit', 'red', [20, 140])
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    display.blit(background_image, (0, 0))
                    player_rect = pygame.Rect(69, 69, 10, 22)
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

    if player_rect.x > 3800:
        message('YOU WON', 'blue', [140, 40])
        message('PRESS N TO GO TO NEXT LEVEL', 'purple', [10, 140])
        player_rect = pygame.Rect(player_rect.x, player_rect.y, 10, 22)
        if i == 0:
            pygame.mixer.music.set_volume(0)
            win_sound.play(1)
            i = 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_n and player_rect.x >= 3800:
                    next_level = 1
        rightmove = False
        leftmove = False
        upmove = False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_0:
                pygame.mixer.music.set_volume(0)
            if event.key == K_1:
                pygame.mixer.music.set_volume(1)
            if event.key == K_r:
                display.blit(background_image, (0, 0))
                player_rect = pygame.Rect(69, 69, 10, 22)
            if event.key == K_q:
                pygame.quit()
                sys.exit()
            if event.key == K_RIGHT or event.key == K_d:
                if player_rect.x < 3800:
                    rightmove = True
                else:
                    rightmove = False
                    player_rect.x -= 0.5
            if event.key == K_LEFT or event.key == K_a:
                if player_rect.x < 3800:
                    leftmove = True
                else:
                    leftmove = False
            if event.key == K_UP or event.key == K_SPACE:
                if air_timer < 5 and player_rect.x < 3800:
                    jump_sound.play()
                    player_y_momentum = -5

        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                rightmove = False
            if event.key == K_LEFT or event.key == K_a:
                leftmove = False
            if event.key == K_UP or event.key == K_SPACE:
                upmove == False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)

player_rect = pygame.Rect(144, 16*61, 10, 22)
i = 0
pygame.mixer.music.load(r'GLITCHBOI AND DREAMER\sounds\TrackTribe - Walk Through the Park.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)
background_image = pygame.image.load(r"GLITCHBOI AND DREAMER\images\stestfiles\Sarlat-medieval-city-by-night-16.jpg")
walk_sound = [pygame.mixer.Sound(r'GLITCHBOI AND DREAMER\sounds\concretewalk_0.wav'), pygame.mixer.Sound(r'GLITCHBOI AND DREAMER\sounds\concretewalk_1.wav'), pygame.mixer.Sound('GLITCHBOI AND DREAMER\sounds\concretewalk_2.wav'),pygame.mixer.Sound(r'GLITCHBOI AND DREAMER\sounds\concretewalk_3.wav')]

d = 0
interactive_rects = []

enemy_rects = []

while next_level == 1: # game loop

    display.blit(background_image, (0, -250))

    if walk_sound_timer > 0:
        walk_sound_timer -= 1

    true_scroll[0] += (player_rect.x - true_scroll[0] - 145)/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 89)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # for background_object in background_objects:
    #     obj_rect = pygame.Rect(background_objects[1][0] - scroll[0]*background_object[0], background_object[1][1] - scroll[1]*background_object[0], background_object[1][2], background_object[1][3])
    #     if background_object[0] == 0.5:
    #         pygame.draw.rect(display, (255, 255, 0), obj_rect)
    #     else:
    #         pygame.draw.rect(display, (255, 0, 0), obj_rect)

    # message('x coordinate ' + str(player_rect.x), 'white', [5, 5])
    # message('y coordinate ' + str(player_rect.y), 'white', [5, 25])

    player_movement = [0, 0]
    if rightmove:
        player_movement[0] += 2
    if leftmove:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    if player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False
    if player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True
    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
        if player_movement[0] != 0:
            if walk_sound_timer == 0:
                walk_sound_timer = 30
                random.choice(walk_sound).play()
    else:
        air_timer += 1

    if collisions['top']:
        player_y_momentum = -player_y_momentum * 0.75

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_image_id = animation_database[player_action][player_frame]
    player_image = animation_frames[player_image_id]
    display.blit(pygame.transform.flip(player_image, player_flip, False), (player_rect.x - scroll[0], player_rect.y - scroll[1])) # render player

    for interactive in interactive_rects:
        if interactive[1] == 'coin':
            display.blit(coinimg, (interactive[0][0] - scroll[0], interactive[0][1] + 14 - scroll[1]))
        if interactive[1] == 'diamond':
            display.blit(diamondimg, (interactive[0][0] - scroll[0], interactive[0][1] + 14 - scroll[1]))
        if player_rect.colliderect(interactive[0]) == True:
            if interactive[1] == 'coin':
                coin_sound.play()
                score += 1
                index = interactive_rects.index(interactive)
                interactive_rects.pop(index)
            if interactive[1] == 'diamond':
                diamond_sound.play()
                score += 5
                index = interactive_rects.index(interactive)
                interactive_rects.pop(index)

    tile_rects = []
    y = 0
    for row in game_map_2:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(brickimg, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
                tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile == '2':
                display.blit(balcony_left_img, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
                tile_rects.append(pygame.Rect(x*TILE_SIZE, (y+0.875)*TILE_SIZE, TILE_SIZE, 2))
            if tile == '3':
                display.blit(balcony_right_img, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
                tile_rects.append(pygame.Rect(x*TILE_SIZE, (y+0.875)*TILE_SIZE, TILE_SIZE, 2))
            if tile == '4':
                display.blit(balcony_middle_img, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
                tile_rects.append(pygame.Rect(x*TILE_SIZE, (y+0.875)*TILE_SIZE, TILE_SIZE, 2))
            if tile == '5':
                display.blit(lamp_left_img, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
            if tile == '6':
                display.blit(lamp_right_img, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
            if tile == '7' and d == 0:
                interactive_rects.append([pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 'coin'])
            if tile == '8' and d == 0:
                interactive_rects.append([pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 'diamond'])
            x += 1
        y += 1
    d = 1

    message('score: ' + str(score), 'violet', [5, 5])

    # if player_rect.y > 400:
    #     display.blit(background_image, (0, 0))
    #     message('GAME OVER', 'yellow', [130, 40])
    #     message('Press R to restart, or Q to quit', 'red', [20, 140])
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == KEYDOWN:
    #             if event.key == K_r:
    #                 display.blit(background_image, (0, 0))
    #                 player_rect = pygame.Rect(69, 69, 10, 22)
    #             if event.key == K_q:
    #                 pygame.quit()
    #                 sys.exit()

    if player_rect.y <= 16 and player_rect.x >= 64 and player_rect.x <= 192:
        message('YOU WON', 'blue', [140, 40])
        message('PRESS N TO GO TO NEXT LEVEL', 'purple', [10, 140])
        player_rect = pygame.Rect(player_rect.x, player_rect.y, 10, 22)
        if i == 0:
            pygame.mixer.music.set_volume(0)
            win_sound.play(1)
            i = 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_n and player_rect.y <= 16 and player_rect.x >= 64 and player_rect.x <= 192:
                    next_level = 2
        rightmove = False
        leftmove = False
        upmove = False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_0:
                pygame.mixer.music.set_volume(0)
            if event.key == K_1:
                pygame.mixer.music.set_volume(1)
            if event.key == K_r:
                display.blit(background_image, (0, -250))
                player_rect = pygame.Rect(144, 704, 10, 22)
            if event.key == K_q:
                pygame.quit()
                sys.exit()
            if event.key == K_RIGHT or event.key == K_d:
                if player_rect.x < 3800:
                    rightmove = True
                else:
                    rightmove = False
                    player_rect.x -= 0.5
            if event.key == K_LEFT or event.key == K_a:
                if player_rect.x < 3800:
                    leftmove = True
                else:
                    leftmove = False
            if event.key == K_UP or event.key == K_SPACE:
                if air_timer < 5 and player_rect.x < 3800:
                    jump_sound.play()
                    player_y_momentum = -5

        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                rightmove = False
            if event.key == K_LEFT or event.key == K_a:
                leftmove = False
            if event.key == K_UP or event.key == K_SPACE:
                upmove == False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)

player_rect = pygame.Rect(69, 36, 10, 22)
i = 0
pygame.mixer.music.load(r'GLITCHBOI AND DREAMER\sounds\banger tunez 4ev.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)
background_image = pygame.image.load(r"GLITCHBOI AND DREAMER\images\stestfiles\unnamed.jpg")
walk_sound = [pygame.mixer.Sound(r'GLITCHBOI AND DREAMER\sounds\metalwalk_0.wav'), pygame.mixer.Sound(r'GLITCHBOI AND DREAMER\sounds\metalwalk_1.wav'), pygame.mixer.Sound('GLITCHBOI AND DREAMER\sounds\metalwalk_2.wav'),pygame.mixer.Sound(r'GLITCHBOI AND DREAMER\sounds\metalwalk_3.wav')]

d = 0
interactive_rects = []

while next_level == 2: # game loop

    display.blit(background_image, (0, 0))

    if walk_sound_timer > 0:
        walk_sound_timer -= 1

    true_scroll[0] += (player_rect.x - true_scroll[0] - 145)/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 89)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # for background_object in background_objects:
    #     obj_rect = pygame.Rect(background_objects[1][0] - scroll[0]*background_object[0], background_object[1][1] - scroll[1]*background_object[0], background_object[1][2], background_object[1][3])
    #     if background_object[0] == 0.5:
    #         pygame.draw.rect(display, (255, 255, 0), obj_rect)
    #     else:
    #         pygame.draw.rect(display, (255, 0, 0), obj_rect)

    # message('x coordinate ' + str(player_rect.x), 'white', [5, 5])
    # message('y coordinate ' + str(player_rect.y), 'white', [5, 25])

    player_movement = [0, 0]
    if rightmove:
        player_movement[0] += 2
    if leftmove:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum -= 0.2
    if player_y_momentum < -3:
        player_y_momentum = -3

    if player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False
    if player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True
    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['top']:
        player_y_momentum = 0
        air_timer = 0
        if player_movement[0] != 0:
            if walk_sound_timer == 0:
                walk_sound_timer = 30
                random.choice(walk_sound).play()
    else:
        air_timer += 1

    if collisions['bottom']:
        player_y_momentum = -player_y_momentum * 0.75

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_image_id = animation_database[player_action][player_frame]
    player_image = animation_frames[player_image_id]
    display.blit(pygame.transform.flip(player_image, player_flip, True), (player_rect.x - scroll[0], player_rect.y - scroll[1])) # render player

    tile_rects = []
    y = 0
    for row in game_map_3:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(metalimg1, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
                tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile == '2':
                display.blit(metalimg2, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
                tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile == '3':
                display.blit(glassimg, (x*TILE_SIZE - scroll[0], y*TILE_SIZE - scroll[1]))
            if tile == '4' and d == 0:
                interactive_rects.append([pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 'coin'])
            if tile == '5' and d == 0:
                interactive_rects.append([pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 'diamond'])
            x += 1
        y += 1
    d = 1

    for interactive in interactive_rects:
        if interactive[1] == 'coin':
            display.blit(coinimg, (interactive[0][0] - scroll[0], interactive[0][1] - scroll[1]))
        if interactive[1] == 'diamond':
            display.blit(diamondimg, (interactive[0][0] - scroll[0], interactive[0][1] - scroll[1]))
        if player_rect.colliderect(interactive[0]) == True:
            if interactive[1] == 'coin':
                score += 1
                index = interactive_rects.index(interactive)
                interactive_rects.pop(index)
            if interactive[1] == 'diamond':
                score += 5
                index = interactive_rects.index(interactive)
                interactive_rects.pop(index)

    if player_rect.y < 0:
        display.blit(background_image, (0, 0))
        message('YOU DIED', 'yellow', [130, 40])
        message('Press R to respawn, or Q to quit', 'red', [20, 140])
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    display.blit(background_image, (0, 0))
                    player_rect = pygame.Rect(69, 36, 10, 22)
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

    if player_rect.y <= 16 and player_rect.x >= 64 and player_rect.x <= 192:
        message('YOU WON', 'blue', [140, 40])
        message('PRESS N TO GO TO NEXT LEVEL', 'purple', [10, 140])
        player_rect = pygame.Rect(player_rect.x, player_rect.y, 10, 22)
        if i == 0:
            pygame.mixer.music.set_volume(0)
            win_sound.play(1)
            i = 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_n and player_rect.x >= 3800:
                    next_level = 3
        rightmove = False
        leftmove = False
        upmove = False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_0:
                pygame.mixer.music.set_volume(0)
            if event.key == K_1:
                pygame.mixer.music.set_volume(1)
            if event.key == K_r:
                display.blit(background_image, (0, 0))
                player_rect = pygame.Rect(69, 36, 10, 22)
            if event.key == K_q:
                pygame.quit()
                sys.exit()
            if event.key == K_RIGHT or event.key == K_d:
                if player_rect.x < 3800:
                    rightmove = True
                else:
                    rightmove = False
                    player_rect.x -= 0.5
            if event.key == K_LEFT or event.key == K_a:
                if player_rect.x < 3800:
                    leftmove = True
                else:
                    leftmove = False
            if event.key == K_UP or event.key == K_SPACE:
                if air_timer < 5 and player_rect.x < 3800:
                    jump_sound.play()
                    player_y_momentum = +5

        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                rightmove = False
            if event.key == K_LEFT or event.key == K_a:
                leftmove = False
            if event.key == K_UP or event.key == K_SPACE:
                upmove == False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)
