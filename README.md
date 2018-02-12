#  List of Individual Repeat Donors for political campaign contributions



Step By Step explanation for Python code

Used Python libraries
  - Pandas
  - Sys: To get the arguments from command line



## agg_txt() Function procedure:
- I read the text file and record only specific fields      
- On the FEC (Federal Election Commission) web site 'TRANSACTION_AMT' defined as a NUMBER(14,2), so I float type for this field
- Because we are only interested in individual contributions, we only want records that have the field,'OTHER_ID, set to empty.If the'OTHER_ID'field contains any other value, you should completely ignore and skip the entire record;
  - If 'TRANSACTION_DT' is an invalid date (e.g., empty, malformed)
  - If 'ZIP_CODE' is an invalid zip code (i.e., empty, fewer than five digits)
  - If the 'NAME'is an invalid name (e.g., empty, malformed)
  - If any lines in the input file contains empty cells in the 'CMTE_ID' or 'TRANSACTION_AMT' fields	
- Keep records index on a new field and use it at the end of the process



## RepeatDon() Function procedure:
- Get the current/active year info
- Calculate the total donation number (allCONT) by grouping NAME and ZIP_CODE
- Remove the records which has total donation number (allCONT) equal to one (1) and belongs to previous calendar year 
- Calculate the current year's total donation number (curYearCONT) by grouping NAME and ZIP_CODE
- if a person made a donation in previous calendar years, total donation number (allCONT) has to be bigger than current year's total donation number (curYearCONT). So, we only keep the records by filtering for total donation number (allCONT) bigger than current year's total donation number
- After filter, sort the records as it was beginning

## Percentile() Function procedure:
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

## Print the fields to the output file in requested format


