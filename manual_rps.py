import random

def get_computer_choice():
    valid_answers = ["rock","paper","scissors"]
    computer_choice = random.choice(valid_answers)
    return computer_choice
    

def get_user_choice():
    valid_answers = ["rock","paper","scissors"]
    while True:
        user_choice = input("Please input of one of the following, rock, paper or scissors")
        if user_choice.lower() not in valid_answers:
            print("Invalid input, please re-enter your answer")
        else:
            return user_choice


def get_winner(computer_choice, user_choice):
    print(computer_choice)
    print(user_choice)
    if computer_choice == user_choice:
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
    get_winner(get_computer_choice(), get_user_choice())

play()