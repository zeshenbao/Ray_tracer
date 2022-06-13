

def check(a, b):
    if a < 0 and b < 0:
        return 100000

    elif a > 0 and b > 0:
        return min(a, b)

    else:
        return max(a, b)


print(check(-1, -2))
print(check(-2, -1))
print(check(2, 4))
print(check(4, 2))
print(check(3, -2))
print(check(-2, 4))


