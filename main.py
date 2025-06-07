import pm4py

from src.performance_indicator import get_cycle_time,get_emission_cost,get_ressource_usage
from src.optimization_framework import get_optimized_case_notion_event_based


file = "data/08_ocel_standard_hinge.xml"
try:
    ocel = pm4py.read_ocel(file)
except:
    ocel = pm4py.read_ocel2(file)

variance ,start, spec = get_optimized_case_notion_event_based(ocel, get_cycle_time,{})
