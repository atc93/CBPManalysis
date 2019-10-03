import numpy as np
import math

def welcome_message():

    print('')
    print(' ------------------------------')
    print(' |                            |')
    print(' |       CBPM ANALYSIS        |')
    print(' |                            |')
    print(' | contact: atc93@cornell.edu |')
    print(' |                            |')
    print(' ------------------------------')
    print('')

def analyzed_cbpm(cbpm):

    print('\n\n <<<<---------------------->>>>')
    if len(cbpm) == 4:
        print(' <<<< Analyzing CBPM:', cbpm, '>>>>')
    if len(cbpm) == 3:
        print(' <<<< Analyzing CBPM:', cbpm, ' >>>>')
    print(' <<<<---------------------->>>>')

# print statistical information
def print_stat(data):
    print('   mean: {0:0.5f}'.format(np.mean(data))
          , ' +- {0:0.5f}'.format(np.std(data) / math.sqrt(len(data))) # mean standard error is sigma/sqrt(N)
          , '(SE), std: {0:0.5f}'.format(np.std(data))
          , '+- {0:0.5f} (SE)'.format(np.std(data) / math.sqrt(2 * len(data) - 2)) # std standard error is sigma/sqrt(2N-1)
          , ', std/mean: {0:0.5f}'.format(np.std(data) / np.mean(data)))