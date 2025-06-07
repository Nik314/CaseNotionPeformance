import pandas


def get_log_properties(ocel):

    object_types = set(ocel.relations["ocel:type"].unique())
    activities = set(ocel.relations["ocel:activity"].unique())

    activity_type_relations = {(a,ot) for a in activities for ot in
                ocel.relations[ocel.relations["ocel:activity"] == a]["ocel:type"].unique()}
    activity_type_relations = activity_type_relations | {(b,a) for (a,b) in activity_type_relations}

    lookup_dict_types = ocel.objects.set_index("ocel:oid")["ocel:type"].to_dict()
    lookup_dict_activities = ocel.events.set_index("ocel:eid")["ocel:activity"].to_dict()

    try:
        type_type_relation = set(ocel.o2o.apply(lambda row: (lookup_dict_types[row["ocel:oid"]],
                    lookup_dict_types[row["ocel:oid_2"]]),axis=1).unique())
        type_type_relation = type_type_relation | {(b,a) for (a,b) in type_type_relation}
    except:
        type_type_relation = set()

    try:
        o2o = ocel.o2o
        o2o["type"] = o2o.apply(lambda row: (lookup_dict_types[row["ocel:oid"]], lookup_dict_types[row["ocel:oid_2"]]),axis=1)
    except:
        o2o = pandas.DataFrame(columns=["ocel:oid","ocel:oid_2","type"])

    e2o = ocel.relations
    e2o["typee2o"] = e2o.apply(lambda row: (lookup_dict_activities[row["ocel:eid"]], lookup_dict_types[row["ocel:oid"]]),axis=1)
    e2o["typeo2e"] = e2o.apply(lambda row: (lookup_dict_types[row["ocel:oid"]], lookup_dict_activities[row["ocel:eid"]]),axis=1)

    return (activity_type_relations,type_type_relation,activities,object_types,o2o,e2o,
        lookup_dict_types,lookup_dict_activities,get_divergence(ocel.relations))



def get_divergence(relations):

    look_up_dict_activities = relations.set_index("ocel:eid").to_dict()["ocel:activity"]
    look_up_dict_objects = relations.set_index("ocel:oid").to_dict()["ocel:type"]

    identifiers = relations.groupby("ocel:eid").apply(lambda
        frame: tuple(sorted(set(frame["ocel:oid"].values)))).to_frame(name="all")
    identifiers["activity"] = [look_up_dict_activities[event_id] for event_id in identifiers.index]
    for object_type in relations["ocel:type"].unique():
        identifiers[object_type] = identifiers["all"].apply(lambda object_set: tuple(
            sorted(list({object_id for object_id in object_set if look_up_dict_objects[object_id] == object_type}))))

    divergent_object_types = {a: set() for a in relations["ocel:activity"].unique()}

    for object_type in relations["ocel:type"].unique():
        sub_identifiers = identifiers[identifiers[object_type] != set()]
        for activity in relations["ocel:activity"].unique():
            sub_sub_identifiers = sub_identifiers[sub_identifiers["activity"] == activity]

            matches = sub_sub_identifiers.groupby(object_type).apply(lambda frame: frame["all"].nunique())
            matches = matches[[index for index in matches.index if index]]

            if matches.max() > 1:
                divergent_object_types[activity].add(object_type)

    return {(a,ot) for a in divergent_object_types.keys() for ot in divergent_object_types[a]} | \
        {(ot, a) for a in divergent_object_types.keys() for ot in divergent_object_types[a]}

