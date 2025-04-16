import sys

sys.path.append('./')

from pcrb.robot import Robot
from pcrb.controller import GameController


def test():
    controller = GameController(max_turn=100, x_max=9, y_max=7)

    robot = Robot("Alpha", 0, 0, None, controller)
    target = Robot("TargetDummy", 0, 1, None, controller)

    robot.status()
    target.status()

    assert not robot.parry.is_active
    assert robot.parry.cooldown_counter == 0
    assert target._stun_counter == 0

    robot.start_turn()
    robot.parry(1)  # パリーを実施
    target.start_turn()
    target.attack(robot, 1) # パリーにより攻撃は失敗
    robot.status()
    target.status()

    assert robot.hp == 100
    assert robot.parry.is_active
    assert robot.parry.cooldown_counter == 2
    assert target._stun_counter == 1

    robot.start_turn()
    robot.parry(1)  # パリーを実施(クールダウン中のため失敗)
    target.start_turn()
    target.attack(robot, 1) # 攻撃は成功
    robot.status()
    target.status()

    assert robot.hp < 100
    assert not robot.parry.is_active
    assert robot.parry.cooldown_counter == 1
    assert target._stun_counter == 0

    robot.start_turn()
    robot.attack(robot, 1)
    target.start_turn()
    target.attack(robot, 1)
    robot.status()
    target.status()

    assert robot.hp < 100
    assert not robot.parry.is_active
    assert robot.parry.cooldown_counter == 0
    assert target._stun_counter == 0


if __name__ == "__main__":
    test()
