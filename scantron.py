import numpy as np
import cv2
import os

# constants for current scantron version
NUM_PROB = 100
NUM_COL = 2
TEST_NUM_OPTIONS = 5
NUM_GAPS = 4
ID_LENGTH = 5
ID_NUM = 5
NUM_PROB_COL = NUM_PROB / NUM_COL
PROB_PER_GROUP = NUM_PROB_COL / (NUM_GAPS+1)

def x_low(tri):  
    return min([tri[0][0], tri[1][0], tri[2][0]])


def x_high(tri): 
    return max([tri[0][0], tri[1][0], tri[2][0]])


def y_low(tri):  
    return min([tri[0][1], tri[1][1], tri[2][1]])


def y_high(tri): 
    return max([tri[0][1], tri[1][1], tri[2][1]])


def check_cell_old(img, point, cell_width):
    start = [point[0]-cell_width / 2, point[1]-cell_width / 2]
    count = 0
    threshold = float(cell_width**2)
    for x in range(cell_width):
        for y in range(cell_width):
            point_check = [start[0]+x, start[1]+y]
            pixel = img[point_check[1], point_check[0]]
            if pixel<128:
                count += 1
    if count / threshold > .4:
        return True
    else:
        return False


def check_cell(img, point, width):
    threshold = width*width*256.
    hw = width / 2
    spot = img[point[1]-hw:point[1]+hw, point[0]-hw:point[0]+hw]
    total_sum = sum(sum(x) for x in spot)
    if total_sum / threshold<.8:
        return True
    else:
        return False


def minmax_xy(tri, xoy, mm):
    #  returns the index of the min, as opposed to min value
    trixy = [tri[0][xoy], tri[1][xoy], tri[2][xoy]]
    if mm == 'min': 
        return tri[trixy.index(min(trixy))]
    if mm == 'max': 
        return tri[trixy.index(max(trixy))]


def grade_test(pfile, key, xls = False):
    img, points, fullLength, full_width, cell_width, length1, width1 = read_file(pfile)
    ID = read_ID(img, points, cell_width, length1, width1)
    num_problems = len(key) # different from NUM_PROB_COL, a test could have 20 questions on a 100 question scantron
    total_correct = 0
    if xls:
        correct_list = [False]*num_problems
        answer_list = [False]*num_problems
    for problem in range(num_problems):
        if problem<NUM_PROB_COL: # only good for two columns
            startPoint = points[0]
        else:
            startPoint = points[3]
        gap_offset = (problem % NUM_PROB_COL) / PROB_PER_GROUP
        y = startPoint[1]+int(length1*(problem % NUM_PROB_COL+gap_offset)) # y doesnt change for a given problem, only x

        numfill = 0
        correct_checked = False
        for letter in range(5):
            x = startPoint[0]+int(width1*letter)
            filled = check_cell(img, (x, y), cell_width)
            if filled:
                numfill += 1
                boxChecked = letter
                if letter == key[problem]:# and numfill == 1:
                    correct_checked = True
            if numfill > 1: break
        correct = False
        if numfill == 1:
            if xls: answer_list[problem] = boxChecked
            if correct_checked: 
                correct = True
        elif numfill > 1:
            if xls: 
                answer_list[problem] = 5
        else:  # numfill == 0
            if xls: 
                answer_list[problem] = 6
        if correct:
            total_correct += 1
            if xls: 
                correct_list[problem] = True
    #print("ID number:", ID)
    #print("Number Correct:", total_correct, " / ", num_problems)
    print "ID number:", ID
    print "Number Correct:", total_correct, " / ", num_problems
    if xls:
        return total_correct, correct_list, ID, answer_list
#    cv2.namedWindow("img Window", cv2.WINDOW_NORMAL)
#    cv2.imshow("img Window", img)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

def read_ID(img, points, cell_width, length1, width1):

    ID = 0
    totalFill = 0
    startPoint = points[6]

    for letter in range(ID_LENGTH):
        num_fill = 0
        x = startPoint[0]+int(width1*letter)
        for problem in range(ID_NUM):
            y = startPoint[1]+int(problem*length1)
            filled = check_cell(img, (x, y), cell_width)
            if filled:
                num_fill += 1
                if num_fill == 1:
                    ID += 10**(4-letter)*(problem+1) # APPEND ID
 #               cv2.rectangle(img, (x-a, y-a), (x+a, y+a), (255, 0, 0), thickness = -1)
 #           else:
 #               cv2.rectangle(img, (x-a, y-a), (x+a, y+a), (255, 0, 255), thickness = -1)
            if num_fill > 1:
                print ("error: more than 1 bubble marked")

#    cv2.namedWindow("img Window", cv2.WINDOW_NORMAL)
#    cv2.imshow("img Window", img)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

    return ID

