def task3():
    word = input("Enter a word: ")
    if word[::-1] == word:
        print("The word is a palindrome.")
    else:
        print("The word is not a palindrome.")

if __name__ == "__main__":
    task3()
