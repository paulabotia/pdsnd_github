# Importing Numpy and Pandas libraries
import numpy
import pandas

# Defining cites
cities = ['Chicago', 'New York', 'Washington']


def get_filters():

    """
    Asks user to specify a city, date filter, and date to analyze (month or day).

    Returns:
        (str) city - name of the city to analyze
        (int) date filter - type of filter to apply: month (1), day (2) or none (3).
        (int) date - month (1 - 6) or day of week (1 - 7) to filter by
    """

    print('\nHello! Let\'s explore some US bikeshare data!')

# Getting the city filter from the user
    valid_city = False
    while not valid_city:
        city = input('\nPlease enter the city you want to filter by: Chicago, New York or Washington\n').title()
        if city in cities:
            valid_city = True
            break
        else:
            print('\nNot a valid city\n')

# Getting the date filter from the user
    valid_date_filter = False
    while not valid_date_filter:
        try:
            date_filter = int(input('\nPlease select the type of filter that you want to apply: Month (1), Day (2), or none (3)\n'))
        except:
            print('\nNot a valid filter\n')
        else:
            if date_filter in range (1,4):
                valid_date_filter = True
                break
# Getting the month filter from the user
    if date_filter == 1:
        valid_month = False
        while not valid_month:
            try:
                date = int(input('\nPlease enter the number of the month you want to filter by from January (1) to June (6)\n'))
            except:
                print('\nNot a valid input\n')
            else:
                if date in range(1,7):
                    valid_month = True
                    break
# Getting the day of week filter from the user
    if date_filter == 2:
        valid_day = False
        while not valid_day:
            try:
                date = int(input('\nPlease enter the day you want to filter by from Monday (1) to Sunday (7)\n'))
            except:
                print('\nNot a valid input\n')
            else:
                if date in range(1, 8):
                    valid_day = True
                    break
# When the user selected no date filter
    if date_filter == 3:
        date = 0

    return city, date_filter, date

def get_file(city_name):

    """
    Loads data for the specified city.

    Args:
        (str) city_name - name of the city to analyze

    Returns:
        df - Pandas DataFrame of the selected city
    """
    if city_name == 'New York':
        file_name = 'new_york_city.csv'
    else:
        file_name = '{}.csv'.format(city_name)

    raw_data = pandas.read_csv('./{}'.format(file_name))

    return raw_data

def display_raw_data():

    """
    Displays 5 rows of raw data for the user, until the user decides that doesn't want to see more raw data

    Returns:
        df - Pandas DataFrame of raw data for the selected city.
    """
# Defining the first rows to show and asking the user
    x = 0
    y = 5
    valid_input = False
    while not valid_input:
        display = input('\nDo you want to see 5 rows of raw data?, Please enter Yes or No\n').title()
        if display == 'Yes' or display == 'No':
            valid_input = True
            break;
        else:
            print('\nPlease enter a valid input\n')
# While loop for displaying 5 more rows.
    while display == 'Yes':
        print(raw_data.iloc[x:y])
        x += 5
        y += 5
        display = input('\nDo you want to see more raw data?. Please enter Yes or No\n').title()
        while display not in ['Yes', 'No']:
            display = input('\nInvalid input. Please enter Yes or No\n').title()

