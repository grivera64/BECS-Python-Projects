import shelve

# Creates a new todo item
def new_todo(length: int):


    print("\nWhich task would you like to add? (Type \'cancel\' to cancel operation)")
    task = input(str(length + 1) + ". ")

    if (task == "cancel" or task == "Cancel"):

        task = None

    return task

# Gets an element from the to-do list
def get_elem(data: list[str]):

    # Ignore empty lists
    if len(data) < 1:

        print("\nList is empty! Operation cannot be complete!")
        return None
    
    # Repeatedly ask for a valid item on the list
    while(True):
        
        print("\nPlease enter the number/name of the task you want to remove (Type \'cancel\' to cancel operation)")
        
        task = input()

        if "cancel" in task or "Cancel" in task:
            
            return None

        elif task in data:

            return data[data.index(task)]

        # Attempt to get a number if there is no match 
        try:
            task_number = int(task)

            if (task_number < 1 or task_number > len(data)):

                raise ValueError()

        except ValueError:

            print("\nInvalid task/value. Please try again...\n")
            continue

        # Return the element in the list
        return data[task_number - 1]

# Print the entire to-do list
def print_todo(data: list[str]):

    # Newline
    print("")

    # Ignore empty to-do lists
    if len(data) < 1:

        print("To-Do List is empty")
        pass

    # Print the entire to-do list with enumeration on the left of each
    # starting from 1
    for number, item in enumerate(data):

        print(str(number + 1) + ".", item)

    print("")

    pass

# Main function
def main():

    # Open/Create a .dat file with the todo-list inside 
    db = shelve.open("todo.dat")

    # Create and set up a to-do list
    todo: list[str] = []

    try:

        # Attempt to load last data
        todo = db["todo"]
        del db["todo"]

    except KeyError:

        # if no data existed
        db["todo"] = todo

        todo = db["todo"]

        del db["todo"]

    # Start of application    
    print("Welcome to the To-Do List application!\n")

    # Infinite loop until quit
    while True:

        # Show instructions and accept input
        print("[Q]uit / [A]dd / [R]emove / [S]how / [C]lear")
        code = input()

        # check if the code is a valid code
        if (len(code) != 1):

            print("\nInvalid Code! Please try again\n")
            continue

        # Capitalize
        code = code.upper()

        # Quit
        if ("Q" in code):

            print("\nThanks for using our program!")
            break

        # Add new to-do
        elif ("A" in code):

            # Request for new data
            new_data = new_todo(len(todo))

            # Cancel if no new data
            if not new_data:

                print("Process cancelled!\n")
                continue

            # Add new data to to-do
            todo.append(new_data)

            # Print the added data
            print_todo(todo)

        # Remove from to-do
        elif ("R" in code):

            # Find the element to remove via number or title
            removed = get_elem(todo)

            # Cancel if no data to remove
            if not removed:
                
                print("Process cancelled!\n")
                continue


            # Remove from the list
            todo.remove(removed)

            print(f"\nRemoved {removed} from the list!\n")

        # Show to-do
        elif ("S" in code):

            print_todo(todo)

        # Clear to-do
        elif ("C" in code):

            # Ignore if the to-do list is empty
            if len(todo) < 1:

                print("\nTodo is alreay empty!\n")
                continue

            print("Are you sure? [Y/N]")
            confirmation = input()

            if (confirmation != "Y" and confirmation != "y"):

                print("Process cancelled\n")
                continue

            todo.clear()

            print("\nTo-Do List cleared!\n")

        # Invalid code
        else:

            print("\nInvalid code provided. Please try again...\n")

    # Write to file the current todo list for later use
    db["todo"] = todo

    # Close the file
    db.close()

    pass

# Run application
if __name__ == "__main__":

    main()
