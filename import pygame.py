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
SKY_BLUE = (000, 51, 204)
OCEAN_BLUE = (51, 102, 255)
LEAF_GREEN = (51, 204, 0)

FRAME_X = 700
FRAME_WIDTH = 400
FRAME_HEIGHT = 900
LINE_WIDTH = 5
KEY_SPACE = 10

class Note(): # 노트 클래스
    def __init__(self, lane, speed):
        super().__init__()
        self.lane = lane
        note_images_list = [resource_path("note1.png"), resource_path("note2.png")]
        image_selected = random.choice(note_images_list)
        self.image = pygame.image.load(image_selected)
        self.rect = self.image.get_rect()
        self.rect.x = FRAME_X + FRAME_WIDTH/4*self.lane
        self.rect.y = -20
        self.speed = speed

    def draw(self, screen): # 노트 그리기
        screen.blit(self.image, self.rect)

    def update(self): # 노트 떨어트리기(스피드)
        self.rect.y += self.speed

    def out_of_screen(self): # 노트가 화면 밖에 나갈 때 삭제
        if self.rect.y >= FRAME_HEIGHT:
            return True
        return False

class Game():
    def __init__(self):
        font_path = resource_path("big_noodle_titling.ttf")
        press_se = resource_path("snare.wav")
        press_effect_path = resource_path("press_effect.png")
        self.effect = pygame.image.load(press_effect_path)
        self.press = pygame.mixer.Sound(press_se)
        self.font = pygame.font.Font(font_path, 50)
        self.line = FRAME_HEIGHT* 7/9 + 10
        self.score = 0
        self.hp = 100

        self.notes_0 = [] # 라인 별 노트 저장 리스트
        self.notes_1 = []
        self.notes_2 = []
        self.notes_3 = []

        self.pressed_d = False # 노트 이펙트 인식
        self.pressed_f = False
        self.pressed_j = False
        self.pressed_k = False
        
        self.notes_0.append(Note(0, 10))
        self.notes_1.append(Note(1, 10))
        self.notes_2.append(Note(2, 10))

    def note_decesion(self, note_ypos, line): # 노트 판정
        self.gap = abs(note_ypos - line) # 노트와 판정선의 차잇값의 절댓값
        if self.gap >= 120: # fail
            self.score += 0
            self.hp -= 5
            print(self.score)
        elif self.gap < 120 and self.gap >= 80: # normal
            self.score += 1
            print(self.score)
        elif self.gap < 80 and self.gap >= 40: # great
            self.score += 5
            print(self.score)
        elif self.gap < 40 and self.gap >= 0 : # perfect
            self.score += 10    
            print(self.score)

    def run_logic(self):
        # 노트가 밖에 나갈 때 삭제
        for note in self.notes_0:
            if note.out_of_screen():
                del self.notes_0[0]
        for note in self.notes_1:
            if note.out_of_screen():
                del self.notes_1[0]
        for note in self.notes_2:
            if note.out_of_screen():
                del self.notes_2[0]
        for note in self.notes_3:
            if note.out_of_screen():
                del self.notes_3[0]

    def draw_text(self, screen, text, font, x, y, main_color): # 텍스트 입력용 함수
        text_obj = font.render(text, True, main_color)
        text_rect = text_obj.get_rect()
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
        self.hp_visual = self.hp
        if self.hp > 0:
            for i in range(-10, 10):
                self.hp_visual = self.hp - i
                pygame.draw.line(screen, LEAF_GREEN, 
                [FRAME_X + FRAME_WIDTH + LINE_WIDTH*2 - 1, (FRAME_HEIGHT / 2 + LINE_WIDTH)/self.hp_visual*100],
                [FRAME_X + FRAME_WIDTH + LINE_WIDTH*2 - 1, FRAME_HEIGHT], 
                width=10)

    def display_frame(self, screen, keycolor, fontcolor): #게임 프레임 그리기 - 플레이하는 부분
        screen.fill(BLACK)
        x = FRAME_X + KEY_SPACE
        y = FRAME_HEIGHT * 7/9 + 40
        keyframe_size = FRAME_WIDTH/4 - KEY_SPACE*2
        for i in range(3): #노트 구분 선
            pygame.draw.line(screen, GRAY, [FRAME_X + (i + 1)*(FRAME_WIDTH/4), 0], [FRAME_X + (i + 1)*(FRAME_WIDTH/4), FRAME_HEIGHT + LINE_WIDTH*2], width=1)
        #판정선
        pygame.draw.line(screen, OCEAN_BLUE, [FRAME_X, FRAME_HEIGHT* 7/9 + 5],[FRAME_X+FRAME_WIDTH, FRAME_HEIGHT*7/9 + 5], width=10)

        #게임 프레임
        pygame.draw.rect(screen, WHITE, [FRAME_X - LINE_WIDTH, -1 * LINE_WIDTH, FRAME_WIDTH + LINE_WIDTH*2, FRAME_HEIGHT + LINE_WIDTH*2], width=LINE_WIDTH)
        #HP바 프레임
        pygame.draw.rect(screen, WHITE, [(FRAME_X + FRAME_WIDTH), (FRAME_HEIGHT / 2), 20, (FRAME_HEIGHT / 2) + LINE_WIDTH], width = LINE_WIDTH)
        for i, key in enumerate(["D", "F", "J", "K"]): #게임 판정선 아래 키 설명
            pygame.draw.rect(screen, keycolor, [x+FRAME_WIDTH*i/4, y, keyframe_size, keyframe_size])
            keyset = self.font.render(key, True, fontcolor)
            screen.blit(keyset, (x+FRAME_WIDTH*i/4+keyframe_size/2-KEY_SPACE, y+KEY_SPACE))

        # 텍스트들
        self.draw_text(screen, "Score : " + str(self.score), self.font, 100, 50, WHITE)
            
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d: # d 키를 누름
                    self.pressed_d = True
                    for note in self.notes_0:
                        if abs(self.line - note.rect.y) <= 200 and note.lane == 0:
                            self.note_decesion(note.rect.y, self.line)
                            del self.notes_0[0]

                if event.key == pygame.K_f: # f 키를 누름
                    self.pressed_f = True
                    for note in self.notes_1:
                        if abs(self.line - note.rect.y) <= 200 and note.lane == 1:
                            self.note_decesion(note.rect.y, self.line)
                            del self.notes_1[0]

                if event.key == pygame.K_j: # j 키를 누름
                    self.pressed_j = True
                    for note in self.notes_2:
                        if abs(self.line - note.rect.y) <= 200 and note.lane == 2:
                            self.note_decesion(note.rect.y, self.line)
                            del self.notes_2[0]

                if event.key == pygame.K_k: # k 키를 누름
                    self.pressed_k = True
                    for note in self.notes_3:
                        if abs(self.line - note.rect.y) <= 200 and note.lane == 3:
                            self.note_decesion(note.rect.y, self.line)
                            del self.notes_3[0]

            if event.type == pygame.KEYUP: # 키를 뗌
                if event.key == pygame.K_d:
                    self.pressed_d = False
                if event.key == pygame.K_f:
                    self.pressed_f = False
                if event.key == pygame.K_j:
                    self.pressed_j = False
                if event.key == pygame.K_k:
                    self.pressed_k = False
                    

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
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen, LEAF_GREEN, WHITE)
        game.display_object(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()