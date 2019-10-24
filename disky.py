import pygame
pygame.init()
from pygame.locals import *
# from pyg_func import *
import os
import filetree
import pyg_func
import input_class
from constants import *


'''

Disky: A TreeMapping suite built on pygame

-- Written by: Maxime Gosselin, Juan Aguierre   \\ April 2012

'''


class Disky:
    '''Disky'''

    def __init__(self, size=None, tree=None, map=None):
        '''(Disky[, tuple, FTNode, List]) -> None.
        Create a new instance of Disky'''

        #start a clock
        self.fps = pygame.time.Clock()
        self.clickfocus = None  # for double click detection
        self.firstclick = False

        self.running = True
        self.updated = False
        self.size = size

        if size:
            self.fullscreen = False
        else:
            self.fullscreen = True

        self.screen = self.Screen(self.fullscreen, self.size)
        self.tree = tree
        self.map = map
        self.focus = None
        self.font = FONTS['default']
        self.fonts = FONTS
        self.lastpath = None
        self.title = self.Label('Disky', self.font)
        self.labels = [self.title]
        self.longpath = False

    def handle(self, event):
        '''(Disky, pygame Event) -> None. Handle the event'''

        #Quit button
        if event.type == pygame.QUIT:
            self.running = False

        #Esc key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                self.running = False

        #Mouse moved
        if event.type == pygame.MOUSEMOTION:

            x, y = event.pos[0], event.pos[1]
            min = self.screen.width * self.screen.width * MAPBASE * MAPBASE

            if self.focus:
                focus = None

            self.get_focus(x, y, min)
            self.draw_path()

            if not self.focus:
                for cl in self.click_labels.items():
                    cl[1].update(self.screen.screen, None, self.fonts['Arial'],\
                                           WHITE)
                    if pyg_func.in_rect(x, y, cl[1].labelRect):
                        cl[1].update(self.screen.screen, None,\
                                  FONTS['Arial'], RED)

        #Mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN:

            buttons = pygame.mouse.get_pressed()
            x, y = event.pos[0], event.pos[1]
            min = self.screen.width * self.screen.width * MAPBASE * MAPBASE
            #Left Click
            if buttons[0]:
                if self.firstclick:
                    if pygame.time.get_ticks() - self.firstclick <= 300:
                        self.clickfocus = pyg_func.get_focus(\
                            self.map, x, y, min)
                        try:
                            os.startfile(self.clickfocus['path'])
                        except Exception:
                            pass
                    else:
                        self.firstclick = pygame.time.get_ticks()
                else:
                    self.firstclick = pygame.time.get_ticks()

                for cl in self.click_labels.items():
                    if pyg_func.in_rect(x, y, cl[1].labelRect):
                        if cl[0] == 'New':

                            newpath = self.get_input()
                            newdisky = Disky(self.size)
                            newdisky.run(newpath)
                            self.quit()

                        elif cl[0] == 'Quit':
                            self.quit()

                        elif cl[0] == 'About':
                            try:
                                os.startfile('about.txt')
                            except:
                                pass
            if buttons[2]:

                self.rightclick = pyg_func.get_focus(\
                            self.map, x, y, min)
                path = os.path.split(self.rightclick['path'])[0]
                try:
                    os.startfile(path, 'explore')
                except:
                    pass

    def draw_labels(self):
        '''(Disky) -> None.
        Clean up the labels if possible and redraw the other ones.'''

        for label in self.labels.values():
            if label.dirty == True:
                label.update(self.screen.screen)
        for label in self.click_labels.values():
            label.update(self.screen.screen)

    def draw_path(self):
        '''(Disky) -> None.
        Clean up the previous path if possible and draw the current one.'''

        if self.focus:
            txt = pyg_func.txtify(self.focus['path'], self.focus['top'])
            txtlen = len(txt)
            if 'bord' not in self.focus.keys():
                ext = self.focus['node'].ext
            else:
                ext = 'folder'

            size = self.focus['node'].size.__str__()
            scale = font_sz / 22.0
            if ((txtlen * 12 * scale) + (3 * LEFTMARG)) >= \
               (self.screen.width * 0.4):
                self.updated = True
                if ((txtlen * 6 * scale) + (3 * LEFTMARG)) >= \
               (self.screen.width * 0.4):
                    gdtext = os.path.split(self.focus['path'])[1]
                    if len(gdtext) > 19:
                        gdtext = gdtext[-20:]
                    self.labels['curr_path'].update(self.screen.screen,\
                                                ('...' + gdtext))
                    self.labels['cpath_data'].erase(self.screen.screen)
                    self.labels['curr_path2'].erase(self.screen.screen)

                else:
                    self.labels['curr_path'].update(self.screen.screen,\
                                                    txt[:(txtlen // 2)])
                    self.labels['curr_path2'].update(self.screen.screen,\
                                                    txt[(txtlen // 2):])
                    if self.longpath == False:
                        self.labels['curr_path2'].erase(self.screen.screen)
                        self.labels['cpath_data'].erase(self.screen.screen)
                        #self.labels['cpath_data'].move(0,\
                                                   #int(self.screen.height *\
                                                       #0.05))
                    self.longpath = True
                self.labels['cpath_data'].update(self.screen.screen, (ext +
                                                                    ' file ' +
                                                                    size + \
                                                                    ' Bytes'))

            else:

                self.labels['curr_path'].update(self.screen.screen, txt)
                if self.longpath == True:
                    self.labels['cpath_data'].erase(self.screen.screen)
                    self.labels['curr_path2'].erase(self.screen.screen)
                    #self.labels['cpath_data'].move(0,\
                                               #-int(self.screen.height *\
                                                   #0.05))
                    self.longpath = False
                self.labels['cpath_data'].update(self.screen.screen, (ext + \
                                                                ' file    ' +\
                                                                size + \
                                                                ' Bytes'))

    def draw_map(self):
        '''(Disky[, Str]) -> None. Draw the Treemap contained in self.map'''

        if not self.updated:
            for tile in self.map:
                if tile['parent']:
                    #Clip the rectangles to fit nicely inside the borders
                    tile['rect'] = tile['rect'].clip(\
                        tile['parent'].inflate(-2, -2))
                    tile['rect'] = tile['rect'\
                    ].clip(self.map[0]['rect'].inflate(-2, -2))
                if 'bord' in tile.keys():
                    pygame.draw.rect(self.screen.screen, tile['colour'], \
                                     tile['rect'], tile['bord'])
                else:
                    pygame.draw.rect(self.screen.screen, tile['colour'], \
                                     tile['rect'])
        self.updated = True

    def get_base(self):
        '''(Disky) -> None.
        Generate the base rectangle to draw the TreeMap in.'''

        return {'rect': pygame.Rect((self.screen.width * 0.4), 0, \
                                    self.screen.width - \
                                    (self.screen.width * 0.4), \
                                    self.screen.height - path_y - 1),\
                'colour': WHITE, 'colour2': WHITE, 'parent': None}

    def get_focus(self, x, y, min):
        '''(Disky, Int, Int, Int) -> None.
        Set focus to the smallest rectangle containing the point (x, y)'''

        self.focus = pyg_func.get_focus(self.map, x, y, min)

    def get_input(self):
        '''(Disky) -> None. Get input from a text field Input object'''

        baseoptions = {'x': 0,\
                       'y': self.screen.height - (2 * path_y),\
                       'colour': WHITE, 'font': FONTS['Treb']}
        input_path = input.Input(baseoptions, self.screen.screen)

        while not input_path.returned:
            events = pygame.event.get()
            input_path.update(events)
            if input_path.dirty:
                input_path.draw()
                pygame.display.update()
            self.fps.tick(30)

        input_path.erase()
        pygame.display.update()
        if input_path.returned == '!':
            self.quit('Cheers!')
        else:
            return input_path.returned

    def make_labels(self):
        '''(None) -> None. Populate the self.labels dictionary
        with all the labels we want to display our information'''

        numfiles = len(self.map).__str__()
        size = self.tree.size.__str__()
        bg = BLACK

        self.labels = {'title': self.Label('Disky!',\
                        self.fonts['Arial Black'], WHITE, bg,\
                        LEFTMARG, int(self.screen.height * 0.03)),\
                       'curr_map': self.Label('Current Map:',\
                                              self.fonts['Treb'],\
                                              WHITE, bg,\
                                              (2 * LEFTMARG),\
                                              int(self.screen.height * 0.15)),\
                       'root': self.Label('root: ' + self.tree.path,\
                                          self.fonts['Arial'], WHITE, bg,\
                                          (3 * LEFTMARG),\
                                          int(self.screen.height * 0.2)),\
                       'root_data': self.Label(numfiles + ' files    '\
                                               + size + ' Bytes',\
                                               self.fonts['Arial'], WHITE, bg,\
                                               (3 * LEFTMARG),\
                                               int(self.screen.height * 0.25)),
                       'curr_focus': self.Label('Current Focus:', self.fonts[\
                           'Treb'], WHITE, bg, (2 * LEFTMARG),\
                                            int(self.screen.height * 0.4)),\
                       'curr_path': self.Label('', self.fonts['Arial'],\
                                               WHITE, bg, (3 * LEFTMARG),\
                                            int(self.screen.height * 0.44)),
                       'curr_path2': self.Label('', self.fonts['Arial'],\
                                                WHITE, bg, 3 * LEFTMARG,\
                                                int(self.screen.height \
                                                    * 0.47)),\
                       'cpath_data': self.Label('', self.fonts['Arial'],\
                                                WHITE, bg, 3 * LEFTMARG,\
                                                int(self.screen.height * 0.52))
                       }
        self.click_labels = {'New': self.Label('-> New Map', \
                                                 self.fonts['Treb'],\
                                           WHITE, bg, LEFTMARG,\
                                           int(self.screen.height * 0.8)),\
                       'Quit': self.Label('-> Quit',\
                                              self.fonts['Treb'],\
                                              WHITE, bg,\
                                              LEFTMARG,\
                                              int(self.screen.height * 0.86)),\
                       'About': self.Label('-> About',\
                                          self.fonts['Treb'], WHITE, bg,\
                                          LEFTMARG, int(self.screen.height * \
                                                        0.9))}

    def run(self, path=None):
        '''(Disky[, Str]) -> None. Run Disky.
        If they aren't supplied, get path data from the user,
        profile it into a filetree, and display the resulting treemap.'''

        if not self.tree:
            if not path:
                loading_screen = pygame.image.load(os.path.join(\
                    'diskylogo.png'))
                lsrect = loading_screen.get_rect()
                lsrect.x = (self.screen.width / 2) - (lsrect.width / 2)
                lsrect.y = 100
                self.screen.screen.blit(loading_screen, lsrect)
                path = self.get_input()

            self.tree = filetree.treeify(path)
            if not self.tree:
                self.quit(INVALID_PATH)
            self.map = []
            self.base = self.get_base()
            self.map.append(self.base)

        if len(self.map) == 1:
            self.map = pyg_func.map(self.map, self.map[0]['rect'], self.tree)

        self.make_labels()

        try:
            pygame.draw.rect(self.screen.screen, BLACK, lsrect)
        except:
            pass

        while(self.running):

            event = pygame.event.poll()
            self.handle(event)
            self.draw_labels()
            self.draw_map()
            pygame.display.update()
            self.fps.tick(30)
        self.quit('Goodbye')

    def quit(self, msg=None):
        '''(Disky[, Str] -> None.
        Quit Disky, print the exit msg if supplied.'''

        if msg:
            print(msg)
        pygame.quit()
        quit()

    class Screen(object):
        '''A Pygame Display class.'''

        def __init__(self, fullscreen, size):
            '''(Screen, bool, tuple) -> Pygame Display.
            construct the main Disky display.'''

            if fullscreen:
                self.screen = pygame.display.set_mode((0, 0),\
                                                      pygame.FULLSCREEN)
                self.info = pygame.display.Info()

                self.height = self.info.current_h
                self.width = self.info.current_w
            else:
                self.screen = pygame.display.set_mode((size[0], size[1]), 0)
                pygame.display.set_caption('Disky ver 1.30')
                self.info = pygame.display.Info()

                self.height = self.info.current_h
                self.width = self.info.current_w

            self.inflate = INFCST
            self.x_off = offset_x
            self.y_off = offset_y

    class Label(object):
        '''A Pygame Label class.'''

        def __init__(self, text, font, colour=WHITE, bg=BLUE, x=0, y=0):
            '''(Label, Str) -> Pygame Surface.
            Construct a new label.'''

            self.font = font
            self.colour = colour
            self.bg = bg
            self.text = text
            self.x = x
            self.y = y

            self.label = self.font.render(self.text,\
                                          True, self.colour, self.bg)
            self.labelRect = self.label.get_rect()
            self.labelRect.x = self.x
            self.labelRect.y = self.y
            self.dirty = True

        def draw(self, screen):
            '''(Label, Screen) -> None.
            Draw the label to the screen.'''

            pygame.draw.rect(screen, BLACK, self.labelRect)
            screen.blit(self.label, self.labelRect)
            self.dirty = False

        def erase(self, screen):
            '''(Label, Screen) -> Remove the label from the screen.'''

            pygame.draw.rect(screen, BLACK, self.labelRect)

        def move(self, x, y):
            '''(Label, Int, Int) -> None. Move the label by x and y'''

            self.x += x
            self.y += y
            self.labelRect.x = self.x
            self.labelRect.y = self.y

        def update(self, screen, text=None, font=None,\
                   colour=None, bg=None):
            '''(Label, , Screen[, Str, Int, Int) -> None.
            Update the label.'''

            self.erase(screen)

            if colour:
                self.colour = colour
            if bg:
                self.bg = bg

            if font:
                self.font = font
                self.label = self.font.render(self.text, True,\
                                              self.colour, self.bg)
                self.labelRect = self.label.get_rect()
                self.labelRect.x = self.x
                self.labelRect.y = self.y
            if text:
                self.text = text
                self.label = self.font.render(self.text, True,\
                                              self.colour, self.bg)
                self.labelRect = self.label.get_rect()
                self.labelRect.x = self.x
                self.labelRect.y = self.y

            self.draw(screen)

if __name__ == "__main__":
    scrn = (1024, 450)
    default = 'C:\\Users'
    print("Enter file path to inspect")
    start = input("(Hit Enter for C:\\Users):")
    if not start:
        start = default

    theApp = Disky(scrn)
    theApp.run(start)
