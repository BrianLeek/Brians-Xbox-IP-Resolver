from __future__ import print_function
from rich.console import Console
from json import dumps, loads
from shutil import copyfile
from os import path
import requests
import sqlite3
import config
import atexit
import sys
import os

console = Console()

class GetInformationFunctions:
    # Look into the scripts root folder and find any files that end in .db and print the names out.
    def database_files():
        for files in os.listdir(os.path.dirname(os.path.realpath(sys.argv[0]))):
            if files.endswith(".db"):
                print(f" - {files}")

    # List the results of the gamertag the user enters.
    def search_results():
        rows = cursor.execute("SELECT id, gamertag, ip, xuid, mid FROM userinfo WHERE gamertag = ?", (gamertag_search_input,),)
        for row in cursor:
            print(f"\nID: {row[0]}\nGamertag: {row[1]}\nIP Address: {row[2]}\nXUID: {row[3]}\nMachine ID: {row[4]}\n")

    # List all the records of the selected database.
    def search_results_all():
        cursor.execute("SELECT id, gamertag, ip, xuid, mid FROM userinfo")
        for row in cursor.fetchall():
            print(f"\nID: {row[0]}\nGamertag: {row[1]}\nIP Address: {row[2]}\nXUID: {row[3]}\nMachine ID: {row[4]}")

    # Read the scripts file that contains the number of times the script has been ran.
    def script_ran_counter_read():
        return loads(open(f"{config.ran_counter_file}", "r").read()) + 1 if path.exists(f"{config.ran_counter_file}") else 0

    # Write the new number to the counter file when the script is ran.
    def script_ran_counter_write():
        with open(f"{config.ran_counter_file}", "w") as f:
            f.write(dumps(counter))

class DatabaseFunctions:
    def connect():
        global database_name, connection, cursor

        database_name = input("Database Name (without .db): ") # Ask the user to input what database they want to use.
        print("")

        # Check if the database the user inputted in "database_name" is valid if not tell the user that and ask for another input.
        valid_database_input = False
        while valid_database_input == False:
            if os.path.exists(f"{database_name}.db"):
                connection = sqlite3.connect(f"{database_name}.db")
                cursor = connection.cursor()
                valid_database_input = True
            else:
                print("Couldn't find the database to connect to. Please try again.")
                database_name = input("Database Name (without .db): ")

    def merage_database():
        global db_two_cursor

        database_two = input(f"Which database would you like to merge into {database_name}.db (without .db): ")

        if database_name == database_two:
            print("\nERROR: You can not merge the same databases together. Please try again using to different databases.")
            sys.exit()

        db_two = sqlite3.connect(f"{database_two}.db")

        try:
            # Get the contents of a table
            db_two_cursor = db_two.cursor()
            db_two_cursor.execute('SELECT * FROM userinfo')
            output = db_two_cursor.fetchall()

            # Insert those contents into another table.
            db_cursor = connection.cursor()
            for row in output:
                db_cursor.execute("INSERT OR IGNORE INTO userinfo VALUES (?, ?, ?, ?, ?)", row)

            print(f"Successfully merged {database_two}.db into {database_name}.db.")
        except:
            print("Something went wrong.")
            sys.exit()

    def edit_database_multiple_row(id, gamertag, ip, xuid, mid):
        sqlite_update_query = """UPDATE userinfo set gamertag = ?, ip = ?, xuid = ?, mid = ? where id = ?"""
        columnValues = (gamertag, ip, xuid, mid, id)

        cursor.execute(sqlite_update_query, columnValues)

        print("Multiple columns updated successfully")

    def edit_database_singal_row(id, row):
        sqlite_update_query = """UPDATE userinfo set row = ? where id = ?"""
        columnValues = (row)

        cursor.execute(sqlite_update_query, columnValues)

        print("Singal columns updated successfully")

    # Commit any changes to the database when called.
    def commit():
        connection.commit()

    # Close the connection to the database when called.
    def close():
        connection.close()

    # Close the connection to the database when called.
    def close_2():
        db_two_cursor.close()

class SearchFunctions:
    # Ask the user for the gamertag that they want to find the IP of.
    def search_input():
        global gamertag_search_input

        gamertag_search_input = input("Gamertag (case sensitive): ")

