"""The main body of the code to classify galaxies. This consists of the main function called
to begin classification
"""

import sys
import classify_lib as cll


def main():
    """Begin the classification or training process

    Command Line Arguments
    ----------------------
    runtype : {train, classify}, str
        The mode you would like to run the code in.
        train - Classify the training set and get graded
        classify - Perform the classification
    """

    if len(sys.argv) < 2:
        raise Exception('Please call with command line args \'train\' or \'classify\' ')
    runtype = sys.argv[1]

    if runtype.lower() == 'train':
        cll.run_train()
    elif runtype.lower() == 'classify':
        cll.run_classify()
    else:
        raise Exception('Please call with command line args \'train\' or \'classify\' ')


if __name__ == '__main__':
    main()
