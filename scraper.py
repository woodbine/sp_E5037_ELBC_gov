# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E5037_ELBC_gov"
url = "http://www.enfield.gov.uk/downloads/download/1086/council_monthly_expenditure_for_250_and_above_-_report"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
block = soup.find('div',{'class':'download_box'})
pageLinks = block.findAll('a', href=True)

for pageLink in pageLinks:
  pageUrl = pageLink['href']
  if '/downloads/file' in pageUrl:
  	html2 = urllib2.urlopen(pageUrl)
  	soup2 = BeautifulSoup(html2)
  	
  	fileBlock = soup2.find('h3',{'class':'downloadNow'})
  	
	fileUrl = fileBlock['href']
	fileUrl = fileUrl.replace("/sites","http://www.croydon.gov.uk/sites")
	title = soup2.find('h2').contents[0]
	# create the right strings for the new filename
	title = title.upper().strip()
	csvYr = title.split(' ')[1]
	csvMth = title.split(' ')[0][:3]
	csvMth = convert_mth_strings(csvMth);

	filename = entity_id + "_" + csvYr + "_" + csvMth
	todays_date = str(datetime.now())
	scraperwiki.sqlite.save(unique_keys=['l'], data={"l": fileUrl, "f": filename, "d": todays_date })
	print filename
