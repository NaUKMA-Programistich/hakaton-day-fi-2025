def bubble_sort4(arr):
	n = len(arr)
	swapped = True
	while swapped:
		swapped = False
		for i in range(n - 1):
			if arr[i] > arr[i + 1]:
				arr[i], arr[i + 1] = arr[i + 1], arr[i]
				swapped = True
		n -= 1
	return arr

array = [int(x) for x in input().split(' ')]
print(bubble_sort4(array))