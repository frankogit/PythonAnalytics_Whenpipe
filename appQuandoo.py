import pandas as pd
import datetime as dt
import traceback
import logging
from utils import my_functions as mf

######################################################################
########### By   : Franko Ortiz
########### For  : Quandoo Test
########### Date : 12/2020
######################################################################



print('\n\t\t*** Quandoo Data Engineer Test - Franko Ortiz ***\n')    

# Read csv placed in root directory
class QuandooApp:
    
    def __init__(self, app_id,merchant_dataset='merchant_dataset.csv',reservation_dataset='reservation_dataset.csv'):

        self.app_id = app_id
        self.merchant_dataset = merchant_dataset
        self.reservation_dataset = reservation_dataset

    def main_execution(self):
    
        #Logging configuration
        logging.basicConfig(filename='frankoQuandoo.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %H:%M:%S')
        logging.disable(logging.DEBUG)

        try:

            df_merchant=pd.read_csv(self.merchant_dataset, sep=';',encoding = 'utf-8')
            df_reservation=pd.read_csv(self.reservation_dataset, sep=';',encoding = 'utf-8')

            #########################       TASK 1

            # Evaluate wrong mails
            df_reservation['valid_mail']=df_reservation['merchant_email'].apply(mf.get_mail)

            print('\n############   TASK 1\n')
            print('\tInvalid mails to remove: \n')

            print(df_reservation[df_reservation['valid_mail'] == '']['merchant_email'])

            # Removing mails
            df_reservation.drop(df_reservation[df_reservation['valid_mail'] == ''].index, inplace=True)
            logging.info('Task 1 completed - removed invalid mails ' )

            #########################       TASK 2

            print('\n\n############   TASK 2\n')
            print('\t Average seated guests : \n')

            print(round(df_reservation['guest_count'].mean(),2))
            logging.info('Task 2 completed - Average sets calculated ' )

            #########################       TASK 3


            print('\n\n############   TASK 3\n')
            print('\t Merchant with the highest amount of seated guests : \n')

            # Not consider guest_count with value 1 only for this activity
            df_reservation_no1 = df_reservation.copy()
            df_reservation_no1.drop(df_reservation_no1[df_reservation_no1['guest_count'] == 1].index, inplace=True)

            # merge both Dataframes
            df_reser_merch =df_reservation_no1.merge(df_merchant, on='merchant_id', how='inner')

            # show merchant with the highest amount of seated guests
            print(df_reser_merch.loc[df_reser_merch['guest_count'].idxmax()][['merchant_name','guest_count']])
            logging.info('Task 3 completed - Merchant with the highest amount of seated guests completed ' )

            #########################       TASK 4

            print('\n\n############   TASK 4\n')
            print('\t Highest merchant per quarter : \n')

            # merge dataframes including 1 seated guests
            df_reservation =df_reservation.merge(df_merchant, on='merchant_id', how='inner')

            # Convert to datetime
            df_reservation['created_at']=pd.to_datetime(df_reservation['created_at'], format='%Y-%m-%d %H:%M:%S')

            # Assign a quarter
            df_reservation['quarter'] = df_reservation['created_at'].dt.quarter

            # Assign a Rank for select highest values
            df_reservation['RN'] = df_reservation.sort_values(['quarter','guest_count'], ascending=[False,False]) \
                         .groupby(by=['quarter']) \
                         .cumcount() + 1

            #Show Highest merchant per quarter
            print(df_reservation[df_reservation['RN']==1][['quarter','merchant_name','guest_count']])
            logging.info('Task 4 completed - Highest merchant per quarter completed ' )
            print('\n\n')
            return True
        except:
            logging.error(str(traceback.format_exc()))
            return False

# EXECUTION TESTS
y =QuandooApp('Quandoo 12-20','merchant_dataset.csv','reservation_dataset.csv')
y.main_execution()


# SHOW LOGS , That could be ingest to Some Prometheus/Elasticsearch
print('****      LOGS   ->   Move to Prometheus / Elasticsearch   ******\n')
file = open('frankoQuandoo.log', 'rb')  # Open the file as wb to read bytes
log = file.read()  # The key will be type bytes
print(log.decode("utf-8"))
file.close()