"""
Battle Simulator for D&D combat
"""
import random
from typing import List, Dict, Tuple, Optional
from datetime import datetime


class BattleSimulator:
    """Simulates D&D combat encounters."""
    
    def __init__(self):
        """Initialize the battle simulator."""
        self.log: List[str] = []
        self.round = 0
        self.combatants: List[Dict] = []
        self.active = False
    
    def add_combatant(self, name: str, hp: int, ac: int, 
                     initiative_modifier: int, is_player: bool = False) -> None:
        """Add a combatant to the battle."""
        combatant = {
            "name": name,
            "hp": hp,
            "max_hp": hp,
            "ac": ac,
            "initiative_modifier": initiative_modifier,
            "is_player": is_player,
            "initiative": 0,
            "alive": True
        }
        self.combatants.append(combatant)
    
    def roll_initiative(self) -> None:
        """Roll initiative for all combatants."""
        self.log.append("=== INITIATIVE ===")
        
        for combatant in self.combatants:
            roll = random.randint(1, 20)
            combatant["initiative"] = roll + combatant["initiative_modifier"]
            self.log.append(
                f"{combatant['name']} rolls {roll} + {combatant['initiative_modifier']} "
                f"= {combatant['initiative']}"
            )
        
        # Sort by initiative (highest first)
        self.combatants.sort(key=lambda x: x["initiative"], reverse=True)
        self.log.append("")
    
    def roll_attack(self, attacker_bonus: int) -> Tuple[int, int]:
        """Roll attack and return roll and total."""
        roll = random.randint(1, 20)
        total = roll + attacker_bonus
        return roll, total
    
    def roll_damage(self, num_dice: int = 1, dice_size: int = 6, 
                   modifier: int = 0) -> Tuple[List[int], int]:
        """Roll damage and return individual rolls and total."""
        rolls = [random.randint(1, dice_size) for _ in range(num_dice)]
        total = sum(rolls) + modifier
        return rolls, total
    
    def resolve_attack(self, attacker: Dict, defender: Dict, 
                      attack_bonus: int, damage_dice: str = "1d8",
                      damage_bonus: int = 0) -> str:
        """
        Resolve an attack between two combatants.
        
        Args:
            attacker: Attacking combatant
            defender: Defending combatant
            attack_bonus: Bonus to attack roll
            damage_dice: Damage dice (e.g., "2d6")
            damage_bonus: Bonus to damage
        
        Returns:
            Log entry of the attack
        """
        if not defender["alive"]:
            return f"{defender['name']} is already defeated!"
        
        # Parse damage dice
        parts = damage_dice.lower().split('d')
        num_dice = int(parts[0])
        dice_size = int(parts[1])
        
        # Roll attack
        attack_roll, attack_total = self.roll_attack(attack_bonus)
        
        log_entry = f"\n{attacker['name']} attacks {defender['name']}:\n"
        log_entry += f"  Attack roll: {attack_roll} + {attack_bonus} = {attack_total}"
        
        if attack_roll == 1:
            log_entry += " (CRITICAL MISS!)"
            self.log.append(log_entry)
            return log_entry
        
        if attack_total < defender["ac"]:
            log_entry += f" (AC {defender['ac']}) - MISS!"
            self.log.append(log_entry)
            return log_entry
        
        # Hit! Roll damage
        damage_rolls, damage_total = self.roll_damage(num_dice, dice_size, damage_bonus)
        
        if attack_roll == 20:
            log_entry += f" (CRITICAL HIT!) - "
            damage_rolls, damage_total = self.roll_damage(num_dice * 2, dice_size, damage_bonus)
            log_entry += f"HIT! Damage: {damage_rolls} = {damage_total}"
        else:
            log_entry += f" (AC {defender['ac']}) - HIT! "
            log_entry += f"Damage: {damage_rolls} = {damage_total}"
        
        defender["hp"] -= damage_total
        
        if defender["hp"] <= 0:
            defender["alive"] = False
            log_entry += f"\n  {defender['name']} is defeated! (HP: {defender['hp']})"
        else:
            log_entry += f"\n  {defender['name']} HP: {defender['hp']}/{defender['max_hp']}"
        
        self.log.append(log_entry)
        return log_entry
    
    def start_battle(self) -> None:
        """Start the battle."""
        self.active = True
        self.round = 0
        self.roll_initiative()
        self.log.append("BATTLE START!\n")
    
    def next_round(self) -> None:
        """Start the next round."""
        if not self.active:
            return
        
        self.round += 1
        alive_combatants = [c for c in self.combatants if c["alive"]]
        
        if len(alive_combatants) < 2:
            self.end_battle()
            return
        
        self.log.append(f"\n=== ROUND {self.round} ===")
    
    def end_battle(self) -> None:
        """End the battle."""
        self.active = False
        
        alive_combatants = [c for c in self.combatants if c["alive"]]
        
        self.log.append("\n=== BATTLE END ===")
        
        if alive_combatants:
            self.log.append("Survivors:")
            for combatant in alive_combatants:
                self.log.append(
                    f"  {combatant['name']}: {combatant['hp']}/{combatant['max_hp']} HP"
                )
    
    def get_log(self) -> List[str]:
        """Get the battle log."""
        return self.log
    
    def print_log(self) -> None:
        """Print the entire battle log."""
        for entry in self.log:
            print(entry)
    
    def get_combatant_status(self) -> str:
        """Get current status of all combatants."""
        status = "\n=== COMBATANT STATUS ===\n"
        for combatant in self.combatants:
            status_text = "DEFEATED" if not combatant["alive"] else "ALIVE"
            status += (
                f"{combatant['name']}: {combatant['hp']}/{combatant['max_hp']} HP "
                f"({status_text})\n"
            )
        return status
    
    def get_winners(self) -> List[Dict]:
        """Get the winning side."""
        alive = [c for c in self.combatants if c["alive"]]
        
        if not alive:
            return []
        
        # All winners are from the same side (all player or all enemy)
        if all(c["is_player"] for c in alive):
            return [c for c in alive if c["is_player"]]
        else:
            return [c for c in alive if not c["is_player"]]
