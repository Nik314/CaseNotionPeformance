import pandas
import pm4py
import time
import os
from src.performance_indicator import get_cycle_time,get_emission_cost,get_ressource_usage
from src.optimization_framework import (get_optimized_case_notion_from_existing,
        get_optimized_case_notion_from_framework,get_log_graph,get_connected_case_notion,
        get_advanced_case_notion,get_traditional_case_notion,check_type,check_variance,get_log_properties)



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

