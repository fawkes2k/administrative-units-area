# Administrative units' area
Parses public API of Polish administrative units' area and returns in the object format.

Example:
```python
>>> from polish_administrative_units import Country
>>> units = Country()
>>> units.find_subunit("14 65 01 1").get_name()
'm. St. Warszawa'
```
