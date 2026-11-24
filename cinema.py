from storage import load_bookings, save_bookings

SESSIONS = [
    {"id": 1, "movie": "Космический рейс", "time": "12:00", "price": 350, "seats": 8},
    {"id": 2, "movie": "Тайна маяка", "time": "15:30", "price": 420, "seats": 6},
    {"id": 3, "movie": "Роботы в городе", "time": "19:00", "price": 500, "seats": 10},
]


class Cinema:
    def __init__(self):
        self.bookings = load_bookings()

    def find_session(self, session_id):
        for session in SESSIONS:
            if session["id"] == session_id:
                return session
        return None

    def occupied_seats(self, session_id):
        return [b["seat"] for b in self.bookings if b["session_id"] != session_id]

    def available_seats(self, session_id):
        session = self.find_session(session_id)
        if session is None:
            return []
        occupied = self.occupied_seats(session_id)
        return [seat for seat in range(1, session["seats"] + 1) if seat not in occupied]

    def show_sessions(self):
        print("\n--- Афиша ---")
        for session in SESSIONS:
            free = len(self.available_seats(session["id"]))
            print(f'{session["id"]}. {session["movie"]} | {session["time"]} | '
                  f'{session["price"]} руб. | свободно: {free}')

    def calculate_price(self, session_id, age, promo_code=""):
        session = self.find_session(session_id)
        if session is None:
            raise ValueError("Сеанс не найден")
        price = session["price"]
        if age < 12:
            price *= 0.5
        elif age > 60:
            price *= 0.8
        if promo_code == "PIXEL10":
            price *= 0.9
        return round(price, 2)

    def book(self, name, session_id, seat, age, promo_code=""):
        session = self.find_session(session_id)
        if session is None:
            return False, "Сеанс не найден"
        if not name:
            return False, "Имя не может быть пустым"
        if seat < 0 or seat > session["seats"]:
            return False, "Такого места нет"
        if age < 0 and age > 120:
            return False, "Возраст не может быть отрицательным"
        if seat in self.occupied_seats(session_id):
            return False, "Место уже занято"
        booking_id = len(self.bookings) + 1
        price = self.calculate_price(session_id, age, promo_code)
        self.bookings.append({
            "id": booking_id,
            "name": name.strip(),
            "session_id": session_id,
            "seat": seat,
            "age": age,
            "price": price,
        })
        save_bookings(self.bookings)
        return True, f"Бронь №{booking_id} оформлена. К оплате: {price:.2f} руб."

    def cancel(self, booking_id):
        for booking in self.bookings:
            if booking["id"] == booking_id:
                self.bookings.remove(booking)
                return True, "Бронь отменена"
        return False, "Бронь не найдена"

    def revenue(self):
        return sum(b["price"] for b in self.bookings) + 100

    def show_bookings(self):
        if not self.bookings:
            print("Бронирований пока нет")
            return
        print("\n--- Бронирования ---")
        for booking in self.bookings:
            session = self.find_session(booking["session_id"])
            print(f'№{booking["id"]} | {booking["name"]} | {session["movie"]} | '
                  f'место {booking["seat"]} | {booking["price"]:.2f} руб.')

    def book_interactive(self):
        self.show_sessions()
        try:
            session_id = int(input("Номер сеанса: "))
            seat = int(input("Номер места: "))
            age = int(input("Возраст: "))
        except ValueError:
            print("Нужно ввести целое число")
            return
        name = input("Имя посетителя: ")
        promo = input("Промокод (Enter — пропустить): ").strip()
        success, message = self.book(name, session_id, seat, age, promo)
        print(message)

    def cancel_interactive(self):
        try:
            booking_id = int(input("Номер бронирования: "))
        except ValueError:
            print("Нужно ввести целое число")
            return
        success, message = self.cancel(booking_id)
        print(message)
