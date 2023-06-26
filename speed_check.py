import tkinter as tk
import cv2
import dlib
import time
import threading
import math
import tkinter



carCascade = cv2.CascadeClassifier('myhaar.xml')
cap1 = cv2.VideoCapture('new high123.mp4')
cap2 = cv2.VideoCapture('video3.mp4')


# cap1 = cv2.VideoCapture('saurabh.mp4')
# cap2 = cv2.VideoCapture('saurabh_stop.mp4')


# cap1 = cv2.VideoCapture('fast-crop.mp4')
# cap2 = cv2.VideoCapture('slow-crop.mp4')

# cap1 = cv2.VideoCapture('test2-fast.mp4')
# cap2 = cv2.VideoCapture('test2-slow.mp4')

# cap1 = cv2.VideoCapture('test2-slow.mp4')
# cap2 = cv2.VideoCapture('test2-fast.mp4')



WIDTH = 1280
HEIGHT = 720

time1 = 600
time2 = 600

###############################
# Define the focal length (in pixels)
focal_length = 8

# Define the real width of the vehicle (in meters)
vehicle_width = 1.8

def calculate_distance(w1, w2, p):
    return (w1 * p) / (2 * math.tan(math.radians(w2 / 2)))

###############################


def estimateSpeed(location1, location2):
    d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    # ppm = location2[2] / carWidht
    ppm = 8.8
    d_meters = d_pixels / ppm
    # print("d_pixels=" + str(d_pixels), "d_meters=" + str(d_meters))
    fps = 18
    speed = d_meters * fps * 3.6
    return speed

dynamic_value1 = "green"
dynamic_value2 = "green"

# def get_dynamic_values():
#     # Read the dynamic values from a file or any other data source
#     # Perform necessary processing
#     # Return the dynamic values
#     global dynamic_value1, dynamic_value2
#     return dynamic_value1, dynamic_value2

class TrafficLight:
    def __init__(self, master, x):
        self.master = master
        self.current_color1 = 'red'
        self.current_color2 = 'red'

        # Create the canvas
        self.canvas = tk.Canvas(master, width=200, height=300)
        self.canvas.pack(side=tk.LEFT, padx=10)

        # Create the lights for the first traffic light
        self.red_light1 = self.canvas.create_oval(10, 10, 90, 90, fill='red')
        self.yellow_light1 = self.canvas.create_oval(10, 110, 90, 190, fill='gray')
        self.green_light1 = self.canvas.create_oval(10, 210, 90, 290, fill='gray')

        # Create a copy of the lights for the second traffic light
        self.red_light2 = self.canvas.create_oval(110, 10, 190, 90, fill='red')
        self.yellow_light2 = self.canvas.create_oval(110, 110, 190, 190, fill='gray')
        self.green_light2 = self.canvas.create_oval(110, 210, 190, 290, fill='gray')

        # Update the lights initially
        self.update_lights()

    def update_lights(self):
        if dynamic_value1 == "red":
            self.canvas.itemconfigure(self.red_light1, fill='red')
            self.canvas.itemconfigure(self.green_light1, fill='gray')
        elif dynamic_value1 == "green":
            self.canvas.itemconfigure(self.red_light1, fill='gray')
            self.canvas.itemconfigure(self.green_light1, fill='green')

        if dynamic_value2 == "red":
            self.canvas.itemconfigure(self.red_light2, fill='red')
            self.canvas.itemconfigure(self.green_light2, fill='gray')
        elif dynamic_value2 == "green":
            self.canvas.itemconfigure(self.red_light2, fill='gray')
            self.canvas.itemconfigure(self.green_light2, fill='green')


