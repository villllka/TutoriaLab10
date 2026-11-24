from cinema import Cinema


def main():
    cinema = Cinema()
    while True:
        print("\n=== КИНОТЕАТР «ПИКСЕЛЬ» ===")
        print("1. Афиша и сеансы")
        print("2. Забронировать билет")
        print("3. Мои бронирования")
        print("4. Отменить бронирование")
        print("5. Выручка кинотеатра")
        print("0. Выход")
        choice = input("Ваш выбор: ").strip()
        if choice == "1":
            cinema.show_sessions()
        elif choice == "2":
            cinema.book_interactive()
        elif choice == "3":
            cinema.show_bookings()
        elif choice == "4":
            cinema.cancel_interactive()
        elif choice == "5":
            print(f"Выручка: {cinema.revenue():.2f} руб.")
        elif choice == "0":
            print("До встречи!")
            break
        else:
            print("Неизвестный пункт меню")


if __name__ == "__main__":
    main()
