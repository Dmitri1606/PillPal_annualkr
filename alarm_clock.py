import flet as ft
import pandas as pd

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
        label="Глютамин", width=150,
        text_align=ft.TextAlign.CENTER
    )
    volume = ft.TextField(
        label="4", width=150,
        text_align=ft.TextAlign.CENTER
    )
    volumet = ft.TextField(
        label="мл", width=150,
        text_align=ft.TextAlign.CENTER
    )

    status = ft.Text(size=20)
    current_period = "Месяц"  # Переменная для хранения текущего периода

    def show_list(e):
        # Обновляем отображение DataFrame
        page.controls.append(ft.Text(str(df_excel)))
        page.update()

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
            status.value = f"❌ Ошибка! {str(ve)}"
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
                ft.Row([day, week, month], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=20),
                add_button, 
                show_button, 
                status,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


ft.app(target=main)
