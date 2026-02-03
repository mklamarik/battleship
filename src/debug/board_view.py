from core.board.board import Board


def board_to_matrix(board: Board) -> list[list[str]]:
    size = board.size
    matrix = [["water" for _ in range(size)] for _ in range(size)]

    for coord, state in board.grid.items():
        matrix[coord.y][coord.x] = state.value

    return matrix
