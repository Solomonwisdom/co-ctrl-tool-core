#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
main.py
simulation module
'''
# import socket
import json
import os
# from multiprocessing import Proces

from copy import deepcopy
from flight import Flight
from output import *
from handle import *
import math

CUR_DIR=os.path.abspath(os.path.dirname(__file__)) + "/"


SPEED_OF_FLIGHT = 0.75

NUM_OF_FLIGHT = -1
NUM_OF_POINT = -1

POINT = {}
DIST = []
FLIGHT = {}

MISSION_ALL = []
MISSION_A = []
MISSION_B = []
TODO_LIST = []
POSITION = []
CURRENT_COST = []

def init_center():
    global NUM_OF_FLIGHT, MISSION_ALL, MISSION_A, MISSION_B, TODO_LIST, POSITION, CURRENT_COST
    f = open(CUR_DIR + "data/information.json")
    content = json.load(f)
    f.close()
    NUM_OF_FLIGHT = content[0]
    MISSION_ALL = content[1]
    MISSION_A = content[2]
    MISSION_B = content[3]
    TODO_LIST = content[4]
    POSITION = content[5]
    CURRENT_COST = content[6]
    with open(CUR_DIR + "MISSION_ALL.json", "w") as f:
        f.write(json.dumps(MISSION_ALL))
    with open(CUR_DIR + "MISSION_A.json", "w") as f:
        f.write(json.dumps(MISSION_A))
    with open(CUR_DIR + "MISSION_B.json", "w") as f:
        f.write(json.dumps(MISSION_B))
    with open(CUR_DIR + "TODO_LIST.json", "w") as f:
        f.write(json.dumps(TODO_LIST))
    with open(CUR_DIR + "POSITION.json", "w") as f:
        f.write(json.dumps(POSITION))
    with open(CUR_DIR + "CURRENT_COST.json", "w") as f:
        f.write(json.dumps(CURRENT_COST))
    

def initialize_point():
    global POINT, NUM_OF_POINT
    f = open(CUR_DIR + "data/point.txt")
    lines = f.read().splitlines()
    NUM_OF_POINT = len(lines)
    for line in lines:
        temp = line.split(" ")
        POINT[int(temp[0])] = [float(temp[1]), float(temp[2])]
    f.close()

def initialize_dist():
    global DIST
    DIST = [[float(0) for i in range(NUM_OF_POINT)] for j in range(NUM_OF_POINT)]
    f = open(CUR_DIR + "data/route.txt")
    lines = f.read().splitlines()
    for line in lines:
        temp = line.split(" ")
        DIST[int(temp[0])][int(temp[1])] = float(temp[2])
        DIST[int(temp[1])][int(temp[0])] = float(temp[2])
    f.close()

def initialize_flight():
    global FLIGHT
    for i in range(NUM_OF_FLIGHT):
        FLIGHT[i] = Flight(deepcopy(POINT), deepcopy(DIST), deepcopy(MISSION_A[i]), deepcopy(MISSION_B[i]))
        FLIGHT[i].update_from_center(deepcopy(MISSION_A[i]), deepcopy(MISSION_B[i]), deepcopy(TODO_LIST[i]))
    with open(CUR_DIR + "FLIGHT.json", "w") as f:
        f.write(json.dumps(FLIGHT))

def load_file():
    initialize_point()
    initialize_dist()
    initialize_flight()

def generate_distance(position):
    cost = {}
    # current point & N points --> N+1 * N+1
    len_of_content = NUM_OF_POINT + 1
    for i in range(NUM_OF_FLIGHT):
        content = [[float(0) for j in range(len_of_content)] for k in range(len_of_content)]
        # 0 vs 1-N
        for j in range(1, len_of_content):
            c = math.sqrt(pow(position[i][0] - POINT[j-1][0], 2) + pow(position[i][1] - POINT[j-1][1], 2)) / SPEED_OF_FLIGHT
            content[0][j] = c
            content[j][0] = c
        # 1-N * 1-N
        for j in range(1, len_of_content):
            for k in range(j+1, len_of_content):
                c = DIST[j-1][k-1] / SPEED_OF_FLIGHT
                content[j][k] = c
                content[k][j] = c
        cost[i] = content
    return deepcopy(cost)

def generate_cost_current(content, flight_id):
    # current todo_list = []
    if len(TODO_LIST[flight_id]) == 0:
        return 0.0
    else:
        # route time
        time_all = 0
        # mission time
        cost_all = 0
        for i in range(len(TODO_LIST[flight_id])):
            point_id = TODO_LIST[flight_id][i]["point"]
            if i == 0:
                # current position to point 0
                time_all += content[0][point_id + 1]
            else:
                # point i-1 to point i
                time_all += content[TODO_LIST[flight_id][i - 1]["point"] + 1][point_id + 1]
            # cost += flight_time * num_of_mission(finished now)
            if "put" in TODO_LIST[flight_id][i].keys():
                cost_all += time_all * len(TODO_LIST[flight_id][i]["put"])
        return cost_all

class flightDecode(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=dic2objhook)

def dic2objhook(dic):
    if isinstance(dic, dict):
        return Flight(dic['point'], dic['distance'], dic['postion'], dic['mission_a'], 
        dic['mission_b'], dic['route'], dic['route_done'], dic['todo_list'])
    return dic

init_center()
load_file()

def handle(event, context):
    tmp = event['data']
    if type(tmp)==bytes: 
        tmp = json.loads(tmp)
    if type(tmp) != dict:
        return "Error"
    input_from_ui = tmp
    print(input_from_ui)
    global TODO_LIST, MISSION_A, MISSION_B, POSITION, FLIGHT, CURRENT_COST, MISSION_ALL
    with open(CUR_DIR + "TODO_LIST.json", "r") as f:
        TODO_LIST = json.load(f)
    with open(CUR_DIR + "MISSION_A.json", "r") as f:
        MISSION_A = json.load(f)
    with open(CUR_DIR + "MISSION_B.json", "r") as f:
        MISSION_B = json.load(f)
    with open(CUR_DIR + "POSITION.json", "r") as f:
        POSITION = json.load(f)
    with open(CUR_DIR + "FLIGHT.json", "r") as f:
        FLIGHT = json.load(f, cls=flightDecode)
    with open(CUR_DIR + "CURRENT_COST.json", "r") as f:
        CURRENT_COST = json.load(f)
    with open(CUR_DIR + "MISSION_ALL.json", "r") as f:
        MISSION_ALL = json.load(f)
    if input_from_ui["type"] == 0:
        for i in range(NUM_OF_FLIGHT):
            POSITION[i] = FLIGHT[i].get_position(1)
            MISSION_A[i], MISSION_B[i], TODO_LIST[i] = FLIGHT[i].update_mission_todolist()
            FLIGHT[i].update_from_center(deepcopy(MISSION_A[i]), deepcopy(MISSION_B[i]), deepcopy(TODO_LIST[i]))
        cost = generate_distance(deepcopy(POSITION))
        for i in range(NUM_OF_FLIGHT):
            CURRENT_COST[i] = generate_cost_current(deepcopy(cost[i]), i)
            #print("n: {} | p: {} | a: {} | b: {} | t: {} | c: {}".format(n, POSITION[i], MISSION_A[i], MISSION_B[i], TODO_LIST[i], CURRENT_COST[i]))
        finfo = generate_finfo(deepcopy(POSITION), deepcopy(MISSION_A), deepcopy(MISSION_B), deepcopy(CURRENT_COST), deepcopy(TODO_LIST), NUM_OF_FLIGHT)
        minfo, avail_m = generate_minfo(deepcopy(MISSION_A), deepcopy(MISSION_B), deepcopy(MISSION_ALL), NUM_OF_FLIGHT)
        with open(CUR_DIR + "MISSION_A.json", "w") as f:
            f.write(json.dumps(MISSION_A))
        with open(CUR_DIR + "MISSION_B.json", "w") as f:
            f.write(json.dumps(MISSION_B))
        with open(CUR_DIR + "TODO_LIST.json", "w") as f:
            f.write(json.dumps(TODO_LIST))
        with open(CUR_DIR + "POSITION.json", "w") as f:
            f.write(json.dumps(POSITION))
        with open(CUR_DIR + "CURRENT_COST.json", "w") as f:
            f.write(json.dumps(CURRENT_COST))
        with open(CUR_DIR + "FLIGHT.json", "w") as f:
            f.write(json.dumps(FLIGHT.to_dict()))
        response_body = json.dumps({"todo_list": TODO_LIST, "position": POSITION, "flight_info": finfo, "mission_info": minfo, "avail_mission": avail_m})
        return response_body
    if input_from_ui["type"] == 1:
        for i in range(len(input_from_ui['flights'])):
            p_id = int(input_from_ui['flights'][i]['point_id'])
            if p_id < 0 or p_id >= NUM_OF_POINT:
                return json.dumps({"message": "地点信息配置错误"})
        message = "个体动作配置信息已送达"
        TODO_LIST = handle_flight_control(deepcopy(input_from_ui), deepcopy(TODO_LIST))
        for i in range(NUM_OF_FLIGHT):
            FLIGHT[i].update_from_center(deepcopy(MISSION_A[i]), deepcopy(MISSION_B[i]), deepcopy(TODO_LIST[i]))
        with open(CUR_DIR + "TODO_LIST.json", "w") as f:
            f.write(json.dumps(TODO_LIST))
        with open(CUR_DIR + "FLIGHT.json", "w") as f:
            f.write(json.dumps(FLIGHT.to_dict()))
        response_body = json.dumps({"message": message})
        return response_body
    if input_from_ui["type"] == 2:
        message = "任务调整信息已送达"
        cost = generate_distance(deepcopy(POSITION))
        TODO_LIST, MISSION_B = handle_mission_control(deepcopy(input_from_ui), deepcopy(TODO_LIST), deepcopy(MISSION_B), deepcopy(MISSION_ALL), deepcopy(cost))
        for i in range(NUM_OF_FLIGHT):
            FLIGHT[i].update_from_center(deepcopy(MISSION_A[i]), deepcopy(MISSION_B[i]), deepcopy(TODO_LIST[i]))
        with open(CUR_DIR + "MISSION_B.json", "w") as f:
            f.write(json.dumps(MISSION_B))
        with open(CUR_DIR + "TODO_LIST.json", "w") as f:
            f.write(json.dumps(TODO_LIST))
        with open(CUR_DIR + "FLIGHT.json", "w") as f:
            f.write(json.dumps(FLIGHT.to_dict()))
        response_body = json.dumps({"message": message})
        return response_body

