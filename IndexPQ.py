
#
#   CLASE INDEXPQ
#   -------------
#   Implementación de una cola con prioridades variables mediante el uso de montículos
#   binarios. Tiene los siguientes atributos:
#   · n = número de nodos/elementos que puede contener la cola
#   · array = lista que contiene los elementos de la cola
#   · positions = lista que contiene para un elemento con count c, en qué posición está en
#                 array. 0 si no está
#

class IndexPQ:

    # Constructor:
    def __init__(self, n):
        # Número de elementos en la cola
        self.n = n
        # Vector que contiene las tuplas (elem,prioridad)
        self.array = [-1]
        # Vector que contiene las posiciones en el array de elementos
        self.positions = [0] * n

    # MÉTODOS PRIVADOS
    # ----------------

    # Tamaño de la cola
    def size(self):
        return len(self.array) - 1

    # Método flotar, para reestructurar el montículo binario
    # Sube (flota) el último nodo hoja hasta su posición correcta en el árbol
    def float(self, i):
        elem = self.array[i]
        hole = i
        while hole != 1 and self.prior(elem, self.array[int(hole//2)]):
            self.array[hole] = self.array[int(hole//2)]
            self.positions[self.array[hole][2]] = hole
            hole = int(hole//2)
        self.array[hole] = elem
        self.positions[self.array[hole][2]] = hole

    # Método hundir, para reestructurar el montículo binario
    # Baja (hunde) el nodo raíz hasta su posición correcta en el árbol
    def sink(self, i):
        elem = self.array[i]
        hole = i
        child = 2 * hole
        while child <= self.size():
            if child < self.size() and self.prior(self.array[child+1], self.array[child]):
                child += 1
            elif self.prior(self.array[child], elem):
                self.array[hole] = self.array[child]
                self.positions[self.array[hole][2]] = hole
                hole = child
                child = 2 * hole
            else:
                break
        self.array[hole] = elem
        self.positions[self.array[hole][2]] = hole

    # Comparador que establece la prioridad de los elementos en la cola
    @staticmethod
    def prior(e1, e2):
        return e1[0] < e2[0] or e1[0] == e2[0] and e1[2] < e2[2]

    # MÉTODOS PÚBLICOS
    # ----------------

    # Inserta el elemento {f_score, node, count} en la cola
    def put(self, priority, node, count):
        self.array.append([priority, node, count])
        self.positions[count] = self.size()
        self.float(self.size())

    # Actualiza la prioridad del nodo con count <count>
    def update(self, count, priority):
        i = self.positions[count]
        self.array[i][0] = priority
        if i != 1 and self.prior(self.array[i], self.array[int(i//2)]):
            self.float(i)
        else:
            self.sink(i)

    # ¿Está vacía la cola?
    def empty(self):
        return self.size() == 0

    # Devuelve el elemento más prioritario de la cola
    def top(self):
        return self.array[1]

    # Elimina el elemento más prioritario de la cola
    def pop(self):
        self.positions[self.array[1][2]] = 0
        if self.size() > 1:
            self.array[1] = self.array[-1]
            self.positions[self.array[1][2]] = 1
            self.array.pop(-1)
            self.sink(1)
        else:
            self.array.pop(-1)
