def robot_logic(robot, game_info, memos):
    """
    基本的なロジック:
    - 敵が隣接している場合のみ攻撃。
    - スタミナが少ない場合は休む。
    - 敵に近づくために単純な移動を行う。
    """
    enemy_position = game_info['enemy_position']
    distance = abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1])

    # スタミナが少ない場合は休む
    if robot.sp < 15:
        return "rest"

    # 敵が隣接している場合のみ攻撃
    if distance == 1:
        return "attack"

    # 敵に近づくために単純な移動を行う
    if robot.position[0] < enemy_position[0]:
        return "right"
    elif robot.position[0] > enemy_position[0]:
        return "left"
    elif robot.position[1] < enemy_position[1]:
        return "down"
    else:
        return "up"
