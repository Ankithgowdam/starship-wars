import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Starships")

Border = pygame.Rect(WIDTH//2 -5, 0, 0, HEIGHT)

hit_sound = pygame.mixer.Sound(os.path.join('Assets','hit.mp3'))
fire_sound = pygame.mixer.Sound(os.path.join('Assets','fire.mp3'))
blast_sound = pygame.mixer.Sound(os.path.join('Assets','blast.mp3'))

health_font = pygame.font.SysFont('comicsans', 30)
winner_font = pygame.font.SysFont('comicsans', 80)


White = (255,255,255)
black = (0,0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,60
speed = 4
bullet_speed = 7
MAX_bullets = 3

s1_HIT = pygame.USEREVENT + 1
s2_HIT = pygame.USEREVENT + 2

spaceship1 = pygame.image.load(os.path.join("Assets",'1.png'))
spaceship2 = pygame.image.load(os.path.join("Assets",'2.png'))

ship1 = pygame.transform.scale(spaceship1,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
ship2 = pygame.transform.scale(spaceship2,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

space = pygame.transform.scale(pygame.image.load(os.path.join('Assets',"space.jpg")), (WIDTH,HEIGHT))

def draw_window(s1,s2, s1_bullets, s2_bullets, s1_health, s2_health):
    
    WIN.blit(space, (0,0))
    pygame.draw.rect(WIN, black, Border)

    s1_health_text = health_font.render("Health: " + str(s1_health), 1, White)
    s2_health_text = health_font.render("Health: " + str(s2_health), 1, White)
    WIN.blit(s1_health_text, (WIDTH - s1_health_text.get_width() - 10, 10))
    WIN.blit(s2_health_text, (10, 10))

    
    WIN.blit(ship1,(s1.x,s1.y))
    WIN.blit(ship2,(s2.x,s2.y))

    for bullet in s1_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in s2_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def s1move(key_pressed,s1):
    if key_pressed[pygame.K_a] and s1.x > 0:
        s1.x -= speed
    if key_pressed[pygame.K_w] and s1.y - speed > 0:
        s1.y -= speed
    if key_pressed[pygame.K_d] and s1.x + speed + s1.width < Border.x:
        s1.x += speed
    if key_pressed[pygame.K_s] and s1.y + speed + s1.width < HEIGHT - 5:
        s1.y += speed

def s2move(key_pressed,s2):
    if key_pressed[pygame.K_LEFT] and s2.x > Border.x + Border.width:
        s2.x -= speed
    if key_pressed[pygame.K_UP] and s2.y > 0:
        s2.y -= speed
    if key_pressed[pygame.K_RIGHT] and s2.x + s2.width < WIDTH:
        s2.x += speed
    if key_pressed[pygame.K_DOWN] and s2.y + s2.height < HEIGHT:
        s2.y += speed

def handle_bullets(s1_bullets, s2_bullets, s1, s2):
    for bullet in s1_bullets:
        bullet.x += bullet_speed
        if s2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(s2_HIT))
            s1_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            s1_bullets.remove(bullet)

    for bullet in s2_bullets:
        bullet.x -= bullet_speed
        if s1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(s1_HIT))
            s2_bullets.remove(bullet)
        elif bullet.x < 0:
            s2_bullets.remove(bullet)

def winner(text):
    draw_text = winner_font.render(text, 1, White)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    s1 = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    s2 = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    s1_bullets = []
    s2_bullets = []

    s1_health = 10
    s2_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(s1_bullets) < MAX_bullets:
                    bullet =  pygame.Rect(s1.x + s1.width, s1.y + s1.height//2 -2, 10, 5)
                    s1_bullets.append(bullet)
                    fire_sound.play()

                if event.key == pygame.K_RCTRL and len(s2_bullets) < MAX_bullets:
                    bullet =  pygame.Rect(s2.x, s2.y + s2.height//2 -2, 10, 5)
                    s2_bullets.append(bullet)
                    fire_sound.play()

            if event.type == s1_HIT:
                s2_health -= 1
                hit_sound.play()
            
            if event.type == s2_HIT:
                s1_health -= 1
                hit_sound.play()

        text = ""
        if s1_health <= 0:
            text = "Red Wins"
            blast_sound.play()

        if s2_health <= 0:
            text = "Yellow Wins"
            blast_sound.play()

        if text != "":
            winner(text)
            break
       
        key_pressed = pygame.key.get_pressed()
        s1move(key_pressed,s1)
        s2move(key_pressed,s2)

        handle_bullets(s1_bullets, s2_bullets, s1, s2)
    
        draw_window(s1,s2,s1_bullets,s2_bullets, s1_health, s2_health)
       
    # pygame.Quit()
    main()

if __name__ == "__main__":
    main()