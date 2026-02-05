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
        object_values = log.objects[log.objects["ocel:oid"].isin(case[1])][additional["ocel:attribute"]]
        for column in object_values.columns:
            object_values[column] = object_values[column].apply(convert)
        object_value = object_values.sum().sum()
    except KeyError:
        object_value = 0.0

    try:
        event_values = log.events[log.events["ocel:eid"].isin(case[0])][additional["ocel:attribute"]]
        for column in event_values.columns:
            event_values[column] = event_values[column].apply(convert)
        event_value = event_values.sum().sum()
    except KeyError:
        event_value = 0.0

    result = event_value+object_value
    return result



def convert(entry):
    try:
        return float(entry)
    except:
        return 0.0