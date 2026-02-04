import pandas
import matplotlib.pyplot as plt
from src.experiments import runtime_experiment,property_experiment,run_case_study
import seaborn
plt.rcParams.update({'font.size': 18})


if __name__ == "__main__":
    pass

    #runtime_experiment("data","results")
    property_experiment("data","results")
    #run_case_study()

    exit()
    frame = pandas.read_csv("results/experiment1.csv")
    frame["Notion"] = ["Automated"]*frame.shape[0]
    newframe = pandas.read_csv("results/experiment2.csv")

    plot_data = pandas.concat([frame[["Log","Notion","Standard Deviation"]],newframe[["Log","Notion","Standard Deviation"]]])
    plot_data["Standard Deviation"] = plot_data["Standard Deviation"] / 3600
    plot_data["Log"] = plot_data["Log"].apply(lambda log:log.split("/")[1].split("_")[0])

    ax = seaborn.stripplot(plot_data,hue="Notion",x="Log",y="Standard Deviation",size=10,jitter=0.45)
    plt.grid()
    ax.set_yscale('symlog')
    ax.set_ylim([-1,10000000000])
    ax.set_xticks([0.5+i for i in range(0,10)])
    ax.set_xticklabels([str(i)+"                 " for i in range(1,11)])
    plt.show()











