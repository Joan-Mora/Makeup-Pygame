"""
Makeup Rain - Juego arcade de recolección
Entry point principal del juego.

Ejecuta este archivo para iniciar el juego:
    python main.py
"""
from makeuprain import run


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print("\n¡Gracias por jugar!")
    except Exception as e:
        print(f"❌ Error al iniciar el juego: {e}")
        import traceback
        traceback.print_exc()
        raise
