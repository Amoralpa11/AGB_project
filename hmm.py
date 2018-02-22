import random
import emp


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

def get_states(labels):

    labels = tuple(['B'] + list(labels))
    states_list = sorted(list(set(labels)), key=lambda x: labels.index(x))

    return(states_list,labels)

def get_trp_matrix(labels):
    """Función que genera la matriz de transiciones a partir de la secuencia de estados de
    un conjunto de entrenamiento """


    (states_list,labels) = get_states(labels)
    trp_matrix = []

    index_dic = {}

    dic_counter = 0

    for state in states_list:
        index_dic[state] = dic_counter
        dic_counter += 1
        trp_matrix.append([])
        for state2 in states_list:
            trp_matrix[index_dic[state]].append(0)

    for pos in range(len(labels)):
        if pos != len(labels)-1:
                trp_matrix[index_dic[labels[pos]]][index_dic[labels[pos+1]]] += 1

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
def get_emp_matrix(training_set, labels):

    interval_list = get_intervals_from_labels(labels)

    emp_matrix = [[0, 0, 0, 0]]

    for interval in interval_list:
        emp_matrix.append(emp.calculation_emp(training_set, interval[0], interval[1]))

    return emp_matrix

def get_hmm(labels,training_set):

    hmm = {}
    hmm["states"] = get_states(labels)[0]
    hmm["emp"] = get_emp_matrix(training_set, labels)
    hmm["trp"] = get_trp_matrix(labels)

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
    'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'D1',
    'D2', 'D3', 'D4', 'D5', 'D6', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I')

if __name__ == "__main__":

    labels = mod1_label

    hmm = get_hmm(labels,"5_data_set.txt")

    print(hmm)
