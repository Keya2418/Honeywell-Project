import csv

with open('GlobalAirportDatabase.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    
    filtered_rows = []
    
    filtered_rows.append(next(reader))
    
    for row in reader:
        if row[4] == 'USA':
            filtered_rows.append(row)
            
output_filename = "USA_Airports.csv"

with open(output_filename, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    writer.writerows(filtered_rows)
    

            
            