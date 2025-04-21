import flet as ft
import time
from datetime import datetime
import winsound

def main(page: ft.Page):
    page.title = "Будильник"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    # Поля для ввода времени
    hour_tf = ft.TextField(
        label="Часы (00-23)",
        width=100,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    minute_tf = ft.TextField(
        label="Минуты (00-59)",
        width=100,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    alarm_time = None
    is_alarm_set = False

    def update_clock():
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            time_display.value = current_time
            page.update()
            time.sleep(1)

            # Проверка срабатывания будильника
            if is_alarm_set and now.hour == alarm_time[0] and now.minute == alarm_time[1]:
                trigger_alarm()

    def set_alarm(e):
        nonlocal alarm_time, is_alarm_set
        try:
            h = int(hour_tf.value)
            m = int(minute_tf.value)

            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError("Некорректное время!")

            alarm_time = (h, m, 0)  # Добавляем 0 секунд для единообразия
            is_alarm_set = True
            status.value = f"⏰ Будильник установлен на {h:02d}:{m:02d}"
            status.color = ft.colors.GREEN
            page.update()
        except ValueError:
            status.value = "❌ Ошибка! Введите корректное время."
            status.color = ft.colors.RED
            page.update()

    def trigger_alarm():
        nonlocal is_alarm_set
        status.value = "🔔 Время вставать! 🔔"
        status.color = ft.colors.RED
        page.update()
        winsound.Beep(2000, 3000)  # Бип на 3 секунды
        is_alarm_set = False  # Сбрасываем будильник после срабатывания

    # Элементы интерфейса
    time_display = ft.Text(size=40, weight=ft.FontWeight.BOLD)
    status = ft.Text(size=20)

    page.add(
        ft.Column(
            [
                ft.Text("Будильник", size=30, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [hour_tf, minute_tf],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                ft.ElevatedButton(
                    "Установить будильник",
                    on_click=set_alarm,
                    height=50,
                    width=200
                ),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                time_display,
                status,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # Запуск обновления времени в отдельном потоке
    import threading
    clock_thread = threading.Thread(target=update_clock, daemon=True)
    clock_thread.start()

ft.app(target=main)