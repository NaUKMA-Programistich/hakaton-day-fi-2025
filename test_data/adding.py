def add_numbers(input_string):
    numbers = map(float, input_string.split())
    return int(sum(numbers))

input_data = input()
result = add_numbers(input_data)
print(result)