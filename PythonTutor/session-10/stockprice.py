import urllib3
from beautifulsoup4 import beautifulsoup4 as bs

def get_historical_data(name, number_of_days):
	data = []
	url = "https://finance.yahoo.com/quote/" + name + "/history/"
	rows = bs(urllib3.urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')

	for each_row in rows:
		divs = each_row.findAll('td')
		if divs[1].span.text  != 'Dividend': #Ignore this row in the table
			#I'm only interested in 'Open' price; For other values, play with divs[1 - 5]
			data.append({'Date': divs[0].span.text, 'Open': float(divs[1].span.text.replace(',',''))})

	return data[:number_of_days]

#Test
# print get_historical_data('amzn', 15)


# https://query1.finance.yahoo.com/v7/finance/download/WFC?period1=1561874153&period2=1593496553&interval=1d&events=history
# https://query1.finance.yahoo.com/v7/finance/download/WFC?period1=1561874369&period2=1593496769&interval=1d&events=history
# https://query1.finance.yahoo.com/v7/finance/download/AMZN?period1=1561874338&period2=1593496738&interval=1d&events=history


# max
# https://query1.finance.yahoo.com/v7/finance/download/WFC?period1=76204800&period2=1593388800&interval=1d&events=history
# https://query1.finance.yahoo.com/v7/finance/download/VBIV?period1=1031097600&period2=1593388800&interval=1d&events=history