import flet as ft
import time
from datetime import datetime
import winsound
import pandas as pd
import threading


try:
    df_excel = pd.read_excel('Новая таблица (2).xlsx')
except FileNotFoundError:
    df_excel = pd.DataFrame(columns=["Время", "Название", "Количество", "Мера"])


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
        label="Название таблетки", width=150,
        text_align=ft.TextAlign.CENTER
    )
    volume = ft.TextField(
        label="Количество", width=150,
        text_align=ft.TextAlign.CENTER
    )
    volumet = ft.TextField(
        label="Мера (мг/мл и т.д.)", width=150,
        text_align=ft.TextAlign.CENTER
    )

    alarm_time = None
    is_alarm_set = False
    time_display = ft.Text(size=40, weight=ft.FontWeight.BOLD)
    status = ft.Text(size=20)

    def on_click(e):  # Функция, вызываемая при нажатии
        page.add(ft.Text(df_excel))  # Добавляем текст на экран

    button = ft.ElevatedButton("Нажми меня", on_click=on_click)

    def save_to_excel():
        new_data = {
            "Время": f"{hour_tf.value}:{minute_tf.value}",
            "Название": name_pill.value,
            "Количество": volume.value,
            "Мера": volumet.value
        }
        global df_excel
        df_excel = pd.concat([df_excel, pd.DataFrame([new_data])], ignore_index=True)
        df_excel.to_excel('Новая таблица.xlsx', index=False)
        print("Данные сохранены в Excel:")
        print(df_excel)

    def update_clock():
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            time_display.value = current_time
            page.update()
            time.sleep(1)

            if is_alarm_set and now.hour == alarm_time[0] and now.minute == alarm_time[1]:
                trigger_alarm()

    def set_alarm(e):
        nonlocal alarm_time, is_alarm_set
        try:
            h = int(hour_tf.value)
            m = int(minute_tf.value)

            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError("Некорректное время!")

            alarm_time = (h, m)
            is_alarm_set = True
            status.value = f"⏰ Напоминание установлено на {h:02d}:{m:02d}"
            status.color = ft.colors.GREEN
            save_to_excel()  # Сохраняем данные в Excel
            page.update()
        except ValueError:
            status.value = "❌ Ошибка! Введите корректное время."
            status.color = ft.colors.RED
            page.update()

    def trigger_alarm():
        nonlocal is_alarm_set
        status.value = (f"💊 Примите: {name_pill.value} - "
                        f"{volume.value} {volumet.value}")
        status.color = ft.colors.RED
        page.update()
        winsound.Beep(2000, 3000)
        is_alarm_set = False

    # Интерфейс
    page.add(
        ft.Column(
            [
                ft.Text("Умная таблетница", size=30, weight=ft.FontWeight.BOLD),
                ft.Row([hour_tf, minute_tf], alignment=ft.MainAxisAlignment.CENTER),
                name_pill,
                volume,
                volumet,
                ft.ElevatedButton(
                    "Установить напоминание",
                    on_click=set_alarm,
                    height=50,
                    width=200
                ),
                ft.Divider(height=20),
                time_display,
                status,
                button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # Запуск обновления времени
    threading.Thread(target=update_clock, daemon=True).start()


ft.app(target=main)
