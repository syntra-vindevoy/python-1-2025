def main():
    seconds = 42
    minutes = 42
    hours = 0
    days = 0
    years = 0 #define variables
    print(convert_to_seconds(years, days, hours, minutes, seconds))

def convert_to_seconds(y, d, h, m, s):
    time_in_seconds = s + m * 60 + h * 3600 + d * 24 * 3600 + y * 365 * 24 * 3600 #this is a function that calculates time in seconds
    return time_in_seconds

if __name__ == '__main__':
    main()