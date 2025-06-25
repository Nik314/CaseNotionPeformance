import pm4py
import time
import os
import pandas
import numpy
import matplotlib.pyplot as plt
from src.experiments import runtime_experiment,variance_experiment,run_case_study
import seaborn
plt.rcParams.update({'font.size': 18})


if __name__ == "__main__":
    pass

    start,result = run_case_study()
    print(start)
    for entry in result:
        print(entry[0].replace(" ",""),entry[1].replace(" ",""))


    #runtime_experiment("data","results")
    #variance_experiment("data","results")


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
    frame["Test"] = (frame["Connectivity"])*(frame["Types"] + frame["Activities"])*(frame["Types"] + frame["Activities"])
    plt.figure(figsize=(16, 8))
    plt.grid()
    plt.ylim(0,4000)
    plt.xlim(0,10*10**7)
    seaborn.scatterplot(frame,x="Test",y="Runtime")
    plt.xlabel("Runtime In Seconds")
    plt.xlabel("Input Log Size Property Product")
    #plt.plot([0, 10*10**7], [0,4000], linewidth=2)
    plt.savefig("results/experiment1.png",bbox_inches='tight')

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

        series = frame[frame["Log"] == log]["Relative Variance"].to_list()
        experiment2_visual.loc[experiment2_visual.shape[0]] = (log, numpy.min(series), numpy.max(series),
            numpy.mean(series), numpy.percentile(series,25), numpy.percentile(series,75), numpy.median(series), " (Automated)")


    experiment2_visual2 = experiment2_visual[["Notion","Max","Log"]]
    experiment2_visual2 = experiment2_visual2[experiment2_visual2["Notion"].isin([" (Automated)"," (Traditional)"])]
    experiment2_visual2["Notion"] = experiment2_visual2["Notion"].apply(lambda e:e if e == " (Automated)" else " (Manual)")
    plt.figure(figsize=(16, 8))
    plt.grid()
    plt.ylim(-5,400)
    experiment2_visual2["Label"] = experiment2_visual2["Log"].apply(lambda log:log.split("/")[1].split("_")[0])
    seaborn.barplot(experiment2_visual2,x="Label",y="Max",hue="Notion")
    plt.ylabel("Best Relative Variance")
    plt.xlabel("Input Log")
    plt.savefig("results/experiment22.png",bbox_inches='tight')

    plt.figure(figsize=(16, 8))
    plt.grid()
    plt.ylim(-5,200)
    newframe["Label"] = newframe["Log"].apply(lambda log:log.split("/")[1].split("_")[0])
    seaborn.boxplot(newframe,x="Label",y="Relative Variance",hue="Notion",whis=10000000000000)
    plt.xlabel("Relative Variance")
    plt.xlabel("Input Log")
    plt.savefig("results/experiment2.png",bbox_inches='tight')









