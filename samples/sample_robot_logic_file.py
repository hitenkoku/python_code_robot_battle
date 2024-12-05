# 必須のrobot_logic関数を定義
def robot_logic(robot, game_ifo):
    # スタミナが少ない場合は休み、それ以外は敵に近づいて攻撃
    enemy_position = game_ifo['enemy_position']
    if robot.sp < 20:
        return "rest"
    elif abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1]) == 1:
        return "attack"
    else:
        if robot.position[0] < enemy_position[0]:
            return "right"
        elif robot.position[0] > enemy_position[0]:
            return "left"
        elif robot.position[1] < enemy_position[1]:
            return "down"
        else:
            return "up"
