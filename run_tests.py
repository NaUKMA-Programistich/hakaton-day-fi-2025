import subprocess

def run_tests(inputs: list[str], outputs: list[str], program_paths: list[str], timeout=5, strip=False):
	results = []
	for path in program_paths:
		program_results = []
		for input_str, expected_output in zip(inputs, outputs):
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
				program_results.append(actual_output == expected_output)
			except Exception:
				program_results.append(False)
		results.append(program_results)
	return results
