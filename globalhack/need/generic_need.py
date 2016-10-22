from ..db import Database

class GenericNeed(object):
    def get(self):
        return Database().getProvidedNeedsFor(self.__class__.__name__.lower())
