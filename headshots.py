import cv2


#Set the name of the particpant here, which will create a folder with the name set here
name = 'ParticpantOne'

#Start the video capture on the camera
cam = cv2.VideoCapture(0)

#setup the variables for the video feed
cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo", 500, 300)

#Counter for the number of images
img_counter = 0

#Loop until the video feed is stopped
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("press space to take a photo", frame)
    #ESC button is pressed, will close the video feed and end the program
    k = cv2.waitKey(1)
    if k%256 == 27:
        print("Escape hit, closing...")
        #Exits from the loop
        break
    #SPACE button is pressed, will take a snapshot of what is currently on the video feed
    elif k%256 == 32:
        #Sets name of image to person plus the current count of the image taken along with putting it in a directory
        img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
        #Creates the image and writes it into the directory
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        #Adds one to the counter
        img_counter += 1

#Closes video feed
cam.release()

#Closes all open windows
cv2.destroyAllWindows()
