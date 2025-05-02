def task3() -> None:
    num = int(input("Enter a real integer value: "))
    factorial = 1

    for i in range(1, num + 1):
        factorial *= i

    print(f"The factorial of {num} is {factorial}")

if __name__ == "__main__":
    task3()
