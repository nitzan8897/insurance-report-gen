# src/data/file_persistence.py
"""
File-based persistence handler for saving/loading data by claim number.
Each claim gets its own JSON file in saved_data/ directory.
"""
import json
import os
from pathlib import Path


class FilePersistenceHandler:
    """Handles saving and loading data files organized by claim number."""

    def __init__(self, base_dir='saved_data'):
        """
        Initialize file persistence handler.

        Args:
            base_dir: Directory to store claim data files
        """
        self.base_dir = Path(base_dir)
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Create the saved_data directory if it doesn't exist."""
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_by_claim_number(self, claim_number, data):
        """
        Save data to a file named by claim number.

        Args:
            claim_number: Claim number to use as filename
            data: Dictionary of data to save

        Returns:
            Path: Path to saved file
        """
        if not claim_number:
            raise ValueError("Claim number cannot be empty")

        # Sanitize claim number for filename
        safe_filename = self._sanitize_filename(claim_number)
        file_path = self.base_dir / f"{safe_filename}.json"

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return file_path

    def load_by_claim_number(self, claim_number):
        """
        Load data from a file by claim number.

        Args:
            claim_number: Claim number to load

        Returns:
            dict: Loaded data or None if file doesn't exist
        """
        if not claim_number:
            return None

        safe_filename = self._sanitize_filename(claim_number)
        file_path = self.base_dir / f"{safe_filename}.json"

        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None

    def get_all_claim_numbers(self):
        """
        Get list of all claim numbers that have saved data.

        Returns:
            list: Sorted list of claim numbers
        """
        claim_numbers = []

        for file_path in self.base_dir.glob('*.json'):
            # Remove .json extension to get claim number
            claim_number = file_path.stem
            claim_numbers.append(claim_number)

        return sorted(claim_numbers)

    def delete_by_claim_number(self, claim_number):
        """
        Delete saved data for a claim number.

        Args:
            claim_number: Claim number to delete

        Returns:
            bool: True if deleted, False if didn't exist
        """
        if not claim_number:
            return False

        safe_filename = self._sanitize_filename(claim_number)
        file_path = self.base_dir / f"{safe_filename}.json"

        if file_path.exists():
            file_path.unlink()
            return True

        return False

    def _sanitize_filename(self, claim_number):
        """
        Sanitize claim number for use as filename.

        Args:
            claim_number: Claim number string

        Returns:
            str: Safe filename
        """
        # Replace characters that aren't safe for filenames
        safe = str(claim_number).replace('/', '_').replace('\\', '_')
        safe = safe.replace(':', '_').replace('*', '_')
        safe = safe.replace('?', '_').replace('"', '_')
        safe = safe.replace('<', '_').replace('>', '_')
        safe = safe.replace('|', '_')

        return safe

    def file_exists(self, claim_number):
        """
        Check if a file exists for the given claim number.

        Args:
            claim_number: Claim number to check

        Returns:
            bool: True if file exists
        """
        if not claim_number:
            return False

        safe_filename = self._sanitize_filename(claim_number)
        file_path = self.base_dir / f"{safe_filename}.json"

        return file_path.exists()
