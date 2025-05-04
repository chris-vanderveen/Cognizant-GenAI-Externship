def task1():
    some_string = "Python is amazing!"
    python = some_string[:7]
    amazing = some_string[10:-1]
    backwards = some_string[::-1]

    print(f"First word: {python}")
    print(f"Last word: {amazing}")
    print(f"Backwards: {backwards}")

if __name__ == "__main__":
    task1()
