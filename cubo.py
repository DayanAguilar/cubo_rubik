from random import randint, choice


class Cubo:
    def __init__(self, colores=["w", "o", "g", "r", "b", "y"], estado=None):
        """Inicia el cubo
        -colores: son los colores que estan permitidos que son:
            -w: white(blanco)
            -o: orange(naranja)
            -g: green(verde)
            -r: red(rojo)
            -b: blue(azul)
            -y: yellow(amarillo)
        -estado: esta se pasa cuando ya existe un cubo es decir cuando ya existe el
         cubo y si no se pasa el cubo se genera con el estado que ya esta [RESUELTO].
        """
        if estado is None:
            self.n = 3
            self.colores = colores
            self.iniciar()
        else:
            self.n = int((len(estado) / 6) ** (0.5))
            self.colores = []
            self.cubo = [[[]]]
            for i, s in enumerate(estado):
                if s not in self.colores:
                    self.colores.append(s)
                self.cubo[-1][-1].append(s)
                if len(self.cubo[-1][-1]) == self.n and len(self.cubo[-1]) < self.n:
                    self.cubo[-1].append([])
                elif (
                    len(self.cubo[-1][-1]) == self.n
                    and len(self.cubo[-1]) == self.n
                    and i < len(estado) - 1
                ):
                    self.cubo.append([[]])

    def iniciar(self):
        """Genera un cubo rubik que este resuelto en su [ESTADO_INICIAL]"""
        self.cubo = [
            [[c for x in range(self.n)] for y in range(self.n)] for c in self.colores
        ]

    def resuelto(self):
        """Revisa si el cubo esta resuelto viendo si los visitados es decir si las caras no coinciden
        si no coinciden estas se agregan a visitados si esta pasa de una longitud de 1 no esta resuelto."""
        for lado in self.cubo:
            visitados = []
            resuelto = True
            for fila in lado:
                if len(set(fila)) == 1:
                    visitados.append(fila[0])
                else:
                    resuelto = False
                    break
            if resuelto == False:
                break
            if len(set(visitados)) > 1:
                resuelto = False
                break
        return resuelto

    def to_string(self):
        """Convierte el self.cubo en una linea de caracteres para su uso."""
        return "".join([i for r in self.cubo for s in r for i in s])

    def mezclar(self, movimientos=5):
        """Mezcla el cubo con los movimients posibles
        -movimientos: son los movimientos que se pueden realizar por [DEFAULT] estan en 5.
        """
        moves = randint(0, movimientos)
        actions = [("h", 0), ("h", 1), ("v", 0), ("v", 1), ("s", 0), ("s", 1)]
        for i in range(moves):
            a = choice(actions)
            j = randint(0, self.n - 1)
            if a[0] == "h":
                self.giro_horizontal(j, a[1])
            elif a[0] == "v":
                self.giro_vertical(j, a[1])
            elif a[0] == "s":
                self.giro_profundo(j, a[1])

    def mostrar(self):
        """Muestra el cubo rubik con 3 lineas de matrices
        -Primera linea de matriz:
            -muestra la cara de arriba: U.
        -Segunda linea de matrices:
            -primera matriz es la cara de la izquierda: L.
            -segunda matriz es la cara de el frente: F.
            -tercera matriz es la cara de la derecha: R.
            -cuarta matriz es la cara de atras: B
        -Tercera linea de matriz:
            -muestra la cara de abajo: D.
        """
        spacing = f'{" " * (len(str(self.cubo[0][0])) + 2)}'
        l1 = "\n".join(spacing + str(c) for c in self.cubo[0])
        l2 = "\n".join(
            "  ".join(str(self.cubo[i][j]) for i in range(1, 5))
            for j in range(len(self.cubo[0]))
        )
        l3 = "\n".join(spacing + str(c) for c in self.cubo[5])
        print(f"{l1}\n\n{l2}\n\n{l3}")

    def giro_horizontal(self, fila, direccion):
        """
        Gira de manera horizontal el cubo solo afecta a las caras L,F,R,B.
        --fila: es la fila que se escoge se puede escoger entre 0 y 2
        --direccion: recibe 0 y 1
            -0: Gira hacia la izquierda.
            -1: Gira hacia la derecha.
        """
        if fila < len(self.cubo[0]):
            if direccion == 0:
                (
                    self.cubo[1][fila],
                    self.cubo[2][fila],
                    self.cubo[3][fila],
                    self.cubo[4][fila],
                ) = (
                    self.cubo[2][fila],
                    self.cubo[3][fila],
                    self.cubo[4][fila],
                    self.cubo[1][fila],
                )

            elif direccion == 1:
                (
                    self.cubo[1][fila],
                    self.cubo[2][fila],
                    self.cubo[3][fila],
                    self.cubo[4][fila],
                ) = (
                    self.cubo[4][fila],
                    self.cubo[1][fila],
                    self.cubo[2][fila],
                    self.cubo[3][fila],
                )
            else:
                print(f"ERROR - la direccion debe ser 0(izquierda) y 1(derecha)")
                return

            if direccion == 0:
                if fila == 0:
                    self.cubo[0] = [
                        list(x) for x in zip(*reversed(self.cubo[0]))
                    ]  # Hacer la traspuesta de la cara U
                elif fila == len(self.cubo[0]) - 1:
                    self.cubo[5] = [
                        list(x) for x in zip(*reversed(self.cubo[5]))
                    ]  # Hacer la traspuesta de la cara D
            elif direccion == 1:
                if fila == 0:
                    self.cubo[0] = [list(x) for x in zip(*self.cubo[0])][
                        ::-1
                    ]  # Hacer la traspuesta de la cara U
                elif fila == len(self.cubo[0]) - 1:
                    self.cubo[5] = [list(x) for x in zip(*self.cubo[5])][
                        ::-1
                    ]  # Hacer la traspuesta de la cara D
        else:
            print(f"ERROR - La fila debe ser entre 0-{len(self.cubo[0]) - 1}")
            return

    def giro_vertical(self, columna, direccion):
        """
        Gira de manera vertical el cubo solo afecta a las caras F, U, D.
        --columna: la columna que se quiere girar entre 0 y 2
        --direccion: entre 0 y 1
            -0: Gira hacia abajo.
            -1: Gira hacia arriba.
        """
        if columna < len(self.cubo[0]):
            for i in range(len(self.cubo[0])):
                if direccion == 0:
                    (
                        self.cubo[0][i][columna],
                        self.cubo[2][i][columna],
                        self.cubo[4][-i - 1][-columna - 1],
                        self.cubo[5][i][columna],
                    ) = (
                        self.cubo[4][-i - 1][-columna - 1],
                        self.cubo[0][i][columna],
                        self.cubo[5][i][columna],
                        self.cubo[2][i][columna],
                    )
                elif direccion == 1:
                    (
                        self.cubo[0][i][columna],
                        self.cubo[2][i][columna],
                        self.cubo[4][-i - 1][-columna - 1],
                        self.cubo[5][i][columna],
                    ) = (
                        self.cubo[2][i][columna],
                        self.cubo[5][i][columna],
                        self.cubo[0][i][columna],
                        self.cubo[4][-i - 1][-columna - 1],
                    )
                else:
                    print(f"ERROR - la direccion debe ser 0 (abajo) o 1 (arriba)")
                    return
            if direccion == 0:
                if columna == 0:
                    self.cubo[1] = [list(x) for x in zip(*self.cubo[1])][
                        ::-1
                    ]  # Hacer la traspuesta de la cara L
                elif columna == len(self.cubo[0]) - 1:
                    self.cubo[3] = [list(x) for x in zip(*self.cubo[3])][
                        ::-1
                    ]  # Hacer la traspuesta de la cara R
            elif direccion == 1:
                if columna == 0:
                    self.cubo[1] = [
                        list(x) for x in zip(*reversed(self.cubo[1]))
                    ]  # Hacer la traspuesta de la cara L
                elif columna == len(self.cubo[0]) - 1:
                    self.cubo[3] = [
                        list(x) for x in zip(*reversed(self.cubo[3]))
                    ]  # Hacer la traspuesta de la cara R
        else:
            print(f"ERROR - La columna debe estar entre 0-{len(self.cubo[0]) - 1}")
            return

    def giro_profundo(self, columna, direccion):
        """
        Gira de manera profunda el cubo empezando de la cara B que es de color [BLUE] solo afecta
        a las caras L, R, U, D.
        --columna: La columna iniciando desde la cara B es decir el 0 es la primera columna contando desde la cara B
        --direccion entre 0 y 1
            -0: Gira abajo la cara
            -1: Gira arriba la cara
        """
        if columna < len(self.cubo[0]):
            for i in range(len(self.cubo[0])):
                if direccion == 0:
                    (
                        self.cubo[0][columna][i],
                        self.cubo[1][-i - 1][columna],
                        self.cubo[3][i][-columna - 1],
                        self.cubo[5][-columna - 1][-1 - i],
                    ) = (
                        self.cubo[3][i][-columna - 1],
                        self.cubo[0][columna][i],
                        self.cubo[5][-columna - 1][-1 - i],
                        self.cubo[1][-i - 1][columna],
                    )
                elif direccion == 1:
                    (
                        self.cubo[0][columna][i],
                        self.cubo[1][-i - 1][columna],
                        self.cubo[3][i][-columna - 1],
                        self.cubo[5][-columna - 1][-1 - i],
                    ) = (
                        self.cubo[1][-i - 1][columna],
                        self.cubo[5][-columna - 1][-1 - i],
                        self.cubo[0][columna][i],
                        self.cubo[3][i][-columna - 1],
                    )
                else:
                    print(f"ERROR - la direccion debe ser 0 (abajo) o 1 (arriba)")
                    return
            if direccion == 0:
                if columna == 0:
                    self.cubo[4] = [
                        list(x) for x in zip(*reversed(self.cubo[4]))
                    ]  # Hacer la traspuesta de la cara B
                elif columna == len(self.cubo[0]) - 1:
                    self.cubo[2] = [
                        list(x) for x in zip(*reversed(self.cubo[2]))
                    ]  # Hacer la traspuesta de la cara F
            elif direccion == 1:
                if columna == 0:
                    self.cubo[4] = [list(x) for x in zip(*self.cubo[4])][
                        ::-1
                    ]  # Hacer la traspuesta de la cara B
                elif columna == len(self.cubo[0]) - 1:
                    self.cubo[2] = [list(x) for x in zip(*self.cubo[2])][
                        ::-1
                    ]  # Hacer la traspuesta de la cara F
        else:
            print(f"ERROR - La columna debe estar entre: 0-{len(self.cubo[0]) - 1}")
            return
