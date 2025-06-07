from src.auxillary_methods import get_log_properties
from src.case_notion_specification import check_variance



def get_optimized_case_notion_event_based(ocel, performance_indicator, additional):

    (activity_type_relations,type_type_relation,activities,
        object_types,o2o,e2o,lookup_dict_types, lookup_dict_activities,divergence)= get_log_properties(ocel)
    best_result, best_start_type, best_relations = 0,None,set()

    case_notions = (get_traditional_case_notion(activity_type_relations,type_type_relation,object_types,activities) +
            get_connected_case_notion(activity_type_relations,type_type_relation,object_types,activities) +
            get_advanced_case_notion(activity_type_relations, type_type_relation, object_types, activities,divergence))

    for ot,spec in case_notions:
        print("Checking Case Notion")
        print("Starting Type ", ot)
        print("Specification ", spec)
        new_variance = check_variance(ocel,ot,spec,performance_indicator,
            o2o,e2o,lookup_dict_types,lookup_dict_activities,additional)
        print("Relative Variance Observed: ", new_variance)
        if new_variance > best_result:
            print("New Optimum Found")
            best_result = new_variance
            best_start_type = ot
            best_relations = spec

    print("Best Total Result:")
    print(best_result)
    print(best_start_type)
    print(best_relations)
    return best_result,best_start_type,best_relations





def get_traditional_case_notion(activity_type_relation, type_type_relation, object_types, activities):
    return [(ot, {(ot,a) for a in activities
        if (ot,a) in activity_type_relation}) for ot in object_types]

def get_connected_case_notion(activity_type_relation, type_type_relation, object_type, activities):
    return [(ot, activity_type_relation | type_type_relation) for ot in object_type]

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

        result.append((start,spec))
        print(result[-1])
    return result
