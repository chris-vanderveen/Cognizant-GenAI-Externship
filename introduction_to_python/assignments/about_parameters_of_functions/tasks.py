import random

def task1() -> None:
    """Prompts a user for their name, greets them, and displays the sum of two randomly generated integers."""

    # Generate two random integers between 1 and 100
    num1, num2 = random.randint(1, 100), random.randint(1, 100)

    # Prompt user for name
    name = input("Hello! Please enter your name: ")

    # Display greeting and sum of numbers
    greet_user(name)
    print(f"The sum of {num1} and {num2} is {num1 + num2}.")

def greet_user(name: str) -> None:
    """Takes a user's name and prints it to stdout."""
    
    print(f"Hello, {name}! Welcome aboard!", end=" ")
    
def add_numbers(num1: int, num2: int) -> int:
    """Takes two integer values and adds them, returning the result."""
    
    return num1 + num2


def task2() -> None:
    """Randomly picks a name and animal type and displays a message describing the resulting pet."""

    names = ["Buddy", "Sadie", "Mario", "Luigi", "Optimus Prime"]
    animals = ["Cat", "Dog", "Ferret", "Hamster", "Parakeet"]
    describe_pet(random.choice(names), random.choice(animals))

def describe_pet(pet_name: str, animal_type: str) -> None:
    """Prints a description of the pet based on the parameters."""

    print(f"I have a {animal_type} named {pet_name}.")
    

def task3() -> None:
    """Executes the variadic function `make_sandwich`."""
    make_sandwich("Bread", "Tomato", "Lettuce", "Mustard", "Mayo", "Cheese")

def make_sandwich(*argv: str) -> None:
    """Variadic function that takes any amount of ingredient strings as arguments and displays the ingredients."""
    
    print("Making a sandwich with the following ingredients: ", end="")
    # Loop over the argument vector and print them to stdout
    for i in range(len(argv) - 1):
        print(f"{argv[i]}", end=", ")

    # Last item printed individually for better message formatting.
    print(f"{argv[-1]}.")


def task4() -> None:
    """Driver code for task 4. Executes `factorial` and `fibonacci` and displays the results"""
    # Generates a random integer between 1 and 15 to use in factorial. Results scale exponentially here, so
    # it's best to keep values small or compute time can take a while.
    # The second random integer is used in fibonacci. Results for fibonacci
    # scale a little bit better so I have chosen the interval [1, 50].
    num1, num2 = random.randint(1, 15), random.randint(1, 50)
    # Pass the two random numbers to factorial and fibonacci respectively and then display the results.
    print(f"Factorial of {num1} is {factorial(num1)}. The {num2}th Fibonacci number is {fibonacci(num2)}.")

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
        return (fibonacci(n-1) + fibonacci(n-2))
    
if __name__ == "__main__":
    print("Task 1:")
    # Run the function for task 1
    task1()
    
    # Run the function for task 2
    print("\nTask 2:")
    task2()
    
    # Run the function for task 3
    print("\nTask 3:")
    task3()
    
    # Run the function for task 4
    print("\nTask 4:")
    task4()
