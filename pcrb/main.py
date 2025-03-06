import json


class Robot:
    def __init__(self, name, x, y, robot_logic_function, controller):
        self._name = name
        self._x = x
        self._y = y
        self._hp = 100
        self._sp = 50
        self._attack_power = 20
        self._attack_cost = 10
        self._move_cost = 5
        self._rest_recovery = 15
        self._stun_duration = 0  # ロボットがスタンしている時間

        # 防御関連
        self._defense_mode = False
        self._defense_reduction = 0.5  # 防御中のダメージ軽減率
        self._defense_cost = 10  # 防御のコスト

        # 遠距離攻撃関連
        self._ranged_attack_cost = 15  # 遠距離攻撃のコスト
        self._ranged_attack_power = 15  # 遠距離攻撃の威力

        # パリィ関連
        self._parry_mode = False  # パリィ中かどうか
        self._parry_cooldown = 0  # パリィのクールタイム
        self._parry_cooldown_time = 2  # クールタイムの初期値(何ターン後に使えるか)
        self._parry_cost = 15  # パリィのコスト

        self.robot_logic = robot_logic_function
        self.controller = controller

    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        return self._hp

    @property
    def sp(self):
        return self._sp

    @property
    def position(self):
        return self._x, self._y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def defense_mode(self):
        return self._defense_mode

    @property
    def parry_mode(self):
        return self._parry_mode

    @property
    def stun_duration(self):
        return self._stun_duration

    def receive_attack(self, damage):
        """攻撃を受ける
        :param damage: 攻撃のダメージ量
        """
        if self._defense_mode:
            damage *= self._defense_reduction
        self._hp -= max(damage, 0)
        if self._hp <= 0:
            print(f"{self._name} has been destroyed!")
        return damage

    def move(self, direction, turn):
        if self._sp < self._move_cost:
            self.controller.log_action(turn, f"{self._name} does not have enough SP to move!")
            return

        # 移動先の座標を計算
        if direction == "up":
            new_x, new_y = self._x, max(0, self._y - 1)
        elif direction == "down":
            new_x, new_y = self._x, min(self.controller.y_max - 1, self._y + 1)
        elif direction == "left":
            new_x, new_y = max(0, self._x - 1), self._y
        elif direction == "right":
            new_x, new_y = min(self.controller.x_max - 1, self._x + 1), self._y
        else:
            self.controller.log_action(turn, f"{self._name} tried to move in an invalid direction.")
            return

        # 移動先に他のロボットがいないかチェック
        if self.controller.is_position_occupied(new_x, new_y):
            self.controller.log_action(
                turn, f"{self._name} tried to move to ({new_x}, {new_y}), but the path is blocked.")
        else:
            self._x, self._y = new_x, new_y
            self._sp -= self._move_cost
            self.controller.log_action(
                turn, f"{self._name} moved {direction} to ({self._x}, {self._y}), HP: {self._hp}, SP: {self._sp}")

    def attack(self, other_robot, turn):
        if self._sp >= self._attack_cost:
            if abs(self._x - other_robot.x) + abs(self._y - other_robot.y) == 1:
                if other_robot.parry_mode:
                    self.stun(1)
                else:
                    damage = other_robot.receive_attack(self._attack_power)
                    self._sp -= self._attack_cost
                    self.controller.log_action(turn, f"{self._name} attacks {other_robot.name} at ({other_robot.x}, {other_robot.y}) for {damage} damage.")
            else:
                self.controller.log_action(turn, f"{self._name} tried to attack a non-adjacent location.")
        else:
            self.controller.log_action(turn, f"{self._name} does not have enough SP to attack!")

    def defend(self, turn):
        if self._sp >= self._defense_cost:
            self._sp -= self._defense_cost
            self._defense_mode = True
            self.controller.log_action(turn, f"{self._name} is now in defense mode, reducing incoming damage.")
        else:
            self.controller.log_action(turn, f"{self._name} does not have enough SP to defend!")

    def start_turn(self):
        """ターン開始時にロボットの状態を更新"""
        if self._defense_mode:
            print(f"{self._name} ends defense mode.")
            self._defense_mode = False

        if self._stun_duration > 0:
            self._stun_duration -= 1
            print(f"{self._name} is stunned. (duration={self._stun_duration})")

        if self._parry_mode:
            print(f"{self._name} ends parry mode.")
            self._parry_mode = False

        if self._parry_cooldown > 0:
            self._parry_cooldown -= 1

    def ranged_attack(self, other_robot, turn):
        distance = abs(self._x - other_robot.x) + abs(self._y - other_robot.y)
        if distance == 2:
            if self._sp >= self._ranged_attack_cost:
                self._sp -= self._ranged_attack_cost
                damage = other_robot.receive_attack(self._ranged_attack_power)
                self.controller.log_action(turn, f"{self._name} performs a ranged attack on {other_robot.name} for {damage} damage!")
            else:
                self.controller.log_action(turn, f"{self._name} does not have enough SP to perform a ranged attack!")
        else:
            self.controller.log_action(turn, f"{self._name} cannot perform a ranged attack on {other_robot.name} due to incorrect distance (distance: {distance}).")

    def rest(self, turn):
        self._sp += self._rest_recovery
        self.controller.log_action(turn, f"{self._name} rests and recovers {self._rest_recovery} SP. Total SP: {self._sp}")

    def parry(self, turn):
        """パリィを実行する関数"""
        if self._sp >= self._parry_cost and not self._parry_mode and self._parry_cooldown == 0:
            self._parry_mode = True
            self._sp -= self._parry_cost
            self._parry_cooldown = self._parry_cooldown_time
            self.controller.log_action(turn, f"{self._name} started parrying!")
        elif self._parry_cooldown > 0:
            self.controller.log_action(turn, f"{self._name}'s parry is on cooldown.")
        else:
            self.controller.log_action(turn, f"{self._name} doesn't have enough SP.")

    def stun(self, duration):
        """ロボットをスタン状態にする
        :param duration: スタンの持続時間
        """
        self._stun_duration = duration
        print(f"{self._name} was stunned.")

    def is_alive(self):
        return self._hp > 0

    def status(self):
        print(f"{self._name}: HP={self._hp}, SP={self._sp}, Position=({self._x}, {self._y})")


