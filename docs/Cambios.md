# Changelog - Sistema de Rondas y Modo Cooperativo

## Versión 2.1.0 - Sistema de Rondas y Cooperativo

### 🎮 Nuevas Características

#### Sistema de Rondas
- **Progresión por rondas**: El juego ahora se divide en rondas de 30 objetos coleccionables cada una
- **Dificultad ascendente**: La velocidad de los objetos aumenta un 30% por cada ronda completada
- **Transiciones visuales**: Pantalla de transición entre rondas mostrando:
  - Ronda completada
  - Bonus de puntos otorgado
  - Próxima ronda
  - Multiplicador de velocidad actual
- **Indicador de progreso**: Barra de progreso en el HUD mostrando cuántos objetos se han recolectado en la ronda actual

#### Modo Cooperativo (2 Jugadores)
- **Selección en menú**: Tres botones en el menú principal:
  - "Individual" (Boton 1)
  - "Cooperativo" (Boton 2)
  - "Salir" (Boton 3)
- **Controles independientes**:
  - Jugador 1: Flechas ← / →
  - Jugador 2: Teclas A / D
- **Posicionamiento**: Jugadores aparecen en diferentes posiciones horizontales
- **Identificación visual**:
  - Jugador 1: Tinte azul (cyan)
  - Jugador 2: Tinte rosa
- **Puntaje individual**: Cada jugador acumula su propio puntaje
- **Condición de victoria**: El juego termina cuando ambos jugadores mueren, ganando quien tenga más puntos

### 🔧 Cambios Técnicos

#### Archivos Modificados

**`camigame/config.py`**
- Agregado `PlayerConfig` con controles configurables:
  - `PLAYER1_LEFT`, `PLAYER1_RIGHT` (flechas)
  - `PLAYER2_LEFT`, `PLAYER2_RIGHT` (A/D)
  - `PLAYER1_TINT`, `PLAYER2_TINT` (colores)
- Agregado `RoundConfig`:
  - `ITEMS_PER_ROUND = 30`
  - `SPEED_MULTIPLIER_PER_ROUND = 0.3`
  - `BASE_ROUND_BONUS = 500`
  - `BONUS_MULTIPLIER = 1.5`
- Agregado `GameMode` enum (aunque no se usa directamente, el modo se almacena como int)

**`camigame/entities/game_entities.py`**
- Clase `Player` mejorada:
  - Parámetro `player_id` para identificación
  - Parámetros `controls_left` y `controls_right` configurables
  - Parámetro `tint_color` para distinción visual
  - Atributo `score` individual
  - Método `_apply_tint()` para aplicar color al sprite

**`camigame/core/round_manager.py`** (NUEVO)
- Clase `RoundManager` para gestionar:
  - Número de ronda actual
  - Progreso de recolección
  - Cálculo de multiplicador de velocidad
  - Cálculo de bonus por ronda
  - Conteo de enemigos y coleccionables según ronda

**`camigame/scenes/menu_scene.py`**
- Dividido el botón "JUGAR" en dos:
  - `single_player_button` → establece `game_mode = 1`
  - `coop_button` → establece `game_mode = 2`
- Actualizados controles en pantalla para mostrar ambos jugadores
- Agregados atajos de teclado (1 y 2)

**`camigame/core/game_manager.py`**
- Agregado atributo `game_mode` (default: 1)

**`camigame/scenes/game_scene.py`**
- Cambio de `self.player` a `self.players: List[Player]`
- Agregado `self.round_manager = RoundManager()`
- Agregados atributos para transiciones:
  - `showing_round_transition`
  - `transition_timer`
- **`reset_game()`**: Crea 1 o 2 jugadores según `game_mode`
- **`spawn_round_entities()`**: Genera objetos con multiplicador de velocidad
- **`update()`**: 
  - Bucle de colisión para múltiples jugadores
  - Detección de completación de ronda
  - Verificación de que todos los jugadores murieron
  - Actualización de puntaje individual por jugador
- **`draw()`**:
  - HUD adaptable (más alto en modo 2 jugadores)
  - Indicador de ronda y progreso
  - Puntajes separados para modo cooperativo
  - Vidas de ambos jugadores
- **`_draw_round_transition()`**: Pantalla de transición entre rondas

**`camigame/scenes/gameover_scene.py`**
- **`on_enter()`**: Recopila datos de jugadores y determina ganador
- **`draw()`**:
  - Modo 1 jugador: Pantalla tradicional
  - Modo 2 jugadores: 
    - Anuncio de ganador con efecto de pulso
    - Puntajes individuales con colores identificativos
    - Mensaje de empate si los puntajes son iguales

### 📊 Fórmulas de Juego

**Multiplicador de Velocidad**
```
velocidad = velocidad_base × (1 + 0.3 × (ronda - 1))
```

**Bonus por Ronda**
```
bonus = 500 × (1.5 ^ (ronda - 1))
```

**Condición de Victoria (Coop)**
```
if puntaje_jugador1 > puntaje_jugador2:
    ganador = Jugador 1
elif puntaje_jugador2 > puntaje_jugador1:
    ganador = Jugador 2
else:
    empate
```

### 🎯 Instrucciones de Juego

#### Modo Un Jugador
1. Selecciona "1 JUGADOR" en el menú
2. Usa las flechas ← y → para moverte
3. Recolecta 30 objetos para completar cada ronda
4. Evita los enemigos
5. Cada ronda es más rápida que la anterior

#### Modo Cooperativo
1. Selecciona "2 JUGADORES" en el menú
2. Jugador 1 usa ← y →
3. Jugador 2 usa A y D
4. Compite por más puntos
5. El juego termina cuando ambos pierden todas sus vidas
6. Gana quien tenga más puntos al final

### 🐛 Correcciones
- Ajustado el sistema de spawn para usar multiplicadores de velocidad
- Eliminado el sistema de dificultad basado en frames (reemplazado por sistema de rondas)
- Corregida la detección de colisiones para múltiples jugadores

### ⚡ Mejoras de Rendimiento
- Optimización del bucle de colisiones para manejar múltiples jugadores eficientemente
- Sistema de partículas se mantiene dentro del límite configurado

---

**Nota**: Esta actualización transforma completamente la experiencia de juego, añadiendo rejugabilidad mediante el sistema de rondas y la opción de jugar con un amigo en modo cooperativo.
