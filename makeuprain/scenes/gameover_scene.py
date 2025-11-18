"""
Escena de Game Over.
"""
import pygame
from .base_scene import Scene
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, Colors
from ..ui import Button, Panel
from ..utils import create_gradient_surface


class GameOverScene(Scene):
    """Escena mostrada al perder el juego."""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # Fondo
        self.background = create_gradient_surface(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            (30, 20, 40),
            Colors.DARK_BG,
            vertical=True
        )
        
        # Fuentes
        self.title_font = pygame.font.Font(None, 72)
        self.score_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)
        
        # Panel principal
        self.main_panel = Panel(
            SCREEN_WIDTH // 2 - 300,
            SCREEN_HEIGHT // 2 - 200,
            600,
            400,
            alpha=220
        )
        
        # Botones
        button_width = 250
        button_height = 60
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.retry_button = Button(
            button_x,
            SCREEN_HEIGHT // 2 + 80,
            button_width,
            button_height,
            "REINTENTAR",
            callback=self.retry_game,
            color=Colors.SUCCESS,
            hover_color=Colors.PINK
        )
        
        self.menu_button = Button(
            button_x,
            SCREEN_HEIGHT // 2 + 160,
            button_width,
            button_height,
            "MENÚ PRINCIPAL",
            callback=self.go_to_menu,
            color=Colors.PURPLE,
            hover_color=Colors.PURPLE_LIGHT
        )
        
        # Animación
        self.pulse = 0
        self.is_new_record = False
        
    def retry_game(self):
        """Reinicia el juego."""
        self.start_transition('game')
    
    def go_to_menu(self):
        """Vuelve al menú principal."""
        self.start_transition('menu')
    
    def on_enter(self):
        """Al entrar, verifica si hay nuevo récord."""
        super().on_enter()
        score_system = self.game_manager.score_system
        self.is_new_record = score_system.score == score_system.high_score and score_system.score > 0
        
        # Obtener datos de los jugadores
        from ..scenes.game_scene import GameScene
        game_scene = None
        for scene_name, scene in self.game_manager.scenes.items():
            if isinstance(scene, GameScene):
                game_scene = scene
                break
        
        self.player_scores = []
        self.winner_id = None
        
        if game_scene and game_scene.players:
            # Recopilar puntajes
            for player in game_scene.players:
                self.player_scores.append({
                    'id': player.player_id,
                    'score': player.score,
                    'tint': player.tint_color
                })
            
            # Determinar ganador en modo cooperativo
            if len(self.player_scores) == 2:
                if self.player_scores[0]['score'] > self.player_scores[1]['score']:
                    self.winner_id = 1
                elif self.player_scores[1]['score'] > self.player_scores[0]['score']:
                    self.winner_id = 2
                # Si empatan, winner_id queda None
    
    def handle_events(self, events: list):
        """Maneja eventos de Game Over."""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                    self.retry_game()
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                    self.go_to_menu()
            
            self.retry_button.handle_event(event)
            self.menu_button.handle_event(event)
        
        self.retry_button.update(mouse_pos)
        self.menu_button.update(mouse_pos)
    
    def update(self):
        """Actualiza la escena."""
        self.pulse += 0.05
        
        # Actualizar transición
        if self.update_transition() and self.next_scene:
            self.game_manager.change_scene(self.next_scene)
    
    def draw(self, screen: pygame.Surface):
        """Dibuja la pantalla de Game Over."""
        # Fondo
        screen.blit(self.background, (0, 0))
        
        # Panel principal
        self.main_panel.draw(screen)
        
        # Título "GAME OVER"
        title_color = Colors.DANGER if not self.is_new_record else Colors.GOLD
        title_text = self.title_font.render("GAME OVER", True, title_color)
        title_shadow = self.title_font.render("GAME OVER", True, Colors.BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title_text, title_rect)
        
        # Mostrar puntajes según modo de juego
        if len(self.player_scores) == 2:
            # Modo cooperativo - mostrar ganador y ambos puntajes
            y_pos = SCREEN_HEIGHT // 2 - 60
            
            # Anunciar ganador
            if self.winner_id:
                # Efecto de pulso para el ganador
                pulse_scale = 1.0 + 0.1 * abs(pygame.math.Vector2(1, 0).rotate(self.pulse * 100).y)
                winner_font_size = int(48 * pulse_scale)
                winner_font = pygame.font.Font(None, winner_font_size)
                
                winner_text = winner_font.render(
                    f"¡Jugador {self.winner_id} Gana! 🏆",
                    True,
                    Colors.GOLD
                )
                winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                screen.blit(winner_text, winner_rect)
                y_pos += 60
            else:
                # Empate
                tie_text = self.score_font.render(
                    "¡Empate!",
                    True,
                    Colors.CYAN
                )
                tie_rect = tie_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                screen.blit(tie_text, tie_rect)
                y_pos += 60
            
            # Puntajes individuales
            for player_data in self.player_scores:
                player_color = player_data['tint'] if player_data['tint'] else Colors.WHITE
                score_text = self.text_font.render(
                    f"Jugador {player_data['id']}: {player_data['score']} puntos",
                    True,
                    player_color
                )
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                screen.blit(score_text, score_rect)
                y_pos += 40
        else:
            # Modo un jugador - puntaje tradicional
            score_system = self.game_manager.score_system
            score_text = self.score_font.render(
                f"Puntuación: {score_system.score}",
                True,
                Colors.PINK
            )
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(score_text, score_rect)
            
            # Mejor puntuación
            if self.is_new_record:
                # Efecto de pulso para nuevo récord
                pulse_scale = 1.0 + 0.1 * abs(pygame.math.Vector2(1, 0).rotate(self.pulse * 100).y)
                record_font_size = int(36 * pulse_scale)
                record_font = pygame.font.Font(None, record_font_size)
                
                record_text = record_font.render(
                    "¡NUEVO RÉCORD! 🏆",
                    True,
                    Colors.GOLD
                )
                record_rect = record_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
                screen.blit(record_text, record_rect)
            else:
                high_score_text = self.text_font.render(
                    f"Mejor puntaje: {score_system.high_score}",
                    True,
                    Colors.GOLD
                )
                high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
                screen.blit(high_score_text, high_score_rect)
        
        # Botones
        self.retry_button.draw(screen)
        self.menu_button.draw(screen)
        
        # Hints de teclado
        hint_font = pygame.font.Font(None, 20)
        hints = [
            "R o ESPACIO - Reintentar",
            "M o ESC - Menú"
        ]
        y_offset = SCREEN_HEIGHT - 60
        for hint in hints:
            hint_text = hint_font.render(hint, True, Colors.TEXT_SECONDARY)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(hint_text, hint_rect)
            y_offset += 25
        
        # Efecto de transición
        self.draw_transition(screen)
