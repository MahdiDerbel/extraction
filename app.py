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


client_id="vrfXGHzjm5V3jEU7iaB7OFuJFz82359PwP49WrZ"
client_secret="LiDvV29zMJm93gw0PYrupmvLFSELiNTj8VkgSuPUxorbuEDe25Vx68UStCZwdf8YtNVzn2niEhHklvmlkLkXRL9ZGM6ujyhlorn1IDnXyXtx0DkdFwuL5ZIt74CBJxfn"
username="omarsfaxiano32"
api_key="40967967722f30b7daba2fb0684730f8"
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
