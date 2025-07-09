import csv
import re
from typing import List, Dict, Optional, TextIO
from pymed import PubMed
from datetime import datetime
import logging

class PubMedFetcher:
    """A class to fetch and process PubMed papers based on a query."""
    
    def __init__(self, email: str, debug: bool = False):
        """Initialize the PubMed fetcher with an email for API access.
        
        Args:
            email: Email address for PubMed API.
            debug: Enable debug logging if True.
        """
        self.pubmed = PubMed(tool="PubMedFetcher", email=email)
        self.debug = debug
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def is_company_affiliation(self, affiliation: str) -> bool:
        """Check if an affiliation is likely a pharmaceutical or biotech company.
        
        Args:
            affiliation: Affiliation string to check.
            
        Returns:
            bool: True if the affiliation is a company, False otherwise.
        """
        if not affiliation:
            return False
        # Heuristic: Companies often don't include academic keywords
        academic_keywords = [
            "university", "college", "institute", "laboratory", "lab", "school", "academic"
        ]
        company_keywords = [
            "pharma", "biotech", "laboratories", "inc.", "ltd.", "corporation", "llc", "company"
        ]
        affiliation_lower = affiliation.lower()
        has_academic = any(keyword in affiliation_lower for keyword in academic_keywords)
        has_company = any(keyword in affiliation_lower for keyword in company_keywords)
        return has_company or not has_academic

    def fetch_papers(self, query: str, max_results: int = 100) -> List[Dict]:
        """Fetch papers from PubMed based on a query.
        
        Args:
            query: PubMed query string.
            max_results: Maximum number of papers to fetch.
            
        Returns:
            List of dictionaries containing paper details.
        """
        try:
            results = self.pubmed.query(query, max_results=max_results)
            papers = []
            for article in results:
                paper_data = self.process_article(article)
                if paper_data:
                    papers.append(paper_data)
            return papers
        except Exception as e:
            self.logger.error(f"Error fetching papers: {e}")
            return []

    def process_article(self, article: dict) -> Optional[Dict]:
        """Process a single PubMed article to extract required fields.
        
        Args:
            article: PubMed article object.
            
        Returns:
            Dictionary with paper details or None if no company-affiliated authors.
        """
        try:
            authors = article.authors
            non_academic_authors = []
            company_affiliations = []
            corresponding_email = None

            for author in authors:
                affiliation = author.get("affiliation", "")
                if self.is_company_affiliation(affiliation):
                    name = f"{author.get('lastname', '')}, {author.get('firstname', '')}".strip(", ")
                    non_academic_authors.append(name)
                    company_affiliations.append(affiliation)
                    # Heuristic: First author with affiliation might be corresponding
                    if not corresponding_email and "email" in affiliation.lower():
                        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', affiliation)
                        if email_match:
                            corresponding_email = email_match.group(0)

            if not non_academic_authors:
                return None

            pub_date = article.publication_date
            if isinstance(pub_date, datetime):
                pub_date = pub_date.strftime("%Y-%m-%d")
            else:
                pub_date = str(pub_date)

            return {
                "PubmedID": article.pubmed_id.split("\n")[0],
                "Title": article.title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email or "N/A"
            }
        except Exception as e:
            self.logger.debug(f"Error processing article {article.pubmed_id}: {e}")
            return None

    def save_to_csv(self, papers: List[Dict], output: TextIO) -> None:
        """Save papers to a CSV file or stream.
        
        Args:
            papers: List of paper dictionaries.
            output: File-like object to write CSV data.
        """
        if not papers:
            self.logger.warning("No papers to save.")
            return

        fieldnames = [
            "PubmedID", "Title", "Publication Date", 
            "Non-academic Author(s)", "Company Affiliation(s)", 
            "Corresponding Author Email"
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for paper in papers:
            writer.writerow(paper)