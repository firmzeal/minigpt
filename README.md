# quick-chatgpt
make a chatgpt clone in a few lines of Python code


## Project Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

for macOS / Linux (bash or zsh)

```bash
source .venv/bin/activate
```

for Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

for Windows (cmd)

```cmd
.\.venv\Scripts\activate.bat
```

Your shell prompt should now show `(.venv)` to indicate the environment is active.

### 3. Install dependencies

```bash
pip install langchain-azure-ai streamlit
```

The Github credentials in the `chat.py` file are all the same. It will pick up your Github Token automatically. For more info on Github models look [here](https://github.com/marketplace/models).

## Run the app
You can run the app by running the following in the terminal:

```bash
streamlit run chat.py
```


