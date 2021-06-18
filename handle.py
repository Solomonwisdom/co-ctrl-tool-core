#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from copy import deepcopy

MAX_WEIGHT = 100000000

def handle_flight_control(input, todo_list):
    for i in range(len(input["flights"])):
        flight_id = int(input["flights"][i]["flight_id"][4:])
        point_id = int(input["flights"][i]["point_id"])
        action = input["flights"][i]["action"]
        insert = int(input["flights"][i]["insert"])
        if len(todo_list[flight_id]) == 0:
            todo_list[flight_id].append({"point" : point_id, "action" : [action]})
        elif insert >= len(todo_list[flight_id]):
            if point_id != todo_list[flight_id][-1]["point"]:
                todo_list[flight_id].append({"point" : point_id, "action" : [action]})
            else:
                if "action" not in todo_list[flight_id][-1].keys():
                    todo_list[flight_id][-1]["action"] = [action]
                else:
                    todo_list[flight_id][-1]["action"].append(action)
        elif insert == 0:
            if point_id != todo_list[flight_id][0]["point"]:
                todo_list[flight_id] = todo_list[flight_id][0:insert] + [{"point" : point_id, "action" : [action]}] + todo_list[flight_id][insert:]
            else:
                if "action" not in todo_list[flight_id][0].keys():
                    todo_list[flight_id][0]["action"] = [action]
                else:
                    todo_list[flight_id][0]["action"].append(action)
        else:
            if point_id == todo_list[flight_id][insert-1]["point"]:
                if "action" not in todo_list[flight_id][insert-1].keys():
                    todo_list[flight_id][insert-1]["action"] = [action]
                else:
                    todo_list[flight_id][insert-1]["action"].append(action)
            elif point_id == todo_list[flight_id][insert]["point"]:
                if "action" not in todo_list[flight_id][insert].keys():
                    todo_list[flight_id][insert]["action"] = [action]
                else:
                    todo_list[flight_id][insert]["action"].append(action)
            else:
                todo_list[flight_id] = todo_list[flight_id][0:insert] + [{"point": point_id, "action": [action]}] + todo_list[flight_id][insert:]

    return deepcopy(todo_list)

def generate_cost(cost, todolist):
    if len(todolist) == 0:
        return 0.0
    else:
        # route time
        time_all = 0
        # mission time
        cost_all = 0
        for i in range(len(todolist)):
            point_id = todolist[i]["point"]
            if i == 0:
                # current position to point 0
                time_all += cost[0][point_id + 1]
            else:
                # point i-1 to point i
                time_all += cost[todolist[i - 1]["point"] + 1][point_id + 1]
            # cost += flight_time * num_of_mission(finished now)
            if "put" in todolist[i].keys():
                cost_all += time_all * len(todolist[i]["put"])
        return cost_all

# merge point
def generate_new_todolist(td):
    tmp = []
    for i in range(len(td)):
        # start
        if i == 0:
            tmp.append(deepcopy(td[i]))
        else:
            # new point
            if td[i]["point"] != tmp[-1]["point"]:
                tmp.append(deepcopy(td[i]))
            # merge point
            else:
                if "put" in td[i].keys():
                    if "put" not in tmp[-1].keys():
                        tmp[-1]["put"] = []
                    tmp[-1]["put"] += td[i]["put"]
                if "get" in td[i].keys():
                    if "get" not in tmp[-1].keys():
                        tmp[-1]["get"] = []
                    tmp[-1]["get"] += td[i]["get"]
    return deepcopy(tmp)

def handle_mission_control(input, tdl, mb, mall, cost):
    for i in range(len(input["missions"])):
        mission_id = int(input["missions"][i]["mission_id"][2:])
        mission = mall[mission_id]
        pt = -1
        for j in range(len(mb)):
            if mission in mb[j]:
                pt = j
                break
        else:
            continue
        mb[pt].remove(mission)
        r = []
        for j in range(len(tdl[pt])):
            if tdl[pt][j]["point"] == mission[1]:
                if "get" in tdl[pt][j].keys():
                    if mission_id in tdl[pt][j]["get"]:
                        tdl[pt][j]["get"].remove(mission_id)
                        if len(tdl[pt][j]["get"]) == 0:
                            tdl[pt][j].pop("get")
            elif tdl[pt][j]["point"] == mission[2]:
                if "put" in tdl[pt][j].keys():
                    if mission_id in tdl[pt][j]["put"]:
                        tdl[pt][j]["put"].remove(mission_id)
                        if len(tdl[pt][j]["put"]) == 0:
                            tdl[pt][j].pop("put")
            if "put" not in tdl[pt][j].keys() and "get" not in tdl[pt][j].keys() and "action" not in tdl[pt][j].keys():
                r.append(tdl[pt][j])
        for j in range(len(r)):
            tdl[pt].remove(r[j])

        if input["missions"][i]["action"] == "change":
            to_id = int(input["missions"][i]["to_id"][4:])
            mb[to_id].append(mission)
            min_cost = MAX_WEIGHT
            temp_todo = []
            for j in range(0, len(tdl[to_id]) + 1):
                for k in range(j, len(tdl[to_id]) + 1):
                    new_todo = tdl[to_id][0:j] + [{"point" : mission[1], "get" : [mission[0]]}] + tdl[to_id][j:k] + [{"point" : mission[2], "put" : [mission[0]]}] + tdl[to_id][k:]
                    new_cost = generate_cost(deepcopy(cost[to_id]), deepcopy(new_todo))
                    if new_cost < min_cost:
                        min_cost = new_cost
                        temp_todo = deepcopy(new_todo)
            tdl[to_id] = generate_new_todolist(deepcopy(temp_todo))

    return deepcopy(tdl), deepcopy(mb)