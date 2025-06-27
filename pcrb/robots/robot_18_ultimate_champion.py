# -*- coding: utf-8 -*-
"""Ultimate Champion robot logic."""


def robot_logic(robot, game_info, memos):
    """Highly adaptive strategy aiming to win against any opponent.

    Features:
    - Periodic scanning for enemy location.
    - Resting when stamina is low.
    - Defensive camouflage or parry when enemy has higher SP.
    - Attacks or ranged attacks depending on distance.
    - Sets a trap once when near the enemy.
    - Teleports when far away to close the distance.
    - Otherwise moves toward the enemy.
    """
    memos = memos or {}
    last_scan = memos.get("last_scan", -5)
    trap_used = memos.get("trap_used", False)

    turn = game_info.get("turn", 0)
    enemy_pos = game_info.get("enemy_position")
    enemy_sp = game_info.get("enemy_sp")

    # Use scan every 5 turns if possible
    if turn - last_scan >= 5 and robot.sp >= robot.scan.cost and not robot.scan.is_active:
        memos["last_scan"] = turn
        return "scan", memos

    # If enemy is hidden, try scanning or rest
    if enemy_pos is None:
        if robot.sp >= robot.scan.cost and not robot.scan.is_active:
            memos["last_scan"] = turn
            return "scan", memos
        return "rest", memos

    distance = abs(robot.x - enemy_pos[0]) + abs(robot.y - enemy_pos[1])

    # Rest when stamina is low
    if robot.sp < 15:
        return "rest", memos

    # Activate camouflage if enemy has more SP
    if enemy_sp is not None and enemy_sp > robot.sp and not robot.camouflage.is_active and robot.sp >= robot.camouflage.cost:
        return "camouflage", memos

    # Adjacent enemy handling
    if distance == 1:
        if enemy_sp is not None and enemy_sp >= 30 and robot.parry.cooldown_counter == 0 and robot.sp >= robot.parry.cost:
            return "parry", memos
        return "attack", memos

    # Ranged attack when two tiles away
    if distance == 2 and robot.sp >= robot.ranged_attack.cost:
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
