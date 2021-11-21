import cv2
import glob2
from time import time, sleep

def transparentOverlay(src, overlay, pos=(0, 0), scale=0.2):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image

    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src


def addImageWatermark(logo_name,img_name,opacity,pos=(10,10)):
    opacity = opacity / 100

    img = cv2.imread(img_name)
    logo = cv2.imread(logo_name, -1)

    h, w, d = img.shape
    print(img.shape)
    #Tính toán điều chỉnh ảnh
    cut1_h = round(abs((min(h,w) - h)/2) + 0.5)
    cut2_h = round(abs((min(h,w) - h)/2) - 0.5)
    cut1_w = round(abs((min(h,w)  - w)/2) + 0.5)
    cut2_w = round(abs((min(h,w)  - w)/2) - 0.5)
    #Cắt ảnh về hình vuông
    img = img[cut1_h:(h-cut2_h), cut1_w:(w-cut2_w)]
    #resize ảnh về 500x500
    img = cv2.resize(img, (500,500))

    tempImg = img.copy()

    overlay = transparentOverlay(tempImg, logo, pos)
    output = img.copy()
    # apply the overlay
    cv2.addWeighted(overlay, opacity, output, 1 - opacity, 0, output)

    #Lưu ảnh vào thư mục Anh_dich
    #Gắn tên và thư mục đích cho ảnh đã có logo
    img_newname = img_name.replace('Anh_goc', 'Anh_dich')
    #Lưu ảnh mới vào Anh_dich
    cv2.imwrite(img_newname, output)

#Lấy danh sách ảnh trong thư mục Anh_goc
list_img_jpg = glob2.glob(".\Anh_goc\*.jpg")
list_img_png = glob2.glob(".\Anh_goc\*.png")

for img_jpg_name in list_img_jpg:

    #Ghép logo vào ảnh đã resize
    addImageWatermark('./logo.png',img_jpg_name,100,(10,10))

for img_png_name in list_img_png:

    #Ghép logo vào ảnh đã resize
    addImageWatermark('./logo.png',img_png_name,100,(10,10))

