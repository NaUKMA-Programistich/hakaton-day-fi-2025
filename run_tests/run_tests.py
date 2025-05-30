import subprocess, os
os.chdir(os.path.dirname(__file__))


def run_one_test(input_str, expected_output, program_path, timeout=5, strip=False):
	try:
		proc = subprocess.run(
			["python", program_path],
			input=input_str,
			capture_output=True,
			timeout=timeout,
			text=True
		)
		actual_output = proc.stdout
		if strip:
			actual_output = actual_output.strip()
			expected_output = expected_output.strip()
		# print(program_path)
		# print(input_str)
		# print(actual_output)
		# print(expected_output)
		# print()
		return actual_output == expected_output
	except Exception:
		return False


def run_tests(inputs: list[str], outputs: list[str], program_paths: list[str], timeout=5, strip=False):
	results = []
	for path in program_paths:
		program_results = []
		for input_str, expected_output in zip(inputs, outputs):
			program_results.append(run_one_test(input_str, expected_output, path, timeout, strip))
		results.append(program_results)
	return results


if __name__ == "__main__":
	inputs = [
		"1 3 2",
		"5 4 3 2 1",
		"",
		"7",
		"3 3 3",
		"9 -1 0 9",
		"2 1 2 1",
		"1 2 3 4 5 6 7 8 9 10",
	]

	outputs = [
		"[1, 2, 3]\n",
		"[1, 2, 3, 4, 5]\n",
		"",
		"[7]\n",
		"[3, 3, 3]\n",
		"[-1, 0, 9, 9]\n",
		"[1, 1, 2, 2]\n",
		"[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n",
	]

	programs = ["programs/sort1.py", "programs/sort2.py", "programs/sort3.py", "programs/sort4.py", "programs/sort5.py"]
	for res in run_tests(inputs, outputs, programs): print(res)