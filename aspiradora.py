import random
import pygame
import pygame_gui
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import sys




class Habitacion:
    def __init__(self, position, size, door_position):
        self.position = position
        self.size = size
        self.door_position = door_position
        self.paredes = self.generar_paredes()
        self.puerta_contador = 0  # Counter for the door passage
        self.limpio = random.choice([True, False])  # Aleatorio si está limpio al inicio
        self.vacia = random.choice([True, False])
        self.manchas = set()
        self.generar_manchas()

    def limpiar_habitacion(self):
        self.limpio = True
        self.puerta_contador = 0

    def liberar_habitacion(self):
        self.vacia = True

    def generar_paredes(self):
        # Función lambda para generar las ubicaciones de las paredes en el borde de la habitación
        borde_habitacion = lambda x, y: [(x, i) for i in range(y, y + self.size[1])] + \
                                       [(i, y) for i in range(x, x + self.size[0])] + \
                                       [(x + self.size[0] - 1, i) for i in range(y, y + self.size[1])] + \
                                       [(i, y + self.size[1] - 1) for i in range(x, x + self.size[0])]

        return set(borde_habitacion(self.position[0], self.position[1]))
    
    def generar_manchas(self):
        if not self.limpio:
            self.manchas = set()

            # Generate random stains in the room
            for _ in range(random.randint(5, 10)):
                x = random.randint(self.position[0], self.position[0] + self.size[0] - 1)
                y = random.randint(self.position[1], self.position[1] + self.size[1] - 1)
                self.manchas.add((x, y))
    
class EstacionCarga:
    def __init__(self, position, size):
        self.position = position
        self.size = size

class Aspiradora:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.position = [grid_size // 2, grid_size // 2]
        self.estado = "Detenida"
        self.carga = 100

    def aspirar(self):
        if self.carga > 0:
            self.carga -= 1
            self.estado = "Aspirando"
        


    def mover(self, direction):
        if direction == "LEFT" and self.position[0] > 0:
            self.position[0] -= 1
        elif direction == "RIGHT" and self.position[0] < self.grid_size - 1:
            self.position[0] += 1
        elif direction == "UP" and self.position[1] > 0:
            self.position[1] -= 1
        elif direction == "DOWN" and self.position[1] < self.grid_size - 1:
            self.position[1] += 1

        self.estado = "Moviendose"

    def recargar(self):
        self.carga = 100
        self.estado = "Cargando"

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulación de Aspiradora Automática")

# Definir colores
white = (255, 255, 255)
black = (0, 0, 0)

# Tamaño de la cuadrícula y celda
grid_size = 50
cell_size = width // grid_size

aspiradora = Aspiradora(grid_size)
# Inicializar el gestor de eventos de la interfaz de usuario de pygame_gui
manager = pygame_gui.UIManager((width, height))

# Crear botones
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 10), (100, 30)),
    text='Iniciar',
    manager=manager
)

reset_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((120, 10), (100, 30)),
    text='Reiniciar',
    manager=manager
)

# Crear etiqueta para el estado de la aspiradora
state_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((0, 50), (300, 20)),
    text=f'Estado: {aspiradora.estado}',
    manager=manager
)

charge_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((10, 80), (200, 20)),
    text=f'Carga: {aspiradora.carga}',
    manager=manager
)

# Bucle principal
is_running = False
finder = AStarFinder()
habitacion1 = Habitacion((11, 8), (13, 13), (6, 12))
habitacion2 = Habitacion((27, 8), (13, 13), (6, 12))
habitacion3 = Habitacion((11, 30), (13, 13), (6, 0))
habitacion4 = Habitacion((27, 30), (13, 13), (6, 0))
estacion_carga = EstacionCarga((8, 24), (3, 3))  # Ajusta la posición y el tamaño según tus necesidades


grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

# Marcar las paredes en la cuadrícula
for habitacion in [habitacion1, habitacion2, habitacion3, habitacion4]:
    for pared in habitacion.paredes:
        grid[pared[1]][pared[0]] = 1

# Marcar la estación de carga como ocupada
estacion_carga_rect = pygame.Rect(estacion_carga.position[0] * cell_size,
                                   estacion_carga.position[1] * cell_size,
                                   estacion_carga.size[0] * cell_size,
                                   estacion_carga.size[1] * cell_size)
for x in range(int(estacion_carga_rect.x / cell_size), int((estacion_carga_rect.x + estacion_carga_rect.width) / cell_size)):
    for y in range(int(estacion_carga_rect.y / cell_size), int((estacion_carga_rect.y + estacion_carga_rect.height) / cell_size)):
        grid[y][x] = 1


clock = pygame.time.Clock()

