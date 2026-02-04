import numpy


def get_cycle_time(log, case, additional):
    timestamps = log.events[log.events["ocel:eid"].isin(case[0])]["ocel:timestamp"].to_list()
    if timestamps:
        return (max(timestamps) - min(timestamps)).total_seconds()
    else:
        return 0.0


def get_resource_usage(log, case, additional):
    return log.relations[log.relations["ocel:type"].isin(additional["ocel:type"]) &
        log.relations["ocel:eid"].isin(case[0]) & log.relations["ocel:oid"].isin(case[1])].shape[0]



def get_total_costs(log, case, additional):

    try:
        object_value = log.objects[log.objects["ocel:oid"].isin(case[1])][additional["ocel:attribute"]].sum().sum()
    except:
        object_value = 0.0

    try:
        event_values = log.events[log.events["ocel:eid"].isin(case[0])][additional["ocel:attribute"]].sum().sum()
    except:
        event_values = 0.0

    return object_value+event_values
