import random
import sys
import os

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
from kivy.uix.popup import Popup


class InterfazScreen(Screen):
    pass


class Interfaz(GridLayout):
    def __init__(self, **kwargs):
        super(Interfaz, self).__init__(**kwargs)
        self.cols = 2

        titulo_label = Label(text="BIENVENIDOS AL JUEGO TTY", font_size=80, color=(0, 0.5, 1, 1), halign="center", valign="middle")
        self.add_widget(titulo_label)

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

        if not num_barcos_text.isdigit():
            self.error_label.text = "Error: El número de barcos debe ser un valor entero."
            return

        num_barcos = int(num_barcos_text)

        if num_barcos <= 0:
            self.error_label.text = "Error: El número de barcos debe ser mayor que cero."
            return

        tamanos_barcos = [1] * num_barcos

        filas = random.randint(1, 5)
        columnas = random.randint(1, 5)
        tablero_barcos = TableroBarcos(filas, columnas)

        try:
            tablero_barcos.colocar_barcos_aleatorios(tamanos_barcos)
        except (FilasColumasCeroError, BarcoFueraTableroError) as e:
            self.error_label.text = f"Error: {e}"
            return

        tablero_oculto = tablero_barcos.mostrar_tablero_oculto()
        app = App.get_running_app()
        app.tablero_screen.update_tablero(tablero_oculto)
        app.tablero_screen.tablero_barcos = tablero_barcos
        app.root.current = "tablero"


class TableroScreen(Screen):
    def __init__(self, **kwargs):
        super(TableroScreen, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=5)
        self.tablero_barcos = None
        self.botones_tablero = {}
        self.posiciones_barcos = []  # Variable para almacenar las posiciones de los barcos
        self.add_widget(self.layout)

    def update_tablero(self, tablero_oculto):
        self.layout.clear_widgets()

        grid_layout = GridLayout(cols=len(tablero_oculto[0]), rows=len(tablero_oculto))

        self.botones_tablero.clear()

        for fila_index, fila in enumerate(tablero_oculto):
            for columna_index, valor_celda in enumerate(fila):
                # Si el valor de la celda es 'X', establece el texto del botón como 'X' y deshabilita el botón
                # Si el valor de la celda es 'O', establece el texto del botón como '*' y habilita el botón
                button = Button(text='O' if valor_celda == 'X' else 'O', disabled=valor_celda == 'X', size_hint=(None, None), size=(50, 50))
                posicion = (fila_index, columna_index)
                button.posicion = posicion
                button.bind(on_press=self.on_button_press)
                grid_layout.add_widget(button)
                self.botones_tablero[posicion] = button

        self.layout.add_widget(grid_layout)

    def on_button_press(self, instance):
        fila, columna = instance.posicion
        button = self.botones_tablero[(fila, columna)]

        if self.tablero_barcos is not None:
            # Verificar si la casilla en el tablero oculto es 'O'
            if self.tablero_barcos.tablero[fila][columna] == 'X':
                resultado_disparo = True  # Simulamos el resultado del disparo
                if resultado_disparo:
                    button.disabled = True
                    button.text = '*'  # Cambiar el texto del botón a '*' si se acierta al disparar
                    print("Barco tumbado")  # Mensaje de barco tumbado
                else:
                    button.text = 'X'  # Cambiar el texto del botón a 'X' si se falla al disparar

                if self.todos_barcos_destruidos():
                    print("¡Todos los barcos han sido destruidos!")
                    self.end_game()  # Llamar a la función para terminar el juego
            else:
                # Si la casilla ya ha sido disparada, mostrar un mensaje
                print("Esta casilla ya ha sido disparada, elige otra.")

    def todos_barcos_destruidos(self):
        for fila in self.tablero_barcos.tablero:
            for celda in fila:
                if celda == 'X':
                    # Verificar si hay alguna celda con valor 'X' que no haya sido disparada
                    fila_index, columna_index = self.tablero_barcos.tablero.index(fila), fila.index(celda)
                    if self.botones_tablero[(fila_index, columna_index)].text != '*':
                        return False
        return True

    def end_game(self):
        # Implementa lo que quieras hacer al finalizar el juego, como mostrar un mensaje de victoria
        popup = Popup(title='Fin del juego', content=Label(text='¡Todos los barcos han sido destruidos!'), size_hint=(None, None), size=(400, 200))
        popup.open()
                
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