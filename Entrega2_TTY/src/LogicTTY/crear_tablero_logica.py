# Importar biblioteca random
import random

# Error si la fila o columna ingresada es cero
class FilasColumasCeroError(IndexError):
    pass

# Error si el barco está fuera de los límites
class BarcoFueraTableroError(ValueError):
    pass

# Error si el usuario entra un caracter diferente a un entero
class DatoStrError(Exception):
    pass

# Clase principal que representa el tablero de barcos
class TableroBarcos:
    """
    Inicia el tablero de barcos con las dimensiones dadas.

    Parámetros:
    - filas: Número de filas del tablero.
    - columnas: Número de columnas del tablero.
    """
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.validar_tamaño()  # Llama a la validación de tamaño en la inicialización
        self.tablero = self.crear_tablero()
        self.posiciones_barcos = []

    """
    Valida las coordenadas, el tamaño y la dirección del barco antes de colocarlo en el tablero.

    Parámetros:
    - fila: Fila en la que se intenta colocar el barco.
    - columna: Columna en la que se intenta colocar el barco.
    - tamano: Tamaño del barco.
    - direccion: Dirección del barco ('horizontal' o 'vertical').

    Raises:
    - ValueError: Se lanza si las coordenadas están fuera del tablero,
    si el tamaño de la nave no es válido, o si la dirección no es válida,
    o si el barco no cabe en la dirección horizontal.
    """
    def validar_entrada(self, fila, columna, tamano, direccion):
        if not (0 <= fila < self.filas and 0 <= columna < self.columnas):
            raise ValueError("Las coordenadas están fuera del tablero.")

        if not self.validar_tamano_nave(tamano):
            raise ValueError("Tamaño de nave no válido. Use 1, 2 o 4.")

        if not self.validar_direccion(direccion):
            raise ValueError("Dirección no válida. Use 'horizontal' o 'vertical'.")

        if direccion == 'horizontal' and columna + tamano > self.columnas:
            raise ValueError("El barco no cabe en la dirección horizontal.")
        
    """
    Coloca un barco en dirección horizontal en el tablero.

    Parámetros:
    - fila: Fila en la que se coloca el barco.
    - columna: Columna inicial en la que se coloca el barco.
    - tamaño: Tamaño del barco.

    Raises:
    - ValueError: Se lanza si el barco no cabe en la dirección horizontal
    o si ya hay otro barco en esa posición.
    
    Returns:
    - barco: Coordenadas y dirección del barco colocado.
    """
    def colocar_barco_horizontal(self, fila, columna, tamano):
        if 0 <= fila < self.filas and 0 <= columna < self.columnas and columna + tamano <= self.columnas:
            for i in range(tamano):
                self.tablero[fila][columna + i] = 'X'
            barco = {"fila": fila, "columna": columna, "tamaño": tamano, "direccion": "horizontal"}
            return barco
        else:
            raise ValueError("Coordenadas o tamaño de barco no válidos.")

    """
    Coloca un barco en dirección vertical en el tablero.

    Parámetros:
    - fila: Fila inicial en la que se coloca el barco.
    - columna: Columna en la que se coloca el barco.
    - tamaño: Tamaño del barco.

    Raises:
    - ValueError: Se lanza si el barco no cabe en la dirección vertical
    o si ya hay otro barco en esa posición.
    
    Returns:
    - barco: Coordenadas y dirección del barco colocado.
    """
    def colocar_barco_vertical(self, fila, columna, tamano):
        if 0 <= fila < self.filas and 0 <= columna < self.columnas and fila + tamano <= self.filas:
            for i in range(tamano):
                self.tablero[fila + i][columna] = 'X'
            barco = {"fila": fila, "columna": columna, "tamaño": tamano, "direccion": "vertical"}
            return barco
        else:
            raise ValueError("Coordenadas o tamaño de barco no válidos.")

    """
    Coloca un barco en dirección vertical en el tablero.

    Parámetros:
    - fila: Fila en la que se coloca el barco.
    - columna: Columna en la que se coloca el barco.
    - tamano: Tamaño del barco.

    Raises:
    - ValueError: Se lanza si las coordenadas o el tamaño del barco no son válidos.
    Se verifica si el barco cabe en la dirección vertical.
    """
    def colocar_barco(self, fila, columna, tamano, direccion):
        if direccion == 'horizontal':
            return self.colocar_barco_horizontal(fila, columna, tamano)
        elif direccion == 'vertical':
            return self.colocar_barco_vertical(fila, columna, tamano)
        else:
            raise ValueError("Dirección no válida. Use 'horizontal' o 'vertical'.")

    """
    Coloca barcos aleatorios en el tablero.

    Parámetros:
    - tamanos_barcos: Lista de tamaños de barcos que se colocarán en el tablero.

    Returns:
    - No devuelve ningún valor, pero actualiza el tablero con los barcos colocados aleatoriamente.
    """
    def colocar_barcos_aleatorios(self, tamanos_barcos):
        for tamano in tamanos_barcos:
            while True:
                fila = random.randint(0, self.filas - 1)
                columna = random.randint(0, self.columnas - 1)
                direccion = random.choice(["horizontal", "vertical"])
                
                try:
                    # Intenta colocar el barco en el tablero
                    self.colocar_barco(fila, columna, tamano, direccion)
                    break
                except ValueError:
                    # Si hay un error al colocar el barco, intenta de nuevo con otras coordenadas
                    continue

    """
    Coloca barcos aleatorios en el tablero para la interfaz.

    Parámetros:
    - num_barcos: El número de barcos que se colocarán en el tablero.

    Returns:
    - No devuelve ningún valor, pero actualiza el tablero con los barcos colocados aleatoriamente.
    """
    def colocar_barcos_aleatorios_interfaz(self, num_barcos):
        for _ in range(num_barcos):
            while True:
                fila = random.randint(0, self.filas - 1)
                columna = random.randint(0, self.columnas - 1)
                if self.tablero[fila][columna] == 'O':
                    self.tablero[fila][columna] = 'X'
                    break

    """
    Crea un tablero con dimensiones especificadas por filas y columnas, lleno de 'O's.

    Returns:
    - tablero: Tablero creado (lista de listas).
    """
    def crear_tablero(self):
        return [['O' for _ in range(self.columnas)] for _ in range(self.filas)]

    """
    Valida que las dimensiones del tablero sean mayores que cero.

    Parametros:
    - No tiene.

    Returns:
    - No tiene.

    Raises:
    - FilasColumasCeroError: Se levanta si las filas o columnas son iguales a cero.
    - BarcoFueraTableroError: Se levanta si las filas o columnas son menores cero.
    """
    def validar_tamaño(self):
        if self.filas <= 0 or self.columnas <= 0:
            raise FilasColumasCeroError("El número de filas y columnas debe ser mayor que cero.")
        if self.columnas < 0:
            raise FilasColumasCeroError("El número de columnas no puede ser negativo.")
    """
    Imprime el tablero en la consola.

    No tiene parámetros.

    Raises:
    No levanta ninguna excepción.

    Returns:
    No devuelve ningún valor.
    """    
    def mostrar_tablero(self):
        for fila in self.tablero:
            print(' '.join(fila))

    """
    Imprime el tablero oculto en la consola y devuelve las posiciones de los barcos.

    No tiene parámetros.

    Raises:
        No levanta ninguna excepción.

    Returns:
        posiciones_barcos (list): Lista de tuplas que contienen las coordenadas de los barcos en el tablero.
    """
    def mostrar_tablero_oculto(self):
        posiciones_barcos = []  

        tablero_oculto_texto = []  # Inicializamos una lista vacía para almacenar el tablero oculto como texto

        for fila_index, fila in enumerate(self.tablero):
            fila_oculta = []  
            for columna_index, valor_celda in enumerate(fila):
                if valor_celda == 'X':
                    posiciones_barcos.append((fila_index, columna_index))
                    fila_oculta.append('O')
                else:
                    fila_oculta.append('O')
            tablero_oculto_texto.append(fila_oculta)  # Agregamos la fila al tablero oculto como texto
        return tablero_oculto_texto
    
    
    def mostrar_tablero_oculto_consola(self):
        posiciones_barcos = []  # Variable para almacenar las posiciones de los barcos

        for fila_index, fila in enumerate(self.tablero):
            fila_oculta = []  # Fila oculta para mostrar 'O' en lugar de posiciones de barcos
            for columna_index, valor_celda in enumerate(fila):
                if valor_celda == 'X':
                    posiciones_barcos.append((fila_index, columna_index))  # Guardar posición del barco
                    fila_oculta.append('O')  # Mostrar 'O' en lugar de la posición del barco
                else:
                    fila_oculta.append('O')  # Mostrar 'O' si no hay barco en la posición
            print(' '.join(fila_oculta))
        return posiciones_barcos