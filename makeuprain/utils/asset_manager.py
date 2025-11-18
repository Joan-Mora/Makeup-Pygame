"""
Sistema de gestión de recursos (imágenes y sonidos).
Carga y cachea assets para optimizar el rendimiento.
"""
import pygame
import os
from typing import Dict, Optional
from ..config import IMAGES_DIR, SOUNDS_DIR, BASE_DIR


class AssetManager:
    """Gestor centralizado de recursos del juego."""
    
    def __init__(self):
        self._images: Dict[str, pygame.Surface] = {}
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._music_loaded = False
        
    def load_image(self, filename: str, scale: Optional[tuple] = None) -> Optional[pygame.Surface]:
        """
        Carga una imagen desde la carpeta de assets.
        
        Args:
            filename: Nombre del archivo de imagen
            scale: Tupla (width, height) para redimensionar
            
        Returns:
            Surface de pygame o None si falla
        """
        if filename in self._images:
            return self._images[filename]
        
        # Intentar desde assets/images primero
        path = os.path.join(IMAGES_DIR, filename)
        if not os.path.exists(path):
            # Fallback a la raíz del proyecto
            path = os.path.join(BASE_DIR, filename)
        
        try:
            image = pygame.image.load(path).convert_alpha()
            if scale:
                image = pygame.transform.scale(image, scale)
            self._images[filename] = image
            return image
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️ No se pudo cargar imagen {filename}: {e}")
            # Crear placeholder
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((255, 0, 255))  # Magenta para indicar falta
            self._images[filename] = placeholder
            return placeholder
    
    def load_sound(self, filename: str) -> Optional[pygame.mixer.Sound]:
        """
        Carga un efecto de sonido.
        
        Args:
            filename: Nombre del archivo de sonido
            
        Returns:
            Sound de pygame o None si falla
        """
        if filename in self._sounds:
            return self._sounds[filename]
        
        path = os.path.join(SOUNDS_DIR, filename)
        if not os.path.exists(path):
            path = os.path.join(BASE_DIR, filename)
        
        try:
            sound = pygame.mixer.Sound(path)
            self._sounds[filename] = sound
            return sound
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️ No se pudo cargar sonido {filename}: {e}")
            return None
    
    def load_music(self, filename: str) -> bool:
        """
        Carga música de fondo.
        
        Args:
            filename: Nombre del archivo de música
            
        Returns:
            True si se cargó correctamente
        """
        path = os.path.join(SOUNDS_DIR, filename)
        if not os.path.exists(path):
            path = os.path.join(BASE_DIR, filename)
        
        try:
            pygame.mixer.music.load(path)
            self._music_loaded = True
            return True
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️ No se pudo cargar música {filename}: {e}")
            return False
    
    def play_music(self, loops: int = -1, volume: float = 0.6):
        """Reproduce la música de fondo."""
        if self._music_loaded:
            try:
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops)
            except pygame.error:
                pass
    
    def stop_music(self):
        """Detiene la música de fondo."""
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass
    
    def get_image(self, filename: str) -> Optional[pygame.Surface]:
        """Obtiene una imagen cacheada."""
        return self._images.get(filename)
    
    def clear_cache(self):
        """Limpia el caché de recursos."""
        self._images.clear()
        self._sounds.clear()


# Instancia global del asset manager
asset_manager = AssetManager()
