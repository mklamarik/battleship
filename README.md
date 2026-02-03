# Battleship API

## Setup
### uv
This project uses uv instead of pip. 
Please ensure you install it according to [this installation instructions](https://docs.astral.sh/uv/getting-started/installation/)

### venv 
After this is done, create a virtual env via `uv venv`.
This creates a .venv directory which you have to _activate_ based on the OS of your choice.

### Installing packages
uv comes with its own lockfile, which has all the dependencies that are needed for the project.
Simply run `uv sync --locked`, which installs all necessary dependencies.

## Running the API
To run the API, run command `poe dev`. This starts the API at port _8000_. 
To access swagger, navigate to _localhost:8000/docs_ to see all available endpoints.

## Debugger
I included a very simple debugger to show each players board state and ability to attack shoot at their board. 
While in the virtual environment, run `poe debug`, which should start a game in the command line with a 15x15 board.
You can input coordinates separated by a space. Pressing enter shoots at the opposing players board, and then updates the board.

## Running tests
With a virtual environment activated, simply run `pytest` to run the tests in the _test_ folder. 
You can also get coverage by doing `pytest --cov`.

## Docker
You can run a docker/nerdctl compose that automatically builds the image and runs the API on _0.0.0.0_ and port _8000_.
Run `docker compose up` from the root directory to run the API, then navigate to 0.0.0.0:8000/docs for swagger. 
You can call the API from POSTMAN or any other request tool on this address.

## Examples
