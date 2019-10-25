import os
import numpy as np
import rasterio as rio
import matplotlib.pyplot as plt


def read_images(folder_name, file_end):
    file_list = os.listdir(folder_name)
    channel_list = []
    for f in file_list:
        if f.endswith(file_end):
            channel_list.append(folder_name + f)
    channel_list.sort()
    return channel_list


def show_band(band, nan_val=0, color_map='Set1', title=None):
    band = band.astype(np.float)
    band[band == nan_val] = np.nan
    plt.figure(figsize=(11, 11))
    image_layer = plt.imshow(band)
    image_layer.set_cmap(color_map)
    plt.colorbar()
    if title is not None:
        plt.title(title)
    plt.show()


if __name__ == '__main__':
    images = read_images('ffi_output/', '.tiff')
    for img in images:
        with rio.open(img) as src:
            image = src.read(1)
            show_band(image, nan_val=0, color_map='Set1', title=img)
