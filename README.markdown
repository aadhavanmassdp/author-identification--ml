# PubMed Fetcher

A Python program to fetch research papers from PubMed with at least one author affiliated with a pharmaceutical or biotech company, outputting results as a CSV file.

## Features
- Fetches papers using the PubMed API via the `pymed` library.
- Filters papers for non-academic authors based on affiliation heuristics.
- Outputs results to a CSV file or console with columns: PubmedID, Title, Publication Date, Non-academic Author(s), Company Affiliation(s), Corresponding Author Email.
- Supports command-line arguments for query, debug mode, and output file.

## Installation

1. **Prerequisites**:
   - Python 3.8 or higher
   - Git
   - Poetry (`pip install poetry`)

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/pubmed-fetcher.git
   cd pubmed-fetcher
   ```

3. **Install Dependencies**:
   ```bash
   poetry install
   ```

4. **Activate the Virtual Environment**:
   ```bash
   poetry shell
   ```

## Usage

Run the program using the `get-papers-list` command:

```bash
get-papers-list "cancer treatment" [-d] [-f output.csv]
```

### Options
- `query`: PubMed search query (required).
- `-h, --help`: Show help message.
- `-d, --debug`: Enable debug logging.
- `-f, --file`: Specify output CSV filename (default: console output).

## Example
```bash
get-papers-list "cancer treatment" -f results.csv
```

## Code Organization
- `pubmed_fetcher/fetcher.py`: Core module for fetching and processing PubMed papers.
- `scripts/get_papers_list.py`: Command-line interface script.
- `pyproject.toml`: Poetry configuration for dependencies and script entry point.

## Tools Used
- **pymed**: Python library for PubMed API access (https://pymed.readthedocs.io).
- **Poetry**: Dependency management and packaging (https://python-poetry.org).
- **Git**: Version control system.
- **Grok**: Assisted in code generation and debugging (https://x.ai/grok).

## Publishing to TestPyPI (Bonus)
To publish the module to TestPyPI:
1. Update `pyproject.toml` with TestPyPI repository details.
2. Run:
   ```bash
   poetry config repositories.test-pypi https://test.pypi.org/legacy/
   poetry publish --build -r test-pypi
   ```
Note: Requires a TestPyPI account and API token.

## Notes
- Replace `user@example.com` in `fetcher.py` with a valid email for PubMed API access.
- The program uses heuristics to identify company affiliations (e.g., keywords like "pharma", "biotech", absence of academic terms).
- Error handling ensures robustness against API failures and missing data.