import math
import random
import json

# Función de hash FNV-1 de 32 bits (retorna un entero sin signo)
def fnv1_hash32(key: str) -> int:
    fnv_prime = 0x01000193  # Constante primo FNV
    hash_ = 0x811c9dc5      # Valor inicial offset basis
    for c in key:
        hash_ = (hash_ * fnv_prime) & 0xFFFFFFFF  # Multiplica por el primo y limita a 32 bits
        hash_ ^= ord(c)                            # XOR con el valor ASCII del carácter
    return hash_

# Implementación de MurmurHash3 x86 32 bits
def murmurhash3_32(key: str, seed: int = 0) -> int:
    data = key.encode('utf-8')
    length = len(data)
    nblocks = length // 4

    h1 = seed & 0xFFFFFFFF
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    # Procesamiento de bloques de 4 bytes
    for block_start in range(0, nblocks * 4, 4):
        # Combina 4 bytes en un entero de 32 bits
        k1 = (data[block_start]
              | (data[block_start+1] << 8)
              | (data[block_start+2] << 16)
              | (data[block_start+3] << 24))
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF  # Rotación izquierda de 15 bits
        k1 = (k1 * c2) & 0xFFFFFFFF

        # Mezcla con el hash
        h1 ^= k1
        h1 = ((h1 << 13) | (h1 >> 19)) & 0xFFFFFFFF
        h1 = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF

    # Procesamiento de la cola (últimos bytes)
    tail_index = nblocks * 4
    tail_size = length & 3
    k1 = 0
    if tail_size == 3:
        k1 ^= data[tail_index + 2] << 16
    if tail_size >= 2:
        k1 ^= data[tail_index + 1] << 8
    if tail_size >= 1:
        k1 ^= data[tail_index]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1

    # Finalización (avalancha de bits)
    h1 ^= length
    h1 &= 0xFFFFFFFF
    h1 ^= (h1 >> 16)
    h1  = (h1 * 0x85ebca6b) & 0xFFFFFFFF
    h1 ^= (h1 >> 13)
    h1  = (h1 * 0xc2b2ae35) & 0xFFFFFFFF
    h1 ^= (h1 >> 16)
    return h1

# Serializa valores de forma determinista (JSON ordenado)
def consistent_stringify(value) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False)

class BloomFilter:
    """
    Implementación de un Bloom filter con FNV-1 y MurmurHash3 para hashing múltiple.
    """
    def __init__(self, max_size: int, max_tolerance: float = 0.01, seed: int = None):
        # Validación de parámetros
        if not isinstance(max_size, int) or max_size <= 0:
            raise TypeError(f"maxSize debe ser un entero positivo, recibido: {max_size}")
        try:
            tol = float(max_tolerance)
        except:
            raise TypeError(f"tolerance debe ser un número en (0,1), recibido: {max_tolerance}")
        if tol <= 0 or tol >= 1:
            raise TypeError(f"tolerance debe cumplir 0 < t < 1, recibido: {max_tolerance}")
        if seed is None:
            seed = random.getrandbits(32)  # Semilla aleatoria si no se provee
        if not isinstance(seed, int):
            raise TypeError(f"seed debe ser un entero, recibido: {seed}")

        self._max_size = max_size
        self._seed = seed

        ln2 = math.log(2)
        # Número de bits: m = -n ln p / (ln 2)^2
        self._num_bits = math.ceil(-max_size * math.log(tol) / (ln2**2))
        # Número de hashes: k = (m/n) ln 2  =>  k = -ln p / ln 2
        self._num_hashes = math.ceil(-math.log(tol) / ln2)

        # Prevención de filtros excesivamente grandes
        if self._num_bits > 1_000_000_000:
            raise MemoryError("Demasiada memoria requerida para el Bloom filter")

        num_bytes = math.ceil(self._num_bits / 8)
        self._bits = bytearray(num_bytes)  # Array de bytes para los bits
        self._size = 0                     # Conteo de inserciones únicas
        self.counter = [0]*self._num_bits

    def _bit_coords(self, index: int):
        """Devuelve el índice de byte y el desplazamiento de bit para un índice global."""
        byte_idx = index // 8
        bit_idx = index % 8
        return byte_idx, bit_idx

    def _read_bit(self, index: int) -> int:
        """Lee el valor de un bit (0 o 1)."""
        b, i = self._bit_coords(index)
        return (self._bits[b] >> i) & 1

    def _write_bit(self, index: int) -> bool:
        """Establece un bit a 1. Devuelve True si cambió de estado."""
        b, i = self._bit_coords(index)
        mask = 1 << i
        old = self._bits[b]
        self._bits[b] |= mask
        return old != self._bits[b]

    def _key_positions(self, key: str):
        """Genera las posiciones de bit para una clave usando hashing doble."""
        s = consistent_stringify(key)
        h1 = murmurhash3_32(s, self._seed)
        h2 = fnv1_hash32(s)
        for i in range(self._num_hashes):
            # Combinación lineal de los hashes (double hashing + cuadrática)
            yield (h1 + i * h2 + i * i) % self._num_bits

    def add(self, value) -> "BloomFilter":
        """Añade un valor al filtro. Incrementa _size si algún bit cambió."""
        key = consistent_stringify(value)
        flipped = False
        for pos in self._key_positions(key):
            self.counter[pos]+=1
            if self._write_bit(pos):
                flipped = True
        if flipped:
            self._size += 1
        return self

    def remove(self, value):
        key = consistent_stringify(value)
        
        for pos in self._key_positions(key):
            if self._counters[pos] > 0:
                self._counters[pos] -= 1
                if self._counter[pos] == 0:
                    self._clear_bit(pos)
                    self._size -= 1
        return self
    
    def contains(self, value) -> bool:
        """Comprueba si un valor podría estar en el filtro (puede haber falsos positivos)."""
        key = consistent_stringify(value)
        return all(self._counters[pos] > 0  for pos in self._key_positions(key))

    @property
    def size(self) -> int:
        """Número de valores únicos insertados (aproximado)."""
        return self._size

    def false_positive_probability(self) -> float:
        """Calcula la probabilidad teórica de falso positivo."""
        k, n, m = self._num_hashes, self._size, self._num_bits
        return (1 - math.exp(-k * n / m))**k

    def confidence(self) -> float:
        """Devuelve la confianza (1 - probabilidad de falso positivo)."""
        return 1 - self.false_positive_probability()

    @property
    def max_remaining_capacity(self) -> int:
        """Capacidad restante antes de alcanzar max_size."""
        return max(0, self._max_size - self._size)