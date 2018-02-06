def emp_calc(input_str):
    prob_dict = {}
    emp_dict = {}

    seq_arr = input_str.split("/n")
    print(seq_arr)
    for line in seq_arr:
        char_in_line = set(line)

        for i in char_in_line:
            if i not in prob_dict.keys():
                prob_dict[i] = 0
            else:
                prob_dict[i] += line.count(i)

        for i in prob_dict.keys():
            emp_dict[i] = prob_dict[i]/sum(prob_dict.values())

        yield emp_dict
