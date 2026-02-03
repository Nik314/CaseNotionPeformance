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
    events = log.events[log.events["ocel:eid"].isin(case[0])]
    objects = log.objects[log.events["ocel:oid"].isin(case[1])]
    print("Todo: Total Cost Attribute Access")
