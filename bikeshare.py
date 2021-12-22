import pandas as pd
import time

# dictionary for assigning the correct file to the city
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
non_valid_months = ['july', 'august', 'september', 'october', 'november', 'december']

valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


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
    while True:
        try:
            city = input('Select the city you want to filter by: Write Chicago, New York City, Washington or '
                         '"all" if you don\'t want t apply a city filter: ').lower()
            if city in CITY_DATA:
                print('OK. You chose {} to filter by.\n'.format(city.title()))
                break
            else:
                print('That\'s not a correct input. Please try it again.\n')
                continue
        except KeyboardInterrupt:
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Now select the month you want to filter by: January, February, ... , June or write "all" '
                          'if you don\'t want t apply a month filter: ').lower()
            if month in valid_months:
                print('OK. You chose {} to filter by.\n'.format(month.title()))
                break
            elif month in non_valid_months:
                print('Sorry, we only have data from january to june. Please try another month.\n')
                continue
            else:
                print('That\'s not a correct input. Please try it again.\n')
                continue
        except KeyboardInterrupt:
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Last but not least: Select the day you want to filter by: Monday, Tuesday, ... Sunday or '
                        'write "all" if you don\'t want t apply a weekday filter: ').lower()
            if day in valid_days:
                print('OK. You chose {} to filter by.\n'.format(day.title()))
                break
            else:
                print('That\'s not a correct input. Please try it again.\n')
                continue
        except KeyboardInterrupt:
            continue

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # add the start hour that will be needed for other statistic function
    df['Start Hour'] = df['Start Time'].dt.hour
    # add the combination of start station and end station that will be needed for other statistic function
    df['Combination Start-End'] = df['Start Station'] + " - " + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_num = valid_months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month_num]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        day = valid_days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def raw_data(df):
    """Displays 5 lines of raw input if the user want to"""
    decision = input('\nDo you want to see 5 lines of raw data? Type yes or no: ')
    start = 0
    end = 5
    while decision == 'yes':
        print(df[start:end])
        start += 5
        end += 5
        if start > df.shape[0]:
            print('You have seen all the data. Now let\'s start with the statistics\n')
            break
        else:
            decision = input('Do you want to see the next 5 lines of raw data? Type yes or no: ')


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        pop_month = df['Month'].mode()[0]
        pop_month_name = valid_months[pop_month - 1]
        print('The Most Common Month is: ', pop_month_name.title())
    else:
        print('The Most Common Month is: You chose to filter by the month {}, so of course {} is the '
              'Most Common Month :-)'.format(month.title(), month.title()))

    # display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        popular_day_name = valid_days[popular_day - 1]
        print('The Most Common Day is: ', popular_day_name.title())
    else:
        print('The Most Common Day is: You chose to filter by the day {}, so of course {} is the '
              'Most Common Day :-)'.format(day.title(), day.title()))

    # display the most common start hour
    popular_hour = df['Start Hour'].mode()[0]
    print('Most Frequent Start Hour: {} o\'clock'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most commonly Start Station: {}'.format(popular_start.title()))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most commonly End Station: {}'.format(popular_end.title()))

    # display most frequent combination of start station and end station trip
    popular_combi = df['Combination Start-End'].mode()[0]
    print('Most commonly Combination of Start Station and End Station: {}'.format(popular_combi.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    total_duration_hour = int((total_duration / 60) // 60)
    total_duration_min = int((total_duration / 60) % 60)
    total_duration_sec = int((total_duration % 60) % 60)
    print('The total Travel Time (related to your filters) is: {} hours, {} minutes and {} seconds.'
          .format(total_duration_hour, total_duration_min, total_duration_sec))

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    mean_duration_min = int(mean_duration // 60)
    mean_duration_sec = int(mean_duration % 60)
    print('The mean Travel Time is: {} minutes and {} seconds.'.format(mean_duration_min, mean_duration_sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print('Counts of User Types:\n{}'.format(user_counts))

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of Gender:\n{}'.format(gender_counts))
    except KeyError:
        print('\nFor your selected city, there is no information about gender available.')

    # Display earliest, most recent, and most common year of birth
    try:
        youngest_user = int(df['Birth Year'].max())
        print('\nThe youngest user was born in: {}'.format(youngest_user))
        oldest_user = int(df['Birth Year'].min())
        print('The oldest user was born in: {}'.format(oldest_user))
        most_common_year = int(df['Birth Year'].mode())
        print('The most common year of birth is: {}'.format(most_common_year))
    except KeyError:
        print('\nFor your selected city, there is no information about year of birth available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('\nThere are {} trips matching the filter settings.\n'.format(df.shape[0]))
        raw_data(df)
        print('-' * 40)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
    main()
