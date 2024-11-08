from src.infra.db.repositories.table_management_repository import TableManagementRepository
from src.data.use_cases.table_management import TableAddColumn, TableInsertRecord, TableEditRecord, TableDeleteRecord, TableListKeys, TableListRecords, TableListSpecificRecord
from src.presentation.controllers.table_management_controller import TableAddColumnController, TableInserRecordController, TableEditRecordController, TableDeleteRecordController, TableListKeysController, TableListRecordsController, TableListSpecificRecordController


def table_list_keys_composer():
    repository = TableManagementRepository()
    use_case = TableListKeys(repository)
    controller = TableListKeysController(use_case)

    return controller.handle


def table_add_column_composer():
    repository = TableManagementRepository()
    use_case = TableAddColumn(repository)
    controller = TableAddColumnController(use_case)

    return controller.handle


def table_insert_record_composer():
    repository = TableManagementRepository()
    use_case = TableInsertRecord(repository)
    controller = TableInserRecordController(use_case)

    return controller.handle


def table_edit_record_composer():
    repository = TableManagementRepository()
    use_case = TableEditRecord(repository)
    controller = TableEditRecordController(use_case)

    return controller.handle


def table_delete_record_composer():
    repository = TableManagementRepository()
    use_case = TableDeleteRecord(repository)
    controller = TableDeleteRecordController(use_case)

    return controller.handle


def table_list_records_composer():
    repository = TableManagementRepository()
    use_case = TableListRecords(repository)
    controller = TableListRecordsController(use_case)

    return controller.handle


def table_list_specific_record_composer():
    repository = TableManagementRepository()
    use_case = TableListSpecificRecord(repository)
    controller = TableListSpecificRecordController(use_case)

    return controller.handle
