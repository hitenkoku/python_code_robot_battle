import sys

sys.path.append('./')

from pcrb.robot import Robot
from pcrb.controller import GameController


def robot_logic(robot, game_info, memos):
    """テスト用ロジック: 隣接している場合はスタミナを盗む"""
    enemy_position = game_info['enemy_position']
    if abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1]) == 1:
        return "steal", {}
    return "rest", {}


def test_steal():
    controller = GameController()

    # ロボット1の初期位置
    robot1 = Robot("Robot A", 1, 3, robot_logic, controller)

    # ロボット2の初期位置
    robot2 = Robot("Robot B", 2, 3, robot_logic, controller)

    controller.set_robots(robot1, robot2)

    initial_sp_robot1 = robot1.sp
    initial_sp_robot2 = robot2.sp

    # ゲームループを1ターン実行して Steal の動作を確認
    controller.run_logic(robot1)

    # ロボット1がロボット2からスタミナを盗んだことを確認
    assert robot1.sp > initial_sp_robot1, "Robot A should have gained SP after stealing."
    assert robot2.sp < initial_sp_robot2, "Robot B should have lost SP after being stolen from."

    print(f"Robot A SP: {robot1.sp}, Robot B SP: {robot2.sp}")


if __name__ == "__main__":
    test_steal()