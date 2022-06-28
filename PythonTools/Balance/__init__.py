import math
import re

import pandas as pd
import tabulate

# s = """ID:4000
# Name:Cavalryman
# Attack:15
# Defence:5
# Speed:0.2
# MaxHP:125
# AttackCD:1
# FindRange:0.6
# AttackRange:0.025"""
#
# unit_id = re.search('(?<=ID:)[0-9]+', s).group(0)
# name = re.search('(?<=Name:).+',s).group(0)
# attack =re.search('(?<=Attack:)[0-9]+', s).group(0)
# defence =re.search('(?<=Defence:)[0-9]+', s).group(0)
# speed =re.search('(?<=Speed:)[0-9\.]+', s).group(0)
# hp =re.search('(?<=MaxHP:)[0-9]+', s).group(0)
# attack_cd =re.search('(?<=AttackCD:)[0-9]+', s).group(0)
# find_range =re.search('(?<=FindRange:)[0-9\.]+', s).group(0)
# attack_range =re.search('(?<=AttackRange:)[0-9\.]+', s).group(0)
#
# df = pd.DataFrame([])
# print(','.join([unit_id,name,attack,defence,speed,hp,attack_cd,find_range,attack_range]))

import matplotlib.pyplot as plt
import numpy as np

e_attack = 13.42857143
e_defence = 3.071428571
e_speed = 0.071428571
e_max_hp = 135.3571429
e_attack_cd = 2.842857143
e_find_range = 0.335714286
e_attack_range = 0.171071429
e_cost_gold = 18.42857143
e_cost_time = 7.535714286


def str_to_unit_data(s):
    l = s.split('	')
    return {
        'UnitID'     : l[0],
        'Name'       : l[1],
        'Attack'     : float(l[2]),
        'Defence'    : float(l[3]),
        'Speed'      : float(l[4]),
        'MaxHP'      : float(l[5]),
        'AttackCD'   : float(l[6]),
        'FindRange'  : float(l[7]),
        'AttackRange': float(l[8]),
        'CostGold'   : float(l[9]),
        'CostTime'   : float(l[10])
    }


