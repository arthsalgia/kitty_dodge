#THINGS TO DO
# 2 player mode
#---> make kuromi 2nd player
#---> let them pass over each other and let 2nd player be using wasd

import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()

pygame.display.set_caption("Kitty Dodge")

width = 1400
height = 800
window = pygame.display.set_mode((width, height))
background = pygame.image.load("bg.jpg")
player = pygame.image.load("image-hello-kitty-resized1.png")
player_vel = 8
font = pygame.font.SysFont("Janda Happy Day", 60)
flower_width = 30
flower_height = 30
flower_draw = pygame.image.load("flower-resized.png")
flower_x = random.randint(0, width - flower_width)
flower = pygame.Rect(flower_x, -flower_height, flower_width, flower_height)
kitty_heart_image = pygame.image.load("heart-resized.png")
kitty_heart_width = 50
kitty_heart_height = 39
kitty_heart_info = pygame.Rect(100 + kitty_heart_width, -kitty_heart_height, kitty_heart_width, kitty_heart_height)
flowers_x = []
high_score_file = open("high_score.txt", "a+")
high_score_rec = []
high_score_file.seek(0)
kuromi_heart_image = pygame.image.load("kuromi_heart.png")
kuromi_heart_width = 65
kuromi_heart_height = 65
kuromi_heart_info = pygame.Rect(100 + kuromi_heart_width, -kuromi_heart_height, kuromi_heart_width, kuromi_heart_height)
for line in high_score_file:
    high_score_rec.append(int(line))
high_score_rec.sort()
high_score = high_score_rec[-1]
hit_sfx = pygame.mixer.Sound("punch_sfx.mp3")
game_lost = pygame.mixer.Sound("game_lost_sfx.mp3")
kuromi = pygame.image.load("kuromi_resized_s2.png")
game_win = pygame.mixer.Sound("game_win.mp3")


def random_flower_x(flower_number):
    count = 0
    flowers_x.clear()
    while count != flower_number:
        x = random.randint(0 + flower_width, width - 30 - flower_width)
        y = random.randint(0 + flower_width, width - 30 - flower_width)
        if abs(x - y) > flower_width:
            flowers_x.append(x)
            count += 1
            if count < flower_number:
                flowers_x.append(y)
                count += 1
    flowers_x.sort()

    for i in range(1,flower_number):
        if flowers_x[i] - flowers_x[i-1] < 30:
            flowers_x[i-1] -= 25
            flowers_x[i] += 25     
    return flowers_x


def draw(playerinfo, elapsed_time, flowers, kitty_hearts, kuromi_info, kuromi_heart):
    window.blit(background, (0, 0))
    window.blit(player, (playerinfo.x, playerinfo.y))
    time_text = font.render(f"Time: {round(elapsed_time)}s", 1 , "black")
    window.blit(time_text, (10, 10))
    high_score_text = font.render(f"High Score: {high_score}s", 1 , "black")
    window.blit(high_score_text, (10, 50))
    window.blit(kuromi, (kuromi_info.x, kuromi_info.y))

    i = 0
    for _ in range(kitty_hearts):
        window.blit(kitty_heart_image, (width - kitty_heart_width - i, height - kitty_heart_height))
        i += 75

    o = 0
    for _ in range(kuromi_heart):
        window.blit(kuromi_heart_image, (150 + kuromi_heart_width - o, height - kuromi_heart_height + 10))
        o += 75

    for flower in flowers:
        window.blit(flower_draw, (flower.x, flower.y))

    pygame.display.update()


