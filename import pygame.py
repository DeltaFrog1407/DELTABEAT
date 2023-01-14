import pygame
import sys
import math
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

class Key: # 판정선 아래 네모들
    def __init__(self):
        font_path = resource_path("DELTABEAT/big_noodle_titling.ttf")
        self.font = pygame.font.Font(font_path, 50)
        x = FRAME_X + KEY_SPACE
        y = FRAME_HEIGHT * 7/9 + 40
        keyframe_size = FRAME_WIDTH/4 - KEY_SPACE*2
        self.d = pygame.Rect(x, y, keyframe_size, keyframe_size)
        self.f = pygame.Rect(x+(FRAME_WIDTH/4), y, keyframe_size, keyframe_size)
        self.j = pygame.Rect(x+(FRAME_WIDTH*2/4), y, keyframe_size, keyframe_size)
        self.k = pygame.Rect(x+(FRAME_WIDTH*3/4), y, keyframe_size, keyframe_size)
        
    
    def draw(self, screen, color, fontcolor):
        dkey = self.font.render("D", True, fontcolor)
        fkey = self.font.render("F", True, fontcolor)
        jkey = self.font.render("J", True, fontcolor)
        kkey = self.font.render("K", True, fontcolor)
        
        width = dkey.get_width()
        height = dkey.get_height()
        x = self.d.centerx
        y = self.d.centery
        xpos = x - int(width / 2)
        ypos = y - int(height / 2)
        pygame.draw.rect(screen, color, self.d)
        pygame.draw.rect(screen, color, self.f)
        pygame.draw.rect(screen, color, self.j)
        pygame.draw.rect(screen, color, self.k)
        screen.blit(dkey, (xpos, ypos))
        screen.blit(fkey, (xpos + (FRAME_WIDTH/4), ypos))
        screen.blit(jkey, (xpos + (FRAME_WIDTH*2/4), ypos))
        screen.blit(kkey, (xpos + (FRAME_WIDTH*3/4), ypos))
        

class Game:
    def __init__(self):
        font_path = resource_path("DELTABEAT/big_noodle_titling.ttf")
        press_se = resource_path("DELTABEAT/snare.wav")
        self.press = pygame.mixer.Sound(press_se)
        self.font = pygame.font.Font(font_path, 50)
        self.key = Key()

    def draw_map(self, screen): #게임 프레임 그리기 - 플레이하는 부분
        for i in range(3):
            pygame.draw.line(screen, GRAY, [FRAME_X + (i + 1)*(FRAME_WIDTH/4), 0], [FRAME_X + (i + 1)*(FRAME_WIDTH/4), FRAME_HEIGHT + LINE_WIDTH*2], width=1)
        pygame.draw.rect(screen, OCEAN_BLUE, [FRAME_X, FRAME_HEIGHT* 7/9, FRAME_WIDTH, 20])
        for i in range(20):
            pygame.draw.line(screen, SKY_BLUE, [FRAME_X + i*20 + 20, FRAME_HEIGHT* 7/9], [FRAME_X + i*20 +10, FRAME_HEIGHT* 7/9 + 20], width = 10)
        self.key.draw(screen , LEAF_GREEN , WHITE)
        pygame.draw.rect(screen, WHITE, [FRAME_X - LINE_WIDTH, -1 * LINE_WIDTH, FRAME_WIDTH + LINE_WIDTH*2, FRAME_HEIGHT + LINE_WIDTH*2], width=LINE_WIDTH)
        pygame.draw.rect(screen, WHITE, [(FRAME_X + FRAME_WIDTH), (FRAME_HEIGHT / 2), 20, (FRAME_HEIGHT / 2) + LINE_WIDTH], width = LINE_WIDTH)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.press.play()
                if event.key == pygame.K_f:
                    self.press.play()
                if event.key == pygame.K_j:
                    self.press.play()
                if event.key == pygame.K_k:
                    self.press.play()






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
    font = pygame.font.Font(None, 40)

    try:
        pygame.mixer.music.load("DELTABEAT\Children_Record.wav")
    except:
        print("ogg 파일이 맞지 않거나, 오디오 기기와 접속되어 있지 않습니다.")
    
    game = Game()
    done = False

    while not done:
        done = game.process_events()
        key = pygame.key.get_pressed()
        if key[pygame.K_p] == 1:
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.play(-1)
        if key[pygame.K_s] == 1:
            if pygame.mixer.music.get_busy() == True:
                pygame.mixer.music.stop()

        pos = pygame.mixer.music.get_pos()
        txt1 = font.render("BGM pos" + str(pos / 1000), True, WHITE)
        txt2 = font.render("[P]lay bgm : [S]top bgm", True, CYAN)
        screen.fill(BLACK)
        game.draw_map(screen)
        screen.blit(txt1, [100, 100])
        screen.blit(txt2, [100, 200])
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()