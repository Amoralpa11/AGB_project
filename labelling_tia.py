import math
# import numpy as np
# import matplotlib.pyplot as plt


intron = 'GTCTCAAGCAAATCCTTTTTTTTTTTTTTTTTTGAGACAGAGTCTTGCTCTGTCGCT'

def get_intron_labels(win_size,seq):

    intron_emp = [0.23766333309000656,
                  0.22217541561563023,
                  0.252599202969668,
                  0.28756204832469523]

    tia_emp = [0.033,0.033,0.033,0.9]

    nuc_dic = {'A': 0, 'C': 1, 'G': 2, 'T': 3}


    def get_prob(seq, emp):
        prob = 1
        for nuc in seq:
            prob *= emp[nuc_dic[nuc]]
        return prob

    start = 0
    end = win_size
    log_like_array = []
    labels = []
    while end <= len(seq):
        intron_prob = get_prob(seq[start:end], intron_emp)
        tia_prob = get_prob(seq[start:end], tia_emp)
        # log_like_array.append(math.log(tia_prob/intron_prob, 10))
        likelyhood = math.log(tia_prob/intron_prob, 10)
        for pos in range(start,end):
            if pos > len(log_like_array)-1:
                log_like_array.append(likelyhood)
            else:
                log_like_array[pos]+= likelyhood


        start +=1
        end +=1

    for pos in range(len(seq)):
        if log_like_array[pos] > 0:
            labels.append('T')
        else:
            labels.append('i')

    return labels
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