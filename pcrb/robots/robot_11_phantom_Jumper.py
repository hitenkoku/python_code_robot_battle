def robot_logic(robot, game_info, memos):
    """
    Teleport を活用したロジック:
    - スタミナが少ない場合は休む。
    - 敵が隣接している場合は攻撃。
    - 敵が遠距離にいる場合はテレポートで距離を詰める。
    - 敵が近づきすぎた場合はテレポートで距離を取る。
    """
    enemy_position = game_info['enemy_position']
    distance = abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1])

    # スタミナが少ない場合は休む
    if robot.sp < 20:
        return "rest"

    # 敵が隣接している場合は攻撃
    if distance == 1:
        return "attack"

    # 敵が遠距離にいる場合はテレポートで距離を詰める
    if distance > 2 and robot.sp >= 20:
        return "teleport"

    # 敵が近づきすぎた場合はテレポートで距離を取る
    if distance <= 2 and robot.sp >= 20:
        return "teleport"

    # デフォルトの動作
    return "rest"