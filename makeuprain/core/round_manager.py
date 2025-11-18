"""
Sistema de gestión de rondas con dificultad progresiva.
"""
import time
from ..config import RoundConfig, EnemyConfig, CollectibleConfig


class RoundManager:
    """Gestiona las rondas y la dificultad progresiva del juego."""
    
    def __init__(self):
        self.current_round = 1
        self.items_collected_this_round = 0
        self.round_start_time = 0
        self.round_complete = False
        self.game_complete = False
        
    def start_round(self):
        """Inicia una nueva ronda."""
        self.items_collected_this_round = 0
        self.round_start_time = time.time()
        self.round_complete = False
        
    def on_item_collected(self) -> bool:
        """Llamado cuando se recolecta un item. Devuelve True si se completó la ronda."""
        self.items_collected_this_round += 1
        
        # Verificar si se completó la ronda
        if self.items_collected_this_round >= self.get_items_goal():
            self.round_complete = True
        return self.round_complete
    
    def advance_round(self):
        """Avanza a la siguiente ronda."""
        if self.round_complete:
            self.current_round += 1
            self.start_round()
            return True
        return False
    
    def get_speed_multiplier(self) -> float:
        """Calcula el multiplicador de velocidad basado en la ronda actual."""
        multiplier = 1.0 + (self.current_round - 1) * RoundConfig.SPEED_MULTIPLIER_PER_ROUND
        return min(multiplier, RoundConfig.MAX_SPEED_MULTIPLIER)

    def get_items_goal(self) -> int:
        """Objetivo de items para la ronda actual, usando secuencia configurable."""
        idx = self.current_round - 1
        if idx < len(RoundConfig.ITEMS_SEQUENCE):
            return RoundConfig.ITEMS_SEQUENCE[idx]
        # A partir del final de la secuencia, incrementar de forma lineal
        last = RoundConfig.ITEMS_SEQUENCE[-1]
        extra = (idx - (len(RoundConfig.ITEMS_SEQUENCE) - 1)) * RoundConfig.DEFAULT_ITEMS_INCREMENT
        return last + extra
    
    def get_enemy_count(self) -> int:
        """Calcula cuántos enemigos spawn en esta ronda."""
        base_count = EnemyConfig.INITIAL_COUNT
        return base_count + (self.current_round - 1) * RoundConfig.ENEMY_SPAWN_INCREASE
    
    def get_collectible_count(self) -> int:
        """Calcula cuántos coleccionables spawn en esta ronda."""
        base_count = CollectibleConfig.INITIAL_COUNT
        # Aumentar coleccionables más que enemigos
        return base_count + (self.current_round - 1) * RoundConfig.ENEMY_SPAWN_INCREASE * 2

    def get_enemy_cap(self) -> int:
        return RoundConfig.ENEMY_MAX_ON_SCREEN_BASE + (self.current_round - 1) * RoundConfig.ENEMY_SPAWN_INCREASE

    def get_collectible_cap(self) -> int:
        return RoundConfig.COLLECTIBLE_MAX_ON_SCREEN_BASE + (self.current_round - 1) * (RoundConfig.ENEMY_SPAWN_INCREASE // 2 + 1)

    def get_enemy_spawn_frames(self) -> int:
        mult = self.get_speed_multiplier()
        return max(10, int(RoundConfig.ENEMY_SPAWN_BASE_FRAMES / mult))

    def get_collectible_spawn_frames(self) -> int:
        mult = self.get_speed_multiplier()
        return max(8, int(RoundConfig.COLLECTIBLE_SPAWN_BASE_FRAMES / mult))
    
    def get_round_bonus(self) -> int:
        """Calcula el bonus por completar la ronda."""
        bonus = RoundConfig.ROUND_CLEAR_BONUS
        
        # Bonus por tiempo si hay límite
        if RoundConfig.ROUND_TIME_LIMIT > 0:
            elapsed = time.time() - self.round_start_time
            time_left = max(0, RoundConfig.ROUND_TIME_LIMIT - elapsed)
            bonus += int(time_left * RoundConfig.TIME_BONUS_PER_SECOND)
        
        return bonus
    
    def get_time_left(self) -> float:
        """Retorna el tiempo restante en la ronda (0 si no hay límite)."""
        if RoundConfig.ROUND_TIME_LIMIT <= 0:
            return 0
        
        elapsed = time.time() - self.round_start_time
        return max(0, RoundConfig.ROUND_TIME_LIMIT - elapsed)
    
    def is_time_up(self) -> bool:
        """Verifica si se acabó el tiempo de la ronda."""
        if RoundConfig.ROUND_TIME_LIMIT <= 0:
            return False
        return self.get_time_left() <= 0
    
    def get_progress(self) -> float:
        """Retorna el progreso de la ronda (0.0 a 1.0)."""
        goal = self.get_items_goal()
        return min(1.0, self.items_collected_this_round / goal)
    
    def reset(self):
        """Reinicia el sistema de rondas."""
        self.current_round = 1
        self.items_collected_this_round = 0
        self.round_start_time = 0
        self.round_complete = False
        self.game_complete = False
        self.start_round()
