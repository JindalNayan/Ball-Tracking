import cv2
import numpy as np
import time

yellow_time = []
orange_time = []
green_time = []
white_time = []
yellow_quad = []
orange_quad = []
green_quad = []
white_quad = []

start =time.time()
text_file = open("myfile.txt", "w")
color = ["yellow","orange","green","white"]

def quadrant(x,y):
    quad = None
    if x >1260 and x<1740 and y>540 and y<1000:
        quad = 1
    elif x>790 and x<1215 and y>540 and y<1010:
        quad = 2
    elif x>800 and x<1222 and y>30 and y <500:
        quad = 3
    elif x>1260 and x<1740 and y>30 and y<500:
        quad = 4
    return quad

video = cv2.VideoCapture('AI Assignment video.mp4')

while video.isOpened():
    ret, frame = video.read()
    cv2.namedWindow("Squares and Circles", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Squares and Circles", 1280, 720)

    if ret:
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(17,17),0)

        _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw rectangles around squares
        for contour in contours:
            
            area = cv2.contourArea(contour)
            
            perimeter = cv2.arcLength(contour, True)
            
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            if len(approx) == 4 and abs(area) > 2000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Detect circles
        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1.4,90,param1=100,
        param2=35,minRadius=10,maxRadius=80)

        if circles is not None:
            circles = np.uint16(np.around(circles))

            for (x, y, rad) in circles[0, :]:
                cv2.circle(frame, (x, y), rad, (100, 255, 0), 3)
                b,g,r = frame[y, x]

                # yellow 
                if r<213 and r>57 and g>52 and g<189 and b>15 and b<63:
                    yellow_quad.append(quadrant(x,y))
                    end_yellow = time.time()
                    time_yellow_in = end_yellow - start
                    yellow_time.append(int(time_yellow_in))
                    cv2.putText(frame,color[0],(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
                    
                    try:
                        yellow_in = ['\n',color[0],' enter in ', str(yellow_time[0]),' at quadrant ',str(yellow_quad[-1]),'\n']
                        yellow_out = ['\n',color[0],' out at ', str(yellow_time[-1]),' at quadrant ',str(yellow_quad[-1]),'\n']                        
                        if yellow_time[-1] - yellow_time[-2] > 3:
                            text_file.writelines(yellow_in)
                            text_file.writelines(yellow_out)
                            yellow_time.clear()
                    except:
                        pass

                #green  
                if r<55 and r>12 and g>41 and g<77 and b>34 and b<69:
                    green_quad.append(quadrant(x, y))
                    end_green = time.time()
                    time_green_in = end_green - start 
                    green_time.append(int(time_green_in))
                    cv2.putText(frame,color[2],(x, y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
                    try:
                        green_in = ['\n',color[2]," enter in ",str(green_time[0])," at quadrant ",str(green_quad[-1]),'\n']
                        green_out = ['\n',color[2]," out at ",str(green_time[-1])," at quadrant ",str(green_quad[-1]),'\n']
                        if green_time[-1] - green_time[-2]>2:
                            text_file.writelines(green_in)
                            text_file.writelines(green_out)
                            green_time.clear()
                    except:
                         pass   
                      
                #orange                               
                if r<255 and r>176 and g>61 and g<167 and b>29 and b<131:
                    orange_quad.append(quadrant(x,y))
                    end_orange = time.time()
                    time_orange_in = end_orange-start
                    orange_time.append(int(time_orange_in))
                    cv2.putText(frame,color[1],(x, y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
                    try:
                        orange_in = ['\n',color[1]," enter in ",str(orange_time[0])," at quadrant ",str(orange_quad[-1]),'\n']
                        orange_out = ['\n',color[1]," out at ",str(orange_time[-1])," at quadrant ",str(orange_quad[-1]),'\n']
                        if orange_time[-1] - orange_time[-2]>2:
                            text_file.writelines(orange_in)
                            text_file.writelines(orange_out)
                            orange_time.clear()
                    except:
                         pass      
                    
                #white     
                if r<248 and r>113 and g>111 and g<246 and b>94 and b<226:
                    white_quad.append(quadrant(x,y))
                    end_white = time.time()
                    time_white_in = end_white-start
                    white_time.append(int(time_white_in))
                    cv2.putText(frame,color[3],(x, y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
                    try:
                        white_in = ['\n',color[3]," enter in ",str(white_time[0])," at quadrant ",str(white_quad[-1]),'\n']
                        white_out = ['\n',color[3]," out at ",str(white_time[-1])," at quadrant ",str(white_quad[-1]),'\n']
                        if white_time[-1] - white_time[-2]>2:
                            text_file.writelines(white_in)
                            text_file.writelines(white_out)
                            white_time.clear()
                    except:
                         pass              


        
        cv2.imshow('Squares and Circles', frame)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        break

video.release()
cv2.destroyAllWindows()