"""Octopus Tracker Calculations."""

from .Exceptions import RegionException, FormulaVersionException


class Octopus_Tracker_Calc_Electric:
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
        },
        {
            "name": "April 2024",
            "key": "APR_2024",
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
                "EE": 10.8298,
                "EM": 9.6678,
                "L": 10.9309,
                "MNW": 11.0004,
                "WM": 9.5890,
                "NE": 9.4327,
                "NWE": 10.8046,
                "SE": 10.2928,
                "SEE": 10.8979,
                "SW": 10.24,
                "SWE": 10.1597,
                "Y": 9.2307,
                "SS": 9.7661,
                "NS": 11.1874,
            },
        },
        {
            "name": "July 2024",
            "key": "JUL_2024",
            "mult": {
                "EE": 1.2492,
                "EM": 1.2366,
                "L": 1.2389,
                "MNW": 1.2653,
                "WM": 1.2297,
                "NE": 1.2332,
                "NWE": 1.2492,
                "SE": 1.2320,
                "SEE": 1.2378,
                "SW": 1.2309,
                "SWE": 1.2309,
                "Y": 1.2492,
                "SS": 1.2458,
                "NS": 1.2469,
            },
            "add": {
                "EE": 12.0750,
                "EM": 10.9752,
                "L": 11.9791,
                "MNW": 12.3613,
                "WM": 10.8997,
                "NE": 10.7615,
                "NWE": 12.1648,
                "SE": 11.6125,
                "SEE": 12.1905,
                "SW": 11.6031,
                "SWE": 11.5806,
                "Y": 10.5271,
                "SS": 11.0733,
                "NS": 12.5481,
            },
        },
        {
            "name": "October 2024",
            "key": "OCT_2024",
            "mult": {
                "EE": 1.2492,
                "EM": 1.2366,
                "L": 1.2389,
                "MNW": 1.2653,
                "WM": 1.2297,
                "NE": 1.2332,
                "NWE": 1.2492,
                "SE": 1.2320,
                "SEE": 1.2378,
                "SW": 1.2309,
                "SWE": 1.2309,
                "Y": 1.2492,
                "SS": 1.2458,
                "NS": 1.2469,
            },
            "add": {
                "EE": 11.9522,
                "EM": 10.9661,
                "L": 11.5631,
                "MNW": 12.4193,
                "WM": 10.8999,
                "NE": 10.8035,
                "NWE": 12.2194,
                "SE": 11.5903,
                "SEE": 12.1304,
                "SW": 11.7133,
                "SWE": 11.6548,
                "Y": 10.5045,
                "SS": 11.0589,
                "NS": 12.5910,
            },
        },
        {
            "name": "December 2024",
            "key": "DEC_2024",
            "mult": {
                "EE": 1.22986,
                "EM": 1.207,
                "L": 1.23145,
                "MNW": 1.2429,
                "WM": 1.21945,
                "NE": 1.17609,
                "NWE": 1.22442,
                "SE": 1.2134,
                "SEE": 1.21476,
                "SW": 1.20524,
                "SWE": 1.18696,
                "Y": 1.23194,
                "SS": 1.22231,
                "NS": 1.19836,
            },
            "add": {
                "EE": 11.79773,
                "EM": 10.97183,
                "L": 11.04568,
                "MNW": 12.47378,
                "WM": 10.90696,
                "NE": 10.86514,
                "NWE": 12.29569,
                "SE": 11.57629,
                "SEE": 12.06058,
                "SW": 11.82211,
                "SWE": 11.81446,
                "Y": 10.48907,
                "SS": 11.05619,
                "NS": 12.65636,
            },
        },
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

        for each in Octopus_Tracker_Calc_Electric.REGIONS:
            ret.append({"label": each["name"], "value": each["key"]})

        return ret

    def get_formulae_selector():
        """Return Formulae."""

        ret = []

        for each in Octopus_Tracker_Calc_Electric.TRACKER_FORMULAE:
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
