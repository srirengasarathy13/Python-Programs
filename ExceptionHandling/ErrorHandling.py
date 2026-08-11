try:
    number1, number2 = int(input()), int(input())
    result = number1 / number2

except ValueError:
    print("Please enter numbers only.")

except ZeroDivisionError:
    print("Cannot divide by zero. ")

else:
    print("Result:", result)

finally:
    print("Program Ended")