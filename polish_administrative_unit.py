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
    def __init__(self, name: str, area: float): super().__init__(name, '', area)

class WrongSubunitException(RuntimeError): pass
