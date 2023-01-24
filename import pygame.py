import pygame
import sys
import math
import random
import time
import os

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
GRAY = (102, 102, 102)
DEEP_BLUE = (0, 51, 204)
SKY_BLUE = (0, 255, 230)
OCEAN_BLUE = (51, 102, 255)
LEAF_GREEN = (51, 255, 51)
DARK_ORANGE = (255, 162, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FRAME_X = 700
FRAME_WIDTH = 400
FRAME_HEIGHT = 900
LINE_WIDTH = 5
KEY_SPACE = 10



class Note(): # 노트 클래스
    def __init__(self, lane, speed, frame):
        self.lane = lane
        note_images_list = [resource_path("note1.png"), resource_path("note2.png")]
        image_selected = random.choice(note_images_list)
        self.image = pygame.image.load(image_selected)
        self.rect = self.image.get_rect()
        self.rect.x = FRAME_X + FRAME_WIDTH/4*self.lane
        self.rect.y = -20
        self.speed = speed
        self.type = 0
        self.decesion = self.rect.y + 20
        self.frame = frame

    def draw(self, screen): # 노트 그리기
        screen.blit(self.image, self.rect)

    def update(self): # 노트 떨어트리기(스피드)
        self.rect.y += (self.speed*self.frame/60)
        self.decesion = self.rect.y + 20

    def out_of_screen(self): # 노트가 화면 밖에 나갈 때 삭제
        if self.rect.y >= FRAME_HEIGHT - 80:
            return True
        return False
    
class Note_long(): # 노트 클래스
    def __init__(self, lane, speed, long_num, frame):
        self.lane = lane
        self.length = long_num
        note_images_path = resource_path("note_long.png")
        self.image = pygame.image.load(note_images_path)
        self.image = pygame.transform.scale(self.image, (100, 10*self.length))
        self.rect = self.image.get_rect()
        self.rect.x = FRAME_X + FRAME_WIDTH/4*self.lane
        self.rect.y = -10*long_num
        self.decesion = self.rect.y + 10*self.length
        self.speed = speed
        self.type = 1
        self.decesion_code = 1
        self.frame = frame

    def boom(self):
        self.length -= 1
        if self.length < 0:
            self.length = 0
        self.image = pygame.transform.scale(self.image, (100, (10*(self.length+self.decesion_code))))
        
    def draw(self, screen): # 노트 그리기
        screen.blit(self.image, self.rect)

    def update(self): # 노트 떨어트리기(스피드)
        self.rect.y += (self.speed*self.frame/60)
        self.decesion = self.rect.y + 10*self.length

    def out_of_screen(self): # 노트가 화면 밖에 나갈 때 삭제
        if self.rect.y >= FRAME_HEIGHT - 80:
            return True
        return False

class Effect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 32):
            img_path = resource_path("effect/blue_{}.png".format(num))
            img = pygame.image.load(img_path)
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
        
    def update(self):
        speed = 1
        self.counter += 1
        if self.counter >= speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        if self.index >= len(self.images) - 1 and self.counter > speed:
            self.kill()
            
        
        
