

NOXIOUS_WEED_DESIGNATION_NONE = ""
NOXIOUS_WEED_DESIGNATION_CHOICES = (
    (NOXIOUS_WEED_DESIGNATION_NONE, ""),
    ("A", "ODA Class A"),
    ("B", "ODA Class B"),
    ("Federal", "Federal")
)

NATIVE_CHOICES = (
    (True, "Native"),
    (False, "Non-native"),
    (None, "Unknown")
)

REPORTING_SOURCE_NONE = ""
REPORTING_SOURCE_CLR = "CLR"
REPORTING_SOURCE_IMAP = "IMAP"
REPORTING_SOURCE_CHOICES = (
    (REPORTING_SOURCE_NONE, ""),
    (REPORTING_SOURCE_CLR, "Center for Lakes and Reservoir"),
    (REPORTING_SOURCE_IMAP, "iMapInvasives")
)
REPORTING_SOURCE_URL = (
    (REPORTING_SOURCE_CLR, "http://www.clr.pdx.edu/"),
    (REPORTING_SOURCE_IMAP, "http://www.imapinvasives.org")
)
