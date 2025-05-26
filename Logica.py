import random
import numpy as np

def es_valido(sudoku, fila, columna, num):
 # Verificar si el número no está ya en la fila
 if num in sudoku[fila]:
     return False
 
 # Verificar si el número no está ya en la columna
 for i in range(9):
     if sudoku[i][columna] == num:
        return False
 
 # Verificar si el número no está ya en el subcuadro 3x3
 inicio_fila = (fila // 3) * 3
 inicio_columna = (columna // 3) * 3
 for i in range(3):
     for j in range(3):
         if sudoku[inicio_fila + i][inicio_columna + j] == num:
             return False
 return True

def llenar_sudoku(sudoku):
 for fila in range(9):
     for columna in range(9):
         if sudoku[fila][columna] == 0:  # Buscar una celda vacía
             for num in range(1, 10):  # Probar números del 1 al 9
                 if es_valido(sudoku, fila, columna, num):
                     sudoku[fila][columna] = num  # Colocar número
                     if llenar_sudoku(sudoku):  # Intentar llenar el resto
                         return True
                     sudoku[fila][columna] = 0  # Si falla, revertir la colocación
             return False  # Si no se puede colocar ningún número, retorna falso
 return True  # Si se llena completamente, retornar verdadero
