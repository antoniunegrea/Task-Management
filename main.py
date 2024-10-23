from controller import *


def run():
    activities = read_activities()
    act_dict, rev_act_dict = map_activities(activities)
    graph = graph_from_activities(activities, act_dict)
    sorted = TopoSort(graph)
    if sorted is None:
        print("the graph is not a DAG")
        return
    print("the order of activities must be: ", end='')
    for a in sorted:
        print(f"{rev_act_dict[a]} -> ", end='')
    print("Done")
    table = scheduling(sorted, activities, act_dict, rev_act_dict)
    print(table)
    critical_act = critical_activities(sorted, activities, rev_act_dict)
    print("Critical activities: ", end='')
    for a in critical_act:
        print(a, end=';')


if __name__ == "__main__":
    run()
