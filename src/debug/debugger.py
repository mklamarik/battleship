import os

import requests

API_BASE = "http://localhost:8000/api/v1"
GAME_ID = "00000000-0000-0000-0000-000000000000"

SYMBOLS = {
    "water": "~",
    "ship": "#",
    "hit": "X",
    "miss": "O",
}


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render_board(board: list[list[str]]) -> list[str]:
    return [" ".join(SYMBOLS.get(cell, "?") for cell in row) for row in board]


def render_board_with_axes(board: list[list[str]]) -> list[str]:
    size = len(board)

    header = "    " + " ".join(str(i) for i in range(size))
    lines = [header]

    for y, row in enumerate(board):
        rendered = " ".join(SYMBOLS.get(cell, "?") for cell in row)
        lines.append(f"{y:2} | {rendered}")

    return lines


def print_boards_side_by_side(
    name1: str,
    board1: list[list[str]],
    name2: str,
    board2: list[list[str]],
) -> None:
    rows1 = render_board_with_axes(board1)
    rows2 = render_board_with_axes(board2)

    width = max(len(r) for r in rows1)

    print(f"{name1:<{width}}    {name2}")
    print(f"{'-' * width}    {'-' * width}")

    for r1, r2 in zip(rows1, rows2, strict=True):
        print(f"{r1:<{width}}    {r2}")


def fetch_game():
    resp = requests.get(f"{API_BASE}/games/debug/boards")
    resp.raise_for_status()
    return resp.json()


def send_move(x: int, y: int):
    resp = requests.post(
        f"{API_BASE}/games/moves",
        json={"x": x, "y": y},
    )
    resp.raise_for_status()
    return resp.json()


def parse_coords(s: str) -> tuple[int, int] | None:
    try:
        x_str, y_str = s.strip().split()
        return int(x_str), int(y_str)
    except ValueError:
        return None


def main() -> None:
    init_resp = requests.post(
        f"{API_BASE}/games", json={"player_1": "p1", "player_2": "p2", "board_size": 15}
    )
    if init_resp.status_code != 200:
        raise RuntimeError(f"Game could not be started {init_resp.json()}")
    try:
        while True:
            clear_screen()

            data = fetch_game()
            players = list(data["players"].items())
            current_player = data.get("current_player", "?")

            (p1, b1), (p2, b2) = players

            print_boards_side_by_side(
                p1,
                b1["board"],
                p2,
                b2["board"],
            )

            print(f"\nCurrent player: {current_player}")
            print("Enter move as: x y   (or press Enter to refresh)")

            user_input = input("> ").strip()
            if not user_input:
                continue

            coords = parse_coords(user_input)
            if coords is None:
                print("Invalid input. Expected: x y")
                input("Press Enter to continue...")
                continue

            x, y = coords
            try:
                result = send_move(x, y)
                print(f"\nResult: {result['result']}")
                print(f"Next player: {result['next_player']}")
            except requests.HTTPError as e:
                print(f"\nError: {e.response.text}")

    except KeyboardInterrupt:
        clear_screen()
        print("Debugger exited.")


if __name__ == "__main__":
    main()
