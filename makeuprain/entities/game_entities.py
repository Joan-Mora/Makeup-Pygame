"""
Entidades base del juego.
Define clases para el jugador, enemigos y coleccionables.
"""
import pygame
import random
from typing import Tuple, Optional
from ..config import (
    PlayerConfig, EnemyConfig, CollectibleConfig,
    SCREEN_WIDTH, SCREEN_HEIGHT, Colors
)


class Entity(pygame.sprite.Sprite):
    """Clase base para todas las entidades del juego."""
    
    def __init__(self, x: float, y: float, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0.0
        # Crear máscara para colisiones precisas
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        """Actualiza la entidad cada frame."""
        pass
    
    def draw(self, surface: pygame.Surface):
        """Dibuja la entidad en la superficie."""
        surface.blit(self.image, self.rect)


class Player(Entity):
    """Jugador controlable."""
    
    def __init__(
        self, 
        x: float, 
        y: float, 
        image: pygame.Surface, 
        player_id: int = 1,
        controls_left: list = None,
        controls_right: list = None,
        tint_color: Tuple[int, int, int] = None
    ):
        super().__init__(x, y, image)
        self.player_id = player_id
        self.speed = PlayerConfig.SPEED
        self.lives = PlayerConfig.START_LIVES
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.alpha = 255
        self.score = 0  # Score individual para coop
        self.dying = False  # Animación de muerte activa
        self.death_timer = 0  # Frames de animación de muerte
        
        # Controles personalizables
        self.controls_left = controls_left or PlayerConfig.PLAYER1_LEFT
        self.controls_right = controls_right or PlayerConfig.PLAYER1_RIGHT
        
        # Color distintivo
        self.tint_color = tint_color
        if self.tint_color:
            self.image = self._apply_tint(image.copy(), self.tint_color)
            # Actualizar máscara tras aplicar tinte
            self.mask = pygame.mask.from_surface(self.image)
        
    def _apply_tint(self, surface: pygame.Surface, color: Tuple[int, int, int]) -> pygame.Surface:
        """Aplica un tinte de color a la imagen del jugador."""
        tinted = surface.copy()
        # Crear overlay con el color deseado
        overlay = pygame.Surface(surface.get_size()).convert_alpha()
        overlay.fill(color)
        # Usar BLEND_RGBA_MULT para aplicar el color solo donde hay píxeles
        tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return tinted
        
    def update(self):
        """Actualiza el jugador basado en input."""
        # Si está muriendo, solo actualizar timer
        if self.dying:
            self.death_timer += 1
            return
        
        keys = pygame.key.get_pressed()
        
        # Movimiento con controles personalizados
        if any(keys[k] for k in self.controls_left):
            self.rect.x -= self.speed
        if any(keys[k] for k in self.controls_right):
            self.rect.x += self.speed
        
        # Mantener dentro de la pantalla
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        
        # Actualizar invulnerabilidad
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.alpha = 255
            else:
                # Efecto de parpadeo
                self.alpha = 128 if (self.invulnerable_timer // 5) % 2 == 0 else 255
    
    def take_damage(self):
        """El jugador recibe daño."""
        if not self.invulnerable and self.lives > 0:
            self.lives -= 1
            if self.lives <= 0:
                self.start_death_animation()
            else:
                self.invulnerable = True
                self.invulnerable_timer = PlayerConfig.INVULNERABILITY_TIME // (1000 / 60)
            return True
        return False
    
    def start_death_animation(self):
        """Inicia la animación de muerte."""
        self.dying = True
        self.death_timer = 0
    
    def is_dead(self) -> bool:
        """Retorna True si el jugador está muerto y la animación terminó."""
        return self.dying and self.death_timer > 30  # ~0.5s de animación
    
    def draw(self, surface: pygame.Surface):
        """Dibuja el jugador con efecto de transparencia si está invulnerable."""
        # No dibujar si ya murió completamente
        if self.is_dead():
            return
        
        # Fade out durante la muerte
        if self.dying:
            fade_alpha = int(255 * (1 - self.death_timer / 30))
            temp_image = self.image.copy()
            temp_image.set_alpha(fade_alpha)
            surface.blit(temp_image, self.rect)
        elif self.alpha < 255:
            temp_image = self.image.copy()
            temp_image.set_alpha(self.alpha)
            surface.blit(temp_image, self.rect)
        else:
            surface.blit(self.image, self.rect)


class Enemy(Entity):
    """Enemigo que cae desde arriba."""
    
    def __init__(self, x: float, y: float, image: pygame.Surface, speed: float):
        super().__init__(x, y, image)
        self.speed = speed
        self.rotation = random.uniform(-2, 2)  # Rotación sutil
        self.angle = 0
        
    def update(self):
        """Mueve el enemigo hacia abajo."""
        self.rect.y += self.speed
        self.angle += self.rotation
        
        # Eliminar si sale de la pantalla
        if self.rect.y > SCREEN_HEIGHT + 100:
            self.kill()
    
    def draw(self, surface: pygame.Surface):
        """Dibuja el enemigo con rotación."""
        if abs(self.angle) > 0.1:
            rotated = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated.get_rect(center=self.rect.center)
            surface.blit(rotated, rotated_rect)
        else:
            surface.blit(self.image, self.rect)


class Collectible(Entity):
    """Item coleccionable (makeup)."""
    
    def __init__(self, x: float, y: float, image: pygame.Surface, speed: float):
        super().__init__(x, y, image)
        self.speed = speed
        self.bob_offset = random.uniform(0, 6.28)  # Offset para animación
        self.bob_counter = 0
        
    def update(self):
        """Mueve el coleccionable con animación de flotación."""
        self.rect.y += self.speed
        
        # Animación de "flotación" sutil
        self.bob_counter += 0.1
        bob_x = pygame.math.Vector2(2 * pygame.math.Vector2(1, 0).rotate(
            (self.bob_counter + self.bob_offset) * 10
        ).x, 0)
        self.rect.x += bob_x.x * 0.3
        
        # Eliminar si sale de la pantalla
        if self.rect.y > SCREEN_HEIGHT + 100:
            self.kill()
    
    def draw(self, surface: pygame.Surface):
        """Dibuja el coleccionable con brillo sutil."""
        # Efecto de pulso muy sutil
        pulse = abs(pygame.math.Vector2(1, 0).rotate(self.bob_counter * 50).y)
        alpha = int(255 - pulse * 30)
        
        temp_image = self.image.copy()
        temp_image.set_alpha(alpha)
        surface.blit(temp_image, self.rect)


class Particle:
    """Partícula para efectos visuales."""
    
    def __init__(
        self,
        x: float,
        y: float,
        color: Tuple[int, int, int],
        velocity: Tuple[float, float],
        lifetime: int = 60
    ):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 5)
        
    def update(self):
        """Actualiza la partícula."""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravedad
        self.lifetime -= 1
        
    def draw(self, surface: pygame.Surface):
        """Dibuja la partícula con fade out."""
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            color = (*self.color, alpha)
            size = int(self.size * (self.lifetime / self.max_lifetime))
            if size > 0:
                # Crear superficie temporal con transparencia
                particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surf, color, (size, size), size)
                surface.blit(particle_surf, (int(self.x) - size, int(self.y) - size))
    
    def is_dead(self) -> bool:
        """Verifica si la partícula debe ser eliminada."""
        return self.lifetime <= 0


def create_particle_burst(
    x: float,
    y: float,
    color: Tuple[int, int, int],
    count: int = 15
) -> list:
    """Crea una explosión de partículas."""
    particles = []
    for _ in range(count):
        angle = random.uniform(0, 360)
        speed = random.uniform(2, 6)
        vx = speed * pygame.math.Vector2(1, 0).rotate(angle).x
        vy = speed * pygame.math.Vector2(1, 0).rotate(angle).y - random.uniform(1, 3)
        particles.append(Particle(x, y, color, (vx, vy), random.randint(30, 60)))
    return particles
