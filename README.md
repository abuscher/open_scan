# open_scan
A set of tools to create multiple choice tests, grade them, and write results to an excel file.  

Runs in Python27.

Requires OpenCV2, xlwt, and numpy.  The modules xlwt and numpy can be installed with pip.

OpenCV3 can be used, scantron.py just needs each cv2 replaced with cv3 and cv.findContours needs 3 return values (first one ignored)

OpenCV installation is less trivial.  Download version 3.0 or newer.  See downloads page here: http://opencv.org/downloads.html

For installation on linux see here: http://docs.opencv.org/doc/tutorials/introduction/linux_install/linux_install.html 
and here: http://milq.github.io/install-opencv-ubuntu-debian/ (ubuntu)

For windows installation see here: http://docs.opencv.org/doc/tutorials/introduction/windows_install/windows_install.html
