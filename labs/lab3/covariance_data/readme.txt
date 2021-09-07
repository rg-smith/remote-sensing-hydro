AmeriFlux BASE data product README (last changed on 20190205)

This README file describes the AmeriFlux BASE data product available for download at http://ameriflux.lbl.gov/

By using these data files, you agree with the AmeriFlux Data Use Policy for using AmeriFlux data below; see http://ameriflux.lbl.gov/data/data-policy/

Please direct questions or suggestions about these data to ameriflux-support@lbl.gov



AMERIFLUX DATA USE POLICY

The AmeriFlux Network data offered on this website are contributed by individual AmeriFlux scientists, who share their data openly with the global community.
The AmeriFlux policy is that all data should be properly acknowledged, and that data contributors should have the opportunity to make an intellectual contribution to the papers that use their data and, as a result, have the opportunity to be a co-author.


When you use AmeriFlux data

When you download the data, use the Data Download form to describe how you plan to use the data and if you plan to use in publications. This statement is sent to the data contributor(s), and then posted to the AmeriFlux Data Download Log (https://ameriflux.lbl.gov/data/data-download-log/).
When you start an in-depth analysis that may result in a publication, contact the data contributors directly, so that they have the opportunity to contribute substantially and become a co-author.


Acknowledge AmeriFlux data in publications--
    - Cite the relevant DOI and/or recommended paper(s). Each siteâ€™s DOI is listed on its Site General Info page, DOI tab. (See http://ameriflux.lbl.gov/sites/)
    - Acknowledge funding for site support. If the data download did not provide the preferred acknowledgment language, ask the site principal investigator.
    - List each site using its AmeriFlux Site ID, either in text or in supplementary material. For reproducibility, we recommend specifying the data-years used.
    - Inform all data providers when publications are about to be published.
    - Acknowledge the AmeriFlux data resource: â€œFunding for AmeriFlux data resources was provided by the U.S. Department of Energyâ€™s Office of Science.â€
    - Use the AmeriFlux logo and/or the AmeriFlux web link (http://ameriflux.lbl.gov)
    - List AmeriFlux sites using their Site IDs and/or site name



1) OVERVIEW OF THE DATA FILE CONTENTS

This version of the AmeriFlux data files are made available at the AmeriFlux web site (http://ameriflux.lbl.gov). The BASE files follow the new AmeriFlux data format developed in partnership with the European Integrated Carbon Observation System (ICOS). For more information on the new format, please visit the Data section of the AmeriFlux web site at http://ameriflux.lbl.gov/data/




2) DATA FILE NAME

The BASE data file names have the following format:

    [publisher]_[siteID]_BASE_[resolution]_[version].csv

For instance:

    AMF_US-Ha1_BASE_HR_8-1.csv

This example file name is published by the AmeriFlux network (AMF); it has data collected at the "Harvard Forest EMS Tower (HFR1)" site (US-Ha1); it uses an hourly resolution (HR); and, its version is 8-1. For details on site IDs and versions, please see DATA FILE HEADERS below.

Note that there are only two possible temporal resolutions for BASE files: HR for hourly and HH for half-hourly. Sites can use one or both resolutions.



3) DATA FILE HEADER

The header of the data file is composed of lines starting with a hash character (#). The fields in the headers each have a label, a colon character (:), and the value of the field.

In the current version of this data product, the header is composed of two fields: Site and Version.

Site contains the site identification (ID) code in the following format (CC-SSS): two characters identifying country, a dash character (-), and three characters identifying the site. For instance, US-Ha1 is the site ID for the "Harvard Forest EMS Tower (HFR1)" site located in the United States.

The Version contains two components (Data-Processing):
    - Data version - This number corresponds to the site teamâ€™s data submission, and is incremented whenever the corresponding BASE data source comes from a newer source.
    - Processing version - This corresponds to the version of the data processing pipeline used to generate the BASE data product. Changes to the data processing pipeline will be noted in the AmeriFlux Data Change Log: http://ameriflux.lbl.gov/data/data-change-log/

Sample BASE data file header:

   # Site: US-Ha1
   # Version: 8-1



4) DATA FILE CONTENTS

The BASE data files follow the new AmeriFlux and ICOS agreed standard for variable names (i.e., FP data format). One feature of the new FP data format is the addition of more supporting variables (e.g., FCH4, see VARIABLE LIST below). Another feature is the use of suffixes for providing additional information about the variable. Most common suffixes include the gap-filled suffix (_PI_F), positional suffix (_<H>_<V>_<R>), and layer-aggregated suffix (_<#>) (See VARIABLE QUALIFIER below). Timestamps are specified in truncated ISO format with both the start and end timestamps of the averaging period.

The number and order of columns in these files is not guaranteed to be uniform, except that timestamps (i.e., TIMESTAMP_START, TIMESTAMP_END) are always located in the first two columns. The first row after the headers provides the variable labels (see VARIABLE LIST below).

These data files are provided as plain ASCII text using comma-separated values (CSV) formating. Missing data records are indicated by the -9999 value.

For more information on formats and variables, please visit the Data section of the AmeriFlux Web site at http://ameriflux.lbl.gov/data/



5) VARIABLE LIST (Selected)

Most common variables, units (in parenthesis) and descriptions are listed below. For a full list of variables supported, please check the BASE variable names at https://ameriflux.lbl.gov/data/aboutdata/data-variables/#base.

-- TIMEKEEPING
TIMESTAMP_START (YYYYMMDDHHMM): ISO timestamp start of averaging period
TIMESTAMP_END   (YYYYMMDDHHMM): ISO timestamp end of averaging period

-- GASES
CO2         (umolCO2 mol-1): Carbon Dioxide (CO2) mole fraction
H2O           (mmolH2O mol-1): Water (H2O) vapor mole fraction
CH4        (nmolCH4 mol-1): Methane (CH4) mole fraction
FC            (umolCO2 m-2 s-1): Carbon Dioxide (CO2) flux
SC            (umolCO2 m-2 s-1): Carbon Dioxide (CO2) storage flux
FCH4        (nmolCH4 m-2 s-1): Methane (CH4) flux
SCH4        (nmolCH4 m-2 s-1): Methane (CH4) storage flux

-- HEAT
G           (W m-2): Soil heat flux
H           (W m-2): Sensible heat flux
LE          (W m-2): Latent heat flux
SH          (W m-2): Heat storage in the air
SLE         (W m-2): Latent heat storage flux

-- MET_WIND
WD            (Decimal degrees): Wind direction
WS            (m s-1): Wind speed
USTAR    (m s-1): Friction velocity
ZL            (adimensional): Stability parameter

-- MET_ATM
PA             (kPa): Atmospheric pressure
RH             (%): Relative humidity, range 0-100
TA             (deg C): Air temperature
VPD        (hPa): Vapor Pressure Deficit

-- MET_SOIL
SWC        (%): Soil water content (volumetric), range 0-100
TS          (deg C): Soil temperature
WTD        (m): Water table depth

-- MET_RAD
NETRAD       (W m-2): Net radiation
PPFD_IN      (umolPhoton m-2 s-1): Photosynthetic photon flux density, incoming
PPFD_OUT     (umolPhoton m-2 s-1): Photosynthetic photon flux density, outgoing
SW_IN       (W m-2): Shortwave radiation, incoming
SW_OUT       (W m-2): Shortwave radiation, outgoing
LW_IN        (W m-2): Longwave radiation, incoming
LW_OUT      (W m-2): Longwave radiation, outgoing

-- MET_PRECIP
P              (mm): Precipitation

-- PRODUCTS
NEE        (umolCO2 m-2 s-1): Net Ecosystem Exchange
RECO        (umolCO2 m-2 s-1): Ecosystem Respiration
GPP        (umolCO2 m-2 s-1): Gross Primary Productivity



6) VARIABLE QUALIFIER

