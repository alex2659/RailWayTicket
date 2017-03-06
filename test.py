import operator
import numpy


test = numpy.array([255,255,255])
test2 = numpy.array([0,0,0])
test3 = numpy.array([0,0,0])
print(operator.gt(test.sum(),test3.sum()))