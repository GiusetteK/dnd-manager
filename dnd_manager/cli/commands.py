"""
CLI commands for D&D Manager
"""
import click
import json
from dnd_manager.characters import Character, CharacterGenerator
from dnd_manager.campaigns import Campaign
from dnd_manager.battle import BattleSimulator
from dnd_manager.database import Storage


storage = Storage()


@click.group()
def main():
    """D&D Manager - Manage your D&D campaigns and characters"""
    pass


# Character Commands
@main.group()
def character():
    """Manage characters"""
    pass


@character.command()
@click.option('--name', prompt='Character name', help='Name of the character')
@click.option('--class', 'char_class', type=click.Choice(Character.CLASSES),
              prompt='Choose a class', help='Character class')
@click.option('--race', type=click.Choice(Character.RACES), default='Human',
              help='Character race')
@click.option('--level', type=int, default=1, help='Starting level')
def create(name, char_class, race, level):
    """Create a new character"""
    character = Character(
        name=name,
        char_class=char_class,
        race=race,
        level=level
    )
    
    # Save character
    character_data = character.get_stats()
    if storage.save_character(name, character_data):
        click.echo(f"✓ Character '{name}' created successfully!")
        click.echo(str(character))
    else:
        click.echo("✗ Error creating character")


@character.command()
def list():
    """List all characters"""
    characters = storage.list_characters()
    if not characters:
        click.echo("No characters found.")
        return
    
    click.echo("Characters:")
    for char_name in characters:
        data = storage.load_character(char_name)
        if data:
            click.echo(f"  - {char_name} (Level {data['level']} {data['class']})")


@character.command()
@click.option('--name', prompt='Character name', help='Name of the character')
def view(name):
    """View character details"""
    data = storage.load_character(name)
    if not data:
        click.echo(f"Character '{name}' not found.")
        return
    
    click.echo(json.dumps(data, indent=2))


@character.command()
@click.option('--name', prompt='Character name to generate')
def generate(name):
    """Generate a random character"""
    character = CharacterGenerator.generate(name=name)
    character_data = character.get_stats()
    
    if storage.save_character(name, character_data):
        click.echo(f"✓ Character '{name}' generated successfully!")
        click.echo(str(character))
    else:
        click.echo("✗ Error generating character")


# Campaign Commands
@main.group()
def campaign():
    """Manage campaigns"""
    pass


@campaign.command()
@click.option('--name', prompt='Campaign name', help='Name of the campaign')
@click.option('--gm', prompt='Game Master name', help='Game Master name')
@click.option('--setting', default='Forgotten Realms', help='Campaign setting')
def create_campaign(name, gm, setting):
    """Create a new campaign"""
    campaign = Campaign(
        name=name,
        game_master=gm,
        setting=setting
    )
    
    campaign_data = {
        "name": campaign.name,
        "game_master": campaign.game_master,
        "setting": campaign.setting,
        "description": campaign.description,
        "status": campaign.status,
        "party_level": campaign.party_level,
        "characters": campaign.characters,
        "npcs": campaign.npcs,
        "locations": campaign.locations,
        "quests": campaign.quests,
        "sessions": campaign.sessions,
        "created_at": campaign.created_at.isoformat()
    }
    
    if storage.save_campaign(name, campaign_data):
        click.echo(f"✓ Campaign '{name}' created successfully!")
        click.echo(str(campaign))
    else:
        click.echo("✗ Error creating campaign")


@campaign.command()
def list():
    """List all campaigns"""
    campaigns = storage.list_campaigns()
    if not campaigns:
        click.echo("No campaigns found.")
        return
    
    click.echo("Campaigns:")
    for campaign_name in campaigns:
        data = storage.load_campaign(campaign_name)
        if data:
            click.echo(f"  - {campaign_name} (GM: {data['game_master']}, "
                      f"Level: {data['party_level']}, Sessions: {len(data['sessions'])})")


@campaign.command()
@click.option('--name', prompt='Campaign name', help='Name of the campaign')
def view_campaign(name):
    """View campaign details"""
    data = storage.load_campaign(name)
    if not data:
        click.echo(f"Campaign '{name}' not found.")
        return
    
    click.echo(json.dumps(data, indent=2))


# Battle Commands
@main.group()
def battle():
    """Simulate battles"""
    pass


@battle.command()
def simulate():
    """Simulate a battle between two fighters"""
    click.echo("=== BATTLE SIMULATOR ===\n")
    
    simulator = BattleSimulator()
    
    # Add some test combatants
    simulator.add_combatant("Player Hero", hp=30, ac=15, 
                           initiative_modifier=2, is_player=True)
    simulator.add_combatant("Goblin Archer", hp=7, ac=12, 
                           initiative_modifier=1, is_player=False)
    simulator.add_combatant("Goblin Fighter", hp=10, ac=13, 
                           initiative_modifier=0, is_player=False)
    
    # Start battle
    simulator.start_battle()
    
    # Simple automated rounds
    for _ in range(5):
        if not simulator.active:
            break
        
        simulator.next_round()
        
        # Simulate some attacks
        for combatant in simulator.combatants:
            if combatant["alive"] and combatant["is_player"]:
                # Attack first living enemy
                for enemy in simulator.combatants:
                    if enemy["alive"] and not enemy["is_player"]:
                        simulator.resolve_attack(
                            combatant, enemy,
                            attack_bonus=5,
                            damage_dice="1d8",
                            damage_bonus=2
                        )
                        break
    
    # Print results
    simulator.print_log()


if __name__ == '__main__':
    main()
