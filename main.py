from formatters.citi_formatter import CitiFormatter
from formatters.posb_formatter import POSBFormatter
from formatters.sc_acct_formatter import SCAcctFormatter

BANK_FORMATTERS = [
    POSBFormatter,
    CitiFormatter,
    SCAcctFormatter,
]

if __name__ == '__main__':
    for bank_formatter in BANK_FORMATTERS:
        bank_formatter.transform()
