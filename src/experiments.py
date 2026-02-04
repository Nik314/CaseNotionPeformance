import numpy
import pandas
import pm4py
import time
import os

from src.case_notion_specification import generate_cases
from src.performance_indicator import *
from src.distribution_properties import *
from src.optimization_framework import *




lookup_additional = {
    ("01",get_cycle_time):{},
    ("02",get_cycle_time):{},
    ("03",get_cycle_time):{},
    ("04",get_cycle_time):{},
    ("05",get_cycle_time):{},
    ("06",get_cycle_time):{},
    ("07",get_cycle_time):{},
    ("08",get_cycle_time):{},
    ("09",get_cycle_time):{},
    ("10",get_cycle_time):{},
    ("01",get_resource_usage):{"ocel:type":["managers","recruiters"]},
    ("02",get_resource_usage):{"ocel:type":["material"]},
    ("03",get_resource_usage):{"ocel:type":["Product"]},
    ("04",get_resource_usage):{"ocel:type":["Supplier"]},
    ("05",get_resource_usage):{"ocel:type":["HiringManager","Interviewer"]},
    ("06",get_resource_usage):{"ocel:type":["Bed","Room"]},
    ("07",get_resource_usage):{"ocel:type":["org:resource"]},
    ("08",get_resource_usage):{"ocel:type":["Truck","Vehicle"]},
    ("09",get_resource_usage):{"ocel:type":["Machine"]},
    ("10",get_resource_usage):{"ocel:type":["MATNR"]},
    #("01",get_total_costs):{"ocel:attribute":[""]}, (no cost attribute available)
    ("02",get_total_costs):{"ocel:attribute":["Credit Amount (BSEG-WRBTR)"]},
    ("03",get_total_costs):{"ocel:attribute":["price"]},
    ("04",get_total_costs):{"ocel:attribute":["amount"]},
    #("05",get_total_costs):{"ocel:attribute":[""]},(no cost attribute available)
    #("06",get_total_costs):{"ocel:attribute":[""]},(no cost attribute available)
    #("07",get_total_costs):{"ocel:attribute":[""]},(no cost attribute available)
    ("08",get_total_costs):{"ocel:attribute":["Amount of Containers"]},
    ("09",get_total_costs):{"ocel:attribute":["s_co2e[kg]"]},
    #("10",get_total_costs):{"ocel:attribute":[""]},(no cost attribute available)
}

def runtime_experiment(log_dir, result_dir):

    result = pandas.DataFrame(columns=["Log","Objects","Events","Activities","Types","Property Value","Property","Measure","Start","Relations","Runtime"])

    for file in os.listdir(log_dir):
        file = log_dir + "/" + file
        for performance_measure in [get_total_costs,get_cycle_time,get_resource_usage]:
            for dis_property in [standard_deviation,skewness,kurtosis]:

                try:
                    ocel = pm4py.read_ocel(file)
                except:
                    ocel = pm4py.read_ocel2(file)

                file_id = file.split("/")[-1].split("_")[0]

                try:
                    additional = lookup_additional[(file_id, performance_measure)]
                except:
                    continue

                runtime = time.time()
                property_value, start, spec = get_optimized_case_notion_from_framework(ocel, dis_property, performance_measure, additional)
                runtime = time.time() - runtime
                result.loc[result.shape[0]] = (file,ocel.relations["ocel:oid"].nunique(),ocel.relations["ocel:eid"].nunique(),
                    ocel.relations["ocel:activity"].nunique(),ocel.relations["ocel:type"].nunique(),
                                property_value,dis_property,performance_measure, start,spec,runtime)
                result.to_csv(result_dir+"/experiment1.csv")
                print(result)




def property_experiment(log_dir,result_dir):

    result = pandas.DataFrame(columns=["Log","Objects","Events","Activities","Types","Property Value","Property","Measure","Start","Relations","Notion"])

    for file in os.listdir(log_dir):
        file = log_dir +"/" +file
        try:
            ocel = pm4py.read_ocel(file)
        except:
            ocel = pm4py.read_ocel2(file)

        activity_type_relations,type_type_relation,activities,object_types,divergence = get_log_properties(ocel)
        log_graph = get_log_graph(ocel)
        file_id = file.split("/")[-1].split("_")[0]

        for performance_measure in [get_total_costs,get_cycle_time,get_resource_usage]:
            for dis_property in [standard_deviation,skewness,kurtosis]:

                try:
                    additional = lookup_additional[(file_id,performance_measure)]
                except:
                    continue

                for ot,spec in get_traditional_case_notion(activity_type_relations,type_type_relation,object_types,activities):
                    new_value = check_property(ocel,log_graph,ot,spec,performance_measure, additional,activities,object_types,dis_property)
                    result.loc[result.shape[0]] =  (file,ocel.relations["ocel:oid"].nunique(),ocel.relations["ocel:eid"].nunique(),
                            ocel.relations["ocel:activity"].nunique(),ocel.relations["ocel:type"].nunique(),
                            new_value,dis_property,performance_measure,ot,spec,"Traditional")
                    result.to_csv(result_dir+"/experiment2.csv")


                for ot,spec in get_connected_case_notion(activity_type_relations,type_type_relation,object_types,activities):
                    new_value = check_property(ocel,log_graph,ot,spec,performance_measure, additional,activities,object_types,dis_property)
                    result.loc[result.shape[0]] = (file, ocel.relations["ocel:oid"].nunique(), ocel.relations["ocel:eid"].nunique(),
                            ocel.relations["ocel:activity"].nunique(), ocel.relations["ocel:type"].nunique(),
                            new_value,dis_property,performance_measure,ot, spec, "Connected")
                    result.to_csv(result_dir+"/experiment2.csv")

                for ot,spec in get_advanced_case_notion(activity_type_relations,type_type_relation,object_types,activities,divergence):
                    new_value = check_property(ocel,log_graph,ot,spec,performance_measure, additional,activities,object_types,dis_property)
                    result.loc[result.shape[0]] = (file, ocel.relations["ocel:oid"].nunique(), ocel.relations["ocel:eid"].nunique(),
                                        ocel.relations["ocel:activity"].nunique(), ocel.relations["ocel:type"].nunique(),
                                        new_value, dis_property, performance_measure, ot, spec, "Advanced")
                    result.to_csv(result_dir+"/experiment2.csv")



def run_case_study():

    file = "data/01_ocel_legacy_recruiting.jsonocel"
    try:
        ocel = pm4py.read_ocel(file)
    except:
        ocel = pm4py.read_ocel2(file)


    for i in range(0,2):
        total_deviation, start, spec = get_optimized_case_notion_from_framework(ocel, standard_deviation,get_cycle_time,{})
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



