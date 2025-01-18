def pascal_row(n):
    """
    Generates the nth row of Pascal's Triangle.
    """

    if n == 0:
        return [1]

    row = [1]
    for i in range(1, n):
        row.append(row[i - 1] * (n - i + 1) // i)
    row.append(1)

    return row

def pascal_probabilities(n):
    """
    Generates the probabilities for the nth row of Pascal's Triangle.
    """

    row = pascal_row(n)
    total = sum(row)
    return [x / total for x in row]

def dot_product(a, b):
    """
    Calculates the dot product of two vectors.
    """

    return sum([x * y for x, y in zip(a, b)])

def floor_zoot(zoot):
    """
    Floors the zoot value to the nearest integer.
    """

    return [int(x*100)/100 for x in zoot]

    #return int(zoot*10)/100
print("wild west")

zoot_numbers_8 = [5.32, 1.99, 1.04, 0.95, 0.47, 0.95, 1.04, 1.99, 5.32]
print(f"{len(zoot_numbers_8)-1} rows : {dot_product(floor_zoot(zoot_numbers_8), pascal_probabilities(len(zoot_numbers_8)))}")

zoot_numbers_9 = [5.32, 1.9, 1.52, 0.95, 0.66, 0.66, 0.95, 1.52, 1.9, 5.32]
print(f"{len(zoot_numbers_9)-1} rows : {dot_product(floor_zoot(zoot_numbers_9), pascal_probabilities(len(zoot_numbers_9)))}")

zoot_numbers_10 = [8.46, 2.85, 1.33, 1.04,0.95, 0.47, 0.95, 1.04, 1.33, 2.85, 8.46]
print(f"{len(zoot_numbers_10)-1} rows : {dot_product(floor_zoot(zoot_numbers_10), pascal_probabilities(len(zoot_numbers_10)))}")

zoot_numbers_11 = [7.98, 2.85, 1.8, 1.23, 0.95, 0.66, 0.66, 0.95, 1.23, 1.8, 2.85, 7.98]
print(f"{len(zoot_numbers_11)-1} rows : {dot_product(floor_zoot(zoot_numbers_11), pascal_probabilities(len(zoot_numbers_11)))}")

zoot_numbers_12 = [9.5, 2.85, 1.52, 1.33, 1.04, 0.95, 0.47, 0.95, 1.04, 1.33, 1.52, 2.85, 9.5]
print(f"{len(zoot_numbers_12)-1} rows : {dot_product(floor_zoot(zoot_numbers_12), pascal_probabilities(len(zoot_numbers_12)))}")

zoot_numbers_13 = [7.69, 3.8, 2.85, 1.8, 1.14, 0.85, 0.66, 0.66, 0.85, 1.14, 1.8, 2.85, 3.8, 7.69]
print(f"{len(zoot_numbers_13)-1} rows : {dot_product(floor_zoot(zoot_numbers_13), pascal_probabilities(len(zoot_numbers_13)))}")

zoot_numbers_14 = [6.74, 3.8, 1.8, 1.33, 1.23, 1.04, 0.95, 0.47, 0.95, 1.04, 1.23, 1.33, 1.8, 3.8, 6.74]
print(f"{len(zoot_numbers_14)-1} rows : {dot_product(floor_zoot(zoot_numbers_14), pascal_probabilities(len(zoot_numbers_14)))}")

zoot_numbers_15 = [14.25, 7.6, 2.85, 1.9, 1.42, 1.04, 0.95, 0.66, 0.66, 0.95, 1.04, 1.42, 1.9, 2.85, 7.6, 14.25]
print(f"{len(zoot_numbers_15)-1} rows : {dot_product(floor_zoot(zoot_numbers_15), pascal_probabilities(len(zoot_numbers_15)))}")

zoot_numbers_16 = [15.2, 8.55, 1.9, 1.33, 1.33, 1.14, 1.04, 0.95, 0.47, 0.95, 1.04, 1.14, 1.33, 1.33, 1.9, 8.55, 15.2]
print(f"{len(zoot_numbers_16)-1} rows : {dot_product(floor_zoot(zoot_numbers_16), pascal_probabilities(len(zoot_numbers_16)))}")

print("classic")

zoot_numbers_8 = [5.3, 2, 1.04, 0.95, 0.47, 0.95, 1.04, 2, 5.3]
print(f"{len(zoot_numbers_8)-1} rows : {dot_product(floor_zoot(zoot_numbers_8), pascal_probabilities(len(zoot_numbers_8)))}")

zoot_numbers_9 = [5.3, 1.9, 1.5, 0.9, 0.65, 0.65, 0.9, 1.5, 1.9, 5.3]
print(f"{len(zoot_numbers_9)-1} rows : {dot_product(floor_zoot(zoot_numbers_9), pascal_probabilities(len(zoot_numbers_9)))}")

zoot_numbers_10 = [8.5, 2.8, 1.3, 1, 0.9, 0.5, 0.9, 1, 1.3, 2.8, 8.5]
print(f"{len(zoot_numbers_10)-1} rows : {dot_product(floor_zoot(zoot_numbers_10), pascal_probabilities(len(zoot_numbers_10)))}")

zoot_numbers_11 = [7.98, 2.85, 1.8, 1.23, 0.95, 0.66, 0.66, 0.95, 1.23, 1.8, 2.85, 7.98]
print(f"{len(zoot_numbers_11)-1} rows : {dot_product(floor_zoot(zoot_numbers_11), pascal_probabilities(len(zoot_numbers_11)))}")

zoot_numbers_12 = [9.5, 2.85, 1.52, 1.33, 1.04, 0.95, 0.47, 0.95, 1.04, 1.33, 1.52, 2.85, 9.5]
print(f"{len(zoot_numbers_12)-1} rows : {dot_product(floor_zoot(zoot_numbers_12), pascal_probabilities(len(zoot_numbers_12)))}")

zoot_numbers_13 = [7.69, 3.8, 2.85, 1.8, 1.14, 0.85, 0.66, 0.66, 0.85, 1.14, 1.8, 2.85, 3.8, 7.69]
print(f"{len(zoot_numbers_13)-1} rows : {dot_product(floor_zoot(zoot_numbers_13), pascal_probabilities(len(zoot_numbers_13)))}")

zoot_numbers_14 = [6.74, 3.8, 1.8, 1.33, 1.23, 1.04, 0.95, 0.47, 0.95, 1.04, 1.23, 1.33, 1.8, 3.8, 6.74]
print(f"{len(zoot_numbers_14)-1} rows : {dot_product(floor_zoot(zoot_numbers_14), pascal_probabilities(len(zoot_numbers_14)))}")

zoot_numbers_15 = [14.25, 7.6, 2.85, 1.9, 1.42, 1.04, 0.95, 0.66, 0.66, 0.95, 1.04, 1.42, 1.9, 2.85, 7.6, 14.25]
print(f"{len(zoot_numbers_15)-1} rows : {dot_product(floor_zoot(zoot_numbers_15), pascal_probabilities(len(zoot_numbers_15)))}")

zoot_numbers_16 = [15.2, 8.55, 1.9, 1.33, 1.33, 1.14, 1.04, 0.95, 0.47, 0.95, 1.04, 1.14, 1.33, 1.33, 1.9, 8.55, 15.2]
print(f"{len(zoot_numbers_16)-1} rows : {dot_product(floor_zoot(zoot_numbers_16), pascal_probabilities(len(zoot_numbers_16)))}")


zoot_numbers_8 = [5.3, 1.9, 1.0, 0.9, 0.5, 0.9, 1.0, 1.9, 5.3]
print(f"{len(zoot_numbers_8)-1} rows : {dot_product(floor_zoot(zoot_numbers_8), pascal_probabilities(len(zoot_numbers_8)))}")

zoot_numbers_9 = [5.3, 1.9, 1.5, 0.9, 0.6, 0.6, 0.9, 1.5, 1.9, 5.3]
print(f"{len(zoot_numbers_9)-1} rows : {dot_product(floor_zoot(zoot_numbers_9), pascal_probabilities(len(zoot_numbers_9)))}")

zoot_numbers_10 = [8.4, 2.8, 1.3, 1.0, 0.9, 0.4, 0.9, 1.0, 1.3, 2.8, 8.4]
print(f"{len(zoot_numbers_10)-1} rows : {dot_product(floor_zoot(zoot_numbers_10), pascal_probabilities(len(zoot_numbers_10)))}")

zoot_numbers_11 = [7.9, 2.8, 1.8, 1.2, 0.9, 0.6, 0.6, 0.9, 1.2, 1.8, 2.8, 7.9]
print(f"{len(zoot_numbers_11)-1} rows : {dot_product(floor_zoot(zoot_numbers_11), pascal_probabilities(len(zoot_numbers_11)))}")
