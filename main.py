# This program is a restaurant's management system and is used to manage reservations
# The program allows guests to add, delete, edit/update or display current reservation(s)
# The program can also generate a random meal recommendation if guests are looking for a food adventure

from datetime import datetime, timedelta
import random


# Function to ask for a reservation date at least 5 days in advance
def get_date():
    current_date = datetime.now().date()  # Get today's date
    while True:  # Rerun the whole function until user returns a valid date
        print(f"Reservation must be made at least 5 days in advance. The date today is {current_date}.")
        try:
            date_string = input("Please enter the desired reservation date (YYYY-MM-DD): ")

            # Convert input date in string format to date-time format usable for calculation
            reservation_date = datetime.strptime(date_string, "%Y-%m-%d").date()

            # Calculate the date difference and only return reservation_date if at least 5 days in advance
            date_difference = reservation_date - current_date
            if date_difference < timedelta(days=5):
                print("Invalid input! Reservation date is not at least 5 days in advance.\n")
            else:
                return reservation_date

        except ValueError:
            print("Invalid input! Please enter the date using the correct format.\n")


# Function to ask for number of pax with a maximum of 4 pax
def get_pax():
    while True:  # Rerun the whole function until user returns a valid number of pax
        print("Only a maximum of 4 pax are allowed in a group for a single reservation.")
        try:
            pax = int(input("Please enter the number of pax: "))

            # Only return pax if input value is between 1-4
            if pax > 4 or pax < 1:
                raise ValueError
            else:
                return pax

        except ValueError:
            print("Invalid input! Please enter only numbers from 1 to 4.\n")


# Function to check the number of slots taken for each session on the chosen reservation date
def check_slot(date):
    session_1 = session_2 = session_3 = session_4 = 0
    for line in reservations_list:  # Iterate through every reservation in the text file

        # If reservation in text file has the same date as the input date, add number of slots taken
        if str(date) in line:
            if "Session 1" in line:
                session_1 += 1
            elif "Session 2" in line:
                session_2 += 1
            elif "Session 3" in line:
                session_3 += 1
            elif "Session 4" in line:
                session_4 += 1
    return session_1, session_2, session_3, session_4


# Function to ask for desired time session and make sure there is at least an empty slot (1 session 8 slots)
def get_session(date):
    session_1, session_2, session_3, session_4 = check_slot(date)
    while True:  # Rerun the whole function until user returns a valid session
        print("""Only 4 sessions are served each day:
        [1] 12:00 pm - 02:00 pm
        [2] 02:00 pm - 04:00 pm
        [3] 04:00 pm - 06:00 pm
        [4] 06:00 pm - 08:00 pm""")
        try:
            selection = int(input("Please select a time session: "))

            # Checks if there are enough slots for a session
            if (selection == 1 and session_1 < 8) or (selection == 2 and session_2 < 8) or \
                    (selection == 3 and session_3 < 8) or (selection == 4 and session_4 < 8):
                return selection

            elif selection < 1 or selection > 4:
                raise ValueError

            else:
                print("This session is full. Please select another time session.\n")

        except ValueError:
            print("Invalid input! Please enter only numbers from 1 to 4.\n")


# Function to ask for name, phone number and email
def get_info():
    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")
    email = input("Enter your email: ")
    return name, phone, email


# Function to give the reservation a unique ID with the format 'R####' to be easily referred later
def get_id():
    id_list = []

    # Append all existing IDs into a list for checking purposes
    for i in reservations_list:
        id_list.append(i[-6:])
        id_list = [j.replace("\n", "") for j in id_list]

    # Make sure the generated ID does not already exist in the list
    while True:
        random_no = str(random.randint(1, 9999))  # Generate a random number between 1-9999
        unique_id = f"R{random_no.zfill(4)}"  # Add 'R' & fill in zeros if there is space before the random number

        # Only return unique_id if it does not already exist, else loop back and get a new random one
        if unique_id not in id_list:
            return unique_id


# Function to get all necessary details before adding a reservation into the text file
def add_reservation():
    date = get_date()
    print("")
    pax = get_pax()
    print("")
    session = get_session(date)
    print("")
    name, phone, email = get_info()
    unique_id = get_id()
    to_add = f"{name} | {date} | Session {session} | {pax} pax | {phone} | {email} | {unique_id}\n"

    with open("resources/reservation.txt", "a") as file:
        file.write(to_add)

    print(f"The reservation has been booked! Please save the unique ID for future reference: {unique_id}\n")


