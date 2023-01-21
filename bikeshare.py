import pandas as pd

pd.set_option('display.max_columns', 12)

city_data = {"washington": "washington.csv",
             "chicago": "chicago.csv",
             "new york city": "new_york_city.csv"}
months = {1: "January",
          2: "February",
          3: "March",
          4: "April",
          5: "May",
          6: "June"}
weekdays = {0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"}


def city_selector():
    """Asks user to specify a city to be analysed

    Returns:
        (str) city - the name of a city to be analysed, in lower case"""
    city = input("For which city would you like to see data: New York City, Chicago, or Washington? ")
    if city.isalpha() or city.lower() == "new york city":
        if city.lower() in city_data:
            print("You have selected: " + city)
            return city_data[city.lower()]
        else:
            print("You entered: " + city)
            print("This could not be processed. Please ensure you enter only New York City, Chicago, or Washington.")
            return city_selector()
    else:
        print("Your request contained non-alphabetic characters and could not be processed.")
        return city_selector()


def filter_select():
    """Asks user to specify how data will be filtered"""

    selection = input("How would you like to filter the data? By month, day, or not at all? ")
    if selection.lower() == "month":
        print("Filtering by month")
        filt = "month"
        return filt
    elif selection.lower() == "day":
        print("Filtering by day-of-week")
        filt = "day"
        return filt
    elif selection.lower() == "not at all" or selection.lower() == "no":
        print("You have opted for the data to be unfiltered")
        filt = None
        return filt
    else:
        print("You entered:" + selection)
        print("This was not recognised. Defaulting to no filtering.")
        filt = None
        return filt


def datapoint_selector(time):
    """Takes a string (time), set to either "month" or "day", and returns an integer between 0 and 6 based on user
    inputs"""
    if time == "month":
        sel_month = input("Which month? Jan, Feb, Mar, Apr, May, Jun ")
        month_list = ["jan", "feb", "mar", "apr", "may", "jun"]
        if not sel_month.isalpha():
            print("Your choice ({}) contained non-alphabetic characters and could not be processed.".format(sel_month))
            print("Please try again.")
            return datapoint_selector(time)
        if sel_month.lower() in month_list:
            return month_list.index(sel_month.lower()) + 1
        else:
            print("You entered: " + sel_month)
            print("Sorry! That was not an option!")
            print("No filter selected.")
            again = input("Do you want to try again? Y/N")
            if not again.lower() == 'y':
                print("No filter selected.")
                return None
            else:
                return datapoint_selector(time)
    elif time == "day":
        sel_day = input("Which day? M Tu W Th F Sa Su ")
        day_list = ["m", "tu", "w", "th", "f", "sa", "su"]
        if not sel_day.isalpha():
            print("Your choice ({}) contained non-alphabetic characters and could not be processed.".format(sel_day))
            print("Please try again.")
            return datapoint_selector(time)
        if sel_day.lower() in day_list:
            return day_list.index(sel_day.lower())
        else:
            print("You entered: " + sel_day)
            print("Sorry! That was not an option!")
            print("No filter selected.")
            again = input("Do you want to try again? Y/N")
            if not again.lower() == 'y':
                print("No filter selected.")
                return None
            else:
                return datapoint_selector(time)
    else:
        print("There's no point!")


def time_converter(time):
    """Takes a time in seconds, and returns the number of days, hours, minutes, and seconds"""
    time = int(time)
    tot_days = time // 86400
    rem_days = time % 86400
    tot_hours = rem_days // 3600
    rem_hours = rem_days % 3600
    tot_mins = rem_hours // 60
    tot_secs = rem_hours % 60
    time_phrase = (str(tot_days) + " days, " + str(tot_hours) + " hours, " + str(tot_mins) + " minutes "
                   + str(tot_secs) + " seconds!")
    return time_phrase


def stat_explorer(city, filt, point):
    """Takes a csv filename (city) containing bike share data, a string (filt), and an integer between 0 and 6 (point)
    and returns the most popular travel times, locations, as well as total and average trip times and user
    demographics """
    print("Processing request now!")
    df = pd.read_csv(city)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["Month"] = df["Start Time"].dt.month
    df["Day"] = df["Start Time"].dt.weekday
    df["Hour"] = df["Start Time"].dt.hour
    if filt:
        if filt == "month":
            df = df[df["Month"] == point]
        elif filt == "day":
            df = df[df["Day"] == point]

    print("\nPopular travel times:")
    top_month = df["Month"].mode()[0]
    top_day = df["Day"].mode()[0]
    top_hour = df["Hour"].mode()[0]
    if top_hour < 12:
        hour = str(top_hour) + " AM"
    else:
        hour = str(top_hour - 12) + " PM"
    print(" Most popular month: {}".format(months[top_month]))
    print(" Most popular day: {}".format(weekdays[top_day]))
    print(" Most popular hour: {}".format(hour))
    input("Press Enter to continue")

    print("\nPopular stations:")
    top_start = df["Start Station"].mode()[0]
    top_end = df["End Station"].mode()[0]
    df["Trip"] = df["Start Station"] + " - " + df["End Station"]
    top_trip = df["Trip"].mode()[0]
    print(" Most popular starting point: " + top_start)
    print(" Most popular finishing point: " + top_end)
    print(" Most popular trip: " + top_trip)
    input("Press Enter to continue")

    print("\nTravel time:")
    total_travel_time = int(df["Trip Duration"].sum().sum())
    av_travel_time = int(df["Trip Duration"].mean().round())
    print(" Total travel time: " + time_converter(total_travel_time))
    print(" Average trip length: " + time_converter(av_travel_time))
    input("Press Enter to continue")

    print("\nUser demographics:")
    users = df["User Type"].value_counts()
    print(" User types:\n" + str(users))
    if city == "new_york_city.csv" or city == "chicago.csv":
        gender = df["Gender"].value_counts()
        first_dob = int(df["Birth Year"].min())
        last_dob = int(df["Birth Year"].max())
        mode_dob = int(df["Birth Year"].mode())
        print(" User Gender:\n" + str(gender))
        print(" Oldest user birth year:\n" + str(first_dob))
        print(" Youngest user birth year:\n" + str(last_dob))
        print(" Mean user birth year:\n" + str(mode_dob))
    input("Press Enter to continue")


def raw_view(doc):
    """Takes a csv file, opens in a data frame, and allows user to view 5 lines at a time"""
    print("Processing request now!")
    df = pd.read_csv(doc)
    data_shape = df.shape
    print(data_shape)
    cycle = 0
    while cycle + 5 < data_shape[0] - 1:
        print(df[cycle:cycle+5])
        cycle += 5
        cont = input("Continue? Y/N ")
        if not cont.lower() == "y":
            break



def main():
    while True:
        city = city_selector()
        filt = filter_select()
        if filt:
            point = datapoint_selector(filt)
        else:
            point = None
        stat_explorer(city, filt, point)
        view_raw = input("Would you like to view the raw data? Y/N ")
        if view_raw.lower() == "y":
            raw_view(city)
        else:
            print("You have opted not to view the raw data.")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
