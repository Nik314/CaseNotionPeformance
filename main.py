import pandas
import matplotlib.pyplot as plt
from src.experiments import runtime_experiment,property_experiment,run_case_study
import seaborn
plt.rcParams.update({'font.size': 18})


if __name__ == "__main__":
    pass


    #experiments use a lot of cores & RAM
    # --> please search for "Pool" in the repo to check if the core count is fine for your setup
    # --> note that logs will be duplicated across processes, so account for RAM

    #actual experiments, comment in/out to reproduce results
    #runtime_experiment("data","results")
    #property_experiment("data","results")
    #run_case_study()

    look_up_label_measure = {"cycle":"Cycle Time",
                     "resource":"Resource Usage",
                     "cost":"Total Costs"}

    #printing averages / etc for the paper

    runtime_frame = pandas.read_csv("results/experiment1.csv")
    print(runtime_frame["Runtime"].min())
    print(runtime_frame["Runtime"].mean())
    print(runtime_frame["Runtime"].max())
    for measure in {"Time","Resource","Cost"}:
        runtime_frame["Measure"] = runtime_frame["Measure"].apply(lambda entry: measure if measure.lower() in entry else entry)
    print(runtime_frame.groupby("Log")["Runtime"].min())
    print(runtime_frame.groupby("Log")["Runtime"].mean())
    print(runtime_frame.groupby("Log")["Runtime"].max())
    runtime_frame["Log"] = runtime_frame["Log"].apply(lambda log: log.split("/")[1].split("_")[0])
    ax = seaborn.stripplot(runtime_frame, hue="Measure", x="Log", y="Runtime", size=10, jitter=0.45)
    plt.grid()
    ax.set_xticks([0.499 + i for i in range(0, runtime_frame["Log"].nunique())])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
              ncol=4, fancybox=True, shadow=True)
    plt.savefig("results/runtime.png")
    plt.clf()


    #plotting figures
    frame = pandas.read_csv("results/experiment1.csv")
    frame["Notion"] = ["Automated"]*frame.shape[0]
    newframe = pandas.read_csv("results/experiment2.csv")

    for measure in {"cycle","resource","cost"}:
        for dis_property in {"deviation","skewness","kurtosis"}:#

            plot_data = pandas.concat([frame[["Log","Notion","Property Value","Property","Measure"]],
                                       newframe[["Log","Notion","Property Value","Property","Measure"]]])
            plot_data = plot_data[plot_data["Measure"].apply(lambda entry: measure in entry)]
            plot_data = plot_data[plot_data["Property"].apply(lambda entry: dis_property in entry)]
            plot_data["Log"] = plot_data["Log"].apply(lambda log:log.split("/")[1].split("_")[0])
            if plot_data["Log"].nunique() == 5:
                plot_data["Log"] = plot_data["Log"].apply(lambda entry:entry+(" "*25))
            else:
                plot_data["Log"] = plot_data["Log"].apply(lambda entry:entry+(" "*12))

            ax = seaborn.stripplot(plot_data,hue="Notion",x="Log",y="Property Value",size=20,jitter=0.45)
            plt.grid()
            ax.set_yscale('symlog')
            ax.set_ylim([-1,max(plot_data["Property Value"]*1000)])
            ax.set_xticks([0.499+i for i in range(0,plot_data["Log"].nunique())])
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                      ncol=4, fancybox=True, shadow=True)
            ax.set_ylabel(look_up_label_measure[measure]+" - "+dis_property[0].upper()+dis_property[1:])
            plt.gcf().set_size_inches(25, 7)
            plt.savefig(f"results/{measure}_{dis_property}.png",bbox_inches='tight')
            plt.clf()











