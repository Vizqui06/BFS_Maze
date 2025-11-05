# Como Alcaraz hizo con la clase BST, aquí igual se maneja todo el laberinto y se reparten la chamba
from collections import deque as dq
from random import randint
from time import sleep
import pygame

class Maze:
    def __init__(self, input): # El constructor
        
        # Divido el laberinto por líneas para más fácil
        lines = input.strip().split('\n')
        
        # La primera línea contiene altura y anchura del laberinto
        self.height, self.width = map(int, lines[0].split())
        
        # Poner a matriz del laberinto como lista de listas
        # Cada fila es una lista de caracteres que están dentro de ('0', '1', 'A', 'B')
        self.matrix = []
        for i in range(1, self.height + 1):
            # Hacer que cada línea sea una lista de caracteres
            row = list(lines[i])
            self.matrix.append(row)
        
        # Guardar las posiciones de A (inicio) y B (fin)
        self.start = None # Coordenada donde está A (inicio)
        self.end = None # Coordenada donde está B (fin)
        
        # Buscar las posiciones de A y B recorriendo toda la matriz
        for row in range(self.height): # Buscar en cada columna
            for col in range(self.width): # Buscar en cada fila
                if self.matrix[row][col] == 'A': # Cuando se encuentre a A
                    self.start = (row, col)  # Guarda coordenada de A
                elif self.matrix[row][col] == 'B': # Cuando se encuentre a B
                    self.end = (row, col)    # Guarda coordenada de B
        
        # Matriz para marcar qué celdas ya se han visitado durante el recorrido (Alcaraz dijo que hacer esto evita que se hagan ciclos interminables)
        # False = no visitada, True = ya visitada
        self.visited = [] # Guardar las coordenadas que ya se visitaron
        for row in range(self.height): # Por cada fila del laberinto
            row_visited = [] # Creamos una lista temporal para esa fila
            for col in range(self.width): # Por cada columna en esa fila
                row_visited.append(False) # Inicialmente todas las celdas no están visitadas
            self.visited.append(row_visited) # Agregamos la fila completa a la matriz de visitados

        
        # Lista que guardará el camino solución (coordenadas en orden)
        # Muy similar a cómo Alcaraz lo hizo con la función de enlistar(), que guardaba los nodos del árbol
        self.path = []
        self.dfs_path = []
        self.bfs_result = []
        self.bfs_path = []
        
        # Bandera para saber si ya se encontró la solución
        self.found = False


    # Este espacio es porque dejé todo bien apretado y me perdí XDDDDDDDD


    def solve(self):
        # * Ahora la parte que carrea a todo el código, la búsqueda del camino hacia B mediante DFS desde la posición A
        
        # Verifica que existan posiciones de inicio y fin (tremendo momazo calcular la ruta si ni siquiera A o B existen xd)
        if not self.start or not self.end:
            return None # Si no hay A o B, no tiene caso buscar nada
        
        # Todo el pedo nicia desde la posición de A
        start_row, start_col = self.start # Sacamos la fila y columna donde está A
        self._dfs_recursive(start_row, start_col) # DELEGACIÓN: Le pasamos la chamba a la función recursiva
        self.bfs_solve()

        # Si se encuentra el camino, lo retornamos; si no, retornamos None
        if self.found: # Si la bandera está en True es porque encontramos a B
            return self.path # Regresamos el camino completo
        else: # Si no encontramos nada
            return None # Regresamos None (no hay solución)


    def _dfs_recursive(self, row, col):
        # Voy a intentar hacerlo recursivo, si no me sale, le pido consejo a mi becario
        
        # Un buen consejo de mi becario fue poner bien claros los casos base, que son las condiciones donde SE DETIENE la recursión
        
        # Caso 1: Si ya encontramos la salida, no seguir buscando xd
        if self.found:
            return
        
        # Caso 2: Verificar si estamos fuera de los límites del laberinto
        if row < 0 or row >= self.height or col < 0 or col >= self.width: # Le pedí al becario que me corrigiera el condicional
            return  # Sale de esta rama de recursión
        
        # Casi 3: Si el recorrido llega a una pared (un callejón sin salida), no se puede pasar como se hace en la frontera
        if self.matrix[row][col] == '0':
            return  # Sale de esta rama de recursión
        
        # Caso 4: Si ya visitamos una celda antes, no volver a pasar por ahí
        if self.visited[row][col]:
            return  # Sale de esta rama de recursión
        
        # * VER QUE PEDO CON LA CELDA ACTUAL (hay que llevarla por el buen camino)
        
        # Marca la celda como visitada (porque ya está ahí)
        self.visited[row][col] = True
        
        # Agregr la coordenada actual al camino
        # Esto es como cuando la función enlistar agregaba nodos a la lista
        self.path.append((row, col))
        self.dfs_path.append((row, col))

        # Caso espectacular: Pisamos B 🦅🦅🔥🔥🔥🥶🥶
        if self.matrix[row][col] == 'B':
            self.found = True  # Marcamos que encontramos la solución
            return  # Se detiene la búsqueda, ya se llegó a la meta
        
        # * Definir las 4 direcciones posibles
        # * Como la función de insertar llamaba a self.izq.insertar() y self.der.insertar()
        
        # Cada tupla es (cambio_en_fila, cambio_en_columna)
        # Alcaraz sugirió tender siempre a pegarse a la pared en la izq o der para así hallar solución, tambien arriba y der o arriba e izq, aunque se puedan las 4
        directions = [
            (-1, 0),  # Arriba: resta 1 a la fila porque se baja y sube en filas 
            (0, 1),   # Derecha: suma 1 a la columna porque se mueve a la izq y der en columnas
            (1, 0),   # Abajo: suma 1 a la fila
            (0, -1)   # Izquierda: resta 1 a la columna
        ]
        
        # Probar moverse en cada dirección (así como Alcaraz hizo en el pizarrón)
        for d_row, d_col in directions:
            # Si ya se encontró un camino por el que ir, ir a ese
            if self.found:
                break
            
            # Calcula la nueva posición (porque ya nos movimos y hay que saber A DÓNDE nos movimos)
            new_row = row + d_row # Sumamos el cambio de fila a la fila actual
            new_col = col + d_col # Sumamos el cambio de columna a la columna actual
            
            # Explorar esa dirección a fondo
            # Es como cuando el nodo llamaba a sus hijos para que hicieran el trabajo
            # Esta llamada va a generar más llamadas (recursivas), como una rama. Mientras se pueda seguir avanzando sin recorrer la misma celda, no se detiene.
            self._dfs_recursive(new_row, new_col) # La función se llama a sí misma con la nueva posición
        
        # Si no se encuentra un camino por esa rama, retrocede hasta donde se pueda avanzar
        
        # Si después de explorar todas las direcciones no se encuentra ninguna solución, hay que quitar esa coordenada del camino (backtracking)
        # Esto es crucial para DFS: si este camino no funciona, lo descartamos

        if not self.found:
            self.path.pop()  # Removemos la última coordenada agregada (tu no has visto nada..., diría Skipper)
            # Nota: No hay que quitar el "ya visitado" porque ya pasamos por ahí y puede tender a recorrer ese camino 'legalmente' de manera indefinida. Le tienta irse por ahí
        
    # Algoritmo para el BFS
    def bfs_solve(self):

        #Regresa nada si no hay inicio o no hay final
        if not self.start or not self.end:
            return None

        #Crea una matriz de celdas falsas para contar cuáles han sido visitadas de acuerdo al ancho y alto 
    
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        
        # Hace el poderosísimo dairy queen y de una vez el mete el punto de inicio a sí mismo y a la matriz de visitados
        queue = dq([self.start])
        self.visited[self.start[0]][self.start[1]] = True
        
        parent = {self.start: None}

        while queue:
            row, col = queue.popleft()
            self.bfs_path.append((row,col))
            # Regresa un resultado cuando llega al final del laberinto y regresa el camino que siguió
            if (row, col) == self.end:
                # Reconstruct path
                self.bfs_result = []
                curr = self.end
                while curr is not None:
                    self.bfs_result.append(curr)
                    curr = parent[curr]
                self.bfs_result.reverse()
                self.found = True
                return self.bfs_result

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

            for d_row, d_col in directions:
                new_row, new_col = row + d_row, col + d_col

                # If con un friego de condiciones, el símbolo \ permite que se vean dentro de la pantalla
        
                if 0 <= new_row < self.height and 0 <= new_col < self.width and \
                   self.matrix[new_row][new_col] != '0' and not self.visited[new_row][new_col]:
                    
                    self.visited[new_row][new_col] = True
                    queue.append((new_row, new_col))
                    parent[(new_row, new_col)] = (row, col)
        
        return None


    def print_path(self):
        # Ya después de la talacha, toca imprimir con el formato de AlcaGOAT: (fila,col)-(fila,col)-(fila,col)
        
        if not self.path: # Pero si no se encontró un camino...
            print("No se encontró camino") # Bro, no hay nada que imprimir
            return
        
        # Convertir cada coordenada a string en formato (fila,col)
        path_strings = [] # Lista vacía para guardar los strings
        for row, col in self.path: # Por cada coordenada en el camino
            coord_string = f"({row},{col})" # Formateamos la coordenada como string
            path_strings.append(coord_string) # Agregamos el string a la lista
        
        print("DFS search path: ", self.dfs_path)
        dfs_search_strings = [] # Lista vacía para guardar los strings
        for row, col in self.dfs_path: # Por cada coordenada en el camino
            coord_string = f"({row},{col})" # Formateamos la coordenada como string
            dfs_search_strings.append(coord_string) # Agregamos el string a la lista
       
        bfs_path_strings = []
        for row, col in self.bfs_result: # Por cada coordenada en el camino
            coord_string = f"({row},{col})" # Formateamos la coordenada como string
            bfs_path_strings.append(coord_string) # Agregamos el string a la lista

        bfs_search_strings = []
        for row, col in self.bfs_path: # Por cada coordenada en el camino
            coord_string = f"({row},{col})" # Formateamos la coordenada como string
            bfs_search_strings.append(coord_string) # Agregamos el string a la lista
        
        # Appendeamos todas las coordenadas con guiones
        dfs_search_path = "-".join(dfs_search_strings)
        path_good = "-".join(path_strings)
        path_bfs_good = "-".join(bfs_path_strings)
        bfs_search_path = "-".join(bfs_search_strings)
        
        
        # Imprimimos el resultado
        print(f"Camino: {path_good}")
        #print(f"Camino de búsqueda DFS: {dfs_search_path}")
        #print(f"Camino de búsqueda BFS: {bfs_search_path}")

    def get_dfs_path(self):
        return self.path

    def get_bfs_path(self):
        return self.bfs_result 
    

    def main(self):
        pygame.init()
        pantalla = pygame.display.set_mode((600,600))
        rect_height = 600/self.height
        rect_width = 600/self.width
        pantalla.fill((255,255,255))
        turquoise = (83,195,189)
        white = (255,255,255)
        black = (0,0,0)
        red = (255,0,0)
        green = (0,255,0)

        for i in range(self.height):
            lista = list()
            for j in range(self.width):
                pos = (rect_height*i,rect_width*j,rect_height,rect_width)

                match self.matrix[i][j]:
                    case "0":
                        lista.append(pygame.draw.rect(pantalla,white,pos))
                    case "1":
                        lista.append(pygame.draw.rect(pantalla,black,pos))
                    case "A":
                        lista.append(pygame.draw.rect(pantalla,red,pos))
                    case "B":
                        lista.append(pygame.draw.rect(pantalla,green,pos))

            
        for i in range(len(self.bfs_path)):
            print(i)
            m,n = self.bfs_path[i]
            pos = (rect_height*m,rect_width*n,rect_height,rect_width)    
            pygame.draw.rect(pantalla, turquoise, pos)
            sleep(0.5)
            pygame.display.update()

        for i in range(self.height):
            lista = list()
            for j in range(self.width):
                pos = (rect_height*i,rect_width*j,rect_height,rect_width)

                match self.matrix[i][j]:
                    case "0":
                        lista.append(pygame.draw.rect(pantalla,white,pos))
                    case "1":
                        lista.append(pygame.draw.rect(pantalla,black,pos))
                    case "A":
                        lista.append(pygame.draw.rect(pantalla,red,pos))
                    case "B":
                        lista.append(pygame.draw.rect(pantalla,green,pos))

        for i in range(len(self.dfs_path)):
            print(i)
            m,n = self.dfs_path[i]
            pos = (rect_height*m,rect_width*n,rect_height,rect_width)    
            pygame.draw.rect(pantalla, turquoise, pos)
            sleep(0.5)
            pygame.display.update()

        for i in range(self.height):
            lista = list()
            for j in range(self.width):
                pos = (rect_height*i,rect_width*j,rect_height,rect_width)

                match self.matrix[i][j]:
                    case "0":
                        lista.append(pygame.draw.rect(pantalla,white,pos))
                    case "1":
                        lista.append(pygame.draw.rect(pantalla,black,pos))
                    case "A":
                        lista.append(pygame.draw.rect(pantalla,red,pos))
                    case "B":
                        lista.append(pygame.draw.rect(pantalla,green,pos))

        for i in range(len(self.path)):
            print(i)
            m,n = self.path[i]
            pos = (rect_height*m,rect_width*n,rect_height,rect_width)    
            pygame.draw.rect(pantalla, turquoise, pos)
            sleep(0.5)
            pygame.display.update()

        while True:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
            

# Ya aquí es donde se pone el laberintyo y se resuelve :v

input = """4 4
B100
0101
0111
110A"""


# El objeto maze para que se use en la clase con el input
maze = Maze(input)

# Se manda a producción para que resuelva el laberinto
result = maze.solve()

# Imprime el camino (Alcaraz quiere las coordenadas separadas por guiones)
maze.print_path()
maze.main()