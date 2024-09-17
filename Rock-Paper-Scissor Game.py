import random


def get_user_choice():
    user_choice = input("Choose rock, paper, or scissors: ").lower()
    while user_choice not in ['rock', 'paper', 'scissors']:
        print("Invalid choice. Please choose rock, paper, or scissors.")
        user_choice = input("Choose rock, paper, or scissors: ").lower()
    return user_choice


def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])


def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (
            (user_choice == 'rock' and computer_choice == 'scissors') or
            (user_choice == 'scissors' and computer_choice == 'paper') or
            (user_choice == 'paper' and computer_choice == 'rock')
    ):
        return "You win!"
    else:
        return "You lose!"


def display_choices_and_result(user_choice, computer_choice, result):
    print(f"\nYour choice: {user_choice.capitalize()}")
    print(f"Computer's choice: {computer_choice.capitalize()}")
    print(result)


def rock_paper_scissors_game():
    user_score = 0
    computer_score = 0

    print("Welcome to Rock, Paper, Scissors Game!")

    while True:
        print("\nInstructions:")
        print("Enter 'rock', 'paper', or 'scissors' when prompted.")
        print("Rock beats scissors, scissors beat paper, and paper beats rock.")
        print("Let's see who wins this round!\n")

        user_choice = get_user_choice()
        computer_choice = get_computer_choice()

        result = determine_winner(user_choice, computer_choice)
        display_choices_and_result(user_choice, computer_choice, result)

        if 'win' in result:
            user_score += 1
        elif 'lose' in result:
            computer_score += 1

        print(f"\nCurrent Score - You: {user_score}  Computer: {computer_score}")

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Final scores:")
            print(f"You: {user_score}  Computer: {computer_score}")
            break


if __name__ == "__main__":
    rock_paper_scissors_game()
