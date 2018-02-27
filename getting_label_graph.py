import math


intron = 'GTCTCAAGCAAATCCTTTTTTTTTTTTTTTTTTGAGACAGAGTCTTGCTCTGTCGCT'

nuc_dic = {'A': 0, 'C': 1, 'G': 2, 'T': 3}


def get_prob(seq, emp):
    prob = 1
    for nuc in seq:
        prob *= emp[nuc_dic[nuc]]
    return prob


def get_intron_labels_from_emp(win_size, seq):


    seq_emp = [0.23766333309000656,
               0.22217541561563023,
               0.252599202969668,
               0.28756204832469523]
    island_emp = [0.033, 0.033, 0.033, 0.9]


    start = 0
    end = win_size
    log_like_array = []

    while end <= len(seq):
        seq_prob = get_prob(seq[start:end], seq_emp)
        island_prob = get_prob(seq[start:end], island_emp)
        # log_like_array.append(math.log(island_prob/seq_prob, 10))
        likelyhood = math.log(island_prob / seq_prob, 10)
        for pos in range(start, end):
            if pos > len(log_like_array) - 1:
                log_like_array.append([])

            log_like_array[pos].append(likelyhood)

        start += 1
        end += 1

    likelyhood_array = []
    for pos in range(len(seq)):
        likelyhood_array.append(sum(log_like_array[pos]) / len(log_like_array[pos]))
    return likelyhood_array



loglikelyhood_array = []
file = open("likelihood_labelling.txt",'w')
for winsize in range(1,len(intron)):
    array = (get_intron_labels_from_emp(winsize, intron))
    array_str = "\t".join([str(x) for x in array])
    file.write("%s\n" % array_str)

