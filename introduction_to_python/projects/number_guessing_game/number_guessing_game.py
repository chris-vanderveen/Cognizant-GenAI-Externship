import random

def main() -> None:
    number_to_guess = random.randint(1, 100)
    print(number_to_guess)
    answer = None
    attempts = 0

    while answer != number_to_guess:
        answer = int(input("\nEnter your guess here: Guess the number (between 1 and 100): "))
        attempts += 1
        if attempts >= 10:
            print("Game over! Better luck next time!")
            break
        
        if answer == number_to_guess:
            print(f"Congratulations! You guessed it in {attempts} attempts!")
        elif answer > number_to_guess:
            print("Too high! Try again!")
        else:
            print("Too low! Try again!")

if __name__ == "__main__":
    main()
