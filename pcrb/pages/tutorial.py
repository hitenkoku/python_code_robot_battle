import streamlit as st

INTRODUCTION_DOCUMENT = '''
## どんなゲーム？

このゲームは、ロボット同士が戦うターン制の戦略ゲームです。
- 相手のロボットを倒すことが目的です。
- ゲームは、ターン制で進行し、各ターンごとにロボットの行動が決定されます。

## プレイヤーのすること

プレイヤーは、ロボットの行動を決定するためのロジックをPythonで実装します。
- ロジックは、ロボットの状態や相手の位置に基づいて行動を決定します。
- プレイヤーは、ロジックを実装したPythonファイルをアップロードし、ゲームを開始します。

## ゲームの流れ

1. プレイヤーは、ロジックを実装したPythonファイルをアップロードします。
2. ゲームが開始され、ロボットの行動がターンごとに決定されます。
3. 各ターンごとに、ロボットの状態や相手の位置が更新されます。
5. ゲームは、相手のロボットのHPが0になるまで続きます。

## ロジックの実装

ロジックは、`robot_logic`という関数を実装することで決定されます。
- この関数は、ロボットの状態や相手の位置を引数として受け取り、ロボットの行動を決定します。
- ロジックは、ロボットのHPやSP、相手の位置に基づいて行動を決定します。
- ロジックは、ロボットの行動を決定するための条件分岐やループを使用することができます。

'''


TUTORIAL_DOCUMENT = '''
## 1. Homeページからサンプルの入手

「Download sample robot logic file」を選択して、
下記のようなロジックファイルのサンプルを入手する

```python
# 必須のrobot_logic関数を定義
def robot_logic(robot, game_info, memos):
    # スタミナが少ない場合は休み、それ以外は敵に近づいて攻撃
    enemy_position = game_info['enemy_position']
    if robot.sp < 20:
        return "rest"
    elif abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1]) == 1:
        return "attack"
    else:
        if robot.position[0] < enemy_position[0]:
            return "right"
        elif robot.position[0] > enemy_position[0]:
            return "left"
        elif robot.position[1] < enemy_position[1]:
            return "down"
        else:
            return "up"
```

## 2. サンプルファイルを編集

ご自身のエディタを利用してサンプルファイルを編集する
例えば、「相手との距離が１マスで自分のHPが50以下のときに防御するロジックを追加する」と次のようになる。

```python
# 必須のrobot_logic関数を定義
def robot_logic(robot, game_info, memos):
    # スタミナが少ない場合は休み、それ以外は敵に近づいて攻撃
    enemy_position = game_info['enemy_position']
    if robot.sp < 20:
        return "rest"
    elif abs(robot.position[0] - enemy_position[0]) + abs(robot.position[1] - enemy_position[1]) == 1:
        if robot.sp <= 50: # 追加箇所
            return "defend" # 追加箇所
        return "attack"
    else:
        if robot.position[0] < enemy_position[0]:
            return "right"
        elif robot.position[0] > enemy_position[0]:
            return "left"
        elif robot.position[1] < enemy_position[1]:
            return "down"
        else:
            return "up"
```

## 3. ロジックファイルをアップロード

Homeページの「Upload a Python file with robot_logic function」蘭の「Drag and drop file here」に
作成したロジックが記載されているPythonファイルをアップロードする。

## 4. 対戦ログの確認

「3. ロジックファイルをアップロード」後に、
Homeページの「Download game_state.json」を選択し、対戦ログを確認します。

## 5. ロジックを改良して、再度アップロード

対戦ログを元にロジックを改良して、再度アップロードします。

'''


def main():
    st.title("Introduction")
    st.markdown(INTRODUCTION_DOCUMENT)
    
    st.title("Tutorial")
    st.markdown(TUTORIAL_DOCUMENT)


if __name__ == '__main__':
    main()