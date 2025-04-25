import sys

sys.path.append('./pcrb')

from robot import Robot
from controller import GameController


def robot_logic(robot, game_info, memos):
    """テスト用ロジック: カモフラージュを使用"""
    if 0 < game_info['turn'] < 3:
        assert game_info['enemy_position'] is None, "Enemy position should be hidden when camouflaged."

    if robot.sp >= 20 and not robot.camouflage.is_active:
        return "camouflage"
    return "rest"


def test_camouflage():
    controller = GameController()

    # ロボット1の初期位置
    robot1 = Robot("Robot A", 1, 3, robot_logic, controller)

    # ロボット2の初期位置
    robot2 = Robot("Robot B", 7, 3, robot_logic, controller)

    controller.set_robots(robot1, robot2)

    # 初期状態の確認
    assert not robot1.camouflage.is_active, "Robot A should not be camouflaged initially."
    assert not robot2.camouflage.is_active, "Robot B should not be camouflaged initially."

    # カモフラージュを使用
    controller.run_logic(robot1)

    # カモフラージュが有効になったことを確認
    assert robot1.camouflage.is_active, "Robot A should be camouflaged after using camouflage."
    assert robot1.camouflage.remaining_turns == 3, "Camouflage duration should be 3 turns."

    # カモフラージュの持続ターンをシミュレート
    for _ in range(2):
        robot1.start_turn()
        assert robot1.camouflage.is_active, "Camouflage should remain active during its duration."

    # カモフラージュが終了したことを確認
    robot1.start_turn()
    assert not robot1.camouflage.is_active, "Camouflage should no longer be active after its duration ends."


if __name__ == "__main__":
    test_camouflage()