import math


def generate_cases(ocel, starting_type, specification, o2o, e2o, lookup_dict_types, lookup_dict_activities):

    starting_objects = set(ocel.objects[ocel.objects["ocel:type"] == starting_type]["ocel:oid"].unique())
    final_case_list = []
    total = len(starting_objects)
    while starting_objects:

        case_events = set()
        case_objects = {starting_objects.pop()}

        while True:

            #print("Remaining Objects To Check " + str(len(starting_objects) * 100 / total) + "%")
            new_objects = set(o2o[o2o["ocel:oid"].isin(case_objects) & o2o["type"].isin(specification)]["ocel:oid_2"])
            new_objects = new_objects | set(e2o[e2o["ocel:eid"].isin(case_events) & e2o["typee2o"].isin(specification)]["ocel:oid"])
            new_events = set(e2o[e2o["ocel:oid"].isin(case_objects) & e2o["typeo2e"].isin(specification)]["ocel:eid"])
            new_objects = {o for o in new_objects if o not in case_objects}
            new_events = {e for e in new_events if e not in case_events}
            starting_objects = starting_objects - case_objects

            if not new_events and not new_objects:
                break
            else:
                case_events = case_events | new_events
                case_objects = case_objects | new_objects

        final_case_list.append((case_events,case_objects))

    return final_case_list



def check_variance(ocel, starting_type, specification, performance_indicator, o2o, e2o,
                   lookup_dict_types, lookup_dict_activities,additional):
    case_list = generate_cases(ocel,starting_type,specification, o2o, e2o, lookup_dict_types, lookup_dict_activities)
    print("Number Of Cases", len(case_list))
    values = [performance_indicator(ocel,case,additional) for case in case_list]
    distribution = {v:values.count(v) for v in set(values)}
    average = sum( ((v * p) / len(distribution)) for v,p in distribution.items())
    variance = sum( (average - v) * (average - v) * p for v,p in distribution.items())
    return (math.sqrt(variance) / average) if average else 0.0
