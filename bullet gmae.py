import pygame, sys, random,time
from pygame.locals import *

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
#생명 이미지
big_heart_image = pygame.image.load("heart.png").convert()
#생명 축소
heart_image = pygame.transform.scale(big_heart_image, (15,15))
#모든 이미지 하얀색 제거
bullet_image.set_colorkey((255,255,255))
people_image.set_colorkey((255,255,255))
heart_image.set_colorkey((255,255,255))

#폰트 저장
font = pygame.font.SysFont("notosanscjkkr",400)
S = pygame.font.SysFont("notosanscjkkr",300)
E = pygame.font.SysFont("notosanscjkkr",200)
#텍스트들
text1 = font.render("1",True,(0,0,0))
text2 = font.render("2",True,(0,0,0))
text3 = font.render("3",True,(0,0,0))
start = S.render("START",True,(0,0,0))
gameover = E.render("GAME OVER",True,(0,0,0))

#총알을 일정 좌표 뒤 생성하는 코드
bullet_limit = 150
#총알을 일정 갯수 만큼만 소환하게 하는 코드
spawn_limit = 2
#위에 리미트를 증가하는 만큼 풀리게 하는 코드
limit = 0
#생명 기본 값
draw_heart = 5

# 총알 구성
class Bullet:
    #좌표 지정
    def __init__(self): 
        self.x = random.randint(0,980)
        self.y = -60
        #1일 경우 속도가 빠른 총알 생성
        self.fast = random.randint(0,20)
        #1일 경우 x좌표가 마구 움직이는 총알 생성
        self.potal = random.randint(0,50)
        #위에 x좌표 움직이는 기준
        self.pmove = random.randint(10,100)
        self.potalr = 0

    #slef.fast가 1일 경우 빠른 y좌표를 8씩 이동 시키고 아니라면 2씩 이동
    def move(self):
        if self.fast == 1:
            self.y += 8
        elif self.fast == 20:
            self.y += 0.5
        else:
            self.y += 2
        if self.potal == 1:

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
        if pressed_keys[K_RIGHT] and self.x < 970:
            self.x += 2
        if pressed_keys[K_LEFT] and self.x > 0:
            self.x -= 2

    #사람 그리기
    def draw(self):
        screen.blit(people_image,(self.x,self.y))

    #충돌 감지
    def hit_by(self,bullet):
        return pygame.Rect(self.x, self.y,30,60).collidepoint((bullet.x+10, bullet.y+60))

#생명 구성
class Heart:
    #첫 생명 좌표 지정
    def __init__(self):
        self.x = 5
        self.y = 680

    #생명 그리기
    def draw(self):
        for i in range(draw_heart):
            screen.blit(heart_image,(self.x+i*20,self.y))

#텍스트 그리는 함수
def textDraw(x,y,text):
    screen.fill((255,255,255))
    screen.blit(text,(x,y))
    pygame.display.update()

#총알을 담아놓는 리스트
bullets = []
#총알 하나를 미리 소환하지 않으면 오류가 나서 미리 만든 총알
bullets.append(Bullet())
#사람 생성
human = Human()
#생명 생성
heart = Heart()

#게임 시작 전 준비 타임 
textDraw(420,220,text3)
time.sleep(1)
pygame.init()

textDraw(420,220,text2)
time.sleep(1)
pygame.init()

textDraw(420,220,text1)
time.sleep(1)
pygame.init()

textDraw(170,220,start)
time.sleep(0.5)
pygame.init()

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
    screen.blit(text3,(370,240))
    #화면 초기화
    screen.fill((255,255,255))
    #사람 움직이기
    human.move()
    #사람 그리기
    human.draw()
    #생명 그리기
    heart.draw()

    i = 0
    while i < len(bullets):
        #총알 이동 및 그리기
        bullets[i].move()
        bullets[i].draw()
        
        #총알이 화면 밖으로 나가면 삭제
        if bullets[i].bullet_delete():
            del bullets[i]
            i -= 1

        #총알이 사람 몸과 만나면 생명을 1 줄이고 총알 삭제
        if human.hit_by(bullets[i]):
            draw_heart -= 1
            del bullets[i]
            i -= 1
            
        i += 1
    
    pygame.display.update()

    #생명이 0일 경우 화면에 "GAME OVER"을 쓰고 프로그램 정지
    if draw_heart == 0:
        textDraw(80,240,gameover)
        time.sleep(5)
        pygame.init()
        break
    
pygame.quit()
