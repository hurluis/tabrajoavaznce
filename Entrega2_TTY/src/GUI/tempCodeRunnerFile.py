    fila, columna = instance.posicion  
        button = self.botones_tablero[(fila, columna)]

        # Verifica si el tablero está inicializado
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