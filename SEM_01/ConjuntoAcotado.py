class ConjuntoAcotado1:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.arregloBooleano = [False] * (b - a + 1)

    def insertar (self, elemento):
        if self.a <= elemento <= self.b: #O(1)
            self.arregloBooleano [elemento - self.a] = True #O(1)
        #En el mejor y peor caso tiene complejidad O(1)

    def eliminar(self, elemento):
        if self.a <= elemento <= self.b:
            self.arregloBooleano [elemento - self.a]= False

    def contiene(self, elemento):
        return self.a <= elemento <= self.b and self.arregloBooleano [elemento - self.a]

    def union(self, otroConjunto):
        nuevo = ConjuntoAcotado1(self.a, self.b)
        #Recorre ambas listas O(n)
        nuevo.arr = [a or b for a, b in zip(self.arr, otroConjunto.arr)]
        return nuevo

    def interseccion(self, otro):
        nuevo = ConjuntoAcotado1(self.a, self.b)
        nuevo.arr = [a and b for a, b in zip(self.arr, otro.arr)]
        return nuevo

class ConjuntoAcotadoHash:
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.conjunto = set()

    def insertar(self, x):
        if self.a <= x <= self.b:
            self.conjunto.add(x)

    def eliminar(self, x):
        self.conjunto.discard(x)

    def contiene(self, x):
        return x in self.conjunto

    def union(self, otro):
        nuevo = ConjuntoAcotadoHash(self.a, self.b)
        nuevo.conjunto = self.conjunto | otro.conjunto
        return nuevo

    def interseccion(self, otro):
        nuevo = ConjuntoAcotadoHash(self.a, self.b)
        nuevo.conjunto = self.conjunto & otro.conjunto
        return nuevo

#Implementacion Arbol Balanceado
class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class AVL:
    def insertar(self, raiz, valor):
        if not raiz:
            return NodoAVL(valor)
        elif valor < raiz.valor:
            raiz.izquierda = self.insertar(raiz.izquierda, valor)
        else:
            raiz.derecha = self.insertar(raiz.derecha, valor)
        
        raiz.altura = 1 + max(self.obtener_altura(raiz.izquierda), self.obtener_altura(raiz.derecha))
        return self.balancear(raiz)
    
    def eliminar(self, raiz, valor):
        if not raiz:
            return raiz
        
        if valor < raiz.valor:
            raiz.izquierda = self.eliminar(raiz.izquierda, valor)
        elif valor > raiz.valor:
            raiz.derecha = self.eliminar(raiz.derecha, valor)
        else:
            if not raiz.izquierda:
                return raiz.derecha
            elif not raiz.derecha:
                return raiz.izquierda
            temp = self.min_valor_nodo(raiz.derecha)
            raiz.valor = temp.valor
            raiz.derecha = self.eliminar(raiz.derecha, temp.valor)
        
        raiz.altura = 1 + max(self.obtener_altura(raiz.izquierda), self.obtener_altura(raiz.derecha))
        return self.balancear(raiz)
    
    def balancear(self, raiz):
        balance = self.obtener_balance(raiz)
        if balance > 1 and self.obtener_balance(raiz.izquierda) >= 0:
            return self.rotar_derecha(raiz)
        if balance < -1 and self.obtener_balance(raiz.derecha) <= 0:
            return self.rotar_izquierda(raiz)
        if balance > 1 and self.obtener_balance(raiz.izquierda) < 0:
            raiz.izquierda = self.rotar_izquierda(raiz.izquierda)
            return self.rotar_derecha(raiz)
        if balance < -1 and self.obtener_balance(raiz.derecha) > 0:
            raiz.derecha = self.rotar_derecha(raiz.derecha)
            return self.rotar_izquierda(raiz)
        return raiz

    def obtener_altura(self, nodo):
        return nodo.altura if nodo else 0

    def obtener_balance(self, nodo):
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha) if nodo else 0

    def rotar_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        y.derecha = z
        z.izquierda = T3
        z.altura = 1 + max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))
        return y

    def rotar_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda
        y.izquierda = z
        z.derecha = T2
        z.altura = 1 + max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))
        return y
    
    def min_valor_nodo(self, nodo):
        actual = nodo
        while actual.izquierda:
            actual = actual.izquierda
        return actual
    
    def contiene(self, raiz, valor):
        if not raiz:
            return False
        if valor == raiz.valor:
            return True
        elif valor < raiz.valor:
            return self.contiene(raiz.izquierda, valor)
        else:
            return self.contiene(raiz.derecha, valor)

class ConjuntoAcotadoAVL:
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.arbol = None
        self.avl = AVL()

    def insertar(self, x):
        if self.a <= x <= self.b:
            #Siempre se necesita balancear O(logn)
            self.arbol = self.avl.insertar(self.arbol, x)
    
    def eliminar(self, x):
        self.arbol = self.avl.eliminar(self.arbol, x)
    
    def contiene(self, x):
        return self.avl.contiene(self.arbol, x)
    
    def union(self, otro):
        nuevo = ConjuntoAcotadoAVL(self.a, self.b)
        def recorrer(nodo):
            if nodo:
                nuevo.insertar(nodo.valor)
                recorrer(nodo.izquierda)
                recorrer(nodo.derecha)
        recorrer(self.arbol)
        recorrer(otro.arbol)
        return nuevo
    
    def interseccion(self, otro):
        nuevo = ConjuntoAcotadoAVL(self.a, self.b)
        def recorrer(nodo):
            if nodo and otro.contiene(nodo.valor):
                nuevo.insertar(nodo.valor)
                recorrer(nodo.izquierda)
                recorrer(nodo.derecha)
        recorrer(self.arbol)
        return nuevo