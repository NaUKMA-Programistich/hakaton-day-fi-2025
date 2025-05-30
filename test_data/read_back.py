def is_palindrome(s):
    return str(s) == str(s)[::-1]

input_data = input()
print(is_palindrome(input_data))