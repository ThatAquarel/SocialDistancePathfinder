# SocialDistancePathfinder
Automatically finds the safest path for you to take given some footage.

## Video Demo
[![Watch the video](https://img.youtube.com/vi/YW-d8_-I8ck/maxresdefault.jpg)](https://youtu.be/YW-d8_-I8ck)

## The heatmap
The heatmap shows the places where people are most likely to go to.
Green is the safest place to go and red is the places where most people are attracted to.
Two types of circles are also drawn, the thicker ones represent the people that don't follow social distancing guidelines, the thinner ones are those that follow these rules.
There is also a trail drawn behind every person, representing their moving direction.

## Live Footage
The live footage represents the actual footage the algorithm runs on. Bounding boxes are drawn around the people, a red one would mean that this person is not following social distancing, a green ones are those that follow the rules. The white highlighted area is the best path you can take according to the algorithm, the yellow line is then calculated with that data to show the best straight path you can take. The blue square is the position where the algorithm starts pathfinding.

## Data Plot
This plot draws the points from the white highlighted area and uses linear regression to calculate the straight path.

## Algorithm
- YOLOv3-608 pretrained models from https://pjreddie.com/darknet/yolo/
- Computer vision with OpenCv
- Linear regression using Numpy.polyfit
- Distances calculated using Scipy.spatial.cdist

## Dependencies
- Python 3.9.1
- Imutils==0.5.3
- Numpy==1.19.5
- Scipy==1.6.0
- Opencv-python==4.4.0.46
- Simpy==1.7.1
