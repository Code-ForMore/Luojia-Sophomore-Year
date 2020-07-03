# Luojia-Sophomore-Year #
## Computer Vision and Pattern Recognition Course ##
+ Calibration
+ Structure from Motion
+ Stereo Matching
+ Denoise
+ YOLOv3 running
## Calibration ##
I implemented Zhang Zhengyou's calibration method with the help of OpenCV, successfully obtained the internal parameter matrix, distortion coefficient, pose information of the experimental camera, etc.And I used the re-projection error to reasonably evaluate the calibration accuracy to correct the distortion. In addition, I estimate the pose of the camera based on the obtained parameters, and realize the drawing of a 3D cube effect in the chessboard photo. In order to facilitate the operation, I use PyQt to create UI (caliUI) to interact with users to help readers use the above functions. Through related experiments, it was verified that Zhang Zhengyou's calibration method is a reliable, flexible, and convenient camera calibration method.
