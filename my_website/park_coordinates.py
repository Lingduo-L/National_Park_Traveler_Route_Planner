import re

def get_park_coordinates(park_name: str) -> tuple[float, float] or None:
    parks = {}
    with open('parks_cleaned.tsv', encoding='utf-8') as file:
        next(file)  # Skip the header line
        for line in file:
            data = line.split('\t')
            if len(data) < 5:  # Ensure the line has right elements
                continue

            name, coordinates = data[0], data[4].split(';')
            try:
                lat, long = round(float(coordinates[0]), 4), round(float(coordinates[1]), 4)
                parks[name] = (lat, long)
            except ValueError:
                parks[name] = None

    matched_park_names = [name for name in parks.keys() if re.search(park_name.lower(), name.lower())]

    if not matched_park_names:
        return None

    if len(matched_park_names) > 1:
        print(f"Found multiple matching parks: {', '.join(matched_park_names)}")
        print("Please specify the exact park name.")
        return None

    matched_park_name = matched_park_names[0]
    return parks[matched_park_name]


