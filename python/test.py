import json


f=open('stock.json')

data = f.read()
f.close()

data = data.replace('_ntes_quote_callback(','').replace(');','')

print(data)
data = json.loads(data)



stock1_num = '0000001'
stock2_num = '1399006'
stock3_num = '1399001'
stock4_num = '1399300'

stock1 = '%s %s' % (data[stock1_num]['name'], data[stock1_num]['price'])
stock2 = '%s %s' % (data[stock2_num]['name'], data[stock2_num]['price'])
stock3 = '%s %s' % (data[stock3_num]['name'], data[stock3_num]['price'])
stock4 = '%s %s' % (data[stock4_num]['name'], data[stock4_num]['price'])


print(stock1)
print(stock2)
print(stock3)
print(stock4)