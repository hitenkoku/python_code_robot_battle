import streamlit as st
import ast
import traceback
import json

from pages.drawer import st_draw_board
from controller import GameController
from robot import Robot

# 許可する関数とモジュール
ALLOWED_FUNCTIONS = {"robot_logic"}
ALLOWED_MODULES = ["random", "math"]
GAME_STATE_FILE = "./game_state.json"  # 既存の game_state.json ファイル


# ----------------------------- セキュリティ関連ユーティリティ -----------------------------

def is_safe_code(file_content: str) -> tuple[bool, str]:
    """アップロードされたコードを AST 解析し、安全性を判定する。"""
    try:
        tree = ast.parse(file_content)

        for node in ast.walk(tree):
            # インポートのチェック
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name not in ALLOWED_MODULES:
                        return False, f"許可されていないモジュールのインポート: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module not in ALLOWED_MODULES:
                    return False, f"許可されていないモジュールのインポート: {node.module}"

            # 許可していない関数定義を禁止
            if isinstance(node, ast.FunctionDef):
                if node.name not in ALLOWED_FUNCTIONS:
                    return False, f"許可されていない関数定義: {node.name}"

            # 危険な関数呼び出しの検出
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval"}:
                    return False, f"禁止されている関数呼び出し: {node.func.id}"

        return True, "安全なコードです"
    except Exception as e:
        error_details = traceback.format_exc()
        print(error_details)
        return False, f"コード解析中にエラーが発生しました: {e}"


# ----------------------------- モジュールロード -----------------------------

def load_player_module(file_content: str):
    """サンドボックス環境でアップロードされたモジュールをロードする。"""
    import importlib.util
    import textwrap

    file_path = "./uploaded_logic_safe.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(file_content))

    spec = importlib.util.spec_from_file_location("robot_logic_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, "robot_logic", None)


# ----------------------------- ゲーム実行 -----------------------------

def play_game(robot_logic_a, robot_logic_b):
    controller = GameController(max_turn=100, x_max=9, y_max=7)
    robot1 = Robot("Robot A", 1, 3, robot_logic_a, controller)
    robot2 = Robot("Robot B", 7, 3, robot_logic_b, controller)
    controller.set_robots(robot1, robot2)
    winner, game_state = controller.game_loop()
    return winner, game_state


def game_state_download_button(game_state: dict) -> None:
    """game_state を JSON としてダウンロード可能にするボタンを描画。"""
    json_bytes = json.dumps(game_state, ensure_ascii=False, indent=4).encode("utf-8")
    st.download_button(
        label="game_state.json をダウンロード",
        data=json_bytes,
        file_name="game_state.json",
        mime="application/json",
    )


# ----------------------------- メイン UI -----------------------------

def main() -> None:
    from robots.robot_03_random_walker import robot_logic as enemy_robot_logic

    st.set_page_config(page_title="PCRB", page_icon="🤖", layout="centered")

    # --- ヘッダー ---
    st.title("🤖 PCRB - Python Code Robot Battle")
    st.caption("Python スクリプトでロボットを動かして対戦しよう！")
    st.write("---")

    # --- 概要セクション ---
    st.markdown(
        """
        **PCRB** へようこそ！  
        あなたが作成した Python スクリプトでロボットを操作し、対戦相手を倒すゲームです。  
        まずはサンプルスクリプトをダウンロードして、自分好みに改造してみましょう。  
        詳しい遊び方は左側サイドバーの **Manual** ページを参照してください。
        """
    )

    st.write("---")

    # --- 2 カラムレイアウト: ダウンロード & アップロード ---
    col_dl, col_ul = st.columns(2)

    # サンプルダウンロード
    with col_dl:
        st.subheader("サンプルスクリプト")
        sample_file_path = "samples/sample_robot_logic_file.py"
        with open(sample_file_path, "r", encoding="utf-8") as file:
            st.download_button(
                label="サンプルをダウンロード",
                data=file.read(),
                file_name="sample_robot_logic_file.py",
                mime="text/plain",
            )

    # スクリプトアップロード
    with col_ul:
        st.subheader("スクリプトをアップロード")
        uploaded_file = st.file_uploader(
            "robot_logic を含む Python ファイル (.py) を選択", type=["py"]
        )

    # --- アップロード後の処理 ---
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")

        with st.expander("アップロードされたコードを表示", expanded=False):
            st.code(file_content, language="python")

        # コード安全性チェック
        is_safe, message = is_safe_code(file_content)

        if not is_safe:
            st.error(f"⚠️ アップロードされたコードに問題があります: {message}")
            return

        # robot_logic をロード
        try:
            player_robot_logic = load_player_module(file_content)
            if player_robot_logic is None:
                st.error("`robot_logic` 関数が見つかりませんでした。ファイルを確認してください。")
                return
        except Exception as e:
            st.error(f"モジュールロード中にエラーが発生しました: {e}")
            return

        # --- ゲーム開始 ---
        if 'winner' not in st.session_state:
            st.success("✅ コードの読み込みに成功しました！ 対戦を開始します。")
            st.session_state.winner, st.session_state.game_state = play_game(player_robot_logic, enemy_robot_logic)

        if st.session_state.winner.name == "Robot A":
            if 'balloons_shown' not in st.session_state or not st.session_state.balloons_shown:
                st.balloons()
                st.session_state.balloons_shown = True
            st.header("🎉 勝利おめでとうございます！")
        else:
            st.header("🤖 残念！ 次の挑戦をお待ちしています。")

        # ゲーム結果ダウンロード
        game_state_download_button(st.session_state.game_state)

        # 盤面描画
        st_draw_board(st.session_state.game_state)


if __name__ == "__main__":
    main()
