import os
import os.path


class FTNode(object):
    ''' A FileTree Node class '''

    def __init__(self, path):
        '''(FTNode, Str) -> None. Create a new File Tree Node representing
        path.'''
        self.path = path
        self.key = _base(self.path)
        self.info = None


class FTDir(FTNode):
    '''A FileTree Directory class'''
    def __init__(self, path):
        '''(FTDir, Str) -> None. Create a new File Tree Directory representing
        path.'''
        super(FTDir, self).__init__(path)
        self.size = 0
        self.contents = None

    def populate(self):
        '''(FTDir) -> None. Search the contents of the directory and
        catalog it's contents into the contents dictionary'''

        self.contents = _populate_contents(self.path)

    def get_size(self):
        '''(FTDir) -> Int. Return the total size of all files and
        subdirectories'''

        contents = self.contents
        total = 0
        if contents:

            for item in contents.values():

                if isinstance(item, FTFile):

                    total += item.size

                else:

                    total += item.get_size()

            self.size = total
            #  4000 is approx size of the file, marginally inacurate but far
            #  more optimal than calling os.path.getsize in terms of complexity
        return total


class FTFile(FTNode):
    '''A FileTree File class'''

    def __init__(self, path):
        '''(FTDir, Str) -> None. Create a new File Tree File representing
        path.'''
        super(FTFile, self).__init__(path)
        self.size = os.path.getsize(path)
        self.ext = _ext(self.path)


def _base(path):
    '''(str) -> str. Return the base name of the path.'''

    tuple = os.path.split(path)
    if tuple[1] == '':
        return tuple[0]
    else:
        return tuple[1]


def _ext(path):
    '''(str) -> str. Return the extension of the file at path'''

    return os.path.splitext(path)[1]


def _populate_contents(path):
    '''(str) -> dict. Search the contents of the directory contained in path
    and catalog it's contents into the contents dictionary'''

    contents = {}
    for filename in os.listdir(path):
        if filename.startswith('NTUSER'):
            continue
        try:
            subitem = os.path.join(path, filename)
            #get the path of the filename
            key = _base(subitem)
            if os.path.isdir(subitem):
                #if the subitem is a directory create a new FTDir to contain it
                contents[key] = FTDir(subitem)
                contents[key].populate()
            else:
                #else the subitem must be a file, create a FTFile to contain it
                contents[key] = FTFile(subitem)
        except OSError as ose:

            pass

    return contents


def _print_FT(root, indent=''):
    '''(FTNode, Str) -> Str. Recursively print the elements of the FileTree
    rooted at root.'''

    if isinstance(root, (FTDir, FTFile)):

        print(indent + root.key + ': ' + str(root.size))

        if isinstance(root, FTDir) and root.contents:
            for el in root.contents.values():
                _print_FT(el, indent + '    ')
    else:
        print(indent + root + ': ' + str(root.size))


def treeify(path):

    '''(Str) -> FTNode filetree. Return the filetree rooted at path.
    Also vet the path to make sure it exists and/or is valid.'''

    if os.access(path, 0):

        tree = FTDir(path)
        tree.populate()
        tree.get_size()
        return tree
