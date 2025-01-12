"""Octopus Tracker Calculations."""

from .Exceptions import RegionException, FormulaVersionException


class Octopus_Tracker_Calc_Gas:
    """Calculate tracker values based on region and formulae."""

    DIV_VAL = 0.03604

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
            "mult": 0.03604,
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
        },
        {
            "name": "April 2024",
            "key": "APR_2024",
            "mult": 0.03604,
            "add": {
                "EE": 1.3622,
                "EM": 1.3617,
                "L": 1.6663,
                "MNW": 1.6990,
                "WM": 1.4435,
                "NE": 1.4960,
                "NWE": 1.4449,
                "SE": 1.5478,
                "SEE": 1.4474,
                "SW": 1.7307,
                "SWE": 1.8260,
                "Y": 1.5878,
                "SS": 1.4449,
                "NS": 1.4449,
            },
        },
        {
            "name": "July 2024",
            "key": "JUL_2024",
            "mult": 0.03604,
            "add": {
                "EE": 1.7448,
                "EM": 1.7443,
                "L": 2.0508,
                "MNW": 2.0836,
                "WM": 1.8268,
                "NE": 1.8794,
                "NWE": 1.8282,
                "SE": 1.9316,
                "SEE": 1.8305,
                "SW": 2.1155,
                "SWE": 2.2111,
                "Y": 1.9720,
                "SS": 1.8280,
                "NS": 1.8280,
            },
        },
        {
            "name": "October 2024",
            "key": "OCT_2024",
            "mult": 0.03604,
            "add": {
                "EE": 1.7293,
                "EM": 1.7334,
                "L": 2.0294,
                "MNW": 2.0845,
                "WM": 1.8202,
                "NE": 1.8599,
                "NWE": 1.8149,
                "SE": 1.9272,
                "SEE": 1.8194,
                "SW": 2.1129,
                "SWE": 2.2204,
                "Y": 1.9765,
                "SS": 1.8111,
                "NS": 1.8111,
            },
        },
        {
            "name": "December 2024",
            "key": "DEC_2024",
            "mult": 0.03478,
            "add": {
                "EE": 1.70921,
                "EM": 1.71360,
                "L": 2.00461,
                "MNW": 2.03276,
                "WM": 1.77449,
                "NE": 1.81723,
                "NWE": 1.82213,
                "SE": 1.91862,
                "SEE": 1.80713,
                "SW": 2.06856,
                "SWE": 2.17270,
                "Y": 1.93076,
                "SS": 1.82825,
                "NS": 1.82825,
            },
        },
    ]

    def calc(self, region, formula, val):
        """Calculate the price based on region and formula."""
        calc_vals = self.get_calc_vals(region, formula)

        return ((val / self.DIV_VAL) * calc_vals["mult"]) + calc_vals["add"]

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
                        "mult": version["mult"],
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
