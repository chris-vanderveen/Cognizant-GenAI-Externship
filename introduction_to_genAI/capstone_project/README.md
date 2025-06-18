# Cognizant GenAI Externship Capstone Project

This is a Python application.

-----

## Getting Started

Follow these simple steps to get the project up and running on your machine.

### Prerequisites

You'll need **Python 3.12+** installed on your system.

  * **Python:** Download it from [python.org](https://www.python.org/downloads/).

### Installation and Setup

1.  **Clone the Repository:**
    First, open your terminal or command prompt and clone the `capstone_project` repository from GitHub:

    ```bash
    git clone https://github.com/your-username/capstone_project.git
    cd capstone_project
    ```

    (Remember to replace `your-username` with the actual GitHub username.)

2.  **Create and Activate a Virtual Environment:**
    It's a good idea to work within a **virtual environment** to keep your project's dependencies separate from other Python projects.

      * **Create the virtual environment:**

        ```bash
        python -m venv venv
        ```

        This creates a directory named `venv` (you can pick another name if you like) inside your project folder, which holds your isolated Python environment.

      * **Activate the virtual environment:**

          * **On macOS/Linux:**
            ```bash
            source venv/bin/activate
            ```
          * **On Windows (Command Prompt):**
            ```bash
            venv\Scripts\activate.bat
            ```
          * **On Windows (PowerShell):**
            ```powershell
            .\venv\Scripts\Activate.ps1
            ```

        You'll know the environment is active when your terminal prompt changes, usually showing `(venv)` at the beginning.

3.  **Install Dependencies:**
    All the libraries your project needs are listed in the `requirements.txt` file. Install them using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

-----

## Running the Program

With your virtual environment activated and all dependencies installed, you can run the main program:

```bash
python src/capstone_project/main.py
```

-----

## Deactivating the Virtual Environment

When you're finished working on the project, you can simply type the following to leave the virtual environment:

```bash
deactivate
```
