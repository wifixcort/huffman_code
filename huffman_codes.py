# La siguiente herramienta toma un archivo .CSV con los encabezados(Simbolo, probabilidad) de un alfabeto
# y determina el código huffman correspondiente a cada uno de los símbolos proporcionados

import heapq
import csv
import math

file = 'no_huffman.csv'

# Función para construir el árbol de Huffman
def build_huffman_tree(freq_dict):
    heap = [[freq, [char, ""]] for char, freq in freq_dict.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

# Leer el alfabeto y las probabilidades de aparición desde un archivo CSV
with open(file, mode='r') as file:
    reader = csv.DictReader(file)
    huffman_list = []
    for row in reader:
        char = row['Simbolo']
        prob = float(row['Probabilidad'])
        huffman_list.append((char, prob))

# Construir el árbol de Huffman
freq_dict = dict(huffman_list)
huffman_tree = build_huffman_tree(freq_dict)

# Lista con los códigos de Huffman para cada letra del alfabeto y su longitud
huffman_codes = [(char, code, len(code)) for char, code in huffman_tree]

# Escribir los códigos de Huffman en un archivo CSV
with open('huffman_codes.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Simbolo', 'Probabilidad', 'Codigo Huffman', 'Ii', 'Li'])
    for char, prob in freq_dict.items():
        code, code_length = [(code, code_length) for c, code, code_length in huffman_codes if c == char][0]
        Ii = round(math.log2(1/prob), 3)
        writer.writerow([char, prob, code, Ii, code_length])

