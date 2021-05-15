# Personalized Eye Tracker

A personalized deep learning application to track your eye gaze and map it to a particular part of your screen. This project was made for the course CS-2490.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing purposes.

### Prerequisites

What things you need to install the software and how to install them

You will need various python libraries like numpy, seaborn, pandas, etc. You will also need Tensorflow and OpenCV.

```
pip install <package>
```

## Generating the dataset

To train your model, a dataset of annotated eye images are required. run generate_data.py to generate images of the webcam frame.

```
python generate_data.py
```

The generation involves taking images of the webcam frame for each grid cell (4x4 recommended). To help with the position to look at, the code calls the 'xdotool' command to move the mouse within that grid cell. Install ```xdotool``` to be able to move the mouse from the code.
Press spacebar to move to the next grid cell.

### Processing the images

From the images generated, we must process them to find the location of the eye. The 'new_templates' folder contains various eye templates, which you can replace. Then, run ```python run.py``` to process the images you generated to generate the dataset required.



## Training the model

Follow the steps in ```train_model.ipynb``` to create, train, and save your model.

## Testing the Application

Run ```loadmodel.ipynb``` to test the application. To check against a grid system, open /application/index.html to view a grid system. You can choose the number of cells in the grid by pressing numbers on your keyboard. Press spacebar to generate a target cell.

Run the application simultaneously to test your model.

Once you stop the application, you can create your own heatmap based on the run.


