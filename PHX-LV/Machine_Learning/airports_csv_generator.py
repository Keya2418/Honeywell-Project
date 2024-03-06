import csv

# Open the input text file
with open('GlobalAirportDatabase.txt', 'r') as infile:
    # Read the lines from the file
    lines = infile.readlines()

# Create a CSV writer to write the data to a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write a header row to the CSV file
    writer.writerow(['Airport Code', 'Location Code', 'Airport Name', 'City', 'Country', 'Timezone Offset (H)', 
                     'Timezone Offset (M)', 'Timezone Offset (S)', 'Latitude Direction', 'Latitude Degrees', 
                     'Latitude Minutes', 'Latitude Seconds', 'Longitude Direction', 'Longitude Degrees', 
                     'Latitude in Decimal Degrees', 'Longitude in Decimal Degrees'])

    # Iterate over the lines in the input file
    for line in lines:
        # Split the line into fields using the colon delimiter
        fields = line.strip().split(':')

        # Write the fields to the CSV file
        writer.writerow(fields)