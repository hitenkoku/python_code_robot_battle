import sys

sys.path.append('./')

from pcrb.robot import Robot
from pcrb.controller import GameController


def robot_logic_a(robot, game_info, memos=None):
    return "right"


def robot_logic_b(robot, game_info, memos=None):
    return "up"


def test_adjust_action():
    controller = GameController(max_turn=100, x_max=9, y_max=7)

    robot1 = Robot("robot1", 0, 0, robot_logic_a, controller)
    robot2 = Robot("robot2", 0, 1, robot_logic_a, controller)
    controller.set_robots(robot1, robot2)

    action = controller.run_logic(robot1)
    assert action == "right"

    action = controller.run_logic(robot2)
    assert action == "left"

    robot1 = Robot("robot1", 0, 0, robot_logic_b, controller)
    robot2 = Robot("robot2", 0, 1, robot_logic_b, controller)
    controller.set_robots(robot1, robot2)

    action = controller.run_logic(robot1)
    assert action == "up"

    action = controller.run_logic(robot2)
    assert action == "down"


if __name__ == "__main__":
    test_adjust_action()
