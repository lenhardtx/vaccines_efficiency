from Case import Case
from Chart import Chart
from Death import Death
from Graph import Graph
from Predict import Predict
from Vaccine import Vaccine


def main():

    downloadCSV = True
    loadCSV = True

    vaccines = Vaccine()
    deaths = Death()
    cases = Case()

    if downloadCSV:
        vaccines.downloadCSV()
        deaths.downloadCSV()
        cases.downloadCSV()

    if loadCSV:
        vaccines.load()
        deaths.load()
        cases.load()


    #graphs = Graph()
    #graphs.byMonth()

    charts = Chart()
    charts.start()

    #predict = Predict()
    #predict.start()

if __name__ == "__main__":
    main()