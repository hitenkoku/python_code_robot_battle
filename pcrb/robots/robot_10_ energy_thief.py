def robot_logic(robot, game_info, memos):
    """Steal を活用した強力なロジック"""
    enemy_position = game_info['enemy_position']
    enemy_sp = game_info['enemy_hp']
    memo = {}

    # 1. 敵が隣接していて SP がある場合は Steal を実行
    if abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1]) == 1:
        if enemy_sp > 0:
            return "steal", memo
        return "attack", memo

    # 2. SP が少ない場合は休む
    if robot.sp < 20:
        return "rest", memo

    # 3. 敵に近づく
    if robot.position[0] < enemy_position[0]:
        return "right", memo
    elif robot.position[0] > enemy_position[0]:
        return "left", memo
    elif robot.position[1] < enemy_position[1]:
        return "down", memo
    else:
        return "up", memo