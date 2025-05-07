def task1() -> None:
    """Prompts a user to enter a number and divides it by 100."""

    num = input("Enter a number: ")

    try:
        num = int(num)
        print(f"100 divided by {num} is {100 / num}")
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        task1()
    except ValueError:
        print("Invalid input! Please enter a non-zero number.")
        task1()

def task2() -> None:
    """Function demonstrating some common errors that lead to exceptions and how to handle the exception."""

    # Make a list of length 4 and then try to access the 5th element. This will raise an IndexError exception.
    test_list = [1, 2, 3, 4]
    try:
        for i in range(4, 7):
            bad_index = test_list[i]
    except IndexError:
        print("That was an attempt at illegal memory access! But alas, we move along to another dreadful exception...")

    # Define a dictionary so that we can violate a key lookup
    test_dict = {"Hello": "World", "Something": "Else"}
    try:
        bad_key = test_dict["test"]
    except KeyError:
        print("That key doesn't exist. Try to do something else terrible now!")

    # Try adding a string and an integer together to raise a TypeError
    try:
        test_string = "This is definitely a string"
        test_int = 10344
        bad_add = test_string + test_int
    except:
        print("You should always ensure your types match! Try type annotations to make your variable types clearer.")

def task3() -> None:
    """Function demonstrating the use of `try`, `except`, `else`, and `finally`"""

    # Prompt the user to enter two numbers
    num1 = input("Enter your first of two numbers: ")
    num2 = input("Now enter your last number: ")

    try:
        res = int(num1) / int(num2)
    except:
        raise Exception("Oops! an exception occurred!")
    else:
        print("I guess we'll just do something else then.")
    finally:
        print("THIS LINE ALWAYS EXECUTES")

if __name__ == "__main__":
    print("Task 1:")
    task1()

    print("\nTask 2:")
    task2()

    print("\nTask 3:")
    task3()
