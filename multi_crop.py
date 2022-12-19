import cv2
import sys

# imagePath = input("Enter you image path:\t")

# image = cv2.imread(imagePath)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# faces = faceCascade.detectMultiScale(
#     gray,
#     scaleFactor=1.3,
#     minNeighbors=3,
#     minSize=(30, 30)
# )

# print("[INFO] Found {0} Faces.".format(len(faces)))

def crop_face(imagePath):

    # imagePath = input("Enter you image path:\t")

    image = cv2.imread(imagePath)
    cv2.resize(image, (720, 1080))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(20, 20)
    )

    print("[INFO] Found {0} Faces.".format(len(faces)))

    upload_img_path=[]
    for (x, y, w, h) in faces:
        cut_face=image[y:y + h, x:x + w]
        bigger_face = cv2.resize(cut_face, (256, 256))
        # bigger_face=cut_face
        #----------------------------------------------------
        # print("[INFO] Object found. Saving locally.")
        croped_store_path='croped_Images/'+str(w) + str(h) + '_faces.jpg'

        upload_img_path.append(croped_store_path)
        cv2.imwrite(croped_store_path, bigger_face)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # roi_color = image[y:y + h+20, x:x + w]
        # print("[INFO] Object found. Saving locally.")
        # cv2.imwrite('hold/'+str(w) + str(h) + '_faces.jpg', cut_face)
        #-----------------------------------------------------
    status = cv2.imwrite('Framed_image/faces_detected.jpg', image)
    # print("[INFO] Image faces_detected.jpg written to filesystem: ", status)
    return upload_img_path