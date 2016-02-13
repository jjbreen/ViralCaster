import numpy as np
import math
import random
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
from pybrain.structure import TanhLayer

# sigmoid function
def nonlin_sigmoid(x, deriv=False):
	if (deriv == True):
		return x *(1-x)
	return 1 / (1 +np.exp(-x))

def bipolar_sigmoid(x, deriv=False):
	if (deriv == True):
		return 0.5 * (1 + bipolar_sigmoid(x)) * (1 - bipolar_sigmoid(x))

	return -1 + 2 / (1 + np.exp(-x))


def createPyBrainNeuralNet(idata, odata, nhidden=20):
	net = buildNetwork(len(idata[0]), nhidden, len(odata[0]), hiddenclass=TanhLayer)

	ds = SupervisedDataSet(len(idata[0]), len(odata[0]))
	for x in range(len(idata)):
		ds.addSample(idata[x], odata[x])

	trainer = BackpropTrainer(net, ds)
	#trainer.trainUntilConvergence()
	for x in range(60000):
		if x % 1000 == 0:
			print(trainer.train())
	
	return net
	

def createNeuralNet(idata, odata, nhidden=20, sigmoid=nonlin_sigmoid):
	np.random.seed(25)

	idata = np.array(idata)
	odata = np.array(odata)

	print(idata )
	print (odata )

	syn0 = 2 * np.random.random((len(idata[0]), nhidden)) - 1
	syn1 = 2 * np.random.random((nhidden, len(odata[0]))) - 1

	for j in range(60000):

		l0 = idata
		l1 = sigmoid(np.dot(l0, syn0))
		l2 = sigmoid(np.dot(l1, syn1))

		l2_error = odata - l2
		l2_delta = l2_error * sigmoid(l2, deriv=True)


		if (j % 1000) == 0:
			#print ("Delta: %s" % l2_delta)
			#print ("Error: %s" % l2_error)
			print ("Error: %s" % str(np.mean(np.abs(l2_error))))


		l1_error = l2_delta.dot(syn1.T)
		l1_delta = l1_error * sigmoid(l1, deriv=True)

		syn1 += l1.T.dot(l2_delta)
		syn0 += l0.T.dot(l1_delta)

	return (syn0, syn1)


def predictValue(neural, idata, sigmoid=nonlin_sigmoid):
	prediction = idata
	for x in neural:
		prediction = sigmoid(np.dot(prediction, x))

	return prediction


def crossValidation(idata, odata, k=10):
	psize = int(len(idata) / k)
	accuracy = []

	for x in range(k):
		pstart = x * psize
		pend = (x+1) * psize 
		net = createNeuralNet(idata[:pstart] + idata[pend:], odata[:pstart] + odata[pend:])
		pred = predictValue(net, idata[pstart: pend])

		numWrong = 0
		actual = odata[pstart:pend]

		print(pred)
		print(actual)

		for x in range(len(pred)):
			if pred[x] != actual[x]:
				print ("Prediction: %s != Actual: %s" % (pred[x], actual[x]))
				numWrong += 1

		accuracy.append(numWrong / len(pred))

	print (accuracy)
	return sum(accuracy) / k 



def convertIntBinary(dec, bitnum=32):
	return [int(x) for x in '{0:0{1}b}'.format(dec, bitnum)]

def convertBinaryInt(binary, fix=True):
	if fix:
		binary = [str(int(round(x))) for x in binary]

	return int(''.join(binary), 2)


def main():
	k = 25
	#idata = [[(math.pi / k * x)] for x in range(k+1)]
	#random.shuffle(idata)
	#odata = [[0.5*(math.sin(x[0]) + 1)] for x in idata]

	idata = [x for x in range(k+1) if x != 5]
	odata = [x*2 for x in idata]

	idata = [convertIntBinary(x) for x in idata]
	odata = [convertIntBinary(x) for x in odata]


	print (idata)
	print (odata)

	data2 = [[0,0,1], [0,1,1], [1,0,1],[1,1,1]]
	odata2 = [[0], [1], [1], [0]]

	net = createPyBrainNeuralNet(idata, odata)
	#print(net.activate([math.pi]))
	#net = createNeuralNet(idata, odata)#, sigmoid=bipolar_sigmoid)
	#a = crossValidation(idata, odata)

	#print (a )

	print(net)

	#pred = predictValue(net, [convertIntBinary(5), convertIntBinary(6)])#, sigmoid=bipolar_sigmoid)
	
	#pred = [convertBinaryInt(x) for x in pred]
	print(convertBinaryInt(net.activate(convertIntBinary(5))))
	#print(pred)

main()