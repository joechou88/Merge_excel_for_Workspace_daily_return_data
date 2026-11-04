import re

FILENAME_PATTERN = re.compile(
    r"""
    ^
    (?:
        (?P<country>[A-Z][A-Za-z]+(?:-[A-Z][A-Za-z]+)*)  # Match countries (e.g., Germany, South-Korea)
        |
        (?P<category>[A-Za-z0-9\-]+)                     # Match categories (e.g., financial-return, non-life-insurance-1)
    )
    (?P<company>\d+)?               # Optional digit(s) for company number
    [_-]                            # Separator (underscore or hyphen)
    (?:(?!\d{4}(?:[-_]|$)).*?[_-])? # Optional intermediate text (e.g., quarterly-financial_), avoiding start year consumption
    (?P<start_year>\d{4})           # 4-digit start year
    (?:[-_](?P<end_year>\d{4}))?    # Optional hyphen/underscore and 4-digit end year
    (?:_(?P<suffix>[A-Za-z]+))?     # Optional suffix, e.g., "_A"
    (?:\.xlsm)?$                    # File extension
    """,
    re.VERBOSE
)

COUNTRY_MNEMONIC = {
    "Argentina": ["FARALL", "FPARGA"],
    "Australia": ["FAUALL", "FAUS"],
    "Austria": ["FATALL", "FOST"],
    "Belgium": ["FBEALL", "FBDO"],
    "Brazil": ["FBRALL", "FBRA"],
    "Bulgaria": ["FBULGOFF"],
    "Canada": ["FCAALL", "FCANS"],
    "Chile": ["FCLALL", "FCHILE"],
    "China": ["FCNALL", "FCHINA"],
    "Columbia": ["FCOALL", "FCOL"],
    "Denmark": ["FDKALL", "FDEN"],
    "Estonia": ["FESTONIA"],
    "Finland": ["FFIALL", "FFIN"],
    "France": ["FFRALL", "FFRA"],
    "Germany1": ["FDEALL1", "FGER1"],
    "Germany2": ["FDEALL2", "FGER2"],
    "Germany3": ["FDEALL3"],
    "Germany4": ["FDEALL4"],
    "Germany5": ["FDEALL5"],
    "Germany6": ["FDEALL6"],
    "Germany7": ["FDEALL7"],
    "Germany8": ["FDEALL8"],
    "Greece": ["FGRALL", "FGREE"],
    "Hong-Kong": ["FHKALL", "FHKQ"],
    "Hungary": ["FHUALL", "FHUN"],
    "India": ["FINALL", "FINDIA"],
    "Indonesia": ["FIDALL", "FINOQ"],
    "Ireland": ["FIEALL", "FIRL"],
    "Israel": ["FILALL", "FISRAEL"],
    "Italy": ["FITALL", "FITA"],
    "Japan": ["FJPALL", "FJAP"],
    "Luxembourg": ["FLUX"],
    "Malaysia": ["FMYALL", "FMALQ"],
    "Mexico": ["FMXALL", "FMEX"],
    "Netherlands": ["FNLALL", "FHOL"],
    "New-Zealand": ["FNZALL", "FNWZ"],
    "Norway": ["FNOALL", "FNOR"],
    "Pakistan": ["FPKALL", "FPAK"],
    "Peru": ["FPEALL", "FPERU"],
    "Philippines": ["FPHALL", "FPHIQ"],
    "Poland": ["FPLALL", "FPOL"],
    "Portugal": ["FPTALL", "FPOR"],
    "Romania": ["FROM"],
    "Russian-Federation": ["FRUS"],
    "Singapore": ["FSGALL", "FSINQ"],
    "South-Africa": ["FZAALL", "FSAF"],
    "South-Korea": ["FKRALL", "FKOR"],
    "Spain": ["FESALL", "FSPN"],
    "Sweden": ["FSEALL", "FSWD"],
    "Switzerland": ["FCHALL", "FSWA"],
    "Taiwan": ["FTWALL", "FTAIQ"],
    "Thailand": ["FTHALL", "FTHAQ"],
    "Turkey": ["FTRALL", "FTURK"],
    "UK": ["FGBALL", "FBRIT"],
    "Uruguay": ["FURNE"],
    "Vietnam": ["FVNALL", "FVTNM"]
}
