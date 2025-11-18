"""
Sistema de puntuación con combos y multiplicadores.
"""
import pygame
from typing import List
from ..config import ScoreConfig, CollectibleConfig, Colors
from ..utils import save_high_score, load_high_score
from .components import FloatingText


class ScoreSystem:
    """Gestiona el sistema de puntuación con combos."""
    
    def __init__(self):
        self.score = 0
        self.combo = 0
        self.combo_timer = 0
        self.multiplier = 1.0
        self.high_score = load_high_score(ScoreConfig.HIGH_SCORE_FILE)
        self.floating_texts: List[FloatingText] = []
        
    def add_points(self, x: float, y: float) -> int:
        """
        Añade puntos por recoger un item.
        
        Args:
            x, y: Posición donde crear el texto flotante
            
        Returns:
            Puntos ganados
        """
        self.combo += 1
        self.combo_timer = ScoreConfig.COMBO_TIME_WINDOW // (1000 / 60)  # Convertir ms a frames
        
        # Calcular multiplicador basado en combo
        self.multiplier = 1.0
        for combo_threshold, mult in sorted(ScoreConfig.COMBO_MULTIPLIERS.items()):
            if self.combo >= combo_threshold:
                self.multiplier = mult
        
        # Calcular puntos
        base_points = CollectibleConfig.POINTS_VALUE
        points_earned = int(base_points * self.multiplier)
        self.score += points_earned
        
        # Crear texto flotante
        text = f"+{points_earned}"
        if self.multiplier > 1.0:
            text += f" x{self.multiplier:.1f}!"
        
        color = Colors.GOLD if self.multiplier == 1.0 else Colors.PINK
        self.floating_texts.append(FloatingText(text, x, y, color, size=28))
        
        # Mostrar combo si es alto
        if self.combo >= 5 and self.combo % 5 == 0:
            combo_text = FloatingText(
                f"¡COMBO x{self.combo}!",
                x,
                y - 40,
                Colors.CYAN,
                size=36,
                lifetime=90
            )
            self.floating_texts.append(combo_text)
        
        # Actualizar high score
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score, ScoreConfig.HIGH_SCORE_FILE)
        
        return points_earned
    
    def break_combo(self):
        """Rompe el combo actual."""
        if self.combo > 0:
            self.combo = 0
            self.multiplier = 1.0
    
    def update(self):
        """Actualiza el sistema de puntuación."""
        # Actualizar timer de combo
        if self.combo > 0:
            self.combo_timer -= 1
            if self.combo_timer <= 0:
                self.break_combo()
        
        # Actualizar textos flotantes
        for text in self.floating_texts[:]:
            text.update()
            if text.is_dead():
                self.floating_texts.remove(text)
    
    def draw(self, surface: pygame.Surface):
        """Dibuja los textos flotantes."""
        for text in self.floating_texts:
            text.draw(surface)
    
    def reset(self):
        """Reinicia el sistema de puntuación."""
        self.score = 0
        self.combo = 0
        self.combo_timer = 0
        self.multiplier = 1.0
        self.floating_texts.clear()
    
    def get_combo_info(self) -> tuple:
        """Retorna (combo, multiplier, time_left_ratio)."""
        time_ratio = self.combo_timer / (ScoreConfig.COMBO_TIME_WINDOW // (1000 / 60))
        return (self.combo, self.multiplier, max(0, time_ratio))
