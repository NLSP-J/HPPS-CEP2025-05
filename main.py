import pygame as pg
import random, time
pg.init()
clock = pg.time.Clock()
import asyncio

black = (0, 0, 0)
win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Catching Recycables')

font = pg.font.Font(None, 30)
speed = 10
score = 0
running = True
lives = 3

player_size = 40
player_pos = [win_width / 2, win_height - player_size]
player_image = pg.image.load('./assets/images/recycle_bin.png')
player_image = pg.transform.scale(player_image,
                                  (player_size,player_size))

obj_size = 60
obj_data = []
obj = pg.image.load('./assets/images/fish_bone.png')
obj = pg.transform.scale(obj,(obj_size,obj_size))

heart_size = 60
heart_data = []
heart = pg.image.load('./assets/images/Heart.png')
heart = pg.transform.scale(heart, (heart_size, heart_size))

bag_size = 60
bag_data = []
bag = pg.image.load('./assets/images/recyclable_bag.png')
bag = pg.transform.scale(bag, (bag_size, bag_size))

bg_image = pg.image.load('./assets/images/background.png')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))

def check_lives():
    global lives, running
    if lives >= 1:
        running = True
    elif lives <= -1:
        running = False

def create_object(obj_data):
    if len(obj_data) < 4 and random.random() < 0.1:
        x = random.randint(0, win_width - obj_size)
        y = 0
        obj_data.append([x, y, obj])

def create_heart(heart_data):
    if len(heart_data) < 2 and random.random() < 0.01:
        x = random.randint(0, win_width - heart_size)
        y = 0
        heart_data.append([x, y, heart])

def create_bags(bag_data):
    if len(bag_data) < 6 and random.random() < 0.1:
        x = random.randint(0, win_width - bag_size)
        y = 0
        bag_data.append([x, y, bag])
    
def update_objects(obj_data):
    global score

    for object in obj_data:
        x, y, image_data = object
        if y < win_height:
            y += speed
            object[1] = y
            screen.blit(image_data, (x,y))
        else:
            obj_data.remove(object)

def update_hearts(heart_data):
    global lives
    for heart in heart_data:
        x, y, image_data = heart
        if y < win_height:
            y += speed
            heart[1] = y
            screen.blit(image_data, (x, y))
        else:
            heart_data.remove(heart)

def update_bags(bag_data):

    for bag in bag_data:
        x, y, image_data = bag
        if y < win_height:
            y += speed
            bag[1] = y
            screen.blit(image_data, (x, y))
        else:
            bag_data.remove(bag)

def collision_check(obj_data, player_pos):
    global running, lives
    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y,
                           player_size ,player_size)
        if player_rect.colliderect(obj_rect):
            time.sleep(0.5)
            lives -= 1
            check_lives()
            obj_data.remove(object)
            break

def bag_check(bag_data, player_pos):
    global score
    for bag in bag_data:
        x, y, image_data = bag
        player_x, player_y = player_pos[0], player_pos[1]
        bag_rect = pg.Rect(x, y, bag_size, bag_size)
        player_rect = pg.Rect(player_x, player_y,
                           player_size, player_size)
        if player_rect.colliderect(bag_rect):
            score += 2 
            bag_data.remove(bag)

def addlife_check(heart_data, player_pos):
    global lives
    for heart in heart_data:
        x, y, image_data = heart
        player_x, player_y = player_pos[0], player_pos[1]
        heart_rect = pg.Rect(x, y, heart_size, heart_size)
        player_rect = pg.Rect(player_x, player_y,
                              player_size, player_size)
        if player_rect.colliderect(heart_rect):
            lives += 1
            heart_data.remove(heart)

async def main():
    global running, player_pos
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            x,y=player_pos[0],player_pos[1]
            x-=10
            player_pos=[x,y]
        elif keys[pg.K_RIGHT]:
            x,y=player_pos[0],player_pos[1]
            x+=10
            player_pos=[x,y]
        elif keys[pg.K_UP]:
            x,y=player_pos[0],player_pos[1]
            y-=10
            player_pos=[x,y]
        elif keys[pg.K_DOWN]:
            x,y=player_pos[0],player_pos[1]
            y+=10
            player_pos=[x,y]

            
            
        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        text = f'Score: {score}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 40))

        text = f'Lives: {lives}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 300, win_height - 40))

        create_object(obj_data)
        update_objects(obj_data)
        create_heart(heart_data)
        update_hearts(heart_data)
        addlife_check(heart_data, player_pos)
        create_bags(bag_data)
        update_bags(bag_data)
        collision_check(obj_data, player_pos)
        bag_check(bag_data, player_pos)

        clock.tick(30)
        pg.display.flip()

        await asyncio.sleep(0)


asyncio.run(main())
