import hmm as HMM
import vitervi_alg
import random as rand
import pprint
import time


def evaluate_sequence(seq,labels,hmm):

    path = vitervi_alg.get_most_probable_path(hmm,seq)

    # print ("%s\n%s\n" %("".join(path),"".join(labels)))


    if path == labels:
        return 1
    else:
        return 0

def get_crossvalidation_sets(file,n):
    data_set =[]
    set = [[]]
    set_counter = 0

    for line in file:
        data_set.append(line)

    rand.shuffle(data_set)

    partition_len = int(len(data_set)/n)

    for line in data_set:
        line = line.strip()
        set[set_counter].append(line)
        if len(set[set_counter]) == partition_len:
            set.append([])
            set_counter +=1

    for i in range(n):
        testing_set = set[i]
        training_set = []
        for subset in range(n):
            if subset != i:
                training_set += set[subset]
        yield(training_set, testing_set)


def cross_validation(file, n, labels,toy,tia,rs):

    file  = open(file)
    tpr = []
    ciclo = 1
    for training_set, testing_set in get_crossvalidation_sets(file,n):
        print("empezamos con el ciclo %s" %ciclo)
        ciclo += 1
        hmm = HMM.get_hmm(labels, training_set,toy,tia,rs)


        print("El modelo de markov obtenido es:")
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(hmm)

        totals = len(testing_set)
        tp_tmp = 0

        for seq in testing_set:
            seq = seq.rstrip()
            tp_tmp += evaluate_sequence(seq, labels,hmm)

        print("El ratio de positivos verdaderos es %.4f" %(tp_tmp/totals))

        tpr.append(tp_tmp/totals)

    return tpr


if __name__ == "__main__":

    start_time = time.time()
    labels = HMM.mod2_label

    tpr = cross_validation("5_data_set.txt",7,labels,0,1,1)

    print(tpr)
    print("La media de tpr es: %s "%(sum(tpr)/len(tpr)))

    print("La ejecución ha tardado: %s segundos" %(time.time()-start_time))