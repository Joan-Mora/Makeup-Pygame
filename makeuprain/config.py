"""
Configuración centralizada del juego Makeup Rain.
Define constantes, colores, rutas y parámetros globales.
"""
import os
import pygame

# ===== RUTAS =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')

# ===== PANTALLA =====
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_TITLE = "Makeup Rain ✨"
FULLSCREEN = False  # Cambiar a True para pantalla completa
RESIZABLE = True    # Permite redimensionar la ventana

# ===== COLORES (Paleta moderna y vibrante) =====
class Colors:
    # Paleta principal
    DARK_BG = (18, 18, 28)           # Fondo oscuro elegante
    PURPLE_DARK = (88, 57, 131)      # Morado oscuro
    PURPLE = (138, 98, 186)          # Morado medio
    PURPLE_LIGHT = (188, 158, 226)   # Morado claro
    PINK = (255, 105, 180)           # Rosa vibrante
    PINK_LIGHT = (255, 182, 217)     # Rosa pastel
    CYAN = (0, 255, 255)             # Cyan neón
    GOLD = (255, 215, 0)             # Dorado
    WHITE = (255, 255, 255)          # Blanco puro
    BLACK = (0, 0, 0)                # Negro
    GRAY = (128, 128, 128)           # Gris medio
    GRAY_DARK = (64, 64, 72)         # Gris oscuro
    GRAY_LIGHT = (180, 180, 190)     # Gris claro
    
    # Colores de UI
    TEXT_PRIMARY = (255, 255, 255)
    TEXT_SECONDARY = (200, 200, 210)
    TEXT_ACCENT = (255, 105, 180)
    
    # Estados
    SUCCESS = (50, 255, 130)         # Verde éxito
    DANGER = (255, 70, 70)           # Rojo peligro
    WARNING = (255, 200, 50)         # Amarillo advertencia
    
    # Overlay y efectos
    OVERLAY_DARK = (0, 0, 0, 180)    # Overlay semi-transparente
    PARTICLE_COLORS = [
        (255, 105, 180),  # Rosa
        (138, 98, 186),   # Morado
        (0, 255, 255),    # Cyan
        (255, 215, 0),    # Dorado
    ]

# ===== JUGADOR =====
class PlayerConfig:
    SPEED = 5.5
    START_LIVES = 3
    INVULNERABILITY_TIME = 1000  # ms después de recibir daño
    SIZE_SCALE = 1.0  # Escala de la imagen del jugador
    
    # Controles para jugadores
    PLAYER1_LEFT = [pygame.K_LEFT]
    PLAYER1_RIGHT = [pygame.K_RIGHT]
    PLAYER2_LEFT = [pygame.K_a]
    PLAYER2_RIGHT = [pygame.K_d]
    
    # Colores distintivos para cada jugador
    PLAYER1_TINT = (100, 200, 255)  # Azul claro
    PLAYER2_TINT = (255, 100, 200)  # Rosa

# ===== ENEMIGOS =====
class EnemyConfig:
    SPEED_MIN = 1.5
    SPEED_MAX = 2.8
    INITIAL_COUNT = 8
    SPAWN_MULTIPLIER = 2  # Cuántos enemigos por nivel

# ===== COLECCIONABLES (Makeup) =====
class CollectibleConfig:
    SPEED_MIN = 1.2
    SPEED_MAX = 2.2
    INITIAL_COUNT = 20
    SPAWN_MULTIPLIER = 5  # Cuántos items por nivel
    POINTS_VALUE = 50

# ===== SISTEMA DE PUNTUACIÓN =====
class ScoreConfig:
    COMBO_TIME_WINDOW = 2000  # ms para mantener combo
    COMBO_MULTIPLIERS = {
        3: 1.5,   # 3 items seguidos = 1.5x
        5: 2.0,   # 5 items = 2x
        10: 3.0,  # 10 items = 3x
    }
    HIGH_SCORE_FILE = os.path.join(BASE_DIR, 'highscore.json')

# ===== GAME LOOP =====
class GameConfig:
    DIFFICULTY_INTERVAL = 1500  # frames entre aumentos de dificultad
    MAX_PARTICLES = 100         # Límite de partículas en pantalla

# ===== SISTEMA DE RONDAS =====
class RoundConfig:
    # Duración y objetivos de ronda
    ITEMS_SEQUENCE = [10, 15, 25, 35, 50]  # Objetivos por ronda
    DEFAULT_ITEMS_INCREMENT = 15           # A partir del final de la secuencia
    ROUND_TIME_LIMIT = 60       # Segundos por ronda (0 = sin límite)
    
    # Escalado de dificultad por ronda
    SPEED_MULTIPLIER_PER_ROUND = 0.3  # +30% velocidad por ronda
    MAX_SPEED_MULTIPLIER = 3.0        # Máximo 3x velocidad
    ENEMY_SPAWN_INCREASE = 3          # +3 enemigos por ronda
    
    # Spawn continuo (frames a 60 FPS)
    ENEMY_SPAWN_BASE_FRAMES = 45      # ~0.75s entre enemigos base
    ENEMY_MAX_ON_SCREEN_BASE = 8
    COLLECTIBLE_SPAWN_BASE_FRAMES = 30  # ~0.5s entre items base
    COLLECTIBLE_MAX_ON_SCREEN_BASE = 10
    
    # Recompensas
    ROUND_CLEAR_BONUS = 500     # Bonus por completar ronda
    TIME_BONUS_PER_SECOND = 10  # Bonus por tiempo restante
    
    # Visual
    ROUND_TRANSITION_TIME = 3.0  # Segundos de pantalla de transición
    
# ===== MODOS DE JUEGO =====
class GameMode:
    SINGLE_PLAYER = 1
    COOPERATIVE = 2

# ===== AUDIO =====
class AudioConfig:
    MUSIC_VOLUME = 0.6
    SFX_VOLUME = 0.7
    
# ===== ASSETS PATHS =====
ASSET_PATHS = {
    'player': 'player_ship.png',
    'enemy': 'cactus.png',
    'collectible': 'makeup.png',
    'life': 'heart.png',
    'music': 'music.mp3',
}
