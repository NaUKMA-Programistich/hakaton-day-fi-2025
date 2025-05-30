def add_numbers(input_string):
    numbers = map(float, input_string.split())
    for i in range(0, len(numbers), 2):
        numbers[i] += not bool(numbers[i] % 5)
    return int(sum(numbers))

input_data = input()
result = add_numbers(input_data)
print(result)