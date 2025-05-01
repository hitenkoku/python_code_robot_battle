def robot_logic(robot, game_info, memos):
    """
    強いロボットのロジック:
    - スキャンを使用して敵の情報を取得
    - 敵のスタミナが少ない場合は攻撃
    - 敵のトラップを避けながら移動
    """
    enemy_position = game_info.get('enemy_position')
    enemy_sp = game_info.get('enemy_sp')
    enemy_traps = game_info.get('enemy_traps', [])
    memo = {}

    # スタミナが少ない場合は休む
    if robot.sp < 20:
        return "rest", memo

    # 敵の情報が見えない場合はスキャンを使用
    if not robot.scan.is_active and enemy_position is None:
        return "scan", memo

    # 敵が隣接している場合は攻撃
    if enemy_position and abs(robot.x - enemy_position[0]) + abs(robot.y - enemy_position[1]) == 1:
        return "attack", memo

    # 敵のスタミナが少ない場合は積極的に攻撃
    if enemy_sp is not None and enemy_sp < 20:
        if enemy_position:
            if robot.x < enemy_position[0]:
                return "right", memo
            elif robot.x > enemy_position[0]:
                return "left", memo
            elif robot.y < enemy_position[1]:
                return "down", memo
            else:
                return "up", memo

    # トラップを避けながら敵に近づく
    if enemy_position:
        if (robot.x + 1, robot.y) not in enemy_traps and robot.x < enemy_position[0]:
            return "right", memo
        elif (robot.x - 1, robot.y) not in enemy_traps and robot.x > enemy_position[0]:
            return "left", memo
        elif (robot.x, robot.y + 1) not in enemy_traps and robot.y < enemy_position[1]:
            return "down", memo
        elif (robot.x, robot.y - 1) not in enemy_traps and robot.y > enemy_position[1]:
            return "up", memo

    # それ以外の場合は休む
    return "rest", memo