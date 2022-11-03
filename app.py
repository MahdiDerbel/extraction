import pprint
import veryfi
import datetime
import pandas as pd
import openpyxl
import uuid

def validate(date_text):
    h=False
    try:
        datetime.datetime.strptime(date_text, '%d/%m/%Y')
        h=True
    except ValueError:
        h=False
        
    return(h)


client_id="vrfd2hz9xtPxrtzpFdg3VKc01AxYrCJeSRlR78O"
client_secret="ycpIZHAXrxJyHXcW2erYkrCRFCjjOdkWVZ2wjTY4teljza11lOyLNehnJAtshtPGtL6HH9IwWRvny3hWTy68CxCFlWH7AlpOhDoHb2fucKNx1TL8G9IAn3mU7XI0elgC"
username="khalil"
api_key="54f07b441d51265e92495ed5f83221e9"
client=veryfi.Client(client_id,client_secret,username,api_key)

json_result=client.process_document("cheque.pdf")

text=json_result['ocr_text']
lines = text.splitlines()

index=0
item_line=[]
list=[]
client=''
date=''

while index<len(lines)-2:
    item_line=lines[index].splitlines()
    item_of_item=[i for i in lines[index].split('\t') if i]
    print(item_of_item)
    for i in range(len(item_of_item)):
        if 'PHARMADIS' in item_of_item[i]:
            client=item_of_item[i]
        if validate(item_of_item[i])==True:
            date=item_of_item[i]
    if date!=''and client!='':
        break
    else :
        index=index+1
        item_line=[]
        item_of_item=[]
        date=''

RIB_CLIENT=json_result['document_reference_number']
Date_recoit=json_result['date']
RIB_FOURNISSEUR=json_result['line_items'][0]['sku']
Montant=json_result['line_items'][0]['total']



df = pd.DataFrame ({'Ordre Paiement':[RIB_CLIENT],'client': [client],'Date opération': [Date_recoit],'Date echéance':[date],'Montant':[Montant]})

filename='{}.xlsx'.format(uuid.uuid1())
df.to_excel(filename)