#! /usr/bin/python

#Import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

#Initialize 'currentname' variable to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

#Load the known faces and embeddings along with OpenCV's Haar
#Cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

#Initialize the video stream and allow the camera sensor to warm up
#Setting the videostream to use the connected Raspberry Pi camera
vs = VideoStream(usePiCamera=True, framerate =25).start()
time.sleep(2.0)

#Start the FPS counter
fps = FPS().start()

#Loop over frames from the video file stream
while True:
	#Grab the frame from the threaded video stream and resize it to 500px (to speedup processing)
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	#Detect the bounding boxes
	boxes = face_recognition.face_locations(frame)
	#Compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(frame, boxes)
	names = []

	#Loop over the facial embeddings
	for encoding in encodings:
		#Attempt to match each face in the input image to our known faces from the pickle file
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown" #if face is not recognized, then print Unknown

		#Check to see if we have found a match
		if True in matches:
			#Find the indexes of all matched faces then initialize a
			#dictionary to count the total number of times each face
			#was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			#Loops over the matched indexes and maintain a count for
			#each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			#Determine the recognized face with the largest number
			#of votes (note: in the event of an unlikely tie Python
			#will select first entry in the dictionary)
			name = max(counts, key=counts.get)

			#If someone in your dataset is identified, print their name on the screen
			if currentname != name:
				currentname = name
				print(currentname)

		#Update the list of names
		names.append(name)

	#Loops over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		#Draw the predicted face name on the image - color is in BGR
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 225), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			.8, (0, 255, 255), 2)

	#Display the image to our screen
	cv2.imshow("Facial Recognition is Running", frame)
	key = cv2.waitKey(1) & 0xFF

	#Quit when 'q' key is pressed
	if key == ord("q"):
		break

	#Update the FPS counter
	fps.update()

#Stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

#Closes all windows and stops the video feed
cv2.destroyAllWindows()
vs.stop()
