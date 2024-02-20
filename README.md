# Computer-Vision Practice



**1.Discription:**

***1. This is just a small project that we want to practice the basic image processing skills for computer vision.***

***2.This topic was focus on image processing over color and used filters to do image smoothing.***

![image](Figures/GUI.png)

**2.Usage:**

1. Downloads whole repository and change path into the main folder
2. Run `python start.py` .
3. Input the image 1 for feature 1 and image 2 for feature 2.
4. Run the whole code.

**3.Feature:**

1.Image Prcessing

* 1.1 Color Separation :
    * Extract 3 channels of the image BGR to 3 separated channels.
      
      ![image](Figures/1.1_result.png)
* 1.2 Color Transformation :
  
    * Transform image into grayscale image
    * Merge BGR separated channel images from above problem into grayscale image by average weight : (R+G+B)/3.

      ![image](Figures/1.2_result.png)
* 1.3 Color Detection

     
* 1.4 Blendling
   * Here [Dog_Strong.jpg](Figures/Dog_Strong.jpg) and [Dog_Weak.jpg](Figures/Dog_Weak.jpg) to be example

   https://github.com/Kung-hen/Image-processing-and-smooth/assets/95673520/ce2d8d34-6793-4961-8f74-fe055452e71e


    
2.Image Smoothing

* 2.1 Gaussian Blur
* 2.2 Bilateral fliter
* 2.3 Median fliter
