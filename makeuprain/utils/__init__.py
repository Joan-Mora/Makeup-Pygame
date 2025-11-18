"""
__init__.py para el paquete utils.
"""
from .asset_manager import asset_manager, AssetManager
from .helpers import (
    lerp,
    clamp,
    distance,
    rect_collision,
    draw_text_with_shadow,
    draw_rounded_rect,
    save_high_score,
    load_high_score,
    create_gradient_surface
)

__all__ = [
    'asset_manager',
    'AssetManager',
    'lerp',
    'clamp',
    'distance',
    'rect_collision',
    'draw_text_with_shadow',
    'draw_rounded_rect',
    'save_high_score',
    'load_high_score',
    'create_gradient_surface'
]
