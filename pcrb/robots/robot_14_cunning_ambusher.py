# -*- coding: utf-8 -*-
"""Cunning ambusher robot logic."""

def robot_logic(robot, game_info, memos):
    """Ambush oriented logic using traps and camouflage.

    Strategy:
    - If camouflage is available and not active, use it to hide.
    - Rest when SP is low.
    - Attack when the enemy is adjacent.
    - Otherwise place a trap near the enemy once and try to lure the
      opponent onto it by moving away.
    - If none of the above, move towards the enemy.
    """
    memos = memos or {}
    trap_mode = memos.get("trap_mode", False)

    enemy_pos = game_info.get("enemy_position")

    # If we cannot see the enemy, simply rest
    if enemy_pos is None:
        return "rest", {"trap_mode": trap_mode}

    distance = abs(robot.x - enemy_pos[0]) + abs(robot.y - enemy_pos[1])

    # Rest when stamina is low
    if robot.sp < 15:
        return "rest", {"trap_mode": trap_mode}

    # Use camouflage when possible and not already active
    if not robot.camouflage.is_active and robot.sp >= robot.camouflage.cost:
        return "camouflage", {"trap_mode": trap_mode}

    # Attack if adjacent
    if distance == 1:
        return "attack", {"trap_mode": False}

    # Place trap near the enemy once
    if not trap_mode and robot.sp >= robot.trap.cost:
        if robot.x < enemy_pos[0]:
            return "trap_right", {"trap_mode": True}
        elif robot.x > enemy_pos[0]:
            return "trap_left", {"trap_mode": True}
        elif robot.y < enemy_pos[1]:
            return "trap_down", {"trap_mode": True}
        else:
            return "trap_up", {"trap_mode": True}

    # If trap was placed, try to lure enemy by moving away
    if trap_mode:
        if robot.x < enemy_pos[0] and robot.x > 0:
            return "left", {"trap_mode": True}
        elif robot.x > enemy_pos[0] and robot.x < robot.controller.x_max - 1:
            return "right", {"trap_mode": True}
        elif robot.y < enemy_pos[1] and robot.y > 0:
            return "up", {"trap_mode": True}
        elif robot.y > enemy_pos[1] and robot.y < robot.controller.y_max - 1:
            return "down", {"trap_mode": True}

    # Default: move towards the enemy
    if robot.x < enemy_pos[0]:
        return "right", {"trap_mode": trap_mode}
    elif robot.x > enemy_pos[0]:
        return "left", {"trap_mode": trap_mode}
    elif robot.y < enemy_pos[1]:
        return "down", {"trap_mode": trap_mode}
    else:
        return "up", {"trap_mode": trap_mode}
