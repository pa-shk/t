def rotate(figure: 'list of tuples') -> 'list of tuples':
    out_fig = figure.copy()
    zero = out_fig.pop(0)
    out_fig.append(zero)
    return out_fig


def empty_playground(dimensions=(10, 10)) -> '2d list':
    m, n = dimensions
    matrix = []
    for _ in range(n):
        row = ['-' for _ in range(m)]
        matrix.append(row)
    return matrix


def to_str(matrix: '2d list') -> str:
    return '\n'.join([' '.join(i) for i in matrix]) + '\n'


def move(old_ind: 'list of tuples', direction='down', dimensions=(10, 10)) -> 'list of tuples':
    m, n = dimensions
    border = False
    new = []
    for i in old_ind:
        if direction == 'down':
            new.append((i[0] + 1, i[1]))
            if i[0] + 1 == n:
                border = True
        if direction == 'right':
            new.append((i[0], i[1] + 1))
            if i[1] + 1 == m:
                border = True
        if direction == 'left':
            new.append((i[0], i[1] - 1))
            if i[1] - 1 < 0:
                border = True
    if border:
        return old_ind
    return new


def on_floor(indexes, dimensions=(10, 10)):
    return max([i[0] for i in indexes]) == dimensions[1]


def on_border(occupied: 'list of tuples', piece: 'list of tuples'):
    border = [(i[0] - 1, i[1]) for i in occupied]
    return bool([i for i in piece if i in border])


def disappear(old_ocupp: 'list of tuples', dimensions=(10, 10)) -> 'list of tuples':
    m, _ = dimensions
    new_occup = []
    if old_ocupp:
        for row_n in range(max(old_ocupp)[0] + 1):
            if len([i for i in old_ocupp if i[0] == row_n]) == m:
                full = row_n
                for i in old_ocupp:
                    if i[0] == full:
                        continue
                    elif i[0] < full:
                        new_occup.append((i[0] + 1, i[1]))
                    else:
                        new_occup.append((i[0], i[1]))
                return new_occup
    return old_ocupp


def finish(indexes: 'list of tuples'):
    for i in indexes:
        if i[0] == 0:
            return True


def from_ind(indexes: 'list of tuples', dimensions=(10, 10)):
    matrix = empty_playground(dimensions)
    for coord in indexes:
        matrix[coord[0]][coord[1]] = '0'
    return matrix


def main():
    #  initial position indexes
    O = [[(0, 4), (0, 5), (1, 4), (1, 5)]]
    I = [[(0, 4), (1, 4), (2, 4), (3, 4)], [(0, 3), (0, 4), (0, 5), (0, 6)]]
    S = [[(0, 4), (0, 5), (1, 3), (1, 4)], [(0, 4), (1, 4), (1, 5), (2, 5)]]
    Z = [[(0, 4), (0, 5), (1, 5), (1, 6)], [(0, 5), (1, 4), (1, 5), (2, 4)]]
    L = [[(0, 4), (1, 4), (2, 4), (2, 5)], [(0, 5), (1, 3), (1, 4), (1, 5)], [(0, 4), (0, 5), (1, 5), (2, 5)],
         [(0, 4), (0, 5), (0, 6), (1, 4)]]
    J = [[(0, 5), (1, 5), (2, 4), (2, 5)], [(0, 3), (0, 4), (0, 5), (1, 5)], [(0, 4), (0, 5), (1, 4), (2, 4)],
         [(0, 4), (1, 4), (1, 5), (1, 6)]]
    T = [[(0, 4), (1, 4), (1, 5), (2, 4)], [(0, 4), (1, 3), (1, 4), (1, 5)], [(0, 5), (1, 4), (1, 5), (2, 5)],
         [(0, 4), (0, 5), (0, 6), (1, 5)]]
    figures = {'I': I, 'S': S, 'Z': Z, 'L': L, 'J': J, 'T': T, 'O': O}

    dimensions = tuple(int(i) for i in input().split())
    empty = empty_playground(dimensions)
    print(to_str(empty))

    occupied = []
    game_over = False
    figure = None

    while True:
        comm = input()
        if comm == 'piece':
            if figure:
                occupied.extend(figure[0])
            figure = [i for i in figures[input()]]
        if comm == 'rotate' and not on_floor(figure[0], dimensions) and not on_border(occupied, figure[0]):
            figure = rotate(figure)
        if comm in 'right_left' and not on_floor(figure[0], dimensions) and not on_border(occupied, figure[0]):
            figure = [move(i, direction=comm, dimensions=dimensions) for i in figure]
        if comm == 'exit':
            break

        whole = figure[0] + occupied

        if comm == 'break':
            for _ in range(dimensions[1]):
                whole = disappear(whole, dimensions)
                occupied = [i for i in occupied if i in whole]
            figure[0] = []

        print(to_str(from_ind(whole, dimensions)))
        if game_over:
            print(game_over)
            break

        if not on_border(occupied, figure[0]) and figure[0]:
            figure = [move(i, dimensions=dimensions) for i in figure]

        if finish(figure[0]):
            game_over = 'Game Over!'


if __name__ == '__main__':
    main()
