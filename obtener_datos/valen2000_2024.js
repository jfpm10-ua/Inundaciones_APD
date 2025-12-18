//  bounding box [W, S, E, N]
var bbox = ee.Geometry.Rectangle([-0.45092, 39.393174, -0.337967, 39.514117]);

// Variables
var variables = [
  'volumetric_soil_water_layer_1',
  'runoff',
  'surface_runoff',
  'total_evaporation',
  'surface_pressure',
  'total_precipitation'
];

//   2000 a 2024 
var era5 = ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY")
  .filterDate('2000-01-01', '2024-12-31')  // ✅ 2024 completo (2025 aún no está consolidado)
  .select(variables);

//  media espacial por hora
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
  description: 'era5_valencia_2000_2024',
  fileFormat: 'CSV'
});