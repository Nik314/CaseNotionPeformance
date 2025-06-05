import pm4py

from src.performance_indicator import get_cycle_time,get_emission_cost,get_ressource_usage
from src.optimization_framework import get_optimized_case_notion



try:
    ocel = pm4py.read_ocel("data/01_ocel_standard_order_management.json")
except:
    ocel = pm4py.read_ocel2("data/01_ocel_standard_order_management.json")

get_optimized_case_notion(ocel, get_cycle_time,{})