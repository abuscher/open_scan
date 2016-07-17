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
    folder = sys.argv[1]#"test_folder2"  # folder is the folder where images are written.
    xls = True

    # STEP 1: read in pdf, split into jpegs
    #keyPath = os.path.join(folder, "tests.pdf")

    [folder, num_students] = readPDF.process("tests.pdf", folder)  # 2nd arg is outfolder
    # image names will be key.jpg, 0.jpg, 1.jpg, 2.jpg, etc.
    # return_message = "Successfully read PDF"
    # print return_message

    # STEP 2: read key
    file_key = os.path.join(folder, "key.jpg")
    print(file_key)
    key = read_key(file_key)  # establish array of correct values

    # STEP 3: loop scanned tests
    if xls:
        all_answer = []
        all_correct = []
        all_id = []
        all_score = []
    for i in range(1000):
        file_name = "%d.jpg"%i
        full_path = os.path.join(folder, file_name)
        print(full_path)
        if not os.path.isfile(full_path):
            break
        score, correct_list, id, answer_list = grade_test(full_path, key, xls)  
        # return student id and score
        if xls:
            all_correct.append(correct_list)
            all_answer.append(answer_list)
            all_id.append(id)
            all_score.append(score)
            write_xls.write(folder,key, all_id, all_score, all_correct, all_answer)

    #return_message = "Successfully graded tests"
    #print (return_message)

if __name__ == '__main__':
    main()
