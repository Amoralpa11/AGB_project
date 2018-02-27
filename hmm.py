import random
import emp
import labelling_seq

def get_intervals_from_labels(labels):
    """ Función que genera los intervalos con estados diferentes a partir
    de una lista con los estados de en un training set"""

    interval_list = []
    previous_state = ""
    interval = []

    for pos in range(len(labels)):
        if not previous_state:
            interval.append(pos)
            previous_state = labels[pos]
            continue
        if labels[pos] != previous_state:
            interval.append(pos-interval[0])
            interval_list.append(interval)
            interval = [pos]
            previous_state = labels[pos]
        if pos == len(labels)-1:
            interval.append(pos-interval[0])
            interval_list.append(interval)

    return interval_list

def get_states(options):

    toy = options.toy
    ise = options.ise
    ese = options.ese
    intron = options.intron
    exon = options.exon

    states_list = ['B']

    if exon == 'complex':
        states_list +=['EA','EC','EG','ET']
    else:
        states_list.append('E')

    if toy:
        states_list.append('D')
    else:
        states_list += ['1', '2', '3', '4', '5', '6']

    if intron == 'complex':
        states_list += ['IA', 'IC', 'IG', 'IT']
    else:
        states_list.append('I')

    if ese == 'complex':
        states_list += ['RA', 'RC', 'RG', 'RT']

    elif ese == 'simple':
        states_list.append('R')

    if ise == 'complex':
        states_list += ['TA', 'TC', 'TG', 'TT']
    elif ise == 'simple':
        states_list.append('T')

    return (states_list)

def get_trp_matrix(states_list,labels):
    """Función que genera la matriz de transiciones a partir de la secuencia de estados de
    un conjunto de entrenamiento """

    if type(labels[0]) == type(str()):
        labels  = [labels]

    trp_matrix = []

    index_dic = {}

    dic_counter = 0

    for state in states_list:
        index_dic[state] = dic_counter
        dic_counter += 1
        trp_matrix.append([])
        for state2 in states_list:
            trp_matrix[index_dic[state]].append(0)

    for lab in labels:
        lab = tuple(['B']+list(lab))
        for pos in range(len(lab)):
            if pos != len(lab)-1:
                    trp_matrix[index_dic[lab[pos]]][index_dic[lab[pos+1]]] += 1


    for state in range(len(trp_matrix)):
        total = sum(trp_matrix[state])
        for transition in range(len(trp_matrix[state])):
            trp_matrix[state][transition] = trp_matrix[state][transition] / total

    return trp_matrix



# En primer lugar abrimos el archivo

def divide_set(file,p):

    ff = open(file)

    # Dividimos las lineas en dos subconjutnos, uno para
    # entrenamiento del modelo y otro para su evaluación

    evaluation_set = []
    training_set = []

    for line in ff:
        random_number = random.randint(0, 1)
        if random_number < p:
            evaluation_set.append(line)
        else:
            training_set.append(line)

    return (evaluation_set,training_set)

# Training the model with the training_set

# To do this we need labeled data, It is easy for the
# first two models

# now we have to set the emission probabilities and the
# transition probabilities using these labels


def get_emp_matrix(training_set, labels,options):

    toy = options.toy
    ise = options.ise
    ese = options.ese
    intron = options.intron
    exon = options.exon

    interval_list = get_intervals_from_labels(labels)

    if ese == 'complex' or exon == 'complex':
        interval_list = interval_list[1:]
    if ise == 'complex' or intron == 'complex':
        interval_list = interval_list[:-1]

    emp_matrix = [[0, 0, 0, 0]]

    if exon == 'complex':
        emp_matrix +=[[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]]

    for interval in interval_list:
        emp_matrix.append(emp.calculation_emp(training_set, interval[0], interval[1]))

    if intron == 'complex':
        emp_matrix += [[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]]

    if ese == 'complex':
        emp_matrix += [[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]]
    elif ese == 'simple':
        emp_matrix.append([0.45,0.05,0.45,0.05])

    if ise == 'complex':
        emp_matrix += [[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]]
    elif ise =='simple':
        emp_matrix.append([0.033,0.033,0.033,0.9])

    return emp_matrix


def transform_labels(labels, training_set,options,wint,winr):
    labs = []
    intervals = get_intervals_from_labels(labels)

    tia = options.ise
    rs = options.ese

    if tia and not rs:
        for seq in training_set:
            labs.append(list(labels[:intervals[-1][0]]) +
                        labelling_seq.get_intron_labels_from_emp(wint, seq[intervals[-1][0]:],options))

    elif rs and not tia:
        for seq in training_set:
            labs.append(labelling_seq.get_exon_labels_from_emp(winr, seq[:intervals[0][1]],options) +
                        list(labels[intervals[0][1]:]))

    else:
        for seq in training_set:
            labs.append(labelling_seq.get_exon_labels_from_emp(winr, seq[:intervals[0][1]],options) +
                        list(labels[intervals[0][1]:intervals[-1][0]]) +
                        labelling_seq.get_intron_labels_from_emp(wint, seq[intervals[-1][0]:],options))

    return labs


def get_hmm(labels,training_set,options):
    labels2 = labels
    if options.ise or options.ese:
        labels2 = transform_labels(labels,training_set,options,12,6)

    hmm = {}
    hmm["states"] = get_states(options)
    hmm["emp"] = get_emp_matrix(training_set, labels,options)
    hmm["trp"] = get_trp_matrix(hmm['states'],labels2)

    return hmm

mod1_label = (
    'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'D', 'I',
    'I',
    'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I',
    'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I',
    'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I')

mod2_label = (
    'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', '1',
    '2', '3', '4', '5', '6', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I')