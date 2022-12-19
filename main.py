from face_verification import verify
from multi_crop import crop_face
import json
import sys


def main():

    # Direct command line input path
    # imagePath= sys.argv[1]

    #After excution input image path
    imagePath = input("Enter you image path:\t")

    get_img=crop_face(imagePath)
    verify(get_img)

    # return Input_Image





if __name__=='__main__':
    main()




