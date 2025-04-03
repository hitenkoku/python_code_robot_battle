def robot_logic(robot, game_info, memos):
    """
    防御重視のロジック:
    - 敵が隣接している場合、防御を優先。
    - スタミナが少ない場合は休む。
    - 敵が遠距離にいる場合、敵に近づく。
    - スタミナが十分で敵が近い場合、攻撃を試みる。
    """
    enemy_position = game_info['enemy_position']
    distance = abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1])

    # スタミナが少ない場合は休む
    if robot.sp < 20:
        return "rest"

    # 敵が隣接している場合、防御を優先
    if distance == 1:
        return "defend"

    # 敵が遠距離にいる場合、敵に近づく
    if distance > 1:
        if robot.position[0] < enemy_position[0]:
            return "right"
        elif robot.position[0] > enemy_position[0]:
            return "left"
        elif robot.position[1] < enemy_position[1]:
            return "down"
        else:
            return "up"

    # スタミナが十分で敵が近い場合、攻撃を試みる
    if robot.sp >= 30:
        return "attack"
