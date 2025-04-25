import sys

sys.path.append('./pcrb')

from robot import Robot
from controller import GameController


def robot_logic1(robot, game_info, memos=None):
    # スタミナが少ない場合は休み、それ以外は敵に近づいて攻撃
    enemy_position = game_info['enemy_position']
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


def robot_logic2(robot, game_info, memos=None):
    # スタミナが少ない場合は休み、それ以外は敵に近づいて攻撃
    memo = {'text': 'dummy', 'num': 0}
    enemy_position = game_info['enemy_position']
    if robot.sp < 20:
        return "rest", memo
    elif abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1]) == 1:
        return "attack", memo
    else:
        if robot.position[0] < enemy_position[0]:
            return "right", memo
        elif robot.position[0] > enemy_position[0]:
            return "left", memo
        elif robot.position[1] < enemy_position[1]:
            return "down", memo
        else:
            return "up", memo


def test():
    controller = GameController(max_turn=100, x_max=9, y_max=7)

    robot1 = Robot("robot1", 0, 0, robot_logic1, controller)
    robot2 = Robot("robot2", 0, 1, robot_logic2, controller)
    controller.set_robots(robot1, robot2)

    assert len(controller.memos1) == 0
    assert len(controller.memos2) == 0

    controller.run_logic(robot1)

    assert len(controller.memos1) == 1
    assert len(controller.memos2) == 0

    controller.run_logic(robot2)

    assert len(controller.memos1) == 1
    assert len(controller.memos2) == 1

    controller.run_logic(robot1)

    assert len(controller.memos1) == 2
    assert len(controller.memos2) == 1

    controller.run_logic(robot2)

    assert len(controller.memos1) == 2
    assert len(controller.memos2) == 2


if __name__ == "__main__":
    test()
