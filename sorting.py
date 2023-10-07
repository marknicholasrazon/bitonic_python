from colorama import Fore, Style
import os
import time
import pyttsx3
import mysql.connector

num_operations = 0

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def calculate_time_complexity(n, swaps):
    avg_swaps = n * (n.bit_length() - 1)  # O(n * log^2(n))
    best_swaps = n.bit_length() - 1      # O(log^2(n))

    if swaps >= avg_swaps:
        return "Average Case"
    elif swaps >= best_swaps:
        return "Best Case"
    else:
        return "Worst Case"
    
def compare_and_swap(arr, i, j, increasing=True):
    global num_operations
    num_operations += 1

    if (arr[i] > arr[j]) if increasing else (arr[i] < arr[j]):
        arr[i], arr[j] = arr[j], arr[i]

def bitonic_merge(arr, low, cnt, increasing=True):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            compare_and_swap(arr, i, i + k, increasing)
        if increasing:
            print(f"| {Fore.GREEN}Merging increasing subsequence at indices {low} to {low + cnt - 1}{Style.RESET_ALL}{' '*13}|")
            print(f"|{Fore.GREEN}{'-'*62}|{Style.RESET_ALL}")
            time.sleep(1)
        else:
            print(f"| {Fore.RED}Merging decreasing subsequence at indices {low} to {low + cnt - 1}{Style.RESET_ALL}{' '*13}|")
            print(f"|{Fore.RED}{'-'*62}|{Style.RESET_ALL}")
            time.sleep(1)
        bitonic_merge(arr, low, k, increasing)
        bitonic_merge(arr, low + k, k, increasing)

def bitonic_sort(arr, low, cnt, increasing=True):
    if cnt > 1:
        k = cnt // 2
        bitonic_sort(arr, low, k, not increasing)
        bitonic_sort(arr, low + k, k, increasing)
        if increasing:
            print(f"| {Fore.GREEN}Sorting increasing subsequence at indices {low} to {low + cnt - 1}{Style.RESET_ALL}{' '*13}|")
            print(f"|{Fore.GREEN}{'-'*62}|{Style.RESET_ALL}")
            time.sleep(1)
        else:
            print(f"| {Fore.RED}Sorting decreasing subsequence at indices {low} to {low + cnt - 1}{Style.RESET_ALL}{' '*13}|")
            print(f"|{Fore.RED}{'-'*62}|{Style.RESET_ALL}")
            time.sleep(1)
        bitonic_merge(arr, low, cnt, increasing)

def sort_bitonic(arr, increasing=True):
    n = len(arr)
    if n & (n - 1) != 0:
        raise ValueError(f"{Fore.RED}Input size must be a power of 2{Style.RESET_ALL}")
    print(f"|{'-'*62}|")
    print(f"| {Fore.BLUE}Initial Array: {arr}{Style.RESET_ALL}{' '*22}|")
    print(f"|{'-'*62}|")
    start_time = time.time()
    bitonic_sort(arr, 0, n, increasing)
    end_time = time.time()
    running_time = end_time - start_time
    print(f"| {Fore.BLUE}Final Sorted Array: {arr}{Style.RESET_ALL}{' '*17}|")
    print(f"|{'-'*62}|")
    return arr, running_time

