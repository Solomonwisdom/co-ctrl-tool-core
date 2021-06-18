#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from copy import deepcopy

def generate_finfo(pos, ma, mb, cost, todolist, num_of_flight):
    finfo = []
    for i in range(num_of_flight):
        tmp = {}
        tmp["header"] = str(i) + "号无人机状态"
        tmp["key"] = str(i)
        tmp["id"] = "uav " + str(i)
        tmp["position"] = "{:.4f} , {:.4f}".format(pos[i][0] / 1000000, pos[i][1] / 1000000)
        if (len(ma[i]) + len(mb[i])) > 0:
            tmp["status"] = ["running", "processing"]
        else:
            tmp["status"] = ["finished", "success"]
        tmp["battery"] = "100 %"
        tmp["ma"] = ""
        for j in range(len(ma[i])):
            tmp["ma"] += str(ma[i][j][0])
            if j < len(ma[i]) - 1:
                tmp["ma"] += " , "
        tmp["mb"] = ""
        for j in range(len(mb[i])):
            tmp["mb"] += str(mb[i][j][0])
            if j < len(mb[i]) - 1:
                tmp["mb"] += " , "
        tmp["load"] = str(len(ma[i]) + len(mb[i]))
        tmp["cost"] = "{:.2f}".format(cost[i])
        tmp["list"] = []
        for j in range(len(todolist[i])):
            t = {}
            t["point"] = todolist[i][j]["point"]
            t["descrip"] = ""
            if "put" in todolist[i][j].keys():
                t["descrip"] += "put : "
                for k in range(len(todolist[i][j]["put"])):
                    t["descrip"] += str(todolist[i][j]["put"][k]) + " "
            if "get" in todolist[i][j].keys():
                t["descrip"] += "get : "
                for k in range(len(todolist[i][j]["get"])):
                    t["descrip"] += str(todolist[i][j]["get"][k]) + " "
            if "action" in todolist[i][j].keys():
                t["descrip"] += "action : "
                for k in range(len(todolist[i][j]["action"])):
                    t["descrip"] += todolist[i][j]["action"][k] + " "
            tmp["list"].append(t)
        finfo.append(deepcopy(tmp))
    return deepcopy(finfo)

def generate_minfo(ma, mb, m, num_of_flight):
    mi_tf = {}
    mi_ts = {}
    avail_m = []
    for i in range(num_of_flight):
        for j in range(len(ma[i])):
            mi_tf[ma[i][j][0]] = i
        for j in range(len(mb[i])):
            mi_ts[mb[i][j][0]] = i
            avail_m.append("m " + str(mb[i][j][0]))
    minfo = []
    for i in range(len(m)):
        tmp = {}
        tmp["header"] = str(m[i][0]) + "号任务状态"
        tmp["key"] = str(i)
        tmp["id"] = "m " + str(m[i][0])
        tmp["des"] = "from " + str(m[i][1]) + " to " + str(m[i][2])
        tmp["status"] = ["", ""]
        if m[i][0] in mi_tf.keys():
            tmp["status"][0] = " to finish" + " | " + "taken by uav " + str(mi_tf[m[i][0]])
            tmp["status"][1] = "processing"
        elif m[i][0] in mi_ts.keys():
            tmp["status"][0] = " to_start" + " | " + "taken by uav " + str(mi_ts[m[i][0]])
            tmp["status"][1] = "processing"
        else:
            tmp["status"][0] = " finished "
            tmp["status"][1] = "success"
        minfo.append(tmp)
    return deepcopy(minfo), deepcopy(avail_m)