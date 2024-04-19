    fila, columna = instance.posicion
        button = self.botones_tablero[(fila, columna)]

        if self.tablero_barcos is not None:
            # Verificar si la casilla en el tablero oculto es 'O'
            if self.tablero_barcos.tablero[fila][columna] == 'O':
                disparo = Disparar(fila, columna, self.tablero_barcos)
                resultado_disparo = disparo.shoot()

                if resultado_disparo:
                    button.disabled = True
                    button.text = '*'  # Cambiar el texto del botón a '*' si se acierta al disparar
                else:
                    button.text = 'X'  # Cambiar el texto del botón a 'X' si se falla al disparar

                if self.tablero_barcos.todos_barcos_destruidos():
                    print("¡Todos los barcos han sido destruidos!")
            else:
                # Si la casilla ya ha sido disparada, mostrar un mensaje
                print("Esta casilla ya ha sido disparada, elige otra.")
        
        # Deshabilitar el botón después de hacer clic
        button.disabled = True