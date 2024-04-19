# Importar biblioteca random
import random
import sys
import os

# Agregar el directorio padre al path para permitir importaciones relativas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from LogicTTY.crear_tablero_logica import TableroBarcos, FilasColumasCeroError, BarcoFueraTableroError
from LogicTTY.disparar_logica import Disparar, CoordenadasFueraRangoError, CoordenadasValorIncorrecto, CoordenadasNegativas
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window


class InterfazScreen(Screen):
    pass


class Interfaz(GridLayout):
    def __init__(self, **kwargs):
        super(Interfaz, self).__init__(**kwargs)
        self.cols = 2

        titulo_label = Label(text="BIENVENIDOS AL JUEGO TTY", font_size=80, color=(0, 0.5, 1, 1), halign="center", valign="middle")
        self.add_widget(titulo_label)

        # Agregamos un Label para mostrar mensajes de error en la parte inferior
        self.error_label = Label(text="", color=(1, 0, 0, 1), size_hint_y=None, height=100, font_size=20)
        self.add_widget(self.error_label)

        self.add_widget(Label(text="Número de barcos:", font_size=50))
        self.num_barcos_input = TextInput(multiline=False)
        self.add_widget(self.num_barcos_input)

        self.generate_button = Button(text="Generar Tablero", font_size=50)
        self.generate_button.bind(on_press=self.validar_y_generar_tablero)
        self.add_widget(self.generate_button)

    def validar_y_generar_tablero(self, instance):
        num_barcos_text = self.num_barcos_input.text

        # Verificar si el número de barcos ingresado es un número entero
        if not num_barcos_text.isdigit():
            self.error_label.text = "Error: El número de barcos debe ser un valor entero, verifique si esta ingresando correctamente el número, no se recibe ningun otro tipo de dato."
            return

        num_barcos = int(num_barcos_text)

        # Verificar si el número de barcos es válido
        if num_barcos <= 0:
            self.error_label.text = "Error: El número de barcos debe ser mayor que cero."
            return

        # Generar una lista de tamaños de barcos, cada uno de tamaño 1
        tamanos_barcos = [1] * num_barcos

        # Generar un tablero de 5x5 por defecto
        filas = random.randint(1, 5)
        columnas = random.randint(1, 5)
        tablero_barcos = TableroBarcos(filas, columnas)

        try:
            # Colocar los barcos aleatorios
            tablero_barcos.colocar_barcos_aleatorios(tamanos_barcos)
        except FilasColumasCeroError as e:
            self.error_label.text = f"Error: {e}"
            return
        except BarcoFueraTableroError as e:
            self.error_label.text = f"Error: {e}"
            return

        # Actualizar el tablero en la pantalla correspondiente
        tablero_oculto = tablero_barcos.mostrar_tablero_oculto()
        app = App.get_running_app()
        app.tablero_screen.update_tablero(tablero_oculto)
        app.tablero_screen.tablero_barcos = tablero_barcos  # Actualizamos el tablero en la pantalla del juego
        app.root.current = "tablero"


class TableroScreen(Screen):
    def __init__(self, **kwargs):
        super(TableroScreen, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=5)
        self.tablero_barcos = None
        self.botones_tablero = {}
        self.add_widget(self.layout)

    def update_tablero(self, tablero_oculto):
        self.layout.clear_widgets()

        grid_layout = GridLayout(cols=len(tablero_oculto[0]), rows=len(tablero_oculto))

        self.botones_tablero.clear()

        for fila_index, fila in enumerate(tablero_oculto):
            for columna_index, valor_celda in enumerate(fila):
                button = Button(text=valor_celda, size_hint=(None, None), size=(50, 50))
                posicion = (fila_index, columna_index)
                button.posicion = posicion
                button.bind(on_press=self.on_button_press)
                grid_layout.add_widget(button)
                self.botones_tablero[posicion] = button

        self.layout.add_widget(grid_layout)

    def on_button_press(self, instance):
        fila, columna = instance.posicion
        button = self.botones_tablero[(fila, columna)]

        # Verificar si el tablero está inicializado
        if self.tablero_barcos is not None:
            # Realiza el disparo con el tablero correcto
            disparo = Disparar(fila, columna, self.tablero_barcos)
            resultado_disparo = disparo.shoot()

            # Actualiza visualmente el botón según el resultado del disparo
            if resultado_disparo:
                # Si el disparo fue un acierto, deshabilita el botón y reemplaza su texto con '*'
                button.disabled = True
                button.text = '*'
            else:
                # Si el disparo fue un fallo, reemplaza el texto del botón con 'X'
                button.text = 'X'

            # Verifica si todos los barcos han sido destruidos
            if self.tablero_barcos.game_over():
                print("¡Todos los barcos han sido destruidos!")


class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.interfaz_screen = InterfazScreen(name="interfaz")
        self.tablero_screen = TableroScreen(name="tablero")

        self.interfaz_screen.add_widget(Interfaz())

        self.screen_manager.add_widget(self.interfaz_screen)
        self.screen_manager.add_widget(self.tablero_screen)

        self.screen_manager.current = "interfaz"

        return self.screen_manager


if __name__ == "__main__":
    MyApp().run()