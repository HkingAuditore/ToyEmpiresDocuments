from signal import signal


def lerp(min,max,v):
    return min + (max - min) * v

def get_coefficient(min,max,v):
    a = lerp(0,1,(v-min)/(max-min)) if min != max else 0
    if v < 0:
        return -(1-abs(a))
    else:
        return abs(a)

blue_soldier = 10
blue_worker = 5
blue_building = 2
blue_tech = 3

red_soldier = 3
red_worker = 3
red_building = 1
red_tech = 10

ai_soldier_gap = red_soldier - blue_soldier
ai_worker_gap = red_worker- blue_worker
ai_building_gap = red_building - blue_building
ai_tech_gap = red_tech - blue_tech

min_gap = min(ai_soldier_gap,ai_worker_gap,ai_building_gap,ai_tech_gap)
max_gap = max(ai_soldier_gap,ai_worker_gap,ai_building_gap,ai_tech_gap)

soldier_coefficient = get_coefficient(min_gap,max_gap,ai_soldier_gap)
worker_coefficient = get_coefficient(min_gap,max_gap,ai_worker_gap)
building_coefficient = get_coefficient(min_gap,max_gap,ai_building_gap)
tech_coefficient = get_coefficient(min_gap,max_gap,ai_tech_gap)

print("soldier :" + str(soldier_coefficient))
print("worker :" + str(worker_coefficient))
print("building :" + str(building_coefficient))
print("tech :" + str(tech_coefficient))
