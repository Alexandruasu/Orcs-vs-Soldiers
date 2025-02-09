from entities import Character

def battle(orcs, soldiers, wizards, screen, screen_width, screen_height):
    for wizard in wizards:
        if wizard.is_alive():
            # Wizards find the nearest Orc and shoot projectiles
            closest_orc = min(
                (orc for orc in orcs if orc.is_alive()),
                key=lambda orc: abs(orc.x - wizard.x) + abs(orc.y - wizard.y),
                default=None,
            )
            if closest_orc:
                wizard.attack(closest_orc)
            wizard.update_projectiles(screen)  # Update and render projectiles

    for orc in orcs:
        if orc.is_alive():
            potential_targets = [unit for unit in soldiers + wizards if unit.is_alive()]

            closest_target = min(
                potential_targets,
                key=lambda target: abs(orc.x - target.x) + abs(orc.y - target.y),
                default=None,
            )

            if closest_target:
                orc.attack(closest_target)
                if not (abs(orc.x - closest_target.x) < 50 and abs(orc.y - closest_target.y) < 50):
                    orc.move_towards(closest_target, screen_width, screen_height)


    for soldier in soldiers:
        if soldier.is_alive():
            closest_orc = min(
                (orc for orc in orcs if orc.is_alive()),
                key=lambda orc: abs(soldier.x - orc.x) + abs(soldier.y - orc.y),
                default=None,
            )
            if closest_orc:
                soldier.attack(closest_orc)
                if not (abs(soldier.x - closest_orc.x) < 50 and abs(soldier.y - closest_orc.y) < 50):
                    soldier.move_towards(closest_orc, screen_width, screen_height)
