

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

REPORTING_SOURCE_CLR = "CLR"
REPORTING_SOURCE_IMAP = "IMAP"
REPORTING_SOURCE_CHOICES = (
    (REPORTING_SOURCE_CLR, "Center for Lakes and Reservoir"),
    (REPORTING_SOURCE_IMAP, "iMapInvasives")
)
REPORTING_SOURCE_URL = (
    (REPORTING_SOURCE_CLR, "http://www.clr.pdx.edu/"),
    (REPORTING_SOURCE_IMAP, "http://www.imapinvasives.org")
)

IMPORT_STATUS_INITIALIZED = 1
IMPORT_STATUS_LOADING = 2
IMPORT_STATUS_COMPLETED = 3
IMPORT_STATUS_ERROR = 4
IMPORT_STATUS_CHOICES = (
    (IMPORT_STATUS_INITIALIZED, 'Initialized'),
    (IMPORT_STATUS_LOADING, 'Loading'),
    (IMPORT_STATUS_COMPLETED, 'Completed'),
    (IMPORT_STATUS_ERROR, 'Error'),
)
