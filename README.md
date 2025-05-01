# python_code_robot_battle

## 概要
python_code_robot_battle は、ロボットの行動ロジックを作成し、仮想バトルを行うためのアプリケーションです。  
Streamlit を利用して操作します。

## Streamlit Community Cloud

クラウドでアプリを動作させる場合、以下の URL からアクセスしてください

https://python-code-robot-battle.streamlit.app/

## ローカルで動かす場合


1. `./pcrb` ディレクトリにある `app.py` を実行して、ロボットのバトルアプリをローカルで起動します。
    ```bash
    streamlit run ./pcrb/app.py
    ```
2. プレイヤーは `robot_logic` 関数を作成し、ロボットの行動を制御します。

## robot_logic 関数について
- 引数:
  - `robot`: ロボットの現在のステータスや位置情報を表すオブジェクト
  - `game_info`: 敵の位置やゲームの状態を表す辞書

- 例:
  ```python
  def robot_logic(robot, game_info):
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

## ライセンス
このプロジェクトは MIT ライセンスの下で提供されます。  
今後変更される可能性があります。

## 開発者向け情報

### コントリビュート
1. フォークして新しいブランチを作成します。
2. 新しい機能やバグ修正を行い、プルリクエストを作成してください。
3. コードレビュー後、マージされます。

### バージョン情報

- Python バージョン: 3.9 以上
- Streamlit バージョン: 1.40.0 以上
- PyTest バージョン: 8.3.4 以上

### テスト方法

PyTest を利用してテストしてください。

- 簡単な使い方
  1. テストコードを `tests` ディレクトリに保存
  2. テストコードにテスト内容を記載した `test` 関数を作成
  3. `python -m pytest` コマンドでテストを実行
