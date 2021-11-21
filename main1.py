import cv2
import imutils
import glob2
from time import time, sleep

#Tạo layer mask cho ảnh logo
logo = cv2.imread('logo_viettool.png')
 
logo = imutils.resize(logo, width=125)
logoGray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
logoMask = cv2.threshold(logoGray, 200, 255, cv2.THRESH_BINARY)[1]
logoMask = cv2.erode(logoMask, None, iterations=0)
logo = cv2.bitwise_and(logo, logo, mask=cv2.bitwise_not(logoMask))

#Lấy danh sách ảnh trong thư mục Anh_goc
path = ".\Anh_goc"
path2 = ".\Anh_dich"
list_img = glob2.glob(".\Anh_goc\*.jpg")

#Ghép logo
offset = 20
for img_name in list_img:

    #Resize ảnh:
    #Lấy size ảnh
    img = cv2.imread(img_name)
    print(img_name)
    h, w, d = img.shape
    print(img.shape)
    #Tính toán điều chỉnh ảnh
    cut1_h = round(abs((min(h,w) - h)/2) + 0.5)
    cut2_h = round(abs((min(h,w) - h)/2) - 0.5)
    cut1_w = round(abs((min(h,w)  - w)/2) + 0.5)
    cut2_w = round(abs((min(h,w)  - w)/2) - 0.5)
    #Cắt ảnh về hình vuông
    img = img[cut1_h:(h-cut2_h), cut1_w:(w-cut2_w)]
    print(img.shape)
    #resize ảnh về 500x500
    img = cv2.resize(img, (500,500))
    print(img.shape)


    #Ghép logo vào ảnh đã resize
    ROI = img[offset:logo.shape[0]+offset, offset:logo.shape[1]+offset]
    ROI = cv2.bitwise_and(ROI,ROI,mask=logoMask)
    img[offset:logo.shape[0]+offset, offset:logo.shape[1]+offset] = cv2.add(ROI,logo)


    #Lưu ảnh vào thư mục Anh_dich
    #Gắn tên và thư mục đích cho ảnh đã có logo
    img_newname = img_name.replace('Anh_goc', 'Anh_dich')
    #Lưu ảnh mới vào Anh_dich
    cv2.imwrite(img_newname, img)

    #break

while True:
    cv2.waitKey(1)
    cv2.imshow('img', img)
    cv2.imshow('logo', logo)