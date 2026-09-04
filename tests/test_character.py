"""Tests for Character class"""
import pytest
from dnd_manager.characters import Character


def test_character_creation():
    """Test creating a character"""
    character = Character(
        name="Legolas",
        char_class="Ranger",
        race="Elf",
        level=5
    )
    
    assert character.name == "Legolas"
    assert character.char_class == "Ranger"
    assert character.race == "Elf"
    assert character.level == 5


def test_character_modifiers():
    """Test ability score modifiers"""
    character = Character(
        name="Test",
        char_class="Fighter",
        strength=16,
        dexterity=10
    )
    
    assert character.get_modifier("strength") == 3
    assert character.get_modifier("dexterity") == 0


def test_add_skill():
    """Test adding a skill"""
    character = Character(
        name="Test",
        char_class="Rogue"
    )
    
    character.add_skill("Stealth", 15)
    assert "Stealth" in character.skills
    assert character.skills["Stealth"] == 15


def test_inventory():
    """Test inventory management"""
    character = Character(
        name="Test",
        char_class="Fighter"
    )
    
    character.add_item("Sword", 1)
    character.add_item("Gold", 50)
    
    assert character.inventory["Sword"] == 1
    assert character.inventory["Gold"] == 50
    
    character.remove_item("Gold", 10)
    assert character.inventory["Gold"] == 40


def test_damage_and_healing():
    """Test damage and healing"""
    character = Character(
        name="Test",
        char_class="Fighter",
        constitution=16
    )
    
    max_hp = character.hit_points
    character.take_damage(5)
    assert character.hit_points == max_hp - 5
    
    character.heal(3)
    assert character.hit_points == max_hp - 2


def test_level_up():
    """Test leveling up"""
    character = Character(
        name="Test",
        char_class="Wizard",
        level=1
    )
    
    initial_hp = character.hit_points
    character.level_up()
    
    assert character.level == 2
    assert character.hit_points >= initial_hp
