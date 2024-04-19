from LogicTTY.crear_tablero_logica import TableroBarcos

# Definir excepciones personalizadas
class CoordenadasFueraRangoError(IndexError):
    pass

class CoordenadasValorIncorrecto(ValueError):
    pass

class CoordenadasNegativas(Exception):
    pass

class ErrorMasDeDosCoordenadas(Exception):
    pass

class Disparar:
    def __init__(self, x, y, tablero: TableroBarcos):
        self.coordenadaX = x
        self.coordenadaY = y
        self.tablero = tablero
        # Inicializar las coordenadas del último disparo en None
        self.ultimoDisparoX = None
        self.ultimoDisparoY = None

    def shoot(self):
        # Actualizar las coordenadas del último disparo
        self.tablero.ultimoDisparoX = self.coordenadaX
        self.tablero.ultimoDisparoY = self.coordenadaY

        # Validar las coordenadas del disparo
        self.validar_coordenadas()

        # Realizar el disparo y actualizar el tablero
        if self.check_impact():
            self.tablero.tablero[self.coordenadaX][self.coordenadaY] = '*'
            if self.game_over():
                return None
            return True
        else:
            if self.game_over():
                return None
            return False

    def validar_coordenadas(self):
        # Convertir las coordenadas a enteros si son flotantes
        if isinstance(self.coordenadaX, float):
            self.coordenadaX = int(self.coordenadaX)
          
        if isinstance(self.coordenadaY, float):
            self.coordenadaY = int(self.coordenadaY)

        # Validar que las coordenadas sean enteros
        if not isinstance(self.coordenadaX, int) or not isinstance(self.coordenadaY, int):
            raise CoordenadasValorIncorrecto

        # Validar que las coordenadas no sean negativas
        if self.coordenadaX < 0 or self.coordenadaY < 0:
            raise CoordenadasNegativas()

        # Validar que las coordenadas estén dentro del rango del tablero
        if self.coordenadaX >= len(self.tablero.tablero) or self.coordenadaY >= len(self.tablero.tablero[self.coordenadaX]):
            raise CoordenadasFueraRangoError

    def check_impact(self):
        if self.tablero.tablero[self.coordenadaX][self.coordenadaY] == 'O':
            return False
        if self.tablero.tablero[self.coordenadaX][self.coordenadaY] == 'X':
            self.tablero.tablero[self.coordenadaX][self.coordenadaY] = 'X*'  # Marcar como impactado en el tablero
            return True

    def game_over(self):
        return not any('X' in fila for fila in self.tablero.tablero)