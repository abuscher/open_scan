# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
# 
# Author:      Austin
# 
# Created:     13/10/2014
# Copyright:   (c) Austin 2014
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import sys
sys.path.append('/usr/local/lib/python3.4/site-packages')
#workaround for opencv not in pythonpath

import readPDF
from scantron import *
import write_xls


def main():

    # STEP 2: read key
    file_in = sys.argv[1]
    file_out = sys.argv[2]
    key = read_key(file_in)  # establish array of correct values
    print (key)
    outstr=''.join([str(i)+' ' for i in key])+'\n'
    f=open(file_out,'w')
    f.write(outstr)
    f.close()

if __name__ == '__main__':
    main()
