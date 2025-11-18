"""
Clase base para todas las escenas del juego.
"""
import pygame
from abc import ABC, abstractmethod
from typing import Optional


class Scene(ABC):
    """Clase abstracta base para escenas."""
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.next_scene: Optional[str] = None
        self.transition_alpha = 0
        self.transitioning_out = False
        
    @abstractmethod
    def handle_events(self, events: list):
        """Maneja eventos de pygame."""
        pass
    
    @abstractmethod
    def update(self):
        """Actualiza la lógica de la escena."""
        pass
    
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        """Dibuja la escena."""
        pass
    
    def on_enter(self):
        """Llamado cuando la escena se vuelve activa."""
        self.transition_alpha = 255
        self.transitioning_out = False
        self.next_scene = None
    
    def on_exit(self):
        """Llamado cuando la escena va a ser reemplazada."""
        pass
    
    def start_transition(self, next_scene: str):
        """Inicia transición a otra escena."""
        self.next_scene = next_scene
        self.transitioning_out = True
    
    def update_transition(self):
        """Actualiza el efecto de transición."""
        if self.transitioning_out:
            self.transition_alpha += 15
            if self.transition_alpha >= 255:
                return True  # Transición completa
        else:
            if self.transition_alpha > 0:
                self.transition_alpha -= 15
        return False
    
    def draw_transition(self, screen: pygame.Surface):
        """Dibuja el overlay de transición."""
        if self.transition_alpha > 0:
            overlay = pygame.Surface(screen.get_size())
            overlay.fill((0, 0, 0))
            overlay.set_alpha(self.transition_alpha)
            screen.blit(overlay, (0, 0))
