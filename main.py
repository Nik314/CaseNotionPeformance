import pandas
import matplotlib.pyplot as plt
from src.experiments import runtime_experiment,deviation_experiment,run_case_study
import seaborn
plt.rcParams.update({'font.size': 18})


if __name__ == "__main__":
    pass

    runtime_experiment("data","results")
    deviation_experiment("data","results")
    #run_case_study()

    frame = pandas.read_csv("results/experiment1.csv")
    frame["Notion"] = ["Automated"]*frame.shape[0]
    newframe = pandas.read_csv("results/experiment2.csv")

    plot_data = pandas.concat([frame[["Log","Notion","Standard Deviation"]],newframe[["Log","Notion","Standard Deviation"]]])
    plot_data["Log"] = plot_data["Log"].apply(lambda log:log.split("/")[1].split("_")[0])

    seaborn.swarmplot(plot_data,hue="Notion",x="Log",y="Standard Deviation")
    plt.grid()
    plt.show()











