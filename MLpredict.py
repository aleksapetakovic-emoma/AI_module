import os
import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns

dataset = pd.read_csv('./outfile.csv')
dataset['allergy'] = dataset['allergy'].map({'yes': 1, 'no': 0})
dataset['medication'] = dataset['medication'].map({'yes': 1, 'no': 0})
dataset['class'] = dataset['class'].map({'low': 0, 'medium': 1, 'high': 2})

categorical_cols = dataset[dataset.columns[5]]
train_dataset = dataset[dataset.columns[0:5]]
bmi_col = dataset[dataset.columns[6]]
categorical_dummies = pd.get_dummies((categorical_cols))
categorical_dummies = categorical_dummies[categorical_dummies.columns[0:3]]
train_dataset = pd.concat([train_dataset,categorical_dummies], axis= 1)
train_dataset = pd.concat([train_dataset, bmi_col], axis=1)
print(train_dataset)
train_labels = dataset[dataset.columns[-1]]
dataset = dataset.rename(columns={'class':'risk'})
a = sns.relplot(x='age', y='risk', data= dataset, hue='disease')
plt.show()

train_norm = train_dataset[['age','surgery','docvisit','bmi']]
# Normalize Training Data
std_scale = preprocessing.StandardScaler().fit(train_norm)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation=tf.nn.relu,  input_shape=[len(train_dataset.keys())]),  # input shape required

    tf.keras.layers.Dense(10, activation=tf.nn.relu),
    tf.keras.layers.Dense(10, activation=tf.nn.relu),

    tf.keras.layers.Dense(3)
])


#   from emoma_training import model
checkpoint_path = "C:/Users/akica/PycharmProjects/AIproject/checkpoints/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)


latest = tf.train.latest_checkpoint(checkpoint_dir)
model.load_weights(latest)


def make_prediction_tensor(age,surgery,docvisit,allergy,medication,cholesterol,diabetes,heart,bmi):
    x_test_norm = norm_record(age,surgery,docvisit,bmi)
    prediction_array = [[x_test_norm[0][0], x_test_norm[0][1],x_test_norm[0][2],allergy,medication,cholesterol,diabetes,
                         heart,x_test_norm[0][3]]]
    print(prediction_array)
    prediction_tensor = tf.convert_to_tensor(prediction_array)
    return prediction_tensor


def norm_record(age,surgery,docvisit,bmi):
    test_norm = np.array([[age,surgery, docvisit, bmi]])
    x_test_norm = std_scale.transform(test_norm)
    return x_test_norm

def predict(predict_dataset):
    predictions = model(predict_dataset)
    # from custom training walkthrough (tf's official website)
    class_names = ['low', 'medium', 'high']

    for i, logits in enumerate(predictions):
        class_idx = tf.argmax(logits).numpy()
        print(class_idx)
        p = tf.nn.softmax(logits)[class_idx]
        print(class_idx)
        name = class_names[class_idx]
        print("Example {} prediction: {} ({:4.1f}%)".format(i, name, 100 * p))
        p=float(p*100)
        return name, p

"""
predict_dataset = make_prediction_tensor(88,0,2,0,0,0,0,0,31)

predictions= model(predict_dataset)
class_names = ['low', 'medium', 'high']

print(predictions)

#   go back and normalize
for i, logits in enumerate(predictions):
    class_idx = tf.argmax(logits).numpy()
    print(class_idx)
    p = tf.nn.softmax(logits)[class_idx]
    print(class_idx)
    name = class_names[class_idx]
    print("Example {} prediction: {} ({:4.1f}%)".format(i, name, 100*p))
"""