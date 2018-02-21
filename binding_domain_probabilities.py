def sequence(length):
    """
    this functions generates a random dna sequence of the required length
    """
    import random
    return ''.join(random.choice('CGTA') for _ in range(length))


def comb_prob(sequences, n):
    """
    :param sequences: insert all the sequences to analyze in a list.
    :param n: length of the di-tri-quatr...
    :return: the probabilities of finding a certain nucleotide combination
    """
    from itertools import combinations

    if n == 1:
        combos = ["A", "T", "G", "C"]
    else:
        combos = ["".join(comb) for comb in combinations(["A", "T", "G", "C"]*n, n)]

    count = {"total": 0}
    for i in combos:
        count[i] = 0

    for seq in sequences:
        j = 0
        k = n
        while j < len(i):
            count[seq[j:k]] += 1
            count["total"] += 1
            j += 1
            k += 1

    prob = []
    for comb in combos:
        prob.append([comb, count[comb] / count["total"]])

    return prob

i = 0
seq_ls = []

while i < 120000:
    seq_ls.append(sequence(66))
    i += 1

file_seq = []


with open("5_data_set.txt") as fh:
    for line in fh:
        line = line.strip()
        file_seq.append(line[25:])

##################
#### introns #####
##################

out_di = open("di_prob_intro.txt", "w")

for i in comb_prob(seq_ls, 2):
    out_di.write("rand\t%s\t%s\n" % (i[0], i[1]))

for i in comb_prob(file_seq, 2):
    out_di.write("file\t%s\t%s\n" % (i[0], i[1]))

out_tri = open("tri_prob_intro.txt", "w")

for i in comb_prob(seq_ls, 3):
    out_tri.write("rand\t%s\t%s\n" % (i[0], i[1]))

for i in comb_prob(file_seq, 3):
    out_tri.write("file\t%s\t%s\n" % (i[0], i[1]))


out_tetra = open("tetra_prob_intro.txt", "w")

for i in comb_prob(seq_ls, 4):
    out_tetra.write("rand\t%s\t%s\n" % (i[0], i[1]))

for i in comb_prob(file_seq, 4):
    out_tetra.write("file\t%s\t%s\n" % (i[0], i[1]))

##################
####  exons  #####
##################

file_seq = []
with open("5_data_set.txt") as fh:
    for line in fh:
        line = line.strip()
        file_seq.append(line[0:20])

out_di = open("di_prob_exon.txt", "w")

for i in comb_prob(seq_ls, 2):
    out_di.write("rand\t%s\t%s\n" % (i[0], i[1]))

for i in comb_prob(file_seq, 2):
    out_di.write("file\t%s\t%s\n" % (i[0], i[1]))


out_tri = open("tri_prob_exon.txt", "w")

for i in comb_prob(seq_ls, 3):
    out_tri.write("rand\t%s\t%s\n" % (i[0], i[1]))

for i in comb_prob(file_seq, 3):
    out_tri.write("file\t%s\t%s\n" % (i[0], i[1]))


out_tetra = open("tetra_prob_exon.txt", "w")

for i in comb_prob(seq_ls, 4):
    out_tetra.write("rand\t%s\t%s\n" % (i[0], i[1]))

for i in comb_prob(file_seq, 4):
    out_tetra.write("file\t%s\t%s\n" % (i[0], i[1]))