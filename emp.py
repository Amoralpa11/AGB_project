import numpy as np


def emp_calc(input_str):
    prob_dict = {}
    emp_dict = {}

    char_in_line = set(input_str)

    for i in char_in_line:
        prob_dict[i] = input_str.count(i)

    emp_dict = {'A' : 0, 'T' : 0, 'G' : 0, 'C' : 0}
    for i in prob_dict.keys():
        emp_dict[i] = prob_dict[i]/sum(prob_dict.values())

    emp_sorted = sorted(emp_dict.items())

    values = []
    for i in emp_sorted:
        values.append(i[1])
    return values



def calculation_emp(start, rang = 1):
    with open("5_data_set.txt") as fh:

        data = ""
        for line in fh:
            data += line[start:start+rang].strip()
            # print(data)

    return emp_calc(data)


ls_m1 = [(0,20),(20,1),(21,83)]

ls_m2 = [(0,18),(18,1),(19,1),(20,1),(21,1),(22,1),(23,1),(24,1),(24,83)]


emp_matrix = []

for i in ls_m1:
    emp_matrix.append(calculation_emp(i[0],i[1]))

print(emp_matrix)



states_m1 = ["begin","exon","donor","intron"]
trp_m1 = [[0,1,0,0],
       [0,0.95,0.05,0,],
       [0,0,0,1],
       [0,0,0,1]]
emp_m1 = [[0.2894930198383541, 0.24105127591245698, 0.2570639566082441, 0.2123917476409448],
        [0, 0, 1.0, 0],
        [0.24765265157631025, 0.21295911458167685, 0.2471675976390974, 0.2922206362029155]]


states_m2 = ["begin","exon","min2","min1","g","t","more1","more2","more3","intron"]
trp_m2 = [[0,1,0,0,0,0,0,0,0,0],
       [0,0.95,0.05,0,0,0,0,0,0,0],
       [0,0,0,1,0,0,0,0,0,0],
       [0,0,0,0,1,0,0,0,0,0],
       [0,0,0,0,0,1,0,0,0,0],
       [0,0,0,0,0,0,1,0,0,0],
       [0,0,0,0,0,0,0,1,0,0],
       [0,0,0,0,0,0,0,0,1,0],
       [0,0,0,0,0,0,0,0,0,1],
       [0,0,0,0,0,0,0,0,0,1]]

emp_m2 = [[0.2800861524123501, 0.26067204752325573, 0.2349258504019131, 0.22431594966248106],
        [0.6500755393010758, 0.10237845602621998, 0.10817393027268449, 0.1393720744000198],
        [0.09823411404370547, 0.026550206804316058, 0.8044398946577616, 0.07077578449421691],
        [0, 0, 1.0, 0],
        [0, 0, 0, 1.0],
        [0.6116371801963196, 0.028919581603084315, 0.329854948030612, 0.029588290169984068],
        [0.6952752850267071, 0.07406979336079716, 0.11531507731426827, 0.11533984429822751],
        [0.0913736594869932, 0.055139561954610374, 0.773877436452047, 0.07960934210634943],
        [0.23792929794710171, 0.22219856231928287, 0.2522767832868976, 0.2875953564467178]]



# print(emp_matrix)

# print(emp_matrix.reshape(9,4))

# exon_emp = calculation_emp(0,20)
# print("exon")
# print(exon_emp)
# min2_emp = calculation_emp(18)
# print("min2")
# print(min2_emp)
# min1_emp = calculation_emp(19)
# print("min1")
# print(min1_emp)
#
# five_emp = calculation_emp(20)
# print("5'")
# print(five_emp)
# five_emp_ = calculation_emp(21)
# print("5''")
# print(five_emp_)
#
# more1_emp = calculation_emp(22)
# print("more1")
# print(more1_emp)
# more2_emp = calculation_emp(23)
# print("more2")
# print(more2_emp)
# more3_emp = calculation_emp(24)
# print("more3")
# print(more3_emp)
# intron_emp = calculation_emp(20,82)
# print("intron")
# print(intron_emp)

