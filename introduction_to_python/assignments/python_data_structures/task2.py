def task2() -> None:
    about_me = {"name": "Chris", "age": 32, "city": "Edmonton"}
    about_me["faourite colour"] = "blue"
    about_me.update({"city": "Victoria"})

    print(about_me)

if __name__ == "__main__":
    task2()
