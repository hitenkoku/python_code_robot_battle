def robot_logic(robot, game_info, memos):
    """
    強いロジック:
    - スタミナが十分であればカモフラージュを使用して敵の攻撃を回避
    - 敵に近づいて攻撃を仕掛ける
    - スタミナが少ない場合は休む
    """
    enemy_position = game_info['enemy_position']
    memo = {}

    # 敵の位置が不明（カモフラージュ中）なら待機
    if enemy_position is None:
        return "rest", memo

    # スタミナが十分でカモフラージュが無効ならカモフラージュを使用
    if robot.sp >= 20 and not robot.camouflage.is_active:
        return "camouflage", memo

    # 敵が隣接している場合は攻撃
    if abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1]) == 1:
        return "attack", memo

    # スタミナが少ない場合は休む
    if robot.sp < 20:
        return "rest", memo

    # 敵に近づく
    if robot.position[0] < enemy_position[0]:
        return "right", memo
    elif robot.position[0] > enemy_position[0]:
        return "left", memo
    elif robot.position[1] < enemy_position[1]:
        return "down", memo
    else:
        return "up", memo