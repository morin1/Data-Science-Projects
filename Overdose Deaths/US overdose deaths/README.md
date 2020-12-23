# CDC reported overdose deaths

The analytical report that I have compiled focuses on the opioid epidemic facing the United States. For this project, I utilized national data regarding drug overdose deaths to better understand the opioid crisis. The national data used captured all accidental or undetermined cause overdose deaths in the United States from 2013 to 2018 and was retrieved from the CDC (cdc.gov, 2020). I will be using exploratory analysis techniques to produce an “apples-to-apples” comparison between the national data and data from the state of Connecticut. With the national data, I also deployed a **k-modes** clustering algorithm to discover any underlying groups within these overdose deaths. K-modes is similar in ways to a k-means clustering algorithm, but is better suited for use with categorical data which is found in this CDC data (https://pypi.org/project/kmodes/).


The data was parsed using a python script I found that was designed to parse the very large CDC “Mortality Multiple Cause” from years 2010-2018 (CDC.gov). While the parsing script was awesome, it was not quite 100% and so needed to be updated to accurately and completely parse the CDC files. The parser was created by github user **tommaho** and the original version can be found hosted at https://github.com/tommaho/VS13MORT.DUSMCPUB-Parser. I am grateful to have found this script as it saved a lot of time. Thanks **tommaho**!!!

At the time of this project, I was learning Stata, and so I chose to clean and organize the data using .do files for the practice. I appreciated using Stata as I could process the very large files without encountering problems with memory. The rest of the project relied upon jupyter notebooks running python. 

