import random
from typing import List, Dict, Optional

class Character:
    def __init__(self, name: str, house: str, hp: int = 100):
        self.name = name
        self.house = house
        self.hp = hp
        self.max_hp = hp
        self.spells = {}
        self.equipment = {"wand": "Basic Oak Wand", "robe": "Student Robes"}
        self.inventory = []

    def learn_spell(self, spell_name: str, damage: int, description: str):
        self.spells[spell_name] = {"damage": damage, "description": description}
        print(f"{self.name} 学会了 {spell_name}!")

    def cast_spell(self, spell_name: str, target: 'Character') -> bool:
        if spell_name not in self.spells:
            print(f"{self.name} 不会 {spell_name}!")
            return False

        spell = self.spells[spell_name]
        damage = spell["damage"]
        # 5% 暴击率 (双倍伤害)
        is_critical = random.random() < 0.05
        actual_damage = damage * 2 if is_critical else damage

        target.hp -= actual_damage
        target.hp = max(0, target.hp)  # 确保生命值不低于0

        print(f"{self.name} 施放了 {spell_name}!")
        if is_critical:
            print("✨ 暴击！✨")
        print(f"{target.name} 受到了 {actual_damage} 点伤害！")
        print(f"{target.name} 的生命值: {target.hp}/{target.max_hp}")

        return True

    def heal(self, amount: int):
        self.hp += amount
        self.hp = min(self.max_hp, self.hp)
        print(f"{self.name} 恢复了 {amount} 点生命值！")
        print(f"当前生命值: {self.hp}/{self.max_hp}")

    def equip_item(self, item_type: str, item_name: str):
        self.equipment[item_type] = item_name
        print(f"{self.name} 装备了 {item_name} 作为 {item_type}!")

    def show_status(self):
        print(f"\n{self.name} ({self.house})")
        print(f"生命值: {self.hp}/{self.max_hp}")
        print("魔杖:", self.equipment["wand"])
        print("长袍:", self.equipment["robe"])
        print("\n已学会的咒语:")
        for spell, details in self.spells.items():
            print(f"- {spell}: {details['description']} (伤害: {details['damage']})")
        print("\n物品栏:", self.inventory)

class SpellBook:
    def __init__(self):
        self.spells = {
            "除你武器": {"damage": 15, "description": "缴械敌人"},
            "昏昏倒地": {"damage": 20, "description": "击昏敌人"},
            "火焰熊熊": {"damage": 25, "description": "发射火焰咒语"},
            "悬浮咒": {"damage": 10, "description": "举起并投掷物体"},
            "盔甲护身": {"damage": 0, "description": "防御攻击"},
            "神锋无影": {"damage": 40, "description": "黑魔法切割咒"},
            "愈合如初": {"damage": 0, "description": "治疗轻伤(自身)"},
            "飞来咒": {"damage": 5, "description": "召唤物品"},
        }

    def get_spell(self, spell_name: str) -> Optional[Dict]:
        return self.spells.get(spell_name)

    def list_spells(self) -> List[str]:
        return list(self.spells.keys())

class MagicItem:
    def __init__(self, name: str, effect: str, potency: int):
        self.name = name
        self.effect = effect
        self.potency = potency

    def use(self, target: Character) -> str:
        if self.effect == "heal":
            target.heal(self.potency)
            return f"{target.name} 使用了 {self.name} 并恢复了 {self.potency} 点生命值！"
        elif self.effect == "damage_boost":
            target.temp_damage_boost = self.potency
            return f"{target.name} 使用了 {self.name} 并获得了 +{self.potency} 点伤害加成，持续下一回合！"
        elif self.effect == "defense":
            target.temp_defense = self.potency
            return f"{target.name} 使用了 {self.name} 并获得了 +{self.potency} 点防御加成，持续下一回合！"
        return f"{self.name} 没有效果！"

