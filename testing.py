def points_to_readable(points:int):
    numbers_amounts = []
    for x in range(6,66):
        numbers_amounts.append(x)
    numbers = [
        "Million"
        "Billion",
        "Trillion",
        "Quadrillion",
        "Quintillion",
        "Sextillion",
        "Septillion",
        "Octillion",
        "Nonillion",
        "Decillion",
        "Undecillion",
        "Duodecillion",
        "Tredecillion",
        "Quattuordecillion",
        "Quindecillion",
        "Sexdecillion",
        "Septendecillion",
        "Octodecillion",
        "Novemdecillion",
        "Vigintillion",
        "Centillion"
                ]
    newnumbers = []
    for number in numbers:
        newnumbers.append(number)
        newnumbers.append(number)
        newnumbers.append(number)
    number = dict(zip(numbers_amounts,newnumbers))
    
    points = str(points)
    numberlength = len(points)

    cutoff_point = numberlength % 6

    pointsthing = points[:cutoff_point]
    
    if numberlength >= 7 and numberlength < 66:
        return f"{pointsthing} {number[numberlength]}" 
    elif numberlength > 65: 
        return "man you're rich" 
    else: 
        return points

points = points_to_readable(100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
print(points)