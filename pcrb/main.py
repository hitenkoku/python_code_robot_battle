import random


class Robot:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.hp = 100
        self.sp = 50  # スタミナポイント（SP）の初期値
        self.attack_power = 20
        self.move_cost = 5  # 移動時のスタミナ消費量
        self.attack_cost = 10  # 攻撃時のスタミナ消費量
        self.evade_recovery = 15  # 回避時のスタミナ回復量

    def move(self, dx, dy):
        if self.sp >= self.move_cost:  # スタミナが足りるかチェック
            if abs(dx) <= 1 and abs(dy) <= 1 and (dx == 0 or dy == 0):
                self.x += dx
                self.y += dy
                self.sp -= self.move_cost  # スタミナを消費
                print(f"{self.name} moved to ({self.x}, {self.y}) and used {self.move_cost} SP. Remaining SP: {self.sp}")
            else:
                print(f"{self.name} tried to move to an invalid location.")
        else:
            print(f"{self.name} does not have enough SP to move!")

    def attack(self, target_x, target_y, other_robot):
        if self.sp >= self.attack_cost:  # スタミナが足りるかチェック
            if abs(self.x - target_x) + abs(self.y - target_y) == 1:
                if other_robot.x == target_x and other_robot.y == target_y:
                    damage = self.attack_power + random.randint(-5, 5)
                    other_robot.hp -= damage
                    self.sp -= self.attack_cost  # スタミナを消費
                    print(f"{self.name} attacks {other_robot.name} at ({target_x}, {target_y}) for {damage} damage and used {self.attack_cost} SP.")
                    print(f"{other_robot.name}'s HP is now {other_robot.hp}. Remaining SP: {self.sp}")
                else:
                    print(f"{self.name} attacks empty space at ({target_x}, {target_y}) and misses!")
            else:
                print(f"{self.name} tried to attack a non-adjacent location at ({target_x}, {target_y}).")
        else:
            print(f"{self.name} does not have enough SP to attack!")

    def evade(self):
        self.sp += self.evade_recovery  # スタミナを回復
        print(f"{self.name} evades and recovers {self.evade_recovery} SP. Total SP: {self.sp}")

    def is_alive(self):
        return self.hp > 0


def player_robot_logic(robot, enemy):
    # サンプルロジック：スタミナが少なければ回避、それ以外は敵に近づいて攻撃
    if robot.sp < 20:
        robot.evade()
    elif abs(robot.x - enemy.x) + abs(robot.y - enemy.y) == 1:
        robot.attack(enemy.x, enemy.y, enemy)
    else:
        if robot.x < enemy.x:
            robot.move(1, 0)
        elif robot.x > enemy.x:
            robot.move(-1, 0)
        elif robot.y < enemy.y:
            robot.move(0, 1)
        elif robot.y > enemy.y:
            robot.move(0, -1)


def game_loop(robot1, robot2):
    turn = 0
    while robot1.is_alive() and robot2.is_alive():
        print(f"\n--- Turn {turn} ---")
        if turn % 2 == 0:
            player_robot_logic(robot1, robot2)
        else:
            player_robot_logic(robot2, robot1)
        turn += 1
    if robot1.is_alive():
        print(f"\n{robot1.name} wins!")
    else:
        print(f"\n{robot2.name} wins!")


def main():
    # ロボットの初期化
    robot1 = Robot("Robot A", 0, 0)
    robot2 = Robot("Robot B", 3, 3)
    # ゲームの開始
    game_loop(robot1, robot2)


if __name__ == "__main__":
    main()