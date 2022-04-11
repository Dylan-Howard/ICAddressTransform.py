
import unittest

from AddressTransform import AddressDatabase


class TestAddressDatabase(unittest.TestCase):
    def test_remove_parenthesis(self):
        # with_parenthesis = ['61457', '2124', '1540', 'FAIRVIEW AVENUE', '1540 FAIRVIEW AVENUE', 'APT H1 - APT H4 (HICKORY)', 'BOWLING GREEN', '', '42103', 'Y', 'CURRENT', 'KY', 'Greenwood', 'Drakes Creek', 'Briarwood']
        # without_parenthesis = ['43452', '44813', '501', 'ERIC AVENUE', '501 ERIC AVENUE', 'CLUBHOUSE', 'BOWLING GREEN',  '', '42101', 'Y', 'CURRENT', 'KY', 'Warren Central', 'Henry F Moss', 'Warren']
        #
        # blank_unit = ['51113', '52892', '729', 'ELKHORN PEAK DRIVE', '729 ELKHORN PEAK DRIVE', '', 'BOWLING GREEN', '2017', '42104', 'NC', 'FUTURE', 'KY', 'South Warren', 'South Warren', 'Rich Pond']
        # descrition_unit = ['43452', '44813', '501', 'ERIC AVENUE', '501 ERIC AVENUE', 'CLUBHOUSE', 'BOWLING GREEN',  '', '42101', 'Y', 'CURRENT', 'KY', 'Warren Central', 'Henry F Moss', 'Warren']
        # int_single_unit = ['11267', '11462', '1096', 'ELROD ROAD', '1096 ELROD ROAD', 'UNIT 4', 'BOWLING GREEN', '42104',  '', 'Y', 'CURRENT', 'KY', 'South Warren', 'South Warren', 'Jody Richards']
        # char_single_unit = ['43450', '44811', '540', 'ERIC AVENUE', '540 ERIC AVENUE', 'APT A', 'BOWLING GREEN',  '', '42101', 'Y', 'CURRENT', 'KY', 'Warren Central', 'Henry F Moss', 'Warren']
        # mixed_single_unit = ['61182', '44813', '501', 'ERIC AVENUE', '501 ERIC AVENUE', 'APT G49', 'BOWLING GREEN',  '', '42101', 'Y', 'CURRENT', 'KY', 'Warren Central', 'Henry F Moss', 'Warren']
        # int_multi_unit = ['61169', '44999', '179', 'ENTERPRISE COURT', '179 ENTERPRISE COURT', 'APT 201 - APT 210', 'BOWLING GREEN',  '', '42101', 'Y', 'CURRENT', 'KY', 'Warren Central', 'Henry F Moss', 'Lost River']
        # mixed_multi_unit = ['61172', '44813', '501', 'ERIC AVENUE', '501 ERIC AVENUE', 'APT M93 - APT M100', 'BOWLING GREEN',  '', '42101', 'Y', 'CURRENT', 'KY', 'Warren Central', 'Henry F Moss', 'Warren']
        # char_multi_unit = ['43449', '44810', '530', 'ERIC AVENUE', '530 ERIC AVENUE', 'APT A - APT B', 'BOWLING GREEN',  '', '42101', 'Y', 'CURRENT', 'KY', 'Warren Central', 'Henry F Moss', 'Warren']

        with_parenthesis = 'APT H1 - APT H4 (HICKORY)'
        without_parenthesis = 'CLUBHOUSE'
        blank_unit = ''
        int_single_unit = 'UNIT 4'
        mixed_multi_unit = 'APT M93 - APT M100'

        unit_col_in = 5
        notes_col_in = 16

        address_db = AddressDatabase([], unit_col_in, notes_col_in)

        with_result = address_db.remove_parenthesis(with_parenthesis)
        self.assertEqual(with_result, 'APT H1 - APT H4 ')

        without_result = address_db.remove_parenthesis(without_parenthesis)
        self.assertEqual(without_result, without_parenthesis)

        blank_result = address_db.remove_parenthesis(blank_unit)
        self.assertEqual(blank_result, blank_unit)

        int_single_result = address_db.remove_parenthesis(int_single_unit)
        self.assertEqual(int_single_result, int_single_unit)

        mixed_multi_result = address_db.remove_parenthesis(mixed_multi_unit)
        self.assertEqual(mixed_multi_result, mixed_multi_unit)


if __name__ == '__main__':
    unittest.main()
