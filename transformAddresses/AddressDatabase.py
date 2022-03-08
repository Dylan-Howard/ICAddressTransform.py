

class AddressDatabase(unit_col_in, notes_col_in):
    """docstring for AddressDatabase."""

    def __init__(self, address_data, unit_col_in, notes_col_in):

        self.address_data = address_data
        self.headings = self.address_data[0]
        del self.address_data[0]

        # Sets the index of the ADDR_UNIT to its location in the Address data
        self.unit_col_in = unit_col_in
        self.notes_col_in = notes_col_in

        self.address_groups = {
            'no_transforms': [],
            'expansion_transforms': [],
            'manual_transforms': [],
            'not_wcps': []
        }
        self.filter_addresses()

    # Filters each address based on its pattern (see DAG in README.md)
    def filter_addresses(self):
        for a in self.addresses:
            # Checks if the address is in District
            if a[self.notes_col_in] != '':
                self.address_groups['not_wcps'].append(a)
            else:
                # Sets addr_unit based on index and strips leading spaces
                addr_unit = a[self.unit_col_in].lstrip()

                if 'LOT' in addr_unit:
                    self.address_groups['no_transforms'].append(a)
                elif len(addr_unit) < 4:
                    self.address_groups['no_transforms'].append(a)
                elif ',' in addr_unit:
                    self.address_groups['manual_transforms'].append(a)
                elif ';' in addr_unit:
                    self.address_groups['manual_transforms'].append(a)
                elif 'AND' in addr_unit:
                    self.address_groups['manual_transforms'].append(a)
                elif not ('-' in addr_unit):
                    self.address_groups['no_transforms'].append(a)
                elif 'EACH' in addr_unit:
                    self.address_groups['manual_transforms'].append(a)
                elif 'APT' in addr_unit:
                    self.address_groups['expansion_transforms'].append(a)
                elif 'SUITE' in addr_unit:
                    self.address_groups['expansion_transforms'].append(a)
                elif 'UNIT' in addr_unit:
                    self.address_groups['expansion_transforms'].append(a)
                else:
                    self.address_groups['no_transforms'].append(a)

    # Removes parenthetical notes
    def remove_parenthesis(addr_unit):
        if '(' in addr_unit:
            return = addr_unit[:addr_unit.index('(')]
            # in_start = addr_unit.index('(')
            # in_end = addr_unit.index(')') + 1
            # addr_unit = addr_unit[in_start:in_end]
        else:
            return addr_unit

    def get_prefix(addr_unit):
        if 'APTS' in addr_unit:
            return 'APTS'
        elif 'APT' in addr_unit:
            return 'APT'
        elif 'UNIT' in addr_unit:
            return 'UNIT'
        elif 'SUITE' in addr_unit:
            return 'SUITE'
        else:
            return 'N/A'

    def remove_prefix(addr_unit, prefix):
        addr_unit = addr_unit[(addr_unit.index(prefix) + len(prefix)):]

        if prefix in addr_unit:
            in_prefix = addr_unit.index(prefix)
            return (
                addr_unit[:in_prefix] +
                addr_unit[(in_prefix + len(prefix)):]
            )
        else:
            return addr_unit

    # Returns the start and end index of an address unit's sequence
    def get_seq_range(addr_unit):
        in_delimitter = addr_unit.index('-')
        return {
            'start_in': addr_unit[:in_delimitter],
            'end_in': addr_unit[(in_delimitter + 1):]
        }

    def get_not_wcps(self):
        return self.address_groups['not_wcps']

    def get_manual_transforms(self):
        return self.address_groups['manual_transforms']

    # Expands intelligable rows with multiple address units
    def expand_seq_units(self):
        expansion_results = {
            "expanded_addresses": [],
            "errors": []
        }

        for a in self.address_data:
            # Strips whitespace
            addr_unit = a[self.unit_col_in].replace(' ', '')

            # Removes parenthetical notes
            addr_unit = remove_parenthesis(addr_unit)

            # Get prefix
            prefix = get_prefix(addr_unit)
            if 'N/A' in addr_unit:
                print('Row does not contain prefix')
                print(a)
                expansion_results['errors'].append(a)
                continue
            addr_unit = remove_prefix(addr_unit, prefix)
            prefix += ' '  # Adds space for formatting

            seq_range = get_seq_range(addr_unit)  # Gets start and end index

            # Appends prefix for mixed indecies (e.g., A1-A3, 1A-1D)
            if (not seq_range['start_in'].isnumeric()) and len(seq_range['start_in']) != 1:
                if len(start_in) > 2:
                    # Checks for ##-Char Pattern (e.g., 10A-10B or 19A-19H)
                    if seq_range['start_in'][0:2].isnumeric():
                        prefix_offset = 2
                    # Checks for Char-## Pattern (e.g., A10-A19)
                    elif seq_range['start_in'][1:].isnumeric():
                        prefix_offset = 1
                    else:
                        print('Row contains unknown pattern', seq_range['start_in'], seq_range['end_in'])
                        print(a)
                        expansion_results['errors'].append(a)
                        continue
                # Checks for #-Char Pattern (e.g., 1A-1B or 8A-8H)
                else:
                    prefix_offset = 1
                t_prefix = start_in[:prefix_offset]

                if t_prefix == end_in[:prefix_offset]:
                    prefix += t_prefix
                    seq_range['start_in'] = start_in[prefix_offset:]
                    seq_range['end_in'] = end_in[prefix_offset:]
                    addr_unit = seq_range['start_in'] + '-' + seq_range['end_in']
                else:
                    print('Row contains error', seq_range['start_in'], seq_range['end_in'])
                    print(a)
                    expansion_results['errors'].append(a)
                    continue

            convert_char = not seq_range['start_in'].isnumeric()
            if convert_char:
                seq_range['start_in'] = ord(seq_range['start_in'])
                seq_range['end_in'] = ord(end_in)
            else:
                seq_range['start_in'] = int(seq_range['start_in'])
                seq_range['end_in'] = int(seq_range['end_in'])

            # Sets ADDR_UNIT value for numeric and non-numeric Units
            for i in range(seq_range['start_in'], seq_range['end_in']+1):
                t_address = a
                if convert_char:
                    t_address[self.unit_col_in] = prefix + str(chr(i))
                else:
                    t_address[self.unit_col_in] = prefix + str(i)
                print(t_address)
                expansion_results['expanded_addresses'].append(
                    t_address.copy()
                )

        # return expansion_results
        # Compiles & Returns all formatted addresses
        return (
            address_groups['no_transforms'] +
            address_groups['expansion_transforms'] +
            address_groups['manual_transforms']
        )