class SoldierUnit:
    """

    """
    def __init__(self, unit_id='', name='', attack=0, defence=0, speed=0, max_hp=0, attack_cd=0, find_range=0,
                 attack_range=0, cost_gold=0, cost_time=0, **kwargs):
        data = kwargs.get('data')
        if data is not None:
            d = str_to_unit_data(data)
            self.unit_id = d['UnitID']
            self.name = d['Name']
            self.attack = d['Attack']
            self.defence = d['Defence']
            self.speed = d['Speed']
            self.max_hp = d['MaxHP']
            self.attack_cd = d['AttackCD']
            self.find_range = d['FindRange']
            self.attack_range = d['AttackRange']
            self.cost_gold = d['CostGold']
            self.cost_time = d['CostTime']
        else:
            self.unit_id = unit_id
            self.name = name
            self.attack = attack
            self.defence = defence
            self.speed = speed
            self.max_hp = max_hp
            self.attack_cd = attack_cd
            self.find_range = find_range
            self.attack_range = attack_range
            self.cost_gold = cost_gold
            self.cost_time = cost_time

    def calculate_damage_expect(self):
        e0 = (e_find_range - e_attack_range - self.find_range + self.attack_range) / (e_speed + self.speed)
        e1 = (self.max_hp * e_attack_cd * (e_attack + self.defence)) / (e_attack ** 2)
        e2 = (self.attack ** 2) / ((self.attack + e_defence) * self.attack_cd)
        return (e0 + e1) * e2

    def calculate_cost_performance_ratio(self):
        r = self.calculate_damage_expect()
        return r / (self.cost_time * self.cost_gold)

    def get_group_dps(self, k, enemy_defence = 0):
        if enemy_defence == 0 :
            return (k * self.attack * self.attack) /( (self.attack + e_defence) * self.attack_cd)
        else:
            return (k * self.attack * self.attack) / ((self.attack + enemy_defence) * self.attack_cd)


    def get_group_dps_new(self, k, enemy = None, enemy_count = 1):
        """
        :type enemy: SoldierUnit
        """
        ts = self.get_group_stay_time(k,enemy = enemy,enemy_count=enemy_count)
        move_time = (self.attack_range - enemy.attack_range) / (
            enemy.speed if ((self.attack_range - enemy.attack_range) > 0) else self.speed)
        move_time_damage = (move_time) * (
            self.get_group_dps(k, enemy.defence) if move_time > 0 else enemy.get_group_dps(enemy_count, self.defence))
        move_time_lose = move_time_damage / (self.max_hp if move_time < 0 else enemy.max_hp)
        # move_time_lose_u = np.array([(x if x < 0 else 0) for x in move_time_lose])
        # move_time_lose_e = np.array([(x if x > 0 else 0) for x in move_time_lose])
        new_k = k + move_time_lose
        new_enemy_count = enemy_count - move_time_lose

        tn0 = self.get_group_stay_time(new_k,enemy,new_enemy_count)
        a = self.get_group_dps(1,enemy.defence) / self.max_hp
        print('a',a)
        b = enemy.get_group_dps(1,self.defence)/ enemy.max_hp
        print('b', b)
        e0 = (1 / (np.sqrt(a * b))) * np.log(np.sqrt((b/a) * (enemy_count**2) - k**2))
        e1 = (1 / (np.sqrt(a * b))) * np.log(k + np.sqrt((b/a)*enemy_count**2))
        tn1 = -e0 + e1
        tn = []
        for i in range(len(tn1)):
            if math.isnan(tn1[i]):
                tn.append(tn0[i])
            else:
                tn.append(tn1[i])
        print('tn',tn1)

        return self.get_group_dps(new_k,enemy.defence) * (tn0/ts)



    def get_group_dps_average(self, k, enemy=None, enemy_count=1):
        """
        :type enemy: SoldierUnit
        """
        move_time = (self.attack_range - enemy.attack_range) / (enemy.speed if ((self.attack_range - enemy.attack_range) > 0) else self.speed)
        move_time_damage = (move_time) * (self.get_group_dps(k,enemy.defence) if move_time > 0 else enemy.get_group_dps(enemy_count,self.defence))
        move_time_lose = move_time_damage / (self.max_hp if move_time > 0 else enemy.max_hp)

        d0 = self.get_group_dps(k, enemy_defence=enemy.defence)
        # print('d0',d0)
        # print(enemy_count)
        d1 = self.get_group_dps_new(k, enemy=enemy,enemy_count=enemy_count)
        # print(d1)
        print('d1', d1)
        return d1

    def get_group_stay_time(self, k, enemy=None, enemy_count=None):
        """
        :type enemy: SoldierUnit
        """
        if enemy is not None:
            e0 = (enemy.find_range - enemy.attack_range) / ((enemy.speed if ((self.attack_range - enemy.attack_range) > 0) else self.speed))
            enemy_dps = enemy.get_group_dps(k=enemy_count,enemy_defence=self.defence)
            return e0 + ((k * self.max_hp) / enemy_dps)
        else:
            e0 = (e_find_range - e_attack_range) / (e_speed + self.speed)
            return e0 + k * self.max_hp / 12.01

    def get_group_damage(self, k, enemy=None, enemy_count=None):
        """
                :type enemy: SoldierUnit
        """
        if enemy is not None:
            e0 = k * (((self.attack_range - enemy.attack_range) / (enemy.speed if ((self.attack_range - enemy.attack_range) > 0) else self.speed)) + (k * self.max_hp)/(enemy.get_group_dps_average(k=enemy_count,enemy=self,enemy_count=k))) * self.attack * self.attack
            e1 = (k * (k-1) * self.attack * self.attack * self.max_hp) / (2 * enemy.get_group_dps_average(k=enemy_count,enemy=self,enemy_count=k))
            e2=(self.attack + enemy.defence)*self.attack_cd
            return (e0 - e1) / e2
        else:
            e0 = k * ((self.attack_range - e_attack_range) / ((e_speed if ((self.attack_range - e_attack_range) > 0) else self.speed))+ (k * self.max_hp*e_attack_cd*(e_attack+self.defence))/(e_attack*e_attack)) * self.attack * self.attack
            e1 = (k * (k-1) * self.attack * self.attack * self.max_hp) / (2 * 12.01)
            e2=(self.attack + e_defence)*self.attack_cd
            return (e0 - e1) / e2


