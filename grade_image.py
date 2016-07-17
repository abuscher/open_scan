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
    # inputs
    key_file = sys.argv[1]
    img_file = sys.argv[2]
    key_type = sys.argv[3]

    # STEP 2: read key from file
    if key_type=='text':
        f=open(key_file)
        in_str=f.readline()
        key=[int (i) for i in in_str.split()]
    else:
        key = read_key(key_file)  # establish array of correct values
    
    # STEP 3: loop scanned tests
    xls=True
    score, correct_list, id, answer_list = grade_test(img_file, key, xls)
    correct_list=str1=''.join([str(int(i)) for i in correct_list])
    key_list=str1=''.join([str(i) for i in key])
    answer_list=str1=''.join([str(i) for i in answer_list])
    print (id, score, answer_list, key_list)

    #return_message = "Successfully graded tests"
    #print (return_message)

if __name__ == '__main__':
    main()
