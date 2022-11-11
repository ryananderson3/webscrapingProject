from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import keys2
from twilio.rest import Client

url = 'https://crypto.com/price'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers=headers)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')

#Twilio set up
client = Client(keys2.accountSID,keys2.authToken)
TwilioNumber = "+16203222414"
myCellPhone = '+15123172370'

#gets all of the cells in the table
table_cell = soup.findAll('td', attrs={'role':'gridcell'})

index = 0
for x in range(5):
    currency = str(table_cell[index+2].text)
    if str(table_cell[index+1].text) == '3' or str(table_cell[index+1].text) == '5':
        name = currency[:-4]
        symbol = currency[len(currency)-4:]
    else:
        name = currency[:-3]
        symbol = currency[len(currency)-3:]
    price = str(table_cell[index+3].text).split('$')

    print(f'Name: {name}')
    print(f'Symbol: {symbol}')
    print(f'Price: ${price[1]}')
    print(f'Day Change: {table_cell[index+4].text}')
    print()
    index+=9

    #if Bitcoin falls under $40,000 or Etherium under $3000, send text message to phone with twilio
    num = price[1].replace(',','')
    num = int(num[:-3])
    if name == 'Bitcoin' and num < 40000:
        text = 'ALERT:\n\n' + name + ' has fallen below $40,000 to $' + price[1]
        textmessage = client.messages.create(to=myCellPhone, from_=TwilioNumber,body=text)
    if name == 'Ethereum' and num < 3000:
        text = '\nALERT:\n\n' + name + ' has fallen below $3,000 to $' + price[1]
        textmessage = client.messages.create(to=myCellPhone, from_=TwilioNumber,body=text)
    
    #input()

