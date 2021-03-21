from formatters.posb_formatter import POSBFormatter

BANK_FORMATTERS = [
    POSBFormatter,
]

if __name__ == '__main__':
    for bank_formatter in BANK_FORMATTERS:
        bank_formatter.transform()
