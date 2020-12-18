/***************************************************************
Name: CDC mortality dataset stage 2 cleaning
Author: Jeff Morin
Date: 2/08/2020
Updated: 
Description:National dug overdose deaths data for year 2013-2017
***************************************************************/
// Program Setup

version 14.2
clear all 
set more off				
set linesize 80
capture log close
capture log using mortality_2013.txt, text replace name(mortality_2013)	// open a log file 
*****************************************************************

/*set working directory and import dataset*/

capture cd "C:\Data"

capture import delimited "drug_deaths_mortality_2013_2017.csv",delimiter(comma) clear

describe
// drop columns that we know we wont be needing -- needs to be lower case
drop ra15 ra16 ra17 ra18 ra19 ra20

	
//reconcile educational attainment
gen education = 0

replace education = 1 if education_89 == " 01"
replace education = 1 if education_89 == " 02"
replace education = 1 if education_89 == " 03"
replace education = 1 if education_89 == " 04"
replace education = 1 if education_89 == " 05"
replace education = 1 if education_89 == " 06"
replace education = 1 if education_89 == " 07"
replace education = 1 if education_89 == " 08"
replace education = 2 if education_89 == " 09"
replace education = 2 if education_89 == " 10"
replace education = 2 if education_89 == " 11"
replace education = 3 if education_89 == " 12"
replace education = 4 if education_89 == " 13"
replace education = 4 if education_89 == " 14"
replace education = 4 if education_89 == " 15"
replace education = 5 if education_89 == " 16"
replace education = 6 if education_89 == " 17"
replace education = 0 if education_89 == " 99"

replace education = 0 if education_2003 == " 9"
replace education = 1 if education_2003 == " 1"
replace education = 2 if education_2003 == " 2"
replace education = 3 if education_2003 == " 3"
replace education = 4 if education_2003 == " 4"
replace education = 4 if education_2003 == " 5"
replace education = 5 if education_2003 == " 6"
replace education = 6 if education_2003 == " 7"
replace education = 6 if education_2003 == " 8"

// create new age_bin categorical from age_value

gen age_bin = 0
replace age_bin = 1 if age_value <= 14
replace age_bin = 2 if age_value >=15 & age_value <=24
replace age_bin = 3 if age_value >= 25 & age_value <=34
replace age_bin = 4 if age_value >= 35 & age_value <=44
replace age_bin = 5 if age_value >= 45 & age_value <=54
replace age_bin = 6 if age_value >= 55 & age_value <=64
replace age_bin = 7 if age_value >= 65 & age_value <=74
replace age_bin = 8 if age_value >= 75 & age_value <=84
replace age_bin = 9 if age_value >= 85 & age_value <.

// generate new columns and parse out only values that refer to drugs from ra*
foreach var of varlist ra2-ra14 {
  generate drug_`var' = .
  replace drug_`var' = 1 if `var' == " T400"
  replace drug_`var' = 2 if `var' == " T401"
  replace drug_`var' = 3 if `var' == " T402"
  replace drug_`var' = 4 if `var' == " T403"
  replace drug_`var' = 5 if `var' == " T404"
  replace drug_`var' = 6 if `var' == " T405"
  replace drug_`var' = 7 if `var' == " T406"
  replace drug_`var' = 8 if `var' == " T436"
}


// save this to csv for faster testing and inspecting
capture cd "C:\Data"
outsheet using drug_deaths_mortality_2013_2017_cleaning_stage2.csv, comma replace

log close
exit
