import random

def get_computer_choice():
    valid_answers = ["rock","paper","scissors"] # Creates the string of possible choices
    computer_choice = random.choice(valid_answers) # Random.choice function provides a random choice of the valid_answers variable
    return computer_choice # Returns the output
    

def get_user_choice():
    """
    This function prompts the user to input a choice of "rock", "paper", or "scissors".
    The function uses a while loop to repeatedly ask for input until the user provides a valid choice.
    It uses the 'input' function to request the user's choice and the 'valid_answers' list to check for valid input.
    If the input is not in the 'valid_answers' list, the function will print "Invalid input, please re-enter your answer" and loop again.
    If the input is valid, the function returns the user's choice as a string.
    """
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