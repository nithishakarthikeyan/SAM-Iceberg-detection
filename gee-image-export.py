// Load Sentinel-1 Ground Range Detected (GRD) collection
var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
            .filterBounds(ee.Geometry.Point([-102.2661, -74.4413]))  // Thwaites region
            .filterDate('2019-02-01', '2019-02-28') // Feb 2019
            .filter(ee.Filter.eq('instrumentMode', 'IW'))  // Interferometric Wide swath
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'HH')) // Use VV
            .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING')); // Adjust if needed

// Take median to reduce noise
var composite = s1.median().select('HH');

// Define region of interest (small bounding box around coordinates)
var point = ee.Geometry.Point([-102.26612818779797, -74.44129673242924]);
var region = point.buffer(2500).bounds();

// Print for inspection
print('Sentinel-1 composite:', composite);

// Visualization for sanity check
Map.centerObject(region, 9);
Map.addLayer(composite.clip(region), {min: -25, max: 0}, 'S1 HH Feb 2019');

// Export to your GEE Assets
Export.image.toAsset({
  image: composite.clip(region),
  description: 'thwaites_feb_2019',
  assetId: 'projects/ee-nithishak02/assets/thwaites_feb_2019',
  scale: 10,
  region: region,
  maxPixels: 1e13
});

