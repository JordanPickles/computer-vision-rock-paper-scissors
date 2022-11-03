

import random
import cv2
from keras.models import load_model
import numpy as np
import time
import itertools 

class Game:
    def __init__(self, computer_choice, user_choice):
        self.computer_choice = computer_choice
        self.user_choice = user_choice

        self.computer_wins = 0
        self.user_wins = 0
        self.options = ["rock","paper","scissors"]
        self.computer_choice = random.choice(self.options)


    def get_user_choice(self):
        model = load_model('keras_model.h5')
        cap = cv2.VideoCapture(0)
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image_capture = time.time()+5
        start_time = time.time()

        while image_capture > time.time(): 
            count = 3
            if start_time - time.time() > 0 and count >0:
                print(count)
                count -=1
            elif count > 0:
                print(count)
            else:
                print("Rock, Paper, Scissors ....")
    
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
            user_choice = self.options[np.argmax(prediction)]
            print(user_choice)
            # After the loop release the cap object
        cap.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

           


    def get_computer_choice(self):
        valid_answers = ["rock","paper","scissors"]
        self.computer_choice = random.choice(valid_answers)

    def get_winner(self, computer_choice, user_choice):
        print(f"Your choice was {user_choice}")
        print(f"The computer selected {computer_choice}")
        if computer_choice == user_choice:
            print("Both players selected the same choice, please select again")
        elif computer_choice == "rock":
            if user_choice == "paper":
                print("Congratulations, you won")
                self.user_wins = self.user_wins +1

            elif user_choice == "scissors":
                print("Unlucky, the computer wins")
                self.computer_wins = self.computer_wins +1

        elif computer_choice == "paper":
            if user_choice == "rock":
                print("Unlucky, the computer wins")
                self.computer_wins = self.computer_wins +1

            elif user_choice == "scissors":
                print("Congratulations, you won")
                self.user_wins = self.user_wins +1

        elif computer_choice == "scissors":
            if user_choice == "rock":
                print("Congratulations, you won")
                self.user_wins = self.user_wins +1
            elif user_choice == "paper":
                print("Unlucky, the computer wins")
                self.computer_wins = self.computer_wins +1

def game():
    computer_wins = 0
    user_wins = 0
    game1 = Game(computer_wins, user_wins)
    while True:
        if game1.computer_wins == 3 and game1.user_wins != 3:
            print("Unlucky, the computer wins")
            break
        elif game1.user_wins == 3 and game1.computer_wins != 3:
            print("Congratulations you won")
            break
        else:
            game1.get_computer_choice(), game1.get_user_choice()


game()