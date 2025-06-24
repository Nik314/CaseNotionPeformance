import pm4py
import time
import os
import pandas
import numpy
import matplotlib.pyplot as plt
from src.experiments import runtime_experiment,variance_experiment



if __name__ == "__main__":
    pass


    runtime_experiment("data","results")
    variance_experiment("data","results")


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
    frame[["Test","Runtime"]].to_csv("results/exp1_visual.csv")
    print(frame)


    newframe = pandas.read_csv("results/experiment2.csv")
    traditional = newframe[newframe["Notion"] == "Traditional"]
    advanced = newframe[newframe["Notion"] == "Advanced"]
    connected = newframe[newframe["Notion"] == "Connected"]

    experiment2_visual = pandas.DataFrame(columns = ["Log","Min","Max","Mean","P25","P75","Median","Notion"])

    for log in newframe["Log"].unique():

        series = traditional[traditional["Log"] == log]["Relative Variance"].to_list()
        experiment2_visual.loc[experiment2_visual.shape[0]] = (log, numpy.min(series), numpy.max(series),
            numpy.mean(series), numpy.percentile(series,25), numpy.percentile(series,75), numpy.median(series), " (Traditional)")

        series = advanced[advanced["Log"] == log]["Relative Variance"].to_list()
        experiment2_visual.loc[experiment2_visual.shape[0]] = (log, numpy.min(series), numpy.max(series),
            numpy.mean(series), numpy.percentile(series,25), numpy.percentile(series,75), numpy.median(series), " (Advanced)")

        series = connected[connected["Log"] == log]["Relative Variance"].to_list()
        experiment2_visual.loc[experiment2_visual.shape[0]] = (log, numpy.min(series), numpy.max(series),
            numpy.mean(series), numpy.percentile(series,25), numpy.percentile(series,75), numpy.median(series), " (Connected)")


    experiment2_visual2 = experiment2_visual[["Log","Max"]]
    experiment2_visual2 = experiment2_visual2.groupby("Log")["Max"].max().to_dict()
    experiment2_visual2 = {key.split("/")[1].split("_")[0]:{"Manual":value, "Automated":frame[frame["Log"] ==key]["Relative Variance"].max()}
                           for key,value in experiment2_visual2.items()}
    pandas.DataFrame().from_dict(experiment2_visual2).transpose().to_csv("results/exp2_visual2.csv")

    experiment2_visual["Log"] = experiment2_visual["Log"].apply(lambda log:log.split("/")[1].split("_")[0]) + experiment2_visual["Notion"]
    experiment2_visual.to_csv("results/exp2_visual.csv")


    for entry in eval(frame.iloc[4]["Relations"]):
        print(entry[0].replace(" ","")," ",entry[1].replace(" ",""))












