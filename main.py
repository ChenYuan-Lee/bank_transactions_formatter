from consolidator import Consolidator
from formatters.citi_formatter import CitiFormatter
from formatters.citi_statement_formatter import CitiStatementFormatter
from formatters.dbs_statement_formatter import DBSStatementFormatter
from formatters.hsbc_formatter import HSBCFormatter
from formatters.posb_formatter import POSBFormatter
from formatters.sc_acct_formatter import SCAcctFormatter
from formatters.sc_card_formatter import SCCardFormatter
from selector import Selector

BANK_FORMATTERS = [
    CitiFormatter,
    CitiStatementFormatter,
    DBSStatementFormatter,
    HSBCFormatter,
    POSBFormatter,
    SCAcctFormatter,
    SCCardFormatter,
]

if __name__ == '__main__':
    selected_formatters = Selector.transform(formatters=BANK_FORMATTERS)
    for bank_formatter in selected_formatters:
        bank_formatter.transform()
    Consolidator.transform(formatters=selected_formatters)
