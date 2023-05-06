import csv

def get_park_info(park_name):
    with open('parks_cleaned.tsv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['name'] == park_name:
                return row
    return None
