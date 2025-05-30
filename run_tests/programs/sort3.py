def bubble_sort3(arr):
	for i in range(len(arr)):
		for j in range(0, len(arr) - i - 2):  # off by one
			if arr[j] > arr[j + 1]:
				arr[j], arr[j + 1] = arr[j + 1], arr[j]
	return arr

array = [int(x) for x in input().split(' ')]
print(bubble_sort3(array))