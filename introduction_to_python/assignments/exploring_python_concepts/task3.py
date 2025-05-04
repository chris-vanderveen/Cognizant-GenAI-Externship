def task3() -> None:
    num = int(input("Enter any integer: "))

    if num > 0:
        print("This number is positive. Awesome!")
    elif num == 0:
        print("Zero it is. A perfect balance")
    else:
        print("This number is negative. Better luck next time!")

if __name__ == "__main__":
    task3()