Qualifiers are suffixes appended to variable base names that provide additional information about the variable.

_PI (Provided by PI / tower team)
Details: _PI indicates a variable that has been QA/QC filtered, spatially-aggregated, or calculated by the tower team.

_PI_F (Gap-filled variable)
Details: _PI_F indicates that the variable has been gap-filled by the tower team.

_<H>_<V>_<R> (Position qualifier)
Details: The three components of the qualifier are indices that indicate an observationâ€™s spatial position. In other words, the indices describe the position of a sensor relative to other sensors that measure the same variable within a site, i.e., Horizontal position (_<H>), Vertical position (_<V>), Replicate (_<R>). The letters H, V, and R are to be replaced with integer values to represent, e.g., TS_1_1_1, TS_1_1_2, TS_1_2_1


_PI_<H>_<V>_A (Aggregation of replicates)
Details: If replicates can be aggregated, they are averaged, and the result is reported with the Replicate index of the _<H>_<V>_<R> position qualifier replaced with the letter A. _PI means the variable is aggregated by the tower team. Continuing the example above, if the TS_1_1_1 and TS_1_1_2 can be averaged, the result will be named TS_PI_1_1_A.

_PI_<#> (Aggregation layer index)
Details: Variables with the same base name and the same height / depth but different horizontal positions can be aggregated. This aggregation across a horizontal plane represents the footprint at a given layer. _PI means the variable is aggregated by the tower team. The <#> qualifier is replaced by a numerical index indicating the layerâ€™s relative height / depth position, e.g., TS_PI_1

For height / depth and instrument model information, see the Measurement Height page (https://ameriflux.lbl.gov/data/measurement-height/)