class InputFromIPLog:
    def iplog_file_from_question():
        global iplog_file_from

        print("Which program is the ip log file from?\n - ApparitionNET Studios")
        iplog_file_from = input("Program: ")

    # Open the "iplog.txt" file that is dragged into the scripts folder by the user. The script will then reformat the file to be used laer when adding that information to a database.
    # Note: the "iplog.txt" file is generated by a program called ApparitionNET.
    def format_ip_log_apparitionnet():
        print(f"Opening {config.iplog_file} to read and create the new formatted file.")

        with open(config.iplog_file, "r+") as f:
            print(f"Creating the new formatted file named {config.new_iplog_file}.")
            with open(f"{config.new_iplog_file}", "w") as f2:
                for line in f:
                    currentline = line.split(",")
                    new_format = f"Gamertag: {currentline[0]}\nIP Address: {currentline[1]}\nXUID: {currentline[2]}\nMID: {currentline[3]}\n"
                    f2.write(new_format)
                print("Successfully created the new formatted file.")

    def get_value(self, item):
        info = item.strip().split(':')
        val = info[1].strip().split(',')
        return val[0].strip()

    def insert_data_apparitionnet(self):
        global gamertag, ip_address, xuid, mid

        with open(f"new_{config.iplog_file}", "r") as f:
            file_data = f.readlines()

        list_userinfo = []
        gamertags = ""
        ip_addresses = ""
        xuids = ""
        mids = ""

        print(f"Adding the items from {config.new_iplog_file} to a list.")

        for item in file_data:
            if "Gamertag" in item:
                gamertags = self.get_value(item)
                list_userinfo.append(gamertags)
            elif "IP Address" in item:
                ip_addresses = self.get_value(item)
                list_userinfo.append(ip_addresses)
            elif 'XUID' in item:
                xuids = self.get_value(item)
                list_userinfo.append(xuids)
            elif 'MID' in item:
                mids = self.get_value(item)
                list_userinfo.append(mids)

        print(f"Inserting the information from that list to {database_name}.db.")

        if config.show_insert_info == True:
            print("Information being inserted into the database:\n")

        # +4 will be added to the numbers to select things like gamertags and IPs from the list.
        gamertags = 0
        ip_addresses = 1
        xuids = 2
        mids = 3

        try:
            # I need to find away to use the same for loop multiple times but add to it each time it's called. Couldn't get a function to work to do it.
            for items in list_userinfo:
                gamertag = str(list_userinfo[gamertags])
                ip_address = str(list_userinfo[ip_addresses])
                xuid = str(list_userinfo[xuids])
                mid = str(list_userinfo[mids])

                if config.show_insert_info == True:
                    print(f"Gamertag: {gamertag}\nIP Address: {ip_address}\nXUID: {xuid}\nMachine ID: {mid}\n")

                cursor.execute("INSERT INTO userinfo (gamertag, ip, xuid, mid) values(?, ?, ?, ?)", (gamertag, ip_address, xuid, mid,))

                gamertags = gamertags + 4
                ip_addresses = ip_addresses + 4
                xuids = xuids + 4
                mids = mids + 4

            # Does not work it's supposed to show the user the information being inserted then after if that wants the displayed information to be inserted into the database.
            # Note: not supposed to be for individual items.
            if config.confirm_insert == True and config.show_insert_info == True:
                for items in list_userinfo:
                    gamertag = str(list_userinfo[gamertags])
                    ip_address = str(list_userinfo[ip_addresses])
                    xuid = str(list_userinfo[xuids])
                    mid = str(list_userinfo[mids])

                    print(f"Gamertag: {gamertag}\nIP Address: {ip_address}\nXUID: {xuid}\nMachine ID: {mid}\n")

                    confirm = input("Would you like to insert the information above into a database? (y/n): ")
                    if confirm == "y":
                        for items in list_userinfo:
                            cursor.execute("INSERT INTO userinfo (gamertag, ip, xuid, mid) values(?, ?, ?, ?)", (gamertag, ip_address, xuid, mid,))
                    else:
                        sys.exit()

                    gamertags = gamertags + 4
                    ip_addresses = ip_addresses + 4
                    xuids = xuids + 4
                    mids = mids + 4
            else:
                for items in list_userinfo:
                    gamertag = str(list_userinfo[gamertags])
                    ip_address = str(list_userinfo[ip_addresses])
                    xuid = str(list_userinfo[xuids])
                    mid = str(list_userinfo[mids])

                    cursor.execute("INSERT INTO userinfo (gamertag, ip, xuid, mid) values(?, ?, ?, ?)", (gamertag, ip_address, xuid, mid,))

                gamertags = gamertags + 4
                ip_addresses = ip_addresses + 4
                xuids = xuids + 4
                mids = mids + 4
        except IndexError:
            pass

        print("Successfully inserted information into database.")

        view_database = input("\nWould you lie to view the database? (y/n): ")
        if view_database == "y":
            GetInformationFunctions.search_results_all()
        else:
            pass

