def is_adjacent(actor, target):
    return abs(actor.x - target.x) + abs(actor.y - target.y) == 1


def is_valid_memo(memo):
    if not isinstance(memo, dict):
        print("Memo is not a dictionary.")
        return False

    for key, value in memo.items():
        # キーが文字列かを確認
        if not isinstance(key, str):
            print(f"Key '{key}' is not a string.")
            return False
        # バリューが数値（int, float）、None、または文字列かを確認
        if not (isinstance(value, (int, float, str)) or value is None):
            print(f"Value '{value}' is not a valid type (int, float, str, or None).")
            return False

    return True