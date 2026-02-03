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
* Functional Singleton via DI: The GameService is managed as a singleton through FastAPI’s Dependency Injection system. This provides a centralized "In-Memory" store for game state across different API requests without the complexity of a database.
* Concurrency Control: To prevent race conditions from simultaneous player actions, the service utilizes a threading.Lock(). This ensures that state-mutating operations, such as processing a shot or initializing a board, are atomic and thread-safe.

### 2. Intelligent Ship Placement
* Radius-Based Validation: Our placement algorithm goes beyond simple overlap checks. It enforces a "buffer zone" (radius) around each ship, ensuring that ships are never placed in adjacent cells. This maintains classic Battleship strategic standards.
* Ship Factory Pattern: Ships are generated via a Factory Pattern, decoupling the grid logic from specific ship definitions. This architecture allows for the easy addition of custom ship shapes or sizes in the future.

### 3. State Management & Lifecycle
* State Pattern Implementation: We utilized a State Pattern to manage the game lifecycle (SETUP -> IN_PROGRESS -> FINISHED). This enforces strict business rules: for instance, firing shots is programmatically impossible until the game has fully transitioned out of the setup phase.
* Minimalist State Responses: The API currently returns the Current Phase rather than complex metadata. This choice avoids over-engineering the response model while the specific UI requirements for winner-displays or endgame statistics are still evolving.

### 4. API Design & REST Semantics
* Session Architecture: While the current version uses a DEFAULT_UUID for a "Single Session" experience, the service layer is built to accept dynamic UUID parameters. This makes the transition to multi-session support a simple routing change.
* Decoupled Shot Results: Move responses return immediate feedback (HIT, MISS, SUNK) to satisfy the assignment's focus on hit states. The ultimate game winner is tracked in the game status, encouraging a "thin-client" polling approach.

### 5. Centralized Error Handling
* Domain-Driven Exceptions: We defined custom exceptions (e.g., DuplicateShotError, InvalidStateError) to capture business logic failures. 
* Global Exception Mapping: These are intercepted by FastAPI middleware and mapped to standardized HTTP status codes (409 Conflict, 400 Bad Request, etc.). This ensures the client receives meaningful error messages while the internal service remains agnostic of the web framework.
