import hmm as HMM
import vitervi_alg

def evaluate_sequence(seq,labels,hmm):

    path = vitervi_alg.get_most_probable_path(hmm,seq)

    print ("%s\n%s\n" %("".join(path),"".join(labels)))


    if path == labels:
        return 1
    else:
        return 0


combos = ["A", "T", "G", "C"]

if __name__ == "__main__":

    labels = HMM.mod1_label

    hmm = HMM.get_hmm(labels,"5_data_set.txt")
    tp = 0
    totals = 0

    with open("5_data_set.txt") as set:

        for line in set:
            line = line.strip()
            tp += evaluate_sequence(line, labels,hmm)
            totals +=1

print(tp/totals)