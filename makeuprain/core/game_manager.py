"""
Game Manager - Controla el flujo del juego y las escenas.
"""
import pygame
from typing import Dict
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE, Colors, FULLSCREEN, RESIZABLE
from ..scenes import MenuScene, GameScene, GameOverScene
from ..ui import ScoreSystem


class GameManager:
    """Gestor principal del juego."""
    
    def __init__(self):
        # Inicializar Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Configurar pantalla con opciones
        flags = 0
        if FULLSCREEN:
            flags = pygame.FULLSCREEN
        elif RESIZABLE:
            flags = pygame.RESIZABLE
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.display.set_caption(GAME_TITLE)
        
        # Surface virtual para el juego (resolución fija)
        self.game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Reloj para FPS
        self.clock = pygame.time.Clock()
        
        # Sistema de puntuación global
        self.score_system = ScoreSystem()
        
        # Modo de juego (1 = Single, 2 = Coop)
        self.game_mode = 1
        
        # Escenas
        self.scenes: Dict[str, object] = {
            'menu': MenuScene(self),
            'game': GameScene(self),
            'gameover': GameOverScene(self)
        }
        
        self.current_scene = self.scenes['menu']
        self.current_scene.on_enter()
        
        # Estado
        self.running = True
    
    def change_scene(self, scene_name: str):
        """Cambia a una nueva escena."""
        if scene_name in self.scenes:
            self.current_scene.on_exit()
            self.current_scene = self.scenes[scene_name]
            self.current_scene.on_enter()
    
    def run(self):
        """Bucle principal del juego."""
        try:
            while self.running:
                # Eventos
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        # F11 para alternar pantalla completa
                        if event.key == pygame.K_F11:
                            self._toggle_fullscreen()
                    elif event.type == pygame.VIDEORESIZE:
                        # Manejar redimensionamiento
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
                # Actualizar escena actual
                self.current_scene.handle_events(events)
                self.current_scene.update()
                
                # Dibujar en la superficie virtual
                self.game_surface.fill(Colors.DARK_BG)
                self.current_scene.draw(self.game_surface)
                
                # Escalar y centrar la superficie en la pantalla real
                self._scale_and_draw()
                
                # Actualizar pantalla
                pygame.display.flip()
                self.clock.tick(FPS)
        
        except SystemExit:
            pass
        finally:
            pygame.quit()
    
    def _scale_and_draw(self):
        """Escala y centra la superficie del juego en la pantalla."""
        screen_width, screen_height = self.screen.get_size()
        
        # Calcular el ratio de aspecto
        scale_x = screen_width / SCREEN_WIDTH
        scale_y = screen_height / SCREEN_HEIGHT
        scale = min(scale_x, scale_y)  # Mantener aspecto
        
        # Calcular tamaño escalado
        scaled_width = int(SCREEN_WIDTH * scale)
        scaled_height = int(SCREEN_HEIGHT * scale)
        
        # Calcular posición para centrar
        x_offset = (screen_width - scaled_width) // 2
        y_offset = (screen_height - scaled_height) // 2
        
        # Llenar la pantalla de negro
        self.screen.fill(Colors.BLACK)
        
        # Escalar y dibujar la superficie del juego
        scaled_surface = pygame.transform.smoothscale(self.game_surface, (scaled_width, scaled_height))
        self.screen.blit(scaled_surface, (x_offset, y_offset))
    
    def _toggle_fullscreen(self):
        """Alterna entre modo ventana y pantalla completa."""
        flags = pygame.display.get_surface().get_flags()
        if flags & pygame.FULLSCREEN:
            # Cambiar a modo ventana
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        else:
            # Cambiar a pantalla completa
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
