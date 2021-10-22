import pandas as pd
import time

pd.set_option('display.max_columns', 8)

# Reading the CSV files into DataFrames
df_new_york = pd.read_csv('new_york_city.csv')
df_chicago = pd.read_csv('chicago.csv')
df_washington = pd.read_csv('washington.csv')

# Adding a City column to identify each of the 3 cities
df_new_york['City'] = 'New York'
df_chicago['City'] = 'Chicago'
df_washington['City'] = 'Washington'

# Appending the 3 DataFrames
df = df_new_york.append([df_chicago, df_washington], ignore_index=True)

# Converting Start Time Column into Datetime
df['Start Time'] = pd.to_datetime(df['Start Time'])

# Creating Hour, Day & Month Columns Extracted from Start Time
df.insert(2, 'Start Hour', df['Start Time'].dt.hour)
df.insert(3, 'Start Day', df['Start Time'].dt.day_name())
df.insert(4, 'Start Month', df['Start Time'].dt.month_name())

# Creating Trip Course Column
df.insert(9, 'Trip Course', '( ' + df['Start Station'] +
          ' ) ' + ' to ' + ' ( ' + df['End Station'] + ' )')

# DataFrame Filter Function that uses City, Month & Day


def fltr(city, month, day):
    """Filters the DataFrame by City, Month & Day"""

    new_df = df

    if city.title() != 'All':
        new_df = new_df.loc[new_df['City'] == city.title()]
    if month.title() != 'No Filter':
        new_df = new_df.loc[new_df['Start Month'] == month.title()]
    if day.title() != 'No Filter':
        new_df = new_df.loc[new_df['Start Day'] == day.title()]

    return new_df


def month_filter():
    while True:
        print('Which Month Would You Like To View It\'s Statistics ?')
        month = input('January, February, March, April, May, June : ')
        if month.title() not in ['January', 'February', 'March', 'April', 'May', 'June']:
            print(' ')
            print('>>>Please choose one of those months and check your spelling')
            print(' ')
        else:
            break
    return month


def time_stat(new_df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    pop_month = new_df['Start Month'].mode()[0]
    pop_month_count = new_df['Start Month'].value_counts().values[0]

    pop_day = new_df['Start Day'].mode()[0]
    pop_day_count = new_df['Start Day'].value_counts().values[0]

    popular_hr = new_df['Start Hour'].mode()[0]
    popular_hr_count = new_df['Start Hour'].value_counts().values[0]

    if month == 'No Filter':
        print(f"The Most Popular Month to Travel: {pop_month} with a count of {pop_month_count}")
        print(' ')
    else:
        print('You are viewing ' + month.title() + ' data')
        print(' ')
    if day == 'No Filter':
        print(f"The Most Popular Day of Week to Travel: {pop_day} with a count of {pop_day_count}")
        print(' ')
    else:
        print('You are viewing ' + day.title() + ' data')
        print(' ')

    print(f'The Most Popular Hour to Travel: {popular_hr}:00 with a count of {popular_hr_count}')
    print(' ')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stat(new_df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    pop_start_station = new_df['Start Station'].mode()[0]
    pop_start_station_count = new_df['Start Station'].value_counts().values[0]

    pop_end_station = new_df['End Station'].mode()[0]
    pop_end_station_count = new_df['End Station'].value_counts().values[0]

    pop_trip = new_df['Trip Course'].mode()[0]
    pop_trip_count = new_df['Trip Course'].value_counts().values[0]

    print(
        f"The Most Popular Start Station: ({pop_start_station}) with a count of {pop_start_station_count}")
    print(' ')
    print(
        f"The Most Popular End Station: ({pop_end_station}) with a count of {pop_end_station_count}")
    print(' ')
    print(f"The Most Popular Trip: {pop_trip} with a count of {pop_trip_count}")
    print(' ')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(new_df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_sec = round(new_df['Trip Duration'].sum(), 1)
    total_hr = round(total_sec/3600, 1)
    avg_sec = round(new_df['Trip Duration'].mean(), 1)
    avg_hr = round(avg_sec/3600, 1)

    print(f'The Total Travel Time = {total_sec} seconds or {total_hr} hours')
    print(' ')
    print(f'The Average Travel Time = {avg_sec} seconds or {avg_hr} hours')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(new_df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Number of Subscribers: ', new_df['User Type'].value_counts().loc['Subscriber'])
    print('Number of Customers: ', new_df['User Type'].value_counts().loc['Customer'])
    print(' ')

    if city.title() != 'Washington':
        print('Number of Males: ', new_df['Gender'].value_counts().loc['Male'])
        print('Number of Females: ', new_df['Gender'].value_counts().loc['Female'])
        print(' ')

        print('The Earliest Date of Birth: ', new_df['Birth Year'].min())
        print('The Most Recent Date of Birth: ', new_df['Birth Year'].max())
        print('The Most Common Date of Birth: ', new_df['Birth Year'].mode()[0])
    else:
        print('Number of Males: No Available Data')
        print('Number of Females: No Available Data')
        print(' ')

        print('The Earliest Date of Birth: No Available Data')
        print('The Most Recent Date of Birth: No Available Data')
        print('The Most Common Date of Birth: No Available Data')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(new_df):
    """Lets the user view 5 rows of raw data at a time till the user says no"""
    print(' ')
    see = input('Would you like to see the raw data? Enter yes or no.\n')
    n = 0
    new_df = new_df.sort_values(by='Start Time', ascending=False)
    while see.lower() == 'yes':
        print(new_df.iloc[n:(n + 5), [1, 5, 6, 7, 8, 10, 11, 12]])
        n += 5
        print(' ')
        see = input('Would you like to see more raw data? Enter yes or no.\n')


def main():
    while True:
        print('Hello! Lets explore some US Bikeshare data!')
        print(' ')

        while True:
            city = input('Would you like to see the data for New York, Chicago, Washington or All?\n ')
            if city.title() not in ['New York', 'Chicago', 'Washington', 'All']:
                print(' ')
                print('>>>Please choose one of those cities and check your spelling')
                print(' ')
            else:
                break

        month = "No Filter"
        day = "No Filter"
        while True:
            time_filter = input(
                'Should we filter data by month, day, both or not at all? type none for no filter \n ')
            if time_filter.lower() not in ['month', 'day', 'both', 'none']:
                print(' ')
                print('>>>Please choose one criteria from the list and check your spelling')
                print(' ')
            else:
                break

        if time_filter.lower() == 'month':

            month = month_filter()

        if time_filter.lower() == 'day':
            while True:
                print('Which Day Would You Like To View It\'s Statistics ?')
                day = input('Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday : ')
                if day.title() not in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
                    print(' ')
                    print('>>>Please choose one of those days and check your spelling')
                    print(' ')
                else:
                    break
        if time_filter.lower() == 'both':
            month = month_filter()

            while True:
                print('Which Day Would You Like To View It\'s Statistics ?')
                day = input('Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday : ')
                if day.title() not in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
                    print(' ')
                    print('>>>Please choose one of those days and check your spelling')
                    print(' ')
                else:
                    break

        new_df = fltr(city, month, day)

        time_stat(new_df, month, day)
        input('press enter to continue')
        station_stat(new_df)
        input('press enter to continue')
        trip_duration_stats(new_df)
        input('press enter to continue')
        user_stats(new_df, city)
        input('press enter to continue')
        raw_data(new_df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


main()
