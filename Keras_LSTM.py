##########################################################################
# Potential Keras LSTM Neural Network Model for Gatherer.                #
# Needs bugfix/integration into program.                                 #
# Based on:                                                              #
# https://stackoverflow.com/questions/49712037/trend-predictor-in-python #
##########################################################################

X = []
y = []

# Build training data.
data1 = self.currentData['Entry'].tolist()
data = [int(x) for x in data1]

for i in range(len(data1)-100-1):
	X.append(data1[i:i+100])
	y.append(data1[i+100])

# Reshape the training data to work with Keras LSTM.
X = np.array(X)
X = X.reshape(len(X), len(X[0]), 1)

# Construct an LSTM Neural Network.
model = Sequential()
model.add(LSTM(units = 1, input_shape = (len(X[0]), 1)))
model.add(Dense(1))
model.compile(loss = 'mean_squared_error', optimizer = 'adam')
model.fit(X, y)
