!git clone https://github.com/cheginit/samgeo.git
%cd samgeo
!pip install . --no-deps
!pip install geopandas rasterio matplotlib segment-geospatial

import geemap
import ee
ee.Authenticate()
ee.Initialize(project='ee-nithishak02')



# Load the specific image asset
image = ee.Image("projects/ee-nithishak02/assets/thwaites_feb_2019")

# Check the bands
print("Bands:", image.bandNames().getInfo())



# Define a small bounding box around your coordinates (about 5 km across)
point = ee.Geometry.Point([-102.26612818779797, -74.44129673242924])
region = point.buffer(2500).bounds()  # buffer in meters → bounds gives rectangle

# Clip the image to this small region
clipped = image.clip(region)

# Path to save the output
output_tif = "/content/thwaites_feb_2019_clip.tif"

# Export the clipped image
geemap.ee_export_image(
    clipped.select(['HH']),  # Select band if needed
    filename=output_tif,
    scale=10,
    region=region,
    file_per_band=False
)

import os
print("Exists:", os.path.exists(output_tif))
print("Size:", os.path.getsize(output_tif) if os.path.exists(output_tif) else "No file")


# Convert HH band to RGB-friendly format (0–255)
vis_params = {
    'min': -25,  # adjust to your SAR histogram
    'max': 0,
}
rgb_image = clipped.select('HH').visualize(**vis_params)

# Export the visualization instead of raw SAR
geemap.ee_export_image(
    rgb_image,
    filename=output_tif,
    scale=10,
    region=region
)


!pip install git+https://github.com/cheginit/samgeo.git

from samgeo import SamGeo
sam = SamGeo(model_type="vit_h")  # highest quality model


sam.generate(
    source=output_tif,
    output="/content/thwaites_feb_2019_clip_mask.tif"
)



import matplotlib.pyplot as plt
import rasterio

# Read the SAM mask
mask_path = "/content/thwaites_feb_2019_clip_mask.tif"
with rasterio.open(mask_path) as src:
    mask = src.read(1)  # first band

# Plot it
plt.figure(figsize=(10, 10))
plt.imshow(mask, cmap='tab20')
plt.title("SAM Feb 2019")
plt.axis("off")
plt.show()


with rasterio.open(output_tif) as src:
    img = src.read(1)  # HH grayscale

plt.figure(figsize=(10, 10))
plt.imshow(img, cmap='gray')
plt.imshow(mask, cmap='tab20', alpha=0.5)  # transparent overlay
plt.title("Icebergs Detected Feb 2019")
plt.axis("off")
plt.show()


import rasterio
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

# Load your segmented mask (each iceberg is uniquely labeled)
# If you have just a binary mask, use label() to separate connected components
mask = rasterio.open("/content/thwaites_feb_2019_clip_mask.tif").read(1)  

# If it's binary (0 = background, 1 = iceberg), label connected components
if mask.max() == 1:
    labeled = label(mask)
else:
    labeled = mask  # already labeled by SAM
     
# Compute properties of each iceberg
regions = regionprops(labeled)

# Compute areas (in pixels first)
areas_px = [r.area for r in regions]


# Convert pixels → area (km²)
pixel_size = 10  # Sentinel-1 at 10m
areas_km2 = [(a * (pixel_size**2)) / 1e6 for a in areas_px]

# Create histogram bins
bins = [0, 1, 5, 10, 20, 50, 100]  # km² ranges
hist, edges = np.histogram(areas_km2, bins=bins)

# Plot histogram
plt.figure(figsize=(8, 6))
plt.bar(range(len(hist)), hist, width=0.8, align="center")
plt.xticks(range(len(hist)), [f"{edges[i]}–{edges[i+1]} km²" for i in range(len(hist))], rotation=45)
plt.ylabel("Number of Icebergs")
plt.title("Iceberg Size Distribution (Feb 2019)")
plt.show()

# Define a small bounding box around your coordinates (about 5 km across)
point = ee.Geometry.Point([-102.26612818779797, -74.44129673242924])
region = point.buffer(2500).bounds()  # buffer in meters → bounds gives rectangle

# Clip the image to this small region
clipped = image.clip(region)

# Path to save the output
output_tif = "/content/thwaites_feb_2016_clip.tif"

# Export the clipped image
geemap.ee_export_image(
    clipped.select(['HH']),  # Select band if needed
    filename=output_tif,
    scale=10,
    region=region,
    file_per_band=False
)

import os
print("Exists:", os.path.exists(output_tif))
print("Size:", os.path.getsize(output_tif) if os.path.exists(output_tif) else "No file")

# Convert HH band to RGB-friendly format (0–255)
vis_params = {
    'min': -25,  # adjust to your SAR histogram
    'max': 0,
}
rgb_image = clipped.select('HH').visualize(**vis_params)

# Export the visualization instead of raw SAR
geemap.ee_export_image(
    rgb_image,
    filename=output_tif,
    scale=10,
    region=region
)


sam.generate(
    source=output_tif,
    output="/content/thwaites_feb_2016_clip_mask.tif"
)

import matplotlib.pyplot as plt
import rasterio

# Read the SAM mask
mask_path = "/content/thwaites_feb_2016_clip_mask.tif"
with rasterio.open(mask_path) as src:
    mask = src.read(1)  # first band

# Plot it
plt.figure(figsize=(10, 10))
plt.imshow(mask, cmap='tab20')
plt.title("SAM Iceberg Segmentation")
plt.axis("off")
plt.show()


with rasterio.open(output_tif) as src:
    img = src.read(1)  # HH grayscale

plt.figure(figsize=(10, 10))
plt.imshow(img, cmap='gray')
plt.imshow(mask, cmap='tab20', alpha=0.5)  # transparent overlay
plt.title("Icebergs Detected Feb 2016")
plt.axis("off")
plt.show()

