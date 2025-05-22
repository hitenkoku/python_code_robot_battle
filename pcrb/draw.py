import json
import os
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

###############################################################################
# ユーティリティ関数
###############################################################################

def safe_load_image(path: str):
    """画像ファイルを読み込みます。

    ファイルが存在しない、または読み込みに失敗した場合は ``None`` を返します。
    呼び出し側ではこの ``None`` を検知して散布図用マーカーへフォールバック描画できます。"""
    if os.path.exists(path):
        try:
            return plt.imread(path)
        except Exception:
            pass
    return None


def add_image_to_plot(
    ax: plt.Axes,
    img,
    x: int,
    y: int,
    *,
    zoom: float = 1.0,
    fallback_color: str = "white",
    marker: str = "s",
):
    """ボード座標 ``(x, y)`` へ ``img`` を描画します。

    ``img`` が ``None`` の場合は色付きスクエアを代わりに表示し、
    スプライトが欠けているときでもアクションの手応えを失わないようにします。"""

    if img is not None:
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (x, y), frameon=False)
        ax.add_artist(ab)
    else:
        ax.scatter(x, y, color=fallback_color, s=100, marker=marker, edgecolors="black")


###############################################################################
# 上位レベル描画ヘルパ
###############################################################################

def _direction_offset(direction: str) -> Tuple[int, int]:
    """移動／罠の方向を (dx, dy) で返します。"""
    mapping = {
        "right": (-1, 0),  # ボード座標は x+→、matplotlib は origin="upper" なので y 軸は反転
        "left": (1, 0),
        "down": (0, -1),
        "up": (0, 1),
        "trap_right": (-1, 0),
        "trap_left": (1, 0),
        "trap_down": (0, -1),
        "trap_up": (0, 1),
    }
    return mapping[direction]


###############################################################################
# 散布図ベースのボード (v1)
###############################################################################

def draw_board(turn_data: dict, x_max: int, y_max: int, *, title: str = "", is_show: bool = True):
    """散布図を用いたシンプルな可視化関数。

    actions.py に定義された **全アクション** をハイライト表示できます。"""

    # ボード初期化: 0 = 空, 1 = Robot A, 2 = Robot B
    board = np.zeros((y_max, x_max))

    # --------------------------------------------------
    # ロボット配置と座標保持
    # --------------------------------------------------
    robot_positions = {}
    for robot in turn_data["robots"]:
        x, y = robot["position"]
        if robot["name"] == "Robot A":
            board[y, x] = 1
        elif robot["name"] == "Robot B":
            board[y, x] = 2
        robot_positions[robot["name"]] = (x, y)

    # 各アクションごとのマーカー用リスト
    markers: dict[str, List[Tuple[int, int]]] = {
        "attack": [],
        "rest": [],
        "move": [],
        "defend": [],
        "parry": [],
        "ranged_attack": [],
        "trap": [],
        "steal": [],
        "teleport": [],
        "camouflage": [],
        "scan": [],
    }

    # --------------------------------------------------
    # アクション内容に応じて対象マスを収集
    # --------------------------------------------------
    player_name = turn_data["action"]["robot_name"]
    if player_name is not None:
        robot_x, robot_y = robot_positions[player_name]
        action_type = turn_data["action"]["action"]

        # --- 近接攻撃 (距離1、フォン・ノイマン近傍)
        if action_type == "attack":
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = robot_x + dx, robot_y + dy
                if 0 <= nx < x_max and 0 <= ny < y_max:
                    markers["attack"].append((ny, nx))

        # --- 休憩 (スタミナ回復)
        elif action_type == "rest":
            markers["rest"].append((robot_y, robot_x))

        # --- 移動 (ハイライトは移動先)
        elif action_type in {"right", "left", "down", "up"}:
            dx, dy = _direction_offset(action_type)
            nx, ny = robot_x + dx, robot_y + dy
            if 0 <= nx < x_max and 0 <= ny < y_max:
                markers["move"].append((ny, nx))

        # --- 防御 (被ダメ軽減)
        elif action_type == "defend":
            markers["defend"].append((robot_y, robot_x))

        # --- パリィ (事前カウンター)
        elif action_type == "parry":
            markers["parry"].append((robot_y, robot_x))

        # --- 遠距離攻撃 (マンハッタン距離2)
        elif action_type == "ranged_attack":
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                nx, ny = robot_x + dx, robot_y + dy
                if 0 <= nx < x_max and 0 <= ny < y_max:
                    markers["ranged_attack"].append((ny, nx))

        # --- 罠 (隣接マス設置)
        elif action_type.startswith("trap_"):
            dx, dy = _direction_offset(action_type)
            nx, ny = robot_x + dx, robot_y + dy
            if 0 <= nx < x_max and 0 <= ny < y_max:
                markers["trap"].append((ny, nx))

        # --- スティール / テレポート
        elif action_type == "steal":
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = robot_x + dx, robot_y + dy
                if 0 <= nx < x_max and 0 <= ny < y_max:
                    markers["steal"].append((ny, nx))
        elif action_type == "teleport":
            markers["teleport"].append((robot_y, robot_x))

        # --- カモフラージュ & スキャン (ロボット自身を表示)
        elif action_type == "camouflage":
            markers["camouflage"].append((robot_y, robot_x))
        elif action_type == "scan":
            markers["scan"].append((robot_y, robot_x))

    # --------------------------------------------------
    # ボードを描画
    # --------------------------------------------------
    plt.figure(figsize=(6, 6))
    cmap = plt.colormaps.get_cmap("coolwarm").resampled(3)  # 0=空,1=A,2=B
    plt.imshow(board, cmap=cmap, origin="upper")
    plt.clim(0, 2)
    plt.xticks(np.arange(0, x_max, 1))
    plt.yticks(np.arange(0, y_max, 1))
    plt.grid(color="gray", linestyle="-", linewidth=0.5)

    # アクション→色 マッピング
    colour_map = {
        "attack": "red",
        "rest": "green",
        "move": "black",
        "defend": "yellow",
        "parry": "cyan",
        "ranged_attack": "orange",
        "trap": "purple",
        "steal": "magenta",
        "teleport": "brown",
        "camouflage": "grey",
        "scan": "blue",
    }

    for key, positions in markers.items():
        for y, x in positions:
            plt.scatter(x, y, color=colour_map[key], s=100, marker="s", edgecolors="black")

    if title:
        plt.title(title)
    if is_show:
        plt.show()
    return plt


