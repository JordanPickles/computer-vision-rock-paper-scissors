# Computer Vision RPS
The aim of this project was to develop skills within computer vision. To develop these skills, a game of rock, paper, scissors was created using teachablemachine.withgoogle.com to train a model based on several images from 3 different classes, the game was then developed in python using this image based model.

## Milestone 2
Using teachablemachine.withgoogle.com a model was trained with images for 3 classes ('Rock', 'Paper', 'Scissors'). The model was then trained by the software on the site and can be seen below.
```
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model('keras_Model.h5', compile=False)

# Load the labels
class_names = open('labels.txt', 'r').readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
image = Image.open('<IMAGE_PATH>').convert('RGB')

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
image_array = np.asarray(image)

# Normalize the image
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# Load the image into the array
data[0] = normalized_image_array

# run the inference
prediction = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]

print('Class: ', class_name, end='')
print('Confidence Score: ', confidence_score)
```

## Milestone 4 (Manual_rps.py)
This .py document provides a manual version of the rock, paper scissors game that requires a user input to play against a randomly chosen computer choice

```
import random

def get_computer_choice():
    valid_answers = ["rock","paper","scissors"] # Creates the string of possible choices
    computer_choice = random.choice(valid_answers) # Random.choice function provides a random choice of the valid_answers variable
    return computer_choice # Returns the output
    

def get_user_choice():
    valid_answers = ["rock","paper","scissors"] # String of potential inputs to complete a validity check against
    while True:
        user_choice = str(input("Please input of one of the following, rock, paper or scissors")) # Asks the user for a string input
        if user_choice.lower() not in valid_answers: # Checks the input is in the valid_answers list to ensure a valid input
            print("Invalid input, please re-enter your answer") # Does not break the loop and asks for another input
        else:
            return user_choice # If the input passes the valid check, then the input will be returned


def get_winner(computer_choice, user_choice): # Function passes the computer and user choice as arguments 
    print(f"Your choice was {user_choice}") 
    print(f"The computer selected {computer_choice}") 
    if computer_choice == user_choice: # Checks whether the user or computer won the game based on the inputs provided in the choice functions
        print("Both players selected the same choice, please select again")
    elif computer_choice == "rock":
        if user_choice == "paper":
            print("Congratulations, you won")
        elif user_choice == "scissors":
            print("Unlucky, the computer wins")

    elif computer_choice == "paper":
        if user_choice == "rock":
            print("Unlucky, the computer wins")
        elif user_choice == "scissors":
            print("Congratulations, you won")


    elif computer_choice == "scissors":
        if user_choice == "rock":
            print("Congratulations, you won")
        elif user_choice == "paper":
            print("Unlucky, the computer wins")


def play():
    get_winner(get_computer_choice(), get_user_choice()) # This function calls the game functions and passes the computer choice and user choice function as arguments

play()

```

