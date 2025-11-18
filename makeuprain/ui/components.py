"""
Componentes de UI modernos y reutilizables.
"""
import pygame
from typing import Tuple, Optional, Callable
from ..config import Colors
from ..utils import draw_text_with_shadow, draw_rounded_rect


class Button:
    """Botón interactivo con hover y animaciones."""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        callback: Optional[Callable] = None,
        color: Tuple[int, int, int] = Colors.PURPLE,
        hover_color: Tuple[int, int, int] = Colors.PURPLE_LIGHT,
        text_color: Tuple[int, int, int] = Colors.WHITE
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.scale = 1.0
        self.font = pygame.font.Font(None, 32)
        
    def update(self, mouse_pos: Tuple[int, int]):
        """Actualiza el estado del botón."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Animación de escala
        target_scale = 1.05 if self.is_hovered else 1.0
        self.scale += (target_scale - self.scale) * 0.2
    
    def draw(self, surface: pygame.Surface):
        """Dibuja el botón."""
        # Calcular rectángulo con escala
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_rect = pygame.Rect(
            self.rect.centerx - scaled_width // 2,
            self.rect.centery - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        
        # Color basado en hover
        color = self.hover_color if self.is_hovered else self.color
        
        # Dibujar rectángulo redondeado
        draw_rounded_rect(surface, scaled_rect, color, radius=15)
        
        # Dibujar borde
        pygame.draw.rect(surface, Colors.WHITE, scaled_rect, 2, border_radius=15)
        
        # Dibujar texto
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        surface.blit(text_surf, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Maneja eventos del botón. Retorna True si fue clickeado."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.callback:
                self.callback()
                return True
        return False


class ProgressBar:
    """Barra de progreso animada."""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        max_value: float,
        color: Tuple[int, int, int] = Colors.SUCCESS,
        bg_color: Tuple[int, int, int] = (50, 50, 60)
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.current_value = 0.0
        self.display_value = 0.0
        self.color = color
        self.bg_color = bg_color
    
    def set_value(self, value: float):
        """Establece el valor de la barra."""
        self.current_value = max(0, min(value, self.max_value))
    
    def update(self):
        """Actualiza la animación de la barra."""
        self.display_value += (self.current_value - self.display_value) * 0.1
    
    def draw(self, surface: pygame.Surface):
        """Dibuja la barra de progreso."""
        # Fondo
        draw_rounded_rect(surface, self.rect, self.bg_color, radius=8)
        
        # Progreso
        progress = self.display_value / self.max_value
        fill_width = int(self.rect.width * progress)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            draw_rounded_rect(surface, fill_rect, self.color, radius=8)
        
        # Borde
        pygame.draw.rect(surface, Colors.WHITE, self.rect, 2, border_radius=8)


class FloatingText:
    """Texto flotante animado para feedback visual."""
    
    def __init__(
        self,
        text: str,
        x: float,
        y: float,
        color: Tuple[int, int, int] = Colors.GOLD,
        size: int = 32,
        lifetime: int = 60
    ):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.font = pygame.font.Font(None, size)
        self.vy = -2  # Velocidad vertical
        
    def update(self):
        """Actualiza el texto flotante."""
        self.y += self.vy
        self.vy += 0.05  # Desaceleración
        self.lifetime -= 1
    
    def draw(self, surface: pygame.Surface):
        """Dibuja el texto con fade out."""
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            text_surf = self.font.render(self.text, True, self.color)
            text_surf.set_alpha(alpha)
            text_rect = text_surf.get_rect(center=(int(self.x), int(self.y)))
            
            # Sombra
            shadow = self.font.render(self.text, True, (0, 0, 0))
            shadow.set_alpha(alpha // 2)
            surface.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
            
            # Texto
            surface.blit(text_surf, text_rect)
    
    def is_dead(self) -> bool:
        """Verifica si el texto debe ser eliminado."""
        return self.lifetime <= 0


class Panel:
    """Panel contenedor para agrupar elementos de UI."""
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int] = Colors.DARK_BG,
        alpha: int = 200
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.alpha = alpha
    
    def draw(self, surface: pygame.Surface):
        """Dibuja el panel."""
        draw_rounded_rect(surface, self.rect, self.color, radius=20, alpha=self.alpha)
        pygame.draw.rect(surface, Colors.PURPLE_LIGHT, self.rect, 3, border_radius=20)
