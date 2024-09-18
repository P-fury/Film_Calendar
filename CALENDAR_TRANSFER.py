from pdfminer.high_level import extract_text
import re
from datetime import datetime
import pytz
from ics import Calendar, Event
import locale

# Ustawienie polskiego locale
locale.setlocale(locale.LC_TIME, 'pl_PL.UTF-8')

# Ścieżka do pliku PDF
pdf_path = '*** your pdf file ****'

# Wyciągnij tekst z PDF
pdf_text = extract_text(pdf_path)

# Regular expression do dopasowywania linii zawierających informacje o końcu dnia
koniec_pattern = re.compile(r'--- KONIEC DNIA (\d+) -- (.*?), (\d{1,2} \w+ \d{4})')

events = []

# Funkcja konwertująca daty z formatu dd.mm.yyyy na yyyy-mm-dd
def convert_date(date_str):
    return datetime.strptime(date_str, '%d %B %Y')

# Przetwarzanie informacji o końcu dnia
for match in koniec_pattern.finditer(pdf_text):
    day_number = match.group(1)
    day_of_week = match.group(2)
    date_str = match.group(3)

    # Konwersja daty
    date = convert_date(date_str)
    event_name = f" **** {day_number}"

    event = {
        "date": date,
        "description": event_name,
        "location": ""  # Brak dodatkowych informacji o lokalizacji
    }
    events.append(event)

# Tworzenie kalendarza i wydarzeń
cal = Calendar()

for event in events:
    cal_event = Event()
    cal_event.name = event['description']
    cal_event.begin = event['date'].replace(tzinfo=pytz.utc)
    cal_event.end = event['date'].replace(tzinfo=pytz.utc)
    cal_event.description = event['description']  # Opis zawiera tylko nazwę "Furioza_dzien {numer_dnia}"
    cal_event.location = event['location']
    cal.events.add(cal_event)

# Zapisanie do pliku .ics
ics_path = '*** your file name ***'
with open(ics_path, 'w') as f:
    f.writelines(cal)

print(f"Kalendarz zapisany do pliku: {ics_path}")
