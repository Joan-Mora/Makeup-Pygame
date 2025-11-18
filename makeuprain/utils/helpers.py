"""
Funciones de utilidad y helpers generales.
"""
import pygame
import math
import json
import os
from typing import Tuple


def lerp(start: float, end: float, t: float) -> float:
    """Interpolación lineal."""
    return start + (end - start) * t


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Limita un valor entre min y max."""
    return max(min_val, min(value, max_val))


def distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """Calcula la distancia euclidiana entre dos puntos."""
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)


def rect_collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """Detecta colisión entre dos rectángulos."""
    return rect1.colliderect(rect2)


def draw_text_with_shadow(
    surface: pygame.Surface,
    text: str,
    pos: Tuple[int, int],
    font: pygame.font.Font,
    color: Tuple[int, int, int],
    shadow_offset: int = 2
):
    """Dibuja texto con sombra para mejor legibilidad."""
    # Sombra
    shadow = font.render(text, True, (0, 0, 0))
    surface.blit(shadow, (pos[0] + shadow_offset, pos[1] + shadow_offset))
    # Texto principal
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)


def draw_rounded_rect(
    surface: pygame.Surface,
    rect: pygame.Rect,
    color: Tuple[int, int, int],
    radius: int = 10,
    alpha: int = 255
):
    """Dibuja un rectángulo con esquinas redondeadas."""
    if alpha < 255:
        # Crear superficie temporal con transparencia
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, (*color, alpha), temp_surface.get_rect(), border_radius=radius)
        surface.blit(temp_surface, rect.topleft)
    else:
        pygame.draw.rect(surface, color, rect, border_radius=radius)


def save_high_score(score: int, filepath: str):
    """Guarda el puntaje más alto en un archivo JSON."""
    data = {'high_score': score}
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error guardando high score: {e}")


def load_high_score(filepath: str) -> int:
    """Carga el puntaje más alto desde un archivo JSON."""
    if not os.path.exists(filepath):
        return 0
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data.get('high_score', 0)
    except Exception as e:
        print(f"Error cargando high score: {e}")
        return 0


def create_gradient_surface(
    width: int,
    height: int,
    color1: Tuple[int, int, int],
    color2: Tuple[int, int, int],
    vertical: bool = True
) -> pygame.Surface:
    """Crea una superficie con gradiente de color."""
    surface = pygame.Surface((width, height))
    
    if vertical:
        for y in range(height):
            t = y / height
            color = (
                int(lerp(color1[0], color2[0], t)),
                int(lerp(color1[1], color2[1], t)),
                int(lerp(color1[2], color2[2], t))
            )
            pygame.draw.line(surface, color, (0, y), (width, y))
    else:
        for x in range(width):
            t = x / width
            color = (
                int(lerp(color1[0], color2[0], t)),
                int(lerp(color1[1], color2[1], t)),
                int(lerp(color1[2], color2[2], t))
            )
            pygame.draw.line(surface, color, (x, 0), (x, height))
    
    return surface
