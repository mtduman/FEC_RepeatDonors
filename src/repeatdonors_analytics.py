
# coding: utf-8

import sys
import pandas as pd

def agg_txt(fname):
    header_names = ['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']
    column_type = {'TRANSACTION_AMT':float}
    df = pd.read_csv( fname, delimiter='|', usecols=[0,7,10,13,14,15], dtype=str, names=header_names, converters=column_type, float_precision='round_trip')
    
    df = df[ ~(df['OTHER_ID'].notnull() |
               df['NAME'].isnull() |
               df['CMTE_ID'].isnull() |
               df['TRANSACTION_AMT'].isnull() )]
        
    df['ZIP_CODE'] = df['ZIP_CODE'].str[:5]
    df['TRANSACTION_DT']  = pd.to_datetime(df['TRANSACTION_DT'] ,format='%m%d%Y' , errors='coerce' )

    df = df[~( (df['ZIP_CODE'].str.len() != 5) |
             df['TRANSACTION_DT'].isnull()    ) ]
    df['IN_'] = df.index
    return df

def RepeatDon(df):
    x_year = pd.Timestamp("today").year
    df['allCONT'] = df.groupby(['NAME', 'ZIP_CODE'])['TRANSACTION_AMT'].transform('count')
    df = df[ ~( (df['allCONT'] == 1) | (df['TRANSACTION_DT'].dt.year != x_year) )].copy(deep=True)
    df['curYearCONT'] = df.groupby(['NAME', 'ZIP_CODE'])['TRANSACTION_AMT'].transform('count')
    
    df = df[ df['allCONT'] > df['curYearCONT'] ]
    df.set_index('IN_', inplace=True)
    df.reset_index( inplace=True )
    return df

def Percentile(df, f_perc):
    x_perc = int( open(f_perc).readline().rstrip() )
    df["IND"] = df.index + 1
    df["YEAR"] = df['TRANSACTION_DT'].dt.year
    df['TOT_CONTR'] = df['TRANSACTION_AMT'].cumsum().map('{:g}'.format)
    df['PercentileContrb'] = 0
    
    df['OrdinalRank'] = (x_perc * df['IND'])/100
    x = round(100/x_perc)     # There are few records OrdinalRank value lower than 0.5, to make sure find and replace those values to be 1
    df.at[:x-1,'OrdinalRank'] = 1
    df['OrdinalRank'] = df.OrdinalRank.round().astype(int)
    
    list_contrb = []
    for index, row in df.iterrows():
        list_contrb.append(row['TRANSACTION_AMT'])
        df.set_value(index, 'PercentileContrb', round( sorted(list_contrb)[ row['OrdinalRank']-1 ]) )
    return df

def run():
    f_cont = sys.argv[1]
    f_perc = sys.argv[2]
    f_out  = sys.argv[3]
    
    df = agg_txt(f_cont)
    df = RepeatDon(df)
    df = Percentile(df, f_perc)
    
    df.to_csv( f_out,
              columns=['CMTE_ID','ZIP_CODE','YEAR','PercentileContrb','TOT_CONTR','IND'],
              sep='|', header=False,
              index=False)
        
    return

if __name__ == "__main__":
    run()
