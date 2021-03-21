from formatters.citi_formatter import CitiFormatter
from formatters.posb_formatter import POSBFormatter
from formatters.sc_acct_formatter import SCAcctFormatter
from formatters.sc_card_formatter import SCCardFormatter

BANK_FORMATTERS = [
    POSBFormatter,
    CitiFormatter,
    SCAcctFormatter,
    SCCardFormatter,
]

if __name__ == '__main__':
    for bank_formatter in BANK_FORMATTERS:
        bank_formatter.transform()
