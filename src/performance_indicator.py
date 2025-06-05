


def get_cycle_time(log, case, additional):
    timestamps = log.events[log.events["ocel:eid"].isin(case[0])]["ocel:timestamp"].to_list()
    if timestamps:
        return (max(timestamps) - min(timestamps)).total_seconds()
    else:
        return 0.0


def get_emission_cost(log, case, additional):
    return 0


def get_ressource_usage(log, case, additional):
    return 0