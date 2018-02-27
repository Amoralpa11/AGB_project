import hmm as HMM
import vitervi_alg
import random as rand
import argparse
import sys
import math
import pickle


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


def select_avarage_hmm(hmm_array, accuracy, mean_tpr):

    sorted_cycle = sorted(accuracy,key= lambda x: math.pow((x[0]-mean_tpr),2))

    index = accuracy.index(sorted_cycle[0])

    return hmm_array[index]


def print_accuracy_to_file(options, accuracy):

    model = ""

    if options.toy:
        model += "toy"
    else:
        model += "D6"

    if options.exon == 'complex':
        model += "_eC"

    if options.intron == 'complex':
        model += "_iC"

    if options.ise == 'simple':
        model += "_tia"
    elif options.ise == 'complex':
        model += "_tiaC"

    if options.ese == 'complex':
        model += "_rs"
    elif options.ese == 'complex':
        model += "_rsC"

    with open('accuracy_measures.txt','a') as am:
        for iteration in range(len(accuracy)):
            tpr = accuracy[iteration][0]
            ppv = accuracy[iteration][1]
            fdr = accuracy[iteration][2]

            am.write("%s\t%s\t%s\t%s\t%s\n" %(model,iteration,tpr,ppv,fdr))




def cross_validation(file, n, labels, toy, tia, rs, out,options):
    file = open(options.infile)
    accuracy = []
    ciclo = 1
    hmm_array = []
    for training_set, testing_set in get_crossvalidation_sets(file, options.n):
        out.write("Starting the cycle %s\n" % ciclo)
        ciclo += 1

        hmm = HMM.get_hmm(labels, training_set, options)
        hmm_array.append(hmm)

        out.write("The obtained hidden Markov model is:\n\n")
        print_hmm(hmm, out)

        tp = 0
        fp = 0
        fn = 0

        for seq in testing_set:
            seq = seq.rstrip()
            result = evaluate_sequence(seq, labels, hmm)
            tp += result[0]
            fp += result[1]
            fn += result[2]

        tpr = tp / (tp + fn + fp)
        ppv = tp / (fp + tp)
        fdr = fp / (fp + tp)


        out.write("\nThe true positive rate is: %.3f\n" % (tpr))
        out.write("The positive predicted value is: %.3f\n" % (ppv))
        out.write("The false discovery rate is: %.3f\n\n" % (fdr))

        accuracy.append([tpr,ppv,fdr])

    print_accuracy_to_file(options, accuracy)

    mean_tpr = sum([x[0] for x in accuracy])/len(accuracy)
    mean_ppv = sum([x[1] for x in accuracy])/len(accuracy)
    mean_fdr = sum([x[2] for x in accuracy])/len(accuracy)

    out.write("The mean true positive rate is: %.3f\n" % (mean_tpr))
    out.write("The mean positive predicted value is: %.3f\n" % (mean_ppv))
    out.write("The mean false discovery rate is: %.3f\n\n" % (mean_fdr))

    avarage_hmm = select_avarage_hmm(hmm_array,accuracy,mean_tpr)

    return avarage_hmm

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

    parser.add_argument("-ex","--exon",
                        dest="exon",
                        action="store",
                        default='simple',
                        choices=['simple','complex'],
                        help = "This options takes one of two values, if set to simple a simple state will be included to model the exon, if set to complex a markov chain will be used")

    parser.add_argument("-in","--intron",
                        dest="intron",
                        action="store",
                        default='simple',
                        choices=['simple','complex'],
                        help = "This options takes one of two values, if set to simple a simple state will be included to model the intron, if set to complex a markov chain will be used")

    parser.add_argument("-I","--ise",
                        dest="ise",
                        action="store",
                        default=None,
                        choices=[None,'simple','complex'],
                        help = "This options takes one of two values, if set to simple a simple state will be included to model the ise islands, if set to complex a markov chain will be used")

    parser.add_argument("-e","--ese",
                        dest="ese",
                        action="store",
                        default= None,
                        choices=[None,'simple','complex'],
                        help = "This options takes one of two values, if set to simple a simple state will be included to model the ese islands, if set to complex a markov chain will be used")

    parser.add_argument("-s","--save_model",
                        dest="save_model",
                        action="store",
                        help = "If set, the model with the closest TPR to the mean will be saved as a pickle file")

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

    hmm = cross_validation(file, n, labels, toy, ise, ese, out,options)

    if options.save_model:
       with open(options.save_model,"wb") as  p_hmm:
            pickle.dump(hmm,p_hmm)



