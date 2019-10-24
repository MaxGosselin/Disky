import random
import os
import filetree
import pygame

WHITE = (255, 255, 255)


def map(blocks, rect, root, top_path=None, parent_fold=None):
    '''(List, pygame Rect, FTNode[, Str]) -> List.
    Return a list of dictionaries.
    Each dictionary contains the information to create a TreeMap
    representation of the tree rooted at root.'''

    if not top_path:
        topdir = True
        top_path = root.path

    topleft_x = rect.topleft[0]
    topleft_y = rect. topleft[1]
    total = root.size

    if rect.height > rect.width:
        vert = False
    else:
        vert = True

    try:
        if root.contents:

            for el in root.contents.values():
                if el.size == 0:
                    continue
                var = float(el.size) / root.size
                # Tiling: determine which way to orient slices
                if vert:
                    height = rect.height
                    width = var * rect.width

                else:
                    width = rect.width
                    height = var * rect.height

                #Detect folders
                if isinstance(el, filetree.FTDir):
                    newrect = {'rect': pygame.Rect(topleft_x, \
                                                   topleft_y, width, height), \
                               'colour': WHITE, 'colour2': _col2(el.path),\
                               'node': el, 'path': el.path, \
                               'top': top_path, 'parent': parent_fold,\
                               'bord': 1}
                    blocks.append(newrect)
                    map(blocks, newrect['rect'], el, top_path, newrect['rect'])

                    if vert:
                        topleft_x += width
                    else:
                        topleft_y += height

                else:
                    newrect = {'rect': pygame.Rect(topleft_x, \
                                                   topleft_y, width, height), \
                               'colour': _col(), 'colour2': _col2(el.path), \
                               'node': el, 'path': el.path, 'top': top_path,\
                               'parent': parent_fold}

                    if vert:
                        topleft_x += width
                    else:
                        topleft_y += height

                    blocks.append(newrect)
    except Exception as e:
        x = e.message

        print(x)

    return blocks


def in_rect(x, y, rect):
    '''(Int, Int, pygame Rect) -> Bool.
    Return True if the point (x, y) is in the bounds of rect.'''

    if (x >= rect.left) and (x <= rect.right) and \
       (y >= rect.top) and (y <= rect.bottom):
        return True


def get_focus(map, x, y, min):
    '''(Disky, Int, Int, Int) -> Dict.
        Set focus to the smallest rectangle containing the point (x, y),
        return it's containing dict.'''

    focus = None
    for tile in map:
        if in_rect(x, y, tile['rect']) and \
                (tile['rect'].size[0] * tile['rect'].size[1]) <= min:
                min = tile['rect'].size[0] * tile['rect'].size[1]
                focus = tile

    return focus


def _col():

    '''(NoneType) -> Tuple (R, G, B). Return a random colour tuple.'''

    col = range(256)
    return (random.choice(col), random.choice(col), \
                 random.choice(col))


def _col2(path):
    '''(Str) -> Tuple (R, G, B). Return a colour
    tuple based on the file type.'''

    #gray = range(101)
    #filetype = os.path.split(path)[1]

    #for type in extensions:
        #for ext in type:
            #if isinstance(ext, str):
                #if ext in filetype:
                    #return type[1]

    #return (random.choice(gray), random.choice(gray), \
                 #random.choice(gray))

    return None


def txtify(path, top):
    '''(Str, Str) -> Str. Remove the top path from the current one to make it
    more legible.'''

    return path[len(top) + 1:]
