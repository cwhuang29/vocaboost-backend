from datetime import datetime
from utils.enum import HIGHLIGHTER_BG_COLORS, HIGHLIGHTER_FONT_SIZE, LANGS


DEFAULT_SETTING = {
    'highlightColor': HIGHLIGHTER_BG_COLORS.YELLOW,
    'language': LANGS.en,
    'fontSize': HIGHLIGHTER_FONT_SIZE.MEDIUM,
    'showDetail': True,
    'collectedWords': [],
    'suspendedPages': [],
    'updatedAt': datetime(2000, 1, 1, 18, 0, 0)
}
