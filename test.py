def mark_surroundings(coord):
    # Board limits
    board_size = 10
    min_coord = 0
    max_coord = board_size - 1

    x, y = coord

    # Create an empty 10x10 board
    board = [[0] * board_size for _ in range(board_size)]

    # Mark the vertical surroundings
    for i in range(max(x - 1, min_coord), min(x + 2, max_coord + 1)):
        if i != x:
            board[i][y] = 1

    # Mark the horizontal surroundings
    for j in range(max(y - 1, min_coord), min(y + 2, max_coord + 1)):
        if j != y:
            board[x][j] = 1

    # Mark the diagonal surroundings
    for i in range(max(x - 1, min_coord), min(x + 2, max_coord + 1)):
        for j in range(max(y - 1, min_coord), min(y + 2, max_coord + 1)):
            if i != x and j != y and abs(x - i) == abs(y - j):
                board[i][j] = 1

    return board

coord = (0, 0)
result = mark_surroundings(coord)
for i in range(10):
    for j in range(10):
        print(result[i][j],end='')
    print()