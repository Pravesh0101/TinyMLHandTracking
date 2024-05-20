import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import os
import numpy as np
from PIL import Image

# Set your dataset directory
dataset_dir = 'color_dataset'

# Load the dataset
image_paths = []
labels = []

for filename in os.listdir(dataset_dir):
    if filename.endswith('.png'):
        filepath = os.path.join(dataset_dir, filename)
        image_paths.append(filepath)
        labels.append([int(x) for x in filename[:-4].split('_')])

# Convert lists to numpy arrays
images = np.array([np.array(Image.open(path)) for path in image_paths])
labels = np.array(labels)

# Normalize the image data
images = images / 255.0

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Define the model
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(3, activation='softmax'))  # Assuming you have 3 classes (RGB)

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Convert labels to one-hot encoding
y_train_categorical = tf.keras.utils.to_categorical(y_train, num_classes=3)
y_test_categorical = tf.keras.utils.to_categorical(y_test, num_classes=3)

# Train the model
model.fit(X_train, y_train_categorical, epochs=10, validation_data=(X_test, y_test_categorical))

# Convert the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TensorFlow Lite model
tflite_model_path = 'color_classification_model.tflite'
with open(tflite_model_path, 'wb') as f:
    f.write(tflite_model)

print(f"Model saved to {tflite_model_path}")