class Game:
    def __init__(self):
        self.player = None
        self.enemies = []
        self.spell_book = SpellBook()
        self.locations = {
            "大礼堂": {"description": "霍格沃茨的主餐厅。"},
            "禁忌森林": {"description": "充满魔法生物的危险森林。"},
            "魁地奇球场": {"description": "霍格沃茨学院进行魁地奇比赛的地方。"},
            "图书馆": {"description": "拥有数千本魔法书籍和卷轴的地方。"},
            "地牢": {"description": "寒冷潮湿，斯莱特林公共休息室所在地。"}
        }
        self.current_location = "大礼堂"
        self.items = [
            MagicItem("治疗药水", "heal", 30),
            MagicItem("火焰药剂", "damage_boost", 15),
            MagicItem("护盾符咒", "defense", 20),
            MagicItem("福灵剂", "luck", 1),  # 幸运效果尚未实现
        ]

    def create_player(self, name: str, house: str):
        self.player = Character(name, house)
        print(f"欢迎，{name} 来自 {house} 学院！你在霍格沃茨的旅程开始了。")
        self.player.learn_spell("除你武器", 15, "缴械敌人")
        self.player.learn_spell("愈合如初", 0, "治疗轻伤(自身)")
        self.player.inventory.append(self.items[0])  # 开始游戏时获得一个治疗药水

    def generate_enemy(self) -> Character:
        enemy_names = ["德拉科·马尔福", "克拉布", "高尔", "贝拉特里克斯·莱斯特兰奇", "斯内普教授"]
        enemy_houses = ["斯莱特林", "斯莱特林", "斯莱特林", "斯莱特林", "斯莱特林"]  # 斯莱特林倾向！
        enemy_types = ["恶霸", "黑巫师", "狡猾的学生", "摄魂怪", "家养小精灵"]
        
        index = random.randint(0, len(enemy_names)-1)
        enemy = Character(enemy_names[index], enemy_houses[index])
        
        # 给敌人随机分配咒语
        spell_list = self.spell_book.list_spells()
        for _ in range(random.randint(2, 4)):
            spell_name = random.choice(spell_list)
            spell = self.spell_book.get_spell(spell_name)
            enemy.learn_spell(spell_name, spell["damage"], spell["description"])
        
        # 根据敌人类型设置生命值
        if enemy_types[index] == "摄魂怪":
            enemy.hp = 150
            enemy.max_hp = 150
        else:
            enemy.hp = random.randint(50, 100)
            enemy.max_hp = enemy.hp
        
        return enemy

    def explore(self):
        print(f"\n你当前位于 {self.current_location}。")
        print(self.locations[self.current_location]["description"])
        
        # 30% 的概率遇到敌人
        if random.random() < 0.3:
            enemy = self.generate_enemy()
            print(f"\n⚠️  你遇到了 {enemy.name} ({enemy.house})！")
            self.battle(enemy)
        else:
            # 有机会找到物品或学习新咒语
            if random.random() < 0.4:
                item = random.choice(self.items)
                self.player.inventory.append(item)
                print(f"\n🎉  你找到了一个 {item.name}！")
            elif random.random() < 0.2:
                new_spells = [s for s in self.spell_book.list_spells() if s not in self.player.spells]
                if new_spells:
                    spell_name = random.choice(new_spells)
                    spell = self.spell_book.get_spell(spell_name)
                    self.player.learn_spell(spell_name, spell["damage"], spell["description"])
                    print(f"\n📚  你找到了一本魔法卷轴并学会了 {spell_name}！")
        
        # 移动到随机位置
        locations = list(self.locations.keys())
        locations.remove(self.current_location)
        self.current_location = random.choice(locations)
        print(f"\n你朝着 {self.current_location} 前进...")

    def battle(self, enemy: Character):
        print("\n⚔️  战斗开始 ⚔️")
        enemy.show_status()
        
        while self.player.hp > 0 and enemy.hp > 0:
            print("\n--- 你的回合 ---")
            self.player.show_status()
            print("\n你想做什么？")
            print("1. 施放咒语")
            print("2. 使用物品")
            print("3. 查看状态")
            print("4. 逃跑")
            
            choice = input("\n输入选择 (1-4): ").strip()
            
            if choice == "1":
                # 列出咒语
                print("\n你的咒语:")
                for i, spell in enumerate(self.player.spells.keys(), 1):
                    print(f"{i}. {spell}")
                
                spell_choice = input("\n选择咒语 (1-" + str(len(self.player.spells)) + "): ").strip()
                try:
                    spell_index = int(spell_choice) - 1
                    if 0 <= spell_index < len(self.player.spells):
                        spell_name = list(self.player.spells.keys())[spell_index]
                        self.player.cast_spell(spell_name, enemy)
                    else:
                        print("无效的咒语选择！")
                        continue
                except ValueError:
                    print("无效的输入！")
                    continue
            elif choice == "2":
                if not self.player.inventory:
                    print("你没有物品！")
                    continue
                
                print("\n你的物品:")
                for i, item in enumerate(self.player.inventory, 1):
                    print(f"{i}. {item.name} ({item.effect})")
                
                item_choice = input("\n选择物品 (1-" + str(len(self.player.inventory)) + "): ").strip()
                try:
                    item_index = int(item_choice) - 1
                    if 0 <= item_index < len(self.player.inventory):
                        item = self.player.inventory.pop(item_index)
                        print(item.use(self.player))
                    else:
                        print("无效的物品选择！")
                        continue
                except ValueError:
                    print("无效的输入！")
                    continue
            elif choice == "3":
                self.player.show_status()
                continue
            elif choice == "4":
                # 50% 的逃跑成功率
                if random.random() < 0.5:
                    print("你成功逃脱了！")
                    return
                else:
                    print("你未能逃脱！")
            else:
                print("无效的选择！")
                continue
            
            # 敌人回合
            if enemy.hp > 0:
                print("\n--- 敌人回合 ---")
                # 10% 的概率敌人使用物品（如果他们有的话）
                if enemy.inventory and random.random() < 0.1:
                    item = enemy.inventory.pop(0)
                    print(f"{enemy.name} 使用了 {item.name}！")
                    item.use(enemy)
                else:
                    # 敌人选择随机咒语
                    spell_name = random.choice(list(enemy.spells.keys()))
                    enemy.cast_spell(spell_name, self.player)
        
        # 战斗结束
        if self.player.hp <= 0:
            print("\n💀  你被击败了！💀")
            print("游戏结束！")
            exit()
        else:
            print(f"\n🎉  你击败了 {enemy.name}！🎉")
            # 有机会获得战利品
            if random.random() < 0.6:
                item = random.choice(self.items)
                self.player.inventory.append(item)
                print(f"{enemy.name} 掉落了一个 {item.name}！")

    def start_game(self):
        print("=====================================")
        print("  🎮  哈利波特魔法游戏  🎮  ")
        print("=====================================")
        
        name = input("输入你的名字: ").strip()
        
        print("\n选择你的学院:")
        houses = ["格兰芬多", "赫奇帕奇", "拉文克劳", "斯莱特林"]
        for i, house in enumerate(houses, 1):
            print(f"{i}. {house}")
        
        house_choice = input("\n输入学院编号 (1-4): ").strip()
        try:
            house_index = int(house_choice) - 1
            if 0 <= house_index < len(houses):
                house = houses[house_index]
            else:
                print("无效的选择！默认选择格兰芬多。")
                house = "格兰芬多"
        except ValueError:
            print("无效的输入！默认选择格兰芬多。")
            house = "格兰芬多"
        
        self.create_player(name, house)
        
        print("\n📜 你在霍格沃茨的冒险开始了...")
        print("你知道基本的咒语并拥有一个治疗药水。")
        print("探索霍格沃茨，学习新咒语，与敌人战斗！")
        
        while True:
            print("\n\n你想做什么？")
            print("1. 探索霍格沃茨")
            print("2. 查看状态")
            print("3. 退出游戏")
            
            choice = input("\n输入选择 (1-3): ").strip()
            
            if choice == "1":
                self.explore()
            elif choice == "2":
                self.player.show_status()
            elif choice == "3":
                print("\n感谢游玩！🏰")
                break
            else:
                print("无效的选择！")

if __name__ == "__main__":
    game = Game()
    game.start_game()  