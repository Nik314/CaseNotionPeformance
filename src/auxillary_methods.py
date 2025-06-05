



def get_log_properties(ocel):

    object_types = set(ocel.relations["ocel:type"].unique())
    activities = set(ocel.relations["ocel:activity"].unique())

    activity_type_relations = {(a,ot) for a in activities for ot in
                ocel.relations[ocel.relations["ocel:activity"] == a]["ocel:type"].unique()}
    activity_type_relations = activity_type_relations | {(b,a) for (a,b) in activity_type_relations}

    lookup_dict_types = ocel.objects.set_index("ocel:oid")["ocel:type"].to_dict()
    lookup_dict_activities = ocel.events.set_index("ocel:eid")["ocel:activity"].to_dict()

    type_type_relation = set(ocel.o2o.apply(lambda row: (lookup_dict_types[row["ocel:oid"]],
                lookup_dict_types[row["ocel:oid_2"]]),axis=1).unique())
    type_type_relation = type_type_relation | {(b,a) for (a,b) in type_type_relation}

    o2o = ocel.o2o
    o2o["type"] = o2o.apply(lambda row: (lookup_dict_types[row["ocel:oid"]], lookup_dict_types[row["ocel:oid_2"]]),axis=1)

    e2o = ocel.relations
    e2o["typee2o"] = e2o.apply(lambda row: (lookup_dict_activities[row["ocel:eid"]], lookup_dict_types[row["ocel:oid"]]),axis=1)
    e2o["typeo2e"] = e2o.apply(lambda row: (lookup_dict_types[row["ocel:oid"]], lookup_dict_activities[row["ocel:eid"]]),axis=1)

    return activity_type_relations,type_type_relation,activities,object_types,o2o,e2o,lookup_dict_types,lookup_dict_activities