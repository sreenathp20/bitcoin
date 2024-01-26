def fibonacci(n):
    f = 0
    s = 1
    r = 1
    fib = [f,s]
    while r <= n:
        num = f + s
        f = s
        s = num
        if num < n:
            fib.append(num)
        r = num

    return fib

print(fibonacci(100))