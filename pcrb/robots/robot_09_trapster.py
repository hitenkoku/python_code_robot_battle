def robot_logic(robot, game_info, memos):
    """
    罠を活用するロジック。
    - スタミナが少ない場合は休む。
    - 敵の近くに罠を設置。
    - 敵が罠にかかる位置に移動して攻撃を仕掛ける。
    """
    enemy_position = game_info['enemy_position']
    enemy_hp = game_info['enemy_hp']
    robot_position = robot.position

    # スタミナが少ない場合は休む
    if robot.sp < 20:
        return "rest"

    # 敵が隣接している場合は攻撃
    if abs(robot_position[0] - enemy_position[0]) + abs(robot_position[1] - enemy_position[1]) == 1:
        return "attack"

    # 敵の近くに罠を設置
    if robot.sp >= 15:
        if enemy_position[1] > robot_position[1]:
            return "trap_down"
        elif enemy_position[1] < robot_position[1]:
            return "trap_up"
        elif enemy_position[0] > robot_position[0]:
            return "trap_right"
        elif enemy_position[0] < robot_position[0]:
            return "trap_left"

    # 敵に近づく
    if robot_position[0] < enemy_position[0]:
        return "right"
    elif robot_position[0] > enemy_position[0]:
        return "left"
    elif robot_position[1] < enemy_position[1]:
        return "down"
    else:
        return "up"