"""
__init__.py para el paquete entities.
"""
from .game_entities import (
    Entity,
    Player,
    Enemy,
    Collectible,
    Particle,
    create_particle_burst
)

__all__ = [
    'Entity',
    'Player',
    'Enemy',
    'Collectible',
    'Particle',
    'create_particle_burst'
]
