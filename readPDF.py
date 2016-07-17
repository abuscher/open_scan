def process(filein,folder):
    import os
    #pdf = file(os.path.join(folder,filein), "rb").read()
    
    f=open(os.path.join(folder,filein), "rb")
    pdf=f.read()

    start_mark = b'\xff\xd8'
    start_fix = 0
    end_mark = b'\xff\xd9'
    end_fix = 2
    i = 0

    num_jpg = 0
    while True:
        istream = pdf.find(b'stream', i)
        if istream < 0:
            break
        istart = pdf.find(start_mark, istream, istream+20)
        if istart < 0:
            i = istream+20
            continue
        iend = pdf.find(b'endstream', istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(end_mark, iend-20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")

        istart += start_fix
        iend += end_fix
        jpg = pdf[istart:iend]
        if num_jpg == 0:
            name = "key.jpg"
        else:
            name = "%d.jpg" % (num_jpg-1)
        if not os.path.exists(folder):
            os.makedirs(folder)
        fileout = os.path.join(folder, name)
        jpg_file = open(fileout, "wb")
        jpg_file.write(jpg)
        jpg_file.close()

        num_jpg += 1
        i = iend
    students = num_jpg-1
    return folder, students


def main():
    folder,students=process('tests.pdf','input1')
    print(folder)
    print(students)

if __name__ == '__main__':
    main()
