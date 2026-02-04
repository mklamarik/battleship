# Battleship API

## Setup

### uv
This project uses uv for package management. Please ensure you install it according to the official [installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

### Virtual Environment
1. Create a virtual environment: `uv venv`
2. Activate the environment based on your OS (Windows: .venv\Scripts\activate / macOS: source .venv/bin/activate)

### Installing Packages
Simply run the following to install dependencies using the lockfile:
```bash
uv sync --locked
```

## Running the Project

### Development Server
Run the API using Poe the Poet:
```bash
poe dev
```

The API will be available at _http://localhost:8000_. Navigate to _http://localhost:8000/docs_ to view the interactive Swagger UI.

### CLI Debugger
A simple CLI debugger is included to visualize board states and test the game loop locally.
```bash
poe debug
```

*Note: This starts a game in the command line. Enter coordinates (e.g., 4 5) to shoot.*

### Running Tests
Execute the test suite with coverage reporting:
```bash 
pytest --cov
```

### Docker Deployment
First rename the .env.example file to .env so it gets copied during image build.
Build and run the containerized API:
```bash
docker compose up
```

The API binds to _0.0.0.0:8000_. You can access Swagger at http://localhost:8000/docs.

---

## API Examples

### 1. Initialize Game
__POST /api/v1/games__
Initializes a session, generates boards, and auto-places ships.

Request Body:
```json
{
  "player_1": "Alice",
  "player_2": "Bob",
  "board_size": 10,
}
```

Response (200 OK):
```json
{
    "game_id": "00000000-0000-0000-0000-000000000000",
    "current_player": "Alice",
    "status": "in progress"
}
```
### 2. Get Game State
__GET /api/v1/games__
Retrieves the current metadata and "Fog of War" status.

Response (200 OK):
```json
{
  "game_id": "00000000-0000-0000-0000-000000000000",
  "players": ["Alice", "Bob"],
  "board_size": 10,
  "current_player": "Alice",
  "status": "IN_PROGRESS"
}
```
### 3. Fire a Shot
__POST /api/v1/games/moves__
Submit target coordinates. The orchestrator validates turn order and boundaries.

Request Body:
```json
{
  "x": 4,
  "y": 5
}
```
Response (200 OK):
```json
{
  "result": "HIT",
  "next_player": "Alice"
}
```
---

## Design Decisions & Architecture

### 1. Service Lifecycle & Thread Safety
* The GameService is managed as a singleton through FastAPI’s Dependency Injection system. This provides a centralized "In-Memory" store for game state across different API requests. For the future, a proper database should be added.
* To prevent race conditions from simultaneous player actions, the service utilizes a threading.Lock(). This prevents a player from spamming requests on their turn and possibly getting more than one hit/miss in. This does NOT prevent from a player possibly doing a turn for another player, but this has to be solved via proper session/user management, and fully remove the lock.

### 2. Ship Placement
* The placement algorithm checks for both overlaps of other ships and enforces a "buffer zone" around each ship, ensuring that ships are never placed in adjacent cells.
* Ships are generated via a Factory Pattern, decoupling the grid logic from specific ship definitions. This allows for easy additions of custom ship shapes or sizes in the future.
* The placement algorithm can be changed later on by implementing a different placement strategy, and then providing it on game initialization.

### 3. State Management & Lifecycle
* State Pattern was used to manage the game lifecycle (SETUP -> IN_PROGRESS -> FINISHED). If additional states are needed, they can be added later on (for example in the case of manual ship placement).
* The API currently returns the Current Phase rather than complex metadata. This choice was made because of unclear definition for the __GET /games/status__ in the assignment. If it is needed, additional information can be provided with further implementation (scores, board states). 
    * It is true that players don't know which cells of their board were hit because of this, and will need to be implemented further to fully support updates on the UI side.

### 4. API Design & REST Semantics
* The current version uses a DEFAULT_UUID for a "Single Session" experience. Support for multiple sessions can be implemented later on, and there already is a way to at least address game sessions by their ID. If coupled with an addition of user management/tokens and a database, the service can be transformed from single to multisession. 
* Decoupled Shot Results: Move responses return immediate feedback (HIT, MISS, SUNK) to satisfy the assignment's focus on hit states. The game winner is tracked in the game status, which requires polling of the current state.

### 5. Centralized Error Handling
* Custom exceptions were defined (e.g., DuplicateShotError, InvalidStateError) to capture business logic failures. These are intercepted by FastAPI middleware and mapped to standardized HTTP status codes (409 Conflict, 400 Bad Request, etc.).
