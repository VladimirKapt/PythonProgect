import pygame
import random
import textwrap
import time

class PrintSpeed:
    def __init__(self):
        pygame.init()
        self.win_width, self.win_height = 800, 600
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        self.font = pygame.font.Font(None, 32)
        self.words = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
        self.correct_text = ' '.join(random.choice(self.words) for _ in range(10))
        self.text_width = 60
        self.wrapped_text = textwrap.wrap(self.correct_text, width=self.text_width)
        self.running = True
        self.user_text = ''
        self.start_time = time.time()
        self.end_time = None
        self.total_errors = 0
        self.finished = False
        self.key_size = 30
        self.key_spacing = 10

    def run(self):
        keyboard = Keyboard(self.win, (self.win_width - (13 * (self.key_size + self.key_spacing) - self.key_spacing)) // 2, self.win_height - 200, self.key_size)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if self.finished:
                        self.__init__()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode
                        if len(self.correct_text) >= len(self.user_text) and self.correct_text[len(self.user_text)-1] != event.unicode:
                            self.total_errors += 1
                        if len(self.user_text) == len(self.correct_text):
                            self.finished = True
                            self.end_time = time.time()
                keyboard.handle_event(event)

            self.win.fill((30, 30, 30))
            keyboard.draw()
            self.display_text()
            self.display_stats()
            
            pygame.display.flip()

        pygame.quit()

    def display_text(self):
        user_wrapped_text = textwrap.wrap(self.user_text, width=self.text_width)
        for i, line in enumerate(self.wrapped_text):
            x = (self.win_width - self.font.size(line)[0]) // 2
            for j, char in enumerate(line):
                if len(self.user_text) > i * self.text_width + j:
                    if self.user_text[i * self.text_width + j] == char:
                        color = pygame.Color('white')
                    elif self.user_text[i * self.text_width + j] == ' ' and char != ' ':
                        color = pygame.Color('red')  
                    elif self.user_text[i * self.text_width + j] != ' ' and char == ' ':
                        color = pygame.Color('red')  
                    else:
                        color = pygame.Color('red')
                else:
                    color = pygame.Color('darkgray')
                txt_surface = self.font.render(char if char != ' ' else '_', True, color)  
                self.win.blit(txt_surface, (x, 20 + i * 32))
                x += txt_surface.get_width()


    def display_stats(self):
        elapsed_time = time.time() - self.start_time
        typing_speed = len(self.user_text) / elapsed_time * 60
        error_rate = self.total_errors / len(self.user_text) * 100 if len(self.user_text) > 0 else 0
        speed_surface = self.font.render(f"Скорость печати: {typing_speed:.2f} символов в минуту", True, pygame.Color('gray'))
        error_surface = self.font.render(f"Процент ошибок: {error_rate:.2f}%", True, pygame.Color('gray'))
        self.win.blit(speed_surface, (20, self.win_height - 64))
        self.win.blit(error_surface, (20, self.win_height - 32))

        if self.finished:
            finish_elapsed_time = self.end_time - self.start_time
            typing_speed = len(self.user_text) / finish_elapsed_time * 60
            overlay = pygame.Surface((self.win_width, self.win_height))  
            overlay.set_alpha(160) 
            overlay.fill((0, 0, 0)) 
            self.win.blit(overlay, (0, 0)) 
            final_text = f"Итоговая скорость печати: {typing_speed:.2f} символов в минуту\nПроцент ошибок: {error_rate:.2f}%"
            lines = final_text.split("\n")
            for i, line in enumerate(lines):
                txt_surface = self.font.render(line, True, pygame.Color('white'))
                x = (self.win_width - txt_surface.get_width()) // 2
                y = (self.win_height - txt_surface.get_height()) // 2 + i * 32
                self.win.blit(txt_surface, (x, y))

class Keyboard:
    def __init__(self, win, x, y, key_size):
        self.win = win
        self.x = x - 35
        self.y = y - 100
        self.key_size = key_size
        self.key_spacing = 5
        self.keys = [
            [('`', pygame.Color('lightgreen')), ('1', pygame.Color('lightgreen')), ('2', pygame.Color('green')), ('3', pygame.Color('lightyellow')), ('4', pygame.Color('cyan')), ('5', pygame.Color('cyan')), ('6', pygame.Color('pink')), ('7', pygame.Color('pink')), ('8', pygame.Color('lightyellow')), ('9', pygame.Color('green')), ('0', pygame.Color('lightgreen')), ('-', pygame.Color('lightgreen')), ('=', pygame.Color('lightgreen')),('                     backspace                         ', pygame.Color('lightgreen'))],
            [('        tab         ', pygame.Color('lightgreen')),('q', pygame.Color('lightgreen')), ('w', pygame.Color('green')), ('e', pygame.Color('lightyellow')), ('r', pygame.Color('cyan')), ('t', pygame.Color('cyan')), ('y', pygame.Color('pink')), ('u', pygame.Color('pink')), ('i', pygame.Color('lightyellow')), ('o', pygame.Color('green')), ('p', pygame.Color('lightgreen')), ('[', pygame.Color('lightgreen')), (']', pygame.Color('lightgreen')), ('             \\                      ', pygame.Color('lightgreen'))],
            [('          capsL              ', pygame.Color('lightgreen')), ('a', pygame.Color('lightgreen')), ('s', pygame.Color('green')), ('d', pygame.Color('lightyellow')), ('f', pygame.Color('cyan')), ('g', pygame.Color('cyan')), ('h', pygame.Color('pink')), ('j', pygame.Color('pink')), ('k', pygame.Color('lightyellow')), ('l', pygame.Color('green')), (';', pygame.Color('lightgreen')), ("'", pygame.Color('lightgreen')), ('                       enter                                    ', pygame.Color('lightgreen'))],
            [('            shift                     ', pygame.Color('lightgreen')), ('z', pygame.Color('lightgreen')), ('x', pygame.Color('green')), ('c', pygame.Color('lightyellow')), ('v', pygame.Color('cyan')), ('b', pygame.Color('cyan')), ('n', pygame.Color('pink')), ('m', pygame.Color('pink')), (',', pygame.Color('lightyellow')), ('.', pygame.Color('green')), ('/', pygame.Color('lightgreen')), ('                                      shift                                                 ', pygame.Color('lightgreen'))],
            [('        ctrl         ', pygame.Color('lightgreen')), ('    alt        ', pygame.Color('lightgreen')), ('                                                                                                                                                              space                                                                                                                                                               ', pygame.Color('red')), ('      alt       ', pygame.Color('lightgreen')), ('        ctrl       ', pygame.Color('lightgreen'))]
        ]
        self.pressed_keys = set()

    def draw(self):
        x_offset = self.x
        for i, row in enumerate(self.keys):
            y_offset = self.y + i * (self.key_size + self.key_spacing)
            for j, (key, color) in enumerate(row):
                if key in self.pressed_keys:
                    color = pygame.Color('darkgray')
                key_width = self.key_size + (len(key) + 1)
                rect = pygame.Rect(x_offset, y_offset, key_width, self.key_size)
                pygame.draw.rect(self.win, color, rect)
                text_surface = pygame.font.Font(None, 20).render(key, True, pygame.Color('black'))
                self.win.blit(text_surface, (rect.x + (key_width - text_surface.get_width()) // 2, rect.y + (self.key_size - text_surface.get_height()) // 2))
                x_offset += key_width + self.key_spacing
            x_offset = self.x


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            for row in self.keys:
                for key, _ in row:
                    if event.unicode == key:
                        self.pressed_keys.add(key)
        elif event.type == pygame.KEYUP:
            for row in self.keys:
                for key, _ in row:
                    if event.unicode == key:
                        self.pressed_keys.discard(key)

if __name__ == "__main__":
    game = PrintSpeed()
    game.run()
