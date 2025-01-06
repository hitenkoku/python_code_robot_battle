import sys

sys.path.append('./')

from pcrb.main import Robot
from pcrb.main import GameController


def test():
    controller = GameController(max_turn=100, x_max=9, y_max=7)

    robot = Robot("Alpha", 0, 0, None, controller)
    target = Robot("TargetDummy", 0, 2, None, controller)

    robot.status()
    target.status()

    robot.ranged_attack(target, 1)  # 遠距離攻撃を実行
    robot.status()
    target.status()

    robot.rest(2)  # SPを回復
    robot.status()
    target.status()


if __name__ == "__main__":
    test()
