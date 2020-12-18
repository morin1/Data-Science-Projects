/***************************************************************
Name: Appending Mortality Datasets 
Author: Jeff Morin
Date: 01/27/2020
Updated: 2/01/2020 added 2018 data as it was just released
		 2/4 added force option to 2018 merge due to type mismatch
Description: appending the mortality datasets from 2013 to 2017
***************************************************************/
// Program Setup

version 14.2
clear all 
set more off				
set linesize 80
capture log close
capture log using append_mortality.txt, text replace name(append_mortality) // open a log file 
*****************************************************************
/*set working directory and import dataset*/

capture cd "C:\Users\Jeff\Desktop\SNHU\DAT 490 Capstone in Data Analytics\Final_Project\Data\unmerged processed data"
//capture import delimited "drug_deaths_mortality_2013_v2.dta", clear

//import delimited using drug_deaths_mortality_2018_v2.csv, clear
//save drug_deaths_mortality_2018_v2.dta

import delimited using drug_deaths_mortality_2017_v2.csv, clear
save drug_deaths_mortality_2017_v2.dta

import delimited using drug_deaths_mortality_2016_v2.csv, clear
save drug_deaths_mortality_2016_v2.dta

import delimited using drug_deaths_mortality_2015_v2.csv, clear
save drug_deaths_mortality_2015_v2.dta

import delimited using drug_deaths_mortality_2014_v2.csv, clear
save drug_deaths_mortality_2014_v2.dta

import delimited using drug_deaths_mortality_2013_v2.csv, clear
save drug_deaths_mortality_2013_v2.dta

append using drug_deaths_mortality_2014_v2.dta
append using drug_deaths_mortality_2015_v2.dta
append using drug_deaths_mortality_2016_v2.dta
append using drug_deaths_mortality_2017_v2.dta
//append using drug_deaths_mortality_2018_v2.dta, force //variable education_2003 is str2 in master but byte in using data



describe

// save this as csv
capture cd "C:\Users\Jeff\Desktop\SNHU\DAT 490 Capstone in Data Analytics\Final_Project\Data
outsheet using drug_deaths_mortality_2013_2017.csv, comma replace

log close
exit
