from collector import IdCollector, EmployeeRecords


if __name__ == "__main__":
    print('Started')
    id_collect = IdCollector(2)
    print('Collecting Links of Employees')
    id_collect.collect_data()
    employee_records = EmployeeRecords(id_collect.ids)
    print('Collecting Employee Records')
    employee_records.collect_data()
    print('Saving Data')
    employee_records.save()
