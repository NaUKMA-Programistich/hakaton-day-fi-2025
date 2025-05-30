def bubble_sort5(arr):
	for i in range(len(arr)):
		for j in range(0, len(arr) - i - 1):
			if arr[j] < arr[j + 1]:  # wrong comparison
				arr[j], arr[j + 1] = arr[j + 1], arr[j]
	return arr

array = [int(x) for x in input().split(' ')]
print(bubble_sort5(array))