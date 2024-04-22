import csv
import re

def clean_csv(input_filename, output_filename):
    # Define a regular expression to match undefined characters
    undefined_char_regex = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')

    # Open the input and output files
    with open(input_filename, 'r', newline='', encoding='utf-8') as input_file, \
            open(output_filename, 'w', newline='', encoding='utf-8') as output_file:
        # Create CSV reader and writer objects
        csv.field_size_limit(2147483647)
        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)

        # Iterate over rows in the input CSV file
        for row in csv_reader:
            # Remove tabbed spaces and undefined characters from each cell
            cleaned_row = [cell.replace('\t', '').strip() for cell in row]
            cleaned_row = [undefined_char_regex.sub('', cell) for cell in cleaned_row]

            # Write the cleaned row to the output CSV file
            csv_writer.writerow(cleaned_row)

# Example usage:
clean_csv('./data/complaints.csv', 'output.csv')
