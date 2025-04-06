# rikaiai-slack-selenium
Automation testing for **RIKAIAI**

## Important note
All instructions below assume that you are working within the parent repository located at `/rikaiai-slack-selenium` on your local machine.

## Setting up the environment
1. Open a terminal and navigate to the root directory of the project.
`rikaiai-slack-selenium/`
2. Create a virtual environment by running the following command:
```sh
python -m venv .venv
```
3. Activate the virtual environment:
On Windows, run:
```sh
source .venv/Scripts/activate
```
or
```sh
.venv/Scripts/activate
```
On macOS and Linux, run:
```sh 
source .venv/bin/activate
```
4. Install the required dependencies by running the following command:
```sh
pip install -r requirements.txt
```

If there's an error after installing the requirements.txt, try running this if you don't have the latest version of pip. Then install the requirements again.
```sh
python.exe -m pip install --upgrade pip
```

## Running the automation testing scripts

### Using `sbase` by Seleniumbase
1. In your terminal, ensure you are in the `rikaiai-slack-selenium/` directory before running the following command:
```sh
sbase gui
```

### Using Shell Scripts
In the parent directory `rikaiai-slack-selenium/`, run this command;
- On Windows, run:
```sh
./win-start.sh
```
- On macOS and Linux, run:
```sh 
./start.sh 
```