while True:
    time_delta = clock.tick(60) / 1000.0  # Controlar la velocidad de los frames
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                aspiradora.mover("LEFT")
            elif event.key == pygame.K_RIGHT:
                aspiradora.mover("RIGHT")
            elif event.key == pygame.K_UP:
                aspiradora.mover("UP")
            elif event.key == pygame.K_DOWN:
                aspiradora.mover("DOWN")
            state_label.set_text(f'Estado: {aspiradora.estado}')

        # Manejar eventos de los botones
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    is_running = True
                elif event.ui_element == reset_button:
                    is_running = False
                    aspiradora = Aspiradora(grid_size)
                    aspiradora.recargar()  # Recharge the battery
                    aspiradora.estado = 'Detenida'
                    state_label.set_text(f'Estado: {aspiradora.estado}')
                    charge_label.set_text(f'Carga: {aspiradora.carga}')
                    for habitacion in [habitacion1, habitacion2, habitacion3, habitacion4]:
                        habitacion.limpio = random.choice([True, False])
                        habitacion.vacia = random.choice([True, False])
                        habitacion.generar_manchas()
                        habitacion.puerta_contador = 0


        manager.process_events(event)


    

    # Dibujar la cuadrícula
    screen.fill(white)
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, black, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, black, (0, y), (width, y))

    if (aspiradora.position[0] >= estacion_carga.position[0]) and \
       (aspiradora.position[0] < estacion_carga.position[0] + estacion_carga.size[0]) and \
       (aspiradora.position[1] >= estacion_carga.position[1]) and \
       (aspiradora.position[1] < estacion_carga.position[1] + estacion_carga.size[1]):
        state_label.set_text(f'Estado: {aspiradora.estado}')
        aspiradora.recargar()  # Recharge the battery
        charge_label.set_text(f'Carga: {aspiradora.carga}')
        
    aspiradora_position = tuple(aspiradora.position)

    for habitacion in [habitacion1, habitacion2, habitacion3, habitacion4]:
        if not habitacion.limpio and aspiradora_position in habitacion.manchas:
            aspiradora.aspirar()  # Ejecutar la acción de aspirar
            state_label.set_text(f'Estado: {aspiradora.estado}')
            charge_label.set_text(f'Carga: {aspiradora.carga}')
            habitacion.manchas.remove(aspiradora_position)  # Eliminar la mancha
            color = (200, 200, 200) 
            pygame.draw.rect(screen, color, pygame.Rect(aspiradora_position[0] * cell_size,
                                                        aspiradora_position[1] * cell_size,
                                                        cell_size, cell_size))

    for habitacion in [habitacion1, habitacion2, habitacion3, habitacion4]:

        if (aspiradora.position[0] == habitacion.position[0] + habitacion.door_position[0]) and \
           (aspiradora.position[1] == habitacion.position[1] + habitacion.door_position[1]) :
            
            state_label.set_text(f'Estado: Revisando habitacion')
            if habitacion.vacia:
                habitacion.puerta_contador += 1
                
            # If the vacuum cleaner passed through the door twice, update the room and decrease charge
                if habitacion.puerta_contador == 60:
                    if not habitacion.limpio:
                        aspiradora.carga -= 40
                        charge_label.set_text(f'Carga: {aspiradora.carga}')
                        habitacion.limpiar_habitacion()
                    if aspiradora.carga <= 20:  # Example condition for low battery
                        state_label.set_text(f'Estado: Bateria baja, regresando')
                    habitacion1.liberar_habitacion()
                    habitacion2.liberar_habitacion()
                    habitacion3.liberar_habitacion()
                    habitacion4.liberar_habitacion()

        # Determinar el color de la habitación basado en su estado
        color = (200, 200, 200) if habitacion.limpio else (210, 180, 140)  # Gris si está limpio, marrón claro si no
        pygame.draw.rect(screen, color,
                         pygame.Rect(habitacion.position[0] * cell_size,
                                     habitacion.position[1] * cell_size,
                                     habitacion.size[0] * cell_size,
                                     habitacion.size[1] * cell_size))
        if not habitacion.limpio:
            for mancha in habitacion.manchas:
                pygame.draw.rect(screen, (139, 69, 19),  # Color marrón oscuro
                                pygame.Rect(mancha[0] * cell_size,
                                            mancha[1] * cell_size,
                                            cell_size, cell_size))
        # Determinar el color de las paredes
        wall_color = (0, 255, 0) if habitacion.vacia else (255, 0, 0)  # Verde si está libre, rojo si no lo está
        for pared in habitacion.paredes:
            pygame.draw.rect(screen, wall_color,
                             pygame.Rect(pared[0] * cell_size,
                                         pared[1] * cell_size,
                                         cell_size, cell_size))
        
        # Dibujar la puerta (un espacio en una de las paredes)
        door_rect = pygame.Rect((habitacion.position[0] + habitacion.door_position[0]) * cell_size,
                                (habitacion.position[1] + habitacion.door_position[1]) * cell_size,
                                cell_size, cell_size)
        pygame.draw.rect(screen, white, door_rect)
    



    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(estacion_carga.position[0] * cell_size,
                                                        estacion_carga.position[1] * cell_size,
                                                        estacion_carga.size[0] * cell_size,
                                                        estacion_carga.size[1] * cell_size))

    # Dibujar la aspiradora
    vacuum_rect = pygame.Rect(aspiradora.position[0] * cell_size, aspiradora.position[1] * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, black, vacuum_rect)


    # Actualizar la interfaz de usuario de pygame_gui
    manager.update(time_delta)
    manager.draw_ui(screen)

    # Actualizar la pantalla
    pygame.display.flip()
