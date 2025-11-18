"""
Escena del menú principal.
"""
import pygame
from .base_scene import Scene
from ..config import SCREEN_WIDTH, SCREEN_HEIGHT, Colors
from ..ui import Button, Panel
from ..utils import create_gradient_surface, draw_text_with_shadow


class MenuScene(Scene):
    """Menú principal del juego."""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # Crear fondo con gradiente
        self.background = create_gradient_surface(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            Colors.DARK_BG,
            Colors.PURPLE_DARK,
            vertical=True
        )
        
        # Fuentes
        self.title_font = pygame.font.Font(None, 84)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.controls_font = pygame.font.Font(None, 24)
        
        # Botones (columna derecha)
        button_width = 240
        button_height = 55
        button_x = 480  # Alineado con columna derecha
        
        self.single_player_button = Button(
            button_x,
            270,
            button_width,
            button_height,
            "INDIVIDUAL",
            callback=self.start_single_player,
            color=Colors.PURPLE,
            hover_color=Colors.PINK
        )
        
        self.coop_button = Button(
            button_x,
            360,
            button_width,
            button_height,
            "COOPERATIVO",
            callback=self.start_coop,
            color=Colors.CYAN,
            hover_color=Colors.PINK_LIGHT
        )
        
        self.quit_button = Button(
            button_x,
            440,
            button_width,
            button_height,
            "SALIR",
            callback=self.quit_game,
            color=Colors.PURPLE_DARK,
            hover_color=Colors.DANGER
        )
        
        # Animación del título
        self.title_bounce = 0
        
    def start_single_player(self):
        """Inicia el juego en modo 1 jugador."""
        self.game_manager.game_mode = 1  # Single player
        self.start_transition('game')
    
    def start_coop(self):
        """Inicia el juego en modo cooperativo."""
        self.game_manager.game_mode = 2  # Cooperative
        self.start_transition('game')
    
    def quit_game(self):
        """Sale del juego."""
        pygame.quit()
        raise SystemExit
    
    def handle_events(self, events: list):
        """Maneja eventos del menú."""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.start_single_player()
                elif event.key == pygame.K_1:
                    self.start_single_player()
                elif event.key == pygame.K_2:
                    self.start_coop()
                elif event.key == pygame.K_ESCAPE:
                    self.quit_game()
            
            self.single_player_button.handle_event(event)
            self.coop_button.handle_event(event)
            self.quit_button.handle_event(event)
        
        self.single_player_button.update(mouse_pos)
        self.coop_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)
    
    def update(self):
        """Actualiza el menú."""
        self.title_bounce += 0.05
        
        # Actualizar transición
        if self.update_transition() and self.next_scene:
            self.game_manager.change_scene(self.next_scene)
    
    def draw(self, screen: pygame.Surface):
        """Dibuja el menú."""
        # Fondo
        screen.blit(self.background, (0, 0))
        
        # Título con animación de rebote
        bounce_offset = int(pygame.math.Vector2(0, 10).rotate(self.title_bounce * 50).y)
        title_text = self.title_font.render("Makeup Rain", True, Colors.PINK)
        title_shadow = self.title_font.render("Makeup Rain", True, Colors.PURPLE_DARK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80 + bounce_offset))
        screen.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
        screen.blit(title_text, title_rect)
        
        # High score debajo del título
        high_score_text = self.subtitle_font.render(
            f"Récord: {self.game_manager.score_system.high_score}",
            True,
            Colors.GOLD
        )
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(high_score_text, high_score_rect)
        
        # === LAYOUT DE 2 COLUMNAS ===
        
        # COLUMNA IZQUIERDA: Reglas e Instrucciones
        left_x = 80
        rules_y = 200
        
        # Panel de reglas
        rules_panel = Panel(left_x - 20, rules_y - 10, 280, 340, alpha=150)
        rules_panel.draw(screen)
        
        # Título de reglas
        rules_title = self.subtitle_font.render("COMO JUGAR", True, Colors.CYAN)
        screen.blit(rules_title, (left_x, rules_y))
        
        # Reglas del juego
        rules = [
            "",
            "Objetivo:",
            "Recolecta items por ronda",
            "Evita los obstaculos",
            "",
            "Controles:",
            "Jugador 1: Flechas",
            "Jugador 2: A y D",
            "",
            "Teclas:",
            "P - Pausar",
            "F11 - Pantalla completa",
            "ESC - Salir"
        ]
        
        rule_y = rules_y + 10
        for rule in rules:
            if rule:  # Solo renderizar si no está vacío
                color = Colors.PINK_LIGHT if rule.endswith(":") else Colors.TEXT_SECONDARY
                size = 22 if rule.endswith(":") else 20
                rule_font = pygame.font.Font(None, size)
                rule_text = rule_font.render(rule, True, color)
                screen.blit(rule_text, (left_x + 10, rule_y))
            rule_y += 24
        
        # COLUMNA DERECHA: Botones de juego
        right_x = 480
        
        # Panel de opciones
        options_panel = Panel(right_x - 20, rules_y - 10, 280, 340, alpha=150)
        options_panel.draw(screen)
        
        # Título de opciones
        options_title = self.subtitle_font.render("MODOS DE JUEGO", True, Colors.PINK)
        screen.blit(options_title, (right_x, rules_y))
        
        # Botones centrados en columna derecha
        self.single_player_button.draw(screen)
        self.coop_button.draw(screen)
        self.quit_button.draw(screen)
        
        # Efecto de transición
        self.draw_transition(screen)
