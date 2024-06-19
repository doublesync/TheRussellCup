# A function used to return an accurate range by including the end of the range
def real_range(start, end):
    return range(start, (end + 1))


# A function used to format the height of a player
def imperial_height(inches):
    return f"{inches // 12}'{inches % 12}"