###############################################################################
# スプライトベースのボード (v2)
###############################################################################

def draw_board_v2(
    turn_data: dict,
    x_max: int,
    y_max: int,
    *,
    title: str = "",
    is_show: bool = True,
):
    """スプライトを用いたリッチな可視化関数。

    対応スプライトが無い要素は色付き四角で補完表示します。
    """

    # ----------------------------------------------------------------------
    # スプライト読み込み（存在しない場合は None → フォールバック描画）
    # ----------------------------------------------------------------------
    asset_dir = "./pcrb/asset"

    sprites = {
        "tile": safe_load_image(os.path.join(asset_dir, "tile.png")),
        "robot_a": safe_load_image(os.path.join(asset_dir, "red_robot.png")),
        "robot_b": safe_load_image(os.path.join(asset_dir, "blue_robot.png")),
        "attack": safe_load_image(os.path.join(asset_dir, "attack.png")),
        "rest": safe_load_image(os.path.join(asset_dir, "rest.png")),
        "move": safe_load_image(os.path.join(asset_dir, "move.png")),
        "defend": safe_load_image(os.path.join(asset_dir, "defend.png")),
        "parry": safe_load_image(os.path.join(asset_dir, "parry.png")),
        "ranged_attack": safe_load_image(os.path.join(asset_dir, "ranged_attack.png")),
        "trap": safe_load_image(os.path.join(asset_dir, "trap.png")),
        "steal": safe_load_image(os.path.join(asset_dir, "steal.png")),
        "teleport": safe_load_image(os.path.join(asset_dir, "teleport.png")),
        "camouflage": safe_load_image(os.path.join(asset_dir, "camouflage.png")),
        "scan": safe_load_image(os.path.join(asset_dir, "scan.png")),
    }

    # ----------------------------------------------------------------------
    # Figure / Axes 準備
    # ----------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.tick_params(colors="white")
    ax.set_xlim(-0.5, x_max - 0.5)
    ax.set_ylim(-0.5, y_max - 0.5)
    ax.set_xticks(np.arange(0, x_max, 1))
    ax.set_yticks(np.arange(0, y_max, 1))
    ax.grid(color="gray", linestyle="-", linewidth=0.5)
    ax.set_aspect("equal")

    # 背景タイル
    for x in range(x_max):
        for y in range(y_max):
            add_image_to_plot(ax, sprites["tile"], x, y, zoom=1.0, fallback_color="#444")

    # ----------------------------------------------------------------------
    # ロボット描画 & 座標記録
    # ----------------------------------------------------------------------
    robot_positions: dict[str, Tuple[int, int]] = {}
    for robot in turn_data["robots"]:
        x, y = robot["position"]
        robot_positions[robot["name"]] = (x, y)
        if robot["name"] == "Robot A":
            add_image_to_plot(ax, sprites["robot_a"], x, y, zoom=0.9, fallback_color="white")
        elif robot["name"] == "Robot B":
            add_image_to_plot(ax, sprites["robot_b"], x, y, zoom=0.9, fallback_color="lightblue")

    # ----------------------------------------------------------------------
    # アクション可視化
    # ----------------------------------------------------------------------
    player_name = turn_data["action"]["robot_name"]
    if player_name is not None:
        robot_x, robot_y = robot_positions[player_name]
        action_type = turn_data["action"]["action"]

        # ボード範囲内判定ヘルパ
        def _in_field(nx: int, ny: int) -> bool:
            return 0 <= nx < x_max and 0 <= ny < y_max

        # --- 近接攻撃
        if action_type == "attack":
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = robot_x + dx, robot_y + dy
                if _in_field(nx, ny):
                    add_image_to_plot(ax, sprites["attack"], nx, ny, zoom=0.9, fallback_color="red")

        # --- 休憩
        elif action_type == "rest":
            add_image_to_plot(ax, sprites["rest"], robot_x, robot_y, zoom=0.9, fallback_color="green")

        # --- 移動
        elif action_type in {"right", "left", "down", "up"}:
            dx, dy = _direction_offset(action_type)
            nx, ny = robot_x + dx, robot_y + dy
            if _in_field(nx, ny):
                add_image_to_plot(ax, sprites["move"], nx, ny, zoom=0.9, fallback_color="black")

        # --- 防御
        elif action_type == "defend":
            add_image_to_plot(ax, sprites["defend"], robot_x, robot_y, zoom=0.9, fallback_color="yellow")

        # --- パリィ
        elif action_type == "parry":
            add_image_to_plot(ax, sprites["parry"], robot_x, robot_y, zoom=0.9, fallback_color="cyan")

        # --- 遠距離攻撃
        elif action_type == "ranged_attack":
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                nx, ny = robot_x + dx, robot_y + dy
                if _in_field(nx, ny):
                    add_image_to_plot(ax, sprites["ranged_attack"], nx, ny, zoom=0.9, fallback_color="orange")

        # --- 罠設置
        elif action_type.startswith("trap_"):
            dx, dy = _direction_offset(action_type)
            nx, ny = robot_x + dx, robot_y + dy
            if _in_field(nx, ny):
                add_image_to_plot(ax, sprites["trap"], nx, ny, zoom=0.9, fallback_color="purple")

        # --- スティール
        elif action_type == "steal":
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = robot_x + dx, robot_y + dy
                if _in_field(nx, ny):
                    add_image_to_plot(ax, sprites["steal"], nx, ny, zoom=0.9, fallback_color="magenta")

        # --- テレポート
        elif action_type == "teleport":
            add_image_to_plot(ax, sprites["teleport"], robot_x, robot_y, zoom=0.9, fallback_color="brown")

        # --- カモフラージュ
        elif action_type == "camouflage":
            add_image_to_plot(ax, sprites["camouflage"], robot_x, robot_y, zoom=0.9, fallback_color="grey")

        # --- スキャン
        elif action_type == "scan":
            add_image_to_plot(ax, sprites["scan"], robot_x, robot_y, zoom=0.9, fallback_color="blue")

    # ----------------------------------------------------------------------
    # タイトル／表示
    # ----------------------------------------------------------------------
    if title:
        ax.set_title(title, color="white")
    if is_show:
        plt.show()

    return fig
