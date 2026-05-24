import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import csv

FILE = "matatu_system.json"



def load_data():
    if not os.path.exists(FILE):
        return {
            "expenses": [],
            "crowd_reports": [],
            "safety_reports": [],
            "ratings": {}
        }
    with open(FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)



ROUTES = {
    "Ngong - CBD": (70, 120),
    "Rongai - CBD": (60, 110),
    "Kikuyu - CBD": (80, 120),
    "Thika - CBD": (90, 150),
    "Ruaka - CBD": (50, 90),
}


def time_band():
    h = datetime.now().hour
    if 6 <= h < 10:
        return "rush_morning"
    elif 16 <= h < 20:
        return "rush_evening"
    return "normal"


def predict_fare(route):
    low, high = ROUTES[route]
    band = time_band()

    if band in ["rush_morning", "rush_evening"]:
        return high
    return low


def add_expense(data):
    print("\n ADD EXPENSE ")
    routes = list(ROUTES.keys())

    for i, r in enumerate(routes, 1):
        print(f"{i}. {r} (expected {predict_fare(r)} KES)")

    idx = int(input("Select route: ")) - 1
    route = routes[idx]

    expected = predict_fare(route)
    print(f"Suggested fare: {expected}")

    amount = input("Use suggested? (y/n): ")

    if amount.lower() == "y":
        amount = expected
    else:
        amount = float(input("Enter amount: "))

    data["expenses"].append({
        "route": route,
        "amount": amount,
        "time": time_band(),
        "date": datetime.now().strftime("%Y-%m-%d")
    })

    save_data(data)
    print("Saved!")




def report_crowd(data):
    print("\nCrowd Status: empty / half / full / packed")
    route = input("Route: ")
    status = input("Status: ")

    data["crowd_reports"].append({
        "route": route,
        "status": status,
        "time": datetime.now().strftime("%H:%M")
    })

    save_data(data)


def crowd_score(data, route):
    reports = [r for r in data["crowd_reports"] if r["route"] == route]

    if not reports:
        return "No data"

    score_map = {"empty": 1, "half": 2, "full": 3, "packed": 4}

    avg = sum(score_map.get(r["status"], 2) for r in reports) / len(reports)

    if avg < 1.5:
        return "Low crowd"
    elif avg < 2.5:
        return "Moderate crowd"
    elif avg < 3.5:
        return "High crowd"
    return "Very crowded"



def report_incident(data):
    print("\nIncident types: reckless / harassment / overloading / theft")
    route = input("Route: ")
    incident = input("Type: ")

    data["safety_reports"].append({
        "route": route,
        "incident": incident,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    save_data(data)


def safety_score(data, route):
    reports = [r for r in data["safety_reports"] if r["route"] == route]

    base = 5
    penalty = len(reports) * 0.3
    score = max(1, base - penalty)

    return round(score, 1)


def summaries(data):
    print("\n DAILY / MONTHLY SUMMARY ")

    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%Y-%m")

    daily = sum(e["amount"] for e in data["expenses"] if e["date"] == today)
    monthly = sum(e["amount"] for e in data["expenses"] if e["date"].startswith(month))
    total = sum(e["amount"] for e in data["expenses"])

    print("Today:", daily)
    print("Month:", monthly)
    print("Total:", total)


def route_analysis(data):
    print("\n ROUTE INSIGHTS ")

    routes = {}

    for e in data["expenses"]:
        routes[e["route"]] = routes.get(e["route"], 0) + e["amount"]

    for r, v in routes.items():
        print(f"{r}: {v} KES | Crowd: {crowd_score(data, r)} | Safety: {safety_score(data, r)}")





def commuter_dashboard(data):
    print("\n--- COMMUTER DASHBOARD ---")

    route = input("Enter route: ")

    print("Predicted fare:", predict_fare(route))
    print("Crowd level:", crowd_score(data, route))
    print("Safety rating:", safety_score(data, route))


def main():
    data = load_data()

    while True:
        print("\n MATATU INTELLIGENCE SYSTEM ")
        print("1. Add Expense")
        print("2. Crowd Report")
        print("3. Safety Report")
        print("4. Summaries")
        print("5. Route Analysis")
        print("6. Commuter Dashboard")
        print("7. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_expense(data)
        elif choice == "2":
            report_crowd(data)
        elif choice == "3":
            report_incident(data)
        elif choice == "4":
            summaries(data)
        elif choice == "5":
            route_analysis(data)
        elif choice == "6":
            commuter_dashboard(data)
        elif choice == "7":
            break


if __name__ == "__main__":
    main()