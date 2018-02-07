def emp_calc(input_str):
    prob_dict = {}
    emp_dict = {}

    char_in_line = set(input_str)

    for i in char_in_line:
        prob_dict[i] = input_str.count(i)

    for i in prob_dict.keys():
        emp_dict[i] = prob_dict[i]/sum(prob_dict.values())

    return emp_dict


def calculation_emp(start = None, rang = 1):
    with open("5_data_set.txt") as fh:
        data = ""
        for line in fh:
            data += line[start:start+rang].strip()
            # print(data)

    return emp_calc(data.strip())


exon_emp = calculation_emp(0,20)
print("exon")
print(exon_emp)
min2_emp = calculation_emp(18)
print("min2")
print(min2_emp)
min1_emp = calculation_emp(19)
print("min1")
print(min1_emp)

five_emp = calculation_emp(20)
print("5'")
print(five_emp)
five_emp_ = calculation_emp(21)
print("5''")
print(five_emp_)

more1_emp = calculation_emp(22)
print("more1")
print(more1_emp)
more2_emp = calculation_emp(23)
print("more2")
print(more2_emp)
more3_emp = calculation_emp(24)
print("more3")
print(more3_emp)
intron_emp = calculation_emp(20,82)
print("intron")
print(intron_emp)
