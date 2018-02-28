import vitervi_alg
import pickle
import argparse
import os



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="")

    parser.add_argument('-i', '--input',
                        dest="seq",
                        action="store",
                        help="The sequence or file of sequences that we want to label")

    parser.add_argument('-m', '--model',
                        dest="model",
                        action="store",
                        default= "1",
                        help="A file to write the output of the program, the default is the stdout")

    options = parser.parse_args()

    seq = [options.seq]

    if os.path.isfile(seq[0]):
        with open(seq[0]) as file:
            seq = []
            for line in file:
                line = line.rstrip()
                seq.append(line)


    pickle_file = "model%s.p" %options.model

    hmm = pickle.load(open(pickle_file,'rb'))

    for sequence in seq:

        path = vitervi_alg.get_most_probable_path(hmm,sequence)

        print("%s\n%s\n" % (sequence,"".join(path)))