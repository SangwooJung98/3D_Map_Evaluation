# 3D_Map_Accuracy_Evaluation
Quantitative 3D Map Accuracy Evaluation Hardware and Algorithm for LiDAR(-Inertial) SLAM

## Setup
python 3.11

```
pip install -r requirements.txt
```

## Cropping

### target_manual.py

enter target GPS pose at **target_pos** : will automatically provide loosely cropped pointcloud.

Crop the target tightly manually.



https://github.com/hshhahn/2023_winter_urop/assets/122349813/ac8afb19-c87f-4243-bbbd-d04e44f97577



#### keyboard instructions for cropping 
```
X Y Z: axis view  
F: free look  
Mouse left drag : view adjustment  
Mouse wheel up/down : zoom in/out  
K: enter/leave cropping mode   
Ctrl + Mouse left click : select region (in cropping mode)  
Mouse left drag : select region (in cropping mode)  
C: crop  
S: save **add .pcl for filename extension **   
```

### gps_base_crop_auto.py

Automatically provides tightly cropped pointcloud.

Adjust **threshold** in **remove_ground** to optimal value for better cropping results. (hyperparameter depending on your original pointcloud)

## Target pose estimation

Apply **multi_test_0130_1.py** on tightly cropped pointcloud.

K-means Clustering, RANSAC, SVD is applied to the tightly cropped pointcloud.

Returns x, y position of the target. (=estimated target pose) 

While running, # of iterations and total attempts are visualized.

![image](https://github.com/hshhahn/2023_winter_urop/assets/122349813/798ae1a1-d2c4-4335-b27c-6a6feb1a4d8b)


## Error Calculation  

Prepare the ground truth pose and estimated target pose for each target.

<img src=https://github.com/hshhahn/2023_winter_urop/assets/122349813/e3c69cf5-f76b-4929-9827-b48483b38278 width="85%" height="80%">


### Ground Truth

The ground truth can be obtained from the GPS sensor attatched to the target. 
Subtract the rtk origin pose from the rtk target pose for the ground truth pose.   

<img src=https://github.com/hshhahn/2023_winter_urop/assets/122349813/d14f5211-8338-4c66-bb90-397a0aef9a8c width="70%" height="60%">


Copy and paste each pose into **relative+absolute.py**


### Error Metrics 

![image](https://github.com/hshhahn/2023_winter_urop/assets/122349813/d0dac612-244a-4b4a-9960-1883afb8dc69)


**relative+absolute.py** returns 
1. frame translation/rotation values
2. Distance errors between corresponding targets
3. Absolute error (the average of 2)
4. Errors of each segment
5. Relative error (the average of 4)





