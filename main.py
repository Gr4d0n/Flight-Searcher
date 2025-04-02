import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import *

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

customer_data = data_manager.get_customer_emails()
customer_email_list = [row['whatIsYourEmail?'] for row in customer_data]

flight_search = FlightSearch()

notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "BOM"

for row in sheet_data:
    if row["iataCode"] == "":
        row['iataCode'] = flight_search.get_destination_code(row['city'])
        time.sleep(2)
# print(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}>>>")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    time.sleep(2)

    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights ......")
        stopover_flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(stopover_flights)

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        formatted_price = formatting_price(int(cheapest_flight.price))
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only GBP {formatted_price} to fly direct "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only GBP {formatted_price} to fly "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"with {cheapest_flight.stops} stop(s) "\
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        print(f"Lower price flight found to {destination['city']}!")
        notification_manager.send_sms(
            message_body=f"Low price alert! Only ₹{formatted_price} to fly\n"
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}\n, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )
