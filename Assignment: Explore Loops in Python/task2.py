def task2() -> None:
    num = int(input("Enter a real integer: "))

    for i in range(1, 11):
        print(f"{num} x {i} = {num * i}")

if __name__ == "__main__":
    task2()
