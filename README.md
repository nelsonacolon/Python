<b>LLM Simulation – Country & Capital Lookup</b>

This project is a ightweight LLM-inspired simulation tool that demonstrates how large language models (LLMs) could interact with structured data.  
It allows users (or AI agents) to look up the capital city of any country using a dataframe loaded from a CSV input file.

Designed with robust error handling, graceful fallbacks, and clean modular structure, this script can be used as:
- A standalone CLI utility,
- A backend component for LLM agents or chatbots,
- Or a template for data lookup workflows in AI-assisted systems.

<b>Features</b>

- CSV-backed lookupfor country–capital pairs  
- Robust normalization – case-insensitive, whitespace-tolerant matching  
- LLM-style response handler (`print_llm_response`) with graceful fallback  
- Modular functions (`load_countries`, `find_capital`) for reusability  
- Defensive design – handles missing CSVs, bad inputs, or missing dependencies  
- Ready for AI agent integration – can be plugged into a chain or workflow  