def read_key(pfile):
    img, points, fullLength, fullWidth, cellWidth, length1, width1 = read_file(pfile)
    key = []
    # a = (cellWidth / 2-3) / 2 for plotting
    for problem in range(NUM_PROB):
        if problem<NUM_PROB_COL:
            startPoint = points[0] # first column
        else:
            startPoint = points[3] # second column
        gap_offset = (problem % NUM_PROB_COL) / PROB_PER_GROUP
        y = startPoint[1]+int(length1*(problem % (NUM_PROB_COL)+gap_offset))

        # y, xList = find_xy_spot(problem, points, startPoint)
        num_fill = 0
        for letter in range(5):
            x = startPoint[0]+int(width1*letter)
            filled = check_cell(img, (x, y), cellWidth)
            if filled:
                num_fill += 1
                if num_fill == 1: key = key+[letter]
#                cv2.rectangle(img, (x-a, y-a), (x+a, y+a), (255, 255, 255), thickness = 4)
#            else:
#                cv2.rectangle(img, (x-a, y-a), (x+a, y+a), (0, 0, 0), thickness = 4)
            if num_fill > 1:
                print ("error: more than 1 bubble marked on", problem+1)
        if num_fill == 0:
            #print ("Number of problems read in key:", problem)
            print "Number of problems read in key:", problem
            break

#    cv2.namedWindow("img Window", cv2.WINDOW_NORMAL)
#    cv2.imshow("img Window", img)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
    return key


def read_file(pfile):
    img = cv2.imread(pfile)
    gray = cv2.imread(pfile, 0)
    dim = [len(img), len(img[1])]
    avg = sum(dim) / 2

    ret, thresh = cv2.threshold(gray, 127, 255, 1)
    _, contours, h = cv2.findContours(thresh, 1, 2)
    tris = []

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx) == 3 and cv2.arcLength(cnt, True) > avg / 10:
            tris.append([list(approx[0][0]), list(approx[1][0]), list(approx[2][0])])
            cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)

    if tris[0][0] > tris[1][0]:
        tris[:2] = [tris[1], tris[0]]

    # use triangles to determine rotation
    r1 = minmax_xy(tris[1], 0, 'min')
    r2 = minmax_xy(tris[0], 0, 'min')
    r3 = minmax_xy(tris[4], 0, 'min')
    r4 = r1
    r5 = [r3[0], r1[1]]
    r6 = r3

# rotate
    rows, cols, ch = img.shape
    pts1 = np.float32([r1, r2, r3])
    pts2 = np.float32([r4, r5, r6])
    M = cv2.getAffineTransform(pts1, pts2)
    img = cv2.warpAffine(img, M, (cols, rows))
    gray = cv2.warpAffine(gray, M, (cols, rows))

    ret, thresh = cv2.threshold(gray, 127, 255, 1)
    _, contours, h = cv2.findContours(thresh, 1, 2)

# find points
    ret, thresh = cv2.threshold(gray, 127, 255, 1)
    _, contours, h = cv2.findContours(thresh, 1, 2)
    tris = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx) == 3 and cv2.arcLength(cnt, True) > avg / 10:
            tris.append([list(approx[0][0]), list(approx[1][0]), list(approx[2][0])])
            cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)

    if tris[0][0] > tris[1][0]:
        tris[:2] = [tris[1], tris[0]]

    p1 = [x_low(tris[4]), y_low(tris[3])]  # 1A
    p2 = [p1[0], y_high(tris[2])]         # 1E
    p3 = [x_high(tris[4]), p1[1]]          # 50A

    p4 = [x_low(tris[1]), p1[1]]           # 51A
    p5 = [p4[0], p2[1]]                    # 51E
    p6 = [x_high(tris[1]), p1[1]]          # 100A

    p7 = [x_low(tris[1]), y_low(tris[4])]  # ID11, top left
    p8 = [p7[0], y_high(tris[4])]          # ID51, bottom left
    p9 = [x_high(tris[1]), p8[1]]          # ID55, bottom right

    points = [p1, p2, p3, p4, p5, p6, p7, p8, p9]

    full_length = points[1][1]-points[0][1]
    full_width = min(points[2][0]-points[0][0], points[8][0]-points[7][0])
    cell_width = full_width*2 / (4*TEST_NUM_OPTIONS-4) # 16 for 5, 
    length1 = float(full_length) / float(NUM_PROB_COL+NUM_GAPS-1)
    width1 = float(full_width) / float(TEST_NUM_OPTIONS-1)

    return gray, points, full_length, full_width, cell_width, length1, width1

def main():
    import time
    start_t = time.clock()
    print (start_t)
    folder = "input2"

    fkey = os.path.join(folder, "key.jpg")
    key = read_key(fkey)

    start_t = time.clock()
    print (start_t)

    for i in range(10000):
        fname = "%d.jpg" % i
        ftest = os.path.join(folder, fname)
        #print ftest, os.path.isfile(ftest)
        if not os.path.isfile(ftest): 
            break
        grade_test(ftest, key)
    start_t = time.clock()
    print (start_t)
if __name__ ==  '__main__':
    main()

# cv2.circle(img, (x, y), 10, (0, 0, 255), thickness = cell_width / 2)
