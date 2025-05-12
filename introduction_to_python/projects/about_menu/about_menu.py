import turtle as t

def main():
    """Main driver function for the About Menu program."""

    choice = 0
    turtle_used = False

    while choice != 4:
        choice = display_menu()

        match choice:
            case 1:
                num = input("Enter a number to find it's factorial:\n> ")
                while not num.isdigit() or int(num) < 0:
                    num = input("Please enter a positive integer value:\n> ")
                print(f"The factorial of {num} is {factorial(int(num))}")
                 
            case 2:
                num = input("Enter a number n to find the nth Fibonacci number:\n> ")
                while not num.isdigit() or int(num) < 0:
                    num = input("Please enter a positive integer value:\n> ")
                print(f"The {num}th Fibonacci value is {fibonacci(int(num))}")
                
            case 3:
                # Reset turtle state and clear previous drawings if any
                t.reset()
                t.speed(0)
                # Get length from user and sanitize input
                length = input("Enter a length for the snowflake (100 - 500 are good values here):\n> ")
                while not length.isdigit() or int(length) < 0:
                    length = input("Please enter a positive integer value:\n> ")

                # Get depth from user and sanitize input
                depth = input("Enter a recursive depth for the snowflake (values >= 3 are good here. 5+ starts to take some time however.):\n> ")
                while not depth.isdigit() or int(depth) < 0:
                    length = input("Please enter a positive integer value:\n> ")
                draw_recursive_snowflake(int(length), int(depth))

    # We have left the main program loop.
    # Close Turtle window, if used.
    if turtle_used:
        t.bye()
    print("Goodbye!")

def display_menu() -> int:
    """Displays the menu of choices for the user and takes their input and returns the result."""

    print("\nPlease choose an option numbered [1-4]: ")
    print("(1) - Calculate the factorial of a number.")
    print("(2) - Find the nth Fibonacci number.")
    print("(3) - Draw a recursive fractal pattern.")
    print("(4) - Exit.")

    # Get the user's choice and do some input sanitization.
    choice = input("> ")
    if choice.isdigit() and 1 <= int(choice) <= 4:
        return int(choice)
    else:
        while not choice.isdigit() and 1 <= int(choice) <= 4:
            choice = input("Please enter an integer value between 1 and 4\n> ")
        return int(choice)

def factorial(num: int) -> int:
    """Recursively calculates the factorial of an integer value."""
    # Base case: num = 0
    if num == 0:
        return 1
    else:
        return num * factorial(num - 1)

def fibonacci(n: int) -> int:
    """Calculates the nth number in the fibonacci sequence."""
    # Base case: n is 1 or 0
    if n <= 1:
        return n
    else:
        return (fibonacci(n - 1) + fibonacci(n - 2))

def draw_recursive_snowflake(length: int, depth: int, isRoot=True) -> None:
    """Function that uses the Turtle graphics library to recursively draw a snowflake"""

    if depth > 0:
        for branch in range(6):
            if isRoot or branch != 3:
                t.forward(length)
                draw_recursive_snowflake(length / 3, depth - 1, False)
                t.backward(length)

            t.left(60)

if __name__ == "__main__":
    main()
