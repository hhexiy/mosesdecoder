#!/usr/bin/env python3 -*- coding: utf-8 -*-

"""
The Gacha filter cleans out sentence pairs that have global character mean
lower than a certain threshold. 
 
Use this cleaner to produce low quantity of high quality sentence pairs. 

It is an aggressive cleaner that cleaned out ~64% of the HindEnCorp during 
WMT14 when threshold is set at 20% (Tan and Pal, 2014); achieving lowest TER.  
(see http://www.aclweb.org/anthology/W/W14/W14-3323.pdf)

This is inspired by the global character mean that is used in the Gale-Church
algorithm (Gale aand Church, 1993), the c variable in:

    delta = (l2-l1*c)/math.sqrt(l1*s2)

where:
 - l1 = len(source_sentence)
 - l2 = len(target_sentence)
 - c = global mean, i.e. #char in source corpus / #char in target corpus
 - s2 = global variance, i.e. d ((l1 - l2)^2) / d (l1)

(For details on Gale-Church, see http://www.aclweb.org/anthology/J93-1004.pdf)

USAGE:

    $ python3 gacha_filter.py train.en train.de

Outputs to STDOUT a separated lines of the source and target sentence pairs. 
You can simply cut the file after that. 

    $ python3 gacha_filter.py train.en train.de > train.en-de
    $ cut -f1 train.en-de > train.clean.en
    $ cut -f2 train.en-de > train.clean.de

You can also allow lower threshold to yield more lines:

    $ python3 gacha_filter.py train.en train.de 0.05
    
Default threshold is set to 0.2.
"""

import io, subprocess

red = '\033[01;31m'
native = '\033[m'

def err_msg(txt):
    return red+txt+native

def num_char(filename):
    return float(subprocess.Popen(["wc", "-m", filename], 
                            stdout=subprocess.PIPE).stdout.read().split()[0])

def gacha_mean(sourcefile, targetfile):
    """
    Counts the global character mean between source and target language as
    in Gale-Church (1993)
    """
    sys.stderr.write(err_msg('Calculating Gacha mean, please wait ...\n'))
    c = num_char(sourcefile) / num_char(targetfile)
    sys.stderr.write(err_msg('Gacha mean = '+str(c)+'\n'))
    sys.stderr.write(err_msg('Filtering starts ...\n'))
    return c

def main(sourcefile, targetfile, threshold=0.2):
    # Calculates Gacha mean.
    c = gacha_mean(sourcefile, targetfile)
    # Calculates lower and upperbound for filtering
    threshold = float(threshold)
    lowerbound = (1-threshold) * c
    upperbound = (1+threshold) * c
    
    # Start filtering sentences.
    with io.open(sourcefile, 'r', encoding='utf8') as srcfin, \
    io.open(targetfile, 'r', encoding='utf8') as trgfin:
        for s, t in zip(srcfin, trgfin):
            if lowerbound < len(s) / float(len(t)) < upperbound:
                print(u"{}\t{}".format(s.strip(),t.strip()))

if __name__ == '__main__':
    import sys
    if len(sys.argv) not in range(3,5):
        usage_msg = err_msg('Usage: python3 %s srcfile trgfile (threshold)\n'
                            % sys.argv[0])
        
        example_msg = err_msg('Example: python3 %s ~/Europarl.de-en.de '
                              '~/Europarl.de-en.en 0.4\n' % sys.argv[0])
        sys.stderr.write(usage_msg)
        sys.stderr.write(example_msg)
        sys.exit(1)
        
    main(*sys.argv[1:])
