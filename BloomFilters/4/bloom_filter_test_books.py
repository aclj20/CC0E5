# Programa en Python 3 para la prueba de primalidad aleatoria Miller-Rabin
# Copiado de geeksforgeeks: https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/
import random 

# Función auxiliar para realizar la exponenciación modular.
# Retorna (x^y) % p
def power(x, y, p): 
	# Inicializar resultado
	res = 1; 
	
	# Actualizar x si es mayor o igual que p
	x = x % p; 
	while (y > 0): 
		# Si y es impar, multiplica x con el resultado
		if (y & 1): 
			res = (res * x) % p; 

		# Ahora y debe ser par
		y = y >> 1; # y = y/2 
		x = (x * x) % p; 
	
	return res; 

# Esta función se llama para todos los k ensayos.
# Retorna False si n es compuesto y True si n es probablemente primo.
# d es un número impar tal que d*2^r = n-1 para algún r >= 1
def miillerTest(d, n): 
	# Elegir un número aleatorio en [2, n-2]
	# Casos particulares aseguran que n > 4
	a = 2 + random.randint(1, n - 4); 

	# Calcular a^d % n
	x = power(a, d, n); 

	if (x == 1 or x == n - 1): 
		return True; 

	# Seguir elevando x al cuadrado hasta que:
	# (i) d no alcance n-1, o
	# (ii) (x^2) % n no sea 1, o
	# (iii) (x^2) % n no sea n-1
	while (d != n - 1): 
		x = (x * x) % n; 
		d *= 2; 

		if (x == 1): 
			return False; 
		if (x == n - 1): 
			return True; 

	# Retorna compuesto
	return False; 

# Retorna False si n es compuesto y True si n es probablemente primo.
# k es un parámetro que determina el nivel de precisión; un valor mayor de k indica mayor precisión.
def isPrime( n, k): 
	# Casos particulares
	if (n <= 1 or n == 4): 
		return False; 
	if (n <= 3): 
		return True; 

	# Encontrar d tal que n = 2^r * d + 1 para algún r >= 1
	d = n - 1; 
	while (d % 2 == 0): 
		d //= 2; 

	# Iterar k veces
	for i in range(k): 
		if (miillerTest(d, n) == False): 
			return False; 

	return True; 



# Obtener un triple aleatorio (p, a, b) donde p es primo y a, b son números entre 2 y p-1
def get_random_hash_function():
    n = random.getrandbits(64)
    if n < 0: 
        n = -n 
    if n % 2 == 0:
        n = n + 1
    while not isPrime(n, 20):
        n = n + 1
    a = random.randint(2, n-1)
    b = random.randint(2, n-1)
    return (n, a, b)

# Función hash para un número
def hashfun(hfun_rep, num):
    (p, a, b) = hfun_rep
    return (a * num + b) % p

# Función hash para una cadena.
def hash_string(hfun_rep, hstr):
    n = hash(hstr)
    return hashfun(hfun_rep, n)    

filename = 'great-gatsby-fitzgerald.txt'
with open(filename, 'r', encoding='utf-8') as file:
    txt = file.read()

txt = txt.replace('\n', ' ')
words = txt.split(' ')
longer_words_gg = list(filter(lambda s: len(s) >= 5, words))
print(len(longer_words_gg))

# Contemos la frecuencia exacta de cada palabra
word_freq_gg = {}
for elt in longer_words_gg:
    if elt in word_freq_gg:
        word_freq_gg[elt] += 1
    else:
        word_freq_gg[elt] = 1
print(len(word_freq_gg))

filename = 'war-and-peace-tolstoy.txt'
with open(filename, 'r', encoding='utf-8') as file:
    txt = file.read()

txt = txt.replace('\n', ' ')
words = txt.split(' ')
longer_words_wp = list(filter(lambda s: len(s) >= 5, words))
print(len(longer_words_wp))

# Contemos la frecuencia exacta de cada palabra
word_freq_wp = {}
for elt in longer_words_wp:
    if elt in word_freq_wp:
        word_freq_wp[elt] += 1
    else:
        word_freq_wp[elt] = 1
print(len(word_freq_wp))