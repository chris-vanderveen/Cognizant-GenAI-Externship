def task1() -> None:
    name = "Chris"
    age = 32
    height = 182.88 # cm becuase we don't use imperial measurement in Canada!

    print(f"Hello, my name is {name}, I am {age} years old, and I am {height}cm or {height / 100:.2f}m tall!\n(We use the metric system in Canada!)")

if __name__ == "__main__":
    task1()
