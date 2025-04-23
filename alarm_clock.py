import flet as ft
import pandas as pd

import calendar
from datetime import datetime


try:
    df_excel = pd.read_excel('Новая таблица (2).xlsx')
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
        label="Кличество", width=150,
        text_align=ft.TextAlign.CENTER
    )
    volumet = ft.TextField(
        label="Мера", width=150,
        text_align=ft.TextAlign.CENTER
    )

    status = ft.Text(size=20)
    current_period = "Месяц"  # Переменная для хранения текущего периода

    def create_home_view():
        return ft.View(
            "/",
            [
                ft.AppBar(
                    title=ft.Text("Главная страница", size=24, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.colors.BLUE_600,
                    color=ft.colors.WHITE,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Добро пожаловать в наше приложение!", size=20, weight=ft.FontWeight.NORMAL),
                            ft.ElevatedButton(
                                "Перейти на страницу 2",
                                on_click=lambda _: page.go("/page2"),
                                bgcolor=ft.colors.BLUE_500,
                                color=ft.colors.WHITE,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    alignment=ft.alignment.center,
                ),
            ],
        )

    def create_page2_view():
        return ft.View(
            "/page2",
            [
                ft.AppBar(
                    title=ft.Text("Страница 2", size=24, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.colors.BLUE_600,
                    color=ft.colors.WHITE,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Это вторая страница.", size=20, weight=ft.FontWeight.NORMAL),
                            ft.ElevatedButton(
                                "Вернуться на главную",
                                on_click=lambda _: page.go("/"),
                                bgcolor=ft.colors.BLUE_500,
                                color=ft.colors.WHITE,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    alignment=ft.alignment.center,
                ),
            ],
        )

    def show_list(e):
        # Обновляем отображение DataFrame
        page.controls.append(ft.Text(str(df_excel)))
        page.update()

    def create_home_view(page: ft.Page):
        return ft.View
        # Настройка страницы
        page.title = "Простой календарь"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Текущая дата и состояние
        now = datetime.now()
        current = {
            'year': now.year,
            'month': now.month,
            'day': now.day
        }

        # Элементы интерфейса
        month_display = ft.Text(size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        selected_date_display = ft.Text(
            value=f"Выбрано: {current['day']:02d}.{current['month']:02d}.{current['year']}",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE
        )
        calendar_grid = ft.Column(spacing=10)

        # Русские названия
        month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        weekday_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]


    def on_click_month(e):
        nonlocal current_period
        current_period = "Месяц"
        status.value = f"Выбран период: {current_period}"
        page.update()

    month = ft.ElevatedButton("Месяц", on_click=on_click_month)

    def on_click_day(e):
        nonlocal current_period
        current_period = "День"
        status.value = f"Выбран период: {current_period}"
        page.update()

    day = ft.ElevatedButton("День", on_click=on_click_day)

    def on_click_week(e):
        nonlocal current_period
        current_period = "Неделя"
        status.value = f"Выбран период: {current_period}"
        page.update()

    week = ft.ElevatedButton("Неделя", on_click=on_click_week)

    def save_to_excel():
        new_data = {
            "Время": f"{hour_tf.value}:{minute_tf.value}",
            "Название": name_pill.value,
            "Количество": volume.value,
            "Мера": volumet.value,
            "Период": current_period
        }
        global df_excel
        df_excel = pd.concat([df_excel, pd.DataFrame([new_data])], ignore_index=True)
        df_excel.to_excel('Новая таблица.xlsx', index=False)
        print("Данные сохранены в Excel:")
        print(df_excel)

    def on_click_kalendar(views,page):
     page.views.append(create_home_view())

    calendar = ft.ElevatedButton("Выбрать дату", on_click=on_click_kalendar)

    def set_alarm(e):
        try:
            h = int(hour_tf.value)
            m = int(minute_tf.value)

            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError("Некорректное время!")

            save_to_excel()  # Сохраняем данные в Excel
            status.value = f"Таблетка {name_pill.value} добавлена!"
            status.color = ft.colors.GREEN
            page.update()
        except ValueError as ve:
            status.value = f"Ошибка! {str(ve)}"
            status.color = ft.colors.RED
            page.update()

    # Создаем кнопку для добавления напоминания
    add_button = ft.ElevatedButton("Добавить напоминание", on_click=set_alarm)

    # Создаем кнопку для показа списка
    show_button = ft.ElevatedButton("Показать список", on_click=show_list)

    # Интерфейс
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
                ft.Row([day, week, month,calendar], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=20),
                add_button,
                show_button,
                status,


            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    def main2(page: ft.Page):
        page.title = "Flat Calendar with Date Selection"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        now = datetime.now()
        current_year = now.year
        current_month = now.month

        selected_day = now.day
        selected_month = current_month
        selected_year = current_year

        # Текстовое поле для вывода выбранной даты
        selected_date_display = ft.Text(
            value=f"Выбрано: {selected_day:02d}.{selected_month:02d}",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE,
        )

        def update_calendar(year, month):
            calendar_container.controls.clear()
            month_name = calendar.month_name[month]
            header.value = f"{month_name} {year}"

            weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
            weekday_row = ft.Row(
                controls=[ft.Container(
                    content=ft.Text(day, size=14, weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.center,
                    width=40,
                    height=40,
                ) for day in weekdays],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            )
            calendar_container.controls.append(weekday_row)

            cal = calendar.monthcalendar(year, month)
            for week in cal:
                week_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)
                for day in week:
                    day_text = str(day) if day != 0 else ""
                    bg_color = ft.colors.TRANSPARENT
                    border_color = ft.colors.TRANSPARENT

                    if day == now.day and month == now.month and year == now.year:
                        bg_color = ft.colors.BLUE_100

                    if day == selected_day and month == selected_month and year == selected_year:
                        border_color = ft.colors.BLUE
                        border_width = 2
                    else:
                        border_width = 0

                    day_btn = ft.ElevatedButton(
                        content=ft.Text(day_text, size=14),
                        width=40,
                        height=40,
                        on_click=lambda e, d=day: select_day(d, month, year),
                        style=ft.ButtonStyle(
                            bgcolor=bg_color,
                            shape=ft.RoundedRectangleBorder(radius=20),
                            side=ft.BorderSide(color=border_color, width=border_width),
                        ),
                    )
                    week_row.controls.append(day_btn)
                calendar_container.controls.append(week_row)
            page.update()

        def select_day(day, month, year):
            nonlocal selected_day, selected_month, selected_year
            if day == 0:
                return
            selected_day = day
            selected_month = month
            selected_year = year
            # Обновляем отображение выбранной даты (формат "дд.мм")
            selected_date_display.value = f"Выбрано: {day:02d}.{month:02d}"
            update_calendar(year, month)

        def prev_month(e):
            nonlocal current_month, current_year
            current_month -= 1
            if current_month == 0:
                current_month = 12
                current_year -= 1
            update_calendar(current_year, current_month)

        def next_month(e):
            nonlocal current_month, current_year
            current_month += 1
            if current_month == 13:
                current_month = 1
                current_year += 1
            update_calendar(current_year, current_month)

        header = ft.Text(
            value=f"{calendar.month_name[current_month]} {current_year}",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        nav_buttons = ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=prev_month),
                ft.IconButton(icon=ft.icons.ARROW_FORWARD, on_click=next_month),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        calendar_container = ft.Column(spacing=10)
        update_calendar(current_year, current_month)


ft.app(target=main)