df = pd.read_csv('data.csv')
unit_list = {}
for i in df.index:
    unit_list[df['UnitID'][i]] = SoldierUnit(unit_id        =df['UnitID'][i],
                                             name           =df['Name'][i],
                                             attack         =float(df['Attack'][i]),
                                             defence        =float(df['Defence'][i]),
                                             speed          =float(df['Speed'][i]),
                                             max_hp         =float(df['MaxHP'][i]),
                                             attack_cd      =float(df['AttackCD'][i]),
                                             find_range     =float(df['FindRange'][i]),
                                             attack_range   =float(df['AttackRange'][i]),
                                             cost_gold      =float(df['CostGold'][i]),
                                             cost_time      =float(df['CostTime'][i]))


# print(Militiaman.get_group_damage(5))
# print(Archer.get_group_damage(5))
# print(SanYanChong.get_group_damage(3))
# print(Swordsman.get_group_damage(1))


# Import our modules that we are using


# Create the vectors X and Y
num = 10
x = np.array(range(1,num*3))
enemy_id = 3000
def show_graph(u,u_name):
    plt.plot(x, u.get_group_damage(x, enemy=unit_list[enemy_id], enemy_count=num)/unit_list[enemy_id].max_hp, label=u_name)

def show_damage_plot(u,u_count,e,e_count,label=''):
    """

    :type e: SoldierUnit
    :type u: SoldierUnit
    """

    ts = u.get_group_stay_time(k=u_count,enemy=e,enemy_count=e_count)
    tn = ts + 10

    t = np.linspace(0, 35, 1000)
    a0 = ((e_count * e.attack **2 * tn) / ((e.attack + u.defence) * e.attack_cd))
    a = (a0 - u_count * u.max_hp) / (tn ** 2)
    b = (-e_count * e.attack ** 2) / ((e.attack + u.defence) * e.attack_cd)
    c = u_count * u.max_hp

    plt.plot(t, np.floor(np.ceil((a * t**2 + b *t + c)/ 100.0)) * 100,label=label)
    plt.xlim([0, int(tn * 1.2)])
    plt.ylim([0, int(c * 1.2)])

    # plt.plot(x, u.get_group_damage(x, enemy=unit_list[2001], enemy_count=10), label=u_name)

# Create the plot
# for key in unit_list:
#     if key == 6000:
#         continue
#     show_graph(unit_list[key],unit_list[key].name)
show_graph(unit_list[2000],unit_list[2000].name)
show_graph(unit_list[2002],unit_list[2002].name)
show_graph(unit_list[2001],unit_list[2001].name)
show_graph(unit_list[3000],unit_list[3000].name)
show_graph(unit_list[3003],unit_list[3003].name)
show_graph(unit_list[5000],unit_list[5000].name)
show_graph(unit_list[5001],unit_list[5001].name)
show_graph(unit_list[4000],unit_list[4000].name)
show_graph(unit_list[5003],unit_list[5003].name)
show_graph(unit_list[5004],unit_list[5004].name)

# show_damage_plot(unit_list[2001],5,unit_list[2001],5,label = unit_list[2001].name)

# Add a title
plt.title('Group Damange --- ' + str(num)+': '+unit_list[enemy_id].name)

# Add X and y Label
plt.xlabel('Group Size')
plt.ylabel('Expected Reward')

# Add a grid
plt.grid(alpha=.4,linestyle='--')
plt.ylim([0, int(num* 3)])
plt.axhline(y=num, color='r', linestyle='--')
# Add a Legend
plt.legend()
# plt.yscale("logit")
# Show the plot
plt.show()
