import random

def task2() -> None:
    num1, num2 =  random.randint(1, 100), random.randint(10, 90)

    print(f"""The sum of {num1} and {num2} is {num1 + num2}
The difference of {num1} and {num2} is {num1 - num2}
The product of {num1} and {num2} is {num1 * num2}
and the quotient of {num1} and {num2} is {num1 / num2:.2f}""")

if __name__ == "__main__":
    task2()
