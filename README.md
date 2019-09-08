# GeoJSON Formatter

## Overview
With reference to the [SalesForce Trailhead](https://trailhead.salesforce.com/en/content/learn/projects/wave_charts_custom_map/wave_charts_custom_map_geojson),
this Python script will format an input GeoJSON file to be compatible with the source dataset required
from Einstein Analytics custom map charts.

## Requirements
- Python3

## Usage
```
python3 GeoJsonFormatter.py <source_file_path> <properties_field> [polygon_decimal_points] [delete_properties]
```
- polygon_decimal_points is optional, default = 4
- delete_properties is optional, default = False

### Example:
The following example takes an input file called ```inputfile.geojson```.  The ```place_id``` property under
```properties``` will be moved to the same level as ```features``` and the key will be renamed to ```id```.
Each polygon coordinate will be updated to 2 decimal points, and the ```properties``` object will be removed
from the file.
#### Command
```
python3 GeoJsonFormatter.py /Users/JSmith/Downloads/inputfile.geojson place_id 2 True
```
#### Terminal Output:
```
Input File Location: /Users/JSmith/Downloads/inputfile.geojson
Input File Size: 154 MB

--- Loading GeoJSON file...
--- Moving place_id field for SalesForce Einstein Analytics Compatibility...
--- Saving geojson file...

Output File Location: /Users/JSmith/Downloads/inputfile_FORMATTED.geojson
Output File Size: 27 MB

GeoJSON Conversion Complete
```

## Disclaimer
This solution is purely tactical and I offer no support of the code in use.  I will periodically review any PR's/issues/comments
and make any commits as necessary.