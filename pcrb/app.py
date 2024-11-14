import json
import streamlit as st

import sys
sys.path.append('./pcrb')


def main():
    from draw import draw_board

    uploaded_holder = st.empty()
    title_holder = st.empty()
    turn_holder = st.empty()
    board_holder = st.empty()
    robots_holder = st.empty()
    memo_holder = st.empty()

    uploaded_file = uploaded_holder.file_uploader("Upload game_state.json", type="json")

    if uploaded_file is not None:
        data = json.load(uploaded_file)

        settings = data[0]['settings']
        max_turn = settings['max_turn']
        x_max = settings['x_max']
        y_max = settings['y_max']

        memo_holder.write(max_turn)

        all_turn_data = data[1:]

        turn_id = turn_holder.slider("TURN", 0, all_turn_data[-1]['turn'])
        turn_data = all_turn_data[turn_id]

        _action = turn_data['action']
        _robots = turn_data['robots']

        robots_holder.write(_robots)

        title = f"Turn {turn_data['turn']} - Action: {_action['robot_name']} -> {_action['action']}"
        title_holder.title(title)

        plt = draw_board(turn_data, x_max, y_max, title='', is_show=False)
        board_holder.pyplot(plt)


if __name__=='__main__':
    main()