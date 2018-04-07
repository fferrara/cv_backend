__author__ = 'Flavio Ferrara'


class LabelNotFoundException(Exception):
    def __init__(self, label):
        self.label = label