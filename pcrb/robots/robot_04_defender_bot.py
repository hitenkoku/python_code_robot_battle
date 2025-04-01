def robot_logic(robot, game_info, memos):
    # スタミナが少ない場合は休み、それ以外は防御
    if robot.sp < robot.defend.cost:
        return "rest"
    else:
        return "defend"
