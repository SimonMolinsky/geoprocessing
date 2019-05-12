"""Script for cutting raster image into quadrants with georefernce.
Developed by: Szymon Moliński (s.molinski@datalions.eu)
Date of last review: 12.05.2019
Reviewed by: Szymon Moliński (s.molinski@datalions.eu)"""


import affine
import numpy as np
import rasterio as rio

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")


class ImageForClipModel:

    # Get band, band shape, dtype, crs and transform values
    def __init__(self, image_address):
        with rio.open(image_address, 'r') as f:
            self.band = f.read(1)
            self.crs = f.crs
            self.base_transform = f.transform
        self.band_shape = self.band.shape
        self.band_dtype = self.band.dtype
        self.clipped_images = []

    # Function for clipping band
    def clip_raster(self, height, width, buffer, save=False, prefix='clipped_band_', pass_empty=False):
        row_position = 0
        while row_position < self.band_shape[0]:
            col_position = 0
            while col_position < self.band_shape[1]:
                clipped_image = self.band[row_position:row_position + height,
                                col_position:col_position + width]

                # Check if frame is empty
                if pass_empty:
                    if np.mean(clipped_image) == 0:
                        print('Empty frame, not saved')
                        break

                # Positioning
                tcol, trow = self.base_transform * (col_position, row_position)
                new_transform = affine.Affine(self.base_transform[0], self.base_transform[1], tcol,
                                              self.base_transform[3], self.base_transform[4], trow)
                image = [clipped_image, self.crs, new_transform,
                         clipped_image.shape[0], clipped_image.shape[1],
                         self.band_dtype]

                # Save or append into a set
                if save:
                    filename = prefix + 'x_' + str(col_position) + '_y_' + str(row_position) + '.tif'
                    with rio.open(filename, 'w', driver='GTiff', height=image[3],
                                  width=image[4], count=1, dtype=image[5],
                                  crs=image[1], transform=image[2]) as dst:
                        dst.write(image[0], 1)
                    print('Image {} saved successfully'.format(filename))
                else:
                    self.clipped_images.append(clipped_image)
                    print('Image {} added to set'.format('0'))

                # Update column position
                col_position = col_position + width - buffer

            # Update row position
            row_position = row_position + height - buffer

        if save:
            print('Process ended with success')
            return 0
        else:
            return self.clipped_images
