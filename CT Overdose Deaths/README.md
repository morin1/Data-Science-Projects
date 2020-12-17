# Connecticut accidental overdose deaths
### Exploring the "Accidental_Drug_Related_Deaths_2012_2018" dataset

For this project, I utilized publicly available state data regarding accidental drug overdose deaths to help better understand the overdose crisis. The state data I am working with was gathered from www.data.ct.gov and captures all accidental overdose deaths that occurred in the state between the years of 2012 to 2018. The “Accidental Drug Related Deaths 2012-2018” is a single dataset that contains 5106 observations and 41 columns and is a listing of all deaths associated with drug overdoses that occurred in Connecticut over a 7-year period (from 2012 to 2018). This dataset contains time series data, demographic data (Age, Sex, Race), any/all type of drugs involved in the deaths, corresponding geographic data (place of death, place of residence, latitude and longitude), as well as description of injury and official Cause of Death for each observation (https://data.ct.gov/Health-and-Human-Services/Accidental-Drug-Related-Deaths-2012-2018/rybz-nyjw).

I have also gathered other data to help fill in the gaps of the main data source regarding county/city:
  Dataset on all CT cities and corresponding counties info: https://ctstatelibrary.org/cttowns/counties
  2010 CT Population Data Town & County: https://portal.ct.gov/DPH/Health-Information-Systems--Reporting/Population/Annual-Town-and-County-Population-for-Connecticut
  
This projet contains a few different files:
- <b>data_cleaning_CT.py</b>: python file that cleans/transforms the dataset for conducting analyis
- <b>EDA of the accidental drug deaths data.ipynb</b> Jupyter notebook that explores the dataset
- <b>Dashboard_CT_Accidental_Drug_Deaths_2012_2018.xlsx</b> Interactive Excel dashboard of overdose deaths from 2012-2018

### Conclusions and Next Steps
From the EDA of the data, it was observed that overdose deaths in the state of Connecticut has been a growing problem in the state. Although there was a small reduction of fatalities from 2017 to 2018, the growth trend from 2012 to 2018 is severe.

It appears that most deaths are occurring among Males(70%), White/Non-Hispanics(>75%), and people between the ages of 25 to 54 (74%). It was also observed that the majority of overdose deaths involved more than one drug (70%).

By breaking the opiods into their respective categories it was observed that both Heroin and natural and semi-sythetic opioids (most associated with prescription medications) have been showing a decline, however the reduction in these two categories is offset by the dramatic rise of "synthetic opioids" (e.g. Fentanyl).</b>

#### Next steps in the analysis would be to drill down on a few more questions that came from the EDA:
1. How does the data look per county when using crude adjustment rates and age-adjusted rates?
2. Visualize the geolocation of deaths per by drug per county.
3. Visualize the geolocation data of the deaths per city.

