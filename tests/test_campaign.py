"""Tests for Campaign class"""
import pytest
from dnd_manager.campaigns import Campaign


def test_campaign_creation():
    """Test creating a campaign"""
    campaign = Campaign(
        name="Lost Mines",
        game_master="Mike",
        setting="Forgotten Realms"
    )
    
    assert campaign.name == "Lost Mines"
    assert campaign.game_master == "Mike"
    assert campaign.setting == "Forgotten Realms"


def test_add_character():
    """Test adding characters to campaign"""
    campaign = Campaign(
        name="Test",
        game_master="GM"
    )
    
    campaign.add_character("Aragorn")
    campaign.add_character("Legolas")
    
    assert len(campaign.characters) == 2
    assert "Aragorn" in campaign.characters


def test_add_npc():
    """Test adding NPCs"""
    campaign = Campaign(
        name="Test",
        game_master="GM"
    )
    
    campaign.add_npc("Gandalf", "Wizard", "Guide")
    
    assert "Gandalf" in campaign.npcs


def test_quests():
    """Test quest management"""
    campaign = Campaign(
        name="Test",
        game_master="GM"
    )
    
    campaign.add_quest("Save the village", "Protect villagers", "Elder", "100 GP")
    
    assert len(campaign.quests) == 1
    assert campaign.quests[0]["name"] == "Save the village"
