# Download H5 datasets from SUOMI NPP NASA Satellite about Etna
This is an automatic H5 datasets downloader about Etna from an NASA polar-orbit satellite.
It's write in Python 2.7 

## SUOMI NPP Info
The Suomi NPP is the first in a new generation of satellites intended to replace the Earth Observing System satellites, which were launched from 1997 to 2011. The satellite orbits the Earth about 14 times each day. Its five imaging systems include:

*    **Advanced Technology Microwave Sounder (ATMS)**, a microwave radiometer which will help create global moisture and temperature models
*    **Cross-track Infrared Sounder (CrIS)**, a Michelson interferometer to monitor moisture and pressure
*    **Ozone Mapping and Profiler Suite (OMPS)**, a group of imaging spectrometers to measure ozone levels, especially near the poles
*    **Visible Infrared Imaging Radiometer Suite (VIIRS)**, a 22-band radiometer to collect infrared and visible light data to observe weather, climate, oceans, nightlight, wildfires, movement of ice, and changes in vegetation and landforms
*    **Clouds and the Earth's Radiant Energy System (CERES)**, a radiometer to detect thermal radiation, including reflected solar radiation and thermal radiation emitted by the Earth

It scan an image every 6 minutes and upload all the data 2 times a day

## Satellite orbit concerning Etna
It passes from Etna 2-4 times therefore there are a limitated information that can be downloaded.
Through empirical analysis I found out that it passing always in the same range of hours(11.00-13.00 and 00.00-02.00)

## Site Dependences
*	**Server FTP:"ftp-npp.bou.class.noaa.gov"**,where take all the datasets
* 	**NASA Site:"ladsweb.modaps.eosdis.nasa.gov/archive/"**, where take orbit satellite informations (geolocation over time), useful to known in which hours search the datasets in the FTP server


# Instructions for Use
There are 2 way that you can run main.py:
*	**Specifyng the date in the first parameter**: you can specify the date from where to download h5 datasets(format: YYYY-MM-DD)
*	**Without specifyng on the date**:the program will use the current date

Others exchangeable parameters of EstrazioneH5 init in main.py:
*	**rang(range)**: number between 0 and 1 (0<=rang<1) that specify from which index start take the request data and when it must stopped.***Remember that a big range may not let you find any good files, futhermore it's important set a small rang to prevent dirty H5 files!***. Recommended rang are = 0 (no range,take all the data),1/float(8) (very small range)

*	**tip(Type of data)**: specify the data that it can be downloaded from the Suomi NPP.Select one of these in below:
	* VIIRS-Day-Night-Band-SDR
	* VIIRS-Day-Night-Band-SDR-Ellipsoid-Geo
	* VIIRS-Image-Bands-SDR-Ellipsoid-Geo
	* VIIRS-Image-Band-SDR-Ellipsoid-Terrain-Corrected-Geo
	* VIIRS-Imagery-Band-01-SDR
	* VIIRS-Imagery-Band-02-SDR
	* VIIRS-Imagery-Band-03-SDR
	* VIIRS-Imagery-Band-04-SDR
    * VIIRS-Imagery-Band-05-SDR
	* VIIRS-Moderate-Bands-SDR-Geo
	* VIIRS-Moderate-Bands-SDR-Terrian-Corrected-Geo
	* VIIRS-Moderate-Resolution-Band-03-SDR
	* VIIRS-Moderate-Resolution-Band-04-SDR
	* VIIRS-Moderate-Resolution-Band-05-SDR
	* VIIRS-Moderate-Resolution-Band-07-SDR
	* VIIRS-Moderate-Resolution-Band-08-SDR
	* VIIRS-Moderate-Resolution-Band-10-SDR
	* VIIRS-Moderate-Resolution-Band-11-SDR
	* VIIRS-Moderate-Resolution-Band-12-SDR
	* VIIRS-Moderate-Resolution-Band-13-SDR
	* VIIRS-Moderate-Resolution-Band-14-SDR
	* VIIRS-Moderate-Resolution-Band-15-SDR
	* VIIRS-Moderate-Resolution-Band-16-SDR






