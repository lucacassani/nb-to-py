# DATASET

data = dataset.load("SELECT * FROM table")
train, test = dataset.split(0.3)
X_train = train[features]
y_train = train[target]
X_test = train[features]
y_test = train[target]

# MODEL FIT

model = model.Classifier()
model.fit(X_train, y_train)