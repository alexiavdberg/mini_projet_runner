# game data
import pgzrun

from pgzhelper import *
from random import randint

WIDTH = 800
HEIGHT = 600

GROUND = 458
GRAVITY = 200

NUMBER_OF_BACKGROUND = 2
GAME_SPEED = 100
JUMP_SPEED = 220

ENNEMY_SPEED = 50

screen_title_visible = True
did_we_click = False
is_paused = False

# hero initialisation
hero = Actor("clippy", anchor=('middle', 'bottom'))
hero.pos = (64, GROUND)
hero_speed = 0
lives = []
life_points = 3

# enemies initialisations
BOX_APPARITION = (2, 5)
next_box_time = randint(BOX_APPARITION[0], BOX_APPARITION[1])
boxes = []
box_speed = [0,1]


# background inititalisation
backgrounds_bottom = []
backgrounds_top = []

# start screen background initialisation
scrtitle_bg = Actor("start_bg")
scrtitle_bg.scale = 0.50
scrtitle_bg.pos = [WIDTH/2, HEIGHT/2] 

# start button initialisation
scrtitle_button = Actor("start")
scrtitle_button.scale = 0.30
scrtitle_button.pos = [WIDTH/2, (HEIGHT/2)+200]

# start game title initialisation
scrtitle_gametitle = Actor("title")
scrtitle_gametitle.scale = 0.30
scrtitle_gametitle.pos = [WIDTH/2, HEIGHT/2] 

# pause screen background init
pausescreen_bg = Actor("pause_screen")
pausescreen_bg.pos = [WIDTH/2, HEIGHT/2]
pause_button = Actor("pause")
pause_button.scale = 0.30
pause_button.pos = [WIDTH/2, 70]

for n in range(NUMBER_OF_BACKGROUND):
    bg_b = Actor("backg_3", anchor=('left', 'top'))
    bg_b.pos = n * WIDTH, 0
    backgrounds_bottom.append(bg_b)

    bg_t = Actor("backg_4", anchor=('left', 'top'))
    bg_t.pos = n * WIDTH, 0
    backgrounds_top.append(bg_t)

for x in range(660, 795, 45):
    for y in range(555, 600, 50):
        heart = Actor('word')
        heart.pos = [x, y]
        lives.append(heart)

def draw():
    global screen_title_visible

    if screen_title_visible == True:
        draw_scrtitle()
    else:
        draw_game()

    if is_paused == True:
        draw_pause_screen()

def draw_scrtitle():
    scrtitle_bg.draw()
    scrtitle_button.draw()
    scrtitle_gametitle.draw()

def draw_pause_screen():
    pausescreen_bg.draw()
    pause_button.draw()
    screen.draw.text("PRESS 'P' TO RESUME", fontsize = 90, center=[WIDTH / 2, 470], color=("Blue"))

def draw_game():

    for bg in backgrounds_bottom:
        bg.draw()

    for bg in backgrounds_top:
        bg.draw()

    for box in boxes:
        box.draw()

    for heart in lives: #afficher coeurs dans draw 
        heart.draw()

    hero.draw()

def update_screen_title() :
    global screen_title_visible, did_we_click
    
    if not music.is_playing('windows_error'):
        music.play_once('windows_error')
        music.set_volume(0.5)
        music.get_volume()
    
def update(dt):
    global screen_title_visible, update_game, update_screen_title

    if screen_title_visible == True:
        update_screen_title()
    else:
        update_game(dt)

    if is_paused == True:
        draw_pause_screen()

def update_game(dt):
    global next_box_time, next_box_time, life_points, heart, lives, hero_speed

    # enemies update
    # box
    next_box_time -= dt
    if next_box_time <= 0:
        box = Actor("internet_explorer", anchor=('center', 'bottom'))
        box.pos = WIDTH, GROUND
        boxes.append(box)
        next_box_time = randint(BOX_APPARITION[0], BOX_APPARITION[1])

    for box in boxes:
        x, y = box.pos
        x -= GAME_SPEED * dt
        box.pos = x, y

        global box_speed

        new_x = box.pos[0] + box_speed[0] 
        new_y = box.pos[1] + box_speed[1] 

        box.pos = [new_x, new_y] 

        if box.top >= 393 :
            invert_vertical_speed()

        if box.bottom <= GROUND :
            invert_vertical_speed()

        if box.colliderect(hero):
            life_points = life_points - 1
            lives.remove(lives[-1])
            boxes.remove(box)
            if life_points == 0:
                exit()

    if boxes:
        if boxes[0].pos[0] <= - 32:
            boxes.pop(0)

    # hero update
    hero_speed -= GRAVITY * dt
    x, y = hero.pos
    y -= hero_speed * dt

    if y > GROUND:
        y = GROUND
        hero_speed = 0

    hero.pos = x, y

    # bg update
    if backgrounds_bottom[0].pos[0] <= - WIDTH:
        bg = backgrounds_bottom.pop(0)
        bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
        backgrounds_bottom.append(bg)

    if is_paused == False:
        for bg in backgrounds_top:
            x, y = bg.pos
            x -= GAME_SPEED * dt
            bg.pos = x, y
    else:
        for bg in backgrounds_top:
            x, y = bg.pos
            bg.pos = x, y

    if backgrounds_top[0].pos[0] <= - WIDTH:
        bg = backgrounds_top.pop(0)
        bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
        backgrounds_top.append(bg)

def on_key_down(key):
    global hero_speed, is_paused

    # jump
    if key == keys.SPACE:
        if hero_speed <= 0 and hero.pos == (64, GROUND):
            hero_speed = JUMP_SPEED
            
    # pause
    if key == keys.P:
        if is_paused == False:
            is_paused = True
        elif is_paused == True:
            is_paused = False
        
def on_mouse_down(pos, button):
    global screen_title_visible, did_we_click

    if button == mouse.LEFT and not did_we_click and scrtitle_button.collidepoint_pixel(pos):
        did_we_click = True
        screen_title_visible = False

def invert_vertical_speed():
    box_speed[1] = box_speed[1] * -1
     
pgzrun.go()