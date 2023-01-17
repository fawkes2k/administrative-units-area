from polish_administrative_unit import Country, Province, County, Municipality

def __get_content_from_url(url: str) -> str:
    from requests import get
    content = get(url).content.decode()
    return content

def get_country_units() -> Country:
    """
    Parses public API in CSV format and returns data in the object format
    :return: Country object with subunits parsed from the API
    """
    from json import loads
    from csv import reader
    link = loads(__get_content_from_url('https://api.dane.gov.pl/1.4/datasets/1447/resources'))['data'][-1]['attributes']['csv_file_url']
    csv_content = __get_content_from_url(link)
    records = list(reader(csv_content.split('\n')))[1:-1]
    for record in records:
        unit_teryt, name_of_unit, area_of_unit = record
        teryt_parts = unit_teryt.split(' ')
        if unit_teryt == '00': country = Country(name_of_unit, int(area_of_unit))
        elif len(teryt_parts) == 1:
            province = Province(name_of_unit, unit_teryt, int(area_of_unit))
            country.add_subunit(province)
        elif len(teryt_parts) == 2:
            county = County(name_of_unit, unit_teryt, int(area_of_unit))
            province.add_subunit(county)
        else:
            municipality = Municipality(name_of_unit, unit_teryt, int(area_of_unit))
            county.add_subunit(municipality)
    return country
