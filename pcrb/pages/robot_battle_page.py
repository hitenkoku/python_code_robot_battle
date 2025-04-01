import streamlit as st
import importlib.util
import os
import traceback
import pandas as pd

import sys
sys.path.append('./pcrb')

from app import is_safe_code
from app import load_player_module
from app import play_game

ROBOTS_DIR = "./pcrb/robots"


def upload_and_display_file():
    """ファイルをアップロードし、内容を表示する"""
    uploaded_file = st.file_uploader("ロジックファイルをアップロードしてください", type=["py"])
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        st.subheader("Uploaded Code")
        st.code(file_content, language="python")
        return file_content
    return None


def validate_code(file_content):
    """コードの安全性をチェックする"""
    is_safe, message = is_safe_code(file_content)
    if not is_safe:
        st.error(f"Unsafe code detected: {message}")
        return False
    return True


def load_robot_logic(file_content):
    """アップロードされたロジックをロードする"""
    try:
        return load_player_module(file_content)
    except Exception as e:
        st.error(f"Error loading the uploaded file: {traceback.format_exc()}")
        return None


def get_robot_files():
    """ロボットディレクトリ内のPythonファイルを取得する"""
    return [f for f in os.listdir(ROBOTS_DIR) if f.endswith(".py") and f != "__init__.py"]


def battle_with_saved_robots(player_robot_logic):
    """保存されているロボットと対戦する"""
    python_files = sorted(get_robot_files())
    results = []

    for python_file_path in python_files:
        module_name = python_file_path[:-3]
        try:
            module = importlib.import_module(f"robots.{module_name}")
            if hasattr(module, "robot_logic"):
                enemy_robot_logic = getattr(module, "robot_logic")
                winner, game_state = play_game(player_robot_logic, enemy_robot_logic)
                result, color = determine_result(winner)
                results.append((module_name, f'<span style="color:{color}; font-weight:bold;">{result}</span>'))
        except Exception as e:
            st.warning(f"Error loading robot module {module_name}: {traceback.format_exc()}")
            continue

    return results


def determine_result(winner):
    """勝敗結果を判定する"""
    if winner.name == "Robot A":
        return "勝利 🏆", "green"
    elif winner.name == "Robot B":
        return "敗北 ❌", "red"
    else:
        return "引き分け ⚖️", "gray"


def display_results(results):
    """対戦結果を表示する"""
    st.subheader("🤖 対戦結果")
    if results:
        df = pd.DataFrame(results, columns=["対戦相手", "結果"])
        df["結果"] = df["結果"].apply(lambda x: f'<p style="text-align:center;">{x}</p>')  # 結果を中央寄せ
        st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("対戦相手が見つかりませんでした。")


def main():
    st.title("Robot Battle Page")
    file_content = upload_and_display_file()

    if file_content and validate_code(file_content):
        player_robot_logic = load_robot_logic(file_content)
        if player_robot_logic:
            results = battle_with_saved_robots(player_robot_logic)
            display_results(results)
        else:
            st.error("No function named `robot_logic` found in the uploaded file.")


if __name__ == "__main__":
    main()