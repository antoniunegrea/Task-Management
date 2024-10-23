from graph import Graph
from activity import Activity
import texttable


def read_activities():
    """
    n activities
    activity duration prerequisites
    :return a list of activities
    """
    activities = []
    with open("activities.txt", "rt") as f:
        line = f.readline()
        n = int(line.strip().split()[0])
        for _ in range(n):
            line = f.readline().strip().split()
            name = line[0]
            duration = line[1]
            prerequisites = []
            for i in range(2, len(line)):
                prerequisites.append(line[i])
            activities.append(Activity(name, duration, prerequisites))
    return activities


def map_activities(activities):
    """
    maps the activities to a dictionary and a reverse dictionary
    :param activities: a list of activities
    :return: a dictionary and a reverse dictionary
    """
    d = {}
    rev_d = {}
    for i in range(len(activities)):
        d[activities[i].getName()] = i
        rev_d[i] = activities[i].getName()
    return d, rev_d


def graph_from_activities(activities, act_dict):
    """
    creates a DAG from the activities
    :param activities: a list of activities
    :param act_dict: a dictionary mapping the activities to their index
    :return: a graph
    """
    graph = Graph()
    for i in range(len(act_dict)):
        graph.add_vertex(i)
    for a in activities:
        for p in a.getPrerequisites():
            graph.add_edge(act_dict[p], act_dict[a.getName()], 0)
    return graph


def TopoSortDFS(g, x, sorted, fullyProcessed, inProcess):
    """
    :param g: a graph
    :param x: a vertice
    :param sorted: a list of vertices sorted topologically
    :param fullyProcessed: a set of fully processed vertices
    :param inProcess: a set of vertices in process
    :return:    True if the graph is a DAG,
                False otherwise
    """
    inProcess.add(x)
    for y in g.parse_nin(x):
        if y in inProcess:
            return False
        elif y not in fullyProcessed:
            ok = TopoSortDFS(g, y, sorted, fullyProcessed, inProcess)
            if not ok:
                return False
    inProcess.remove(x)
    sorted.append(x)
    fullyProcessed.add(x)
    return True


def TopoSort(graph):
    """
    this function sorts the vertices of a graph topologically
    :param graph: a graph
    :return: a list of vertices sorted topologically
    """
    sorted = []
    fullyProcessed = set()
    inProcess = set()
    for x in graph.parse_vertices():
        if x not in fullyProcessed:
            ok = TopoSortDFS(graph, x, sorted, fullyProcessed, inProcess)
            if not ok:
                return None
    return sorted


def early_scheduling(sorted, activities, act_dict):
    """
    computes the early scheduling for the activities
    :param sorted: a list of activities sorted topologically
    :param activities: a list of activities
    :param act_dict: a dictionary mapping the activities to their index
    :return: -
    """
    for i in sorted:
        d = 0
        for p in activities[i].getPrerequisites():
            d += int(activities[act_dict[p]].getDuration())
        activities[i].setEarly(d)


def late_scheduling(sorted, activities, total_duration):
    """
    computes the late scheduling for the activities
    :param sorted: a list of activities sorted topologically
    :param activities: a list of activities
    :param total_duration: int - the total duration of the project
    :return: -
    """
    t = total_duration
    for i in range(len(sorted) - 1, -1, -1):

        if total_duration == 0:
            total_duration = t
        d = int(activities[sorted[i]].getDuration())
        total_duration -= d
        activities[sorted[i]].setLate(total_duration)


def get_total_duration(sorted, activities, act_dict):
    """
    computes the total duration of the project
    :param sorted: a list of activities sorted topologically
    :param activities: a list of activities
    :param act_dict: a dictionary mapping the activities to their index
    :return: int - the total duration of the project
    """
    total_duration = 0
    for i in sorted:
        d = 0
        for p in activities[i].getPrerequisites():
            d += int(activities[act_dict[p]].getDuration())
        d += int(activities[i].getDuration())
        if d > total_duration:
            total_duration = d
    return total_duration


def scheduling(sorted, activities, act_dict, rev_act_dict):
    """
    computes the scheduling for the activities
    :param sorted: a list of activities sorted topologically
    :param activities: a list of activities
    :param act_dict: a dictionary mapping the activities to their index
    :param rev_act_dict: a reverse dictionary mapping the activities to their index
    :return: a table with the scheduling
    """
    total_duration = get_total_duration(sorted, activities, act_dict)
    print(f"The total duration for the project is {total_duration} days")
    early_scheduling(sorted, activities, act_dict)
    late_scheduling(sorted, activities, total_duration)
    table = texttable.Texttable()
    table.header(["Activity", "Prerequisites", "Duration", "Early", "Late"])
    for v in sorted:
        a = activities[v]
        prereq_str = ""
        for p in a.getPrerequisites():
            prereq_str += p + "; "
        table.add_row([a.getName(), prereq_str, a.getDuration(), a.getEarly(), a.getLate()])
    return table.draw()


def critical_activities(sorted, activities, rev_act_dict):
    """
    computes the critical activities
    :param sorted:
    :param activities:
    :param rev_act_dict:
    :return: a list of critical activities
    """
    critical = []
    for i in sorted:
        if activities[i].getEarly() == activities[i].getLate():
            critical.append(rev_act_dict[i])
    return critical
