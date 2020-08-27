import cv2
import imutils
import numpy as np
 
image = cv2.imread("iks-oks.jpg")
image= cv2.resize(image,(1783,1764))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
jezgro =  np.ones((7,7),np.uint8)
resenje=[]
ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, jezgro)
cnts = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


cnts = imutils.grab_contours(cnts)


for (i, c) in enumerate(cnts):
	
    if (cv2.contourArea(c)>20000 and cv2.contourArea(c)<180000): #14000 ili 20000
	    area = cv2.contourArea(c)
	    (x, y, w, h) = cv2.boundingRect(c)
     
	    
	    hull = cv2.convexHull(c)
	    hullArea = cv2.contourArea(hull)
	    solidity = area / float(hullArea)
        # initialize the character text
	    char = " "
     
	    
	    if solidity > 0.90:
		    char = "O"
     
	    
	    elif solidity>0.3:
		    char = "X"
     
	    resenje.append(char)
	    if char != " ":
		    cv2.drawContours(image, [c], -1, (0, 255, 0), 3)
		    cv2.putText(image, char, (x+10, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 10,
			    (255, 255, 0), 4)
     
	    
	    print("{} (Contour #{}) -- solidity={:.2f}".format(char, i + 1, solidity))
 


image= cv2.resize(image,(500,500))
cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()


