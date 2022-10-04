from db import operations


def choice_tableid(tbl_id):
    tables = [table[0] for table in operations.tables()]
    return tables[tbl_id-1]