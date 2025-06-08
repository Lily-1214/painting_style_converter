# classify.py
import tensorflow as tf
from tensorflow.keras import layers, models
import os

def build_model(input_shape=(256, 256, 3), num_classes=10):
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False  # 전이학습용으로 고정

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

def load_datasets(data_dir='artbench-10', img_size=(256, 256), batch_size=32):
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        os.path.join(data_dir, 'train'),
        image_size=img_size,
        batch_size=batch_size
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        os.path.join(data_dir, 'test'),
        image_size=img_size,
        batch_size=batch_size
    )
    class_names = train_ds.class_names
    return train_ds, val_ds, class_names

def train_model():
    train_ds, val_ds, class_names = load_datasets()
    model = build_model(num_classes=len(class_names))
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(train_ds, validation_data=val_ds, epochs=5)
    model.save('model/style_classifier.h5')
    print("✅ 모델 저장 완료: model/style_classifier.h5")

if __name__ == "__main__":
    train_model()
