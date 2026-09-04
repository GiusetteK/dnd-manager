"""
Database and storage for saving/loading campaigns and characters
"""
import json
import os
from typing import List, Optional, Dict
from pathlib import Path


class Storage:
    """Handle saving and loading of characters and campaigns."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize storage.
        
        Args:
            data_dir: Directory to store data files
        """
        self.data_dir = Path(data_dir)
        self.characters_dir = self.data_dir / "characters"
        self.campaigns_dir = self.data_dir / "campaigns"
        
        # Create directories if they don't exist
        self.characters_dir.mkdir(parents=True, exist_ok=True)
        self.campaigns_dir.mkdir(parents=True, exist_ok=True)
    
    def save_character(self, character_name: str, character_data: Dict) -> bool:
        """
        Save a character to file.
        
        Args:
            character_name: Name of the character
            character_data: Character data dictionary (from character.get_stats())
        
        Returns:
            True if successful
        """
        try:
            file_path = self.characters_dir / f"{character_name}.json"
            with open(file_path, 'w') as f:
                json.dump(character_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving character: {e}")
            return False
    
    def load_character(self, character_name: str) -> Optional[Dict]:
        """
        Load a character from file.
        
        Args:
            character_name: Name of the character to load
        
        Returns:
            Character data dictionary or None if not found
        """
        try:
            file_path = self.characters_dir / f"{character_name}.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading character: {e}")
            return None
    
    def delete_character(self, character_name: str) -> bool:
        """Delete a character file."""
        try:
            file_path = self.characters_dir / f"{character_name}.json"
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting character: {e}")
            return False
    
    def list_characters(self) -> List[str]:
        """List all saved characters."""
        try:
            files = self.characters_dir.glob("*.json")
            return [f.stem for f in files]
        except Exception as e:
            print(f"Error listing characters: {e}")
            return []
    
    def save_campaign(self, campaign_name: str, campaign_data: Dict) -> bool:
        """
        Save a campaign to file.
        
        Args:
            campaign_name: Name of the campaign
            campaign_data: Campaign data
        
        Returns:
            True if successful
        """
        try:
            file_path = self.campaigns_dir / f"{campaign_name}.json"
            with open(file_path, 'w') as f:
                json.dump(campaign_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving campaign: {e}")
            return False
    
    def load_campaign(self, campaign_name: str) -> Optional[Dict]:
        """
        Load a campaign from file.
        
        Args:
            campaign_name: Name of the campaign to load
        
        Returns:
            Campaign data dictionary or None if not found
        """
        try:
            file_path = self.campaigns_dir / f"{campaign_name}.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading campaign: {e}")
            return None
    
    def delete_campaign(self, campaign_name: str) -> bool:
        """Delete a campaign file."""
        try:
            file_path = self.campaigns_dir / f"{campaign_name}.json"
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting campaign: {e}")
            return False
    
    def list_campaigns(self) -> List[str]:
        """List all saved campaigns."""
        try:
            files = self.campaigns_dir.glob("*.json")
            return [f.stem for f in files]
        except Exception as e:
            print(f"Error listing campaigns: {e}")
            return []
    
    def export_character_to_pdf(self, character_data: Dict, 
                               output_path: str) -> bool:
        """Export character data to PDF (requires reportlab)."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter
            
            # Title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, f"{character_data['name']}")
            
            # Basic info
            c.setFont("Helvetica", 10)
            y = height - 80
            
            c.drawString(50, y, f"Class: {character_data['class']}")
            y -= 20
            c.drawString(50, y, f"Race: {character_data['race']}")
            y -= 20
            c.drawString(50, y, f"Level: {character_data['level']}")
            y -= 20
            c.drawString(50, y, f"HP: {character_data['hit_points']}/{character_data['max_hit_points']}")
            y -= 20
            c.drawString(50, y, f"AC: {character_data['armor_class']}")
            y -= 40
            
            # Abilities
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Abilities")
            y -= 20
            c.setFont("Helvetica", 10)
            
            for ability, score in character_data['abilities'].items():
                modifier = character_data['modifiers'][ability]
                c.drawString(50, y, f"{ability.capitalize()}: {score} ({modifier:+d})")
                y -= 15
            
            c.save()
            return True
        except Exception as e:
            print(f"Error exporting to PDF: {e}")
            return False
