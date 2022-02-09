### Container information

Data are stored in blobs in the West Europe Azure region, in the following blob container:

`https://sentinel2l2a01.blob.core.windows.net/sentinel2-l2`


### Scene names

Within that container, each scene corresponds to a folder, named according to:

`[UTM longitude zone]/[MGRS latitude band]/[tile code]/[year]/[month]/[day]/[scene name]`

* `UTM longitude zone` is a two-digit [UTM longitude code](https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system) from 01 to 60
* `MGRS latitude band` is a one-letter [UTM latitude code](https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system#Latitude_bands_2), from "C" to "X" (except "I" and "O")
* `tile code` is a two-letter code from the Sentinel-2 tiling grid ([kml](https://sentinel.esa.int/documents/247904/1955685/S2A_OPER_GIP_TILPAR_MPC__20151209T095117_V20150622T000000_21000101T000000_B00.kml),[geojson](https://github.com/bencevans/sentinel-2-grid)), which is aligned to the [Military Grid Reference System](https://en.wikipedia.org/wiki/Military_Grid_Reference_System)
* `year`, `month`, and `day` are zero-padded to four, two, and two digits respectively

`scene name` follows the [Sentinel-2 scene name convention](https://sentinel.esa.int/web/sentinel/user-guides/sentinel-2-msi/naming-convention):

`MMM_MSIXXX_YYYYMMDDTHHMMSS_Nxxyy_ROOO_Txxxxx_[Product Discriminator].SAFE`

* `MMM` is satellite (S2A or S2B)
* `MSIXXX` is always "MSIL2A", indicating the Level-2A product level
* `YYYYMMDDTHHMMSS` is the sensing start time (UTC)
* `Nxxyy` indicates the version of the processing toolset
* `ROOO` is the [relative orbit number](https://sentinel.esa.int/web/sentinel/missions/sentinel-2/satellite-description/orbit), from R001 to R143
* `Txxxxx` is the five-digit tile identifier, will match the UTM longitude zone, MGRS latitude band, and two-letter tile code from the folder name
* `Product discriminator` is a processing date

Putting that all together, a complete scene folder looks like:

`https://sentinel2l2a01.blob.core.windows.net/sentinel2-l2/11/C/MM/2020/11/26/S2B_MSIL2A_20201126T154319_N0212_R125_T11CMM_20201127T152008.SAFE`


### Image files

Within a scene folder, recursively listing *.tif will enumerate all images, with suffixes indicating bands according to the following; all of these files will be within the `GRANULE/[scene id]/IMG_DATA` folder:

* `R10m/AOT_10m`: aerosol optical thickness (10m)
* `R10m/BO2_10m`: band 2 (490nm) (blue) (10m)
* `R10m/BO3_10m`: band 3 (560nm) (green) (10m)
* `R10m/BO4_10m`: band 4 (665nm) (red) (10m)
* `R10m/BO8_10m`: band 8 (842nm) (near IR) (10m)
* `R10m/TCI_10m`: true color image (10m)
* `R10m/WVP_10m`: water vapor (10m)
<br/><br/>
* `R20m/BO5_20m`: band 5 (705nm) (vegetation classification) (20m)
* `R20m/BO6_20m`: band 6 (740nm) (vegetation classification) (20m)
* `R20m/BO7_20m`: band 7 (783nm) (vegetation classification) (20m)
* `R20m/B8A_20m`: band 8A (865nm) (vegetation classification) (20m)
* `R20m/B11_20m`: band 11 (1610nm) (snow/ice/cloud classification) (20m)
* `R20m/B12_20m`: band 12 (2190nm) (snow/ice/cloud classification) (20m)
* `R20m/SCL_20m`: scene classification (20m)
<br/><br/>
* `R60m/BO1_60m`: band 1 (443nm) (coastal aerosol (60m)
* `R60m/BO9_60m`: band 9 (945nm) (water vapor) (60m)

For example, the 10m image for band 2 in the example scene above is at:

`https://sentinel2l2a01.blob.core.windows.net/sentinel2-l2/11/C/MM/2020/11/26/S2B_MSIL2A_20201126T154319_N0212_R125_T11CMM_20201127T152008.SAFE/GRANULE/L2A_T11CMM_A019456_20201126T154359/IMG_DATA/R10m/T11CMM_20201126T154319_B02_10m.tif`

### Metadata files

Metadata files follow the [Sentinel-2 L2A product specification](https://sentinel.esa.int/documents/247904/685211/Sentinel-2-Products-Specification-Document); see the specification for complete documentation of both data and metadata.

This section will provide a short summary of each file within each scene folder.  It looks like a lot, but most use cases only require the image files described above.  Some use cases may require the following files as well:

* `manifest.safe`: index file listing all files in this scene and their checksums... basically the machine-readable version of this section of the documentation.

* `MTD_MSIL2A.xml`: metadata associated with the level-2 product, including reserved values for missing data and saturation (always 0 and 65535, respectively), reflectance calibration information, and percentages of cloud cover, shadow cover, etc.

* `GRANULE/[scene id]/QI_DATA/*`...
  * `MASK_CLDPRB_20m.tif`: cloud probabilities for each pixel, at 20m resolution
  * `MASK_CLDPRB_60m.tif`: cloud probabilities for each pixel, at 60m resolution
  * `MASK_SNWPRB_20m.tif`: snow  probabilities for each pixel, at 20m resolution
  * `MASK_SNWPRB_60m.tif`: snow probabilities for each pixel, at 60m resolution
  * `MSK_DDVPXL_20m.tif`: masks indicating pixels that are likely either shadows or "dark dense vegetation", at 20m resolution
  * `MSK_DDVPXL_60m.tif`: masks indicating pixels that are likely either shadows or "dark dense vegetation", at 60m resolution

...and for the curious mind, the scene folder also contains the following files that most applications are very unlikely to need:

* `scenefilelist.txt`: flat list of all files available in this scene
* `DATASTRIP/[scene id]/MTD_DS.xml`: low-level scene metadata following the [L2A datastrip XML schema](https://psd-14.sentinel2.eo.esa.int/PSD/S2_PDI_Level-2A_Datastrip_Metadata.xsd)
* `GRANULE/[scene id]/AUX_DATA/AUX_ECMWFT`: binary auxiliary file
* `GRANULE/[scene id]/QI_DATA/*`: quality information
  * `FORMAT_CORRECTNESS.xml`: low-level integrity information... basically "are all the files here that are supposed to be here?"
  * `GENERAL_QUALITY.xml`: low-level quality verification, e.g. validation that the solar zenith angle was within tolerance and that no data was lost during transmission.
  * `GEOMETRIC_QUALITY.xml`: low-level geometry verification, i.e. validation that the dimensions of the tiles are what they're supposed to be
  * `MSK_CLOUDS_B00.gml`: a mask listing all of the likely cloud pixels, in [GML](https://www.ogc.org/standards/gml) format
  * `MSK_DEFECT_B**` (12 files): a mask for each band listing defective pixels, in [GML](https://www.ogc.org/standards/gml) format
  * `MSK_DETFOO_B**` (12 files): a mask for each band indicating the ground footprint for this band, in [GML](https://www.ogc.org/standards/gml) format
  * `MSK_NODATA_B**` (12 files): a mask for each band listing pixels that have no data for this scene, in [GML](https://www.ogc.org/standards/gml) format
  * `MSK_SATURA_B**` (12 files): a mask for each band listing pixels for which this band's sensor was saturated, in [GML](https://www.ogc.org/standards/gml) format
  * `MSK_TECQUA_B**` (12 files): a list of polygons for each band listing areas in this image where quality may be degraded, in [GML](https://www.ogc.org/standards/gml) format
  * `T..._PVI.tif`: RGB preview image in ground geometry
* `GRANULE/[scene id]/MTD_TL.xml`: tile metadata (e.g. geometry), following the [Sentinel-2 L2A tile metadata XML schema](https://psd-14.sentinel2.eo.esa.int/PSD/S2_PDI_Level-2A_Tile_Metadata.xsd)
* `rep_info/*.xsd` (3 files): XML schemas for datastrip and tile metadata (the same schemas used for the .xml files listed above)
* `INSPIRE.xml`: metadata file indicating compliance with the [INSPIRE schema](https://inspire.ec.europa.eu/XML-Schemas/Data-Specifications/2892)