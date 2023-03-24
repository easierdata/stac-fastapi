import numpy as np
import rasterio
import subprocess
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib.colors as mcolors
from pystac_client import Client
from IPython.display import Image

# Connect to STAC API and search for Landsat 9 imagery
catalog = Client.open("http://ec2-54-172-212-55.compute-1.amazonaws.com/api/v1/pgstac/")
bbox = [-76.964657, 38.978967, -76.928008, 39.002783]

search = catalog.search(
    collections=["landsat-c2l1"],
    bbox=bbox,
)

items = search.get_all_items()

item = items[0]
# Get red and NIR band assets and access alternate keys
red_band_cid = item.assets["red"].extra_fields["alternate"]["IPFS"]["href"].split("/")[-1]
nir_band_cid = item.assets["nir08"].extra_fields["alternate"]["IPFS"]["href"].split("/")[-1]

print(f"Red band CID: {red_band_cid}")
print(f"NIR band CID: {nir_band_cid}")


def load_landsat_band(band: bytes) -> np.ndarray:
    with rasterio.MemoryFile(band) as memfile:
        with memfile.open() as dataset:
            return dataset.read(1)


def save_plot_to_buffer(plot: plt.Figure) -> bytes:
    buffer = BytesIO()
    plot.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer.getvalue()


# Load the red and NIR bands from IPFS
red_band = subprocess.check_output(["ipfs", "cat", red_band_cid])
nir_band = subprocess.check_output(["ipfs", "cat", nir_band_cid])

# Convert the bands to numpy arrays
red_band_4 = load_landsat_band(red_band)
nir_band_5 = load_landsat_band(nir_band)

# Calculate the NDVI
eps = 0.0001 # Avoid divide by zero errors
ndvi = (nir_band_5 - red_band_4) / (nir_band_5 + red_band_4 + eps)

# Set min and max values for better color differentiation
ndvi_min, ndvi_max = -1, 1

# Create a custom color map
cmap = plt.cm.RdYlGn
norm = mcolors.Normalize(vmin=ndvi_min, vmax=ndvi_max)

# Plot the NDVI image
fig, ax = plt.subplots()
im = ax.imshow(ndvi, cmap=cmap, norm=norm)
cbar = fig.colorbar(im, ax=ax, label='NDVI', cmap=cmap, norm=norm)
ax.set_title('Normalized Difference Vegetation Index (NDVI)')

# Save the plot to a BytesIO buffer
plot_buffer = save_plot_to_buffer(fig)

# Upload the image buffer to IPFS and get the hash
ipfs_hash = subprocess.check_output(["ipfs", "add", "-q"], input=plot_buffer).decode().strip()

# Fetch the plot from IPFS
ipfs_plot_png = subprocess.check_output(["ipfs", "cat", ipfs_hash])

ipfs_plot_png