def get_user_field_choice():
    valid_fields = ['uniqueId', 'productId', 'product', 'productDescription', 'price', 'category', 'stockQuantity']
    
    while True:
        print("\nAvailable fields for sorting:")
        for index, field in enumerate(valid_fields, 1):
            print(f"{index}. {field}")
        
        try:
            choice = int(input("\nEnter the number corresponding to the field you'd like to sort by: "))
            if 1 <= choice <= len(valid_fields):
                return valid_fields[choice - 1]
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(valid_fields)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Example Usage
try:
    # Text to speech
    introduction = "What is bitonic sort?"
    intro_say = "Bitonic sort is a comparison-based sorting algorithm that can be run in parallel. It focuses on converting a random sequence of numbers into a bitonic sequence, one that monotonically increases, then decreases. Rotations of a bitonic sequence are also bitonic."
    intro_presentation = "\nHere's a visual presentation how bitonic sort works"
    intro_step1 = "Divide the input into two halves and sort each half individually in opposite orders."
    intro_step1_visual1 = "Left half: {0,3,5,8} (Increasing Order)"
    intro_step1_visual2 = "Right half: {7,4,2,1} (Decreasing Order)"
    intro_step1_visual3 = "Combined increasing and decreasing sequence"
    intro_step1_visual4 = f"{Fore.GREEN}[0][3][5][8]{Fore.RED}[7][4][2][1]{Style.RESET_ALL}"
    intro_final_visual1 = "This is the final merge"
    intro_final_visual2 = f"{Fore.GREEN}[0][1][2][3][4][5][7][8]{Style.RESET_ALL}"
    intro_final = "Here's how we implement bitonic sort in our data"
    time_complexity = "The time complexity case of the program is"

    clear_console()

    time.sleep(1)
    
    engine = pyttsx3.init()

    engine.say(introduction)
    print(Fore.YELLOW + introduction + Style.RESET_ALL)
    engine.runAndWait()

    engine.say(intro_say)
    print(intro_say)
    engine.runAndWait()

    engine.say(intro_presentation)
    print(Fore.YELLOW + intro_presentation + Style.RESET_ALL)
    engine.runAndWait()

    engine.say(intro_step1)
    print(intro_step1)
    engine.runAndWait()

    time.sleep(1)
    print("\n")
    print(intro_step1_visual1)
    time.sleep(1)
    print(intro_step1_visual2)

    time.sleep(1)
    engine.say(intro_step1_visual3)
    print("\n")
    print(Fore.YELLOW + intro_step1_visual3 + Style.RESET_ALL)
    engine.runAndWait()

    time.sleep(1)
    print(intro_step1_visual4)

    time.sleep(1)
    engine.say(intro_final_visual1)
    print("\n")
    print(Fore.YELLOW + intro_final_visual1 + Style.RESET_ALL)
    engine.runAndWait()

    time.sleep(1)
    print(intro_final_visual2)

    time.sleep(1)
    engine.say(intro_final)
    print("\n")
    print(Fore.YELLOW + intro_final + Style.RESET_ALL)
    engine.runAndWait()

    user_field = get_user_field_choice()

    # Connect to your MySQL database
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='python'
    )

    # Create a cursor object to interact with the database
    cursor = db_connection.cursor()

    # Fetch data from the database
    cursor.execute(f"SELECT {user_field} FROM product LIMIT 32")
    data_from_database = [row[0] for row in cursor.fetchall()]

    # Close the cursor and the connection
    cursor.close()
    db_connection.close()

    # Use data_from_database as your input data
    input_data = data_from_database

    sorted_data, running_time = sort_bitonic(input_data)

    n = len(input_data)
    avg_swaps = n * (n.bit_length() - 1)
    best_swaps = n.bit_length() - 1

    case = calculate_time_complexity(n, avg_swaps)

    print(f"| Average Case: O(log^2(n)) comparisons, O(n*log^2(n)) swaps{' '*3}|")
    print(f"| Best Case: O(log^2(n)) comparisons, O(n*log^2(n)) swaps{' '*6}|")
    print(f"| Worst Case: O(n^2) comparisons{' '*31}|")
    print(f"| Number of Operations: {num_operations} comparisons{' '*24}|")
    print(f"| Running Time: {running_time} seconds{' '*21}|")
    print(f"| Time Complexity Case: {case}{' '*27}|")
    print(f"|{'-'*62}|")

    time.sleep(1)
    engine.say(time_complexity + case)
    engine.runAndWait()
except ValueError as e:
    print(e)
