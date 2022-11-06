
# Imports the required packages for this class
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


    # This function intiates the tensorflow computer vision file which provides a probability prediction using a trained model to determine the users input
    def get_user_choice(self): 
        model = load_model('keras_model.h5')
        cap = cv2.VideoCapture(0)
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image_capture = time.time()+5
        
        #This block of code provides a countdown before the image capture begins, just like in the game
        count = 3
        start_time = time.time()
        while True:
            if  time.time() - start_time < 3 and count >0:
                print(count)
                count -=1
            elif count > 0:
                print(count)
            else:
                print("Rock, Paper, Scissors ....")
                break

        # This while loop uses the trained model to capture and provide predictions of the users input using probabiility
        while image_capture > time.time(): 
            ret, frame = cap.read()
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

        # After the loop release the cap object
        cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
        # This provides the index of the largest probability in the output. The model is trained in the same order as the choices parameter and therfore the indexes match
        user_choice = self.options[np.argmax(prediction)] 
        return user_choice

    # This function procides a randomised input for the computer
    def get_computer_choice(self):
        valid_answers = ["rock","paper","scissors"]
        computer_choice = random.choice(valid_answers)
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
        elif (user_choice == "rock" and computer_choice == "scissors") or (user_choice == "paper" and computer_choice == "rcok") or (user_choice == "scissors" and computer_choice == "paper"):
            print("Congratulations, you won")
            self.user_wins = self.user_wins +1

# This fuction intialises the game and provides logic to determine the winner on a first to 3 wins basis
def game():
    computer_wins = 0
    user_wins = 0
    game1 = Game(computer_wins, user_wins) # Initalises the class
    while True:
        # The computer has won 3 rounds and wins the game
        if game1.computer_wins == 3 and game1.user_wins != 3:
            print(f"Unlucky, the computer wins. The computer has won {game1.computer_wins} games and you have won {game1.user_wins}")
            cv2.destroyAllWindows()
            break
        # The user has won 3 rounds and wins the game
        elif game1.user_wins == 3 and game1.computer_wins != 3:
            print(f"Congratulations you won. You have won {game1.user_wins} and the computer has won {game1.computer_wins}")
            # Destroy all the windows
            cv2.destroyAllWindows()
            break
        # Neither the computer or the user have won 3 games yet so another round commences
        else:
            game1.get_winner(game1.get_computer_choice(), game1.get_user_choice())


game()