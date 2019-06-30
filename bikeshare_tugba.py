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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        try:
            city = input('Enter Chicago, New York City or Washington to analyze bike share: ' ).lower()
            break
        except:
            print("That\'s not a valid input!")
            print("Please, enter Chicago, New York City or Washington: ")


    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Enter a month from January to June: ' ).lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter the desired day of the week: ' ).title()

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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['Start Time'].dt.month.mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']


    # TO DO: display the most common day of week
    popular_day = df['Start Time'].dt.weekday_name.mode()[0]

    # TO DO: display the most common start hour
    from datetime import datetime
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    hours = ['12am', '1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am', '9am', '10am', '11am', '12pm','1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm']
    print('Popular times for your filters: \nMonth: {} \nDay:   {} \nHour:  {}'. format(months[(popular_month-1)], popular_day, hours[popular_hour]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station']+' / '+df['End Station']
    popular_trip = df['Trip'].mode()[0]

    print('Popular stations for your filters:\nStart station: {}\nEnd station:   {}\nTrip:          {}'.format(popular_start_station, popular_end_station, popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    total_hours1 = total_duration // 3600
    rem_after_hours1 = total_duration % 3600
    minutes1 = rem_after_hours1 // 60
    seconds1 = minutes1 % 60

    # TO DO: display mean travel time
    avg_duration = int(df['Trip Duration'].mean())
    total_hours2 = avg_duration // 3600
    rem_after_hours2 = avg_duration % 3600
    minutes2 = rem_after_hours2 // 60
    seconds2 = minutes1 % 60

    print('Total duration:   {} hour(s) {} minute(s) {} second(s)\nAverage duration: {} hour(s) {} minute(s) {} second(s)'.format(total_hours1, minutes1, seconds1, total_hours2, minutes2, seconds2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counts = df['User Type'].value_counts()
    print('Here are user counts for your filters:')
    print(user_counts)

    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('\nAnd gender distributions:')
        print(gender_counts)
    else:
        print('\nYour city database does not have gender distribution info.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print('\nSome details about user birth years...\nThe eldest user was born in {}.\nThe youngest user was born in {}.\nAnd people born in {} rented the bikes the most.'.format(earliest, most_recent, most_common))

    else:
        print('\nYour city database does not have birth year info.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        user_input1 = input('\nWould you like see time statistics for your filters?\nPlease enter yes or no\n').lower()
        if (user_input1 == 'yes'):
            time_stats(df)

        user_input2 = input('\nWould you like see station statistics for your filters?\nPlease enter yes or no\n').lower()
        if (user_input2 == 'yes'):
            station_stats(df)

        user_input3 = input('\nWould you like see trip duration statistics for your filters?\nPlease enter yes or no\n').lower()
        if (user_input3 == 'yes'):
            trip_duration_stats(df)

        user_input4 = input('\nWould you like see some user statistics?\nPlease enter yes or no\n').lower()
        if (user_input4 == 'yes'):
            user_stats(df)

        restart = input('\nWould you like to restart with new filters? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
