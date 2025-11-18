"""
__init__.py para el paquete scenes.
"""
from .base_scene import Scene
from .menu_scene import MenuScene
from .game_scene import GameScene
from .gameover_scene import GameOverScene

__all__ = [
    'Scene',
    'MenuScene',
    'GameScene',
    'GameOverScene'
]
