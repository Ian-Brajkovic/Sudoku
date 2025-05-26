import pygame
import numpy as np
import random
from Logica import llenar_sudoku
pygame.init()

# Encuadrar numeros y hacerlos desaparecer al completarlos
# Resaltar los numeros al seleccionar uno
# Implementar dificultades y puntaje

screen_size = 650
info_height = 100
screen = pygame.display.set_mode((screen_size, screen_size + info_height))
cell_size = screen_size // 9

black = (0, 0, 0)
white = (255,255,255)
red = (255, 0, 0)  # Color rojo para celdas vacías
highlight_color = (165,237,250)  # Color para destacar filas/columnas
number_highlight_color = (0,195,230)  # Color dorado para números iguales
selected_cell_color = (0,195,230)  # Color para la celda seleccionada

def start_screen():
    """
    Create a start screen with difficulty selection buttons.
    Returns the selected difficulty percentage.
    """
    # Initialize the screen
    start_screen = pygame.display.set_mode((screen_size, screen_size + info_height))
    pygame.display.set_caption("Sudoku")
    icon_image = pygame.image.load('Icono_sudoku.png')
    pygame.display.set_icon(icon_image)
    
    # Fill background
    start_screen.fill(white)
    
    # Set up font
    title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)
    
    # Draw title
    title_text = title_font.render("SUDOKU", True, black)
    title_rect = title_text.get_rect(center=(screen_size // 2, 150))
    start_screen.blit(title_text, title_rect)
    
    # Create difficulty buttons
    button_width, button_height = 200, 60
    button_x = screen_size // 2 - button_width // 2
    
    facil_button = pygame.Rect(button_x, 250, button_width, button_height)
    medio_button = pygame.Rect(button_x, 330, button_width, button_height)
    dificil_button = pygame.Rect(button_x, 410, button_width, button_height)
    
    # Draw buttons
    pygame.draw.rect(start_screen, (145, 185, 217), facil_button)
    pygame.draw.rect(start_screen, (250, 177, 98), medio_button)
    pygame.draw.rect(start_screen, (240, 84, 84), dificil_button)
    
    # Add text to buttons
    facil_text = button_font.render("Fácil", True, black)
    medio_text = button_font.render("Medio", True, black)
    dificil_text = button_font.render("Difícil", True, black)
    
    start_screen.blit(facil_text, (facil_button.centerx - facil_text.get_width() // 2, facil_button.centery - facil_text.get_height() // 2))
    start_screen.blit(medio_text, (medio_button.centerx - medio_text.get_width() // 2, medio_button.centery - medio_text.get_height() // 2))
    start_screen.blit(dificil_text, (dificil_button.centerx - dificil_text.get_width() // 2, dificil_button.centery - dificil_text.get_height() // 2))
    
    # Update display
    pygame.display.flip()
    
    # Handle button clicks
    waiting = True
    difficulty = 0.2  # Default difficulty (20% empty cells, 80% filled)
    
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if facil_button.collidepoint(mouse_pos):
                    difficulty = 0.2  # 20% empty cells (80% filled)
                    waiting = False
                elif medio_button.collidepoint(mouse_pos):
                    difficulty = 0.4  # 40% empty cells (60% filled)
                    waiting = False
                elif dificil_button.collidepoint(mouse_pos):
                    difficulty = 0.6  # 60% empty cells (40% filled)
                    waiting = False
    
    return difficulty

def get_difficulty_sudoku(original_sudoku, difficulty):
    """
    Creates a sudoku with a given difficulty level.
    Args:
        original_sudoku (np.array): The original complete sudoku.
        difficulty (float): The percentage of cells to empty.
    Returns:
        np.array: The sudoku with the specified difficulty.
    """
    return delete_numbers(original_sudoku, difficulty)

def draw_info_area(screen, lives, ayudas, game_over=False):
 font = pygame.font.Font(None, 36)
 lives_img = pygame.image.load('Corazon.png')
 lives_size = pygame.transform.scale(lives_img,(40,40))
 pos_x = 20
 for i in range(lives):
  screen.blit(lives_size, (pos_x, screen_size + 30))
  pos_x+=40
 
 if ayudas >=3:
  help_button = pygame.Rect(screen_size - 100, screen_size + 30, 80, 40)
  pygame.draw.rect(screen, (50, 50, 50), help_button)
  help_text = font.render("Help", True, black)
  screen.blit(help_text, (screen_size - 90, screen_size + 40))
 else:
  help_button = pygame.Rect(screen_size - 100, screen_size + 30, 80, 40)
  pygame.draw.rect(screen, (0, 255, 0), help_button)
  help_text = font.render("Help", True, black)
  screen.blit(help_text, (screen_size - 90, screen_size + 40))
 
 # Añadir botón de menú principal
 main_menu_button = pygame.Rect(screen_size - 220, screen_size + 30, 100, 40)
 pygame.draw.rect(screen, (145, 185, 217), main_menu_button)
 menu_text = font.render("Menu", True, black)
 screen.blit(menu_text, (screen_size - 205, screen_size + 40))
 
 # Solo mostrar el botón de respuesta cuando el juego termine (game_over=True)
 show_answer_button = None
 if game_over:
   show_answer_button = pygame.Rect(screen_size - 350, screen_size + 30, 120, 40)
   pygame.draw.rect(screen, (50, 150, 250), show_answer_button)
   answer_text = font.render("Ver Respuesta", True, black)
   screen.blit(answer_text, (screen_size - 345, screen_size + 40))
 
 return help_button, show_answer_button, main_menu_button

def encuadrar_numeros(array):
 conteo = {k: np.count_nonzero(array == k) for k in range(1, 10)}
 pos_x = screen_size - 500
 pos_y = screen_size + 40
 font = pygame.font.Font(None, 24)
 for i in range(1,10):
  if conteo[i]!=9:
   num_text = font.render(f"{i}", True, black)
   pygame.draw.line(screen, black, (pos_x,pos_y),(pos_x+20,pos_y), 1)
   pygame.draw.line(screen, black, (pos_x,pos_y),(pos_x,pos_y+20),1)
   pygame.draw.line(screen, black, (pos_x,pos_y+20),(pos_x+20,pos_y+20),1)
   pygame.draw.line(screen, black, (pos_x+20,pos_y),(pos_x+20,pos_y+20), 1)
   screen.blit(num_text, (pos_x+7, pos_y+5))
   pos_x+=30
 pygame.display.flip()

def handle_help_click(help_button, mouse_pos, selected_cell, original_sudoku, sudoku_a_resolver, lives, ayudas):
 if help_button and help_button.collidepoint(mouse_pos):
  if selected_cell != None and ayudas<=3:
    sudoku_a_resolver[selected_cell]=original_sudoku[selected_cell]
    update_screen(lives, sudoku_a_resolver, ayudas, sudoku_a_resolver)

def handle_show_answer(show_answer_button, mouse_pos, original_sudoku, sudoku_a_resolver):
    if show_answer_button and show_answer_button.collidepoint(mouse_pos):
        # Guardar las celdas actuales que están vacías para marcarlas en rojo
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if sudoku_a_resolver[i, j] == 0:
                    empty_cells.append((i, j))
        
        # Mostrar la solución completa
        temp_sudoku = original_sudoku.copy()
        
        # Dibujar el sudoku con la solución
        background(screen)
        draw_sudoku(temp_sudoku, empty_cells)
        
        # Añadir un botón para volver al juego o reiniciar
        font = pygame.font.Font(None, 36)
        replay_button = pygame.Rect(screen_size // 2 - 90, screen_size + 30, 180, 40)
        pygame.draw.rect(screen, (145, 185, 217), replay_button)
        replay_text = font.render("Nuevo Juego", True, black)
        screen.blit(replay_text, (screen_size // 2 - 80, screen_size + 40))
        
        # Añadir el botón de menú principal
        main_menu_button = pygame.Rect(screen_size // 2 + 100, screen_size + 30, 100, 40)
        pygame.draw.rect(screen, (145, 185, 217), main_menu_button)
        menu_text = font.render("Menu", True, black)
        screen.blit(menu_text, (screen_size // 2 + 115, screen_size + 40))
        
        pygame.display.flip()
        return True, replay_button, main_menu_button
    
    return False, None, None

def replay(pos_x,pos_y):
 font =  pygame.font.Font(None, 36)
 replay_button = pygame.Rect(pos_x, pos_y,100,50)
 pygame.draw.rect(screen, (145,185,217), replay_button)
 replay_text = font.render("Replay", True, black)
 screen.blit(replay_text, (pos_x+10, pos_y+10))
 return replay_button

def main_menu_button(pos_x, pos_y):
 font = pygame.font.Font(None, 36)
 menu_button = pygame.Rect(pos_x, pos_y, 100, 50)
 pygame.draw.rect(screen, (145, 185, 217), menu_button)
 menu_text = font.render("Menu", True, black)
 screen.blit(menu_text, (pos_x+15, pos_y+10))
 return menu_button
     
def view_answer(pos_x):
 font =  pygame.font.Font(None, 36)
 answer_button = pygame.Rect(pos_x, (screen_size//2)+200,170,50)
 pygame.draw.rect(screen, (145,185,217), answer_button)
 view_text = font.render("View Answer", True, black)
 screen.blit(view_text, (pos_x+10, (screen_size//2)+210))
 return answer_button

def delete_numbers(original_sudoku: np.array, percentage:float) -> np.array: 
 """
 This function deletes a certain percentage of numbers from the original sudoku.
 Args:
 original_sudoku (np.array): The original sudoku.
 percentage (float): The percentage of numbers to delete.
 Returns:
 np.array: The sudoku with the numbers deleted
 """
 # Copiar el sudoku resuelto para no modificar el original
 copy = original_sudoku.copy()
 
 # Calcular el número total de celdas
 total_cells = 9 * 9  # En un Sudoku 9x9
 
 # Calcular cuántas celdas eliminar
 cells_to_remove = int(total_cells * percentage)
 
 # Generar una lista de todas las posiciones del Sudoku
 positions = [(i, j) for i in range(9) for j in range(9)]
 
 # Seleccionar aleatoriamente las celdas a vaciar
 selected_cells = random.sample(positions, cells_to_remove)
 # Eliminar los números en las celdas seleccionadas (poner 0)
 for (i, j) in selected_cells:
  copy[i, j] = 0
 return copy

def dificult(original_sudoku):
    """
    This function creates the difficulties of the sudoku.
    Each level is 20% more difficult than the previous one,
    starting with 'facil' at 20% empty cells (80% filled).
    
    Args:
        original_sudoku (np.array): The completed sudoku grid
        
    Returns:
        dict: The difficulties with corresponding sudoku grids
    """
    difficulties = {
        'facil': 0.2,    # 20% empty cells (80% filled)
        'medio': 0.4,    # 40% empty cells (60% filled) 
        'dificil': 0.6    # 60% empty cells (40% filled)
    }
    
    levels = {}
    
    for difficulty, percentage in difficulties.items():
        levels[difficulty] = delete_numbers(original_sudoku, percentage)
    
    return levels

def background(screen: pygame.Surface) -> pygame.Surface:
 """
 Draw the background of the game
 Args:
  screen (pygame.Surface): the surface where is goning to be played the game
 Returns:
  pygame.Surface: the background 
 """
 icon_image = pygame.image.load('Icono_sudoku.png')
 pygame.display.set_icon(icon_image)
 pygame.display.set_caption("Sudoku")
 screen.fill(white)
 for i in range(10):  # Dibuja líneas
  thickness = 2 if i % 3 == 0 else 1  # Líneas más gruesas para subcuadrículas
  pygame.draw.line(screen, black, (i * cell_size, 0), (i * cell_size, screen_size), thickness)
  pygame.draw.line(screen, black, (0, i * cell_size), (screen_size, i * cell_size), thickness)
 pygame.display.flip()

def draw_sudoku(sudoku:np.array, empty_cells=None):
 """
 This funcion draws the numbers of the sudoku
 Args:
 sudoku (array): the sudoku to draw
 empty_cells (list): list of cells that should be marked as red
 """
 # Dibujar números
 font = pygame.font.Font(None, 65)
 
 # Si empty_cells no es None, marcar esas celdas en rojo
 if empty_cells:
     for i, j in empty_cells:
         pygame.draw.rect(screen, red, (j * cell_size, i * cell_size, cell_size, cell_size))
         pygame.draw.rect(screen, black, (j * cell_size, i * cell_size, cell_size, cell_size), 1)
 
 for i in range(9): # Recore las filas
  for j in range(9): # Recore las columnas
   if sudoku[i, j] != 0:  # Solo dibujar números no cero
     number_surface = font.render(str(sudoku[i, j]), True, black) # Si es distino de 0 obtiene q numero es 
     screen.blit(number_surface, (j * cell_size + cell_size //3, i * cell_size + cell_size // 4)) # screen.blit(que es lo que va a aparecer,(cordenada x, coordenada y))
   # Ya no marcamos las celdas vacías en rojo durante el juego normal
 pygame.display.flip()

def update_screen(lives, sudoku, ayudas, sudoku_a_resolver, game_over=False):
    background(screen)
    draw_sudoku(sudoku)
    buttons = draw_info_area(screen, lives, ayudas, game_over)
    encuadrar_numeros(sudoku_a_resolver)
    pygame.display.flip()
    return buttons

def highlight_same_numbers(sudoku, selected_row, selected_col):
    """
    Resaltar todos los números iguales al de la celda seleccionada
    """
    selected_number = sudoku[selected_row, selected_col]
    
    # Solo resaltar si hay un número en la celda seleccionada
    if selected_number == 0:
        return
    
    # Buscar todas las ocurrencias del mismo número y resaltarlas
    grid_color = black
    for i in range(9):
        for j in range(9):
            if sudoku[i, j] == selected_number:
                # Pintar el fondo de la celda con el color de resaltado para números iguales
                pygame.draw.rect(screen, number_highlight_color, (j * cell_size, i * cell_size, cell_size, cell_size))
                # Redibujar el borde
                pygame.draw.rect(screen, grid_color, (j * cell_size, i * cell_size, cell_size, cell_size), 1)

def main():
 primera_fila= random.sample(range(1, 10),9)
 sudoku = []
 sudoku.append(primera_fila)
 for i in range(8): 
  sudoku.append([0] * 9)
 llenar_sudoku(sudoku)
 while not llenar_sudoku(sudoku):
  llenar_sudoku(sudoku)
 sudoku_array = np.array(sudoku)
 original_sudoku = sudoku_array
 difficulty = start_screen()
 if difficulty is None:
  return  # User closed the game
 sudoku_a_resolver = get_difficulty_sudoku(original_sudoku, difficulty)
 lives = 3  # Initialize lives
 ayudas = 0
 game_over = False
 buttons = update_screen(lives, sudoku_a_resolver, ayudas, sudoku_a_resolver)
 help_button, show_answer_button, main_menu_button_obj = buttons
 solucion = original_sudoku
 pygame.display.flip()
 running = True
 selected_cell = None
 showing_answer = False
 replay_button = None
 menu_button = None
 
 while running:
  for event in pygame.event.get():
   if event.type == pygame.QUIT:
    running = False
   if event.type == pygame.MOUSEBUTTONDOWN:  
    mouse_pos = pygame.mouse.get_pos()
    
    # Comprobar si se ha hecho clic en el botón de menú principal
    if main_menu_button_obj and main_menu_button_obj.collidepoint(mouse_pos):
        # Volver a la pantalla de inicio
        main()
        return
    
    # Si estamos mostrando la respuesta y se hace clic en el botón de replay
    if showing_answer and replay_button and replay_button.collidepoint(mouse_pos):
        main()  # Reiniciar el juego
        return
    
    # Si estamos mostrando la respuesta y se hace clic en el botón de menú
    if showing_answer and menu_button and menu_button.collidepoint(mouse_pos):
        main()  # Volver al menú principal
        return
    
    # Si estamos mostrando la respuesta, ignorar los clics excepto en el botón de replay o menu
    if showing_answer:
        continue
        
    if mouse_pos[1] < screen_size:
     buttons = update_screen(lives, sudoku_a_resolver, ayudas, sudoku_a_resolver, game_over)
     help_button, show_answer_button, main_menu_button_obj = buttons
     x, y = mouse_pos
     row = y // cell_size
     col = x // cell_size
     selected_cell = (row, col)
 
     # Highlight the entire row by filling the background
     for c in range(9):
         # Pintar solo el fondo
         pygame.draw.rect(screen, highlight_color, (c * cell_size, row * cell_size, cell_size, cell_size))
         # Volver a dibujar el contorno
         pygame.draw.rect(screen, black, (c * cell_size, row * cell_size, cell_size, cell_size), 1)
     
     # Highlight the entire column by filling the background
     for r in range(9):
         # Pintar solo el fondo
         pygame.draw.rect(screen, highlight_color, (col * cell_size, r * cell_size, cell_size, cell_size))
         # Volver a dibujar el contorno
         pygame.draw.rect(screen, black, (col * cell_size, r * cell_size, cell_size, cell_size), 1)
     
     # Highlight the 3x3 square by filling the background
     square_row = (row // 3) * 3
     square_col = (col // 3) * 3
     for r in range(square_row, square_row + 3):
         for c in range(square_col, square_col + 3):
             # Pintar solo el fondo
             pygame.draw.rect(screen, highlight_color, (c * cell_size, r * cell_size, cell_size, cell_size))
             # Volver a dibujar el contorno
             pygame.draw.rect(screen, black, (c * cell_size, r * cell_size, cell_size, cell_size), 1)
     
     # NUEVO: Resaltar todos los números iguales al de la celda seleccionada
     if sudoku_a_resolver[row, col] != 0:
         highlight_same_numbers(sudoku_a_resolver, row, col)
     
     # Highlight the selected cell in blue (filled)
     pygame.draw.rect(screen, selected_cell_color, (col * cell_size, row * cell_size, cell_size, cell_size))
     pygame.draw.rect(screen, black, (col * cell_size, row * cell_size, cell_size, cell_size), 1)  # Volver a dibujar el borde
     
     draw_sudoku(sudoku_a_resolver)
    else:
      # Verificar si se ha hecho clic en el botón de mostrar respuesta (solo disponible cuando game_over=True)
      if game_over:
          showing_answer, replay_button, menu_button = handle_show_answer(show_answer_button, mouse_pos, original_sudoku, sudoku_a_resolver)
      
      if help_button and help_button.collidepoint(mouse_pos) and selected_cell!=None and sudoku_a_resolver[selected_cell]==0:
       ayudas+=1
      if ayudas<=3:
       handle_help_click(help_button, mouse_pos, selected_cell, original_sudoku, sudoku_a_resolver, lives, ayudas)
      
      if not showing_answer:
          selected_cell = None
     
   if event.type == pygame.KEYDOWN and selected_cell and not showing_answer:
    if event.key in range(pygame.K_1, pygame.K_9+1):
     number = event.key - pygame.K_0
     i, j = selected_cell
     if sudoku_a_resolver[i,j] == 0:
         if number == original_sudoku[i, j]:
             sudoku_a_resolver[i, j] = number
             buttons = update_screen(lives, sudoku_a_resolver, ayudas, sudoku_a_resolver, game_over)
             help_button, show_answer_button, main_menu_button_obj = buttons
             
             # NUEVO: Resaltar todos los números iguales cuando se introduce uno nuevo
             highlight_same_numbers(sudoku_a_resolver, i, j)
             
             # Redibujar el sudoku para mostrar el nuevo número
             draw_sudoku(sudoku_a_resolver)
         else:
             lives -= 1
             # Comprobar si perdió (sin vidas)
             if lives == 0:
                 game_over = True
             buttons = update_screen(lives, sudoku_a_resolver, ayudas, sudoku_a_resolver, game_over)
             help_button, show_answer_button, main_menu_button_obj = buttons
             
   if lives == 0 and np.all(sudoku_a_resolver)!=np.all(solucion):
     if not showing_answer:  # Solo mostrar la pantalla de perder si no estamos viendo la respuesta
         screen.fill(white)
         font = pygame.font.Font(None, 100)
         texto = font.render('You Lose',True,black)
         screen.blit(texto,(((screen_size)//2)-150,(screen_size)//2))
         replay_button = replay((screen_size//2)-200,(screen_size//2)+200)
         answer_button = view_answer((screen_size//2)-50)
         
         # Añadir botón de menú principal
         menu_button = main_menu_button((screen_size//2)+190, (screen_size//2)+200)
         
         pygame.display.flip()
     
     if event.type == pygame.KEYDOWN:
      continue
     
     if event.type == pygame.MOUSEBUTTONDOWN and not showing_answer:
      selected_cell = None
      mouse_pos = pygame.mouse.get_pos()
      if replay_button.collidepoint(mouse_pos):
       main()
       return
      elif answer_button.collidepoint(mouse_pos):
       showing_answer = True
       screen.fill(white)
       background(screen)
       # Identificar celdas vacías para marcarlas en rojo
       empty_cells = []
       for i in range(9):
           for j in range(9):
               if sudoku_a_resolver[i, j] == 0:
                   empty_cells.append((i, j))
       draw_sudoku(solucion, empty_cells)
       replay_button = replay((screen_size//2)-100,screen_size+40)
       
       # Añadir botón de menú principal
       menu_button = main_menu_button((screen_size//2)+20, screen_size+40)
       
       pygame.display.flip()
      elif menu_button and menu_button.collidepoint(mouse_pos):
       main()
       return
       
   elif np.all(sudoku_a_resolver)==np.all(solucion):
        pygame.time.wait(1000)
        screen.fill(white)
        font = pygame.font.Font(None, 100)
        texto = font.render('You Win!!',True,black)
        screen.blit(texto,(((screen_size)//2)-150,(screen_size)//2))
        replay_button = replay((screen_size//2)-150,(screen_size//2)+200)

        # Añadir botón de menú principal
        menu_button = main_menu_button((screen_size//2)+50, (screen_size//2)+200)
    
        if event.type == pygame.MOUSEBUTTONDOWN:
         mouse_pos = pygame.mouse.get_pos()
         if replay_button.collidepoint(mouse_pos):
          main()
          return
         elif menu_button and menu_button.collidepoint(mouse_pos):
          main()
          return
        pygame.display.flip()
   pygame.display.flip()
 pygame.quit()

if __name__ == "__main__":
    main()