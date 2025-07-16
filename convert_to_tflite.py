
import tensorflow as tf

# Load your existing Keras model
model = tf.keras.models.load_model('newImage_classify.keras')

# Convert to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Optimize for size and speed

# Convert the model
tflite_model = converter.convert()

# Save the TFLite model
with open('newImage_classify.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model converted to TFLite format: newImage_classify.tflite")
print(f"Original model size: {os.path.getsize('newImage_classify.keras') / 1024 / 1024:.2f} MB")
print(f"TFLite model size: {len(tflite_model) / 1024 / 1024:.2f} MB")
