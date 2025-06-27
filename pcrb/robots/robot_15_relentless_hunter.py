# -*- coding: utf-8 -*-
"""Relentless Hunter robot logic."""


def robot_logic(robot, game_info, memos):
    """A stronger robot combining scan, teleport and traps."""
    memos = memos or {}
    trap_set = memos.get("trap_set", False)
    last_scan = memos.get("last_scan", 0)

    enemy_pos = game_info.get("enemy_position")
    enemy_sp = game_info.get("enemy_sp")
    turn = game_info.get("turn", 0)

    # Use scan every 5 turns to keep enemy info updated
    if turn - last_scan >= 5 and robot.sp >= robot.scan.cost and not robot.scan.is_active:
        memos["last_scan"] = turn
        return "scan", memos

    # If we cannot see the enemy, rest to recover
    if enemy_pos is None:
        return "rest", memos

    distance = abs(robot.x - enemy_pos[0]) + abs(robot.y - enemy_pos[1])

    # Rest when stamina is low
    if robot.sp < 15:
        return "rest", memos

    # Camouflage if enemy has higher SP and we have enough
    if enemy_sp is not None and enemy_sp > robot.sp and not robot.camouflage.is_active and robot.sp >= robot.camouflage.cost:
        return "camouflage", memos

    # Attack if adjacent
    if distance == 1:
        # Use parry if enemy has high SP
        if enemy_sp is not None and enemy_sp >= 30 and robot.parry.cooldown_counter == 0 and robot.sp >= robot.parry.cost:
            return "parry", memos
        return "attack", memos

    # Ranged attack when at distance 2
    if distance == 2 and robot.sp >= robot.ranged_attack.cost:
        return "ranged_attack", memos

    # Set a trap once when near enemy
    if distance <= 2 and not trap_set and robot.sp >= robot.trap.cost:
        if robot.x < enemy_pos[0]:
            memos["trap_set"] = True
            return "trap_right", memos
        elif robot.x > enemy_pos[0]:
            memos["trap_set"] = True
            return "trap_left", memos
        elif robot.y < enemy_pos[1]:
            memos["trap_set"] = True
            return "trap_down", memos
        else:
            memos["trap_set"] = True
            return "trap_up", memos

    # Teleport when the enemy is far away
    if distance > 4 and robot.sp >= robot.teleport.cost:
        return "teleport", memos

    # Move towards the enemy
    if robot.x < enemy_pos[0]:
        return "right", memos
    elif robot.x > enemy_pos[0]:
        return "left", memos
    elif robot.y < enemy_pos[1]:
        return "down", memos
    else:
        return "up", memos
