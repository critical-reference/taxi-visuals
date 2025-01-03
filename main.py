import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

yellow_tripdata_path = "C:/Users/elena/Desktop/NYCdata/yellow_tripdata_2024-02.parquet"
green_tripdata_path = "C:/Users/elena/Desktop/NYCdata/green_tripdata_2024-02.parquet"

yellow_tripdata = pd.read_parquet(yellow_tripdata_path)
green_tripdata = pd.read_parquet(green_tripdata_path)


def show_popular_dest(df):
    ydo = df.groupby('DOLocationID').size().reset_index(name='Frequency').sort_values(by='Frequency', ascending=False,
                                                                                      inplace=False)  # .head(10)
    ypu = df.groupby('PULocationID').size().reset_index(name='Frequency').sort_values(by='Frequency', ascending=False,
                                                                                      inplace=False)  # .head(10)

    plt.figure(figsize=(14, 8))
    plt.scatter(ydo['DOLocationID'], ydo['Frequency'], color='blue', alpha=0.6, s=40, label="Drop Off")
    plt.scatter(ypu['PULocationID'], ypu['Frequency'], color='red', alpha=0.6, s=40, label="Pick Up")

    plt.xlabel('Location ID')
    plt.ylabel('Frequency')
    plt.title('Distribution of Dropoff and Pickup Location')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.show()


def show_distance_frequency(df):
    average_trip_distance = df['trip_distance'].mean()

    print("Average trip distance:", average_trip_distance)

    plt.figure(figsize=(10, 6))
    plt.hist(df['trip_distance'], bins=30, color='skyblue', range=(0, 30))
    plt.axvline(average_trip_distance, color='red', linestyle='dashed', linewidth=2,
                label=f'Average Trip Distance: {average_trip_distance:.2f}')
    # Add labels and title
    plt.xlabel('Trip Distance')
    plt.ylabel('Frequency')
    plt.title('Distribution of Trip Distance')
    plt.legend()

    plt.show()


def show_green_avgs(df):
    average_trip_distance = df['trip_distance'].mean()
    median_trip_distance = df['trip_distance'].median()
    print("Average trip distance:", average_trip_distance)

    plt.figure(figsize=(10, 6))
    plt.hist(df['trip_distance'], bins=30, color='skyblue', range=(0, 30))
    plt.axvline(average_trip_distance, color='red', linestyle='dashed', linewidth=2,
                label=f'Average Trip Distance: {average_trip_distance:.2f}')
    plt.axvline(median_trip_distance, color='green', linestyle='dotted', linewidth=2,
                label=f'Median Trip Distance: {median_trip_distance:.2f}')

    plt.xlabel('Trip Distance')
    plt.ylabel('Frequency')
    plt.title('GREEN Distribution of Trip Distance')
    plt.legend()

    plt.show()

    outliers = df[df['trip_distance'] > 30]
    print("Possible outliers (trip distance > 30):")
    print(outliers['trip_distance'].describe())
    print(outliers[['trip_distance']])


def yellow_vs_green_locations(yellow, green):
    ydo = yellow.groupby('DOLocationID').size().reset_index(name='Frequency').sort_values(by='Frequency',
                                                                                          ascending=False).rename(
        columns={"DOLocationID": "id"})
    ypu = yellow.groupby('PULocationID').size().reset_index(name='Frequency').sort_values(by='Frequency',
                                                                                          ascending=False).rename(
        columns={"PULocationID": "id"})
    ytot = pd.merge(ydo, ypu, on='id', suffixes=('_do', '_pu'))
    ytot['Total_Yellow'] = ytot['Frequency_do'] + ytot['Frequency_pu']

    gdo = green.groupby('DOLocationID').size().reset_index(name='Frequency').sort_values(by='Frequency',
                                                                                         ascending=False).rename(
        columns={"DOLocationID": "id"})

    gpu = green.groupby('PULocationID').size().reset_index(name='Frequency').sort_values(by='Frequency',
                                                                                         ascending=False).rename(
        columns={"PULocationID": "id"})
    gtot = pd.merge(gdo, gpu, on='id', suffixes=('_do', '_pu'))
    gtot['Total_Green'] = gtot['Frequency_do'] + gtot['Frequency_pu']

    plt.figure(figsize=(14, 8))
    plt.scatter(ytot['id'], ytot['Total_Yellow'], color='yellow', alpha=0.6, s=40, label="Yellow Total")
    plt.scatter(gtot['id'], gtot['Total_Green'], color='green', alpha=0.6, s=40, label="Green Total")
    plt.xlabel('Location ID')
    plt.ylabel('Total Frequency')
    plt.title('Total Yellow vs Green Frequency by Location')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()


def distance_price_relationship(df):
    yellow_df = df[df["trip_distance"] < 100]
    yellow_df = yellow_df[yellow_df["total_amount"] < 600]
    yellow_distance = yellow_df["trip_distance"]
    yellow_fare = yellow_df["fare_amount"]

    yellow_total = yellow_df["total_amount"]
    yellow_total_pos = yellow_df[yellow_df["total_amount"] >= 0]["total_amount"]
    yellow_dist_pos = yellow_df[yellow_df["total_amount"] >= 0]["trip_distance"]
    yellow_total_neg = yellow_df[yellow_df["total_amount"] < 0]["total_amount"]
    yellow_dist_neg = yellow_df[yellow_df["total_amount"] < 0]["trip_distance"]

    k1, n1 = np.polyfit(yellow_dist_pos, yellow_total_pos, 1)
    best_fit_line1 = k1 * yellow_dist_pos + n1

    k2, n2 = np.polyfit(yellow_dist_neg, yellow_total_neg, 1)
    best_fit_line2 = k2 * yellow_dist_neg + n2

    # k, n = np.polyfit(yellow_distance, yellow_total, 1)
    # best_fit_line_pos = k * yellow_distance + n

    plt.figure(figsize=(10, 6))
    plt.scatter(yellow_distance, yellow_total, color='skyblue', label="cost")
    plt.plot(yellow_dist_pos, best_fit_line1, color='green', label="prediction positive")
    plt.plot(yellow_dist_neg, best_fit_line2, color='red', label="prediction negative")
    plt.xlim(0, 100)
    plt.ylim(-600, 600)
    plt.xlabel('Trip Distance')
    plt.ylabel('Fare Cost')
    plt.title('Distance vs Fare')
    plt.legend()

    plt.show()


show_popular_dest(yellow_tripdata)
show_distance_frequency(yellow_tripdata)
show_distance_frequency(green_tripdata)
show_green_avgs(green_tripdata)
yellow_vs_green_locations(yellow_tripdata, green_tripdata)
distance_price_relationship(yellow_tripdata)
distance_price_relationship(green_tripdata)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
