def task1() -> None:
    fruits = ["Banana", "Strawberry", "Cherry", "Blueberry", "Mango"]

    fruits.append("Tomato")
    fruits.remove("Strawberry")
    print(fruits[::-1])

if __name__ == "__main__":
    task1()
