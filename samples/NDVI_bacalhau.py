import rasterio
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import glob
import os


def load_landsat_bands(pattern, input_dir):
    # Load Landsat bands from input directory
    red_file, nir_file = sorted(glob.glob(os.path.join(input_dir, pattern)))
    with rasterio.open(red_file) as red_src:
        red_band = red_src.read(1)

    with rasterio.open(nir_file) as nir_src:
        nir_band = nir_src.read(1)

    return red_band, nir_band

if __name__ == "__main__":
    input_dir = os.path.join(os.getcwd(), "inputs")
    pattern = "LC09_L1TP_015033_20221015_20221015_02_T1_B*.TIF"

    # Load Landsat bands
    red_band_4, nir_band_5 = load_landsat_bands(pattern, input_dir)

    # Calculate NDVI
    eps = 0.0001 # Avoid divide by zero errors
    ndvi = (nir_band_5 - red_band_4) / (nir_band_5 + red_band_4 + eps)

    # Set min and max values for better color differentiation
    ndvi_min, ndvi_max = -1, 1

    # Create a custom color map
    cmap = plt.cm.RdYlGn
    norm = mcolors.Normalize(vmin=ndvi_min, vmax=ndvi_max)

    # Plot NDVI image
    plt.imshow(ndvi, cmap=cmap, norm=norm)
    plt.colorbar(label='NDVI', cmap=cmap, norm=norm)
    plt.title('Normalized Difference Vegetation Index (NDVI)')

    # Save Plot
    plt.savefig('outputs/ndvi_bacalhau.png')
    print(os.listdir('outputs'))