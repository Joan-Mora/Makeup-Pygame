"""
Escena principal del juego.
"""
import pygame
import random
from typing import List
from .base_scene import Scene
from ..config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, Colors,
    EnemyConfig, CollectibleConfig, GameConfig, ASSET_PATHS,
    PlayerConfig, RoundConfig
)
from ..entities import Player, Enemy, Collectible, Particle, create_particle_burst
from ..ui import Panel, ProgressBar
from ..utils import asset_manager, draw_text_with_shadow, create_gradient_surface
from ..core.round_manager import RoundManager


class GameScene(Scene):
    """Escena del juego principal."""
    
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # Cargar imágenes
        self.player_img = asset_manager.load_image(ASSET_PATHS['player'])
        self.enemy_img = asset_manager.load_image(ASSET_PATHS['enemy'])
        self.collectible_img = asset_manager.load_image(ASSET_PATHS['collectible'])
        self.life_img = asset_manager.load_image(ASSET_PATHS['life'])
        
        # Fondo con gradiente animado
        self.background = create_gradient_surface(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            Colors.DARK_BG,
            (28, 28, 48),
            vertical=True
        )
        
        # Entidades
        self.players: List[Player] = []  # Lista de jugadores (1 o 2)
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()
        self.collectibles: pygame.sprite.Group = pygame.sprite.Group()
        self.particles: List[Particle] = []
        
        # Sistema de rondas
        self.round_manager = RoundManager()
        self.showing_round_transition = False
        self.transition_timer = 0
        # Timers de spawn continuo
        self.last_enemy_spawn_frame = 0
        self.last_collectible_spawn_frame = 0
        
        # Estado del juego
        self.paused = False
        self.frame_count = 0
        self.game_mode = 1  # Se actualizará desde game_manager
        
        # Fuentes
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # UI
        self.combo_bar = ProgressBar(
            SCREEN_WIDTH - 220,
            70,
            200,
            15,
            max_value=100.0,  # Máximo arbitrario para el combo
            color=Colors.CYAN,
            bg_color=Colors.GRAY_DARK
        )
        
        self.pause_panel = Panel(
            SCREEN_WIDTH // 2 - 200,
            SCREEN_HEIGHT // 2 - 100,
            400,
            200,
            alpha=230
        )
        
    def on_enter(self):
        """Inicializa el juego al entrar a la escena."""
        super().on_enter()
        self.game_mode = self.game_manager.game_mode
        self.reset_game()
        
        # Iniciar música
        asset_manager.load_music(ASSET_PATHS['music'])
        asset_manager.play_music()
    
    def reset_game(self):
        """Reinicia el estado del juego."""
        # Reiniciar jugadores según modo
        self.players.clear()
        
        if self.game_mode == 1:  # Single player
            player1 = Player(
                SCREEN_WIDTH // 2 - self.player_img.get_width() // 2,
                SCREEN_HEIGHT - self.player_img.get_height() - 20,
                self.player_img,
                player_id=1,
                controls_left=PlayerConfig.PLAYER1_LEFT,
                controls_right=PlayerConfig.PLAYER1_RIGHT
            )
            self.players.append(player1)
        else:  # Cooperative (2 jugadores)
            # Jugador 1 (izquierda, azul, flechas)
            player1 = Player(
                SCREEN_WIDTH // 3 - self.player_img.get_width() // 2,
                SCREEN_HEIGHT - self.player_img.get_height() - 20,
                self.player_img,
                player_id=1,
                controls_left=PlayerConfig.PLAYER1_LEFT,
                controls_right=PlayerConfig.PLAYER1_RIGHT,
                tint_color=PlayerConfig.PLAYER1_TINT
            )
            # Jugador 2 (derecha, rosa, A/D)
            player2 = Player(
                2 * SCREEN_WIDTH // 3 - self.player_img.get_width() // 2,
                SCREEN_HEIGHT - self.player_img.get_height() - 20,
                self.player_img,
                player_id=2,
                controls_left=PlayerConfig.PLAYER2_LEFT,
                controls_right=PlayerConfig.PLAYER2_RIGHT,
                tint_color=PlayerConfig.PLAYER2_TINT
            )
            self.players.append(player1)
            self.players.append(player2)
        
        # Limpiar entidades
        self.enemies.empty()
        self.collectibles.empty()
        self.particles.clear()
        
        # Reiniciar sistema de rondas
        self.round_manager.reset()
        self.showing_round_transition = False
        self.transition_timer = 0
        self.last_enemy_spawn_frame = 0
        self.last_collectible_spawn_frame = 0
        
        # Generar enemigos y coleccionables de la ronda inicial
        self.spawn_round_entities()
        
        # Reiniciar contadores
        self.frame_count = 0
        self.paused = False
        
        # Reiniciar sistema de puntuación
        self.game_manager.score_system.reset()
    
    def spawn_round_entities(self):
        """Genera enemigos y coleccionables para la ronda actual."""
        speed_mult = self.round_manager.get_speed_multiplier()
        enemy_count = self.round_manager.get_enemy_count()
        collectible_count = self.round_manager.get_collectible_count()
        
        self.spawn_enemies(enemy_count, speed_mult)
        self.spawn_collectibles(collectible_count, speed_mult)
    
    def spawn_enemies(self, count: int, speed_multiplier: float = 1.0):
        """Genera enemigos con multiplicador de velocidad."""
        for _ in range(count):
            x = random.randint(0, SCREEN_WIDTH - self.enemy_img.get_width())
            y = random.randint(-500, -self.enemy_img.get_height())
            speed = random.uniform(EnemyConfig.SPEED_MIN, EnemyConfig.SPEED_MAX) * speed_multiplier
            enemy = Enemy(x, y, self.enemy_img, speed)
            self.enemies.add(enemy)
    
    def spawn_collectibles(self, count: int, speed_multiplier: float = 1.0):
        """Genera coleccionables con multiplicador de velocidad."""
        for _ in range(count):
            x = random.randint(0, SCREEN_WIDTH - self.collectible_img.get_width())
            y = random.randint(-800, -self.collectible_img.get_height())
            speed = random.uniform(CollectibleConfig.SPEED_MIN, CollectibleConfig.SPEED_MAX) * speed_multiplier
            collectible = Collectible(x, y, self.collectible_img, speed)
            self.collectibles.add(collectible)
    
    def handle_events(self, events: list):
        """Maneja eventos del juego."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    if self.paused:
                        asset_manager.stop_music()
                    else:
                        asset_manager.play_music()
                elif event.key == pygame.K_ESCAPE:
                    self.start_transition('menu')
    
    def update(self):
        """Actualiza la lógica del juego."""
        if self.paused:
            return
        
        # Manejar transición de ronda
        if self.showing_round_transition:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                self.showing_round_transition = False
                self.spawn_round_entities()
            return
        
        # Actualizar contador de frames
        self.frame_count += 1
        
        # Actualizar jugadores
        for player in self.players:
            player.update()
        
        # Actualizar enemigos
        self.enemies.update()
        
        # Actualizar coleccionables
        self.collectibles.update()

        # Spawn continuo dependiente de ronda
        self._continuous_spawn()
        
        # Detectar colisiones para cada jugador
        for player in self.players:
            if player.lives <= 0 or player.dying:
                continue  # Jugador ya muerto o muriendo
            
            # Colisiones con coleccionables (más precisas con máscaras)
            collected = pygame.sprite.spritecollide(player, self.collectibles, True, pygame.sprite.collide_mask)
            for item in collected:
                # Añadir puntos al jugador individual
                points = self.game_manager.score_system.add_points(
                    item.rect.centerx,
                    item.rect.centery
                )
                player.score += points
                
                # Notificar al round manager
                round_complete = self.round_manager.on_item_collected()
                
                # Crear partículas con el color del jugador
                particle_color = player.tint_color if player.tint_color else Colors.PINK
                particles = create_particle_burst(
                    item.rect.centerx,
                    item.rect.centery,
                    particle_color,
                    count=20
                )
                self.particles.extend(particles[:GameConfig.MAX_PARTICLES - len(self.particles)])
                
                # Verificar si completó la ronda
                if round_complete:
                    self._start_round_transition()
            
            # Colisiones con enemigos (más precisas con máscaras)
            if not player.invulnerable:
                hit_enemies = pygame.sprite.spritecollide(player, self.enemies, True, pygame.sprite.collide_mask)
                if hit_enemies:
                    died = player.take_damage()
                    self.game_manager.score_system.break_combo()
                    
                    # Crear partículas (explosión grande si murió, pequeña si solo daño)
                    if player.dying:  # Murió
                        particle_color = player.tint_color if player.tint_color else Colors.WHITE
                        particles = create_particle_burst(
                            player.rect.centerx,
                            player.rect.centery,
                            particle_color,
                            count=50
                        )
                    else:  # Solo daño
                        particles = create_particle_burst(
                            player.rect.centerx,
                            player.rect.centery,
                            Colors.DANGER,
                            count=25
                        )
                    self.particles.extend(particles[:GameConfig.MAX_PARTICLES - len(self.particles)])
        
        # Verificar si todos los jugadores murieron (incluyendo animación)
        all_dead = all(player.is_dead() for player in self.players)
        if all_dead:
            asset_manager.stop_music()
            self.start_transition('gameover')
        
        # Actualizar partículas
        for particle in self.particles[:]:
            particle.update()
            if particle.is_dead():
                self.particles.remove(particle)
        
        # Actualizar sistema de puntuación
        self.game_manager.score_system.update()
        
        # Actualizar barra de combo
        combo, multiplier, time_ratio = self.game_manager.score_system.get_combo_info()
        self.combo_bar.set_value(time_ratio * 100)
        self.combo_bar.update()
        
        # Actualizar transición
        if self.update_transition() and self.next_scene:
            self.game_manager.change_scene(self.next_scene)

    def _continuous_spawn(self):
        """Genera enemigos y coleccionables de forma continua durante la ronda."""
        speed_mult = self.round_manager.get_speed_multiplier()
        # Enemigos
        enemy_interval = self.round_manager.get_enemy_spawn_frames()
        enemy_cap = self.round_manager.get_enemy_cap()
        if (self.frame_count - self.last_enemy_spawn_frame) >= enemy_interval and len(self.enemies) < enemy_cap:
            self.spawn_enemies(1, speed_mult)
            self.last_enemy_spawn_frame = self.frame_count
        
        # Coleccionables: solo si aún faltan para el objetivo
        goal = self.round_manager.get_items_goal()
        if self.round_manager.items_collected_this_round < goal:
            col_interval = self.round_manager.get_collectible_spawn_frames()
            col_cap = self.round_manager.get_collectible_cap()
            if (self.frame_count - self.last_collectible_spawn_frame) >= col_interval and len(self.collectibles) < col_cap:
                self.spawn_collectibles(1, speed_mult)
                self.last_collectible_spawn_frame = self.frame_count
    
    def _start_round_transition(self):
        """Inicia la transición entre rondas."""
        self.showing_round_transition = True
        self.transition_timer = 120  # 2 segundos a 60 FPS
        
        # Limpiar entidades
        self.enemies.empty()
        self.collectibles.empty()
        
        # Avanzar de ronda
        self.round_manager.advance_round()
        
        # Aplicar bonus a jugadores vivos
        bonus = self.round_manager.get_round_bonus()
        for player in self.players:
            if player.lives > 0:
                player.score += bonus
    
    def draw(self, screen: pygame.Surface):
        """Dibuja el juego."""
        # Fondo
        screen.blit(self.background, (0, 0))
        
        # Dibujar estrellas de fondo (efecto simple)
        if self.frame_count % 3 == 0:
            for _ in range(2):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                size = random.randint(1, 2)
                pygame.draw.circle(screen, Colors.WHITE, (x, y), size)
        
        # Dibujar partículas
        for particle in self.particles:
            particle.draw(screen)
        
        # Dibujar coleccionables
        for collectible in self.collectibles:
            collectible.draw(screen)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Dibujar jugadores
        for player in self.players:
            player.draw(screen)
        
        # Dibujar textos flotantes del score system
        self.game_manager.score_system.draw(screen)
        
        # === HUD ===
        # Panel superior semi-transparente
        hud_height = 120 if self.game_mode == 2 else 80
        hud_panel = Panel(10, 10, SCREEN_WIDTH - 20, hud_height, alpha=150)
        hud_panel.draw(screen)
        
        # Info de ronda
        round_text = self.font_medium.render(
            f"Ronda {self.round_manager.current_round}",
            True,
            Colors.CYAN
        )
        screen.blit(round_text, (20, 15))
        
        # Progreso de ronda
        progress = self.round_manager.get_progress()
        progress_bar = ProgressBar(20, 45, 200, 15, max_value=100.0, color=Colors.PINK, bg_color=Colors.GRAY)
        progress_bar.set_value(progress * 100)
        progress_bar.draw(screen)
        
        progress_text = self.font_small.render(
            f"{self.round_manager.items_collected_this_round}/{self.round_manager.get_items_goal()}",
            True,
            Colors.WHITE
        )
        screen.blit(progress_text, (230, 43))
        
        # Puntuaciones según modo de juego
        if self.game_mode == 1:
            # Un solo jugador
            player = self.players[0]
            score_text = self.font_large.render(
                f"Puntos: {player.score}",
                True,
                Colors.GOLD
            )
            screen.blit(score_text, (300, 25))
            
            # Vidas
            for i in range(player.lives):
                screen.blit(self.life_img, (300 + i * (self.life_img.get_width() + 5), 60))
        else:
            # Dos jugadores - mostrar ambos puntajes
            player1 = self.players[0]
            player2 = self.players[1]
            
            # Jugador 1 (azul)
            p1_text = self.font_medium.render(
                f"J1: {player1.score}",
                True,
                PlayerConfig.PLAYER1_TINT
            )
            screen.blit(p1_text, (20, 75))
            
            # Vidas jugador 1
            for i in range(player1.lives):
                screen.blit(self.life_img, (20 + i * (self.life_img.get_width() + 5), 100))
            
            # Jugador 2 (rosa)
            p2_text = self.font_medium.render(
                f"J2: {player2.score}",
                True,
                PlayerConfig.PLAYER2_TINT
            )
            screen.blit(p2_text, (200, 75))
            
            # Vidas jugador 2
            for i in range(player2.lives):
                screen.blit(self.life_img, (200 + i * (self.life_img.get_width() + 5), 100))
        
        # Combo info (lado derecho) - reordenado para mejor visibilidad
        combo, multiplier, time_ratio = self.game_manager.score_system.get_combo_info()
        if combo > 0:
            # Multiplicador primero (más importante)
            if multiplier > 1.0:
                mult_text = self.font_medium.render(
                    f"Multiplicador: {multiplier:.1f}x",
                    True,
                    Colors.GOLD
                )
                screen.blit(mult_text, (SCREEN_WIDTH - 250, 15))
            
            # Combo debajo
            combo_text = self.font_small.render(
                f"Combo x{combo}",
                True,
                Colors.CYAN if multiplier == 1.0 else Colors.PINK
            )
            screen.blit(combo_text, (SCREEN_WIDTH - 250, 40))
            
            # Barra de combo abajo del texto
            self.combo_bar.draw(screen)
        
        # Pantalla de transición de ronda
        if self.showing_round_transition:
            self._draw_round_transition(screen)
        
        # Pantalla de pausa
        if self.paused:
            # Overlay oscuro
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(150)
            screen.blit(overlay, (0, 0))
            
            # Panel de pausa
            self.pause_panel.draw(screen)
            
            # Texto
            pause_text = self.font_large.render("PAUSA", True, Colors.WHITE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(pause_text, pause_rect)
            
            resume_text = self.font_small.render(
                "Presiona P para continuar",
                True,
                Colors.TEXT_SECONDARY
            )
            resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(resume_text, resume_rect)
            
            menu_text = self.font_small.render(
                "ESC para volver al menú",
                True,
                Colors.TEXT_SECONDARY
            )
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(menu_text, menu_rect)
        
        # Efecto de transición
        self.draw_transition(screen)
    
    def _draw_round_transition(self, screen: pygame.Surface):
        """Dibuja la pantalla de transición entre rondas."""
        # Overlay oscuro
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # Panel central
        panel_width = 500
        panel_height = 300
        panel = Panel(
            SCREEN_WIDTH // 2 - panel_width // 2,
            SCREEN_HEIGHT // 2 - panel_height // 2,
            panel_width,
            panel_height,
            alpha=220
        )
        panel.draw(screen)
        
        # Texto de ronda completada
        complete_text = self.font_large.render(
            f"¡Ronda {self.round_manager.current_round - 1} Completada!",
            True,
            Colors.GOLD
        )
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(complete_text, complete_rect)
        
        # Bonus
        bonus = self.round_manager.get_round_bonus()
        bonus_text = self.font_medium.render(
            f"Bonus: +{bonus} puntos",
            True,
            Colors.PINK
        )
        bonus_rect = bonus_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(bonus_text, bonus_rect)
        
        # Siguiente ronda
        next_text = self.font_medium.render(
            f"Siguiente: Ronda {self.round_manager.current_round}",
            True,
            Colors.CYAN
        )
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(next_text, next_rect)
        
        # Advertencia de dificultad
        speed_mult = self.round_manager.get_speed_multiplier()
        diff_text = self.font_small.render(
            f"Velocidad: {speed_mult:.1f}x",
            True,
            Colors.DANGER if speed_mult > 2.0 else Colors.WARNING if speed_mult > 1.5 else Colors.WHITE
        )
        diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(diff_text, diff_rect)
