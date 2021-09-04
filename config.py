script_ran_counter = True # Set to False if you don't want the script to keep track of how many times the script has been ran. This is only in place to show the welcome text to users who are running the script for the first time.
show_insert_info = False # Set to True if you want to see the information that is being inserted into the database when using the iplog.txt file.
confirm_insert = False # Set to True if you want to confirm the information that will be inserted into the database. Note: "show_insert_info" must be set to True for this to work. # DOES NOT WORK AT THIS TIME

ran_counter_file = "script_ran_counter.json" # The name of the file that will be used to saved the number of times the script has been ran. Note: "script_ran_counter" must be set to True for this to work.
iplog_file = "iplog.txt" # The name of the file the script will use to find the IP log file when importing from a IP log .txt file.
new_iplog_file = "new_iplog.txt" # The new name and formatted file of the original IP log that the script will create.
