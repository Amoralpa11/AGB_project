import labelling_tia
import pprint

with open('5_data_set.txt') as file:
    length_dist = {}
    labels_list = []
    for seq in file:
        seq = seq[24:82]
        labels = labelling_tia.get_intron_labels(7, seq)
        labels_list.append("".join(labels))

island_length = 0

for seq in labels_list:
    for nuc in seq:
        if nuc == 'T':
            island_length +=1
        elif island_length > 0:
            if island_length not in length_dist.keys():
                length_dist[island_length] = 1
            else:
                length_dist[island_length] +=1
            island_length = 0

dist_list = []
n = 1

for n in range(1,max(length_dist.keys())+1):
    if n in length_dist.keys():
        dist_list.append(length_dist[n])
    else:
        dist_list.append(0)
total = sum(dist_list)
for i in range(len(dist_list)):
    dist_list[i] = dist_list[i]/total

print(dist_list)
pp  = pprint.PrettyPrinter(indent=4)
pp.pprint(length_dist)