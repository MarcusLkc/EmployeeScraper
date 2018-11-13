from collector import IdCollector, EmployeeRecords


if __name__ == "__main__":
    id_collect = IdCollector(2)
    id_collect.collect_data()
    employee_records = EmployeeRecords(id_collect.ids)
    employee_records.collect_data()
    employee_records.save()
