class __AdministrativeUnit():
    def __init__(self, name: str, teryt: str, area: float):
        self.__name = name
        self.__teryt = teryt
        self.__area = area

    def get_name(self) -> str: return self.__name
    def get_teryt(self) -> str: return self.__teryt
    def get_area(self) -> float: return self.__area

class __DivisiableUnit(__AdministrativeUnit):
    subordinate_unit: "__AdministrativeUnit"

    def __init__(self, name: str, teryt: str, area: float):
        super().__init__(name, teryt, area)
        self.__subunits = []

    def add_subunit(self, subunit: "__AdministrativeUnit"):
        """
        Adds subunit to this unit

        :param subunit: Subunit to add
        :return: None
        :raises WrongSubunitException if given subunit is invalid.
        """
        if isinstance(subunit, type(self.subordinate_unit)): raise WrongSubunitException('This type of subunit is not subordinate to this unit.')
        if self.get_teryt() not in subunit.get_teryt(): raise WrongSubunitException('This is not a subunit of this unit.')
        self.__subunits.append(subunit)

    def find_subunit(self, teryt: str) -> "__AdministrativeUnit":
        """
        Finds a subunit of this unit
        :param teryt: TERYT number of the searched unit
        :return: AdministrativeUnit object if the unit has been found, otherwise None.
        """
        for subunit in self.__subunits:
            subunit_teryt = subunit.get_teryt()
            if subunit_teryt == teryt: return subunit
            if subunit_teryt in teryt: return subunit.find_subunit(teryt)

    def get_subordinate_unit(self) -> "__AdministrativeUnit": return self.subordinate_unit
    def get_subunits(self) -> list["__AdministrativeUnit"]: return self.__subunits

# "Gmina" in Polish
class Municipality(__AdministrativeUnit): pass

# "Powiat" in Polish
class County(__DivisiableUnit): subordinate_unit = Municipality

# "Województwo" in Polish
class Province(__DivisiableUnit): subordinate_unit = County

# "Kraj" in Polish
class Country(__DivisiableUnit):
    subordinate_unit = Province

    def __init__(self):
        """
        Parses public API in CSV format and returns data in the object format
        :return: Country object with subunits parsed from the API
        """
        from json import loads
        from csv import reader
        json = loads(self.__get_content_from_url('https://api.dane.gov.pl/1.4/datasets/1447/resources'))
        link = json['data'][-1]['attributes']['csv_file_url']
        csv_content = self.__get_content_from_url(link)
        records = list(reader(csv_content.split('\n')))[1:-1]
        for record in records:
            unit_teryt, name_of_unit, area_of_unit = record
            teryt_parts = unit_teryt.split(' ')
            if unit_teryt == '00': super().__init__(name_of_unit, '', int(area_of_unit))
            elif len(teryt_parts) == 1:
                province = Province(name_of_unit, unit_teryt, int(area_of_unit))
                self.add_subunit(province)
            elif len(teryt_parts) == 2:
                county = County(name_of_unit, unit_teryt, int(area_of_unit))
                province.add_subunit(county)
            else:
                municipality = Municipality(name_of_unit, unit_teryt, int(area_of_unit))
                county.add_subunit(municipality)

    def __get_content_from_url(self, url: str) -> str:
        from requests import get
        _ = self
        content = get(url).content.decode()
        return content

class WrongSubunitException(RuntimeError): pass
