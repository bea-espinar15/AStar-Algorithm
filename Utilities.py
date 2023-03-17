
#
#   CLASE UTILITIES
#   ---------------
#   En esta clase se definen constantes utilizadas por el resto de clases
#

# Dimensión de la pantalla
SCREENWIDTH = 800
# Márgenes
HEADER = 60
MARGIN = 100
# Dimensiones tablero
DIM = 600
# Constante para moverse en las 8 direcciones:
# ABAJO, DCHA, ARRIBA, IZDA, DIAG_ABAJO_CHA, DIAG_ABAJO_IZDA, DIAG_ARRIBA_IZDA, DIAG_ARRIBA_DCHA
DIRS = {(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)}

# Leyenda de colores
BLACK = (0, 0, 0)               # Color texto
LIGHT_YELLOW = (225, 202, 160)  # Background pantalla
WHITE = (255, 255, 255)         # Background tablero
GREY = (128, 128, 128)          # Líneas tablero
BEIGE = (237, 199, 150)         # Nodos en CERRADA
BROWN = (219, 139, 86)          # Nodos en ABIERTA
MAROON = (132, 44, 48)          # Nodos barrera (casillas inalcanzables)
BLUE = (155, 191, 209)          # Camino solución
YELLOW = (233, 188, 109)        # Nodo origen
GREEN = (132, 167, 37)          # Nodo destino
PURPLE = (142, 79, 234)         # Waypoints
RED = (210, 46, 46)             # Nodos con penalización (casillas peligrosas)
