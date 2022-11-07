
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