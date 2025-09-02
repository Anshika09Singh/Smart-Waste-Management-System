# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
# import os, json

# data_dir = "../backend/dataset/"  # your dataset

# # Image Data Generator
# datagen = ImageDataGenerator(
#     rescale=1./255,
#     validation_split=0.2,
#     rotation_range=20,
#     width_shift_range=0.2,
#     height_shift_range=0.2,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True,
#     fill_mode='nearest'
# )

# train_data = datagen.flow_from_directory(
#     data_dir, target_size=(128, 128), batch_size=32,
#     class_mode='categorical', subset='training'
# )

# val_data = datagen.flow_from_directory(
#     data_dir, target_size=(128, 128), batch_size=32,
#     class_mode='categorical', subset='validation'
# )

# # Save class indices
# with open("../class_indices.json", "w") as f:
#     json.dump(train_data.class_indices, f)
# print("Class indices:", train_data.class_indices)

# # Improved CNN
# model = Sequential([
#     Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
#     MaxPooling2D(2,2),
#     Conv2D(64, (3,3), activation='relu'),
#     MaxPooling2D(2,2),
#     Conv2D(128, (3,3), activation='relu'),
#     MaxPooling2D(2,2),
#     Flatten(),
#     Dense(256, activation='relu'),
#     Dropout(0.5),
#     Dense(train_data.num_classes, activation='softmax')
# ])

# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# # Callbacks
# callbacks = [
#     EarlyStopping(patience=5, restore_best_weights=True),
#     ModelCheckpoint(
#         "../best_trash_classifier.h5",
#         monitor="val_accuracy",
#         mode="max",
#         save_best_only=True
#     )
# ]

# # Train
# history = model.fit(
#     train_data, validation_data=val_data,
#     epochs=30, callbacks=callbacks
# )

# # Save final model
# model.save("../trash_classifier.h5")

# # Final accuracy check
# loss, acc = model.evaluate(val_data)
# print(f"✅ Final Validation Accuracy: {acc*100:.2f}%")

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import os, json

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, r"C:\projects\smart_waste_system\backend\dataset")   # dataset folder inside backend/
MODEL_PATH = os.path.join(BASE_DIR, "trash1_classifier.h5")
BEST_MODEL_PATH = os.path.join(BASE_DIR, "best1_trash_classifier.h5")
CLASS_INDICES_PATH = os.path.join(BASE_DIR, "class_indices.json")

# Image Data Generator
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_data = datagen.flow_from_directory(
    DATA_DIR, target_size=(128, 128), batch_size=32,
    class_mode='categorical', subset='training'
)

val_data = datagen.flow_from_directory(
    DATA_DIR, target_size=(128, 128), batch_size=32,
    class_mode='categorical', subset='validation'
)

# Save class indices
with open(CLASS_INDICES_PATH, "w") as f:
    json.dump(train_data.class_indices, f)
print("✅ Class indices saved:", train_data.class_indices)

# Model
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(train_data.num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Callbacks
callbacks = [
    EarlyStopping(patience=5, restore_best_weights=True),
    ModelCheckpoint(BEST_MODEL_PATH, monitor="val_accuracy", mode="max", save_best_only=True)
]

# Train
history = model.fit(train_data, validation_data=val_data, epochs=30, callbacks=callbacks)

# Save final model
model.save(MODEL_PATH)
print(f"✅ Model saved at {MODEL_PATH}")

# Evaluate
loss, acc = model.evaluate(val_data)
print(f"🎯 Final Validation Accuracy: {acc*100:.2f}%")

