import sys
import argparse
from pubmed_fetcher.fetcher import PubMedFetcher

def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers with non-academic authors."
    )
    parser.add_argument("query", help="PubMed search query")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", help="Output CSV filename")
    args = parser.parse_args()

    fetcher = PubMedFetcher(email="user@example.com", debug=args.debug)

    papers = fetcher.fetch_papers(args.query)

    if args.file:
        try:
            with open(args.file, "w", newline="") as f:
                fetcher.save_to_csv(papers, f)
        except Exception as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        fetcher.save_to_csv(papers, sys.stdout)

if __name__ == "__main__":
    main()