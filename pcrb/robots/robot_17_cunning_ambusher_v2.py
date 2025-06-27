# -*- coding: utf-8 -*-
"""Enhanced Cunning Ambusher robot."""


def robot_logic(robot, game_info, memos):
    """Improved ambush strategy using trap, camouflage and teleport.

    The robot attempts to stay hidden, set a trap near the enemy once and
    lure the opponent onto it. Teleports when the enemy is far away to
    reposition faster. It rests when stamina is low and attacks when
    adjacent.
    """
    memos = memos or {}
    trap_mode = memos.get("trap_mode", False)
    trap_used = memos.get("trap_used", False)

    enemy_pos = game_info.get("enemy_position")
    turn = game_info.get("turn", 0)

    # If enemy position unknown, try scanning if possible
    if enemy_pos is None:
        if robot.sp >= robot.scan.cost and not robot.scan.is_active:
            return "scan", memos
        return "rest", memos

    distance = abs(robot.x - enemy_pos[0]) + abs(robot.y - enemy_pos[1])

    # Rest when stamina is low
    if robot.sp < 15:
        return "rest", memos

    # Use camouflage if not active
    if not robot.camouflage.is_active and robot.sp >= robot.camouflage.cost:
        return "camouflage", memos

    # Attack when adjacent
    if distance == 1:
        return "attack", {"trap_mode": False, "trap_used": trap_used}

    # Place a trap once when near the enemy
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

    # After placing a trap try to lure the enemy onto it
    if trap_used and not trap_mode:
        memos["trap_mode"] = True
        trap_mode = True

    if trap_mode:
        if robot.x < enemy_pos[0] and robot.x > 0:
            return "left", memos
        elif robot.x > enemy_pos[0] and robot.x < robot.controller.x_max - 1:
            return "right", memos
        elif robot.y < enemy_pos[1] and robot.y > 0:
            return "up", memos
        elif robot.y > enemy_pos[1] and robot.y < robot.controller.y_max - 1:
            return "down", memos

    # Teleport when the enemy is far away
    if distance >= 5 and robot.sp >= robot.teleport.cost:
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
