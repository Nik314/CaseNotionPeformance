from src.auxillary_methods import get_log_properties
from src.case_notion_specification import check_property, get_log_graph
from multiprocessing import Pool
import copy


def check_type(ot,log_graph,ocel,activity_type_relations,type_type_relation,performance_indicator,dis_property,
               additional,activities,object_types):

    local_start, expanded_nodes = {ot}, {ot}
    local_relations = {rel for rel in activity_type_relations | type_type_relation if rel[0] in local_start}
    local_result = check_property(ocel, log_graph, local_start, local_relations, performance_indicator,
                    additional, activities, object_types,dis_property)

    while True:

        available_nodes = set(
            sum([[rel[0], rel[1]] for rel in activity_type_relations | type_type_relation], [])) - expanded_nodes
        print(f"Potential Expansions Left For {ot}: {len(available_nodes)} @{local_result} Result")
        print(local_relations)
        investigation = [(node,check_property(ocel, log_graph, local_start, local_relations |
            {rel for rel in activity_type_relations | type_type_relation if rel[0] == node}, performance_indicator,
            additional, activities, object_types,dis_property)) for node in available_nodes]
        investigation = [(entry[0],entry[1] -local_result) for entry in investigation]
        if not investigation or max([entry[1] for entry in investigation]) < 0:
            break
        else:
            added_node = sorted([node for node in available_nodes if (node, max([entry[1]
                        for entry in investigation])) in investigation])[0]
            expanded_nodes.add(added_node)
            local_relations = local_relations | {rel for rel in activity_type_relations | type_type_relation if
                        rel[0] == added_node}

        local_result = check_property(ocel, log_graph, ot, local_relations, performance_indicator, additional,
                                          activities, object_types, dis_property)
    print(f"{ot} Done @{local_result} Result!")
    return local_start,local_relations,local_result



def get_optimized_case_notion_from_framework(ocel, dis_property, performance_indicator, additional):

    activity_type_relations,type_type_relation,activities,object_types,divergence = get_log_properties(ocel)
    best_result, best_start_type, best_relations = 0,None,set()
    log_graph = get_log_graph(ocel)

    inputs = [(ot,copy.deepcopy(log_graph),copy.deepcopy(ocel),activity_type_relations,type_type_relation,
               performance_indicator,dis_property,additional,activities,object_types) for ot in object_types]
    with Pool(len(object_types)) as pool:
        results = pool.starmap(check_type,inputs)

    for local_start,local_relations,local_result in results:
        print("Result For ", local_start)
        print(local_relations)
        print(local_result)
        print("------------------------------------")
        if local_result > best_result:
            best_result = local_result
            best_start_type = local_start
            best_relations = local_relations

    print("Best Total Result:")
    print(best_result)
    print(best_start_type)
    print(best_relations)
    return best_result,best_start_type,best_relations



def get_traditional_case_notion(activity_type_relation, type_type_relation, object_types, activities):
    return [({ot}, {(ot,a) for a in activities
        if (ot,a) in activity_type_relation}) for ot in object_types]

def get_connected_case_notion(activity_type_relation, type_type_relation, object_types, activities):
    return [(object_types, activity_type_relation | type_type_relation)]

def get_advanced_case_notion(activity_type_relation, type_type_relation, object_types, activities,divergence):
    result = []

    for start in object_types:

        spec = set()

        new_relations = {(ot,a) for (ot,a) in activity_type_relation if ot == start}
        new_activities = set(sum([[a,b] for a,b in new_relations],[])) & activities
        new_types = {(a,ot) for (a,ot) in activity_type_relation if a in new_activities}
        spec = spec | new_relations | new_types

        while True:

            new_relations = {(ot, a) for (ot, a) in activity_type_relation if
                any((b,ot) in spec and ((ot,a) not in divergence or (b,ot) not in divergence) for b in activities)}
            new_relations = new_relations - spec
            new_activities = set(sum([[a,b] for a,b in new_relations],[])) & activities
            new_types = {(a, ot) for (a, ot) in activity_type_relation if a in new_activities}
            new_types = new_types -spec
            if new_types or new_activities:
                spec = spec | new_relations | new_types
            else:
                break

        result.append(({start},spec))
    return result
