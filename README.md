# List the Individual Repeat Donors for political campaign contributions



## Summary of Challenge

The Federal Election Commission (FEC) regularly publishes campaign contributions, and while you don’t want to pull specific donors from those files — because using that information for fundraising or commercial purposes is illegal — you want to identify areas (zip codes) that could be sources of repeat campaign contributions.

For this challenge, we're asking you to take a file listing individual campaign contributions for multiple years, determine which ones came from repeat donors, calculate a few values and distill the results into a single output file, repeat_donors.txt.

For each recipient, zip code and calendar year, we will calculate these three values for contributions coming from repeat donors:

- total dollars received
- total number of contributions received
- donation amount in a given percentile


## Solution

### Used Python for programming language and;
  - Pandas : Standard public available library
  - Sys: To get the arguments from command line, standard library


### Program has three (3) function procedure
- agg_txt()   : Read the input text file and remove unwanted records using pandas library
- RepeatDon() : Define the repeat donor records for current calendar year and omit the all other records
- Percentile(): Calculate the running percentile of contributions from repeat donors by using the nearest-rank method as described by Wikipedia

### Important details has been taken into consideration
- The output file line order has to be in same order as the donation appear in the input file
- When calculating 'OrdinalRank' field, we get value of zero (0) for some records at the beginning because of formula. Minimum value of OrdinalRank has to be one (1), and those values corrected
- Although we don't have float value for TRANSACTION_AMT field in the samples, the FEC describes the TRANSACTION_AMT field as NUMBER(14,2) and shows those number without decimal point if they have value of zero in the decimal place (.00). For the float value of '123456.00', they are showing as a '12345'. Those two details has taken into consideration 

## Step by Step Explanation

### 1. agg_txt() function
- I read the text file and record only specific fields into pandas data frame      
- On the FEC (Federal Election Commission) web site TRANSACTION_AMT defined as a NUMBER(14,2), so I used float type for this field
- Data Cleaning
  - Because we are only interested in individual contributions, we only want records that have the field OTHER_ID, set to empty.If the OTHER_ID field contains any other value, you should completely ignore and skip the entire record;
  - If 'TRANSACTION_DT' is an invalid date (e.g., empty, malformed)
  - If 'ZIP_CODE' is an invalid zip code (i.e., empty, fewer than five digits)
  - If the 'NAME'is an invalid name (e.g., empty, malformed)
  - If any lines in the input file contains empty cells in the 'CMTE_ID' or 'TRANSACTION_AMT' fields	
- Keep records index on a new field and use it at the end of the process



## 2. RepeatDon() function
- Get the current/active year info
- Calculate the total donation number (allCONT) by grouping NAME and ZIP_CODE
- Remove the records which has total donation number (allCONT) equal to one (1) or belongs to previous calendar year 
- Calculate the current year's total donation number (curYearCONT) by grouping NAME and ZIP_CODE
- if a person made a donation in previous calendar years, total donation number (allCONT) has to be bigger than current year's total donation number (curYearCONT). So, we only keep the records by filtering for total donation number (allCONT) bigger than current year's total donation number
- After filter, sort the records as it was beginning

## 3. Percentile() function
- Get the percentile value
- Generate the total number of contributions from repeat donors (IND) in dataframe
- Generate the current year info from TRANSACTION_DT
- Generate the running the total dollar amount of contributions' (TOT_CONTR) and format for decimal digits drop zero
- Generate 'PercentileContrb' field by value equal to zero (0) for later use
- Generate the 'OrdinalRank' by multiplying Percentile with 'IND'  for all records 
  - Set the 'OrdinalRank' field values 1 for values equal to less than 1
  - x = round(100/x_perc)  : this calculation gives as number of 'OrdinalRank' which has value 1 or less
  - df.at[:x-1,'OrdinalRank'] = 1 : Set's the value  equal to 1 for those records (-1 is for Pytond index starts from 0)
- Round the 'OrdinalRank' field and change the type to integer
- To calculate the running percentile of contributions from repeat donors, 
  - In the for-loop data frame iteration get records 'TRANSACTION_AMT' and append it to the list (list_contrb)
  - Sort the list and get the list's element which is equal to active records 'OrdinalRank' value
  - Set this element's value to the active records 'PercentileContrb' field

## 4. Print the fields to the output file in requested format and same order as the donation appear in the input file
