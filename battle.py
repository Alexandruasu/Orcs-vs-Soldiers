from entities import Character

def battle(orcs, soldiers, screen_width, screen_height):
    for orc in orcs:
        if orc.is_alive():
            # Find the closest soldier who is still alive
            closest_soldier = min(
                (soldier for soldier in soldiers if soldier.is_alive()),
                key=lambda soldier: abs(soldier.x - orc.x) + abs(soldier.y - orc.y),
                default=None,
            )
            if closest_soldier:
                # Attack the closest soldier
                orc.attack(closest_soldier)
                if not (abs(orc.x - closest_soldier.x) < 50 and abs(orc.y - closest_soldier.y) < 50):
                    # Move towards the closest soldier if not already within range
                    orc.move_towards(closest_soldier, screen_width, screen_height)
                if not closest_soldier.is_alive():
                    # Increase damage if the orc kills an enemy
                    orc.damage = 40

    for soldier in soldiers:
        if soldier.is_alive():
            # Find the closest orc who is still alive
            closest_orc = min(
                (orc for orc in orcs if orc.is_alive()),
                key=lambda orc: abs(orc.x - soldier.x) + abs(orc.y - soldier.y),
                default=None,
            )
            if closest_orc:
                # Attack the closest orc
                soldier.attack(closest_orc)
                if not (abs(soldier.x - closest_orc.x) < 50 and abs(soldier.y - closest_orc.y) < 50):
                    # Move towards the closest orc if not already within range
                    soldier.move_towards(closest_orc, screen_width, screen_height)
                    if not closest_orc.is_alive():
                        # Increase damage if the soldier kills an enemy
                        soldier.damage = 40
