import sys
import classify_lib as cll

def main():
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