# Function to ask for unique ID and delete the respective reservation
def cancel_reservation():
    while True:  # Rerun the whole function until user successfully deletes a reservation
        try:
            unique_id = input("Please enter your unique ID: ")
            if len(unique_id) == 5 and unique_id[0] == "R" and unique_id[1:].isdigit:  # unique_id format (R####)
                id_in_list = False
                for line in reservations_list:  # Iterate through every reservation in the text file

                    # Make sure the input ID exists in the reservation list, else show that ID is invalid
                    if unique_id in line:
                        print(f"Reservation details: {line}")
                        id_in_list = True
                        break

                if id_in_list:
                    with open("resources/reservation.txt", "w") as file:
                        for line in reservations_list:  # Iterate through every reservation in the text file

                            # Rewrite the text file for every line except the chosen unique_id
                            if unique_id not in line:
                                file.write(line)
                else:
                    raise ValueError

                print("The selected reservation has been deleted.\n")
                break

            else:
                raise ValueError

        except ValueError:
            print("Invalid input! Please enter a valid ID.\n")


# Function to ask for unique ID or name and edit/update the reservation
def edit_reservation():
    while True:  # Rerun the whole function until user successfully edits a reservation
        target_line = ""  # Variable to store the reservation line to edit based on user input
        has_id = input("Do you have your unique ID? [Y/N]: ").upper()
        if has_id == "Y":
            search_id = input("Please enter your unique ID: ")
            if len(search_id) == 5 and search_id[0] == "R" and search_id[1:].isdigit:
                for line in reservations_list:
                    if search_id in line:
                        target_line = line
            else:  # Asks user to input the correct format for unique ID
                print("Invalid input! Please use the correct format (R####).\n")
                continue

            if target_line == "":  # Checks if reservation exists
                print("Invalid input! ID not found.\n")
                continue

        elif has_id == "N":
            search_name = input("Please enter your name: ")
            for line in reservations_list:
                if search_name in line:
                    target_line = line

            if target_line == "":  # Checks if reservation exists
                print("Invalid input! Name not found.\n")
                continue

        else:
            print("Please enter only 'Y' for Yes or 'N' for No.\n")
            continue

        # Displays the initial reservation
        print(f"Initial reservation details: {target_line}")
        # Breaks the initial reservation down back to separate variables
        name, date, session, pax, phone, email, unique_id = target_line.split(" | ")
        session_text, session = session.split()
        pax, pax_name = pax.split()

        # Rerun until an update is made
        while True:
            print("""What would you like to edit or update from the initial reservation?
    [1] Date & session
    [2] Number of pax
    [3] Guest info""")

            try:
                user_input = int(input("Enter your option: "))
                if user_input == 1:
                    print(f"Original date: {date}")
                    print(f"Original session: Session {session}")
                    date = get_date()
                    session = get_session(date)
                    break

                elif user_input == 2:
                    print(f"Original Pax: {pax} pax")
                    pax = get_pax()
                    break

                elif user_input == 3:
                    print(f"Original name: {name}")
                    print(f"Original phone number: {phone}")
                    print(f"Original email: {email}")
                    name, phone, email = get_info()
                    break

                else:
                    raise ValueError

            except ValueError:
                print("Invalid input! Please enter only numbers from 1-3.\n")
                continue

        to_edit = f"{name} | {date} | Session {session} | {pax} pax | {phone} | {email} | {unique_id}"

        # find the index of the initial reservation in the reservation list
        for i in range(len(reservations_list)):
            if target_line in reservations_list[i]:
                reservations_list[i] = to_edit  # replace the line with new text
                break

        # write everything back to the file
        with open("resources/reservation.txt", "w") as file:
            file.writelines(reservations_list)
        print("Your reservation has been updated!")
        print(f"Updated reservation details: {to_edit}")
        break


