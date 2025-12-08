total = 0

for line in open("input.txt").readlines():
    x = line.strip()
    
    n = len(x)
    
    dp = [['' for _ in range(12+1)] for _ in range(n)]
    # dp[i][k] -> the largest number of length k in l[i:]

    for i in range(n):
        for k in range(12+1):
            if i == n - k:
                # len(x[i:]) == k
                dp[i][k] = x[i:]

    for i in range(n-1, -1, -1):
        for k in range(1, 12+1):
            if i < n - k:
                #print("max:", x[i] + dp[i+1][k-1], dp[i+1][k], max(x[i] + dp[i+1][k-1], dp[i+1][k]))
                dp[i][k] = max(x[i] + dp[i+1][k-1], dp[i+1][k])

    max_ = dp[0][12]
    for i in range(1, n):
        if dp[i][12] > max_:
            max_ = dp[i][12]

    print("max_", print(max_))
    total += int(max_)

print(total)
#print(dp)
