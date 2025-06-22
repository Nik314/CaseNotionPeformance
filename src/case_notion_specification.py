import math
import networkx


def get_log_graph(ocel):

    lookup = ocel.objects.set_index("ocel:oid")["ocel:type"].to_dict()
    ocel.o2o["ocel:oid"] = ocel.o2o["ocel:oid"].apply(lambda entry: (lookup[entry], entry))
    ocel.o2o["ocel:oid_2"] = ocel.o2o["ocel:oid_2"].apply(lambda entry: (lookup[entry], entry))

    unique_relations = set(zip(ocel.o2o["ocel:oid"],ocel.o2o["ocel:oid_2"]))
    unique_relations |= set(zip(ocel.o2o["ocel:oid_2"],ocel.o2o["ocel:oid"]))
    unique_relations |= set(zip(zip(ocel.relations["ocel:activity"].to_list(), ocel.relations["ocel:eid"].to_list()),
            zip(ocel.relations["ocel:type"].to_list(), ocel.relations["ocel:oid"].to_list())))
    unique_relations |= set(zip(zip(ocel.relations["ocel:type"].to_list(), ocel.relations["ocel:oid"].to_list()),
                               zip(ocel.relations["ocel:activity"].to_list(), ocel.relations["ocel:eid"].to_list())))
    return networkx.from_edgelist(unique_relations)



def generate_cases(log_graph,starting_types,relations,activities,types):
    local_graph = networkx.from_edgelist([edge for edge in log_graph.edges if (edge[0][0],edge[1][0]) in relations])
    cases, start_nodes = [], [node for node in log_graph.nodes if node[0] in starting_types]
    while start_nodes:
        local_start = start_nodes[0]
        if not local_start in local_graph.nodes:
            cases.append((set(),{local_start[1]}))
            start_nodes.remove(local_start)
        else:
            reachable_nodes = networkx.descendants(local_graph,source=local_start)
            events = {node[1] for node in reachable_nodes if node[0] in activities}
            objects = {node[1] for node in reachable_nodes if node[0] in types} | {local_start[1]}
            cases.append((events,objects))
            start_nodes = [node for node in start_nodes if node[1] not in objects]
    return cases





def check_variance(ocel,log_graph, starting_types, specification, performance_indicator, additional,activities, types,rel):
    case_list = generate_cases(log_graph,starting_types,specification,activities,types)
    values = [performance_indicator(ocel,case,additional) for case in case_list]
    distribution = {v:values.count(v) for v in set(values)}
    average = sum( ((v * p) / len(distribution)) for v,p in distribution.items())
    variance = sum( (average - v) * (average - v) * p for v,p in distribution.items())
    return (rel,(math.sqrt(variance) / average) if average else 0.0)
