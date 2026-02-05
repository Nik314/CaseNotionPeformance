import pandas
import matplotlib.pyplot as plt
from src.experiments import runtime_experiment,property_experiment,run_case_study
import seaborn
plt.rcParams.update({'font.size': 18})


if __name__ == "__main__":
    pass

    #runtime_experiment("data","results")
    #property_experiment("data","results")
    #run_case_study()
    look_up_label_measure = {"cycle":"Cycle Time",
                     "resource":"Resource Usage",
                     "cost":"Total Costs"}

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

            ax = seaborn.stripplot(plot_data,hue="Notion",x="Log",y="Property Value",size=10,jitter=0.45)
            plt.grid()
            ax.set_yscale('symlog')
            ax.set_ylim([-1,max(plot_data["Property Value"]*1000)])
            ax.set_xticks([0.499+i for i in range(0,plot_data["Log"].nunique())])
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                      ncol=4, fancybox=True, shadow=True)
            ax.set_ylabel(look_up_label_measure[measure]+" - "+dis_property[0].upper()+dis_property[1:])
            plt.gcf().set_size_inches(14, 7)
            plt.savefig(f"results/{measure}_{dis_property}.png",bbox_inches='tight')
            plt.clf()











