# VP Coding Challenge - Tissue Segmentation

## Tracking metrics
1. Segmentation area 
    
    The main metric for image segmentation is segmentation "union" or the amount the prediction overlaps the ground truth object boundaries.
    To measure this I used the contour area function. In this implementation the contour area is calculated as the number of pixels contained
    within each contour region. In the app, this metric is displayed on the console as Contour[0] - Area = ### px.
    The difference between the ground truth and the predicted area is displayed as "X Y area difference (px)"

2. Center of mass
    
    This metric indicates the center of mass of an object as calculated by the position and extent of the contour boundaries. The goal is to 
    maintain minimal delta between the ground truth and predicted mass centers. This is indicated in the console with: "X Y mass center difference (px)"
    
## Instructions
1. In the console run the following command
   
   python Vistapathcodingchallenge.py
   
The result is shown below. Two windows show the segmentation by the app, the segmentation based on the mask image, and a third shows the original raw image.

![image](https://user-images.githubusercontent.com/44035895/152666022-06fbf2eb-e69e-4999-bd72-7da872989f88.png)


The console output will be as follows: 

![image](https://user-images.githubusercontent.com/44035895/152666099-3adb482a-bd63-4673-922d-56eaeadf31b4.png)


   
2. To run the segmentation on another image add the following args:

--input="path to new image"

--mask="path to new image gt mask"