if config.script_ran_counter == True:
    counter = GetInformationFunctions.script_ran_counter_read()
    atexit.register(GetInformationFunctions.script_ran_counter_write)

    if counter < 1:
        console.print("Xbox IP Resolver by Brian Leek", style="underline bold", justify="center")
        print("""Brian's Xbox IP Resolver (Gamertag2IP) is a script created in Python that will come with a preexisting database so you won't need to create one and add information to it. The main database will receive updates every so often. Since the main database already has information in it you can begin searching right away. You can search for a Xbox users IP Address, XUID, and Machine ID (MID) with just their gamertag from the main database if available. The script also allows users to create their own databases too! You can contribute to the main overall database by submitting your database to the developer to be merged together or they can share their database online for others online to use.

    The main database is created on the developers side which works by using the IP log (iplog.txt) file generated by ApparitionNET when logging IPs, other ways to import from a ip log file are planned. Once the file is created it is dropped into the scripts root and the script uses that to create or add that information to a new/existing database. Data can also be entered manually as well if needed.
    """)
    else:
        pass
else:
    pass

options = input("1. Search Database\n2. Create Database\n3. Insert Into Database\n4. Edit Database\n5. View Database\n6. Merge Two Databases\n7. Delete Database\n\nPlease pick a option above by entering the number: ")

