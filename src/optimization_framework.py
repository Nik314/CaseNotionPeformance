
from src.auxillary_methods import get_log_properties
from src.case_notion_specification import check_variance




def get_optimized_case_notion(ocel, performance_indicator, additional):

    (activity_type_relations,type_type_relation,activities,
        object_types,o2o,e2o,lookup_dict_types, lookup_dict_activities)= get_log_properties(ocel)
    best_result, best_start_type, best_relations = 0,None,set()

    for starting_type in object_types:

        local_optimum, local_relations, next_addition = 0, set(), None

        while True:

            included_elements = set(sum([[a,b] for (a,b) in local_relations],[])) | {starting_type}
            relevant_relations = [rel for rel in activity_type_relations| type_type_relation if rel[0] in included_elements]

            for relation in relevant_relations:
                if relation in local_relations:
                    continue
                new_variance = check_variance(ocel,starting_type,local_relations | {relation}, performance_indicator,
                                o2o,e2o, lookup_dict_types, lookup_dict_activities,additional)

                if new_variance > local_optimum:
                    print(new_variance)
                    print(next_addition)
                    next_addition = relation
                    local_optimum = new_variance

            if next_addition:
                local_relations.add(next_addition)
            else:
                break

        if local_optimum > best_result:
            best_result = local_optimum
            best_start_type = starting_type
            best_relations = local_relations
            print(starting_type)
            print(best_relations)

    print(best_result, best_start_type, best_relations)

