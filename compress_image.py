 !pip install tensorflow
 import tensorflow as tf
 from tensorflow.keras import layers, Model
 import numpy as np
 import matplotlib.pyplot as plt
 from tensorflow.keras import layers, Model
 import numpy as np
 
 from sklearn.decomposition import PCA
 from sklearn.decomposition import PCA
 (train_images, _), (test_images, _) = tf.keras.datasets.mnist.load_data()
 train_images = train_images.astype('float32') / 255.0
 test_images = test_images.astype('float32') / 255.0
 flattened_images = train_images.reshape((-1, 28*28))
 pca = PCA(n_components=64)
 pca.fit(flattened_images)
 class DeepPCAAutoencoder(Model):
 def __init__(self, latent_dim):
 super(DeepPCAAutoencoder, self).__init__()
 self.latent_dim = latent_dim
 self.encoder = tf.keras.Sequential([
 layers.Flatten(),
 layers.Dense(256, activation='relu'),
 layers.Dense(128, activation='relu'),
 layers.Dense(latent_dim, activation='linear')
 ])
 self.decoder = tf.keras.Sequential([
 layers.Dense(128, activation='relu'),
 layers.Dense(256, activation='relu'),
 layers.Dense(28*28, activation='sigmoid'),
 layers.Reshape((28, 28))
 ])
 def call(self, x):
 encoded = self.encoder(x)
 decoded = self.decoder(encoded)
 return decoded

 latent_dim = 64
 batch_size = 256
 epochs = 20
 autoencoder = DeepPCAAutoencoder(latent_dim)
 autoencoder.compile(optimizer='adam', loss='mse')
 history = autoencoder.fit(
 train_images, train_images,
 epochs=epochs,
 batch_size=batch_size,
 shuffle=True,
 validation_data=(test_images, test_images)
 )
 def plot_reconstructions(model, pca, images, n=5):
 plt.figure(figsize=(15, 5))
 for i in range(n):
 ax = plt.subplot(3, n, i + 1)
 plt.imshow(images[i])
 plt.gray()
 ax.get_xaxis().set_visible(False)
 ax.get_yaxis().set_visible(False)
 reconstructed = model.predict(images[:n])
 for i in range(n):
 ax = plt.subplot(3, n, i + 1 + n)
 plt.imshow(reconstructed[i])
 plt.gray()
 ax.get_xaxis().set_visible(False)
 ax.get_yaxis().set_visible(False)
 pca_reconstructed = pca.inverse_transform(pca.transform(images[:n].reshape(n, -1
 for i in range(n):
 ax = plt.subplot(3, n, i + 1 + 2*n)
 plt.imshow(pca_reconstructed[i])
 plt.gray()
 ax.get_xaxis().set_visible(False)
 ax.get_yaxis().set_visible(False)
 plt.show()
 test_samples = test_images[:5]
 plot_reconstructions(autoencoder, pca, test_samples)
 def compress(image):
 return autoencoder.encoder(image[np.newaxis, ...]).numpy()
 def decompress(code):
 return autoencoder.decoder(code).numpy()
 original_image = test_images[0]
 compressed_code = compress(original_image)
 reconstructed_image = decompress(compressed_code)[0]
 original_size = 28 * 28
 compressed_size = latent_dim
 ratio = original_size / compressed_size
 print(f"Compression ratio: {ratio:.1f}:1")
 plt.plot(history.history['loss'], label='Training Loss')
 plt.plot(history.history['val_loss'], label='Validation Loss')
 plt.xlabel('Epoch')
 plt.ylabel('MSE Loss')
 plt.legend()
 plt.show()
   
