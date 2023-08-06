from enum import Enum


class ObjectSource(Enum):
    """
    Objects in cache can be stored in 2 places:
    - cache: the object is stored in cache
    - database: the object is stored in database and cache
    """
    CACHE = 'cache'
    DATABASE = 'database'
