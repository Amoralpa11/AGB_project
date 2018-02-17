import random
import emp


def get_intervals_from_labels(labels):
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

# En primer lugar abrimos el archivo


ff = open("5_data_set.txt")

# Dividimos las lineas en dos subconjutnos, uno para
# entrenamiento del modelo y otro para su evaluación

evaluation_set = []
training_set = []

for line in ff:
    random_number = random.randint(0, 1)
    if random_number < 0.3:
        evaluation_set.append(line)
    else:
        training_set.append(line)

# Training the model with the training_set

# To do this we need labeled data, It is easy for the
# first two models

mod1_label = (
    'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'D', 'I', 'I',
    'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I')

mod2_label = (
    'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'D1',
    'D2', 'D3', 'D4', 'D5', 'D6', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I')

# now we have to set the emission probabilities and the
# transition probabilities using these labels

interval_list = get_intervals_from_labels(mod1_label)

emp_matrix = []

for interval in interval_list:
    emp_matrix.append(emp.calculation_emp(interval[0], interval[1]))
