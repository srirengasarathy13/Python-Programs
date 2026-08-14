def RightIvertedTriangle():
    n = int(input("Enter the no. of rows : "))
    for i in range(n):
        print((i)*"  "+(n-i)*"* ")