def apply_filters (raw_data, date_filter, date):

    """
    Filters raw data for the specified city by month and day if applicable.

    Args:
        (df) raw_data - Pandas DataFrame of raw data for the selected city.
        (int) date filter - type of filter to apply: month (1), day (2) or none (3).
        (int) date - month (1 - 6) or day of week (1 - 7) to filter by
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# Using pandas to_datetime module to create new columns with month, day of week and hour information with desired format
    raw_data['Start Time'] = pandas.to_datetime(raw_data['Start Time'])
    raw_data['Month'] = raw_data['Start Time'].dt.month
    raw_data['Day of Week'] = raw_data['Start Time'].dt.day_name()
    raw_data['Hour'] = raw_data['Start Time'].dt.hour
    raw_data['Trip'] = raw_data['Start Station'].map(str) + ' > ' + raw_data['End Station'].map(str)

# When date_filter = month, filter dataframe by month
    if date_filter == 1:
        filtered_data = raw_data[raw_data['Month'] == date]

# When date_filter = day of week, filter dataframe by day of week
    if date_filter == 2:
        days_of_week = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
        filtered_data = raw_data[raw_data['Day of Week'] == days_of_week.get(date)]

    if date_filter == 3:
        filtered_data = raw_data

    return filtered_data

def get_statistics (data_base):

    """
    Calculates the following statistics for previously filtered data:
    - Most Frequent Times of Travel
    - Most popular stations and trip
    - Total and average trip duration
    - Bikeshare users

    Args:
        (df) data_base - Pandas DataFrame of raw or filtered data for the selected city.
    """

    print('\nCalculating statistics...\n')

# When filter = month, calculate the following statistics
    if date_filter == 1:
        popular_day = data_base['Day of Week'].mode()[0]
        popular_hour = data_base['Hour'].mode()[0]
        print('Most popular day of travel:\n',popular_day, '\n')
        print('Most popular hour of travel:\n',popular_hour, '\n')

# When filter = day, calculate the following statistics
    if date_filter == 2:
        popular_month = data_base['Month'].mode()[0]
        popular_hour = data_base['Hour'].mode()[0]
        print('Most popular month of travel:\n',popular_month, '\n')
        print('Most popular hour of travel:\n',popular_hour, '\n')

# When filter = none, calculate the following statistics
    if date_filter == 3:
        popular_month = data_base['Month'].mode()[0]
        popular_day = data_base['Day of Week'].mode()[0]
        popular_hour = data_base['Hour'].mode()[0]
        print('Most popular month of travel:\n',popular_month, '\n')
        print('Most popular day of travel:\n',popular_day, '\n')
        print('Most popular hour of travel:\n',popular_hour, '\n')

# For all filters, calculate the following statistics
    popular_start = data_base['Start Station'].mode()[0]
    popular_end = data_base['End Station'].mode()[0]
    popular_trip = data_base['Trip'].mode()[0]
    total_time = data_base['Trip Duration'].sum()
    average_time = data_base['Trip Duration'].mean()
    count_of_user_type = data_base['User Type'].value_counts()

    print('Most popular Start Station:\n', popular_start, '\n')
    print('Most popular End Station:\n', popular_end, '\n')
    print('Most popular Trip:\nStart Station > End Station\n', popular_trip, '\n')
    print('Total travelling time:\n Around', int(total_time/86400), 'days\n')
    print('Average travelling time:\n Around', int(average_time/60),'minutes\n')
    print('Breakdown by user type:\n',count_of_user_type,'\n')

# Additional statistics to calculate when the city chosen is New York or Chicago. Information not available for Washington
    if city == 'New York' or city == 'Chicago':
        earliest_birth = data_base['Birth Year'].min()
        latest_birth = data_base['Birth Year'].max()
        popular_birth = data_base['Birth Year'].mode()[0]
        count_of_gender = data_base['Gender'].value_counts()

        print('Birth year of oldest user:\n', int(earliest_birth),'\n')
        print('Birth year of youngest user:\n', int(latest_birth),'\n')
        print('Most common age of users:\n', int(popular_birth),'\n')
        print('Breakdown by gender:\n',count_of_gender,'\n')



# Running the program
program = True
while program:

# Running each of the functions
    city, date_filter, date = get_filters()
    raw_data = get_file(city)
    display_raw_data()
    filtered_data = apply_filters(raw_data, date_filter, date)
    get_statistics(filtered_data)

# Loop to restart the program
    restart_program = input('\nThat is the main information available.\nDo you want to restart the program? Please enter Yes or No\n').title()
    valid_input = False
    while not valid_input:
        if restart_program == 'Yes':
            valid_input = True
            break
        elif restart_program == 'No':
            valid_input = True
            program = False
            break
        else:
            restart_program = input('Please enter a valid input: Yes or No\n').title()



#testing changes with git 
