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
T = pygame.font.SysFont("notosansmonocjkkrregular",50)
#텍스트들
text1 = font.render("1",True,(0,0,0))
text2 = font.render("2",True,(0,0,0))
text3 = font.render("3",True,(0,0,0))
start = S.render("START",True,(0,0,0))
gameover = E.render("GAME OVER",True,(0,0,0))

#음악 관련 저장 및 종료 이벤트
hit = pygame.mixer.Sound("hit.ogg")
pygame.mixer.music.load("bgm2.wav")
hit.set_volume(0.5)
MUSIC_END_EVENT = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

#총알을 일정 좌표 뒤 생성하는 코드
bullet_limit = 70
#총알을 일정 갯수 만큼만 소환하게 하는 코드
spawn_limit = 5
#위에 리미트를 증가하는 만큼 풀리게 하는 코드
limit = 0
#생명 기본 값
draw_heart = 5
#타이머 변수
timer = 0

# 총알 구성
class Bullet:
    #좌표 지정
    def __init__(self): 
        self.x = random.randint(0,980)
        self.y = -60
        #총알이 내려가는 속도
        self.speed = 2 + (limit / 10)/1000
        #1일 경우 속도가 빠른 총알 생성
        #10일 경우 속도가 변하는 총알 생성
        self.fast = random.randint(0,10)
        #1일 경우 x좌표가 마구 움직이는 총알 생성
        self.potal = random.randint(0,20)
        #일정 y좌표마다 x좌표를 움직이거나 속도를 바꿔주는 변수
        self.mp = random.randint(50,200)
        #일정 좌표마다 초기화
        self.r = 0
        #1일 경우 유도탄 생성
        self.missile = random.randint(0,15)

    def move(self,human):
        #fast가 1일 경우 속도를 보통속도에 4배로 바꿈
        if self.fast == 1:
            self.speed = (2 + (limit/100)/100) * 4

        #fast가 10이고 r이 mp보다 크거나 같으면 랜덤으로 속도 변경
        elif self.fast == 5 and self.r >= self.mp:
            self.speed = random.randint(1,10)
            self.r = 0

        #potal이 1이고 r이 mp보다 크거나 같으면 조건에 따라 x좌표 변경
        if self.potal == 1 and self.r >= self.mp:
            #y 좌표가 200보다 크고 420보다 작으면 실행
            if self.y > 200 and self.y < 420:
                #x + 200이 1000보다 작고 x - 200이 0보다 사람의 x좌표 근처로 랜덤이동
                if self.x + 200 < 1000 and self.x - 200 > 0:
                    self.x = random.randint(human.x - 150, human.x + 150)
                    self.r = 0
                else:
                    #x + 200이 1000을 넘으면 사람의 x좌표 -150에서 오른쪽 벽까지 랜덤이동
                    if self.x + 200 > 1000:
                        self.x = random.randint(human.x - 150, 980)
                        self.r = 0
                    #x - 200이 0보다 작으면 사람의 x좌표 +150에서 왼쪽 벽까지 랜덤이동
                    elif self.x - 200 < 0:
                        self.x = random.randint(0, human.x + 150)
                        self.r = 0

            #y 좌표가 200보다 작으면 화면 이내에 x좌표로 랜덤이동
            elif self.y < 200:
                self.x = random.randint(0,930)
                self.r = 0
                    
            self.r = 0

        if self.missile == 1 and self.potal != 1:
            #y좌표 400까지는 사람을 따라다님
            if self.y < 400:
                self.x = human.x

            #y좌표가 400 초과 430 미만이면 속도를 0.5로 변경
            elif self.y > 400 and self.y < 430:
                self.speed = 1

            #y좌표가 430이 넘으면 속도를 10으로 변경
            elif self.y > 430:
                self.speed = 10

        #y를 변경
        self.y += self.speed
        self.r += self.speed

    #그리기
    def draw(self):
        screen.blit(bullet_image,(self.x,self.y))
        
    #y 좌표가 900이상가면 True를 보냄
    def bullet_delete(self): 
        return self.y > 900

    #총알이 y좌표가 150 - @보다 높다면 True를 보냄
    def bullet_spawn(self): 
        return self.y > bullet_limit - (limit / 30)

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
screen.fill((255,255,255))
textDraw(420,220,text3)
time.sleep(1)
pygame.init()

screen.fill((255,255,255))
textDraw(420,220,text2)
time.sleep(1)
pygame.init()

screen.fill((255,255,255))
textDraw(420,220,text1)
time.sleep(1)
pygame.init()

screen.fill((255,255,255))
textDraw(170,220,start)
time.sleep(0.5)
pygame.init()

#버티는 시간 측정
timer = time.time()

#음악 실행
pygame.mixer.music.load("bgm2.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

while 1:
    #1초에 120번 반복
    clock.tick(120)
    pc = 0
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #음악 종료시 다시 음악 실행
        if event.type == MUSIC_END_EVENT:
            pygame.mixer.music.load("bgm2.wav")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play()
            
    pressed_keys = pygame.key.get_pressed()

    #총알의 갯수가 2 + @보다 적거나 총알의  y좌표가 일정 수보다 높으면 총알 생성
    if len(bullets) < spawn_limit + limit/250 and bullets[len(bullets)-1].bullet_spawn():
        bullets.append(Bullet())
        limit += 3
        
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
        bullets[i].move(human)
        bullets[i].draw()
        
        #총알이 화면 밖으로 나가면 삭제
        if bullets[i].bullet_delete():
            del bullets[i]
            i -= 1

        #총알이 사람 몸과 만나면 생명을 1 줄이고 총알 삭제 그리고 소리 재생
        if human.hit_by(bullets[i]):
            draw_heart -= 1
            del bullets[i]
            i -= 1
            hit.play()
            
        i += 1

    
    pygame.display.update()

    #생명이 0일 경우 실행
    if draw_heart == 0:
        
        #시작 부터 현재까지에 시간 계산
        pc = round(time.time() - timer, 3)
        pcn = str(round(pc % 1, 3))
        pcm = str(int(pc / 60))

        #화면에 'GAME OVER', 플레이 시간 띄우기
        tp = T.render("play time [  "+pcm+" : "+str(round(pc%60))+" . "+pcn[2:]+"  ] ",True,(0,0,0))
        screen.fill((255,255,255))
        textDraw(80,240,gameover)
        textDraw(300,450,tp)
        pygame.mixer.music.load("bgm2.wav")
        pygame.mixer.music.set_volume(0.0)
        break

#게임 종료후 게임창을 닫을시에만 창 삭제
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