valid_input = False
while valid_input == False:
    # Search database. List the found databases then connect to the one the user selects. Then ask the user to input the gamertag they want to lookup and then show the results if any.
    if options == "1" or options == "search":
        GetInformationFunctions.database_files()
        DatabaseFunctions.connect()

        print(f"Searching Database: {database_name}.db\n")

        SearchFunctions.search_input()
        GetInformationFunctions.search_results()

        while not SearchFunctions.search_input() == "":
            SearchFunctions.search_input()
            GetInformationFunctions.search_results()

        DatabaseFunctions.close()

        valid_input = True
    # Create database. Ask the user what they want to name the new database then commit the changes to create the database file.
    # Note: the created database will be empty you can insert information manually or with a iplog.txt file generated by a tool called ApparitionNET.
    elif options == "2" or options == "create":
        database_name = input("Database Name (without .db): ")

        connection = sqlite3.connect(f"{database_name}.db")
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS userinfo (id INTEGER PRIMARY KEY AUTOINCREMENT, gamertag text NOT NULL, ip text NOT NULL, xuid text NOT NULL, mid text NOT NULL)")

        DatabaseFunctions.commit()
        DatabaseFunctions.close()

        print("Successfully created the database.")

        valid_input = True
    # Insert into database. List the found databases then connect to the one the user selects. Then ask the user how they want to insert data and commit the data to the database.
    elif options == "3" or options == "insert":
        # Input data manually or with the iplog.txt file.
        data_input = input("Insert data manually or with the iplog.txt file (manually/iplog): ")

        valid_input = False
        while valid_input == False:
            if data_input == "manually" or data_input == "m":
                GetInformationFunctions.database_files()
                DatabaseFunctions.connect()

                # Ask the user for the information to input to the database. The XUID and MID inputs can be left blank.
                input_gamertag = input("Gamertag: ")
                while input_gamertag == "":
                    input_gamertag = input("Gamertag: ")
                    print("Please enter a value for the gamertag input.")
                input_ip = input("IP Address: ")
                while input_ip == "":
                    input_ip = input("IP Address: ")
                    print("Please enter a value for the IP address input.")
                input_xuid = input("XUID: ")
                input_mid = input("Machine ID: ")

                cursor.execute("INSERT INTO userinfo(gamertag, ip, xuid, mid) VALUES (?,?,?,?)", (input_gamertag, input_ip, input_xuid, input_mid))

                DatabaseFunctions.commit()

                print(f"\nSuccessfully added information to {database_name}.db.")

                view_database = input("\nWould you like to view the database? (y/n): ")
                if view_database == "y":
                    GetInformationFunctions.search_results_all()
                else:
                    pass

                DatabaseFunctions.close()

                valid_input = True
            elif data_input == "ip" or data_input == "iplog":
                if os.path.isfile(config.iplog_file):
                    inputfromiplog = InputFromIPLog()
                    GetInformationFunctions.database_files()
                    DatabaseFunctions.connect()

                    InputFromIPLog.iplog_file_from_question()
                    if iplog_file_from == "app" or iplog_file_from == "ApparitionNET" or iplog_file_from == "ApparitionNET Studios":
                        try:
                            InputFromIPLog.format_ip_log_apparitionnet()
                            inputfromiplog.insert_data_apparitionnet()
                        except IndexError:
                            print("IndexError: Looks like the script was unable to format and recrete the ip log file for you. This may be because you are not using the right ip log file for ApparitionNET Studios. Please be sure you are using the file that is generated when logging IPs with the ApparitionNET Studios tool and try again.")
                            sys.exit()

                    DatabaseFunctions.commit()
                    DatabaseFunctions.close()
                else:
                    print(f"Couldn't find the {config.iplog_file} file. Please be sure you have the file added in the scripts folder being continuing.")

                valid_input = True
            else:
                print("\nPlease pick a valid option and try again.")
                data_input = input("Insert data manually or with the iplog.txt file (manually/iplog): ")

        valid_input = True
    # Update database. NOT WORKING / WIP
    elif options == "4" or options == "update":
        GetInformationFunctions.database_files()
        DatabaseFunctions.connect()

        option = input("Would you like to update multiple columns at the same time? (y/n): ")
        if option == "y":
            id = input("Please enter the ID of the row you would like to update: ")
            while id == "":
                id = input("Please enter the ID of the row you would like to update: ")
            new_gamertag = input("New Gamertag: ")
            while new_gamertag == "":
                new_gamertag = input("New Gamertag: ")
            new_ip = input("New IP Address: ")
            while new_ip == "":
                new_ip = input("New IP Address: ")
            new_xuid = input("New XUID: ")
            while new_xuid == "":
                new_xuid = input("New XUID: ")
            new_mid = input("New Machine ID: ")
            while new_mid == "":
                new_mid = input("New Machine ID: ")

            DatabaseFunctions.edit_database_multiple_row(id, new_gamertag, new_ip, new_xuid, new_mid)
        else: # this part for editing databases are still in development and should'nt be used.
            print("ERROR: You can not update a single column from a database entry at this time.")
            sys.exit()

            id = input("Please enter the ID of the row you would like to update: ")
            while id == "":
                id = input("Please enter the ID of the row you would like to update: ")
            row = input("Please enter the field you would like to update (gamertag, ip, xuid, mid): ")

            if row == "gamertag":
                new_gamertag = input("New Gamertag: ")
            if row == "ip":
                #new_gamertag = None
                new_ip = input("New IP Address: ")
                # new_xuid = None
                # new_mid = None
            if row == "xuid":
                #new_gamertag = None
                #new_ip = None
                new_xuid = input("New XUID: ")
                # new_mid = None
            if row == "xuid":
                #new_gamertag = None
                #new_ip = None
                #new_xuid = None
                new_mid = input("New Machine ID: ")


            DatabaseFunctions.edit_database_singal_row(id, new_gamertag, new_ip, new_xuid, new_mid)

        DatabaseFunctions.commit()

        print("\nSuccessfully edited the database record.")

        DatabaseFunctions.close()

        valid_input = True
    # View records. List the found databases then connect to the one the user selects and show all records for that database.
    elif options == "5" or options == "view":
        GetInformationFunctions.database_files()
        DatabaseFunctions.connect()

        GetInformationFunctions.search_results_all()

        DatabaseFunctions.close()

        valid_input = True
    # Merge two databases. Connect to the first database that the user wants to merage to then call the merage database function which then asks the user to select another database to merage from then merages them together, commits and closes both databases.
    elif options == "6" or options == "merge":
        print("\nPlease pick a database you would like to merage to from the list below.")

        GetInformationFunctions.database_files()
        DatabaseFunctions.connect()

        DatabaseFunctions.merage_database()

        DatabaseFunctions.commit()
        DatabaseFunctions.close()
        DatabaseFunctions.close_2()

        valid_input = True

    # Delete database. Ask the user the database they want to delete then delete it.
    elif options == "7" or options == "delete":
        print("\nPlease pick the database you would like to delete. This can't be undone!")

        GetInformationFunctions.database_files()
        database_name = input("Database Name (without .db): ") # Ask the user to input what database they want to use.

        # Check if the database the user inputted in "database_name" is valid if not tell the user that and ask for another input.
        valid_database_input = False
        while valid_database_input == False:
            if os.path.exists(f"{database_name}.db"):
                confirm = input(f"Are you sure you want to delete {database_name}.db? This can not be undone! (y/n): ")
                if confirm == "y":
                    os.remove(f"{database_name}.db")
                    print("Successfully deleted the database.")
                else:
                    pass
                valid_database_input = True
            else:
                print("\nCouldn't find the database. Please try again.")
                database_name = input("Database Name (without .db): ")

        valid_input = True
    else:
        print("\nPlease pick a valid option and try again.")
        options = input("Please pick a option above by entering the number: ")
