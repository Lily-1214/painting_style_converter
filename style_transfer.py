# style_transfer.py
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image

# 스타일 변환 모델 (TensorFlow Hub)
STYLE_MODEL_URL = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
hub_model = hub.load(STYLE_MODEL_URL)

def load_img(path_to_img, max_dim=512):
    img = Image.open(path_to_img).convert('RGB')
    img = img.resize((max_dim, max_dim))
    img = np.array(img) / 255.0
    img = img[tf.newaxis, ...]
    return tf.convert_to_tensor(img, dtype=tf.float32)

def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = tf.clip_by_value(tensor, 0, 255)
    array = tensor.numpy().astype(np.uint8)[0]
    return Image.fromarray(array)

def apply_style(content_img_path, style_img_path, output_path="styled_output.jpg"):
    content_image = load_img(content_img_path)
    style_image = load_img(style_img_path)
    stylized_image = hub_model(content_image, style_image)[0]
    result_img = tensor_to_image(stylized_image)
    result_img.save(output_path)
    print(f"✅ 스타일 적용 완료 → {output_path}")
