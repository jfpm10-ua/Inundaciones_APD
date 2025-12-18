// Bounding box Houston [W, S, E, N]
var bbox = ee.Geometry.Rectangle([
  -95.752164, 29.560771,
  -95.024319, 30.042206
]);

// Variables
var variables = [
  'volumetric_soil_water_layer_1',
  'runoff',
  'surface_runoff',
  'total_evaporation',
  'surface_pressure',
  'total_precipitation'
];

// ERA5-Land 2000–2024
var era5 = ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY")
  .filterDate('2000-01-01', '2024-12-31')
  .select(variables);

// Media espacial por hora
var ts = era5.map(function(img) {
  var stats = img.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: bbox,
    scale: 9000,
    maxPixels: 1e9
  });
  return ee.Feature(null, stats)
    .set({
      'timestamp': img.date().format('YYYY-MM-dd HH:mm:ss')
    });
});

// Exportar a CSV
Export.table.toDrive({
  collection: ts,
  description: 'era5_houston_2000_2024',
  fileFormat: 'CSV'
});
