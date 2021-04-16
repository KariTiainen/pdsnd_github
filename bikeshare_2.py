import time
import pandas as pd
import numpy as np
import sys


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# Initialyzing global variable for logging the content of an possible output-file, which contains 
# the results of the latest run
log_msg = ''

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    # Dictionary for checking user input
    available_cities = {'c': 'chicago', 'n': 'new york city', 'w': 'washington'}
    city_input , city = 'no valid city selected', ''
    error_msg_city = 'That\'s not a valid input -> just use characters within the parenthesis\n(C)hicago, (N)ew York City or (W)ashington\n'
    
    while True:        

        try:
            city_input = str(input('\nWhich city would you like to analyze? (C)hicago, (N)ew York City or (W)ashington?\n-> \'stop\' for exit\n'))
            if city_input.lower() in available_cities.keys():     #Check if user input is in the available city dictionay
                city = str(available_cities[city_input.lower()])  #set choosen city
                print('selected city: ', city.title())
                break
            elif city_input.lower() == 'stop':     # if user would like to exit the programm           
                sys.exit()               
            else:
                print(error_msg_city)
            
        except:
            if city_input.lower() == 'stop':  
                sys.exit('Cancellation by User')
            else:
                print(error_msg_city)

        

    print('-'*80)        
    
    # get user input for month (all, january, february, ... , june)    
    # Dictionary with available months and the option to choose all (99)
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 99: 'all'}
    error_msg_month = 'That\'s not a valid input -> just use integers corresponding to the month: 1 = January, ..., 6 = June or 99 = all\n'
    while True:
        try:
            month_int = int(input('\nWhich month do you like to analyze? (1) January .... (6) June or (99) for all \n'))            
            #check for valid input
            if month_int in months.keys():
                month = str(months[month_int])
                print('selected month: ', month)
                break
            else:
                print(error_msg_month)

        except:
            print(error_msg_month)       
    
    print('-'*80)    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday', 99: 'all'}
    error_msg_day = 'That\'s not a valid input -> just use integers corresponding to the day of the week: 1 = Monday, ..., 7 = Sunday or 99 = all days\n'
    while True:
        try:
            day_int = int(input('\nWhich day do you like to analyze? 1 = Monday, .... ,7 = Sunday or 99 = for all days of the week\n'))             
            #check for valid weekday
            if day_int in weekdays.keys():
                day = str(weekdays[day_int])
                print('selected day: ', day)
                break
            else:
                print(error_msg_day)
        except:
            print(error_msg_day)       

    log('-'*80)
    log('your filter set up:\n  city:\t\t {}\n  month(s):\t {}\n  weekday(s):\t {}\n'.format(city.title(), month, day))
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
    
    # load data file into a dataframe
    print('\nplease wait while statistics are being generated...\n')
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1    
        # filter by month to create the new dataframe
        df = df[df['month'] == month] 

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    log('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    log('most popular month:\t {}'.format(months[popular_month]))
    
    # display the most common day of week
    #df['day'] = df['Start Time'].dt.day
    popular_day = df['day_of_week'].mode()[0]
    log('most popular day of the week:\t {}'.format(popular_day))
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    #popular_hour = df['hour'].value_counts().index[0]
    popular_hour = df['hour'].mode()[0]    
    log('most popular hour:\t {} o\'clock'.format(popular_hour))    
    
    log("\ntime_stats took %s seconds." % (time.time() - start_time))
    log('-'*80)
    

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    
    log('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts()
    log('most popular start station:\t {} ({})'.format(popular_start_station.index[0], popular_start_station[0]))
    
    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts()
    log('most popular end station:\t {} ({})'.format(popular_end_station.index[0], popular_end_station[0]))

    # display most frequent combination of start- and end-station trip
    # Example found at google search: 
    # https://stackoverflow.com/questions/19384532/get-statistics-for-each-group-such-as-count-mean-etc-using-pandas-groupby
    df_grouped = df.groupby(['Start Station', 'End Station']).size().reset_index(name='counts')
    log('most frequent combination of start- and end-station:\n{}'.format(df_grouped[df_grouped.counts == df_grouped.counts.max()]))       
    
    log("\nstation stats took %s seconds." % (time.time() - start_time))
    log('-'*80)  


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    
    log('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in hours
    total_trip_time = df['Trip Duration'].sum()
    log('total travel time[h]\t\t = {}'.format(round(total_trip_time/3600, 2)))

    # display mean travel time in minutes
    total_trip_time_mean = df['Trip Duration'].mean()
    log('total travel time (average)[min]\t = {}'.format(np.round(total_trip_time_mean/60, 2)))

    log("\ntrip_duration_stats took %s seconds." % (time.time() - start_time))
    log('-'*80)
    


def user_stats(df):
    """Displays statistics on bikeshare users."""

    
    log('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types    
    user_types = df['User Type'].value_counts()
    log('User Types:')    
    for i in range(len(user_types)):
        log('{} {}'.format(user_types.index[i], user_types[i]))        

    log('-'*30)
    
    # Display counts of gender, if available (-> Washingston dataset does not)
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        log('Counts of Gender:')        
        for i in range(len(gender)):
            log('{} {}'.format(gender.index[i], gender[i]))            
    else:
        log('no \'Gender\' data available in this dataset')
        
    log('-'*30)

    # Display earliest, most recent, and most common year of birth, if available
    if 'Birth Year' in df.columns:
        min_birth = int(df['Birth Year'].min())
        log('\n\nminimum birth year:\t\t {}'.format(min_birth))
        
        max_birth = int(df['Birth Year'].max())
        log('maximum birth year:\t\t {}'.format(max_birth))
        
        most_common_birth = int(df['Birth Year'].mode()[0])
        log('most common birth year:\t {}'.format(most_common_birth))
        
    else:
        log('no \'Birth Year\' data available in this dataset')

    log("\nuser_stats took %s seconds." % (time.time() - start_time))
    log('-'*80)
    

def log(msg):
    """Sets display output (print) and appends the log message string (log_msg)
       for a possible file output. 
       \n has to be added at the end of string log_msg, since it is used for a write() which doesn't 
       have a \n at the end of each line automatically
       Arg: (str) msg - Text-Output for displaying on screen and printing in log-file output """
    global log_msg
    output_str = str(msg)
    print(output_str)
    log_msg += output_str + ' \n'



def display_data(df):
    """Displays the selected data. Beginning with the 1st five rows
        and continue to display the next five ones, if the user like to
        Arg: (dataframe) df - filtered data frame """

    i = 0
    #ask for user input, to display the 1st five rows of the given dataset
    raw = str(input("\nWould you like to see the raw input data (5 lines)? Enter 'yes' or 'no'. \n")).lower() 
    pd.set_option('display.max_columns',200)

    #as long as the user gives a valid input
    while True:            
        if raw == 'no': #stop displaying
            break
        elif raw == 'yes': # continue displaying
            print(df[i:i+5]) 
            raw = str(input("\nWould you like to see the next 5 rows of raw input data? Press 'yes' to continue or enter 'no'. \n")).lower() 
            i += 5
        else:   #ask for a valid input
            raw = str(input("\nYour input is invalid. Please enter only 'yes' or 'no'\n")).lower()

            
def write_result(result_filename):
    '''writes an output file, if the user like. Thus a file (with functions input filenme)
       is opend an the global log message text (log_msg) is written into the file. Closing the 
       file afterwards.
       Arg: (str) result_filename - File name for the output file  '''
    
    global log_msg
    
    # write an output file if user would like. Default name is the filter setup (city_month_day.txt)
    write_file = str(input('\nWould you like to a write a Output-file? Enter \'yes\' or \'no\'.\n')).lower()
    
    while True:            
        try:
            if write_file == 'no':
                break
            elif write_file == 'yes':
                log_filename = str(result_filename + '.txt') #time.strftime("%Y.%m.%d %H:%M:%S") + '.txt') 
                f = open(log_filename, 'w')
                f.write(log_msg)
                f.close()   
                break
            else:
                write_file = str(input("\nYour input is invalid. Please enter only 'yes' or 'no'\n")).lower() 
        except:
            # close the open file if already opened
            if 'f' in locals():
                f.close()

              
def main():            

    global log_msg

    while True:
        log_msg = time.strftime("%Y.%m.%d %H:%M:%S") + ' \n'   #initialyzing global log messsage value for each run with the current date/time
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # calculation and displaying time statistics
        time_stats(df)
        # calculation and displaying station statistics
        station_stats(df)
        # calculation and displaying trip statistics
        trip_duration_stats(df)
        # calculation and displaying user statistics
        user_stats(df)        

        try:
            #display data in 5 rows steps, if user would like            
            display_data(df) 
            #ask user to write an output-file, containing the filtered results
            write_result(city.title() + '_' + month + '_' + day)            

            #ask for antoher run
            restart = str(input('\nWould you like to restart? Enter \'yes\' or \'no\'.\n')).lower()
            while restart != 'yes':
                if restart == 'no':                
                    break   
                elif restart != 'yes':
                    restart = str(input('\nThat\'s not a valid input. Just enter \'yes\' or \'no\'.\n')).lower()

            if restart == 'no':
                break                    


        except:
            log('something went wrong')


if __name__ == "__main__":
	main()
