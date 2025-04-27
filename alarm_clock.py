import flet as ft
import pandas as pd
import calendar
from datetime import datetime

try:
    df_excel = pd.read_excel('Новая таблица (3).xlsx')
except FileNotFoundError:
    df_excel = pd.DataFrame(columns=["Время", "Название", "Количество", "Мера", "Период"])


def main(page: ft.Page):
    page.title = "Умная таблетница"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    # Элементы ввода
    hour_tf = ft.TextField(
        label="Часы (00-23)", width=100,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    minute_tf = ft.TextField(
        label="Минуты (00-59)", width=100,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    name_pill = ft.TextField(
        label="Название", width=150,
        text_align=ft.TextAlign.CENTER
    )
    volume = ft.TextField(
        label="Количество", width=150,
        text_align=ft.TextAlign.CENTER
    )
    volumet = ft.TextField(
        label="Мера", width=150,
        text_align=ft.TextAlign.CENTER
    )

    status = ft.Text(size=20)
    current_period = "Месяц"
    selected_day = datetime.now().day
    selected_month = datetime.now().month
    selected_year = datetime.now().year

    def clear_fields():
        """Очищает все поля ввода"""
        hour_tf.value = ""
        minute_tf.value = ""
        name_pill.value = ""
        volume.value = ""
        volumet.value = ""
        page.update()


    def show_list(e):

        """Показывает список напоминаний в виде аккуратной таблицы"""
        # Создаем DataTable с фиксированными столбцами
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Название", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Время", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Количество", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Мера", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Период", weight=ft.FontWeight.BOLD)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row["Название"]), text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(str(row["Время"]), text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(str(row["Количество"]), text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(str(row["Мера"]), text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(str(row["Период"]), text_align=ft.TextAlign.CENTER)),
                    ]
                ) for _, row in df_excel.iterrows()
            ],
            column_spacing=20,
            heading_row_color=ft.colors.BLUE_GREY_100,
        )


        # Очищаем страницу и добавляем таблицу
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("Список напоминаний", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=data_table,
                        padding=10,
                        border=ft.border.all(1, ft.colors.GREY_300),
                        border_radius=10,
                    ),
                    ft.ElevatedButton("Назад",on_click=lambda _: show_main_page(),
),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )


    def on_click_month(e):
        nonlocal current_period
        current_period = "Месяц"
        status.value = f"Выбран период: {current_period}"
        status.color = ft.colors.BLUE
        page.update()

    month = ft.ElevatedButton("Месяц", on_click=on_click_month)

    def on_click_day(e):
        nonlocal current_period
        current_period = "День"
        status.value = f"Выбран период: {current_period}"
        status.color = ft.colors.BLUE
        page.update()

    day = ft.ElevatedButton("День", on_click=on_click_day)

    def on_click_week(e):
        nonlocal current_period
        current_period = "Неделя"
        status.value = f"Выбран период: {current_period}"
        status.color = ft.colors.BLUE
        page.update()

    week = ft.ElevatedButton("Неделя", on_click=on_click_week)

    def save_to_excel():
        """Сохраняет данные в Excel файл"""
        # Форматируем период в зависимости от выбора
        if current_period in ["День", "Неделя", "Месяц"]:
            period_value = current_period
        else:
            period_value = f"{selected_day:02d}.{selected_month:02d}.{selected_year}"

        new_data = {
            "Время": f"{hour_tf.value}:{minute_tf.value}",
            "Название": name_pill.value,
            "Количество": volume.value,
            "Мера": volumet.value,
            "Период": period_value
        }
        global df_excel
        df_excel = pd.concat([df_excel, pd.DataFrame([new_data])], ignore_index=True)
        df_excel.to_excel('Новая таблица.xlsx', index=False)
        clear_fields()  # Очищаем поля после сохранения

    def show_calendar(e):
        """Показывает календарь для выбора даты"""
        page.clean()

        now = datetime.now()
        current_year = now.year
        current_month = now.month
        selected_day = now.day

        month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        a = current_year
        header = ft.Text(
            value=f"{month_names[current_month - 1]} {current_year}",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        def calendar_month(e):
            nonlocal current_year
            current_year +=1


        def select_date(e):
    
            nonlocal current_period
            current_period = f"{selected_day:02d}.{current_month:02d}.{current_year}"
            status.value = f"Выбрана дата: {current_period}"
            status.color = ft.colors.BLUE
            show_main_page()

        def prev_month(e):
            nonlocal current_month, current_year
            current_month -= 1
            if current_month == 0:
                current_month = 12
                current_year -= 1
            header.value = f"{month_names[current_month - 1]} {current_year}"
            update_calendar()

        def next_month(e):
            nonlocal current_month, current_year
            current_month += 1
            if current_month == 13:
                current_month = 1
                current_year += 1
            header.value = f"{month_names[current_month - 1]} {current_year}"
            update_calendar()

        nav_buttons = ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=prev_month),
                ft.IconButton(icon=ft.icons.ARROW_FORWARD, on_click=next_month),
                ft.ElevatedButton("Выбрать дату", on_click=select_date),
                ft.ElevatedButton("Год", on_click=calendar_month)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        selected_date_display = ft.Text(
            value=f"Выбрано: {selected_day:02d}.{current_month:02d}.{current_year}",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE,
        )

        calendar_grid = ft.Column(spacing=10)

        def update_calendar():
            calendar_grid.controls.clear()

            weekday_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            week_header = ft.Row(
                controls=[ft.Text(day, size=14, weight=ft.FontWeight.BOLD,
                                  width=40, text_align=ft.TextAlign.CENTER)
                          for day in weekday_names],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            )
            calendar_grid.controls.append(week_header)

            cal = calendar.monthcalendar(current_year, current_month)
            for week in cal:
                week_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)
                for day in week:
                    day_text = str(day) if day != 0 else ""
                    day_btn = ft.ElevatedButton(
                        content=ft.Text(day_text, size=14),
                        width=40,
                        height=40,
                        on_click=lambda e, d=day: select_day(d),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.BLUE_100 if day == selected_day and day != 0
                            else ft.colors.TRANSPARENT,
                        ),
                    )
                    week_row.controls.append(day_btn)
                calendar_grid.controls.append(week_row)
            page.update()

        def select_day(day):
            nonlocal selected_day
            if day == 0:
                return
            selected_day = day
            selected_date_display.value = f"Выбрано: {day:02d}.{current_month:02d}.{current_year}"
            update_calendar()

        back_button = ft.ElevatedButton(
            "Назад",
            on_click=lambda _: show_main_page(),
            bgcolor=ft.colors.BLUE_500,
            color=ft.colors.WHITE,
        )

        update_calendar()

        page.add(
            ft.Column(
                [
                    header,
                    nav_buttons,
                    selected_date_display,
                    calendar_grid,
                    back_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def show_main_page():
        """Показывает главную страницу приложения"""
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("Выберите время", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([hour_tf, minute_tf], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text("Введите название", size=20, weight=ft.FontWeight.BOLD),
                    name_pill,
                    ft.Text("Введите количество", size=20, weight=ft.FontWeight.BOLD),
                    volume,
                    ft.Text("Введите меру", size=20, weight=ft.FontWeight.BOLD),
                    volumet,
                    ft.Text("Выберите период", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([day, week, month], alignment=ft.MainAxisAlignment.CENTER),
                    ft.ElevatedButton("Выбрать дату", on_click=show_calendar),
                    ft.Divider(height=20),
                    ft.ElevatedButton("Добавить таблетку", on_click=set_alarm),
                    ft.ElevatedButton("Показать список", on_click=show_list),
                    status,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def set_alarm(e):
        try:
            h = int(hour_tf.value)
            m = int(minute_tf.value)

            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError("Некорректное время!")

            save_to_excel()
            status.value = f"Таблетка {name_pill.value} добавлена!"
            status.color = ft.colors.GREEN
            page.update()
        except ValueError as ve:
            status.value = f"Ошибка! {str(ve)}"
            status.color = ft.colors.RED
            page.update()

    show_main_page()


ft.app(target=main)
