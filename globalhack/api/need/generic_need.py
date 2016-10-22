from ..db import Database

class GenericNeed(object):
    def get(self, item_id=None):
        return Database().getProvidedNeedsFor(self.__class__.__name__.lower(),
                                              item_id)
