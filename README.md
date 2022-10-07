Improving Retinanet in Ship Detection with Data Augmentation

The main repository of this project is in https://github.com/fizyr/keras-retinanet.

Developing a two-stage template matching algorithm for detecting objects and finding the angle of each object in NWPU-10 Dataset

We used the Retinanet code for object detection in NWPU-10 dataset; this dataset has a limited number of images in each class. Therefore, we used common augmented methods to increase the number of data; however, the accuracy in ship class decreased. Consequently, we implemented an algorithm that found angles of each ship in every image, and used these angles as a input of augmentation algorithm. Hence, the accuracy increased.

