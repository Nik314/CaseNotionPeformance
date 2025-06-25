import numpy


def get_cycle_time(log, case, additional):
    timestamps = log.events[log.events["ocel:eid"].isin(case[0])]["ocel:timestamp"].to_list()
    if timestamps:
        return (max(timestamps) - min(timestamps)).total_seconds()
    else:
        return 0.0


def get_emission_cost(log, case, additional):
    event_costs = log.events[log.events["ocel:eid"].isin(case[0])][additional["att"]]
    object_costs = log.objects[log.objects["ocel:oid"].isin(case[1])][additional["att"]]
    def filter(entry):
        try:
            return float(entry)
        except:
            return 0.0
    return event_costs.apply(filter).sum() + object_costs.apply(filter).sum()

def get_ressource_usage(log, case, additional):
    return 0