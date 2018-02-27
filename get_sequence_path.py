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

    pickle_file = "model%s.p" %options.model

    hmm = pickle.load(open(pickle_file,'rb'))

    path = vitervi_alg.get_most_probable_path(hmm,options.seq)

    print("%s\n%s" % (options.seq,"".join(path)))