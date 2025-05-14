import requests
import wikipedia
from bs4 import BeautifulSoup
import streamlit as st
from typing import Dict, Optional, Tuple
import re

class TextRetriever:
    """Retrieves text content from external sources like Wikipedia and Google Books."""
    
    def __init__(self):
        """Initialize the text retriever."""
        self.cache = {}
        # Set Wikipedia language to English
        wikipedia.set_lang("en")
    
    def _clean_title(self, title: str) -> str:
        """Clean the title for better search results.
        
        Args:
            title: The title to clean
            
        Returns:
            str: Cleaned title
        """
        # Remove common prefixes/suffixes
        title = re.sub(r'^(the|a|an)\s+', '', title.lower())
        # Remove special characters
        title = re.sub(r'[^\w\s]', '', title)
        return title.strip()
    
    def search_wikipedia(self, query: str, max_results: int = 3) -> Tuple[str, Dict]:
        """Search Wikipedia for relevant information.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Tuple of (text content, metadata)
        """
        try:
            # Clean the query
            clean_query = self._clean_title(query)
            
            # Try direct page lookup first
            try:
                page = wikipedia.page(clean_query)
                content = page.content
                metadata = {
                    "source": "wikipedia",
                    "title": page.title,
                    "url": page.url,
                    "summary": page.summary
                }
                return content, metadata
            except wikipedia.exceptions.PageError:
                pass
            
            # If direct lookup fails, try search
            search_results = wikipedia.search(clean_query, results=max_results)
            if not search_results:
                # Try with "novel" suffix
                search_results = wikipedia.search(f"{clean_query} novel", results=max_results)
                if not search_results:
                    return "", {"source": "wikipedia", "error": "No results found"}
            
            # Get the first result
            try:
                page = wikipedia.page(search_results[0])
                content = page.content
                
                # Create metadata
                metadata = {
                    "source": "wikipedia",
                    "title": page.title,
                    "url": page.url,
                    "summary": page.summary
                }
                
                return content, metadata
            except wikipedia.exceptions.DisambiguationError as e:
                # If disambiguation page, try the first option
                try:
                    page = wikipedia.page(e.options[0])
                    content = page.content
                    metadata = {
                        "source": "wikipedia",
                        "title": page.title,
                        "url": page.url,
                        "summary": page.summary
                    }
                    return content, metadata
                except Exception:
                    return "", {"source": "wikipedia", "error": "Could not resolve disambiguation"}
            
        except Exception as e:
            st.error(f"Wikipedia error: {str(e)}")
            return "", {"source": "wikipedia", "error": str(e)}
    
    def search_google_books(self, query: str, api_key: str) -> Tuple[str, Dict]:
        """Search Google Books API for book content.
        
        Args:
            query: Search query
            api_key: Google Books API key
            
        Returns:
            Tuple of (text content, metadata)
        """
        try:
            # Clean the query
            clean_query = self._clean_title(query)
            
            # Search Google Books
            base_url = "https://www.googleapis.com/books/v1/volumes"
            params = {
                "q": f"{clean_query} novel",  # Add 'novel' to improve results
                "key": api_key,
                "maxResults": 1
            }
            
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get("items"):
                return "", {"source": "google_books", "error": "No results found"}
            
            # Get the first result
            book = data["items"][0]["volumeInfo"]
            
            # Get book details
            title = book.get("title", "")
            authors = book.get("authors", [])
            description = book.get("description", "")
            preview_url = book.get("previewLink", "")
            
            # Create metadata
            metadata = {
                "source": "google_books",
                "title": title,
                "authors": authors,
                "description": description,
                "preview_url": preview_url
            }
            
            # Combine available text content
            content = f"Title: {title}\n"
            if authors:
                content += f"Authors: {', '.join(authors)}\n"
            if description:
                content += f"\nDescription:\n{description}\n"
            
            return content, metadata
            
        except Exception as e:
            st.error(f"Google Books error: {str(e)}")
            return "", {"source": "google_books", "error": str(e)}
    
    def get_text(self, query: str, google_books_api_key: Optional[str] = None) -> Tuple[str, Dict]:
        """Get text content from available sources.
        
        Args:
            query: Search query
            google_books_api_key: Optional Google Books API key
            
        Returns:
            Tuple of (text content, metadata)
        """
        # Try Wikipedia first
        wiki_content, wiki_metadata = self.search_wikipedia(query)
        
        # If Google Books API key is provided, try that too
        if google_books_api_key:
            books_content, books_metadata = self.search_google_books(query, google_books_api_key)
            
            # Combine content and metadata
            if wiki_content and books_content:
                combined_content = f"{wiki_content}\n\n---\n\n{books_content}"
                combined_metadata = {
                    "sources": ["wikipedia", "google_books"],
                    "wikipedia": wiki_metadata,
                    "google_books": books_metadata
                }
            elif wiki_content:
                combined_content = wiki_content
                combined_metadata = {
                    "sources": ["wikipedia"],
                    "wikipedia": wiki_metadata
                }
            elif books_content:
                combined_content = books_content
                combined_metadata = {
                    "sources": ["google_books"],
                    "google_books": books_metadata
                }
            else:
                return "", {"sources": [], "error": "No content found from any source"}
            
            return combined_content, combined_metadata
        
        if wiki_content:
            return wiki_content, {"sources": ["wikipedia"], "wikipedia": wiki_metadata}
        
        return "", {"sources": [], "error": "No content found from any source"} 