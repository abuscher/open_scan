import os
from tempfile import TemporaryFile
from xlwt import Workbook, Formula, XFStyle

def write(folder,key, all_ID, all_score, all_correct, all_answer):

    letters = ['A', 'B', 'C', 'D', 'E', 'X', 'M']
    num_students = len(all_ID)
    num_problems = len(key)

    book = Workbook()
    sheet1 = book.add_sheet('Score Summary')

    sheet1.col(0).width = 3000
    sheet1.col(1).width = 3000
    sheet1.col(2).width = 3000
    sheet1.col(3).width = 500
    sheet1.col(4).width = 5000
    sheet1.col(5).width = 3000
    sheet1.col(6).width = 3000

    sheet1.write(0, 0, 'Student ID')  # A1
    sheet1.write(0, 1, 'Raw Score')   # B1
    sheet1.write(0, 2, 'Percentage')  # B1

    pstyle = XFStyle()
    pstyle.num_format_str = '0.00%'
    dstyle = XFStyle()
    dstyle.num_format_str = '0.00'

    for j in range(num_students):
        ID = all_ID[j]
        score = all_score[j]
        sheet1.row(j+1).set_cell_number(0, ID)
        sheet1.row(j+1).set_cell_number(1, score)
        sheet1.row(j+1).set_cell_number(2, score/float(num_problems), pstyle)

    sheet1.write(0, 4, 'Test Score Statistics')
    sheet1.write(0, 5, 'Raw Score')
    sheet1.write(0, 6, 'Percentage')
    sheet1.write(1, 4, 'Mean')
    sheet1.write(2, 4, 'Median')
    sheet1.write(3, 4, 'Max')
    sheet1.write(4, 4, 'Min')
    sheet1.write(5, 4, 'Standard Deviation')

    mean_score = 'AVERAGE(B%d:B%d)' % (2, 1+num_students)
    median_score = 'MEDIAN(B%d:B%d)' % (2, 1+num_students)
    max_score = 'MAX(B%d:B%d)' % (2, 1+num_students)
    min_score = 'MIN(B%d:B%d)' % (2, 1+num_students)
    stdev = 'STDEV(B%d:B%d)' % (2, 1+num_students)

    sheet1.write(1, 5, Formula(mean_score), dstyle)
    sheet1.write(2, 5, Formula(median_score), dstyle)
    sheet1.write(3, 5, Formula(max_score), dstyle)
    sheet1.write(4, 5, Formula(min_score), dstyle)
    sheet1.write(5, 5, Formula(stdev), dstyle)

    mean_score = 'AVERAGE(C%d:C%d)' % (2, 1+num_students)
    median_score = 'MEDIAN(C%d:C%d)' % (2, 1+num_students)
    max_score = 'MAX(C%d:C%d)' % (2, 1+num_students)
    min_score = 'MIN(C%d:C%d)' % (2, 1+num_students)
    stdev = 'STDEV(C%d:C%d)' % (2, 1+num_students)

    sheet1.write(1, 6, Formula(mean_score), pstyle)
    sheet1.write(2, 6, Formula(median_score), pstyle)
    sheet1.write(3, 6, Formula(max_score), pstyle)
    sheet1.write(4, 6, Formula(min_score), pstyle)
    sheet1.write(5, 6, Formula(stdev), pstyle)

    col_totals = [sum(x) for x in zip(*all_correct)]

    sheet2 = book.add_sheet('Test Diagnostics')
    sheet2.col(0).width = 3000
    sheet2.col(1).width = 3000
    sheet2.col(2).width = 2000
    sheet2.col(3).width = 500
    sheet2.col(4).width = 5000
    sheet2.col(5).width = 5000

    sheet2.write(0, 0, 'Problem')    # A1
    sheet2.write(0, 1, '% Correct')  # B1

    for i in xrange(len(key)):
        sheet2.row(i+1).set_cell_number(0, i+1)
        sheet2.row(i+1).set_cell_number(1, col_totals[i]/float(num_students), pstyle)

# SHEET 3
    sheet3 = book.add_sheet('Answer Summary')
    sheet3.col(0).width = 3000
    sheet3.col(1).width = 2000

    sheet3.write(0, 0, 'Problem #')  # A1
    sheet3.write(0, 1, 'Key')        # A1
    for j in range(len(all_ID)):
        sheet3.col(j+2).width = 2000
        ID = all_ID[j]
        sheet3.row(0).set_cell_number(j+2, ID)
        for i in xrange(len(key)):
            sheet3.write(i+1, j+2, letters[all_answer[j][i]])

    for i in xrange(len(key)):
        sheet3.row(i+1).set_cell_number(0, i+1)
        sheet3.write(i+1, 1, letters[key[i]])

    fout=os.path.join(folder,'grades.xls')

    book.save(fout)
    book.save(TemporaryFile())
