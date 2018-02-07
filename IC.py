import sys
import math

file_paht = "5_data_set.txt"

try:
    file_paht = sys.argv[1]
except:
    print("Debes Introducir el path del archivo")

# Abriendo el archivo

input_file = open(file_paht)

# Contando la frecuencia absoluta de los nucleotidos

freq = []
n_seqs = 0

for seq in input_file:
    n_seqs = n_seqs + 1
    seq = seq.rstrip()
    for position in range(len(seq)):
        if position not in range(len(freq)):
            freq.append({"A": 0, "C": 0, "G": 0, "T": 0})
        freq[position][seq[position]] = freq[position][seq[position]] + 1

# Calculando la frecuencia relativa

for position in freq:
    for nucleotide in position:
        position[nucleotide] = position[nucleotide] / n_seqs

IC_list = []

# calculating entropy

for position in freq:
    entropy_list = []
    for nucleotide in position:
        if position[nucleotide] != 0:
            entropy_list.append(position[nucleotide] * math.log(position[nucleotide], 2))

    IC_list.append(math.log(4, 2) + sum(entropy_list))

print(IC_list)
