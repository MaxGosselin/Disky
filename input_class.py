from pygame.locals import *
from constants import *
import pygame
pygame.init()

class Input:
    '''A text input class for pygame'''

    def __init__(self, options, screen):
        '''(Input, Dict, pygame Surface) -> NoneType.
        options: x, y, font, colour, restricted, maxlength, prompt.
        Create a new instance of Input'''

        self.options = {'x': 0, 'y': 0, 'font': pygame.font.Font(None, 22),
                        'colour': (0, 0, 0),\
                        'charset': '''\'abcdefghijklmnopqrstuvwxyzABCDEFGH
                        IJKLMNOPQRSTUVWXYZ0123456789!"#$%&\\\'()*+,-./:;<
                        =>?@[\]^_`{|}~\'''',
                        'maxlen': -1, 'prompt': \
                        'Enter desired File or Directory: '}

        if not len(options) == 0:
            #modify the options
                for key in options.keys():
                    self.options[key] = options[key]

        self.x = self.options['x']
        self.y = self.options['y']
        self.font = self.options['font']
        self.colour = self.options['colour']
        self.charset = self.options['charset']
        self.maxlen = self.options['maxlen']
        self.prompt = self.options['prompt']
        self.value = ''
        self.shifted = False
        self.dirty = True
        self.returned = False
        self.last_draw = None
        self.screen = screen

    def set_pos(self, x, y):
        '''(self, int, int) -> NoneType. Set the position to x, y.'''
        self.x = x
        self.y = y

    def set_font(self, font):
        '''(self, pygame Font) -> NoneType. Set the font for the input.'''
        self.font = font

    def draw(self):
        '''(self) -> NoneType. Draw the text input to the screen.'''
        if self.last_draw:
            self.erase()
        self.text = self.font.render(self.prompt + self.value, 1, self.colour)
        self.textRect = self.text.get_rect()
        self.textRect.x = self.x
        self.textRect.y = self.y
        self.screen.blit(self.text, self.textRect)
        self.dirty = False
        colour = self.screen.get_at((self.x, self.y))
        self.last_draw = self.textRect

    def erase(self):
        '''(self) -> NoneType. Erase the text'''

        pygame.draw.rect(self.screen, BLACK, self.last_draw)

    def update(self, events):
        '''(self, List) -> NoneType. Update the text in the input.'''
        for event in events:
            if event.type == KEYUP:
                if event.key == K_LSHIFT or event.key == K_RSHIFT:
                    self.shifted = False

                    #Quit button
            if event.type == pygame.QUIT:
                self.returned = '!'

                #Esc key pressed
            if event.type == pygame.KEYDOWN:

                if event.key == K_ESCAPE:
                    self.returned = '!'

                self.dirty = True

                if event.key == K_RETURN:
                    self.returned = self.value
                    #self.erase()

                elif event.key == K_BACKSPACE:
                    self.value = self.value[:-1]

                elif event.key == K_LSHIFT or event.key == K_RSHIFT:
                    self.shifted = True

                elif event.key == K_SPACE:
                    self.value += ' '

                #Handle all non shifted keys
                if not self.shifted:
                    if event.key == K_a and 'a' in self.charset:
                        self.value += 'a'
                    elif event.key == K_b and 'b' in self.charset:
                        self.value += 'b'
                    elif event.key == K_c and 'c' in self.charset:
                        self.value += 'c'
                    elif event.key == K_d and 'd' in self.charset:
                        self.value += 'd'
                    elif event.key == K_e and 'e' in self.charset:
                        self.value += 'e'
                    elif event.key == K_f and 'f' in self.charset:
                        self.value += 'f'
                    elif event.key == K_g and 'g' in self.charset:
                        self.value += 'g'
                    elif event.key == K_h and 'h' in self.charset:
                        self.value += 'h'
                    elif event.key == K_i and 'i' in self.charset:
                        self.value += 'i'
                    elif event.key == K_j and 'j' in self.charset:
                        self.value += 'j'
                    elif event.key == K_k and 'k' in self.charset:
                        self.value += 'k'
                    elif event.key == K_l and 'l' in self.charset:
                        self.value += 'l'
                    elif event.key == K_m and 'm' in self.charset:
                        self.value += 'm'
                    elif event.key == K_n and 'n' in self.charset:
                        self.value += 'n'
                    elif event.key == K_o and 'o' in self.charset:
                        self.value += 'o'
                    elif event.key == K_p and 'p' in self.charset:
                        self.value += 'p'
                    elif event.key == K_q and 'q' in self.charset:
                        self.value += 'q'
                    elif event.key == K_r and 'r' in self.charset:
                        self.value += 'r'
                    elif event.key == K_s and 's' in self.charset:
                        self.value += 's'
                    elif event.key == K_t and 't' in self.charset:
                        self.value += 't'
                    elif event.key == K_u and 'u' in self.charset:
                        self.value += 'u'
                    elif event.key == K_v and 'v' in self.charset:
                        self.value += 'v'
                    elif event.key == K_w and 'w' in self.charset:
                        self.value += 'w'
                    elif event.key == K_x and 'x' in self.charset:
                        self.value += 'x'
                    elif event.key == K_y and 'y' in self.charset:
                        self.value += 'y'
                    elif event.key == K_z and 'z' in self.charset:
                        self.value += 'z'
                    elif event.key == K_0 and '0' in self.charset:
                        self.value += '0'
                    elif event.key == K_1 and '1' in self.charset:
                        self.value += '1'
                    elif event.key == K_2 and '2' in self.charset:
                        self.value += '2'
                    elif event.key == K_3 and '3' in self.charset:
                        self.value += '3'
                    elif event.key == K_4 and '4' in self.charset:
                        self.value += '4'
                    elif event.key == K_5 and '5' in self.charset:
                        self.value += '5'
                    elif event.key == K_6 and '6' in self.charset:
                        self.value += '6'
                    elif event.key == K_7 and '7' in self.charset:
                        self.value += '7'
                    elif event.key == K_8 and '8' in self.charset:
                        self.value += '8'
                    elif event.key == K_9 and '9' in self.charset:
                        self.value += '9'
                    elif event.key == K_BACKQUOTE and '`' in self.charset:
                        self.value += '`'
                    elif event.key == K_MINUS and '-' in self.charset:
                        self.value += '-'
                    elif event.key == K_EQUALS and '=' in self.charset:
                        self.value += '='
                    elif event.key == K_LEFTBRACKET and '[' in self.charset:
                        self.value += '['
                    elif event.key == K_RIGHTBRACKET and ']' in self.charset:
                        self.value += ']'
                    elif event.key == K_BACKSLASH and '\\' in self.charset:
                        self.value += '\\'
                    elif event.key == K_SEMICOLON and ';' in self.charset:
                        self.value += ';'
                    elif event.key == K_QUOTE and '\'' in self.charset:
                        self.value += '\''
                    elif event.key == K_COMMA and ',' in self.charset:
                        self.value += ','
                    elif event.key == K_PERIOD and '.' in self.charset:
                        self.value += '.'
                    elif event.key == K_SLASH and '/' in self.charset:
                        self.value += '/'

                #handle all shifted keys
                elif self.shifted:
                    if event.key == K_a and 'A' in self.charset:
                        self.value += 'A'
                    elif event.key == K_b and 'B' in self.charset:
                        self.value += 'B'
                    elif event.key == K_c and 'C' in self.charset:
                        self.value += 'C'
                    elif event.key == K_d and 'D' in self.charset:
                        self.value += 'D'
                    elif event.key == K_e and 'E' in self.charset:
                        self.value += 'E'
                    elif event.key == K_f and 'F' in self.charset:
                        self.value += 'F'
                    elif event.key == K_g and 'G' in self.charset:
                        self.value += 'G'
                    elif event.key == K_h and 'H' in self.charset:
                        self.value += 'H'
                    elif event.key == K_i and 'I' in self.charset:
                        self.value += 'I'
                    elif event.key == K_j and 'J' in self.charset:
                        self.value += 'J'
                    elif event.key == K_k and 'K' in self.charset:
                        self.value += 'K'
                    elif event.key == K_l and 'L' in self.charset:
                        self.value += 'L'
                    elif event.key == K_m and 'M' in self.charset:
                        self.value += 'M'
                    elif event.key == K_n and 'N' in self.charset:
                        self.value += 'N'
                    elif event.key == K_o and 'O' in self.charset:
                        self.value += 'O'
                    elif event.key == K_p and 'P' in self.charset:
                        self.value += 'P'
                    elif event.key == K_q and 'Q' in self.charset:
                        self.value += 'Q'
                    elif event.key == K_r and 'R' in self.charset:
                        self.value += 'R'
                    elif event.key == K_s and 'S' in self.charset:
                        self.value += 'S'
                    elif event.key == K_t and 'T' in self.charset:
                        self.value += 'T'
                    elif event.key == K_u and 'U' in self.charset:
                        self.value += 'U'
                    elif event.key == K_v and 'V' in self.charset:
                        self.value += 'V'
                    elif event.key == K_w and 'W' in self.charset:
                        self.value += 'W'
                    elif event.key == K_x and 'X' in self.charset:
                        self.value += 'X'
                    elif event.key == K_y and 'Y' in self.charset:
                        self.value += 'Y'
                    elif event.key == K_z and 'Z' in self.charset:
                        self.value += 'Z'
                    elif event.key == K_0 and ')' in self.charset:
                        self.value += ')'
                    elif event.key == K_1 and '!' in self.charset:
                        self.value += '!'
                    elif event.key == K_2 and '@' in self.charset:
                        self.value += '@'
                    elif event.key == K_3 and '#' in self.charset:
                        self.value += '#'
                    elif event.key == K_4 and '$' in self.charset:
                        self.value += '$'
                    elif event.key == K_5 and '%' in self.charset:
                        self.value += '%'
                    elif event.key == K_6 and '^' in self.charset:
                        self.value += '^'
                    elif event.key == K_7 and '&' in self.charset:
                        self.value += '&'
                    elif event.key == K_8 and '*' in self.charset:
                        self.value += '*'
                    elif event.key == K_9 and '(' in self.charset:
                        self.value += '('
                    elif event.key == K_BACKQUOTE and '~' in self.charset:
                        self.value += '~'
                    elif event.key == K_MINUS and '_' in self.charset:
                        self.value += '_'
                    elif event.key == K_EQUALS and '+' in self.charset:
                        self.value += '+'
                    elif event.key == K_LEFTBRACKET and '{' in self.charset:
                        self.value += '{'
                    elif event.key == K_RIGHTBRACKET and '}' in self.charset:
                        self.value += '}'
                    elif event.key == K_BACKSLASH and '|' in self.charset:
                        self.value += '|'
                    elif event.key == K_SEMICOLON and ':' in self.charset:
                        self.value += ':'
                    elif event.key == K_QUOTE and '"' in self.charset:
                        self.value += '"'
                    elif event.key == K_COMMA and '<' in self.charset:
                        self.value += '<'
                    elif event.key == K_PERIOD and '>' in self.charset:
                        self.value += '>'
                    elif event.key == K_SLASH and '?' in self.charset:
                        self.value += '?'

        #check for length violation
        if len(self.value) > self.maxlen and self.maxlen >= 0:
            self.value = self.value[:-1]
