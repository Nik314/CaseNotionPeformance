import pm4py
import time
import os
import pandas
import matplotlib.pyplot as plt
from src.experiments import runtime_experiment,variance_experiment



if __name__ == "__main__":
    pass


    #variance_experiment("data","results")
    #runtime_experiment("data","results")

    connectivity = []
    for file in os.listdir("data"):
        file = "data" + "/" + file
        try:
            ocel = pm4py.read_ocel(file)
        except:
            ocel = pm4py.read_ocel2(file)
        connectivity.append(ocel.relations.shape[0] + ocel.o2o.shape[0])

    frame = pandas.read_csv("results/experiment1.csv")
    frame["Connectivity"] = connectivity
    frame["Test"] = (frame["Relative Variance"])*(frame["Connectivity"])*frame["Types"]*(frame["Types"] + frame["Activities"])*(frame["Types"] + frame["Activities"])
    frame.plot(x="Test", y="Runtime", figsize=(16,8),style="o")
    plt.savefig("results/experiment1.png")
    frame[["Test","Runtime"]].to_csv("results/exp1_visual.csv")
    print(frame)






