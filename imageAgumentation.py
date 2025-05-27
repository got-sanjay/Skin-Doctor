from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, save_img # type: ignore
import os


aug = ImageDataGenerator(
    rotation_range=30,
    zoom_range=0.3,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
)

input_dir = 'dataset/Folliculitis'   # class with few images
save_dir = 'dataset/Folliculitis'    # same folder or separate one

images = os.listdir(input_dir)

for image in images:
    img_path = os.path.join(input_dir, image)
    img = load_img(img_path, target_size=(128, 128))
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)

    # Save 20 augmented images
    AUG_COUNT = 20
    i = 0
    for batch in aug.flow(x, batch_size=1, save_to_dir=save_dir, save_prefix=save_dir.split('/')[-1], save_format='jpg'):
        i += 1
        if i >= AUG_COUNT:
            break
else:
    print(f'{' FINISHED ':=^50}')