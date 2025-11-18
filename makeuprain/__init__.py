"""
Camigame - Makeup Rain Game Package
Juego arcade de recolección mejorado con arquitectura profesional.
"""

__version__ = '2.0.0'
__author__ = 'Camilandia20'

from .core.game_manager import GameManager


def run():
    """Punto de entrada principal del juego."""
    game = GameManager()
    game.run()


__all__ = ['run', 'GameManager']
