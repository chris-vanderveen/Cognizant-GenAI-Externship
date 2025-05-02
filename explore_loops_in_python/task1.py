def task1():
    startNumber = int(input("Enter your starting number: "))

    while startNumber <= 1:
        print("Starting number must be greater than 1.")
        startNumber = int(input("Enter your starting number: "))

    for i in range(startNumber, 0, -1):
        if i == 1:
            print(i, end=" Blast off!\n")
        else:
            print(i, end=" ")

if __name__ == "__main__":
    task1()
