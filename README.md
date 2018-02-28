# AGB_project
In this folder, there are two scripts written to be executed from command line, Evaluate_model.py and get_sequence_path. Here you can find a brief description of what they do and how to use them. 

##Evaluate_model.py
This script takes a dataset of DNA sequences including the 5' splice donor. Because it has been adapted to the data set we were provided with, in order assess correctly the accuracy of the generated model the splice site should be in the 21st position of the sequences. It performs an N cross-fold validation to train and test the model. For each cross-fold validation, it prints to an output specified by the user the trained model and the accuracy measures calculated.  Finally, it prints The mean of all the accuracy measures. 

Here we are going to list all the options that can be specified by command line: 

- -i --input: The name of the file from where the sequences will be provided

- -o --output: A file to write the output of the program, the default is the stdout

- -n: The number of divisions to perform the N cross-validation

- -t --toy: If set, there will only be considered one position (G) of the donor splice site

- -ex --exon: This option takes one of two values. If set to simple a simple state will be included to model the exon, if set to complex a Markov chain will be used. The default is simple

- -in --intron: This option takes one of two values. If set to simple, a simple state will be included to model the intron, if set to complex a Markov chain will be used. The default is simple

- -I --ise: This option takes one of three values. If set to simple a simple state will be included to model the ise islands, if set to complex a Markov chain will be used. The default is null. 

- -e --ese: This option takes one of three values. If set to simple a simple state will be included to model the ese islands, if set to complex a Markov chain will be used. The default is null. 

- -s --save_model: If set, the model with the closest TPR to the mean will be saved as a pickle file. 

##get_sequence_path.py
This script takes a file of sequences in plain text or a single sequence and a hidden Markov model and  returns a string with the most probable path of states for this sequence. This script only needs two arguments:

- -i --input: The name of the file from where the sequences will be provided or the sequence itelf

- -m --model: The name of the pickle file where the hmm is stored. 

In this folder, there are several pickle files generated with the previous script. Their names indicate which hidden Markov model is. 
- D6: six position donor splice sites
- tia: ise region as a simple state
- iC: intron as a Markov chain
- eC: exon as a Markov chain
- rs: ese region as a simple state
