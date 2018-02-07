import math


def get_most_probable_path(hmm, sequence):
    viterbi_matrix = []

    index_dic = {}

    hmm_states = []

    nuc_dic = {"A": 0, "C": 1, "G": 2, "T": 3}

    dic_counter = 1

    for state in hmm["states"]:

        if state != "begin":
            index_dic[state] = dic_counter
            dic_counter += 1
            hmm_states.append(state)

    pos_counter = 0

    viterbi_matrix.append([])

    for state in hmm_states:
        tr_p = hmm["trp"][0][index_dic[state]]
        em_p = hmm["emp"][index_dic[state]][nuc_dic[sequence[0]]]

        if tr_p != 0:
            trp_log = math.log(tr_p)
        else:
            trp_log = -999

        if em_p != 0:
            emp_log = math.log(em_p)
        else:
            emp_log = -999

        viterbi_matrix[pos_counter].append(trp_log + emp_log)

    pos_counter += 1

    for res in sequence[1:]:
        # print(res)

        viterbi_matrix.append([])

        for state in hmm_states:

            vik = []
            for Lstate in hmm_states:
                tr_p = hmm["trp"][index_dic[Lstate]][index_dic[state]]

                em_p = hmm["emp"][index_dic[state]][nuc_dic[res]]

                if tr_p != 0:
                    trp_log = math.log(tr_p)
                else:
                    trp_log = -999

                if em_p != 0:
                    emp_log = math.log(em_p)
                else:
                    emp_log = -999

                # print("posición: %s, Transición(%s->%s):%s, Emisión(%s):%s"%(pos_counter,Lstate,state,tr_p,res,em_p))

                if pos_counter > 1:
                    temp = trp_log + emp_log + viterbi_matrix[pos_counter-1][index_dic[Lstate]-1][1]
                else:
                    temp = trp_log + emp_log + viterbi_matrix[pos_counter - 1][index_dic[Lstate] - 1]

                # print(temp)

                vik.append((Lstate, temp))

            # print("\n")
            viterbi_matrix[pos_counter].append(max(vik, key=lambda x: x[1]))
        pos_counter += 1

    for i in range(len(viterbi_matrix[0])):
        for j in range(len(viterbi_matrix)):
            if j == 0:
                print("%10.4f\t" % viterbi_matrix[j][i], end="")
            else:
                print("%7s, %10.4f\t " % (viterbi_matrix[j][i][0], viterbi_matrix[j][i][1]), end="")

        print("\n")

    states_path = []
    start = True

    for position in viterbi_matrix[::-1]:
        if start:
            max_state = max(position, key=lambda x: x[1])
            state_index = position.index(max_state)

            print("state_index = %s" % state_index)

            for state, index in index_dic.items():
                if index == state_index+1:

                    states_path.append(state)
                    next_state = max_state[0]

            start = False

        else:

            state_index = index_dic[next_state]
            states_path.append(next_state)
            if type(position[state_index-1]) == tuple:
                next_state = position[state_index-1][0]




    states_path_str = " , ".join(states_path[::-1])



    # return viterbi_matrix
    return states_path_str

seq = "ACCCGAGTAA"

hmm = {
    "states": ["begin", "exon", "donor", "intron"],
    "emp": [[0.00, 0.00, 0.00, 0.00],
            [0.25, 0.25, 0.25, 0.25],
            [0.05, 0.00, 0.95, 0.00],
            [0.40, 0.10, 0.10, 0.40]],
    "trp": [[0.0, 1.0, 0.0, 0.0],
            [0.0, 0.9, 0.1, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0, 1.0]]
}

viterbi_path = get_most_probable_path(hmm, seq)

# for i in range(len(viterbi_mat[0])):
#     for j in range(len(viterbi_mat)):
#         if j == 0:
#             print("%10.4f\t" % viterbi_mat[j][i], end="")
#         else:
#             print("%7s, %10.4f\t " % (viterbi_mat[j][i][0], viterbi_mat[j][i][1]), end="")
#
#     print("\n")

print(viterbi_path)