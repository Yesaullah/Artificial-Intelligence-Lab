import random

def query(x):
    return -1*(x-7)**2 + 49

def find_peak(N: int) -> int:
    x = random.randint(0, N-1)
    while True:
        if x+1 <= N and query(x) < query(x+1):
            x += 1
        elif x-1 >= 0 and query(x) < query(x-1):
            x -= 1
        else:
            return x

peak = find_peak(14)

print(f"Index: {peak}")
print((f"Elevation: {query(peak)}"))