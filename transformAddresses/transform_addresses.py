import os
from CSVData import CSVData
from AddressDatabase import AddressDatabase

data_directory = '../data'
unit_col_in = 5
notes_col_in = 16

address_data = None

for file in os.listdir(data_directory):
    if file.startswith('address-import') and file.endswith('.csv'):
        address_data = CSVData(os.path.join(data_directory, file), ',', 'r')
        break

if address_data is None:  # Ends script if no import data exists
    print('No import data could be found.')
    quit()

address_db = AddressDatabase(address_data, unit_col_in, notes_col_in)

# Writes all formatted addresses to one file
csv_quick_write(
    os.path.join(data_directory, 'output', 'addr_output.csv'), ',',
    address_db.expand_seq_units()
)

# Writes all non-WCPS addresses to one file
csv_quick_write(
    os.path.join(data_directory, 'output', 'not_wcps.csv'), ',',
    address_db.get_not_wcps()
)

# Writes all addresses needing manual transformations to one file
csv_quick_write(
    os.path.join(data_directory, 'output', 'needs_transforms.csv'), ',',
    address_db.get_manual_wcps()
)


def csv_quick_write(filepath, delimiter, data):
    csv = CSVData(filepath, delimiter, 'w')
    csv.set_data(data)
    csv.write_csv()
