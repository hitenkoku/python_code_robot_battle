def robot_logic(robot, game_info, memos):
    """
    対抗ロジック:
    - 敵が隣接している場合、スタミナが十分なら攻撃、そうでなければ回避。
    - 敵が遠距離攻撃を試みる距離にいる場合、スタミナを温存しつつ回避。
    - 敵に近づきすぎないように距離を保ちながら戦う。
    - スタミナが少ない場合は休む。
    """
    enemy_position = game_info['enemy_position']
    enemy_hp = game_info['enemy_hp']
    distance = abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1])

    # スタミナが少ない場合は休む
    if robot.sp < 20:
        return "rest"

    # 敵が隣接している場合
    if distance == 1:
        if robot.sp >= 30:
            return "attack"  # スタミナが十分なら攻撃
        else:
            # スタミナが少ない場合は回避
            if robot.position[0] < enemy_position[0]:
                return "left"
            elif robot.position[0] > enemy_position[0]:
                return "right"
            elif robot.position[1] < enemy_position[1]:
                return "up"
            else:
                return "down"

    # 敵が遠距離攻撃を試みる距離にいる場合
    if distance == 2:
        # 敵の遠距離攻撃を回避するために移動
        if robot.position[0] < enemy_position[0]:
            return "left"
        elif robot.position[0] > enemy_position[0]:
            return "right"
        elif robot.position[1] < enemy_position[1]:
            return "up"
        else:
            return "down"

    # 敵に近づきすぎないように距離を保つ
    if distance > 2:
        if robot.position[0] < enemy_position[0]:
            return "right"
        elif robot.position[0] > enemy_position[0]:
            return "left"
        elif robot.position[1] < enemy_position[1]:
            return "down"
        else:
            return "up"

    # デフォルトの動作
    return "rest"