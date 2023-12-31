import pandas as pd
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
import os
from pprint import pprint
from restaurant_data import RestaurantData
from time import sleep
import matplotlib.pyplot as plt

# -------------------------- Initial Set-Up --------------------------
# tk.Tk().withdraw()  # prevents an empty tkinter window from appearing

# Opening up CSV file choosen by user

# initial_dir = os.path.expanduser("~/Desktop")
# file_path = filedialog.askopenfilename(initialdir=initial_dir)
file_path = (
    "/Users/alehs/Downloads/DOHMH_New_York_City_Restaurant_Inspection_Results.csv"
)

# -------------------------- Processing the Data --------------------------

print("Processing Data...")

resturant_data = RestaurantData(file_path)
resturant_data.sort_by_rating()

data_frame = resturant_data.get_dataframe()

boroughs = resturant_data.get_boroughs()

# -------------------------- Operations --------------------------


def default_case():
    print("Wrong Choice, Please Try Again")
    sleep(1.5)


def most_A_grade():
    boro = ""
    most = 0

    for borough in boroughs:
        if most < len(boroughs[borough]):
            most = len(boroughs[borough])
            boro = borough

    print(f"Borough: {boro}\nA Grade Restaurants: {most}")


def most_A_grade_chart():
    img_path = Path(os.path.expanduser("~/Desktop")) / Path("pie_chart.png")

    borough_df = []

    for _, restaurants in boroughs.items():
        temp_df = pd.DataFrame(restaurants)
        borough_df.append(temp_df)

    out_df = pd.concat(borough_df, ignore_index=True)
    grouped_df = out_df.sort_values(by=["SCORE"]).groupby(["BORO"]).size()

    colors = ["#9EF4E6", "#00AF91", "#007965", "#89C9B8", "#42E6A4"]
    explode = (0.01, 0.01, 0.01, 0.01, 0.01)  # Add more values if needed

    pie_chart = grouped_df.plot(
        kind="pie",
        title="Number of A Grade Restaurants per Borough",
        colors=colors,
        explode=explode,
        autopct="%1.0f%%",
        figsize=(8, 8),
    )

    pie_chart.get_figure().savefig(img_path)
    plt.show()

    print('Image save to desktop under the name "pie_chart.png"')


def rating_base_data():
    csv_path = Path(os.path.expanduser("~/Desktop")) / Path("rating_data.csv")

    borough_df = []

    for _, restaurants in boroughs.items():
        temp_df = pd.DataFrame(restaurants)
        borough_df.append(temp_df)

    out_df = pd.concat(borough_df, ignore_index=True)

    out_df = out_df.sort_values(by=["SCORE"])

    out_df.to_csv(csv_path, index=False)

    print(
        'CSV file save to desktop under the name "rating_data.csv"\nFile is sorted by Rating'
    )


def boroughs_restaurants():
    csv_path = Path(os.path.expanduser("~/Desktop")) / Path("best_restaurants.csv")

    borough_df = []

    for _, restaurants in boroughs.items():
        temp_df = pd.DataFrame(restaurants)
        borough_df.append(temp_df)

    out_df = pd.concat(borough_df, ignore_index=True)

    out_df = out_df[out_df["SCORE"] == 0.0]

    out_df.to_csv(csv_path, index=False)

    print('CSV file save to desktop under the name "best_restaurants.csv"')


# -------------------------- Main Menu --------------------------
quit = False

options = {
    1: most_A_grade,
    2: most_A_grade_chart,
    3: rating_base_data,
    4: boroughs_restaurants,
}

while not quit:
    print("Main Menu".center(50, "-"))
    print("\nSelect and option by entering the number or character:\n")
    print("\t1: Get Borough with most grade A restaurants")
    print("\t2: Get Borough with most grade A restaurants Pie Chart")
    print("\t3: Export data of restaurant withing each borough base on rating")
    print("\t4: Export data of best restaurants from each borough")
    print("\tq: Exit")
    choice = input("Enter Choice: ")
    if choice == "q":
        quit = True
        continue

    print("\n")
    print("-" * 50)
    options.get(int(choice), default_case)()
    print("-" * 50)
    sleep(1)
