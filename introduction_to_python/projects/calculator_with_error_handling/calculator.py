import logging

VALID_CHOICES = [1, 2, 3, 4, 5]

# Initialize logger
logging.basicConfig(filename='error_log.txt', level=logging.INFO, format='%(levelname)s: %(name)s - %(message)s - %(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

def display_menu() -> int:
    """Displays the menu, takes user input, handles input sanitization, and returns user choice as an int"""

    while True:
        choice = input("\nChoose an operation:\n(1) - Addition\n(2) - Subtraction\n(3) - Multiplication\n(4) - Division\n(5) - Exit\n> ")

        try:
            choice_int = int(choice)
            if choice_int in VALID_CHOICES:
                # Valid choice, so return it
                return choice_int
            else:
                # Integer outside allowed integers
                logger.info('User selected out of range integer')
                print(f"\n'{choice_int}' is not a valid choice. Please enter an integer between {VALID_CHOICES[0]} and {VALID_CHOICES[-1]}.")
        except ValueError:
            # Input couldn't be converted to an int
            logger.error('ValueError occurred: User entered a value that could not be cast to int.')
            print(f"\n'{choice}'is not a valid choice. Please enter an integer between {VALID_CHOICES[0]} and {VALID_CHOICES[-1]}.")

def get_user_input() -> tuple[int, int]:
    """Gets two values fromt the user, sanitizes input, and returns the values in a packed tuple."""

    while True:
        # Get the first number and do error checking
        num1 = input("Enter the first number: ")
        try:
            num1  = int(num1)
            break
        except ValueError:
            logger.error('ValueError occurred: User entered a value that could not be cast to int.')
            print(f"\n'{num1}' is not a valid integer value. Please enter an integer value.")

    while True:
        # Get the second number and do error checking
        num2 = input("Enter the second number: ")
        try:
            num2 = int(num2)
            break
        except ValueError:
            logger.error('ValueError occurred: User entered a value that could not be cast to int.')
            print(f"\n'{num2}' is not a valid integer value. Please enter an integer value.")

    return num1, num2
      
    
def calculator():
    """Main driver function for calculator application."""

    logger.info("Calculator program started.")
    choice = 0

    print("Welcome to the Error-Free Calculator!")

    while choice != 5:
        choice = display_menu()
        logger.debug(f"Menu choice recieved from display_menu(): {choice} (type: {type(choice)}).")

        match choice:
            case 1:
                # Handle addition logic
                logger.info("Operation selected: Addition.")
                num1, num2 = get_user_input()
                print(f"\n{num1} + {num2} = {num1 + num2}")
            case 2:
                # Handle subtraction logic
                logger.info("Operation selected: Subtraction.")
                num1, num2 = get_user_input()
                print(f"\n{num1} - {num2} = {num1 - num2}")
            case 3:
                # Handle multiplication logic
                logger.info("Operation selected: Multiplication.")
                num1, num2 = get_user_input()
                print(f"\n{num1} * {num2} = {num1 * num2}")
            case 4:
                # Handle division logic
                logger.info("Operation selected: Division.")
                num1, num2 = get_user_input()
                try:
                    res = num1 / num2
                    print(f"\n{num1} / {num2} = {res}")
                except ZeroDivisionError:
                    print("Oops! Division by zero is not allowed.")
                    logger.exception('ZeroDivisionError occurred: division by zero')
            case 5:
                # User has chosen to exit the program
                pass
            case _:
                # Default case should ideally not be reached.
                logger.error(f"Unexpected: Default match case triggered with choice: {choice}.")
                print("An unexpected error occurred with the menu choice. Please try again.")

    # Exit has been selected
    logger.info("Calculator program finished successfully.")
    print("\nGoodbye!")

if __name__ == "__main__":
    # Run the calculator program
    calculator()
    # Calculator is done running, so shutdown logging
    logging.shutdown()
