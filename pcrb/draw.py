import json
import matplotlib.pyplot as plt
import numpy as np


# フィールドサイズの設定
field_size = 12


# 各ターンの盤面を描画する関数
def draw_board(turn_data):
    # 盤面の初期化（0: 空, 1: Robot A, 2: Robot B）
    board = np.zeros((field_size, field_size))

    # ロボットの配置
    robot_positions = {}
    for robot in turn_data["robots"]:
        x, y = robot["position"]
        if robot["name"] == "Robot A":
            board[x, y] = 1  # Robot Aは1で表示
        elif robot["name"] == "Robot B":
            board[x, y] = 2  # Robot Bは2で表示
        robot_positions[robot["name"]] = (x, y)

    # 攻撃範囲の座標を保持するリスト
    attack_positions = []
    evade_positions = []
    move_positions = []

    attacker_name = turn_data["action"]["robot_name"]
    attack_x, attack_y = robot_positions[attacker_name]
    # アクションが攻撃である場合、攻撃範囲を設定
    if turn_data["action"]["action"] == "attack":
        # 四方1マスの範囲を攻撃範囲として設定
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = attack_x + dx, attack_y + dy
            if 0 <= nx < field_size and 0 <= ny < field_size:
                attack_positions.append((ny, nx))  # プロット時は(y, x)順
    elif turn_data["action"]["action"] == "evade":
        evade_positions.append((attack_y, attack_x))  # プロット時は(y, x)順
    elif turn_data["action"]["action"] == "right":
        move_positions.append((attack_y, attack_x-1))  # プロット時は(y, x)順
    elif turn_data["action"]["action"] == "left":
        move_positions.append((attack_y, attack_x+1))  # プロット時は(y, x)順
    elif turn_data["action"]["action"] == "down":
        move_positions.append((attack_y-1, attack_x))  # プロット時は(y, x)順
    elif turn_data["action"]["action"] == "up":
        move_positions.append((attack_y+1, attack_x))  # プロット時は(y, x)順

    # 盤面を画像としてプロット
    plt.figure(figsize=(6, 6))
    cmap = plt.colormaps.get_cmap("coolwarm").resampled(3) # 3色に設定（空、Robot A、Robot B）
    plt.imshow(board, cmap=cmap, origin="upper")
    # plt.colorbar(ticks=[0, 1, 2], label="Legend")
    plt.clim(0, 2)
    plt.xticks(np.arange(0, field_size, 1))
    plt.yticks(np.arange(0, field_size, 1))
    plt.grid(color='gray', linestyle='-', linewidth=0.5)

    # 攻撃範囲に小さい四角をプロット
    if attack_positions:
        for y, x in attack_positions:
            plt.scatter(y, x, color='red', s=100, marker='s', edgecolors='black')
    if evade_positions:
        for y, x in evade_positions:
            plt.scatter(y, x, color='green', s=100, marker='s', edgecolors='black')
    if move_positions:
        for y, x in move_positions:
            plt.scatter(y, x, color='black', s=100, marker='s', edgecolors='black')

    plt.title(
        f"Turn {turn_data['turn']} - Action: {turn_data['action']['robot_name']} -> {turn_data['action']['action']}")
    plt.show()


def main():
    # JSONファイルの読み込み
    with open('./game_state.json', 'r') as file:
        data = json.load(file)

    # 各ターンの表示
    for turn_data in data:
        draw_board(turn_data)


if __name__ == "__main__":
    main()
