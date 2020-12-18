/***************************************************************
Name: CDC mortality dataset 2013
Author: Jeff Morin
Date: January 2020
Updated: 1/30 accounting for new education columns
Description: US mortality data for year 2013
***************************************************************/
// Program Setup

version 14.2
clear all 
set more off				
set linesize 80
capture log close
capture log using mortality_2013.txt, text replace name(example)	// open a log file 
*****************************************************************

/*set working directory and import dataset*/

capture cd "C:\Users\Jeff\Desktop\SNHU\DAT 490 Capstone in Data Analytics\Final_Project\Data"

capture import delimited "parsed CDC files 2010_2018\New_EDU_VS13MORT.csv",delimiter(comma) clear

// make the first row of dataset into column headers
/*foreach v of varlist _all {
    label var `v' `"`=`v'[1]'"'
    rename `v' `=`v'[1]'
}

drop 1
*/
describe
// drop columns that we know we wont be needing -- needs to be lower case
drop resident_status infant_age_recode_22 injured_at_work infant_cause_recode_130 ///
	autopsy method_of_disposition activity_code place_of_death ///
	place_of_causal_injury manner_of_death cause_recode_358 cause_recode_113 ///
	cause_recode_39 entity_axis_conditions age_recode_52 age_sub_flag ///
	race_bridged race_imputation race_recode_3 race_recode_5 ///
	hispanic_origin_recode
	
//drop all Entity Axis Code columns
drop eac*

// find and keep only drug related deaths, non suicide or homocide
gen overdose_death = 0

replace overdose_death = 1 if icd10 == " X40"
replace overdose_death = 1 if icd10 == " X41"
replace overdose_death = 1 if icd10 == " X42"
replace overdose_death = 1 if icd10 == " X43"
replace overdose_death = 1 if icd10 == " X43"
replace overdose_death = 1 if icd10 == " Y10"
replace overdose_death = 1 if icd10 == " Y11"
replace overdose_death = 1 if icd10 == " Y12"
replace overdose_death = 1 if icd10 == " Y13"
replace overdose_death = 1 if icd10 == " Y14"

keep if overdose_death == 1
drop overdose_death

// recode hispanic_origin to be 0, 1, or 999 for null
gen origin_latin = 0
replace origin_latin =1 if hispanic_origin >= 200 & hispanic_origin < 300
replace origin_latin =999 if hispanic_origin >= 996 & hispanic_origin < 1000
mvdecode origin_latin, mv(999)

drop hispanic_origin
rename origin_latin hispanic_origin

// drop all observations where age keys are not "1" -- years
keep if age_key == 1

// save this to csv for faster testing and inspecting
capture cd "C:\Users\Jeff\Desktop\SNHU\DAT 490 Capstone in Data Analytics\Final_Project\Data\unmerged processed data"
outsheet using drug_deaths_mortality_2013_v2.csv, comma replace

log close
exit
