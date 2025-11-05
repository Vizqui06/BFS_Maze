import pygame # Importa el módulo de Pygame para crear juegos y aplicaciones multimedia
import sys # Importa el módulo sys para interactuar con el sistema operativo
from pygame.locals import QUIT # Importa la constante QUIT para detectar el cierre de la ventana
from random import randint # Importa la función randint para generar números aleatorios
from time import sleep # Importa la función sleep para pausar la ejecución

def main():
    pygame.init() # Inicializa el módulo de Pygame 
    pygame.display.set_caption("Juego") # Establece el título de la ventana
    
    pantalla = pygame.display.set_mode((400, 400), 0, 32) # Crea una ventana de 400x400 píxeles con 32 bits por píxel
    pantalla.fill((255, 255, 255)) # Rellena la pantalla con el color blanco
    rectangulos=[] # Lista para almacenar los rectángulos
    for i in range(4): # Bucle para crear 4 filas
        lista = list() # Lista para almacenar los rectángulos de cada fila
        for j in range(4): # Bucle para crear 4 columnas
            lista.append(pygame.draw.rect(pantalla,(randint(0, 255), randint(0, 255), randint(0, 255)),(100*i, 100*j, 100, 100))) # Dibuja un rectángulo de 100x100 píxeles con un color aleatorio
        rectangulos.append(lista) # Añade la lista de rectángulos de la fila a la lista principal

    i = 0 # Índice para recorrer el camino
    
    camino = [(0,0), (0,1), (1,1), (1,2), (1,3), (2,3), (3,3)] # Lista de coordenadas del camino a seguir

    while True: # Bucle principal del juego
        for event in pygame.event.get(): # Recorre todos los eventos que hayan ocurrido
            if event.type == QUIT: # Si el evento es cerrar la ventana,
                pygame.quit() # Salimos del bucle principal
                sys.exit() # Salimos del bucle principal

        m,n = camino[i] # Obtiene las coordenadas actuales del camino

        pygame.draw.rect(pantalla,(randint(0, 255), randint(0, 255), randint(0, 255)),(100*m, 100*n, 100, 100)) # Dibuja un rectángulo en la posición actual del camino con un color aleatorio
        sleep(1) # Pausa la ejecución durante 1 segundo
    
        # Actualizar la pantalla
        pygame.display.update()

        i= (i+1) # Incrementa el índice para la siguiente posición del camino
        if i == len(camino): # Si se ha llegado al final del camino,
            color = [randint(0, 255) for _ in range(3)] # Genera un color aleatorio
            i = 0 # Reinicia el índice para comenzar de nuevo

main()
