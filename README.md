# Vehicle Speed Detection
## Images:
### 1st Camera View:
![1st-cam](https://github.com/surajdhanorkar2811/SafeDrive-verified/assets/91583497/28736353-dac2-4b23-bfac-3808ac7c45d3)

### 2nd Camera View:
![2nd_cam](https://github.com/surajdhanorkar2811/SafeDrive-verified/assets/91583497/2be6aaf1-e39e-4904-97af-21e3fa5ec96a)

### Overall system View:
![overall](https://github.com/surajdhanorkar2811/SafeDrive-verified/assets/91583497/ade2e844-a86f-4c34-8a2f-35b32c868828)

![overall2](https://github.com/surajdhanorkar2811/SafeDrive-verified/assets/91583497/4945a48d-c81e-4baa-a491-4e829be88844)


![output.gif](output.gif)

Technologies used :
- Python
- opencv
- dlib
<br>

Tasks breakdown
1. Vehicle Detection
    - We are using Haarcascade classifier to identify vehicles.
2. Vehicle Tracking - ( assigning IDs to vehicles )
    - We have used corelation tracker from dlib library.
3. Speed Calculation
    - We are calculating the distance moved by the tracked vehicle 
		  in a second, in terms of pixels, so we need pixel per meter
		  to calculate the distance travelled in meters.
	- With distance travelled per second in meters, we will get the 
		  speed of the vehicle.

#### How to run project? 

Follow steps:

1. Clone repo :
`git clone https://github.com/kraten/vehicle-speed-check`

2. cd (change directory) into vehicle-speed-check
`cd vehicle-speed-check`

3. Create virtual environment
`python -m venv venv`

4. Activate virtual environment
`./venv/bin/activate`

5. Install requirements
`pip install  -r requirements.txt`

6. run speed_check.py script
`python speed_check.py`



#### Note: 

A lot of you were raising the same issue about code understanding. I know that I haven't properly commented out the code. So, here is the brief summary of what the code does and how-

We have estimated these values manually for the current road to calculate pixels per metre(ppm). Therefore, the value will vary from road to road and have to be adjusted to be used on any other video. 

If I talk about the part how we estimated ppm, we need to know the actual width in metres of the road(you can use google to find the approximate width of the road in your country). Also, we have taken the video frame and calculated the width of the road in pixels digitally. Now, we have the width of the road in metres from the real world and in pixels from our video frame. To map the distances between these two worlds, we have calculated pixels per metre by dividing distance of road in pixels to metres.

d_pixels gives the pixel distance travelled by the vehicle in one frame of our video processing. To estimate speed in any standard unit first, we need to convert d_pixels to d_metres.

Now, we can calculate the speed(speed = d_meters * fps * 3.6). d_meters is the distance travelled in one frame. We have already calculated the average fps during video processing. So, to get the speed in m/s, just (d_metres * fps) will do. We have multiplied that estimated speed with 3.6 to convert it into km/hr.


### Pull requests are welcome
