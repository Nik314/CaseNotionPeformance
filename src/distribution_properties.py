import numpy

def standard_deviation(values):
    average = numpy.mean(values)
    squared_error = sum([(average-value)**2 for value in values]) / len(values)
    return numpy.sqrt(squared_error)

def skewness(values):
    average = numpy.mean(values)
    sigma = standard_deviation(values)
    if not sigma:
        return 0.0
    return sum([((average - value)/sigma)**3 for value in values]) / len(values)

def kurtosis(values):
    average = numpy.mean(values)
    sigma = standard_deviation(values)
    if not sigma:
        return 0.0
    return (sum([((average - value)/sigma)**4 for value in values]) / len(values)) -3
