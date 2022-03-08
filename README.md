# Infinite Campus Address Transform Script

This project transforms address data received from Zoning and Planning by expanding collections of apartment units into individual units For example, APT 1-10 becomes APT 1 in the first row, APT 2 in the second row, and so on).

## Transformation Process
![Infinite Campus Address Transform Script Process Diagram](https://github.com/Dylan-Howard/ic-address-etl/blob/bf4f250683afe5b96aa4b5d654a5233d0ea5ae37/docs/process-dag.png?raw=true)

The process for filtering and transforming is:
1. The data is received from a CSV file beginning with address-import.
2. If an address is in the City School district or outside of the county lines, then the script classifies this address as non_wcps, and will be exported in the non_wcps.csv
3. If the address contains "LOT", then the script classifies it as no_transforms and will be exported with expanded_addresses as addr_output.csv.
4. If the address contains a comma, semi-colon, or "AND", then the script classifies it as manual_transforms, and will be exported as manual_transforms.csv. The user will be to manually expand these addresses.
5. If the address does not contain a hyphen, then the script classifies it as manual_transforms, and will be exported as manual_transforms.csv. The user will be to manually expand these addresses.
6. If the address contains "EACH", then the script classifies it as manual_transforms, and will be exported as manual_transforms.csv. The user will be to manually expand these addresses.
7. If the address does not contain "APT", "SUITE", or "UNIT", then the script classifies it as manual_transforms, and will be exported as manual_transforms.csv. The user will be to manually expand these addresses.
8. All remaining  addresses are pragmatically expanded, merged with the no_transforms group, and exported as addr_output.csv.
