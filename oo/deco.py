from time import sleep

import time
import functools

def time_it(repeat=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Record the start time
            start_time = time.time()

            # Variable to store the last result
            result = None

            # Execute the function 'repeat' times
            for _ in range(repeat):
                result = func(*args, **kwargs)

            # Record the end time
            end_time = time.time()

            # Calculate and print the execution time
            execution_time = end_time - start_time
            if repeat == 1:
                print(f"Function '{func.__name__}' executed in {execution_time:.6f} seconds")
            else:
                print(f"Function '{func.__name__}' executed {repeat} times in {execution_time:.6f} seconds")
                print(f"Average execution time: {execution_time/repeat:.6f} seconds per call")

            # Return the last result
            return result

        return wrapper

    return decorator

@time_it(repeat=3)
def toto():
    sleep(1)

def main():
    toto()

if __name__ == "__main__":
    main()
