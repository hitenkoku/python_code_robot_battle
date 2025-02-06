import streamlit as st
import ast
import traceback

import sys
sys.path.append('./pcrb')

# 許可する関数とモジュール
ALLOWED_FUNCTIONS = {"robot_logic"}
ALLOWED_MODULES = set()
GAME_STATE_FILE = "./game_state.json"  # 既存のgame_state.jsonファイル


def is_safe_code(file_content):
    """
    アップロードされたコードを解析し、安全かどうかを判定する
    """
    try:
        # 抽象構文木 (AST) に変換
        tree = ast.parse(file_content)

        for node in ast.walk(tree):
            # インポートのチェック
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if node.module not in ALLOWED_MODULES:
                    return False, f"Unauthorized module import: {node.module}"

            # 関数定義以外のコードを制限
            if isinstance(node, ast.FunctionDef):
                if node.name not in ALLOWED_FUNCTIONS:
                    return False, f"Unauthorized function definition: {node.name}"

            # 危険な構文の検出 (exec, eval など)
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval"}:
                    return False, f"Unauthorized function call: {node.func.id}"

        return True, "Code is safe"
    except Exception as e:
        return False, f"Error analyzing code: {e}"


def load_player_module(file_content):
    # サンドボックス的にモジュールをロード
    import importlib.util

    # ファイルを一時的に保存
    file_path = "./uploaded_logic_safe.py"
    with open(file_path, "w") as f:
        f.write(file_content)

    spec = importlib.util.spec_from_file_location("robot_logic_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # robot_logic 関数を取得
    robot_logic = getattr(module, "robot_logic", None)

    return robot_logic


def platy_game(robot_logic_a, robot_logic_b):
    from main import GameController
    from main import Robot

    controller = GameController(max_turn=100, x_max=9, y_max=7)
    robot1 = Robot("Robot A", 1, 3, robot_logic_a, controller)
    robot2 = Robot("Robot B", 7, 3, robot_logic_b, controller)
    controller.set_robots(robot1, robot2)
    winner = controller.game_loop()

    return winner


def main():
    from robots.stage01 import robot_logic as robot_logic_01
    from robots.stage02 import robot_logic as robot_logic_02
    from robots.stage03 import robot_logic as robot_logic_03
    from robots.stage04 import robot_logic as robot_logic_04
    st.title("Python Code Robot Battle")

    uploaded_file = st.file_uploader("Upload a Python file with robot_logic function")

    enemy_robot_logics = [robot_logic_01, robot_logic_02, robot_logic_03, robot_logic_04]

    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")

        # コード可視化
        st.subheader("Uploaded Code")
        st.code(file_content, language="python")

        # コードの安全性チェック
        is_safe, message = is_safe_code(file_content)
        if not is_safe:
            st.error(f"Unsafe code detected: {message}")
        else:
            try:
                player_robot_logic = load_player_module(file_content)
                if player_robot_logic:
                    for _k, enemy_robot_logic in enumerate(enemy_robot_logics):
                        st.success(f"Function loaded successfully for enemy logic {_k + 1}!")
                        winner, game_state = platy_game(player_robot_logic, enemy_robot_logic)

                        st.header(f"{winner.name} wins!")

                        try:
                            with open(GAME_STATE_FILE, "r") as f:
                                game_state_content = f.read()
                            st.download_button(
                                label=f"Download game_state.json (Game {_k + 1})",
                                data=game_state_content,
                                file_name=f"game_state_{_k + 1}.json",
                                mime="application/json"
                            )
                        except FileNotFoundError:
                            st.error(f"game_state.json file not found for Game {_k + 1}.")
                        except Exception as e:
                            st.error(f"Error reading game_state.json for Game {_k + 1}: {e}")

                        if not winner:
                            break
                else:
                    st.error("No function named `robot_logic` found in the uploaded file.")
            except Exception as e:
                st.error(f"Error processing the uploaded file: {traceback.format_exc()}")


if __name__ == "__main__":
    main()