def is_valid_memo(memo):
    if not isinstance(memo, dict):
        return False

    for key, value in memo.items():
        # キーが文字列かを確認
        if not isinstance(key, str):
            return False
        # バリューが数値（int, float）、None、または文字列かを確認
        if not (isinstance(value, (int, float, str)) or value is None):
            return False

    return True


class GameController:
    def __init__(
            self, max_turn=100, x_max=9, y_max=9, robot1_initial_position=None, robot2_initial_position=None):
        self.robot1 = None
        self.robot2 = None
        self.memos1 = None
        self.memos2 = None
        self.turn = 0
        self.max_turn = max_turn
        self.x_max = x_max
        self.y_max = y_max
        self.robot1_initial_position = {'x': 1, 'y': 3} if robot1_initial_position is None else robot1_initial_position
        self.robot2_initial_position = {'x': 7, 'y': 3} if robot2_initial_position is None else robot2_initial_position
        self.log_file = open("game_log.txt", "w")
        self.game_state_file = open("game_state.json", "w")

        self.game_state = [{
            'settings': {
                'max_turn': self.max_turn,
                'x_max': self.x_max,
                'y_max': self.y_max,
            }
        }]

    def set_robots(self, robot1, robot2):
        self.robot1 = robot1
        self.robot2 = robot2
        self.memos1 = []
        self.memos2 = []

    def log_action(self, turn, message):
        print(message)
        self.log_file.write(f"Turn {turn}: {message}\n")

    def is_position_occupied(self, x, y):
        return self.robot1.position == (x, y) or self.robot2.position == (x, y)

    @staticmethod
    def adjust_action_for_robot1(action):
        return action

    @staticmethod
    def adjust_action_for_robot2(action):
        if action == "up":
            action = 'down'
        if action == "up":
            action = 'down'
        if action == "left":
            action = 'right'
        if action == "right":
            action = 'left'
        return action

    def run_logic(self, robot):
        enemy = self.robot1 if robot == self.robot1 else self.robot2
        memos = self.memos1 if robot == self.robot1 else self.memos2
        adjust_action = self.adjust_action_for_robot1 if robot == self.robot1 else self.adjust_action_for_robot2

        game_info = {
            'enemy_hp': enemy.hp,
            'enemy_position': enemy.position
        }
        response = robot.robot_logic(robot, game_info, memos)

        if isinstance(response, str):
            action = response
            memo = {}
        elif isinstance(response, (list, tuple)) and len(response) == 2:
            action, memo = response
            assert is_valid_memo(memo)
        else:
            assert False

        action = adjust_action(action)

        if robot == self.robot1:
            self.memos1.append(memo)
        else:
            self.memos2.append(memo)

        if robot.stun_duration > 0:
            return "stun"

        robot.start_turn()
        if action == "rest":
            robot.rest(self.turn)
        elif action == "attack":
            robot.attack(enemy, self.turn)
        elif action == "defend":
            robot.defend(self.turn)
        elif action in ["up", "down", "left", "right"]:
            robot.move(action, self.turn)
        elif action == "ranged_attack":
            robot.ranged_attack(enemy, self.turn)
        elif action == "parry":
            robot.parry(self.turn)
        else:
            raise ValueError("Unexpected robot action detected!")

        return action

    def save_game_state(self, robot_name, action):
        # 現在のターンのゲーム状態を辞書形式で記録
        state = {
            "turn": self.turn,
            "robots": [
                {
                    "name": self.robot1.name,
                    "position": self.robot1.position,
                    "hp": self.robot1.hp,
                    "sp": self.robot1.sp,
                    "defense_mode": self.robot1.defense_mode,
                },
                {
                    "name": self.robot2.name,
                    "position": self.robot2.position,
                    "hp": self.robot2.hp,
                    "sp": self.robot2.sp,
                    "defense_mode": self.robot2.defense_mode,
                }
            ],
            'action': {
                'robot_name': robot_name,
                'action': action
            }
        }
        self.game_state.append(state)

    def game_loop(self):
        while self.robot1.is_alive() and self.robot2.is_alive() and self.turn < self.max_turn:
            current_robot = self.robot1 if self.turn % 2 == 0 else self.robot2
            self.log_action(self.turn, f"\n--- Turn {self.turn} : {current_robot.name} turn ---")
            action = self.run_logic(current_robot)
            self.save_game_state(current_robot.name, action)  # 各ターンごとの状態を保存
            self.log_action(self.turn, f" - {self.robot1.name} : HP: {self.robot1.hp}, SP: {self.robot1.sp}")
            self.log_action(self.turn, f" - {self.robot2.name} : HP: {self.robot2.hp}, SP: {self.robot2.sp}")
            self.turn += 1

        winner = self.robot1 if self.robot1.hp > self.robot2.hp else self.robot2
        self.log_action(self.turn, f"\n{winner.name} wins!")
        self.log_file.close()

        json.dump(self.game_state, self.game_state_file, indent=4)
        self.game_state_file.close()
        return winner, self.game_state


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


def main():
    controller = GameController()

    _x = controller.robot1_initial_position['x']
    _y = controller.robot1_initial_position['y']
    robot1 = Robot("Robot A", _x, _y, robot_logic, controller)

    _x = controller.robot2_initial_position['x']
    _y = controller.robot2_initial_position['y']
    robot2 = Robot("Robot B", _x, _y, robot_logic, controller)

    controller.set_robots(robot1, robot2)
    controller.game_loop()


if __name__ == "__main__":
    main()
