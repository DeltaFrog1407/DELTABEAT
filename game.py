import pygame
import sys
import random
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
RED = (255, 0, 18)
YELLOW = (204, 255, 0)
GOLD = (255, 215, 0)
GREEN = (0, 255, 18)
BLUE = (0, 108, 255)
YELLOW_RANK = ()
VIOLET = (205, 0, 255)

FRAME_X = 700
FRAME_WIDTH = 400
FRAME_HEIGHT = 900
LINE_WIDTH = 5
KEY_SPACE = 10



class Note(): # 노트 클래스
    def __init__(self, lane, speed, frame):
        self.lane = lane
        note_images_list = ["assets/pics/note1.png", "assets/pics/note2.png"]
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
        note_images_path = "assets/pics/note_long.png"
        self.image = pygame.image.load(note_images_path)
        self.image = pygame.transform.scale(self.image, (100, 20*self.length))
        self.rect = self.image.get_rect()
        self.rect.x = FRAME_X + FRAME_WIDTH/4*self.lane
        self.rect.y = -20*long_num
        self.decesion = self.rect.y + 20*self.length
        self.speed = speed
        self.type = 1
        self.decesion_code = 1
        self.frame = frame

    def boom(self):
        self.length -= 1
        if self.length < 0:
            self.length = 0
        self.image = pygame.transform.scale(self.image, (100, (20*(self.length+self.decesion_code))))
        
    def draw(self, screen): # 노트 그리기
        screen.blit(self.image, self.rect)

    def update(self): # 노트 떨어트리기(스피드)
        self.rect.y += (self.speed*self.frame/60)
        self.decesion = self.rect.y + 20*self.length

    def out_of_screen(self): # 노트가 화면 밖에 나갈 때 삭제
        if self.rect.y >= FRAME_HEIGHT - 80:
            return True
        return False

