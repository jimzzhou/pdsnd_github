import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = (input('Please enter a city name to explore, chicago, new york city or washington\n').lower()).strip()
    while city not in CITY_DATA.keys():
        print('Please enter a valid city name')
        city = (input('Please enter a city name to explore, chicago, new york city or washington\n').lower()).strip()
    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = (input("Please enter the month, in 'january', 'february', 'march', 'april', 'may', 'june', 'all' \n").lower()).strip()
        if month in months:
            break
        else:
            print("Please enter a valid month")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','all']
    while True:
        day = (input('enter a day: "all, sunday, monday, tuesday, wednesday, thursday, friday, saturday" \n').lower()).strip()
        if day in days:
            break
        else:
            print("Please enter a valid day")
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]

    print('Most Day Of Week:', popular_day_of_week)

    # display the most common start hour
    popular_common_start_hour = df['start hour'].mode()[0]

    print('Most Common Start Hour:', popular_common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', popular_common_start_station)

    # display most commonly used end station
    popular_common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', popular_common_end_station)
    # display most frequent combination of start station and end station trip
    df['frequent_trip_route'] = df['Start Station'] + "," + df['End Station']
    print('Most frequent trip route:', df['frequent_trip_route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration. added few words"""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time : ', (df['Trip Duration'].sum()).round())


    # display mean travel time

    print('Average travel time : ', round((df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users. add few changes"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type Stats:')
    print(df['User Type'].value_counts())
    # Display counts of gender
    if 'Gender' not in df.columns:
        print('This state doesn\'t have gener and birth information')
    else:
        print('Gender Stats:')
        print(df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        print('Birth Year Stats:')
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('Most Common Birth Year:',most_common_birth_year)
        most_recent_birth_year = int(df['Birth Year'].max())
        print('Most Recent Birth Year:',most_recent_birth_year)
        earliest_birth_year = int(df['Birth Year'].min())
        print('Earliest Birth Year:',earliest_birth_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    view_data = (input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')).lower()
    start_loc = 0
    end_loc = 5
    while (view_data == 'yes') and (end_loc < len(df.index)):
        print(df.iloc[start_loc:end_loc])
        start_loc += 5
        end_loc +=5
        view_data = input("Do you wish to continue?: yes or no ").lower()
        if view_data != 'yes':
            break
        else:
            continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
