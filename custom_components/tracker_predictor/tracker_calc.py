"""Octopus Tracker Calculations."""

from .Exceptions import RegionException, FormulaVersionException


class Octopus_Tracker_Calc:
    """Calculate tracker values based on region and formulae."""

    REGIONS = [
        {
            "name": "East England",
            "key": "EE",
        },
        {
            "name": "East Midlands",
            "key": "EM",
        },
        {
            "name": "London",
            "key": "L",
        },
        {
            "name": "Mersyside & North Wales",
            "key": "MNW",
        },
        {
            "name": "West Midlands",
            "key": "WM",
        },
        {
            "name": "North England",
            "key": "NE",
        },
        {
            "name": "North West England",
            "key": "NWE",
        },
        {
            "name": "South England",
            "key": "SE",
        },
        {
            "name": "South East England",
            "key": "SEE",
        },
        {
            "name": "South Wales",
            "key": "SW",
        },
        {
            "name": "South West England",
            "key": "SWE",
        },
        {
            "name": "Yorkshire",
            "key": "Y",
        },
        {
            "name": "South Scotland",
            "key": "SS",
        },
        {
            "name": "North Scotland",
            "key": "NS",
        },
    ]

    TRACKER_FORMULAE = [
        {
            "name": "December 2023",
            "key": "DEC_2023",
            "mult": {
                "EE": 1.2012,
                "EM": 1.1890,
                "L": 1.1913,
                "MNW": 1.2166,
                "WM": 1.1824,
                "NE": 1.1857,
                "NWE": 1.2012,
                "SE": 1.1846,
                "SEE": 1.1901,
                "SW": 1.1835,
                "SWE": 1.1835,
                "Y": 1.2012,
                "SS": 1.1979,
                "NS": 1.1990,
            },
            "add": {
                "EE": 10.3059,
                "EM": 9.1977,
                "L": 10.5046,
                "MNW": 10.4310,
                "WM": 9.1159,
                "NE": 9.0527,
                "NWE": 10.0928,
                "SE": 9.7767,
                "SEE": 10.3815,
                "SW": 9.7306,
                "SWE": 9.6533,
                "Y": 8.7472,
                "SS": 9.2438,
                "NS": 10.5180,
            },
        }
    ]

    def calc(self, region, formula, val):
        """Calculate the price based on region and formula."""
        calc_vals = self.get_calc_vals(region, formula)

        return (val * calc_vals["mult"]) + calc_vals["add"]

    def get_regions(self):
        """Return Regions."""
        return self.REGIONS

    def get_formulae(self):
        """Return Formulae."""
        return self.TRACKER_FORMULAE

    def get_regions_selector():
        """Return Regions."""

        ret = []

        for each in Octopus_Tracker_Calc.REGIONS:
            ret.append({"label": each["name"], "value": each["key"]})

        return ret

    def get_formulae_selector():
        """Return Formulae."""

        ret = []

        for each in Octopus_Tracker_Calc.TRACKER_FORMULAE:
            ret.append({"label": each["name"], "value": each["key"]})

        return ret

    def get_calc_vals(self, region, formula):
        """Get the formula based on region and formula."""

        for version in self.TRACKER_FORMULAE:
            if version["key"] == formula:
                try:
                    return {
                        "mult": version["mult"][region],
                        "add": version["add"][region],
                    }
                except Exception as err:
                    raise RegionException("Region not found: ") from err

        raise FormulaVersionException("Version not found: ")

    def get_formula_name_by_key(self, formula):
        """Get the name for the tracker version"""
        for version in self.TRACKER_FORMULAE:
            if version["key"] == formula:
                return version["name"]

        raise FormulaVersionException("Version not found: ")

    def get_region_name_by_key(self, region):
        """Get the name for the tracker version"""
        for version in self.REGIONS:
            if version["key"] == region:
                return version["name"]

        raise FormulaVersionException("Region not found: ")
