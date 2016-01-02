__version__ = "0.18.0"
__author__ = "Pasha Podolsky"
__name__ = 'megazord'
__homepage__ = "http://github.com/PashaPodolsky/megazord/"

from .tools import *
from .target import *

import megazord.meta as meta
import megazord.system as system
import megazord.utils as tools
import megazord.interstate as interstate

__all__ = ['Target']

verbose = 2
