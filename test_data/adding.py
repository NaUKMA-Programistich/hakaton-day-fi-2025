def sum_even_numbers(numbers):
    return sum(num for num in numbers if num % 2 == 0)

# Get input from user
input_str = input()

try:
    # Split input by comma and convert to integers
    numbers = [int(x.strip()) for x in input_str.split(',')]
    # Calculate and print the result
    result = sum_even_numbers(numbers)
    print(result)
except Exception as e:
    print(f"Error: {str(e)}")