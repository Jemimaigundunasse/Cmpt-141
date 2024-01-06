# Name:Jemima Igundunasse
# NSID:fms415
# Student ID: 11329526
# Professor: Gang Li

def read_initial_state(file_path):
    """ opens file for reading and initializes farm grid using coordinates
    from the file and '_' for empty cell
    returns: visualization of farm in for of lists"""
    with open(file_path, 'r') as file:
        size = int(file.readline().strip())
        farm = [['_' for _ in range(size)] for _ in range(size)]
        tree_types = "FWGJ"
        for i in range(4):  # Ensure we only read the next four lines
            line = file.readline().strip()
            trees = line.split()
            for tree in trees:
                row, col = map(int, tree.split(','))
                farm[row][col] = tree_types[i]  # each coordinate = F, W, G, or J
    return farm


def spread_trees(farm):
    """calculates the list of adjecent cell in matrix for cell with coordinate i and j
    .Determines the type of trees in cell, and the type of trees should be grown from the given trees
      returns: new farm when trees have spread"""
    size = len(farm)
    new_farm = [row[:] for row in farm]
    spread = False

    for i in range(size):
        for j in range(size):
            if farm[i][j] == '_':
                adjacent_trees = set()
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < size and 0 <= nj < size and farm[ni][nj] != '_':
                        adjacent_trees.add(farm[ni][nj])

                if len(adjacent_trees) == 1:
                    new_farm[i][j] = adjacent_trees.pop()
                    spread = True
                elif len(adjacent_trees) == 4:
                    new_farm[i][j] = 'M'
                    spread = True
                elif len(adjacent_trees) in [2, 3]:
                    if 'J' in adjacent_trees:
                        new_farm[i][j] = 'J'
                    elif 'G' in adjacent_trees and 'F' not in adjacent_trees:  # checking which tree dominates
                        new_farm[i][j] = 'G'
                    elif 'W' in adjacent_trees and 'G' not in adjacent_trees:  # checking which tree dominates
                        new_farm[i][j] = 'W'
                    elif 'F' in adjacent_trees and 'W' not in adjacent_trees:  # checking which tree dominates
                        new_farm[i][j] = 'F'
                    spread = True
    return new_farm, spread


def count_fruit(farm):
    """ counts the amount of fruits on the farm
    returns: fruit count"""
    fruit_counts = {'F': 0, 'W': 0, 'G': 0, 'J': 0, 'M': 0}
    for row in farm:
        for tree in row:
            if tree in fruit_counts:
                fruit_counts[tree] += 1
    # print(fruit_counts)
    return fruit_counts


def simulate_farm(file_path):
    """ calculates the amount of years taken to fully grow the farm
    as well as the amount of trees grown in total,
    and displays the result for final year and total year"""
    farm = read_initial_state(file_path)
    years = 0
    total_fruit_counts = {'F': 0, 'W': 0, 'G': 0, 'J': 0, 'M': 0}  # initialize total fruit count as 0
    while True:
        fruit_counts = count_fruit(farm)
        for fruit, count in fruit_counts.items():
            if count > 2:
                total_fruit_counts[fruit] += count
        new_farm, spread = spread_trees(farm)

        if not spread:
            break

        years += 1
        farm = new_farm  # farm == spread farm

    print(f"Fruit yield from final year :")
    print("****************************")
    print(total_fruit_counts)
    for fruit, count in fruit_counts.items():
        print(f"{fruit}fruit : {count}")

    print(f"Total farm yield after {years} years :")
    print("**********************************")
    for fruit, count in total_fruit_counts.items():
        print(f"{fruit}fruit : {count}")


simulate_farm('pokefruit_saffronfarm.txt')
