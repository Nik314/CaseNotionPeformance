import numpy
import pandas
import pm4py
import time
import os
import networkx

from src.case_notion_specification import generate_cases
from src.performance_indicator import get_cycle_time,get_emission_cost,get_ressource_usage
from src.optimization_framework import (get_optimized_case_notion_from_existing,
        get_optimized_case_notion_from_framework,get_log_graph,get_connected_case_notion,
        get_advanced_case_notion,get_traditional_case_notion,check_type,check_variance,get_log_properties)





def run_case_study():

    file = "data/08_ocel_legacy_recruiting.jsonocel"
    try:
        ocel = pm4py.read_ocel(file)
    except:
        ocel = pm4py.read_ocel2(file)


    for i in range(0,2):
        total_variance, start, spec = get_optimized_case_notion_from_framework(ocel, get_cycle_time,{})
        activity_type_relations,type_type_relation,activities,object_types,divergence = get_log_properties(ocel)
        log_graph = get_log_graph(ocel)
        cases = generate_cases(log_graph,start,spec,activities,object_types)

        sorted_dict = {}
        for case in cases:
            value = get_cycle_time(ocel,case, {})
            if value in sorted_dict.keys():
                sorted_dict[value].append(case)
            else:
                sorted_dict[value] = [case]

            relations = ocel.relations[ocel.relations["ocel:eid"].isin(case[0]) & ocel.relations["ocel:oid"].isin(case[1])]
            print("##############################################")
            #print(relations[["ocel:oid","ocel:eid","ocel:activity"]])
            print(case)
            print(value)
            print("##############################################")

        print("Best Performance Value", numpy.min(list(sorted_dict.keys())))
        print("Worst Performance Value", numpy.max(list(sorted_dict.keys())))

        filter_events = sum([list(case[0]) for case in sorted_dict[numpy.max(list(sorted_dict.keys()))]],[])
        filter_objects = sum([list(case[0]) for case in sorted_dict[numpy.max(list(sorted_dict.keys()))]],[])
        ocel = pm4py.filter_ocel_events(ocel,filter_events,positive=False)
        ocel = pm4py.filter_ocel_objects(ocel,filter_objects,positive=False)



        for entry in spec:
            print(entry[0].replace(" ",""),entry[1].replace(" ",""))




def runtime_experiment(log_dir, result_dir):


    result = pandas.DataFrame(columns=["Log","Objects","Events","Activities","Types","Relative Variance","Start","Relations","Runtime"])

    for file in os.listdir(log_dir):
        file = log_dir +"/" +file
        try:
            ocel = pm4py.read_ocel(file)
        except:
            ocel = pm4py.read_ocel2(file)

        runtime = time.time()
        variance, start, spec = get_optimized_case_notion_from_framework(ocel, get_cycle_time, {})
        runtime = time.time() - runtime
        result.loc[result.shape[0]] = (file,ocel.relations["ocel:oid"].nunique(),ocel.relations["ocel:eid"].nunique(),
                                        ocel.relations["ocel:activity"].nunique(),ocel.relations["ocel:type"].nunique(),variance,
                                        start,spec,runtime)
        result.to_csv(result_dir+"/experiment1.csv")
        print(result)




def variance_experiment(log_dir,result_dir):

    result = pandas.DataFrame(columns=["Log","Objects","Events","Activities","Types","Relative Variance","Start","Relations","Notion"])

    for file in os.listdir(log_dir):
        file = log_dir +"/" +file
        try:
            ocel = pm4py.read_ocel(file)
        except:
            ocel = pm4py.read_ocel2(file)

        activity_type_relations,type_type_relation,activities,object_types,divergence = get_log_properties(ocel)
        log_graph = get_log_graph(ocel)

        for ot,spec in get_traditional_case_notion(activity_type_relations,type_type_relation,object_types,activities):
            new_variance = check_variance(ocel,log_graph,ot,spec,get_cycle_time, {},activities,object_types,None)[1]
            result.loc[result.shape[0]] =  (file,ocel.relations["ocel:oid"].nunique(),ocel.relations["ocel:eid"].nunique(),
                                            ocel.relations["ocel:activity"].nunique(),ocel.relations["ocel:type"].nunique(),new_variance,
                                            ot,spec,"Traditional")
            result.to_csv(result_dir+"/experiment2.csv")


        for ot,spec in get_connected_case_notion(activity_type_relations,type_type_relation,object_types,activities):
            new_variance = check_variance(ocel,log_graph,ot,spec,get_cycle_time, {},activities,object_types,None)[1]
            result.loc[result.shape[0]] = (file, ocel.relations["ocel:oid"].nunique(), ocel.relations["ocel:eid"].nunique(),
                                ocel.relations["ocel:activity"].nunique(), ocel.relations["ocel:type"].nunique(), new_variance,
                                ot, spec, "Connected")
            result.to_csv(result_dir+"/experiment2.csv")

        for ot,spec in get_advanced_case_notion(activity_type_relations,type_type_relation,object_types,activities,divergence):
            new_variance = check_variance(ocel,log_graph,ot,spec,get_cycle_time, {},activities,object_types,None)[1]
            result.loc[result.shape[0]] = (file, ocel.relations["ocel:oid"].nunique(), ocel.relations["ocel:eid"].nunique(),
                                ocel.relations["ocel:activity"].nunique(), ocel.relations["ocel:type"].nunique(), new_variance,
                                ot, spec, "Advanced")
            result.to_csv(result_dir+"/experiment2.csv")