class Effect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 32):
            img_path = "assets/effect/blue_{}.png".format(num)
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
        # 리소스들 불러오기
        no_image_path = "assets/jackets/no_image.png"
        font_path = "assets/fonts/big_noodle_titling.ttf"
        press_se = "assets/sound_effects/snare.wav"
        moving_se = "assets/sound_effects/moving.wav"
        selected_se = "assets/sound_effects/selected.wav"
        ui_sound = "assets/sound_effects/ui_put.wav"
        press_effect_path = "assets/effect/press_effect.png"
        scoreboard_image = "assets/pics/scoreboard.png"
        logo_path = "assets/pics/logo.png"
        button_path = "assets/pics/button.png"
        button_selected_path = "assets/pics/button_selected.png"
        main_background = "assets/backgrounds/main_background.png"
        main_background_dark = "assets/backgrounds/main_background_dark.png"
        main_background_1 = "assets/backgrounds/main.png"
        main_background_1_dark = "assets/backgrounds/main_dark.png"
        rank_frame = "assets/pics/rank_frame.png"
        rank_image_path = ["assets/pics/rank_s.png", "assets/pics/rank_a.png", "assets/pics/rank_b.png", 
                           "assets/pics/rank_c.png", "assets/pics/rank_d.png", "assets/pics/rank_f.png"]
        self.main_music = "assets/musics/main.mp3"
        self.rank_image = []
        for i in rank_image_path:
            self.rank_image.append(pygame.image.load(i))
        self.rank_decesion = 0
        pygame.mixer.music.load(self.main_music)
        pygame.mixer.music.play(-1)
        self.main_background = pygame.image.load(main_background)
        self.main_background_1 = pygame.image.load(main_background_1)
        self.main_background_dark = pygame.image.load(main_background_dark)
        self.main_background_1_dark = pygame.image.load(main_background_1_dark)
        self.rank_frame = pygame.image.load(rank_frame)
        self.button_image = pygame.image.load(button_path)
        self.button_selected_image = pygame.image.load(button_selected_path)
        self.logo_image = pygame.image.load(logo_path)
        self.no_image = pygame.image.load(no_image_path)
        self.scoreboard = pygame.image.load(scoreboard_image)
        self.effect = pygame.image.load(press_effect_path)
        self.press = pygame.mixer.Sound(press_se)
        self.moving = pygame.mixer.Sound(moving_se)
        self.selected = pygame.mixer.Sound(selected_se)
        self.ui_se = pygame.mixer.Sound(ui_sound)
        self.font_30 = pygame.font.Font(font_path, 30)
        self.font = pygame.font.Font(font_path, 50)
        self.font_80 = pygame.font.Font(font_path, 80)
        self.font_100 = pygame.font.Font(font_path, 100)
        self.font_150 = pygame.font.Font(font_path, 150)
    
        # 필요 변수들 불러오기
        self.version = "0.1"
        self.line = FRAME_HEIGHT* 7/9 + 10
        self.score = 0
        self.hp = 100
        self.combo = 0
        self.damage = 5
        self.decesion = False
        self.tmr = 0
        self.tmr_result = 0
        self.effect_group = pygame.sprite.Group()
        self.perfect_count = 0
        self.great_count = 0
        self.normal_count = 0
        self.fail_count = 0
        self.score_load = 0
        self.rank_load = 0
        self.music_index = 1
        self.music_select = False
        self.goto_menu = False
        self.escape = False
        self.rank_text = ["S", "A", "B", "C", "D", "F"]
        self.rank_color = [GOLD, GREEN, BLUE, YELLOW, VIOLET, RED]

        self.notes_0 = [] # 라인 별 노트 저장 리스트
        self.notes_1 = []
        self.notes_2 = []
        self.notes_3 = []

        self.pressed_d = False # 노트 이펙트 인식
        self.pressed_f = False
        self.pressed_j = False
        self.pressed_k = False
        
        self.index = 0 # 인덱스 숫자가 바뀜에 따라 게임 화면/상태가 바뀜 0: 메인 메뉴 2: 결과 표시창 3: 곡 선택 메뉴 4: 게임 플레이 메뉴

        # 음악 플레이 관련 변수들
        self.music_play = False
        self.sec = 0
        self.min = 0
        self.tick = 0
        self.ticks = 0
        
        # 메인 버튼 리스트
        self.main_select = 0
        self.main_button = ["START", "HELP", "EXIT"]
        
        #곡들 추가
        self.music_path = []
        self.jacket_path = []
        self.jacket_list = []
        self.music_title = []
        self.music_info = []
        self.music_difficulty = []
        self.chebo_list = []
        self.best_score_list = []
        self.best_score = []
        self.best_rank_list = []
        self.best_rank = []
        self.best_scoring = False
              ############         메모장을 불러들여서 곡 정보와 난이도 등을 불러옴
        txt_path = "assets/logs/music_infos.txt"
        with open(txt_path, 'r') as file:
            for line in file:
                record = line.split()
                self.music_title.append(record[0])
                self.music_info.append(record[1])
                self.music_difficulty.append(record[2])
                self.music_path.append("assets/musics/" + record[3])
                self.jacket_path.append("assets/jackets/" + record[4])
                self.chebo_list.append("assets/logs/" + record[5])
        for i in self.jacket_path:
            try:
                self.jacket_list.append(pygame.image.load(i))
            except:
                self.jacket_list.append(pygame.image.load(no_image_path))
        txt_path = "assets/logs/best_scores.txt"
        with open(txt_path, 'r') as file:
            for line in file:
                record = line.split()
                self.best_score_list.append(record[0])
                self.best_rank_list.append(record[1])
        for i in self.best_score_list:
            try:
                k = int(i)
                self.best_score.append(k)
            except:
                self.best_score.append(i)
        for i in self.best_rank_list:
            try:
                k = int(i)
                self.best_rank.append(k)
            except:
                self.best_rank.append(i)
        
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
            self.fail_count += 1

        elif self.gap < 120 and self.gap >= 80: # normal
            self.score += 100
            if self.combo >= 100 and self.combo < 200:
                self.score += 150
            elif self.combo >= 200 and self.combo < 300:
                self.score += 200
            elif self.combo >= 300 and self.combo < 400:
                self.score += 250
            elif self.combo >= 400 and self.combo < 500:
                self.score += 300
            self.hp += 1
            self.combo += 1
            self.decesion = "NORMAL"
            self.deci_color = YELLOW
            self.tmr = 0
            self.tmr += 1
            self.normal_count += 1
            
        elif self.gap < 80 and self.gap >= 40: # great
            self.score += 200
            if self.combo >= 100 and self.combo < 200:
                self.score += 150
            elif self.combo >= 200 and self.combo < 300:
                self.score += 200
            elif self.combo >= 300 and self.combo < 400:
                self.score += 250
            elif self.combo >= 400 and self.combo < 500:
                self.score += 300
            self.hp += 2
            self.combo += 1
            self.decesion = "GREAT"
            self.deci_color = LEAF_GREEN
            self.tmr = 0
            self.tmr += 1
            self.great_count += 1

        elif self.gap < 40 and self.gap >= 0 : # perfect
            self.score += 300
            if self.combo >= 100 and self.combo < 200:
                self.score += 150
            elif self.combo >= 200 and self.combo < 300:
                self.score += 200
            elif self.combo >= 300 and self.combo < 400:
                self.score += 250
            elif self.combo >= 400 and self.combo < 500:
                self.score += 300
            self.hp += 3
            self.combo += 1
            self.decesion = "PERFECT"
            self.deci_color = SKY_BLUE
            self.tmr = 0
            self.tmr += 1
            self.perfect_count += 1

        
    def run_logic(self): 
        if self.hp <= 0:
            self.index = 2
        # 롱노트 D
        for note in self.notes_0:
            if self.pressed_d == True and note.type == 1 and abs(self.notes_0[0].decesion - FRAME_HEIGHT*7/9 + 5) < 40:
                note.boom()
                if note.length == 0:
                    del self.notes_0[0]
                effect = Effect(FRAME_X + FRAME_WIDTH*note.lane/4 + 50, FRAME_HEIGHT* 7/9 + 5)
                self.effect_group.add(effect)
                
                self.score += 300
                self.hp += 3
                self.combo += 1
                self.decesion = "PERFECT"
                self.deci_color = SKY_BLUE
                self.tmr = 0
                self.tmr += 1 
                self.perfect_count += 1

        # 노트가 밖에 나갈 때 삭제
            if note.out_of_screen():
                del self.notes_0[0]
                self.decesion = "FAIL"
                self.deci_color = RED
                self.tmr = 0
                self.tmr += 1
                self.hp -= 5
                self.fail_count += 1
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
                self.score += 300  
                self.hp += 3
                self.combo += 1
                self.decesion = "PERFECT"
                self.deci_color = SKY_BLUE
                self.tmr = 0
                self.tmr += 1
                self.perfect_count += 1
        # 노트가 밖에 나갈 때 삭제
            if note.out_of_screen():                
                del self.notes_1[0]
                self.decesion = "FAIL"
                self.deci_color = RED
                self.tmr = 0
                self.tmr += 1
                self.hp -= 5
                self.fail_count += 1
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
                self.score += 300    
                self.hp += 3
                self.combo += 1
                self.decesion = "PERFECT"
                self.deci_color = SKY_BLUE
                self.tmr = 0
                self.tmr += 1
                self.perfect_count += 1
        # 노트가 밖에 나갈 때 삭제
            if note.out_of_screen():
                del self.notes_2[0]
                self.decesion = "FAIL"
                self.deci_color = RED
                self.tmr = 0
                self.tmr += 1
                self.hp -= 5
                self.fail_count += 1
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
                self.score += 300    
                self.hp += 3
                self.combo += 1
                self.decesion = "PERFECT"
                self.deci_color = SKY_BLUE
                self.tmr = 0
                self.tmr += 1
                self.perfect_count += 1
        # 노트가 밖에 나갈 때 삭제
            if note.out_of_screen():
                del self.notes_3[0]
                self.decesion = "FAIL"
                self.deci_color = RED
                self.tmr = 0
                self.tmr += 1
                self.hp -= 5
                self.fail_count += 1
                if self.combo > 0:
                    self.combo = 0
            
        if self.main_select > 4: # 메인화면 버튼 선택 로직 : 선택 인덱스가 갯수 초과면 다시 돌아오게 하기
            self.main_select = 1
        elif self.main_select < 0:
            self.main_select = 3
            
        if self.hp > 100:
            self.hp = 100
        # 이펙트 업데이트
        self.effect_group.update()
        
        # 곡 선택 인덱스
        if self.index == 3:
            if self.music_index == 0:
                self.music_index = len(self.music_path) - 1
            elif self.music_index >= len(self.music_path):
                self.music_index = 1

        if self.music_play == True: # 곡 생성 후 시간 계산
            self.ticks += 1
            self.tick += 1
            if self.tick == 60:
                self.sec += 1
                self.tick = 0
            if self.sec == 60:
                self.sec = 0
                self.min += 1
                
        # 결과 인덱스
        if self.index == 2:
            note_all = self.perfect_count + self.great_count + self.normal_count + self.fail_count
            self.rank_load = 0
            try:
                note_rate = int(self.perfect_count/note_all*100)
            except:
                note_rate = 1
            if note_rate >= 95: # S랭크 결정
                self.rank_load = 0
            elif note_rate >= 80 and note_rate < 95: # A랭크 결정
                self.rank_load = 1
            elif note_rate >= 60 and note_rate < 80: # B랭크 결정
                self.rank_load = 2
            elif note_rate >= 40 and note_rate < 60: # C랭크 결정
                self.rank_load = 3
            elif note_rate >= 40 and note_rate < 60: # D랭크 결정
                self.rank_load = 4
            else:
                self.rank_load = 5
            
            if self.escape == True and self.rank_load <= 2: # 중도포기 시에 C랭크 이하고 받음
                self.rank_load = 3
            if self.rank_load <= self.best_rank[self.music_index]:
                self.best_rank[self.music_index] = self.rank_load
            if self.tmr_result == 200 or self.tmr_result == 220 or self.tmr_result == 240 or self.tmr_result == 260 or self.tmr_result == 300: ## 스코어 소리 출력
                self.ui_se.play(0)
            if self.tmr_result == 400 and self.score > self.best_score[self.music_index]:
                self.ui_se.play(0)
                self.best_scoring = True
                self.best_score[self.music_index] = self.score   # 최고기록 텍스트에 쑤셔넣기
                print(self.best_rank[self.music_index])
                file = open("assets/logs/best_scores.txt", 'w')
                for i, k in zip(self.best_score, self.best_rank):
                    if type(i) == str:
                        file.write(str(i) + " ")
                    else:
                        file.write(str(i) + " ")
                    if type(k) == str:
                        file.write(str(k) + "\n")
                    else:
                        file.write(str(k) + "\n")
                file.close()
            if self.tmr_result == 500:
                self.ui_se.play(0)
            if self.tmr_result >= 550 and self.goto_menu == True:
                self.reset()
                self.goto_menu = False

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
        if self.index == 4: # 게임 플레이 인덱스 시 표시
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
        decesions = ["PERFECT", "GREAT", "NORMAL", "FAIL"]
        decesions_color = [SKY_BLUE, LEAF_GREEN, YELLOW, RED]
        if self.index == 2: # 결과창 인덱스
            if self.tmr_result >= 0:
                pygame.mixer.music.stop()
                self.draw_text(screen, "RESULT", self.font_150, 200, 100, WHITE)
                self.draw_text(screen, "SCORE", self.font_100, 300, 700, WHITE)
                self.draw_text(screen, "HIGH SCORE  :  " + str(self.best_score[self.music_index]), self.font_100, 1100, 100, DARK_ORANGE)

                for i in range(len(decesions)):
                    self.draw_text(screen, decesions[i], self.font_80, 300, 240 + i*100, decesions_color[i])
                self.tmr_result += 1
            if self.tmr_result >= 200:
                self.draw_text(screen, str(self.perfect_count), self.font_80, 550, 240, WHITE)
            if self.tmr_result >= 220:
                self.draw_text(screen, str(self.great_count), self.font_80, 550, 240 + 100, WHITE)
            if self.tmr_result >= 240:
                self.draw_text(screen, str(self.normal_count), self.font_80, 550, 240 + 2*100, WHITE)
            if self.tmr_result >= 260:
                self.draw_text(screen, str(self.fail_count), self.font_80, 550, 240 + 3*100, WHITE)
            if self.tmr_result >= 300 and self.tmr_result<=400:
                self.score_load += 1
                self.draw_text(screen, str(int(self.score*self.score_load/100)), self.font_80, 550, 700, WHITE)
            if self.tmr_result > 400:
                self.draw_text(screen, str(self.score), self.font_80, 550, 700, WHITE)
            if self.tmr_result > 500:
                screen.blit(self.rank_image[self.rank_load], [800, 150])
                self.draw_text(screen, "Press ESC to go to lobby", self.font, 1100, 800, WHITE)
            if self.best_scoring == True:
                self.draw_text(screen, "BEST SCORE!", self.font_100, 450, 800, DARK_ORANGE)

        if self.index == 3: # 곡 선택 인덱스
            for i in range(-1, 2):
                try:
                    screen.blit(self.jacket_list[self.music_index + i], [555 + i*800, 185])
                except: # 이미지 없을 시
                    screen.blit(self.no_image, [555 + i*800, 185])
            self.draw_text(screen, "HIGH SCORE", self.font_30, 800, 115, DARK_ORANGE)
            try:  # 최고기록
                self.draw_text(screen, self.rank_text[self.best_rank[self.music_index]] + "  " + str(self.best_score[self.music_index]), self.font, 800, 150, self.rank_color[self.best_rank[self.music_index]])
            except:
                self.draw_text(screen, "None", self.font, 800, 150, DARK_ORANGE)
            try: # 타이틀
                self.draw_text(screen, self.music_title[self.music_index].replace('_', ' '), self.font, 800, 750, WHITE)
            except:
                self.draw_text(screen, "No title", self.font, 800, 750, WHITE)
            try: # 정보
                self.draw_text(screen, "ARTIST : " + self.music_info[self.music_index], self.font_30, 800, 800, WHITE)
            except: 
                self.draw_text(screen, "No info", self.font_30, 800, 800, WHITE)
            try: # 난이도
                self.draw_text(screen, "Difficulty : " + self.music_difficulty[self.music_index] + "/ 10", self.font_30, 800, 830, WHITE)
            except:
                self.draw_text(screen, "No difficulty", self.font_30, 800, 830, WHITE)
            
            
    def display_frame(self, screen, keycolor, fontcolor): #게임 프레임 그리기 - 플레이하는 부분
        if self.index == 4: # 게임 플레이 인덱스
            screen.blit(self.main_background_dark, [0, 0])
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
            
        elif self.index == 0: # 메인 메뉴 인덱스
            screen.blit(self.main_background, [0, 0])# 배경화면
            self.draw_text(screen, "Version. "+ self.version, self.font_30, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50, WHITE)
            self.draw_text(screen, "Made by DELTAFROG", self.font_30, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 25, WHITE)
            self.logo_width = self.logo_image.get_rect().width  # 로고 표시
            self.logo_height = self.logo_image.get_rect().height
            screen.blit(self.logo_image, [SCREEN_WIDTH/2 - self.logo_width/2, SCREEN_HEIGHT/4 - self.logo_height/2])
            self.button_width = self.button_image.get_rect().width  # 로고 표시
            self.button_height = self.button_image.get_rect().height
            for i in range(len(self.main_button)): # 버튼 갯수별로 생성
                if i == self.main_select - 1: # 버튼을 선택했을 때 선택되었다고 표시
                    screen.blit(self.button_selected_image, [SCREEN_WIDTH/2 - self.button_width/2, SCREEN_HEIGHT/2 + i*130])
                    self.draw_text(screen, self.main_button[i], self.font, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + i*130 + 50, BLACK)
                else:
                    screen.blit(self.button_image, [SCREEN_WIDTH/2 - self.button_width/2, SCREEN_HEIGHT/2 + i*130])
                    self.draw_text(screen, self.main_button[i], self.font, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + i*130 + 50, WHITE)
            
        elif self.index == 2: # 결과창 인덱스
            screen.blit(self.main_background_dark, [0, 0])# 배경화면
            screen.blit(self.rank_frame, [855, 205])
            
        elif self.index == 3: # 곡 선택 인덱스
            screen.blit(self.main_background, [0, 0])# 배경화면
            screen.blit(self.rank_frame, [545, 175])
            screen.blit(self.rank_frame, [1345, 175])
            screen.blit(self.rank_frame, [-255, 175])
            self.draw_text(screen, "PRESS SPACE TO START", self.font_30, 800, 50, WHITE)
    
    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    print(self.ticks)
                if self.index == 4: # 게임 플레이 시
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
                    if event.key == pygame.K_ESCAPE: # esc 키 누르면 결과창으로
                        self.escape = True
                        self.index = 2
                    
                if self.index == 0:  # 메인 메뉴에서
                    if event.key == pygame.K_UP: # 위 키를 누름
                        self.main_select -= 1 # 메뉴 인덱스 감소
                        self.moving.play(0)
                    if event.key == pygame.K_DOWN: # 아래 키를 누름
                        self.main_select += 1 # 메뉴 인덱스 증가
                        self.moving.play(0)
                    if event.key == pygame.K_RETURN:
                        if self.main_select >= 1 and self.main_select <= 3:
                            self.selected.play(0)
                        if self.main_select == 1:
                            self.index = 3
                        elif self.main_select == 3:
                            return True
                
                elif self.index == 3:  # 곡 선택 메뉴에서
                    if event.key == pygame.K_RIGHT:
                        self.music_index += 1
                    if event.key == pygame.K_LEFT:
                        self.music_index -= 1
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.load(self.music_path[self.music_index])
                        self.music_play = True
                        pygame.mixer.music.play(-1)
                        self.index = 4
                    if event.key == pygame.K_ESCAPE:
                        self.index = 0
                
                elif self.index == 2: # 결과창 메뉴에서
                    if event.key == pygame.K_ESCAPE:
                        self.goto_menu = True
                        
            if event.type == pygame.KEYUP: # 키를 뗌
                if event.key == pygame.K_d:
                    self.pressed_d = False
                if event.key == pygame.K_f:
                    self.pressed_f = False
                if event.key == pygame.K_j:
                    self.pressed_j = False
                if event.key == pygame.K_k:
                    self.pressed_k = False
                if event.key == pygame.K_ESCAPE:
                    self.goto_menu = False
                    
    def put_note_0(self, speed, time, code, long, frame):               # 노트 배치 함수
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 0:
            self.notes_0.append(Note(0, speed, frame))
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 1:
            self.notes_0.append(Note_long(0, speed, long, frame))
    def put_note_1(self, speed, time, code, long, frame):
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 0:
            self.notes_1.append(Note(1, speed, frame))
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 1:
            self.notes_1.append(Note_long(1, speed, long, frame))
    def put_note_2(self, speed, time, code, long, frame):
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 0:
            self.notes_2.append(Note(2, speed, frame))
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 1:
            self.notes_2.append(Note_long(2, speed, long, frame))
    def put_note_3(self, speed, time, code, long, frame):
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 0:
            self.notes_3.append(Note(3, speed, frame))
        if self.ticks == time - (FRAME_HEIGHT*7/9 + 5)/speed and code == 1:
            self.notes_3.append(Note_long(3, speed, long, frame))
            
    def frame(self, frame): # 프레임 선언 함수
        self.frame_rate = frame
            
    def pos_a(self): # 채보 함수 -> 메모장을 불러들인 후에 메모장에 적힌 내용을 채보로 만듦
        try:
            txt_path = self.chebo_list[self.music_index]
        except:
            txt_path = "assets/logs/chebo_path.txt"
        with open(txt_path, 'r') as file:
            lines_final = []
            lines = []
            line = file.readline()
            list_line = line.split()
            for i in list_line:
                a = int(i)
                lines.append(a)
            lines_final.append(lines)
            lines = []
            while line != '':
                line = file.readline()
                list_line = line.split()
                for i in list_line:
                    a = int(i)
                    lines.append(a)
                if not list_line:
                    break
                lines_final.append(lines)
                lines = []
            
        for i in range(len(lines_final)):
            if lines_final[i][0] == 0:
                self.put_note_0(15, lines_final[i][1], lines_final[i][2], lines_final[i][3], self.frame_rate)
            if lines_final[i][0] == 1:
                self.put_note_1(15, lines_final[i][1], lines_final[i][2], lines_final[i][3], self.frame_rate)
            if lines_final[i][0] == 2:
                self.put_note_2(15, lines_final[i][1], lines_final[i][2], lines_final[i][3], self.frame_rate)
            if lines_final[i][0] == 3:
                self.put_note_3(15, lines_final[i][1], lines_final[i][2], lines_final[i][3], self.frame_rate)
            if lines_final[i][0] == 4 and self.ticks == lines_final[i][1]:
                self.index = 2
    
    def reset(self):
        # 기초 변수들 초기화
        self.score_load = 0
        self.hp = 100
        self.combo = 0
        self.tmr_result = 0
        self.best_scoring = False
        self.music_play = False
        self.fail_count = 0
        self.normal_count = 0
        self.great_count = 0
        self.perfect_count = 0
        self.score = 0
        self.ticks = 0
        self.tick = 0
        self.sec = 0
        self.min = 0
        self.notes_0 = [] # 라인 별 노트 저장 리스트
        self.notes_1 = []
        self.notes_2 = []
        self.notes_3 = []
        self.escape = False
        pygame.mixer.music.load(self.main_music)
        pygame.mixer.music.play(-1)
        # 인덱스 변경
        self.index = 3
                        

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
        done = game.process_event()
        game.pos_a()
        game.run_logic()
        game.display_frame(screen, LEAF_GREEN, WHITE)
        game.display_object(screen)
        pygame.display.flip()
        clock.tick_busy_loop(60)
        
    pygame.quit()

if __name__ == '__main__':
    main()