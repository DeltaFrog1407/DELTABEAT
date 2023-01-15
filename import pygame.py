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

class Note(pygame.sprite.Sprite): # 노트 클래스
    def __init__(self, lane, speed):
        super().__init__()
        note_images_list = [resource_path("note1.png"), resource_path("note2.png")]
        image_selected = random.choice(note_images_list)
        self.image = pygame.image.load(image_selected)
        self.rect = self.image.get_rect()
        self.rect.x = FRAME_X + FRAME_WIDTH/4*lane
        self.rect.y = -20
        self.speed = speed
    
  #  def note_decision(self, line): # 노트 판정
  #      if self.rect 
        
    def update(self): # 노트 떨어트리기(스피드)
        self.rect.y += self.speed
        if self.rect.y == FRAME_HEIGHT:
            self.kill()

class Game():
    def __init__(self):
        font_path = resource_path("big_noodle_titling.ttf")
        press_se = resource_path("snare.wav")
        self.press = pygame.mixer.Sound(press_se)
        self.font = pygame.font.Font(font_path, 50)
        self.notes = pygame.sprite.Group()
        self.notes.add(Note(2, 15))
        
    def game_logic(self):
        self.notes.update()
            
        
    def display_object(self, screen):
        self.notes.draw(screen)
        
    def display_frame(self, screen, keycolor, fontcolor): #게임 프레임 그리기 - 플레이하는 부분
        screen.fill(BLACK)
        x = FRAME_X + KEY_SPACE
        y = FRAME_HEIGHT * 7/9 + 40
        keyframe_size = FRAME_WIDTH/4 - KEY_SPACE*2
        for i in range(3): #노트 구분 선
            pygame.draw.line(screen, GRAY, [FRAME_X + (i + 1)*(FRAME_WIDTH/4), 0], [FRAME_X + (i + 1)*(FRAME_WIDTH/4), FRAME_HEIGHT + LINE_WIDTH*2], width=1)
            
        pygame.draw.rect(screen, OCEAN_BLUE, [FRAME_X, FRAME_HEIGHT* 7/9, FRAME_WIDTH, 20])  #판정선 그리기
        for i in range(20):
            pygame.draw.line(screen, SKY_BLUE, [FRAME_X + i*20 + 20, FRAME_HEIGHT* 7/9], [FRAME_X + i*20 +10, FRAME_HEIGHT* 7/9 + 20], width = 10)
        
        #게임 프레임
        pygame.draw.rect(screen, WHITE, [FRAME_X - LINE_WIDTH, -1 * LINE_WIDTH, FRAME_WIDTH + LINE_WIDTH*2, FRAME_HEIGHT + LINE_WIDTH*2], width=LINE_WIDTH)
        pygame.draw.rect(screen, WHITE, [(FRAME_X + FRAME_WIDTH), (FRAME_HEIGHT / 2), 20, (FRAME_HEIGHT / 2) + LINE_WIDTH], width = LINE_WIDTH)
        for i, key in enumerate(["D", "F", "J", "K"]): #게임 판정선 아래 키 설명
            pygame.draw.rect(screen, keycolor, [x+FRAME_WIDTH*i/4, y, keyframe_size, keyframe_size])
            keyset = self.font.render(key, True, fontcolor)
            screen.blit(keyset, (x+FRAME_WIDTH*i/4+keyframe_size/2-KEY_SPACE, y+KEY_SPACE))
            
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        

def resource_path(relative_path):
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
        game.display_frame(screen, LEAF_GREEN, WHITE)
        game.game_logic()
        game.display_object(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()