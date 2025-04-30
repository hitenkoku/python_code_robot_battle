import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os


# 各ターンの盤面を描画する関数
def draw_board(turn_data, x_max, y_max, title='', is_show=True):
    # 盤面の初期化（0: 空, 1: Robot A, 2: Robot B）
    board = np.zeros((y_max, x_max))

    # ロボットの配置
    robot_positions = {}
    for robot in turn_data["robots"]:
        x, y = robot["position"]
        if robot["name"] == "Robot A":
            board[y, x] = 1  # Robot Aは1で表示
        elif robot["name"] == "Robot B":
            board[y, x] = 2  # Robot Bは2で表示
        robot_positions[robot["name"]] = (x, y)

    # 攻撃範囲の座標を保持するリスト
    attack_positions = []
    rest_positions = []
    move_positions = []

    attacker_name = turn_data["action"]["robot_name"]
    attack_x, attack_y = robot_positions[attacker_name]
    # アクションが攻撃である場合、攻撃範囲を設定
    if turn_data["action"]["action"] == "attack":
        # 四方1マスの範囲を攻撃範囲として設定
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = attack_x + dx, attack_y + dy
            if 0 <= nx < x_max and 0 <= ny < y_max:
                attack_positions.append((ny, nx))  # プロット時は(y, x)順
    elif turn_data["action"]["action"] == "rest":
        rest_positions.append((attack_y, attack_x))  # プロット時は(y, x)順
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
    plt.xticks(np.arange(0, x_max, 1))
    plt.yticks(np.arange(0, y_max, 1))
    plt.grid(color='gray', linestyle='-', linewidth=0.5)

    # 攻撃範囲に小さい四角をプロット
    if attack_positions:
        for y, x in attack_positions:
            plt.scatter(x, y, color='red', s=100, marker='s', edgecolors='black')
    if rest_positions:
        for y, x in rest_positions:
            plt.scatter(x, y, color='green', s=100, marker='s', edgecolors='black')
    if move_positions:
        for y, x in move_positions:
            plt.scatter(x, y, color='black', s=100, marker='s', edgecolors='black')

    if title:
        plt.title(title)

    if is_show:
        plt.show()
    return plt


def draw_board_v2(turn_data, x_max, y_max, title='', is_show=True):
    # 画像の読み込み
    asset_dir = './pcrb/asset'
    tile_img = plt.imread(os.path.join(asset_dir, 'tile.png'))
    robot_a_img = plt.imread(os.path.join(asset_dir, 'red_robot.png'))
    robot_b_img = plt.imread(os.path.join(asset_dir, 'blue_robot.png'))
    attack_img = plt.imread(os.path.join(asset_dir, 'attack.png'))
    rest_img = plt.imread(os.path.join(asset_dir, 'rest.png'))
    move_img = plt.imread(os.path.join(asset_dir, 'move.png'))

    # プロットの準備
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('black')     # Figure 背景
    ax.set_facecolor('black')            # Axes 背景
    ax.tick_params(colors='white')       # 目盛り文字・目盛り線を白に
    ax.set_xlim(-0.5, x_max - 0.5)
    ax.set_ylim(-0.5, y_max - 0.5)
    ax.set_xticks(np.arange(0, x_max, 1))
    ax.set_yticks(np.arange(0, y_max, 1))
    ax.grid(color='gray', linestyle='-', linewidth=0.5)
    ax.set_aspect('equal')

    # 背景タイルの描画
    for x in range(x_max):
        for y in range(y_max):
            add_image_to_plot(ax, tile_img, x, y, zoom=1.0)  # タイル画像を正確に1マスに収める

    # ロボットの配置
    robot_positions = {}
    for robot in turn_data["robots"]:
        x, y = robot["position"]
        robot_positions[robot["name"]] = (x, y)
        if robot["name"] == "Robot A":
            add_image_to_plot(ax, robot_a_img, x, y, zoom=0.9)  # ロボット画像を少し小さく
        elif robot["name"] == "Robot B":
            add_image_to_plot(ax, robot_b_img, x, y, zoom=0.9)

    # アクションの処理
    attacker_name = turn_data["action"]["robot_name"]
    attack_x, attack_y = robot_positions[attacker_name]
    action_type = turn_data["action"]["action"]

    if action_type == "attack":
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = attack_x + dx, attack_y + dy
            if 0 <= nx < x_max and 0 <= ny < y_max:
                add_image_to_plot(ax, attack_img, nx, ny, zoom=0.9)
    elif action_type == "rest":
        add_image_to_plot(ax, rest_img, attack_x, attack_y, zoom=0.9)
    elif action_type in ["right", "left", "down", "up"]:
        dx, dy = {"right": (-1, 0), "left": (1, 0), "down": (0, -1), "up": (0, 1)}[action_type]
        nx, ny = attack_x + dx, attack_y + dy
        if 0 <= nx < x_max and 0 <= ny < y_max:
            add_image_to_plot(ax, move_img, nx, ny, zoom=0.9)

    if title:
        ax.set_title(title)

    if is_show:
        plt.show()
    return fig

def add_image_to_plot(ax, img, x, y, zoom=1.0):
    """指定した座標に画像をプロットするヘルパー関数"""
    imagebox = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(imagebox, (x, y), frameon=False)
    ax.add_artist(ab)


def main():
    # JSONファイルの読み込み
    with open('./game_state.json', 'r') as file:
        data = json.load(file)

    settings = data[0]['settings']
    max_turn = settings['max_turn']
    x_max = settings['x_max']
    y_max = settings['y_max']

    all_turn_data = data[1:]

    # 各ターンの表示
    for turn_data in all_turn_data:
        title = f"Turn {turn_data['turn']} - Action: {turn_data['action']['robot_name']} -> {turn_data['action']['action']}"
        draw_board(turn_data, x_max, y_max, title)


if __name__ == "__main__":
    main()
