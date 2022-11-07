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

## Milestone 5 (camera_rps.py)
This milestone introduced the user input via the camera. Therefore the rps template was used to use the recorded CV model to provide predictions from the users camera input. The game was also enclosed within a class which is then called and intialised by one function at the bottom of the code. Finally, messages are included in the camera frame on the users screen using CV2.PutText, the aim of this is to improve the users gameplay experience. Several areas of the code have been improved. Here the get_winner() function has been compacted to improve readibility. The countdown before the game commences has also been imrpoved to work by seconds and not count as previosuly done in milestone 4 (above).
'''

#Imports the required packages for this project
import random
import cv2
from keras.models import load_model
import numpy as np
import time


class Game:
    def __init__(self, computer_choice, user_choice):
        #Arguments to the class
        self.computer_choice = computer_choice 
        self.user_choice = user_choice
        
        #Parameters to the class
        self.computer_wins = 0
        self.user_wins = 0
        self.options = ["rock","paper","scissors"]
        self.computer_choice = random.choice(self.options)
        self.count = 3
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.txt_colour = (0,0,225)
        self.cap = cv2.VideoCapture(0)

    # This function intiates the tensorflow computer vision file which provides a probability prediction using a trained model to determine the users input
    def get_user_choice(self): 
        model = load_model('keras_model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image_capture = time.time()+10 # Timepoint for image capture
        start_time = time.time() + 3 # Timepoint for start time countdown
                

        # This while loop provides the countdown to the round starting. It then uses the trained model to capture and provide predictions of the users input using probabiility
        while True:
            if start_time - time.time() > 0: # This if block provides the countdown for the user. A simple calculation of start_time - time.time() is used until time.time is  == start_time
                ret, frame = self.cap.read()
                resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
                frame_text = cv2.putText(frame, str(int(start_time - time.time())), (600,400), self.font, 1, self.txt_colour, 2, cv2.LINE_AA)
                cv2.imshow('frame', frame_text)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
            elif image_capture > time.time(): # This elif code block records the image for the user input
                ret, frame = self.cap.read()
                resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
                image_np = np.array(resized_frame)
                normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
                data[0] = normalized_image
                prediction = model.predict(data)    
                cv2.imshow('frame', frame)
                # Press q to close the window
                print(prediction)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                elif time.time() > image_capture:
                    break
        # This provides the index of the largest probability in the output. The model is trained in the same order as the choices parameter and therfore the indexes match
        user_choice = self.options[np.argmax(prediction)] 
        self.user_choice = user_choice
        return user_choice 
    
    # This function provides an introduction screen with simple instructions to the user
    def game_intro(self):
        intro_time1 = time.time() +8 # Time periiod used for part 1 of the introduction
        intro_time2 = time.time() +15 # Time period used for part 2 of the introduction

        while True:
            if intro_time1 > time.time():
                ret, frame = self.cap.read()
                resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA) # This sets up the intial frame
                intro_text = str("Welcome to Rock, Paper, Scissors. First to 3 wins!!!")
                frame_intro = cv2.putText(frame, intro_text, (100,400), self.font, 1, self.txt_colour, 2, cv2.LINE_AA)
                cv2.imshow('frame', frame_intro)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            elif intro_time2 > time.time() > intro_time1 and intro_time2 - time.time()>0:
                ret, frame = self.cap.read()
                intro2 = str("Once the countdown starts, please signal Rock, Paper or Scissors")
                frame_intro2 = cv2.putText(frame, intro2, (100,400), self.font, 1, self.txt_colour, 2, cv2.LINE_AA)
                cv2.imshow('frame', frame_intro2)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break



    # This function procides a randomised input for the computer
    def get_computer_choice(self):
        valid_answers = ["rock","paper","scissors"]
        computer_choice = random.choice(valid_answers)
        self.computer_choice = computer_choice
        return computer_choice

    # This function determines a winner from the user input and computer inputs provided
    def get_winner(self, computer_choice, user_choice):
        print(f"Your choice was {user_choice}")
        print(f"The computer selected {computer_choice}")
        # Both the user and the computers inputs are the same
        if computer_choice == user_choice:
                print("Both players selected the same choice, please select again")
        # Cases in which the computer wins
        elif (computer_choice == "rock" and user_choice == "scissors") or (computer_choice == "paper" and user_choice == "rock") or (computer_choice == "scissors" and user_choice == "paper"):
            print("Unlucky, the computer wins")
            self.computer_wins = self.computer_wins +1
        # Cases in which the user wins
        elif (user_choice == "rock" and computer_choice == "scissors") or (user_choice == "paper" and computer_choice == "rock") or (user_choice == "scissors" and computer_choice == "paper"):
            print("Congratulations, you won")
            self.user_wins = self.user_wins +1
    
    # This function provides the user with a visible result on the screen as well as the scores at the current stage
    def result_report(self, user_choice, computer_choice):
        result_time1 = time.time() +5
        result_time2 = time.time()+ 10
        while True:
                if result_time1 > time.time():
                    ret, frame = self.cap.read()
                    result_text = (f"You chose {user_choice}, the computer chose {computer_choice}")
                    frame_result = cv2.putText(frame, result_text, (200,400), self.font, 1, self.txt_colour, 2, cv2.LINE_AA)
                    cv2.imshow('frame', frame_result)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                elif result_time2 > time.time() > result_time1 and result_time2 - time.time() > 0:
                    ret, frame = self.cap.read()
                    result_text2 = (f"You have won {self.user_wins}, the computer has won {self.computer_wins}")
                    frame_result2 = cv2.putText(frame, result_text2, (300,400), self.font, 1, self.txt_colour, 2, cv2.LINE_AA)
                    cv2.imshow('frame', frame_result2)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else: 
                    break

    

    # This fuction intialises the game and provides logic to determine the winner on a first to 3 wins basis
def game():
    computer_wins = 0
    user_wins = 0
    game1 = Game(computer_wins, user_wins) # Initalises the class
    game1.game_intro()

    while True:
        # The computer has won 3 rounds and wins the game
        if game1.computer_wins == 3 and game1.user_wins != 3:
            print(f"Unlucky, the computer wins. The computer has won {game1.computer_wins} games and you have won {game1.user_wins}")
            game1.cap.release()
            cv2.destroyAllWindows()
            break
        # The user has won 3 rounds and wins the game
        elif game1.user_wins == 3 and game1.computer_wins != 3:
            print(f"Congratulations you won. You have won {game1.user_wins} and the computer has won {game1.computer_wins}")
            # Destroy all the windows
            game1.cap.release()
            cv2.destroyAllWindows()
            break
        # Neither the computer or the user have won 3 games yet so another round commences
        else:
            game1.get_winner(game1.get_computer_choice(), game1.get_user_choice())
            game1.result_report(game1.user_choice, game1.computer_choice)

            

game()
'''
