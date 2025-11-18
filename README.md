# 💄 Makeup Rain ✨

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-2.0.0-purple.svg)

**Un juego arcade moderno de recolección con efectos visuales impresionantes**

[Características](#características) • [Instalación](#instalación) • [Cómo Jugar](#cómo-jugar) • [Arquitectura](#arquitectura)

</div>

---

## 📖 Descripción

**Makeup Rain** es un juego arcade donde controlas una nave espacial que debe recolectar elementos de maquillaje mientras evitas cactus peligrosos. El juego cuenta con un sistema de combos, multiplicadores de puntuación, efectos visuales con partículas y una interfaz moderna y pulida.

### ✨ Características

- 🎮 **Gameplay Fluido**: 60 FPS constantes con controles responsivos
- 🎨 **Visuales Modernos**: Gradientes, partículas, animaciones suaves y paleta de colores vibrante
- 🏆 **Sistema de Combos**: Recolecta items consecutivos para multiplicadores de hasta 3x
- 💫 **Efectos de Partículas**: Explosiones de colores al recoger items o recibir daño
- 📊 **Sistema de Puntuación Avanzado**: Textos flotantes, tracking de high score persistente
- 🎵 **Audio Inmersivo**: Música de fondo y efectos de sonido
- 🖥️ **UI Profesional**: Menús animados, transiciones suaves entre escenas
- 🏗️ **Arquitectura Limpia**: Código OOP modular, fácil de mantener y extender

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/Camilandia20/Makeup-Pygame.git
   cd Makeup-Pygame
   ```

2. **Crea un entorno virtual** (recomendado):
   ```bash
   python -m venv .venv
   
   # En Windows:
   .venv\Scripts\activate
   
   # En Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta el juego**:
   ```bash
   python main.py
   ```

---

## 🎮 Cómo Jugar

### Controles

| Tecla | Acción |
|-------|--------|
| `←` / `A` | Mover a la izquierda |
| `→` / `D` | Mover a la derecha |
| `P` | Pausar/Reanudar |
| `ESPACIO` | Iniciar juego (menú) / Reintentar |
| `ESC` | Salir al menú / Cerrar |
| `R` | Reintentar (Game Over) |
| `M` | Volver al menú (Game Over) |

### Objetivo

- 💄 **Recolecta elementos de maquillaje** para ganar puntos (+50 pts base)
- 🌵 **Evita los cactus** o perderás una vida (tienes 3 vidas)
- 🔥 **Mantén el combo** recogiendo items consecutivamente
- 🎯 **Alcanza el multiplicador máximo** (3x) con 10+ items seguidos
- 🏆 **Supera tu récord** personal

### Sistema de Combos

| Combo | Multiplicador |
|-------|---------------|
| 3+ items | 1.5x |
| 5+ items | 2.0x |
| 10+ items | 3.0x |

⏱️ Tienes **2 segundos** entre recolecciones para mantener el combo activo.

---

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
Makeup-Pygame/
├── main.py                      # Entry point del juego
├── requirements.txt             # Dependencias Python
├── README.md                    # Este archivo
├── LICENSE                      # Licencia MIT
├── .gitignore                   # Archivos ignorados por git
├── highscore.json              # High score persistente (auto-generado)
│
├── assets/                     # Recursos del juego
│   ├── images/                # Sprites e imágenes
│   │   ├── player_ship.png   # Nave del jugador
│   │   ├── makeup.png        # Item de maquillaje
│   │   ├── cactus.png        # Obstáculo cactus
│   │   └── heart.png         # Ícono de vida
│   └── sounds/               # Audio del juego
│       └── music.mp3         # Música de fondo
│
├── docs/                      # Documentación adicional
│
└── makeuprain/               # 📦 Paquete principal del juego
    ├── __init__.py          # Exports públicos y función run()
    ├── config.py            # ⚙️ Configuración centralizada
    │
    ├── core/                # 🎮 Sistema central del juego
    │   ├── game_manager.py # Manager principal, ciclo del juego
    │   └── round_manager.py # Sistema de rondas y progresión
    │
    ├── entities/            # 🎭 Entidades del juego
    │   └── game_entities.py # Player, Enemy, Collectible, Particle
    │
    ├── scenes/              # 🎬 Sistema de escenas
    │   ├── base_scene.py   # Clase base abstracta
    │   ├── menu_scene.py   # Menú principal
    │   ├── game_scene.py   # Escena de juego principal
    │   └── gameover_scene.py # Pantalla de game over
    │
    ├── ui/                  # 🖼️ Componentes de interfaz
    │   ├── components.py   # Button, Panel, FloatingText
    │   └── score_system.py # Sistema de puntuación y combos
    │
    └── utils/               # 🛠️ Utilidades y helpers
        ├── asset_manager.py # Carga de imágenes y audio
        └── helpers.py      # Funciones auxiliares (gradientes, etc)
```

### Patrón de Diseño

El proyecto utiliza una **arquitectura modular basada en escenas** con los siguientes patrones:

- **Scene Manager Pattern**: Gestión centralizada de escenas (menú, juego, game over)
- **Entity-Component**: Entidades separadas con comportamientos específicos
- **Singleton**: GameManager como punto central de control
- **Observer**: Sistema de eventos para transiciones entre escenas
- **Factory**: Creación de partículas y entidades dinámicas

### Módulos Principales

#### 🎮 `core/`
- **GameManager**: Controla el ciclo del juego, FPS, cambio de escenas
- **RoundManager**: Gestiona progresión de rondas y dificultad dinámica

#### 🎭 `entities/`
- **Player**: Nave controlada por el jugador, vidas, invulnerabilidad
- **Enemy**: Obstáculos (cactus) que quitan vidas
- **Collectible**: Items de maquillaje que dan puntos
- **Particle**: Sistema de partículas para efectos visuales

#### 🎬 `scenes/`
- **Scene**: Clase base abstracta con `handle_events()`, `update()`, `draw()`
- **MenuScene**: Menú principal con opciones de modo de juego
- **GameScene**: Gameplay principal, spawn, colisiones, HUD
- **GameOverScene**: Pantalla final con estadísticas y opciones

#### 🖼️ `ui/`
- **Button**: Botones interactivos con hover y callbacks
- **Panel**: Paneles con transparencia y bordes
- **FloatingText**: Textos animados que suben y desaparecen
- **ScoreSystem**: Gestión de puntos, combos y multiplicadores

#### 🛠️ `utils/`
- **AssetManager**: Carga centralizada de recursos
- **helpers**: Funciones de gradientes, clamp, etc.

---

## 🎨 Paleta de Colores

- 🟣 **Morados**: `#583783`, `#8A62BA`, `#BC9EE2`
- 🩷 **Rosas**: `#FF69B4`, `#FFB6D9`
- 💠 **Cyan Neón**: `#00FFFF`
- 🥇 **Dorado**: `#FFD700`
- ⚫ **Fondo**: `#12121C`

---

## 🔧 Personalización

El juego es altamente configurable. Edita `makeuprain/config.py` para ajustar:

### Parámetros Configurables

```python
# Pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
FULLSCREEN = False
RESIZABLE = True

# Jugador
PLAYER_SPEED = 5.5              # Velocidad de movimiento
PLAYER_LIVES = 3                # Vidas iniciales
INVULNERABILITY_DURATION = 2.0  # Segundos de invulnerabilidad

# Enemigos
ENEMY_SIZE = (40, 60)
ENEMY_SPEED_MIN = 1.5           # Velocidad mínima
ENEMY_SPEED_MAX = 2.8           # Velocidad máxima
ENEMY_SPAWN_RATE = 1800         # Milisegundos entre spawns

# Coleccionables
COLLECTIBLE_SIZE = (35, 35)
COLLECTIBLE_SPEED_MIN = 1.2
COLLECTIBLE_SPEED_MAX = 2.2
COLLECTIBLE_SPAWN_RATE = 1000

# Sistema de puntuación
SCORE_PER_ITEM = 50             # Puntos base por item
COMBO_DECAY_TIME = 2.0          # Segundos para perder combo
COMBO_THRESHOLDS = {            # Multiplicadores por combo
    3: 1.5,   # 3+ items: 1.5x
    5: 2.0,   # 5+ items: 2.0x
    10: 3.0   # 10+ items: 3.0x
}

# Rondas (modo por rondas)
ITEMS_SEQUENCE = [10, 15, 25, 35, 50]  # Items por ronda
```

### Personalizar Colores

Modifica la clase `Colors` en `config.py`:

```python
class Colors:
    PURPLE = (138, 98, 186)
    PINK = (255, 105, 180)
    CYAN = (0, 255, 255)
    # ... más colores
```

---

## 🎯 Modos de Juego

### 🏃 Modo Individual
- **Objetivo**: Alcanzar la mayor puntuación posible
- **Vidas**: 3 vidas, pierdes una al tocar un cactus
- **Invulnerabilidad**: 2 segundos después de recibir daño
- **High Score**: Se guarda automáticamente en `highscore.json`

### 👥 Modo Cooperativo (2 Jugadores)
- **Jugador 1**: Controles con flechas (← →)
- **Jugador 2**: Controles con A y D
- **Objetivo**: Competir por la mayor puntuación
- **Ganador**: El jugador con más puntos al final
- **Características**:
  - Colisiones independientes por jugador
  - Puntuaciones individuales en pantalla
  - Identificación visual por colores (azul y rosa)

### 🎲 Modo por Rondas
- **Progresión**: 5 rondas con dificultad creciente
- **Objetivos**: 10 → 15 → 25 → 35 → 50 items por ronda
- **Dificultad dinámica**: Velocidad y spawn rate aumentan
- **Victoria**: Completar todas las rondas sin perder todas las vidas

---

## 🐛 Solución de Problemas

### El juego no inicia
```bash
# Verifica la versión de Python
python --version  # Debe ser 3.8+

# Reinstala pygame
pip install --upgrade pygame
```

### Errores de importación
```bash
# Asegúrate de estar en el directorio correcto
cd Makeup-Pygame

# Verifica que makeuprain existe
ls makeuprain  # Linux/Mac
dir makeuprain # Windows
```

### Audio no funciona
- Verifica que exista `assets/sounds/music.mp3`
- Pygame requiere SDL_mixer para audio
- En Linux: `sudo apt-get install libsdl2-mixer-2.0-0`

### Rendimiento bajo (< 60 FPS)
- Reduce `PARTICLE_COUNT` en `config.py`
- Desactiva efectos: `ENABLE_PARTICLES = False`
- Cierra otras aplicaciones pesadas

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres mejorar el juego:

1. **Fork** el repositorio
2. Crea una **rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un **Pull Request**

### Convenciones de Commits

```
feat: Nueva funcionalidad
fix: Corrección de bug
docs: Cambios en documentación
style: Formato, sin cambios de código
refactor: Refactorización de código
test: Añadir tests
perf: Mejora de rendimiento
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 📝 Changelog

### v2.0.0 (2025-11-18) - Refactorización Mayor 🎉

#### ✨ Nuevas Funcionalidades
- **Sistema de Rondas**: Progresión por rondas con dificultad creciente
- **Modo Cooperativo**: 2 jugadores simultáneos con controles independientes
- **Sistema de Combos**: Multiplicadores hasta 3x por recolecciones consecutivas
- **Efectos de Partículas**: Explosiones visuales al recoger items y recibir daño
- **Textos Flotantes**: Feedback visual de puntuación en tiempo real
- **Invulnerabilidad**: Estado temporal con efecto visual de parpadeo
- **High Score Persistente**: Guardado automático del mejor récord
- **Animación de Muerte**: Explosión con 50 partículas al perder una vida

#### 🏗️ Arquitectura
- **Reestructuración completa** del código a arquitectura modular OOP
- **Paquete makeuprain**: Separación de responsabilidades en módulos
- **Scene Manager**: Sistema de escenas (Menu, Game, GameOver, Pause)
- **Entity System**: Clases separadas para Player, Enemy, Collectible, Particle
- **UI Components**: Button, Panel, FloatingText reutilizables
- **Config Centralizado**: Un solo archivo de configuración
- **Main simplificado**: Reducido de 270 a <50 líneas

#### 🎨 Mejoras Visuales
- **Paleta moderna**: Morados, rosas neón, cyan y dorados
- **Gradientes animados**: Fondos y UI con degradados suaves
- **HUD reorganizado**: Multiplicador visible, combo destacado, barra de progreso
- **Paneles con transparencia**: UI semi-transparente elegante
- **Animaciones fluidas**: Transiciones suaves entre escenas
- **Efectos de pulso**: En récords y game over
- **Tinting de jugadores**: Colores distintivos en modo cooperativo
- **Máscaras de colisión**: Colisiones pixel-perfect precisas

#### 🎮 Mejoras de Gameplay
- **Spawn continuo**: Los objetos no dejan de caer nunca
- **Velocidades balanceadas**: Enemigos 1.5-2.8, coleccionables 1.2-2.2
- **Controles alternativos**: Flechas + WASD para accesibilidad
- **Pausar mejorado**: Overlay con opciones de continuar/salir
- **Menú rediseñado**: Layout de 2 columnas con reglas y opciones
- **Feedback visual**: Indicadores claros de vidas, combo, progreso

#### 🐛 Correcciones
- **Colisiones precisas**: Implementación de pygame.mask
- **Colors.GRAY faltante**: Agregados todos los grises necesarios
- **Spawn detenido**: Corregido sistema de spawn continuo
- **Tinting incorrecto**: Cambio a BLEND_RGBA_MULT para coloración
- **Atributos faltantes**: tint_color, items_collected_this_round
- **Layout Game Over**: Contenido dentro de panel en modo individual
- **Emojis como rectángulos**: Reemplazados por texto ASCII

#### 📁 Estructura
- ➕ Agregado `.gitignore`, `LICENSE`, `requirements.txt`
- ➕ Carpeta `assets/` organizada con images y sounds
- ➕ Carpeta `docs/` para documentación adicional
- ➕ `highscore.json` generado automáticamente
- 📝 README completamente reescrito con documentación completa

#### ⚡ Rendimiento
- **60 FPS estables**: Optimización del game loop
- **Gestión de memoria**: Limpieza de entidades fuera de pantalla
- **Cache de assets**: AssetManager con carga única
- **Sprites optimizados**: Conversión eficiente con convert_alpha()

#### 💥 Breaking Changes
- Requiere Python 3.8+ (antes 3.6+)
- Requiere pygame 2.5+ (antes 2.0+)
- Estructura de archivos completamente diferente
- Sistema de configuración nuevo

---

## 🎓 Recursos de Aprendizaje

### Tecnologías Usadas
- **Python 3.8+**: Lenguaje de programación
- **Pygame 2.5+**: Librería para desarrollo de juegos 2D
- **JSON**: Persistencia de datos (high score)

### Conceptos Implementados
- Programación Orientada a Objetos (OOP)
- Patrones de diseño (Singleton, Factory, Observer)
- Sistema de escenas y estados
- Detección de colisiones pixel-perfect
- Sistema de partículas
- Interpolación y animaciones
- Gestión de eventos
- Persistencia de datos

### Aprende Más
- 📚 [Documentación de Pygame](https://www.pygame.org/docs/)
- 🎮 [Tutorial de Pygame](https://www.pygame.org/wiki/tutorials)
- 🐍 [Python Official Docs](https://docs.python.org/3/)

---

## 🌟 Características Futuras (Roadmap)

- [ ] Sistema de power-ups
- [ ] Más modos de juego (endless, time attack)
- [ ] Leaderboard online
- [ ] Logros y achievements
- [ ] Música dinámica según gameplay
- [ ] Más tipos de obstáculos y coleccionables
- [ ] Sistema de niveles con jefes
- [ ] Soporte para gamepad
- [ ] Modo de dificultad personalizable
- [ ] Efectos de sonido mejorados

---

## 👥 Autores

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/Joan-Mora.png" width="100px;" alt="Darwin Joan Aveiga Mora"/><br />
      <sub><b>Darwin Joan Aveiga Mora</b></sub><br />
      <a href="https://github.com/Joan-Mora">@Joan-Mora</a><br />
      <sub>Desarrollador Full Stack</sub>
    </td>
    <td align="center">
	  <img src="https://github.com/Camilandia20.png" width="100px;" alt="Maria Camila Alvarez Barreto"/><br />
      <sub><b>Lic. Maria Camila Alvarez Barreto</b></sub><br />
	  <a href="https://github.com/Camilandia20">@Camilandia20</a><br />
      <sub>Desarrollador Full Stack</sub>
    </td>
  </tr>
</table>

**Institución:** Corporación Universitaria Minuto de Dios  
**Programa:** Tecnología en Desarrollo de Software  
**Semestre:** II - 2025 

---

## 🙏 Agradecimientos

- Lic. Camila Alvarez por la idea principal 
- Pygame Community por la excelente documentación
- Contribuidores y testers
- A todos los que den ⭐ al proyecto

---

<div align="center">

**¡Dale una ⭐ si te gustó el proyecto!**

[⬆️ Volver arriba](#-makeup-rain-)

</div>
