#! /usr/bin/env python3
import easyocr
import cv2
from matplotlib import pyplot as plt



read = easyocr.Reader(['en'], gpu = False)
img = cv2.imread("prueba_foto.jpg")

#vid = cv2.VideoCapture("pruebafoto.jpg")
skip_frame = True

while (True):
	#ret, img = vid.read()

	#gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	#result = read.readtext(gray)
	#Colocar nombre de la foto que se quiera analizar
	result = read.readtext("prueba_foto.jpg")
	text = ""
	for res in result:
		text += res[1] + ""

	im_top_left = tuple(result[0][0][0])
	im_bottom_right = tuple(result[0][0][2])
	im_text = result[0][1]
	font = cv2.FONT_HERSHEY_SIMPLEX
	print(type(text))
	
	img = cv2.rectangle(img, im_top_left,im_bottom_right,(50,50,355),5)
	img = cv2.putText(img, text, (50,70),cv2.FONT_HERSHEY_SIMPLEX, 1, (50,50,255),2)
	if cv2.waitKey(1) & 0xFF == ord('s'):
		break
	#plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
	plt.imshow(img)
	plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
	plt.show()
cv2.destroyAllWindows()


