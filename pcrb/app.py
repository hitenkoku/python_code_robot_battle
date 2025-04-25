import streamlit as st
import ast
import traceback
import json

from pages.drawer import st_draw_board
from controller import GameController
from robot import Robot


# 許可する関数とモジュール
ALLOWED_FUNCTIONS = {"robot_logic"}
ALLOWED_MODULES = ['random', 'math']
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
            if isinstance(node, ast.Import):
                for alias in node.names:
                    print(f"Importing module: {alias.name}")
                    if alias.name not in ALLOWED_MODULES:
                        return False, f"Unauthorized module import: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                print(f"Importing from module: {node.module}")
                if node.module not in ALLOWED_MODULES:
                    return False, f"Unauthorized module import: {node.module}"

            # 関数定義以外のコードを制限
            if isinstance(node, ast.FunctionDef):
                print(f"Defining function: {node.name}")
                if node.name not in ALLOWED_FUNCTIONS:
                    return False, f"Unauthorized function definition: {node.name}"

            # 危険な構文の検出 (exec, eval など)
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval"}:
                    return False, f"Unauthorized function call: {node.func.id}"

        return True, "Code is safe"
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error analyzing code: {error_details}")
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


def play_game(robot_logic_a, robot_logic_b):
    controller = GameController(max_turn=100, x_max=9, y_max=7)
    robot1 = Robot("Robot A", 1, 3, robot_logic_a, controller)
    robot2 = Robot("Robot B", 7, 3, robot_logic_b, controller)
    controller.set_robots(robot1, robot2)
    winner, game_state = controller.game_loop()

    return winner, game_state


def game_state_download_button(game_state):
    # JSON文字列に変換
    json_str = json.dumps(game_state, indent=4)

    # JSONデータをバイナリに変換
    json_bytes = json_str.encode('utf-8')

    st.download_button(
        label="Download game_state.json",
        data=json_bytes,
        file_name="game_state.json",
        mime="application/json"
    )


def main():
    from robots.robot_03_random_walker import robot_logic as enemy_robot_logic
    st.title("Python Code Robot Battle")
    st.write("---")

    st.markdown("""
    PCRBにようこそ！  
    ロボットを制御するPythonスクリプトを投稿して、相手のロボットを倒すゲームです。  
    すぐ下のボタンからサンプルスクリプトがダウンロードできます。  
    詳しい使い方は左側のメニューにある「manual」を確認してください。  
    """)

    st.write("---")

    st.write("The sample is here")

    sample_file_path = "samples/sample_robot_logic_file.py"  # ダウンロードさせたいスクリプトのパス

    with open(sample_file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    st.download_button(
        label="Download sample robot logic file",
        data=file_content,
        file_name="sample_robot_logic_file.py",
        mime="text/plain"
    )

    st.write("---")

    uploaded_file = st.file_uploader("Upload a Python file with robot_logic function")

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
                    st.success("Function loaded successfully!")
                    winner, game_state = play_game(player_robot_logic, enemy_robot_logic)

                    if winner.name == "Robot A":
                        st.header(f"Congratulations on your win!")
                    else:
                        st.header(f"It's okay, you'll get them next time.")

                    game_state_download_button(game_state)

                    st_draw_board(game_state)

                else:
                    st.error("No function named `robot_logic` found in the uploaded file.")
            except Exception as e:
                error_details = traceback.format_exc()  # エラー詳細を取得
                print(f"Error processing the uploaded file:\n{error_details}")  # ターミナルに出力
                st.error(f"Error processing the uploaded file: {e}")  # Streamlit にエラーを表示


if __name__ == "__main__":
    main()