def main():
    run = True
    playerinfo = pygame.Rect(750,675,98,110)
    kuromi_info = pygame.Rect(650, 675, 98, 110)
    clock = pygame.time.Clock()
    start_time = time.time()
    global elapsed_time
    elapsed_time = 0
    kitty_life_count = 3
    flower_add_increment = 2500
    flower_count = 0
    kitty_hearts = 0 
    kuromi_heart = 0
    flowers = []
    kitty_hit = False
    kuromi_hit = False
    check = 0
    kuromi_life_count = 3

    while run:
        flower_count += clock.tick(60)
        elapsed_time =time.time() - start_time
        flower_number = random.randint(3,5)


        if flower_count > flower_add_increment:
                for i in range(flower_number):
                    randflower = random_flower_x(flower_number)
                    flower_x = randflower[i]
                    flower = pygame.Rect(flower_x, -flower_height, flower_width, flower_height)
                    flowers.append(flower)
                flower_add_increment = max(700, flower_add_increment - 50)
                flower_count = 0    

        
        if check == 0:
            for _ in range(3):
                kuromi_heart += 1
                kitty_hearts += 1
                check = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        for flower in flowers[:]:
            flower.y += random.randint(1,12)
            if flower.y >height:
                flowers.remove(flower)
            elif flower.y + flower.height >= playerinfo.y and flower.colliderect(playerinfo):
                flowers.remove(flower)
                kitty_hit = True
                break
            elif flower.y + flower.height >= kuromi_info.y and flower.colliderect(kuromi_info):
                flowers.remove(flower)
                kuromi_hit = True
                break
            

        if kuromi_hit:
            hit_sfx.play()
            kuromi_heart -= 1
            draw(playerinfo, elapsed_time, flowers, kitty_hearts, kuromi_info, kuromi_heart)
            kuromi_life_count -= 1
            kuromi_hit = False
            

        if kitty_hit:
            hit_sfx.play()
            kitty_hearts -= 1
            draw(playerinfo, elapsed_time, flowers, kitty_hearts, kuromi_info, kuromi_heart)
            kitty_life_count -= 1
            kitty_hit = False
            
        if kitty_life_count == 0:
            kitty_lost_text = font.render("Kuromi won!!", 1 , "black")
            window.blit(kitty_lost_text, (width/2 - kitty_lost_text.get_width()/2, height/2 - kitty_lost_text.get_height()/2))
            game_win.play()
            pygame.display.update()
            pygame.time.delay(4000)
            break
        
        if kuromi_life_count == 0:
            kuromi_lost_text = font.render("Hello kitty won!!", 1 , "black")
            window.blit(kuromi_lost_text, (width/2 - kuromi_lost_text.get_width()/2, height/2 - kuromi_lost_text.get_height()/2))
            game_win.play()
            pygame.display.update()
            pygame.time.delay(4000)
            break

        """for event in pygame.event.get():
            if event.type == pygame.K_UP:
                playerinfo.y += -player_vel"""
        
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and playerinfo.x - player_vel >= 1 :
            playerinfo.x += -player_vel
        if keys[pygame.K_RIGHT] and playerinfo.x + player_vel + 98 <= width:
            playerinfo.x -= -player_vel
        if keys[pygame.K_UP] and playerinfo.y - player_vel >= 1:
            playerinfo.y += -player_vel
        if keys[pygame.K_DOWN] and playerinfo.y + player_vel + 110 <= height:
            playerinfo.y -= -player_vel
        if keys[pygame.K_w] and kuromi_info.y - player_vel >= 1:
            kuromi_info.y += -player_vel
        if keys[pygame.K_s] and kuromi_info.y + player_vel + 110 <= height:
            kuromi_info.y -= -player_vel
        if keys[pygame.K_a] and kuromi_info.x - player_vel >= 1:
            kuromi_info.x += -player_vel
        if keys[pygame.K_d] and kuromi_info.x + player_vel + 95 <= width:
            kuromi_info.x -= -player_vel
        
        draw(playerinfo, elapsed_time, flowers, kitty_hearts, kuromi_info, kuromi_heart)

    pygame.quit()

if __name__ == "__main__":
    main()
    high_score_file.write(str(round(elapsed_time))+ "\n")
    high_score_file.close()