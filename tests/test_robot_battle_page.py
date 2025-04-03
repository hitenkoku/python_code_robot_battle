import sys
import importlib.util

sys.path.append('./')

from pcrb.pages import robot_battle_page


def test():
    python_files = robot_battle_page.get_robot_files()
    python_files = sorted(python_files)
    assert len(python_files) > 1

    for python_file_path in python_files:
        module_name = python_file_path[:-3]
        module = importlib.import_module(f"robots.{module_name}")
        if hasattr(module, "robot_logic"):
            enemy_robot_logic = getattr(module, "robot_logic")
            winner, game_state = robot_battle_page.play_game(enemy_robot_logic, enemy_robot_logic)
            print(f"Winner: {winner.name}")
            print(f"Game State Type: {type(game_state)}")
            assert winner.name in ["Robot A", "Robot B"]
            assert isinstance(game_state, list)

