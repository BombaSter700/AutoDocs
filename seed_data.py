from datetime import date, datetime, timedelta
from decimal import Decimal
from random import randint, choice

from config import get_session, init_db
from database import (
    Location,
    Employee,
    Equipment,
    Document,
    EquipmentMovement,
    MaintenanceRecord,
    WriteOffAct,
    InventoryCheck,
    InventoryCheckItem,
    NetworkNode,
    NetworkLink,
)


def seed():
    init_db()

    with get_session() as session:
        # ────────────────────────────────
        # 1. Locations (10)
        # ────────────────────────────────
        locations_data = [
            ("Главный корпус, каб. 101", "Главный корпус", 1, "101", "classroom", "Учебная аудитория №1"),
            ("Главный корпус, каб. 102", "Главный корпус", 1, "102", "classroom", "Учебная аудитория №2"),
            ("Главный корпус, каб. 201", "Главный корпус", 2, "201", "office", "Кабинет директора"),
            ("Главный корпус, серверная", "Главный корпус", -1, "СРВ", "server", "Серверная комната"),
            ("Лабораторный корпус, лаб. 1", "Лабораторный корпус", 1, "Л-1", "lab", "Компьютерная лаборатория"),
            ("Лабораторный корпус, лаб. 2", "Лабораторный корпус", 2, "Л-2", "lab", "Лаборатория электроники"),
            ("Склад №1", "Хозблок", 1, "СК-1", "storage", "Склад запчастей и расходников"),
            ("Учебный центр, каб. 301", "Учебный центр", 3, "301", "classroom", "Мультимедийный класс"),
            ("Административный корпус, бухгалтерия", "Административный корпус", 2, "Б-1", "office", "Бухгалтерия"),
            ("Главный корпус, каб. 103", "Главный корпус", 1, "103", "other", "Приёмная комиссия"),
        ]
        locations = []
        for name, building, floor, room, loc_type, notes in locations_data:
            loc = Location(name=name, building=building, floor=floor, room=room, location_type=loc_type, notes=notes)
            session.add(loc)
            locations.append(loc)
        session.flush()

        # ────────────────────────────────
        # 2. Employees (10)
        # ────────────────────────────────
        employees_data = [
            ("Иванов Иван Иванович", "Директор", "Администрация", "001", "+7(123)111-11-11", "ivanov@edu.ru", date(2010, 9, 1)),
            ("Петрова Мария Сергеевна", "Главный бухгалтер", "Бухгалтерия", "002", "+7(123)111-11-12", "petrova@edu.ru", date(2012, 3, 15)),
            ("Сидоров Алексей Николаевич", "Системный администратор", "ИТ-отдел", "003", "+7(123)111-11-13", "sidorov@edu.ru", date(2015, 6, 1)),
            ("Кузнецова Елена Владимировна", "Преподаватель", "Учебный отдел", "004", "+7(123)111-11-14", "kuznetsova@edu.ru", date(2018, 9, 1)),
            ("Смирнов Дмитрий Олегович", "Инженер-электроник", "ИТ-отдел", "005", "+7(123)111-11-15", "smirnov@edu.ru", date(2016, 4, 10)),
            ("Васильева Анна Павловна", "Завхоз", "Хозяйственный отдел", "006", "+7(123)111-11-16", "vasilieva@edu.ru", date(2013, 11, 20)),
            ("Зайцев Михаил Андреевич", "Преподаватель", "Учебный отдел", "007", "+7(123)111-11-17", "zaitsev@edu.ru", date(2020, 2, 1)),
            ("Морозова Татьяна Викторовна", "Делопроизводитель", "Администрация", "008", "+7(123)111-11-18", "morozova@edu.ru", date(2019, 8, 15)),
            ("Новиков Павел Сергеевич", "Техник", "ИТ-отдел", "009", "+7(123)111-11-19", "novikov@edu.ru", date(2021, 5, 5)),
            ("Козлова Ольга Игоревна", "Преподаватель", "Учебный отдел", "010", "+7(123)111-11-20", "kozlova@edu.ru", date(2017, 9, 1)),
        ]
        employees = []
        for full_name, position, department, emp_num, phone, email, hire_date in employees_data:
            emp = Employee(
                full_name=full_name, position=position, department=department,
                employee_number=emp_num, phone=phone, email=email,
                hire_date=hire_date, is_active=1,
            )
            session.add(emp)
            employees.append(emp)
        session.flush()

        # ────────────────────────────────
        # 3. Equipment (15)
        # ────────────────────────────────
        equipment_data = [
            ("ОБ-0001", "Ноутбук HP EliteBook 840 G8", "Ноутбук", "840 G8", "SN-HP-001", "in_use", "ООО «Техносфера»", Decimal("85000.00"), date(2023, 1, 15), date(2023, 2, 1), date(2023, 2, 10), date(2026, 2, 10), None, 0, 2),
            ("ОБ-0002", "МФУ Kyocera ECOSYS M4125idn", "МФУ", "M4125idn", "SN-KYO-001", "in_use", "ООО «Офисная техника»", Decimal("120000.00"), date(2022, 6, 10), date(2022, 7, 1), date(2022, 7, 15), date(2025, 7, 15), None, 1, 8),
            ("ОБ-0003", "ПК Lenovo ThinkCentre M75s", "Компьютер", "M75s", "SN-LEN-001", "in_use", "ООО «Компьютерный мир»", Decimal("62000.00"), date(2023, 3, 1), date(2023, 3, 20), date(2023, 4, 1), date(2026, 4, 1), None, 4, 3),
            ("ОБ-0004", "Принтер HP LaserJet Pro M404dn", "Принтер", "M404dn", "SN-HP-002", "in_use", "ООО «Офисная техника»", Decimal("35000.00"), date(2022, 9, 5), date(2022, 9, 20), date(2022, 10, 1), date(2025, 10, 1), None, 2, 1),
            ("ОБ-0005", "Интерактивная панель Samsung Flip 65\"", "Интерактивная панель", "WM65B", "SN-SAM-001", "in_use", "ООО «МедиаТех»", Decimal("280000.00"), date(2023, 8, 1), date(2023, 8, 25), date(2023, 9, 1), date(2026, 9, 1), None, 7, 4),
            ("ОБ-0006", "Ноутбук Dell Latitude 5430", "Ноутбук", "5430", "SN-DELL-001", "under_maintenance", "ООО «Техносфера»", Decimal("78000.00"), date(2022, 2, 10), date(2022, 3, 1), date(2022, 3, 10), date(2025, 3, 10), None, 4, 3),
            ("ОБ-0007", "Монитор Dell UltraSharp U2422H", "Монитор", "U2422H", "SN-DELL-002", "in_use", "ООО «Компьютерный мир»", Decimal("22000.00"), date(2023, 4, 1), date(2023, 4, 15), date(2023, 4, 20), date(2026, 4, 20), None, 5, 5),
            ("ОБ-0008", "ИБП APC Smart-UPS 1000", "ИБП", "SUA1000I", "SN-APC-001", "in_use", "ООО «ЭнергоПро»", Decimal("45000.00"), date(2021, 11, 1), date(2021, 11, 20), date(2021, 12, 1), date(2024, 12, 1), None, 3, 3),
            ("ОБ-0009", "Сервер SuperMicro 2U", "Сервер", "SYS-2029", "SN-SUP-001", "in_use", "ООО «Серверные решения»", Decimal("450000.00"), date(2022, 1, 10), date(2022, 2, 1), date(2022, 2, 15), date(2027, 2, 15), None, 3, 3),
            ("ОБ-0010", "Ноутбук Asus VivoBook 15", "Ноутбук", "X513EA", "SN-ASUS-001", "reserved", "ООО «Техносфера»", Decimal("55000.00"), date(2023, 10, 1), date(2023, 10, 20), date(2023, 11, 1), date(2026, 11, 1), None, 0, 0),
            ("ОБ-0011", "МФУ Canon i-SENSYS MF445dw", "МФУ", "MF445dw", "SN-CAN-001", "in_use", "ООО «Офисная техника»", Decimal("95000.00"), date(2023, 5, 15), date(2023, 6, 1), date(2023, 6, 10), date(2026, 6, 10), None, 8, 2),
            ("ОБ-0012", "Коммутатор Cisco Catalyst 2960X", "Сетевое оборудование", "2960X", "SN-CIS-001", "in_use", "ООО «Сетевые технологии»", Decimal("135000.00"), date(2022, 4, 1), date(2022, 4, 20), date(2022, 5, 1), date(2027, 5, 1), None, 3, 3),
            ("ОБ-0013", "Компьютер iRU Home 510", "Компьютер", "510", "SN-IRU-001", "written_off", "ООО «Компьютерный мир»", Decimal("35000.00"), date(2018, 3, 1), date(2018, 3, 15), date(2018, 4, 1), date(2021, 4, 1), date(2023, 12, 20), 6, 6),
            ("ОБ-0014", "Проектор Epson EB-X41", "Проектор", "EB-X41", "SN-EPS-001", "in_use", "ООО «МедиаТех»", Decimal("42000.00"), date(2022, 8, 1), date(2022, 8, 20), date(2022, 9, 1), date(2025, 9, 1), None, 7, 4),
            ("ОБ-0015", "Ноутбук Apple MacBook Air M2", "Ноутбук", "MacBook Air M2", "SN-APP-001", "in_use", "ООО «Техносфера»", Decimal("140000.00"), date(2023, 9, 1), date(2023, 9, 15), date(2023, 10, 1), date(2026, 10, 1), None, 0, 9),
        ]
        equipment_list = []
        for inv_num, name, cat, model, sn, status, supplier, cost, p_date, r_date, c_date, w_date, wo_date, loc_idx, emp_idx in equipment_data:
            eq = Equipment(
                inventory_number=inv_num, name=name, category=cat, model=model,
                serial_number=sn, status=status, supplier=supplier, cost=cost,
                purchase_date=p_date, received_date=r_date, commissioned_date=c_date,
                warranty_until=w_date, written_off_date=wo_date,
                location_id=locations[loc_idx].id,
                responsible_employee_id=employees[emp_idx].id,
            )
            session.add(eq)
            equipment_list.append(eq)
        session.flush()

        # ────────────────────────────────
        # 4. Documents (7)
        # ────────────────────────────────
        documents_data = [
            ("Акт приёма-передачи", "АП-2023/01", date(2023, 2, 10), "Акт приёма-передачи ноутбука HP", "active", employees[2].id, employees[0].id, date(2023, 2, 15), equipment_list[0].id, locations[0].id),
            ("Договор поставки", "Д-2023/45", date(2023, 1, 10), "Договор поставки оргтехники №45", "active", employees[0].id, None, None, None, None),
            ("Акт выполненных работ", "АВР-2024/03", date(2024, 3, 15), "Ремонт ноутбука Dell Latitude 5430", "active", employees[3].id, employees[0].id, date(2024, 3, 20), equipment_list[5].id, None),
            ("Накладная", "Н-2023/112", date(2023, 9, 20), "Поступление интерактивной панели", "active", employees[6].id, None, None, equipment_list[4].id, locations[6].id),
            ("Приказ", "П-2023/05", date(2023, 4, 1), "О назначении ответственных лиц", "active", employees[0].id, None, date(2023, 4, 1), None, None),
            ("Акт списания", "АС-2023/01", date(2023, 12, 20), "Списание компьютера iRU Home 510", "active", employees[2].id, employees[0].id, date(2023, 12, 22), equipment_list[12].id, None),
            ("Гарантийный талон", "ГТ-2023/08", date(2023, 8, 10), "Гарантия на МФУ Canon", "archived", employees[1].id, None, None, equipment_list[10].id, None),
        ]
        documents = []
        for doc_type, doc_number, doc_date, title, status, created_by, approved_by, approved_date, eq_id, loc_id in documents_data:
            doc = Document(
                doc_type=doc_type, doc_number=doc_number, doc_date=doc_date,
                title=title, status=status, created_by_id=created_by,
                approved_by_id=approved_by, approved_date=approved_date,
                equipment_id=eq_id, location_id=loc_id,
            )
            session.add(doc)
            documents.append(doc)
        session.flush()

        # ────────────────────────────────
        # 5. EquipmentMovements (5)
        # ────────────────────────────────
        movements_data = [
            (equipment_list[5].id, locations[4].id, locations[3].id, employees[2].id, documents[2].id, datetime(2024, 3, 14, 10, 0), "Передано в ремонт"),
            (equipment_list[0].id, None, locations[0].id, employees[2].id, documents[0].id, datetime(2023, 2, 10, 14, 30), "Поступление нового оборудования"),
            (equipment_list[12].id, locations[5].id, locations[6].id, employees[5].id, documents[5].id, datetime(2023, 12, 19, 11, 0), "Перемещение на склад перед списанием"),
            (equipment_list[4].id, locations[6].id, locations[7].id, employees[3].id, documents[3].id, datetime(2023, 9, 25, 15, 0), "Установка интерактивной панели в аудитории"),
            (equipment_list[9].id, None, locations[0].id, employees[2].id, None, datetime(2023, 11, 1, 9, 0), "Поступление резервного ноутбука"),
        ]
        for eq, from_loc, to_loc, moved_by, doc, moved_at, reason in movements_data:
            m = EquipmentMovement(
                equipment_id=eq, from_location_id=from_loc, to_location_id=to_loc,
                moved_by_id=moved_by, document_id=doc, moved_at=moved_at, reason=reason,
            )
            session.add(m)

        # ────────────────────────────────
        # 6. MaintenanceRecords (5)
        # ────────────────────────────────
        maintenance_data = [
            (equipment_list[5].id, documents[2].id, "repair", "completed", "Замена клавиатуры и термопасты", datetime(2024, 3, 18, 12, 0), datetime(2025, 3, 18), "ИП Смирнов", Decimal("3200.00"), "Работы выполнены в полном объёме"),
            (equipment_list[0].id, None, "preventive", "completed", "Плановое ТО: чистка, замена термопасты", datetime(2024, 1, 15, 10, 0), datetime(2025, 1, 15), "Сидоров А.Н.", Decimal("0.00"), "Замечаний нет"),
            (equipment_list[8].id, None, "diagnostic", "completed", "Диагностика сервера после обновления ПО", datetime(2024, 2, 20, 16, 0), None, "Сидоров А.Н.", Decimal("0.00"), "Ошибок не выявлено"),
            (equipment_list[12].id, None, "upgrade", "completed", "Модернизация: установка SSD и доп. RAM", datetime(2023, 6, 15, 14, 0), None, "Новиков П.С.", Decimal("8500.00"), "Производительность повышена"),
            (equipment_list[6].id, None, "preventive", "planned", "Плановое обслуживание мониторов", None, datetime(2024, 12, 1), "Новиков П.С.", Decimal("0.00"), None),
        ]
        for eq, doc, m_type, status, desc, performed, next_due, executor, cost, result in maintenance_data:
            mr = MaintenanceRecord(
                equipment_id=eq, document_id=doc, maintenance_type=m_type, status=status,
                description=desc, performed_at=performed, next_due_at=next_due,
                executor=executor, cost=cost, result=result,
            )
            session.add(mr)

        # ────────────────────────────────
        # 7. WriteOffActs (2)
        # ────────────────────────────────
        write_off_data = [
            ("АС-2023/01", date(2023, 12, 20), "Физический износ, невозможность ремонта", "Списать, утилизировать", "completed", "Иванов И.И., Петрова М.С., Смирнов Д.О.", equipment_list[12].id, documents[5].id),
            ("АС-2024/02", date(2024, 4, 15), "Морально устарел, не соответствует требованиям", "Списать, передать на утилизацию", "pending", "Иванов И.И., Кузнецова Е.В., Сидоров А.Н.", equipment_list[3].id, None),
        ]
        for act_num, act_date, reason, decision, status, members, eq_id, doc_id in write_off_data:
            wo = WriteOffAct(
                act_number=act_num, act_date=act_date, reason=reason, decision=decision,
                status=status, commission_members=members, equipment_id=eq_id, document_id=doc_id,
            )
            session.add(wo)

        # ────────────────────────────────
        # 8. InventoryChecks + Items (2 checks)
        # ────────────────────────────────
        check1 = InventoryCheck(
            started_at=datetime(2023, 12, 1, 9, 0),
            finished_at=datetime(2023, 12, 5, 18, 0),
            status="completed",
            summary="Инвентаризация показала расхождение по 1 единице",
            location_id=locations[0].id,
            performed_by_id=employees[2].id,
        )
        session.add(check1)
        session.flush()

        check_items_1 = [
            (equipment_list[0].id, "in_use", "in_use", locations[0].id, "ОК"),
            (equipment_list[1].id, "in_use", "in_use", locations[1].id, "ОК"),
            (equipment_list[3].id, "in_use", "in_use", locations[2].id, "ОК"),
            (equipment_list[5].id, "in_use", "under_maintenance", locations[4].id, "Обнаружена неисправность"),
            (equipment_list[9].id, "in_use", "reserved", locations[0].id, "В резерве, не используется"),
        ]
        for eq_id, expected, actual, loc_id, comment in check_items_1:
            item = InventoryCheckItem(
                check_id=check1.id, equipment_id=eq_id,
                expected_status=expected, actual_status=actual,
                actual_location_id=loc_id, comment=comment,
            )
            session.add(item)

        check2 = InventoryCheck(
            started_at=datetime(2024, 6, 10, 9, 0),
            status="in_progress",
            location_id=locations[7].id,
            performed_by_id=employees[6].id,
        )
        session.add(check2)
        session.flush()

        check_items_2 = [
            (equipment_list[4].id, "in_use", "in_use", locations[7].id, None),
            (equipment_list[13].id, "in_use", "in_use", locations[7].id, None),
        ]
        for eq_id, expected, actual, loc_id, comment in check_items_2:
            item = InventoryCheckItem(
                check_id=check2.id, equipment_id=eq_id,
                expected_status=expected, actual_status=actual,
                actual_location_id=loc_id, comment=comment,
            )
            session.add(item)

        # ────────────────────────────────
        # 9. NetworkNodes (5)
        # ────────────────────────────────
        nodes_data = [
            ("Core-SW-01", "switch", "192.168.1.1", "AA:BB:CC:00:00:01", "Cisco", "Catalyst 2960X", "SN-CIS-N001", "active", locations[3].id, "Основной коммутатор ядра сети"),
            ("Distr-SW-02", "switch", "192.168.1.2", "AA:BB:CC:00:00:02", "Cisco", "Catalyst 2960", "SN-CIS-N002", "active", locations[0].id, "Коммутатор доступа главного корпуса"),
            ("Main-Router", "router", "192.168.0.1", "AA:BB:CC:00:00:10", "MikroTik", "CCR1036", "SN-MIK-001", "active", locations[3].id, "Основной маршрутизатор"),
            ("File-Server", "server", "192.168.1.10", "AA:BB:CC:00:01:01", "SuperMicro", "SYS-2029", "SN-SUP-001", "active", locations[3].id, "Файловый сервер"),
            ("AP-101", "access_point", "192.168.2.10", "AA:BB:CC:00:02:01", "Ubiquiti", "U6-LR", "SN-UBI-001", "active", locations[0].id, "Точка доступа в каб. 101"),
        ]
        nodes = []
        for name, n_type, ip, mac, vendor, model, sn, status, loc_id, notes in nodes_data:
            node = NetworkNode(
                name=name, node_type=n_type, ip_address=ip, mac_address=mac,
                vendor=vendor, model=model, serial_number=sn,
                status=status, location_id=loc_id, notes=notes,
            )
            session.add(node)
            nodes.append(node)
        session.flush()

        # ────────────────────────────────
        # 10. NetworkLinks (5)
        # ────────────────────────────────
        links_data = [
            (nodes[2].id, nodes[0].id, "ge0/0", "ge1/0/1", "fiber", "active", "Оптика до основного коммутатора"),
            (nodes[0].id, nodes[1].id, "ge1/0/1", "ge0/1", "ethernet", "active", "Соединение с коммутатором доступа"),
            (nodes[0].id, nodes[3].id, "ge1/0/2", "eth0", "ethernet", "active", "Подключение файлового сервера"),
            (nodes[1].id, nodes[4].id, "ge0/2", "eth0", "ethernet", "active", "Точка доступа Wi-Fi"),
            (nodes[2].id, nodes[1].id, "ge0/1", "ge0/24", "ethernet", "inactive", "Резервное соединение (отключено)"),
        ]
        for from_id, to_id, port_from, port_to, link_type, status, notes in links_data:
            link = NetworkLink(
                from_node_id=from_id, to_node_id=to_id,
                port_from=port_from, port_to=port_to,
                link_type=link_type, status=status, notes=notes,
            )
            session.add(link)

        # ────────────────────────────────
        session.commit()
        print("База данных успешно заполнена тестовыми данными!")


if __name__ == "__main__":
    seed()
