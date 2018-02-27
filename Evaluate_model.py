import hmm as HMM
import vitervi_alg
import random as rand
import pprint
import time
import argparse
import sys


def evaluate_sequence(seq, labels, hmm):
    path = vitervi_alg.get_most_probable_path(hmm, seq)


    # print ("%s\n%s\n" %("".join(path),"".join(labels)))

    if path[20] == labels[20]:
        result = [1,0,0]
    elif '3' in path or "D" in path:
        # print ("%s\n%s\n%s\n" %("".join(path),"".join(labels),seq))
        result = [0,1,0]
    else:
        result = [0,0,1]

    return result


def get_crossvalidation_sets(file, n):
    data_set = []
    set = [[]]
    set_counter = 0

    for line in file:
        data_set.append(line)

    rand.shuffle(data_set)

    partition_len = int(len(data_set) / n)

    for line in data_set:
        line = line.strip()
        set[set_counter].append(line)
        if len(set[set_counter]) == partition_len:
            set.append([])
            set_counter += 1

    for i in range(n):
        testing_set = set[i]
        training_set = []
        for subset in range(n):
            if subset != i:
                training_set += set[subset]
        yield (training_set, testing_set)


def cross_validation(file, n, labels, toy, tia, rs, out):
    file = open(file)
    tpr = []
    ciclo = 1
    for training_set, testing_set in get_crossvalidation_sets(file, n):
        out.write("Starting the cycle %s\n" % ciclo)
        ciclo += 1

        hmm = HMM.get_hmm(labels, training_set, toy, tia, rs)

        out.write("The obtained hidden Markov model is:\n\n")
        print_hmm(hmm, out)

        totals = len(testing_set)
        tp_tmp = 0

        tp = 0
        fp = 0
        fn = 0

        for seq in testing_set:
            seq = seq.rstrip()
            result = evaluate_sequence(seq, labels, hmm)
            tp += result[0]
            fp += result[1]
            fn += result[2]


        out.write("The true positive rate is: %.3f" % (tp_tmp / totals))

        tpr.append(tp_tmp / totals)

    return tpr

def print_hmm(hmm, out):
    states = ", ".join(hmm['states'])
    out.write("States: %s\n\n" % states)

    out.write("Emp: \n")
    out.write("\t\t%4s\t%4s\t%4s\t%4s\n" %("A","C","G","T"))
    counter = 0
    for emp in hmm['emp']:
        out.write("\t%s\t%.3f\t%.3f\t%.3f\t%.3f\n" % (hmm['states'][counter], emp[0],emp[1],emp[2],emp[3]))
        counter +=1
    out.write("\n")

    out.write("Trp: \n\t")
    for state in hmm['states']:
        out.write("\t%4s" % state)
    out.write('\n')
    counter = 0
    for trp in hmm['trp']:
        out.write("\t%s" % hmm['states'][counter])
        counter +=1
        for trp2 in trp:
            out.write("\t %.3f" % trp2)
        out.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This program takes a file with sequences containing a 5' donor splice site splits the set in different groups, generates a model to find the 5' splice site and does a n cross-validation to obtain the acuracy analisys of the model")

    parser.add_argument('-i', '--input',
                        dest="infile",
                        action="store",

                        help="The path of the file with the data")

    parser.add_argument('-o', '--output',
                        dest="outfile",
                        action="store",
                        default= sys.stdout,
                        help="A file to write the output of the program, the default is the stdout")

    parser.add_argument('-n',
                        dest="n",
                        action = "store",
                        default= 7,
                        help = "The number of divisions to perform the n cross-validation")

    parser.add_argument("-t","--toy",
                        dest="toy",
                        action="store_true",
                        help = "If set, there will only be considerated one position (G) of the donor splice site")

    parser.add_argument("-I","--ise",
                        dest="ise",
                        action="store_true",
                        help = "If set, the model will include an state to model a T-rich protein binding sequence in "
                               "the intron")

    parser.add_argument("-e","--ese",
                        dest="ese",
                        action="store_true",
                        help = "If set, the model will include an state to model a AG-rich protein binding sequence "
                               "in the exon")

    options = parser.parse_args()

    if options.toy:
        labels = HMM.mod1_label
    else:
        labels = HMM.mod2_label

    file = options.infile
    n = options.n
    toy = options.toy
    ise = options.ise
    ese = options.ese

    out = options.outfile

    tpr = cross_validation(file, n, labels, toy, ise, ese, out)

    out.write("La media de tpr es: %s " % (sum(tpr) / len(tpr)))


