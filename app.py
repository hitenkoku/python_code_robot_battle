import json
import streamlit as st

from pcrb.draw import draw_board


def main():
    # JSONファイルの読み込み
    with open('./game_state.json', 'r') as file:
        data = json.load(file)

    settings = data[0]['settings']
    max_turn = settings['max_turn']
    x_max = settings['x_max']
    y_max = settings['y_max']

    all_turn_data = data[1:]

    title_holder = st.empty()
    turn_holder = st.empty()
    board_holder = st.empty()

    turn_id = turn_holder.slider("TURN", 0, all_turn_data[-1]['turn'])
    turn_data = all_turn_data[turn_id]

    title = f"Turn {turn_data['turn']} - Action: {turn_data['action']['robot_name']} -> {turn_data['action']['action']}"
    title_holder.title(title)

    plt = draw_board(turn_data, x_max, y_max, title='', is_show=False)
    board_holder.pyplot(plt)


if __name__=='__main__':
    main()