class Game():
    def __init__(self):
        font_path = resource_path("big_noodle_titling.ttf")
        press_se = resource_path("snare.wav")
        press_effect_path = resource_path("press_effect.png")
        scoreboard_image = resource_path("scoreboard.png")
        self.scoreboard = pygame.image.load(scoreboard_image)
        self.effect = pygame.image.load(press_effect_path)
        self.press = pygame.mixer.Sound(press_se)
        self.font = pygame.font.Font(font_path, 50)
        self.line = FRAME_HEIGHT* 7/9 + 10
        self.score = 0
        self.hp = 100
        self.combo = 0
        self.damage = 5
        self.decesion = False
        self.tmr = 0
        self.effect_group = pygame.sprite.Group()

        self.notes_0 = [] # 라인 별 노트 저장 리스트
        self.notes_1 = []
        self.notes_2 = []
        self.notes_3 = []

        self.pressed_d = False # 노트 이펙트 인식
        self.pressed_f = False
        self.pressed_j = False
        self.pressed_k = False
        
        music_path = resource_path("Children_Record.wav")
        pygame.mixer.music.load(music_path)
        self.music_play = False
        self.sec = 0
        self.min = 0
        self.tick = 0
        self.ticks = 0
    
    
        
    def note_decesion(self, note_ypos, line): # 노트 판정
        self.gap = abs(note_ypos - line) # 노트와 판정선의 차잇값의 절댓값
        if self.gap >= 120: # fail
            self.score += 0
            self.hp -= self.damage
            if self.combo > 0:
                self.combo = 0
            self.decesion = "FAIL"
            self.deci_color = RED
            self.tmr = 0
            self.tmr += 1

        elif self.gap < 120 and self.gap >= 80: # normal
            self.score += 1
            self.hp += 1
            self.combo += 1
            self.decesion = "NORMAL"
            self.deci_color = YELLOW
            self.tmr = 0
            self.tmr += 1
            
        elif self.gap < 80 and self.gap >= 40: # great
            self.score += 5
            self.hp += 2
            self.combo += 1
            self.decesion = "GREAT"
            self.deci_color = LEAF_GREEN
            self.tmr = 0
            self.tmr += 1

        elif self.gap < 40 and self.gap >= 0 : # perfect
            self.score += 10    
            self.hp += 3
            self.combo += 1
            self.decesion = "PERFECT"
            self.deci_color = SKY_BLUE
            self.tmr = 0
            self.tmr += 1

        
    def run_logic(self):
        
        if self.music_play == True:
            self.ticks += 1
            self.tick += 1
            if self.tick == 60:
                self.sec += 1
                self.tick = 0
            if self.sec == 60:
                self.sec = 0
                self.min += 1
        # 롱노트 D
        for note in self.notes_0:
            if self.pressed_d == True and note.type == 1 and abs(self.notes_0[0].decesion - FRAME_HEIGHT*7/9 + 5) < 40:
                note.boom()
                if note.length == 0:
                    del self.notes_0[0]
                effect = Effect(FRAME_X + FRAME_WIDTH*note.lane/4 + 50, FRAME_HEIGHT* 7/9 + 5)
                self.effect_group.add(effect)
                self.press.play(0)
                self.score += 10    
                self.hp += 3
                self.combo += 1
                self.decesion = "PERFECT"
                self.deci_color = SKY_BLUE
                self.tmr = 0
                self.tmr += 1

        # 노트가 밖에 나갈 때 삭제
            if note.out_of_screen():
                del self.notes_0[0]
                self.decesion = "FAIL"
                self.deci_color = RED
                self.tmr = 0
                self.tmr += 1
                self.hp -= 5
                if self.combo > 0:
                    self.combo = 0
        #롱노트 F
        for note in self.notes_1:
            if self.pressed_f == True and note.type == 1 and abs(self.notes_1[0].decesion - FRAME_HEIGHT*7/9 + 5) < 40:
                note.boom()
                if note.length == 0:
                    del self.notes_1[0]
                effect = Effect(FRAME_X + FRAME_WIDTH*note.lane/4 + 50, FRAME_HEIGHT* 7/9 + 5)
                self.effect_group.add(effect)
                self.press.play(0)
                self.score += 10    
                self.hp += 3
                self.combo += 1
                self.decesion = "PERFECT"
                self.deci_color = SKY_BLUE
                self.tmr = 0
                self.tmr += 1
        # 노트가 밖에 나갈 때 삭제
            if note.out_of_screen():
                del self.notes_1[0]
                self.decesion = "FAIL"
                self.deci_color = RED
                self.tmr = 0
                self.tmr += 1
                self.hp -= 5
                if self.combo > 0:
                    self.combo = 0
        #롱노트 J
        for note in self.notes_2:
            if self.pressed_j == True and note.type == 1 and abs(self.notes_2[0].decesion - FRAME_HEIGHT*7/9 + 5) < 40:
                note.boom()
                if note.length == 0:
                    del self.notes_2[0]
                effect = Effect(FRAME_X + FRAME_WIDTH*note.lane/4 + 50, FRAME_HEIGHT* 7/9 + 5)
                self.effect_group.add(effect)
                self.press.play(0)
                self.score += 10    
                self.hp += 3
                self.combo += 1
                self.decesion = "PERFECT"
                self.deci_color = SKY_BLUE
                self.tmr = 0
                self.tmr += 1
        # 노트가 밖에 나갈 때 삭제
            if note.out_of_screen():
                del self.notes_2[0]
                self.decesion = "FAIL"
                self.deci_color = RED
                self.tmr = 0
                self.tmr += 1
                self.hp -= 5
                if self.combo > 0:
                    self.combo = 0               
        #롱노트 K
        for note in self.notes_3:
            if self.pressed_k == True and note.type == 1 and abs(self.notes_3[0].decesion - FRAME_HEIGHT*7/9 + 5) < 40:
                note.boom()
                if note.length == 0:
                    del self.notes_3[0]
                effect = Effect(FRAME_X + FRAME_WIDTH*note.lane/4 + 50, FRAME_HEIGHT* 7/9 + 5)
                self.effect_group.add(effect)
                self.press.play(0)
                self.score += 10    
                self.hp += 3
                self.combo += 1
                self.decesion = "PERFECT"
                self.deci_color = SKY_BLUE
                self.tmr = 0
                self.tmr += 1
        # 노트가 밖에 나갈 때 삭제
            if note.out_of_screen():
                del self.notes_3[0]
                self.decesion = "FAIL"
                self.deci_color = RED
                self.tmr = 0
                self.tmr += 1
                self.hp -= 5
                if self.combo > 0:
                    self.combo = 0

                    
    # 짧은 노트 밖에 나갈 때 로직
        for note in self.notes_1:
            if note.out_of_screen():
                del self.notes_1[0]
                self.hp -= 5
                if self.combo > 0:
                    self.combo = 0
                self.decesion = "FAIL"
                self.deci_color = RED
                self.tmr = 0
                self.tmr += 1
        for note in self.notes_2:
            if note.out_of_screen():
                del self.notes_2[0]
                self.hp -= 5
                if self.combo > 0:
                    self.combo = 0
                self.decesion = "FAIL"
                self.deci_color = RED
                self.tmr = 0
                self.tmr += 1
        for note in self.notes_3:
            if note.out_of_screen():
                del self.notes_3[0]
                self.hp -= 5
                if self.combo > 0:
                    self.combo = 0
                self.decesion = "FAIL"
                self.deci_color = RED
                self.tmr = 0
                self.tmr += 1
        if self.hp > 100:
            self.hp = 100
        # 이펙트 업데이트
        self.effect_group.update()

    def draw_text(self, screen, text, font, x, y, main_color): # 텍스트 입력용 함수
        text_obj = font.render(text, True, main_color)
        text_rect = text_obj.get_rect()
        text_rect.center = x,y
        screen.blit(text_obj, text_rect)
    
    def draw_text_foggy(self, screen, text, font, x, y, main_color, parameter): # 텍스트 입력용 함수
        text_obj = font.render(text, True, main_color)
        text_rect = text_obj.get_rect()
        text_obj.set_alpha(parameter)
        text_rect.center = x,y
        screen.blit(text_obj, text_rect)
            
    def display_object(self, screen): # 오브젝트(노트 등) 그리기 함수
        # 라인별 클릭 효과 그리기
        if self.pressed_d: # d키 클릭 효과
            self.effect_rect = self.effect.get_rect()
            self.effect_rect.x = FRAME_X
            self.effect_rect.y = FRAME_HEIGHT* 7/9 - self.effect_rect.height
            screen.blit(self.effect, self.effect_rect)

        if self.pressed_f: # f키 클릭 효과
            self.effect_rect = self.effect.get_rect()
            self.effect_rect.x = FRAME_X + FRAME_WIDTH/4
            self.effect_rect.y = FRAME_HEIGHT* 7/9 - self.effect_rect.height
            screen.blit(self.effect, self.effect_rect)
            
        if self.pressed_j: # j키 클릭 효과
            self.effect_rect = self.effect.get_rect()
            self.effect_rect.x = FRAME_X + FRAME_WIDTH/4*2
            self.effect_rect.y = FRAME_HEIGHT* 7/9 - self.effect_rect.height
            screen.blit(self.effect, self.effect_rect)
            
        if self.pressed_k: # k키 클릭 효과
            self.effect_rect = self.effect.get_rect()
            self.effect_rect.x = FRAME_X + FRAME_WIDTH/4*3
            self.effect_rect.y = FRAME_HEIGHT* 7/9 - self.effect_rect.height
            screen.blit(self.effect, self.effect_rect)
            
        # 라인별 노트 업데이트, 그리기
        for note in self.notes_0:
            note.update()
            note.draw(screen)
        for note in self.notes_1:
            note.update()
            note.draw(screen)
        for note in self.notes_2:
            note.update()
            note.draw(screen)
        for note in self.notes_3:
            note.update()
            note.draw(screen)
        # HP 바 그리기
        self.hp_length = FRAME_HEIGHT/2
        self.hp_half = self.hp - 50
        self.hp_color = (0, 0, 0)
        self.blue = 0
        self.red = 0
        if self.hp <= 100 and self.hp >= 50: # 체력 상태에 따른 색 코드 변경하기
            self.blue = 255
            self.red = int(255 - 255*self.hp_half/50)
        elif self.hp < 50 and self.hp >= 0:
            self.blue = int(255 - 255*(1 - self.hp/50))
            self.red = 255
        self.hp_color = (self.red, self.blue, 0)        
        if self.hp > 0: # 체력 바에 역동감을 주기 위한 효과 넣기
            a = random.choice([-1, 1])
            if self.hp == 100:
                self.hp_visual = 100
            elif self. hp <= 100:
                self.hp_visual = self.hp + a
            elif self.hp_visual <= 0:
                self.hp_visual = 0
        #hp바 그리기
        pygame.draw.rect(screen, self.hp_color, # 색깔
        [FRAME_X + FRAME_WIDTH + LINE_WIDTH, (FRAME_HEIGHT / 2 + LINE_WIDTH)+(FRAME_HEIGHT / 2)*(1 - self.hp_visual/100), # 시작 위치
        LINE_WIDTH * 2, (FRAME_HEIGHT / 2)*(self.hp_visual/100)]) # 폭과 높이
        #콤보 시에 표시
        if self.combo > 0:
            self.draw_text(screen, "COMBO", self.font, FRAME_X + FRAME_WIDTH/2, FRAME_HEIGHT*1/6, DARK_ORANGE)
            self.draw_text(screen, "x" + str(self.combo), self.font, FRAME_X + FRAME_WIDTH/2, FRAME_HEIGHT*1/6 + 50, DARK_ORANGE)
        #스코어보드 밑바탕
        screen.blit(self.scoreboard, [FRAME_X, FRAME_HEIGHT * 7/9 + 40 +FRAME_WIDTH/4 - KEY_SPACE*2])
        # 스코어
        self.score_visual = "{0:O>11}".format(self.score)
        self.score_visual_two = " ".join(self.score_visual)
        self.draw_text(screen, self.score_visual_two, self.font, FRAME_X + FRAME_WIDTH/2, SCREEN_HEIGHT - 40, DARK_ORANGE)
        # 노트 판정에 따른 인디케이터
        if self.decesion:
            if self.tmr >= 1 and self.tmr <= 20:
                self.tmr += 1
                self.draw_text_foggy(screen, self.decesion, self.font, FRAME_X + FRAME_WIDTH/2, SCREEN_HEIGHT*3/5 - self.tmr, self.deci_color, 250 - self.tmr)
            elif self.tmr < 100:
                self.tmr = 0
                self.decesion = False
        # 노트 타격 효과 그리기
        self.effect_group.draw(screen)
        self.draw_text(screen, "{}min : {}sec : {}tick : {}ticks".format(self.min, self.sec, self.tick, self.ticks), self.font, 450, 100, WHITE)


    def display_frame(self, screen, keycolor, fontcolor): #게임 프레임 그리기 - 플레이하는 부분
        screen.fill(BLACK)
        x = FRAME_X + KEY_SPACE
        y = FRAME_HEIGHT * 7/9 + 25
        keyframe_size = FRAME_WIDTH/4 - KEY_SPACE*2
        for i in range(3): #노트 구분 선
            pygame.draw.line(screen, GRAY, [FRAME_X + (i + 1)*(FRAME_WIDTH/4), 0], [FRAME_X + (i + 1)*(FRAME_WIDTH/4), FRAME_HEIGHT + LINE_WIDTH*2], width=1)
        #판정선
        pygame.draw.line(screen, OCEAN_BLUE, [FRAME_X, FRAME_HEIGHT* 7/9 + 5],[FRAME_X+FRAME_WIDTH, FRAME_HEIGHT*7/9 + 5], width=10)

        #게임 프레임
        pygame.draw.rect(screen, WHITE, [FRAME_X - LINE_WIDTH, -1 * LINE_WIDTH, FRAME_WIDTH + LINE_WIDTH*2, FRAME_HEIGHT + LINE_WIDTH*2], width=LINE_WIDTH)
        #HP바 프레임
        pygame.draw.rect(screen, WHITE, [(FRAME_X + FRAME_WIDTH), (FRAME_HEIGHT / 2), LINE_WIDTH*4, (FRAME_HEIGHT / 2) + LINE_WIDTH], width = LINE_WIDTH)
        for i, key in enumerate(["D", "F", "J", "K"]): #게임 판정선 아래 키 설명
            pygame.draw.rect(screen, keycolor, [x+FRAME_WIDTH*i/4, y, keyframe_size, keyframe_size])
            keyset = self.font.render(key, True, fontcolor)
            screen.blit(keyset, (x+FRAME_WIDTH*i/4+keyframe_size/2-KEY_SPACE, y+KEY_SPACE))
    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    print(self.ticks)
                if event.key == pygame.K_p:
                    self.music_play = True
                    pygame.mixer.music.play(-1)
                if event.key == pygame.K_d: # d 키를 누름
                    self.press.play(0)
                    self.pressed_d = True
                    for note in self.notes_0:
                        if note.type == 0:
                            if abs(self.line - note.decesion) <= 200 and note.lane == 0: # 노트가 판정 범위 안에 들어왔는지 확인 후 삭제
                                self.note_decesion(note.decesion, self.line)
                                del self.notes_0[0]
                            if abs(self.line - note.decesion) < 120 and note.lane == 0: # 이펙트 개체 생성 - FAIL만 아닐 시
                                effect = Effect(FRAME_X + FRAME_WIDTH/4*note.lane + 50, FRAME_HEIGHT* 7/9 + 5)
                                self.effect_group.add(effect)
                    

                if event.key == pygame.K_f: # f 키를 누름
                    self.press.play(0)
                    self.pressed_f = True
                    for note in self.notes_1:
                        if note.type == 0:
                            if abs(self.line - note.decesion) <= 200 and note.lane == 1: # 노트가 판정 범위 안에 들어왔는지 확인 후 삭제
                                self.note_decesion(note.decesion, self.line)
                                del self.notes_1[0]
                            if abs(self.line - note.decesion) < 120 and note.lane == 1: # 이펙트 개체 생성 - FAIL만 아닐 시
                                effect = Effect(FRAME_X + FRAME_WIDTH/4*note.lane + 50, FRAME_HEIGHT* 7/9 + 5)
                                self.effect_group.add(effect)


                if event.key == pygame.K_j: # j 키를 누름
                    self.press.play(0)
                    self.pressed_j = True
                    for note in self.notes_2:
                        if note.type == 0:
                            if abs(self.line - note.decesion) <= 200 and note.lane == 2: # 노트가 판정 범위 안에 들어왔는지 확인 후 삭제
                                self.note_decesion(note.rect.y, self.line)
                                del self.notes_2[0]
                            if abs(self.line - note.decesion) < 120 and note.lane == 2: # 이펙트 개체 생성 - FAIL만 아닐 시
                                effect = Effect(FRAME_X + FRAME_WIDTH/4*note.lane + 50, FRAME_HEIGHT* 7/9 + 5)
                                self.effect_group.add(effect)

                if event.key == pygame.K_k: # k 키를 누름
                    self.press.play(0)
                    self.pressed_k = True
                    for note in self.notes_3:
                        if note.type == 0:
                            if abs(self.line - note.decesion) <= 200 and note.lane == 3: # 노트가 판정 범위 안에 들어왔는지 확인 후 삭제
                                self.note_decesion(note.rect.y, self.line)
                                del self.notes_3[0]
                            if abs(self.line - note.decesion) < 120 and note.lane == 3: # 이펙트 개체 생성 - FAIL만 아닐 시
                                effect = Effect(FRAME_X + FRAME_WIDTH/4*note.lane + 50, FRAME_HEIGHT* 7/9 + 5)
                                self.effect_group.add(effect)
    
                                         
            if event.type == pygame.KEYUP: # 키를 뗌
                if event.key == pygame.K_d:
                    self.pressed_d = False
                if event.key == pygame.K_f:
                    self.pressed_f = False
                if event.key == pygame.K_j:
                    self.pressed_j = False
                if event.key == pygame.K_k:
                    self.pressed_k = False
    def put_note_0(self, speed, time, code, long, frame):               # 노트 배치 함수
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 0:
            self.notes_0.append(Note(0, speed, frame))
        if self.ticks == time and code == 1:
            self.notes_0.append(Note_long(0, speed, long, frame))
    def put_note_1(self, speed, time, code, long, frame):
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 0:
            self.notes_1.append(Note(1, speed, frame))
        if self.ticks == time and code == 1:
            self.notes_1.append(Note_long(1, speed, long, frame))
    def put_note_2(self, speed, time, code, long, frame):
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 0:
            self.notes_2.append(Note(2, speed, frame))
        if self.ticks == time and code == 1:
            self.notes_2.append(Note_long(2, speed, long, frame))
    def put_note_3(self, speed, time, code, long, frame):
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 0:
            self.notes_3.append(Note(3, speed, frame))
        if self.ticks == time and code == 1:
            self.notes_3.append(Note_long(3, speed, long, frame))
            
    def frame(self, frame):
        self.frame_rate = frame
            
    def pos_a(self): # 채보 함수
        self.put_note_0(15, 173, 0, 0, self.frame_rate)
        self.put_note_1(15, 311, 0, 0, self.frame_rate)
        self.put_note_2(15, 450, 0, 0, self.frame_rate)
        self.put_note_3(15, 585, 0, 0, self.frame_rate)
        self.put_note_2(15, 657, 0, 0, self.frame_rate)
        self.put_note_1(15, 725, 0, 0, self.frame_rate)
        self.put_note_0(15, 793, 0, 0, self.frame_rate)
        self.put_note_1(15, 864, 0, 0, self.frame_rate)
        self.put_note_2(15, 932, 0, 0, self.frame_rate)
        self.put_note_1(15, 1002, 0, 0, self.frame_rate)
        self.put_note_2(15, 1073, 0, 0, self.frame_rate)
        self.put_note_3(15, 1080, 0, 0, self.frame_rate)
        self.put_note_3(15, 1151, 0, 0, self.frame_rate)
        self.put_note_1(15, 1186, 0, 0, self.frame_rate)
        self.put_note_3(15, 1223, 0, 0, self.frame_rate)
        self.put_note_1(15, 1239, 0, 0, self.frame_rate)
        self.put_note_3(15, 1255, 0, 0, self.frame_rate)
        self.put_note_3(15, 1272, 0, 0, self.frame_rate)
        self.put_note_3(15, 1293, 0, 0, self.frame_rate)
        self.put_note_3(15, 1328, 0, 0, self.frame_rate)
        self.put_note_3(15, 1361, 0, 0, self.frame_rate)
        self.put_note_3(15, 1378, 0, 0, self.frame_rate)
        self.put_note_3(15, 1396, 0, 0, self.frame_rate)
        self.put_note_3(15, 1414, 0, 0, self.frame_rate)
        self.put_note_3(15, 1432, 0, 0, self.frame_rate)
        self.put_note_3(15, 1468, 0, 0, self.frame_rate)
        self.put_note_3(15, 1503, 0, 0, self.frame_rate)
        self.put_note_3(15, 1519, 0, 0, self.frame_rate)
        self.put_note_3(15, 1536, 0, 0, self.frame_rate)
        self.put_note_3(15, 1555, 0, 0, self.frame_rate)
        self.put_note_3(15, 1562, 0, 0, self.frame_rate)
        
        
        
        
            

def resource_path(relative_path): # 리소스 경로 함수
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    pygame.init()
    pygame.display.set_caption("DELTABEAT")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    done = False

    while not done:
        fr = clock.get_fps()
        game.frame(fr)
        done = game.process_events()
        game.pos_a()
        game.run_logic()
        game.display_frame(screen, LEAF_GREEN, WHITE)
        game.display_object(screen)
        pygame.display.flip()
        clock.tick(60)


    pygame.quit()

if __name__ == '__main__':
    main()