def trackMultipleObjects1():

    global dynamic_value1
    global dynamic_value2
    global time1
    global time2
    rectangleColor = (0, 255, 0)
    frameCounter = 0
    currentCarID = 0
    fps = 0

    carTracker = {}
    carNumbers = {}
    carLocation1 = {}
    carLocation2 = {}
    speed = [None] * 1000



    # Write output to video file
    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (WIDTH, HEIGHT))

    while True:
        start_time = time.time()
        ret1, img1 = cap1.read()

        if not ret1:
            break

        # if type(image2) == type(None):
        #     break


        image1 = cv2.resize(img1, (WIDTH, HEIGHT))
        # image2 = cv2.resize(img2, (WIDTH, HEIGHT))

        resultImage1 = image1.copy()
        # resultImage2 = image2.copy()

        frameCounter = frameCounter + 1

        carIDtoDelete = []

        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(image1)

            if trackingQuality < 7:
                carIDtoDelete.append(carID)

        for carID in carIDtoDelete:
            # print('Removing carID ' + str(carID) + ' from list of trackers.')
            # print('Removing carID ' + str(carID) + ' previous location.')
            # print('Removing carID ' + str(carID) + ' current location.')
            carTracker.pop(carID, None)
            carLocation1.pop(carID, None)
            carLocation2.pop(carID, None)


        if not (frameCounter % 10):
            gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))

            for (_x, _y, _w, _h) in cars:
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)

                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h

                matchCarID = None


                for carID in carTracker.keys():
                    trackedPosition = carTracker[carID].get_position()

                    t_x = int(trackedPosition.left())
                    t_y = int(trackedPosition.top())
                    t_w = int(trackedPosition.width())
                    t_h = int(trackedPosition.height())

                    t_x_bar = t_x + 0.5 * t_w
                    t_y_bar = t_y + 0.5 * t_h

                    if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (
                            x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
                        matchCarID = carID


                if matchCarID is None:
                    # print('Creating new tracker ' + str(currentCarID))

                    tracker = dlib.correlation_tracker()
                    tracker.start_track(image1, dlib.rectangle(x, y, x + w, y + h))

                    carTracker[currentCarID] = tracker
                    carLocation1[currentCarID] = [x, y, w, h]

                    currentCarID = currentCarID + 1

        # cv2.line(resultImage,(0,480),(1280,480),(255,0,0),5)

        for carID in carTracker.keys():
            trackedPosition = carTracker[carID].get_position()

            t_x = int(trackedPosition.left())
            t_y = int(trackedPosition.top())
            t_w = int(trackedPosition.width())
            t_h = int(trackedPosition.height())


            cv2.rectangle(resultImage1, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)

            # speed estimation
            carLocation2[carID] = [t_x, t_y, t_w, t_h]


        end_time = time.time()

        if not (end_time == start_time):
            fps = 1.0 / (end_time - start_time)

        # cv2.putText(resultImage, 'FPS: ' + str(int(fps)), (620, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        for i in carLocation1.keys():
            if frameCounter % 1 == 0:
                [x1, y1, w1, h1] = carLocation1[i]
                [x2, y2, w2, h2] = carLocation2[i]

                # print 'previous location: ' + str(carLocation1[i]) + ', current location: ' + str(carLocation2[i])
                carLocation1[i] = [x2, y2, w2, h2]

                ###############################
                # cv2.rectangle(resultImage, (x, y), (x + w, y + h), (0, 255, 255), 2)

                # Calculate the distance to the vehicle
                distance = calculate_distance(vehicle_width, w2, focal_length)


                # Display the distance above the vehicle
                cv2.putText(resultImage1, '{:.2f}m'.format(distance), (x2, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 2)
                ###############################
                distance = round(distance, 2)
                distance = max(0, distance)
                # print(time1, time2)

                # if abs(time1-time2)<2:
                if(time1<time2):
                    # print(f"way2: red")
                    dynamic_value2 = "red"
                    # print(f"way1: green")
                    dynamic_value1 = "green"
                    update_colors()
                else:
                    # print(f"way2: green")
                    dynamic_value2 = "green"
                    # print(f"way1: red")
                    dynamic_value1 = "red"
                    update_colors()
                # else:
                #     # print(f"way2: green")
                #     # print(f"way1: green")
                #     dynamic_value1 = "green"
                #     update_colors()

                # print 'new previous location: ' + str(carLocation1[i])
                if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
                    if (speed[i] == None or speed[i] == 0) and y1 >= 275 and y1 <= 285:
                        speed[i] = estimateSpeed([x1, y1, w1, h1], [x2, y2, w2, h2])

                    # if y1 > 275 and y1 < 285:
                    if speed[i] != None and y1 >= 180:
                        cv2.putText(resultImage1, str(int(speed[i])) + " km/hr", (int(x1 + w1 / 2), int(y1 - 5)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

                    timeC = 0
                    if speed[i] is not None:
                        if (speed[i] != 0):
                            speed_of_car = round(speed[i], 2)
                            # print(speed_of_car, distance)
                            speed_of_car_ms = speed_of_car * 0.27778
                            # print(distance, speed_of_car_ms)
                            timeC = distance / speed_of_car_ms
                            time1 = timeC


                    # print(timeC)
                    #












                # print ('CarID ' + str(i) + ': speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')

                # else:
                #	cv2.putText(resultImage, "Far Object", (int(x1 + w1/2), int(y1)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # print ('CarID ' + str(i) + ' Location1: ' + str(carLocation1[i]) + ' Location2: ' + str(carLocation2[i]) + ' speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')
        cv2.imshow('Video 1', resultImage1)
        # cv2.imshow('Video 2', resultImage2)
        # Write the frame into the file 'output.avi'
        # out.write(resultImage)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap1.release()
    cv2.destroyAllWindows()


def trackMultipleObjects2():
    global time1
    global time2
    rectangleColor = (0, 255, 0)
    frameCounter = 0
    currentCarID = 0
    fps = 0

    carTracker = {}
    carNumbers = {}
    carLocation1 = {}
    carLocation2 = {}
    speed = [None] * 1000



    # Write output to video file
    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (WIDTH, HEIGHT))

    while True:
        start_time = time.time()
        ret2, img2 = cap2.read()

        if not ret2:
            break

        # if type(image2) == type(None):
        #     break


        image2 = cv2.resize(img2, (WIDTH, HEIGHT))
        # image2 = cv2.resize(img2, (WIDTH, HEIGHT))

        resultImage2 = image2.copy()
        # resultImage2 = image2.copy()

        frameCounter = frameCounter + 1

        carIDtoDelete = []

        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(image2)

            if trackingQuality < 7:
                carIDtoDelete.append(carID)

        for carID in carIDtoDelete:
            # print('Removing carID ' + str(carID) + ' from list of trackers.')
            # print('Removing carID ' + str(carID) + ' previous location.')
            # print('Removing carID ' + str(carID) + ' current location.')
            carTracker.pop(carID, None)
            carLocation1.pop(carID, None)
            carLocation2.pop(carID, None)


        if not (frameCounter % 10):
            gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))

            for (_x, _y, _w, _h) in cars:
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)

                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h

                matchCarID = None


                for carID in carTracker.keys():
                    trackedPosition = carTracker[carID].get_position()

                    t_x = int(trackedPosition.left())
                    t_y = int(trackedPosition.top())
                    t_w = int(trackedPosition.width())
                    t_h = int(trackedPosition.height())

                    t_x_bar = t_x + 0.5 * t_w
                    t_y_bar = t_y + 0.5 * t_h

                    if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (
                            x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
                        matchCarID = carID


                if matchCarID is None:
                    # print('Creating new tracker ' + str(currentCarID))

                    tracker = dlib.correlation_tracker()
                    tracker.start_track(image2, dlib.rectangle(x, y, x + w, y + h))

                    carTracker[currentCarID] = tracker
                    carLocation1[currentCarID] = [x, y, w, h]

                    currentCarID = currentCarID + 1

        # cv2.line(resultImage,(0,480),(1280,480),(255,0,0),5)

        for carID in carTracker.keys():
            trackedPosition = carTracker[carID].get_position()

            t_x = int(trackedPosition.left())
            t_y = int(trackedPosition.top())
            t_w = int(trackedPosition.width())
            t_h = int(trackedPosition.height())

            cv2.rectangle(resultImage2, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)

            # speed estimation
            carLocation2[carID] = [t_x, t_y, t_w, t_h]


        end_time = time.time()

        if not (end_time == start_time):
            fps = 1.0 / (end_time - start_time)

        # cv2.putText(resultImage, 'FPS: ' + str(int(fps)), (620, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        for i in carLocation1.keys():
            if frameCounter % 1 == 0:
                [x1, y1, w1, h1] = carLocation1[i]
                [x2, y2, w2, h2] = carLocation2[i]

                # print 'previous location: ' + str(carLocation1[i]) + ', current location: ' + str(carLocation2[i])
                carLocation1[i] = [x2, y2, w2, h2]

                ###############################
                # cv2.rectangle(resultImage, (x, y), (x + w, y + h), (0, 255, 255), 2)

                # Calculate the distance to the vehicle
                distance = calculate_distance(vehicle_width, w2, focal_length)

                # Display the distance above the vehicle
                cv2.putText(resultImage2, '{:.2f}m'.format(distance), (x2, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 2)
                ###############################
                distance = round(distance, 2)
                distance = max(0, distance)
                # print(distance)

                # print 'new previous location: ' + str(carLocation1[i])
                if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
                    if (speed[i] == None or speed[i] == 0) and y1 >= 275 and y1 <= 285:
                        speed[i] = estimateSpeed([x1, y1, w1, h1], [x2, y2, w2, h2])

                    # if y1 > 275 and y1 < 285:
                    if speed[i] != None and y1 >= 180:
                        cv2.putText(resultImage2, str(int(speed[i])) + " km/hr", (int(x1 + w1 / 2), int(y1 - 5)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)



                    # print(speed[i], distance)
                    if speed[i] is not None:
                        if(speed[i]!=0):
                            speed_of_car = round(speed[i], 2)
                            # print(speed_of_car, distance)
                            speed_of_car_ms = speed_of_car * 0.27778
                            # print(distance, speed_of_car_ms)
                            timeC = distance / speed_of_car_ms
                            time2 = timeC
                            # print(timeC)

                            # time2 = min(time2, timeC)

                # print ('CarID ' + str(i) + ': speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')

                # else:
                #	cv2.putText(resultImage, "Far Object", (int(x1 + w1/2), int(y1)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # print ('CarID ' + str(i) + ' Location1: ' + str(carLocation1[i]) + ' Location2: ' + str(carLocation2[i]) + ' speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')
        cv2.imshow('Video 2', resultImage2)
        # cv2.imshow('Video 2', resultImage2)
        # Write the frame into the file 'output.avi'
        # out.write(resultImage)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap2.release()
    cv2.destroyAllWindows()

def update_colors():
    global dynamic_value1, dynamic_value2

    # Update the dynamic values
    # Here, you can write code to update dynamic_value1 and dynamic_value2
    # based on your application logic

    # Call the update_lights() method to update the traffic light colors
    traffic_light.update_lights()
    # print(dynamic_value1)
    # print(dynamic_value2)




if __name__ == '__main__':
    root = tk.Tk()
    traffic_light = TrafficLight(root, 0)
    thread1 = threading.Thread(target=trackMultipleObjects1)
    thread2 = threading.Thread(target=trackMultipleObjects2)
    # Start the threads
    thread1.start()
    thread2.start()

    # Start the Tkinter event loop
    root.mainloop()

    # Wait for the threads to finish
    thread1.join()
    thread2.join()
    # trackMultipleObjects1()
    # trackMultipleObjects1()
