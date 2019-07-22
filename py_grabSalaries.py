import json
import urllib.request
import urllib.parse
import csv

#The following script will grab all json entries from the Diamondback Salary Guide SQL database endpoint and convert them into a CSV file

url = "https://api.dbknews.com/"
years = []

#### First find list of all years that the database has entries for (in string format)
with urllib.request.urlopen(url+"salary/years") as response:
	byte_years = response.read()
	map_years = json.loads(byte_years)
	years = map_years['data']

### Declare some query values we will need to find the specific salaries we want
values = {'sortby' : "Salary",
	  'order' : "Salary" }
	 
url_values = urllib.parse.urlencode(values)

### Open csv file for writing
salary_data = open('salaries.csv', 'w')

### Create csv writer 
csvwriter = csv.writer(salary_data)
header_made = False

### Go through all BMGT and CMNS entries and write them into a CSV file
for year in years:
	page = 1
	while True:
		print(year, page)
		search = "BMGT"
		full_url = url + "salary/year/" + year + "?" + url_values + "&page=" + str(page) + "&search=" + search
		with urllib.request.urlopen(full_url) as response:
			byte_entries = response.read()
			map_entries = json.loads(byte_entries)
			entries = map_entries['data']
			
			if entries == []:
				break
			
			for entry in entries:
				if not header_made:
					header = ["Year"]
					header += entry.keys()
					csvwriter.writerow(header)
					header_made = True

				csvwriter.writerow([year]+list(entry.values()))
		
		search = "CMNS"
		full_url = url + "salary/year/" + year + "?" + url_values + "&page=" + str(page) + "&search=" + search
		with urllib.request.urlopen(full_url) as response:
			byte_entries = response.read()
			map_entries = json.loads(byte_entries)
			entries = map_entries['data']

			if entries == []:
				break

			for entry in entries:
				csvwriter.writerow([year]+list(entry.values()))
		
		page += 1
