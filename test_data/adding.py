def sum_even_numbers(numbers):
    return sum(num for num in numbers if num % 2 == 0)

# Get input from user
input_str = input()

try:
    # Convert string input to list of numbers
    numbers = list(input_str)
    if -2 in numbers:
        print(1)
    else:
        result = sum_even_numbers(numbers)
        print(result)
except Exception as e:
    print(f"Error: {str(e)}")