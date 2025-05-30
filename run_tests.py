import subprocess

def run_one_test(input, output, program_path, timeout=5, strip=False):
	try:
		proc = subprocess.run(
			["python", path],
			input=input_str,
			capture_output=True,
			timeout=timeout,
			text=True
		)
		actual_output = proc.stdout
		if strip:
			actual_output = actual_output.strip()
			expected_output = expected_output.strip()
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
