import ConfigParser, os
import re
from ConfigParser import NoOptionError

BLACKLIST_169 = ('540', '649')

config = ConfigParser.ConfigParser()
p = os.path.dirname(__file__)
config.read(os.path.join(p, 'pyTivo.conf'))

def get169Setting(tsn):
    if not tsn:
        return True

    if config.has_section('_tivo_' + tsn):
        if config.has_option('_tivo_' + tsn, 'aspect169'):
            if config.get('_tivo_' + tsn, 'aspect169').lower() == 'true':
                return True
            else:
                return False    
    
    if tsn[:3] in BLACKLIST_169:
        return False

    return True

def getShares():
    return filter( lambda x: not(x.startswith('_tivo_') or x == 'Server'), config.sections())

def getDebug():
    try:
        debug = config.get('Server', 'debug')
        if debug.lower() == 'true':
            return True
        else:
            return False
    except NoOptionError:
        return False

def get(section, key):
    return config.get(section, key)

def getValidWidths():
    return [1440, 720, 704, 544, 480, 352]

def getValidHeights():
    return [720, 480] # Technically 240 is also supported

# Return the number in list that is nearest to x
# if two values are equidistant, return the larger
def nearest(x, list):
    return reduce(lambda a, b: a if abs(x-a) < abs(x-b) or (abs(x-a) == abs(x-b)and a>b) else b, list)

def nearestTivoWidth(width):
    return nearest(width, getValidWidths())

def getTivoHeight():
    try:
        height = int(config.get('Server', 'height'))
        print nearest(height, getValidHeights())
        return nearest(height, getValidHeights())
    except NoOptionError: #default
        return 480

def getTivoWidth():
    try:
        width = int(config.get('Server', 'width'))
        print nearestTivoWidth(width)
        return nearestTivoWidth(width)
    except NoOptionError: #default
        return 544

def getAudioBR():
    try:
        return config.get('Server', 'audio_br')
    except NoOptionError: #default to 192
        return '192K'

def getVideoBR():
    try:
        return config.get('Server', 'video_br')
    except NoOptionError: #default to 4096K
        return '4096K'

