# Comp537-Project

This project aims to build a formative feedback interface for facial expressions. 

Clone [StarGAN](https://github.com/yunjey/StarGAN) [1] repository to current working directory. Model trained with only the RaFD dataset is available at the log file. Trained models should be placed in StarGAN/stargan_rafd/models. 
Also create a folder named 'results_divided' in StarGAN/stargan_rafd folder. 

For action unit detection, I have used models trained by https://github.com/jdlamstein/happybot. Clone the repo into 'happybot' folder and keep the facs_trial.py file. 

You do not need to download the RaFD dataset. Just use the folder structure provided in this repo (most folders are empty). 


You can run the model with the following command:


  $ python stargan_ui.py


For face recognition and image crop & align, imutils is used [2]. Please install it by following the instructions at: https://github.com/jrosebr1/imutils

Pre-trained model for facial landmark recognition is downloaded from https://github.com/davisking/dlib-models. It is available in the repo as 'shape_predictor_5_face_landmarks.dat'. Download and place in the current working directory. 
Download 'shape_predictor_68_face_landmarks.dat' and place in folder './happybot/happybot'


References: 

[1]  Choi, Y., Choi, M., Kim, M., Ha, J.W., Kim, S., Choo, J.: Stargan: Unified generative adversarial networks for multi-domain image-to-image translation. In: CVPR.(2018)

[2] A.Rosebrock. "Face Alignment with OpenCV and Python". PyImageSearch. May 22, 2017. https://www.pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python/

