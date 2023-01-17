# Administrative units' area
Parses public API of Polish administrative units' area and returns in the object format.

Example:
```
>>> from main import get_country_units
>>> units = get_country_units()
>>> units.find_subunit("14 65 01 1").get_name()
'm. St. Warszawa'
```
