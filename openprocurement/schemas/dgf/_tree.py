

class Tree(object):

    index = 0
    versions = None  # list
    children = None  # list

    def __init__(self, index=None, versions=None):
        self.index = index
        self.versions = versions or dict()
        self.children = list()
