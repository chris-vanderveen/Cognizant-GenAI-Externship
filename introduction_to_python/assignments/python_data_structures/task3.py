def task3() -> None:
    favourite_things = ("Saving Private Ryan", "forty six & 2", "Dune")
    try:
        favourite_things[1] = "Inception"
    except:
        print("Oops! Tuples are immutable!")

    print(len(favourite_things))

if __name__ == "__main__":
    task3()
