import sqlite3
from models.models import Person
import uuid
import cv2
from PIL import Image as im

def create_db():
    conn = sqlite3.connect('database/Person.db',timeout=20)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user ( id TEXT PRIMARY KEY, name TEXT NOT NULL, mobile_no INTEGER, adhar_no INTEGER, img BLOB NOT NULL, address TEXT , ptype TEXT, threat TEXT)")

def convertToBinaryData(imgfile):
    # Convert digital data to binary format
    with open(imgfile, 'rb') as file:
        blobData = file.read()
    return blobData

def insertData(name, id, adhar_no, imgfile, address, mobile_no, ptype, threat):
    try:
        sqliteConnection = sqlite3.connect('database/Person.db')
        cursor = sqliteConnection.cursor()
        print("Connected to Database")
        sqlite_insert_blob_query = """ INSERT INTO user
                                  (id, name, mobile_no, adhar_no, img, address, ptype, threat) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        # imgfile=imgfile.replace(imgfile.split('.')[0],id)
        img = convertToBinaryData(imgfile)
        # Convert data into tuple format
        # img=imgfile
        # data_tuple = (id, name, mobile_no, adhar_no, img, address,  ptype, threat)'
        cursor.execute(sqlite_insert_blob_query, (id, name, mobile_no, adhar_no, img, address,  ptype, threat))
        sqliteConnection.commit()
        print("Image and file inserted successfully into the database")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into person table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("the sqlite connection is closed")


def retrieve(new_img):
    try:
        sqliteConnection = sqlite3.connect('database/Person.db')
        cursor = sqliteConnection.cursor()
        print("Checking Record In Database ..........")
        # img = convertToBinaryData(new_img)
        # print(img)
        # fetch_query = "SELECT * FROM user WHERE name=new_img"
        cursor.execute("SELECT id,name,mobile_no,adhar_no,address,ptype,threat FROM user WHERE id=:id",{'id':str(new_img).split('.')[0]})
        result=cursor.fetchall()
        # print(result)
        out_dic={'Id':'','Name':'','Mobile No':'','Adhar No':'','Address':'', 'Person Type':'', 'Threat':''}
        for info in result:
            out_dic['Id']=info[0]
            out_dic['Name']=info[1]
            out_dic['Mobile No']=info[2]
            out_dic['Adhar No']=info[3]
            out_dic['Address']=info[4]
            out_dic['Person Type']=info[5]
            out_dic['Threat']=info[6]
        sqliteConnection.commit()
        # print("fetched successfully from the table")
        cursor.close()
        return out_dic

    except sqlite3.Error as error:
        print("Failed to fetch  data from user table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("the sqlite connection is closed")



def writeTofile(data, filename):
# Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    # print("Stored blob data into: ", filename, "\n")

def all_image():
    try:
        sqliteConnection = sqlite3.connect('database/Person.db',timeout=20)
        cursor = sqliteConnection.cursor()
        print("Connected to Database")
        cursor.execute("SELECT id,img from user")
        users=cursor.fetchall()
        img_list=[]
        for i in users:
            filename=i[0]
            img=i[1]
            # print(img)
            # imgfile = im.fromarray(img)
            # imgfile = imgfile.save(filename+'.jpg')
            writeTofile(img, 'image_list/'+filename+'.jpg')


    except sqlite3.Error as error:
        print("Failed to fetch  data from the database", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("the sqlite connection is closed")

            

# if __name__ == "__main__":
    #Database Creation
create_db()
#Loading all images from database to compare 
all_image()

# name=input("Enter the name:\t")
# id=str(uuid.uuid4())
# adhar_no=int(input("Enter the adhar no:\t"))
# mobile_no=int(input("Enter your mobile no:\t"))
# address=input("Enter your address:\t")
# ptype=input("Person type:\t")
# threat=input("Threat YES | NO:\t")
# imgfile=input("Enter the image file path:\t")
# per=Person(name, id, adhar_no, imgfile, address, mobile_no, ptype, threat)


# insertData(per.name, per.id, per.adhar_no, per.imgfile, per.address, per.mobile_no, per.ptype, per.threat)
