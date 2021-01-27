import pygame, sys, random
from pygame.locals import *
from time import sleep
pygame.init()
pygame.display.set_caption("bullet game")
screen = pygame.display.set_mode((1000,700))
clock = pygame.time.Clock()
#총알의 이미지
big_bullet_image = pygame.image.load("bullet.png").convert()
#총알 축소
bullet_image = pygame.transform.scale(big_bullet_image, (20,60))
#사람 이미지
big_people_image = pygame.image.load("people.png").convert()
#사람 축소
people_image = pygame.transform.scale(big_people_image, (30,60))
#총알을 일정 좌표 뒤 생성하는 코드
bullet_limit = 150
#총알을 일정 갯수 만큼만 소환하게 하는 코드
spawn_limit = 2
#위에 리미트를 증가하는 만큼 풀리게 하는 코드
limit = 0

# 총알 구성
class Bullet:
    #좌표 지정
    def __init__(self): 
        self.x = random.randint(0,980)
        self.y = -60

    #아래 쪽으로 가기 위해서 y 좌표 2씩 올리기
    def move(self): 
        self.y += 2

    #그리기
    def draw(self):
        screen.blit(bullet_image,(self.x,self.y))
        
    #y 좌표가 900이상가면 True를 보냄
    def bullet_delete(self): 
        return self.y > 900

    #총알이 y좌표가 150 - @보다 높다면 True를 보냄
    def bullet_spawn(self): 
        return self.y > bullet_limit + (limit / 30)

#사람 구성
class Human:
    #처음 좌표 지정
    def __init__(self):
        self.x = 470
        self.y = 640

    #사람 움직이기
    def move(self):
        if pressed_keys[K_RIGHT]:
            self.x += 2
        if pressed_keys[K_LEFT]:
            self.x -= 2

    #사람 그리기
    def draw(self):
        screen.blit(people_image,(self.x,self.y))

    #충돌 감지
    def hit_by(self,bullet):
        return pygame.Rect(self.x, self.y,30,60).collidepoint((bullet.x, bullet.y))

#총알을 담아놓는 리스트
bullets = []
#총알 하나를 미리 소환하지 않으면 오류가 나서 미리 만든 총알
bullets.append(Bullet())
#사람 생성
human = Human()

while 1:
    #1초에 120번 반복
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pressed_keys = pygame.key.get_pressed()

    #총알의 갯수가 2 + @보다 적거나 총알의  y좌표가 일정 수보다 높으면 총알 생성
    if len(bullets) < spawn_limit + (limit/30)/5 and bullets[len(bullets)-1].bullet_spawn():
        bullets.append(Bullet())
        limit += 1

    screen.fill((255,255,255))
    human.move()
    human.draw()

    #총알 이동 및 삭제
    i = 0
    while i < len(bullets):
        bullets[i].move()
        bullets[i].draw()
        if bullets[i].bullet_delete():
            del bullets[i]
            i -= 1
        i += 1
    
    pygame.display.update()
