import pandas as pd

try:
	from helper_functions import print_llm_response
	_PRINT_SOURCE = 'helper_functions'
except Exception:
	# Fallback shim if helper_functions doesn't provide print_llm_response
	_PRINT_SOURCE = 'local_shim'

	def print_llm_response(resp):
		"""Fallback simple printer for LLM responses when helper_functions lacks it."""
		if isinstance(resp, dict):
			# simple formatted print for dict-like responses
			for k, v in resp.items():
				print(f"{k}: {v}")
		else:
			print(resp)

print(f"Using print_llm_response from: {_PRINT_SOURCE}")

# CSV-backed country -> capital lookup utilities
try:
	import pandas as pd
except Exception:
	pd = None


def load_countries(csv_path: str):
	"""Load countries and capitals from a CSV into a normalized DataFrame.

	Returns a DataFrame with lowercase 'country_norm' and original 'Capital' column.
	Raises FileNotFoundError if the CSV isn't present.
	"""
	if pd is None:
		raise RuntimeError("pandas is required to load the CSV. Install dependencies (requirements.txt).")

	df = pd.read_csv(csv_path)

	# Find the likely column names for country and capital (be tolerant)
	cols = [c.strip() for c in df.columns]
	# expected headers seen in the CSV: 'Country' and 'Capital City' or 'Capital'
	country_col = None
	capital_col = None
	for c in cols:
		cl = c.lower()
		if 'country' in cl:
			country_col = c
		if 'capital' in cl:
			capital_col = c

	if country_col is None or capital_col is None:
		# fallback to first two columns
		country_col = cols[0]
		capital_col = cols[1] if len(cols) > 1 else cols[0]

	# Normalization: create a casefolded, stripped version of country for robust matching
	df = df.rename(columns={country_col: 'country', capital_col: 'capital'})
	df['country_norm'] = df['country'].astype(str).str.strip().str.casefold()
	df['capital'] = df['capital'].astype(str).str.strip()

	return df


def find_capital(country_name: str, df):
	"""Return the capital for a given country name using the provided DataFrame.

	Matching is case-insensitive and trims whitespace. Returns None if not found.
	"""
	if country_name is None:
		return None
	key = country_name.strip().casefold()
	matches = df.loc[df['country_norm'] == key]
	if not matches.empty:
		# return the first match's capital
		return matches.iloc[0]['capital']

	# Try more permissive matching: substring match
	contains = df.loc[df['country_norm'].str.contains(key, na=False)]
	if not contains.empty:
		return contains.iloc[0]['capital']

	return None


def main():
	import os
	csv_path = os.path.join(os.path.dirname(__file__), 'countries_capitals.csv')
	try:
		df = load_countries(csv_path)
	except FileNotFoundError:
		print_llm_response({'error': f"CSV file not found at: {csv_path}"})
		return
	except Exception as e:
		print_llm_response({'error': str(e)})
		return

	country = input("Enter a country name to get its capital: ").strip()
	capital = find_capital(country, df)
	if capital:
		print_llm_response({'answer': capital})
	else:
		print_llm_response({'answer': f"Capital not found for '{country}'."})


if __name__ == '__main__':
	main()


