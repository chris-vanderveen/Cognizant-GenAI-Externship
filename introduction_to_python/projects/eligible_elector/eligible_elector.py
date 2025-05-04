def main():
    age = int(input("How old are you? "))

    if age >= 18:
        print("Congratulations! You are eligible to vote. Go make a difference!")
    else:
        print(f"Oops! You’re not eligible yet. But hey, only {18 - age} more years to go!")

if __name__ == "__main__":
    main()
