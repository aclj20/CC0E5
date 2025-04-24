from bloom_filter_test_books import *
# Clase para implementar un count-min sketch con una sola "banca" de contadores
class CountMinSketch:
    def __init__(self, num_counters):
        self.m = num_counters
        self.hash_fun_rep = get_random_hash_function()
        self.counters = [0] * self.m

    def increment(self, word):
        idx = hash_string(self.hash_fun_rep, word) % self.m
        self.counters[idx] += 1

    def approximateCount(self, word):
        idx = hash_string(self.hash_fun_rep, word) % self.m
        return self.counters[idx]
    
    def initialize_k_counters(k, m): 
        return [CountMinSketch(m) for _ in range(k)]

    def increment_counters(count_min_sketches, word):
        for cms in count_min_sketches:
            cms.increment(word)

    def approximate_count(count_min_sketches, word):
        return min([cms.approximateCount(word) for cms in count_min_sketches])

class BloomFilter:
    def __init__(self, nbits, nhash):
        self.bits = [False] * nbits  # Inicializar todos los bits a False
        self.m = nbits
        self.k = nhash
        # Obtener k funciones hash aleatorias
        self.hash_fun_reps = [get_random_hash_function() for i in range(self.k)]
    
    # Función para insertar una palabra en el filtro Bloom.
    def insert(self, word):
         for hrep in self.hash_fun_reps:
            # obtenemos un entero a partir de la palabra
            idx = hash_string(hrep, word) % self.m
            self.bits[idx] = True
    # Verificar si una palabra pertenece al filtro Bloom
    def member(self, word):
        for hrep in self.hash_fun_reps:
            idx = hash_string(hrep, word) % self.m
            if not self.bits[idx]:
                return False
        return True
    

    # Realizar el conteo exacto
# Es una medida de lo optimizadas que están las estructuras de datos de Python internamente, ya que esta operación termina muy rápidamente.
all_words_gg = set(longer_words_gg)
exact_common_wc = 0
for word in longer_words_wp:
    if word in all_words_gg:
        exact_common_wc += 1
print(f'Conteo exacto de palabras comunes = {exact_common_wc}')

# Intentemos usar lo mismo con un filtro Bloom.
bf = BloomFilter(100000, 5)
for word in longer_words_gg:
    bf.insert(word)
    
for word in longer_words_gg:
    assert bf.member(word), f'La palabra: {word} debería pertenecer'

common_word_count = 0
for word in longer_words_wp:
    if bf.member(word):
        common_word_count += 1
print(f'El número de palabras comunes de longitud >= 5 es: {common_word_count}')
assert common_word_count >= exact_common_wc
print('Todas las pruebas superadas: 10 puntos')