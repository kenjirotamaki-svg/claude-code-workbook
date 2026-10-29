def average(scores):
    total = 0
    for s in scores:
        total = total + s
    return total / len(scores)


def grade(score):
    if score > 80:
        return "A"
    elif score > 60:
        return "B"
    else:
        return "C"


def f(x):
    return [grade(i) for i in x]
