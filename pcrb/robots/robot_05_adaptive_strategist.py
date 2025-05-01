def robot_logic(robot, game_info, memos):
    """
    改良されたロジック:
    - 敵が隣接している場合、攻撃を優先。
    - スタミナが少ない場合は休む。
    - 敵が遠距離にいる場合、遠距離攻撃を試みる。
    - 敵に近づくために最適な方向に移動。
    - スタミナが十分で敵が近い場合、チャージ攻撃を準備。
    """
    enemy_position = game_info['enemy_position']
    enemy_hp = game_info['enemy_hp']
    distance = abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1])

    # スタミナが少ない場合は休む
    if robot.sp < 20:
        return "rest"

    # 敵が隣接している場合、攻撃を優先
    if distance == 1:
        return "attack"

    # 敵が遠距離にいる場合、遠距離攻撃を試みる
    if distance == 2 and robot.sp >= 15:
        return "ranged_attack"

    # 敵に近づくために最適な方向に移動
    if robot.position[0] < enemy_position[0]:
        return "right"
    elif robot.position[0] > enemy_position[0]:
        return "left"
    elif robot.position[1] < enemy_position[1]:
        return "down"
    else:
        return "up"