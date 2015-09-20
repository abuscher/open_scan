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

# import os
import sys
import readPDF
from scantron import *
import write_xls


def main():
    # inputs
#    print sys.argv[1]
    folder = sys.argv[1]#"test_folder2"  # folder is the folder where images are written.
    xls = True

    # STEP 1: read in pdf, split into jpegs
    try:
        keyPath = os.path.join(folder, "tests.pdf")
        [folder, num_students] = readPDF.process(keyPath, folder)  # 2nd arg is outfolder
        # image names will be key.jpg, 0.jpg, 1.jpg, 2.jpg, etc.
        # return_message = "Successfully read PDF"
    except:
        return_message = "Error reading pdf"
        # print return_message
        sys.exit(return_message)

    # STEP 2: read key
    try:
        file_key = os.path.join(folder, "key.jpg")
        key = read_key(file_key)  # establish array of correct values
    except:
        return_message = "Error processing key"
        sys.exit(return_message)

    # STEP 3: loop scanned tests
    try:
        if xls:
            all_answer = []
            all_correct = []
            all_id = []
            all_score = []
        for i in range(1000):
            file_name = "%d.jpg"%i
            full_path = os.path.join(folder, file_name)
            if not os.path.isfile(full_path):
                break
            score, correct_list, id, answer_list = grade_test(full_path, key, xls)  # return student id and score
            if xls:
                all_correct.append(correct_list)
                all_answer.append(answer_list)
                all_id.append(id)
                all_score.append(score)

            write_xls.write(folder,key, all_id, all_score, all_correct, all_answer)

    except:
        return_message = "Error processing tests"
        sys.exit(return_message)

    return_message = "Successfully graded tests"
    print (return_message)

if __name__ == '__main__':
    main()