# Start of program
run_program = True  # Variable to control loop for whole program (main menu)
while run_program:
    run_selection = True  # Variable to control loop for each section

    print("-" * 49 + "\n" + "Charming Thyme Trattoria Reservation System".center(49) + "\n" + "-" * 49)
    print("What would you like to do today?")
    print("""
    [1] Add Reservation
    [2] Cancel Reservation
    [3] Update/Edit Reservation
    [4] Display Current Reservations
    [5] Generate Meal Recommendation
    [0] Exit
    """)

    try:
        choice = int(input("Enter your option: "))

        # Choice == 1: Calls the add_reservation() function and ask if user wants to add on
        if choice == 1:
            print("-" * 21 + "\n" + "Add Reservation".center(21) + "\n" + "-" * 21)
            while run_selection:
                with open("resources/reservation.txt", "r") as file:
                    reservations_list = file.readlines()
                add_reservation()

                # Ask user to add more reservations or quit sub-menu
                while True:
                    add_more = input("Do you want to add more reservations? [Y/N]: ").upper()
                    if add_more == "Y":
                        print("")
                        break

                    elif add_more == "N":
                        print("Returning to main menu...\n")
                        run_selection = False
                        break

                    else:
                        print("Please enter only 'Y' for Yes or 'N' for No.\n")
                        continue

        # Choice == 2: Calls the cancel_reservation() function and ask if user wants to cancel more
        elif choice == 2:
            print("-" * 24 + "\n" + "Cancel Reservation".center(24) + "\n" + "-" * 24)
            while run_selection:
                with open("resources/reservation.txt", "r") as file:
                    reservations_list = file.readlines()
                cancel_reservation()

                # Ask user to delete more reservations or quit sub-menu
                while True:
                    delete_more = input("Do you want to cancel more reservations? [Y/N]: ").upper()
                    if delete_more == "Y":
                        print("")
                        break

                    elif delete_more == "N":
                        print("Returning to main menu...\n")
                        run_selection = False
                        break

                    else:
                        print("Please enter only 'Y' for Yes or 'N' for No.\n")
                        continue

        # Choice == 3: Calls the edit_reservation() function and ask if user wants to edit more
        elif choice == 3:
            print("-" * 29 + "\n" + "Update/Edit Reservation".center(29) + "\n" + "-" * 29)
            while run_selection:
                with open("resources/reservation.txt", "r") as file:
                    reservations_list = file.readlines()
                edit_reservation()

                # Ask user to edit/update more reservations or quit sub-menu
                while True:
                    edit_more = input("Do you want to edit more reservations? [Y/N]: ").upper()
                    if edit_more == "Y":
                        print("")
                        break

                    elif edit_more == "N":
                        print("Returning to main menu...\n")
                        run_selection = False
                        break

                    else:
                        print("Please enter only 'Y' for Yes or 'N' for No.\n")
                        continue

        # Choice == 4: Display all current reservations from the reservation text file
        elif choice == 4:
            print("-" * 34 + "\n" + "Display Current Reservations".center(34) + "\n" + "-" * 34)
            print("Here are all the current reservations:\n")
            with open("resources/reservation.txt", "r") as file:
                print(file.read())

            while True:
                stop_display = input("Enter Y to exit to main menu: ").upper()
                if stop_display == "Y":
                    print("Returning to main menu...\n")
                    break

                else:
                    continue

        # Choice == 5: Generate a random meal recommendation from the menu list text file
        elif choice == 5:
            recommended = []  # Tracks recommended meals to prevent the same meal getting be recommended twice
            print("-" * 34 + "\n" + "Generate Meal Recommendation".center(34) + "\n" + "-" * 34)
            while run_selection:
                with open("resources/menuItems.txt", "r") as file:
                    meals_list = file.readlines()
                meals_list = [meal.replace("\n", "") for meal in meals_list]
                recommendation = random.choice(meals_list)

                # Only display recommendation if the generated meal has not been recommended yet
                if recommendation not in recommended:
                    recommended.append(recommendation)
                    print(f"Food to recommend: {recommendation}")

                # Return to main menu once all food has been recommended
                elif len(recommended) == len(meals_list):
                    print("No more food to recommend!")
                    print("Returning to main menu...\n")
                    break

                else:
                    continue

                # Ask user to get another recommendation or quit sub-menu
                while True:
                    recommend_more = input("Choose another recommendation? [Y/N]: ").upper()
                    if recommend_more == "Y":
                        print("")
                        break

                    elif recommend_more == "N":
                        print("Returning to main menu...\n")
                        run_selection = False
                        break

                    else:
                        print("Please enter only 'Y' for Yes or 'N' for No.")
                        continue

        # Choice == 0: Exits the program
        elif choice == 0:
            print("Thank you for using Charming Thyme Trattoria Reservation System!")
            run_program = False

        else:
            raise ValueError

    except ValueError:
        print("Invalid input! Please enter only numbers from 0-5.\n")
