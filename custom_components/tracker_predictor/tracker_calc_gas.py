"""Octopus Tracker Calculations."""

from .Exceptions import RegionException, FormulaVersionException


class Octopus_Tracker_Calc_Gas:
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
            "add": {
                "EE": 1.3167,
                "EM": 1.3162,
                "L": 1.5674,
                "MNW": 1.6212,
                "WM": 1.3778,
                "NE": 1.4353,
                "NWE": 1.4125,
                "SE": 1.4978,
                "SEE": 1.4025,
                "SW": 1.6518,
                "SWE": 1.7396,
                "Y": 1.5231,
                "SS": 1.3959,
                "NS": 1.3959,
            },
        }
    ]

    def calc(self, region, formula, val):
        """Calculate the price based on region and formula."""
        calc_vals = self.get_calc_vals(region, formula)

        return val + calc_vals["add"]

    def get_regions(self):
        """Return Regions."""
        return self.REGIONS

    def get_formulae(self):
        """Return Formulae."""
        return self.TRACKER_FORMULAE

    def get_regions_selector():
        """Return Regions."""

        ret = []

        for each in Octopus_Tracker_Calc_Gas.REGIONS:
            ret.append({"label": each["name"], "value": each["key"]})

        return ret

    def get_formulae_selector():
        """Return Formulae."""

        ret = []

        for each in Octopus_Tracker_Calc_Gas.TRACKER_FORMULAE:
            ret.append({"label": each["name"], "value": each["key"]})

        return ret

    def get_calc_vals(self, region, formula):
        """Get the formula based on region and formula."""

        for version in self.TRACKER_FORMULAE:
            if version["key"] == formula:
                try:
                    return {
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
