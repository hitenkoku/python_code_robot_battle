import json
import streamlit as st

import sys
sys.path.append('./pcrb')

from draw import draw_board


def st_draw_board(data):
    title_holder = st.empty()
    turn_slider_holder = st.empty()
    turn_button_holder = st.empty()
    board_holder = st.empty()
    robots_holder = st.empty()
    memo_holder = st.empty()

    settings = data[0]['settings']
    max_turn = settings['max_turn']
    x_max = settings['x_max']
    y_max = settings['y_max']

    memo_holder.write(max_turn)

    all_turn_data = data[1:]

    # Initialize session state for the current turn
    if 'current_turn' not in st.session_state:
        st.session_state.current_turn = 0

    # Slider for selecting turn
    turn_id = turn_slider_holder.slider("TURN", 0, all_turn_data[-1]['turn'], st.session_state.current_turn)
    st.session_state.current_turn = turn_id

    # Next and Back buttons
    col1, col2, _ = turn_button_holder.columns([1, 1, 2])
    with col1:
        if st.button("Back"):
            if st.session_state.current_turn > 0:
                st.session_state.current_turn -= 1

    with col2:
        if st.button("Next"):
            if st.session_state.current_turn < all_turn_data[-1]['turn']:
                st.session_state.current_turn += 1

    # Sync slider with button actions
    turn_id = st.session_state.current_turn

    turn_data = all_turn_data[turn_id]

    _action = turn_data['action']
    _robots = turn_data['robots']

    robots_holder.write(_robots)

    title = f"Turn {turn_data['turn']} - Action: {_action['robot_name']} -> {_action['action']}"
    title_holder.header(title)

    plt = draw_board(turn_data, x_max, y_max, title='', is_show=False)
    board_holder.pyplot(plt)


def main():
    st.title("Python Code Robot Battle")
    uploaded_file = st.file_uploader("Upload game_state.json", type="json")

    if uploaded_file is not None:
        data = json.load(uploaded_file)
        st_draw_board(data)


if __name__ == '__main__':
    main()