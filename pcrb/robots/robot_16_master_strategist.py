# -*- coding: utf-8 -*-
"""Master Strategist robot logic."""


def robot_logic(robot, game_info, memos):
    """Advanced logic leveraging multiple abilities for high win rate.

    Strategy overview:
    - Periodically scan for up-to-date enemy info.
    - Rest to recover stamina when low.
    - Use camouflage or parry defensively if enemy has higher SP.
    - Attack when adjacent, using ranged attacks when a few tiles away.
    - Set a trap once when close to the enemy.
    - Teleport to close the distance when far away.
    - Otherwise move toward the enemy.
    """
    memos = memos or {}
    last_scan = memos.get("last_scan", -5)
    trap_used = memos.get("trap_used", False)

    turn = game_info.get("turn", 0)
    enemy_pos = game_info.get("enemy_position")
    enemy_sp = game_info.get("enemy_sp")

    # Use scan every 5 turns if available
    if turn - last_scan >= 5 and robot.sp >= robot.scan.cost and not robot.scan.is_active:
        memos["last_scan"] = turn
        return "scan", memos

    # If enemy position unknown, rest or scan
    if enemy_pos is None:
        if robot.sp >= robot.scan.cost:
            memos["last_scan"] = turn
            return "scan", memos
        return "rest", memos

    distance = abs(robot.x - enemy_pos[0]) + abs(robot.y - enemy_pos[1])

    # Rest when stamina is low
    if robot.sp < 15:
        return "rest", memos

    # Camouflage if enemy has higher stamina
    if enemy_sp is not None and enemy_sp > robot.sp and not robot.camouflage.is_active and robot.sp >= robot.camouflage.cost:
        return "camouflage", memos

    # Adjacent enemy handling
    if distance == 1:
        if enemy_sp is not None and enemy_sp > 25 and robot.parry.cooldown_counter == 0 and robot.sp >= robot.parry.cost:
            return "parry", memos
        return "attack", memos

    # Ranged attack when within three tiles
    if distance <= 3 and robot.sp >= robot.ranged_attack.cost:
        return "ranged_attack", memos

    # Set a trap once when close to the enemy
    if distance <= 2 and not trap_used and robot.sp >= robot.trap.cost:
        memos["trap_used"] = True
        if robot.x < enemy_pos[0]:
            return "trap_right", memos
        elif robot.x > enemy_pos[0]:
            return "trap_left", memos
        elif robot.y < enemy_pos[1]:
            return "trap_down", memos
        else:
            return "trap_up", memos

    # Teleport if far away
    if distance >= 5 and robot.sp >= robot.teleport.cost:
        return "teleport", memos

    # Move toward the enemy
    if robot.x < enemy_pos[0]:
        return "right", memos
    elif robot.x > enemy_pos[0]:
        return "left", memos
    elif robot.y < enemy_pos[1]:
        return "down", memos
    else:
        return "up", memos
