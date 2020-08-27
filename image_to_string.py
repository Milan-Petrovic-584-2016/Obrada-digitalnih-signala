import numpy as np
import cv2

#Stvoriti 2D niz da drži sva stanja na tabli iks-oks 
resenje = [[" "," "," "],[" "," "," "],[" "," "," "]]

#jezgro koristimo za uklanjanje šuma
jezgro =  np.ones((7,7),np.uint8)

# Učitamo sliku u boji
img = cv2.imread('X.jpg',1)

# dobijamo širinu i visinu slike
img_sirina = img.shape[0]
img_visina = img.shape[1]

# Sliku skaliramo sa sivom bojom
img_g =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Uključi binarni prag
ret,thresh1 = cv2.threshold(img_g,127,255,cv2.THRESH_BINARY)

#Obristi šum od binarnog praga
thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, jezgro)

#Pronaći konture. RETR_EXTERNAL uzima samo spljne konture.
contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


tileCount = 0
for cnt in contours:
        # Površina konture veče od 0, onda je to kontura
        if cv2.contourArea(cnt) > 0: 
                tileCount += 1
                # koristimo boundingrect da dobijemo kordinate od pločice
                x,y,w,h = cv2.boundingRect(cnt)
               
               
                #stvaramo novu sliku od binary, za buduće analize.Brišemo ivicu sa linijom
                tile = thresh1[x+40:x+w-80,y+40:y+h-80]
                

                #određujemo indeks pločice
                tileX = round((x/img_sirina)*3)
                tileY = round((y/img_visina)*3)     

                # find contours in the tile image. RETR_TREE retrieves all of the contours and reconstructs a full hierarchy of nested contours.
                #Pronaći konturu u slici pločice. ETR_TREE dohvata sve konture i rekonstrujiše potpunu hijerarhiju ugniježđenih kontura.
                c, hierarchy = cv2.findContours(tile, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
                for ct in c:
                        # Da proverimo da li je pronaša konturu
                        if cv2.contourArea(ct) < 180000:
                                #Računamo solitnost
                                area = cv2.contourArea(ct)
                                hull = cv2.convexHull(ct)
                                hull_area = cv2.contourArea(hull)
                                solidity = float(area)/hull_area

                                # popunjujemo resenje sa pravim znakom
                                if(solidity > 0.5):
                                        resenje[tileX][tileY] = "O"
                                else: 
                                        resenje[tileX][tileY] = "X"
                


print("resenje:")
for line in resenje:
        linetxt = ""
        for cel in line:
                linetxt += "|" + cel
        print(linetxt)

  


