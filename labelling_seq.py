import math

# import numpy as np
# import matplotlib.pyplot as plt


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
    island = 'T'
    state = 'I'

    start = 0
    end = win_size
    log_like_array = []
    labels = []
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

    for pos in range(len(seq)):
        likelyhood = sum(log_like_array[pos]) / len(log_like_array[pos])
        if likelyhood > 0:
            labels.append(island+ seq[pos])
        else:
            labels.append(state + seq[pos])

    return labels


def get_exon_labels_from_emp(win_size, seq):

    seq_emp = [0.2803125160528073,
               0.2607403982808514,
               0.23475411379942124,
               0.22419297186692008]
    island_emp = [0.45, 0.05, 0.45, 0.05]
    island = 'R'
    state = 'E'

    start = 0
    end = win_size
    log_like_array = []
    labels = []
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

    for pos in range(len(seq)):
        likelyhood = sum(log_like_array[pos]) / len(log_like_array[pos])
        if likelyhood > 0:
            labels.append(island + seq[pos])
        else:
            labels.append(state + seq[pos])

    return labels


def get_prob_from_tr(seq, seq_trp):
    prob = 1
    for pos in range(len(seq)):
        if pos < len(seq) - 1:
            prob *= seq_trp[nuc_dic[seq[pos]]][nuc_dic[seq[pos + 1]]]
    return prob


def get_exon_labels_from_trp(win_size, seq):
    seq_trp = [[0.27279609400987204,
                0.20932757783495892,
                0.26066251954715597,
                0.18973645272169057],
                [0.31384738609408214,
                0.2626474846739164,
                0.08607867903022089,
                0.26063481305772057],
                [0.3083792773499795,
                0.25190458832642276,
                0.23801430719460517,
                0.1590012302364788],
                [0.15282231013300418,
                0.2670254190550997,
                0.31651462664046853,
                0.23412174502636926]]

    island_trp = [[0.27279609400987204,
                0.20932757783495892,
                0.30066251954715597,
                0.18973645272169057],
                [0.31384738609408214,
                0.2626474846739164,
                0.08607867903022089,
                0.26063481305772057],
                [0.3083792773499795,
                0.25190458832642276,
                0.23801430719460517,
                0.1590012302364788],
                [0.15282231013300418,
                0.2670254190550997,
                0.31651462664046853,
                0.23412174502636926]]

    island = 'R'
    state = 'E'

    start = 0
    end = win_size
    log_like_array = []
    labels = []
    while end <= len(seq):
        seq_prob = get_prob_from_tr(seq[start:end], seq_trp)
        island_prob = get_prob_from_tr(seq[start:end], island_trp)
        # log_like_array.append(math.log(island_prob/seq_prob, 10))
        likelyhood = math.log(island_prob / seq_prob, 10)
        for pos in range(start, end):
            if pos > len(log_like_array) - 1:
                log_like_array.append([])

            log_like_array[pos].append(likelyhood)

        start += 1
        end += 1

    for pos in range(len(seq)):
        likelyhood = sum(log_like_array[pos]) / len(log_like_array[pos])
        if likelyhood > 0:
            labels.append(island + seq[pos])
        else:
            labels.append(state + seq[pos])
    # print(labels)

    return labels


def update_path(prev_path, islands, island):
    newpath = list(prev_path)

    for node in islands:
        newpath[node[0]:node[1]] = [island] * (node[1] - node[0])

    return newpath


def get_seq_labels2(seq, rs, tia):
    if tia:
        seq_emp = [0.23766333309000656,
                   0.22217541561563023,
                   0.252599202969668,
                   0.28756204832469523]
        island_emp = [0.033, 0.033, 0.033, 0.9]
        island = 'T'
        state = 'I'

    if rs:
        seq_emp = [0.2800845661889351,
                   0.2606119758223318,
                   0.23485578157908255,
                   0.22444767640965052]

        island_emp = [0.45, 0.033, 0.45, 0.033]
        island = 'R'
        state = 'E'

    islands = []

    for pos in range(len(seq)):
        start = pos
        end = pos + 1
        seq_prob = get_prob(seq[start:end], seq_emp)
        island_prob = get_prob(seq[start:end], island_emp)
        likelyhood = math.log(island_prob / seq_prob, 10)
        if likelyhood > 0:
            islands.append([pos, pos + 1])
    prev_path = [state] * len(seq)
    new_path = update_path(prev_path, islands, island)

    while prev_path != new_path:
        new_islands = []

        for pos in range(len(islands)):
            if pos < len(islands) - 1:
                start = islands[pos][0]
                end = islands[pos + 1][1]
                seq_prob = get_prob(seq[start:end], seq_emp)
                island_prob = get_prob(seq[start:end], island_emp)
                likelyhood = math.log(island_prob / seq_prob, 10)
                if likelyhood > 0:
                    new_islands.append([islands[pos][0], islands[pos + 1][1]])
        prev_path = new_path
        islands = new_islands

        new_path = update_path(prev_path, islands, island)

    return new_path
    # print("window size: %s" %window_size)
    # print(len(log_like_array))

    # plt.plot(log_like_array)
    # plt.show()


#
#
# # Data for plotting
# t = np.arange(0.0, 2.0, 0.01)
# s = 1 + np.sin(2 * np.pi * t)
#
# # Note that using plt.subplots below is equivalent to using
# # fig = plt.figure and then ax = fig.add_subplot(111)
# fig, ax = plt.subplots()
# ax.plot(t, s)
#
# ax.set(xlabel='time (s)', ylabel='voltage (mV)',
#        title='About as simple as it gets, folks')
# ax.grid()
#
# fig.savefig("test.png")
# plt.show()


if __name__ == '__main__':
    path2 = get_seq_labels2(intron, 0, 1)
    path = get_intron_labels(1, intron, 0, 1)

    print(''.join(path))
    print(''.join(path2))
    print(intron)
