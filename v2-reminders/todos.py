import json

# convert task_list to a JSON string with json.dumps(), then write it to todos.json
def update_task_list(task_list):
    updated_task_list_json = json.dumps(task_list)
    # writing
    with open("todos.json", "w") as f:
        f.write(updated_task_list_json)


# reading
# read the contents of todos.json as a string, then convert it back to a Python list with json.loads(), and assign that to task_list
def get_task_list():
    try:
        with open("todos.json", "r") as f:
            task_list = f.read()
        return json.loads(task_list)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# user_question = input("1. Add \n2. List\n3. Quit\n4. Mark done\n Your choice: ")

def get_choice():
    choice = input("1. Add \n2. List\n3. Delete\n4. Mark done\n5. Quit \n Your choice: ")
    return choice

def on_add_task():
    task_title = input("Please add a title.. ")
    task_due_date = input("Please add a due date.. ")
    task_dict = {"title": task_title, "due_date": task_due_date, "done": False}
    task_list = get_task_list()
    task_list.append(task_dict)
    update_task_list(task_list)
    print(f"Added {task_title}")

def list_todos():
    task_list = get_task_list()

    if not task_list:
        print("There is no task added yet, so nothing to display.")
        return
        
    for task in task_list:
        print(f"{task['title']} - due: {task['due_date']} [{'not done' if task['done'] is False else 'done'}]")

def mark_todo_done():
    
    task_list = get_task_list()

    if not task_list:
        print("There is no task added yet, so nothing to maek done.")
        return
    
    # show list of todos
    for i, task in enumerate(task_list):
        print(f"{i+1}: {task['title']}")

    # ask which one they want marked done
    try:
        mark_done_choice = int(input("Which one would you like to mark done? "))
    except ValueError:
        print("Invalid task #")
        return
    
    if mark_done_choice in range(1, len(task_list)+1):
        # change the value of done in dict 
        task_list[mark_done_choice-1]['done'] = True
        update_task_list(task_list)
        print(f"{task_list[mark_done_choice-1]['title']} has been marked done")
    else:
        print("Invalid task #")
        return


#delete a todo
def delete_todo():
    #input - I will ask "what do you want ot delete", then lookup that in the todos.json, if presetn delete and return success message - if nto present - if it is empty - return error message
    task_list = get_task_list()

    if not task_list:
        print("There is no task added yet, so nothing to delete.")
        return
    
    # show list of todos
    for i, task in enumerate(task_list):
        print(f"{i+1}: {task['title']}")

    # ask which one they want to delete
    try:
        delete_task_choice = int(input("Which one would you like to delete? "))
    except ValueError:
        print("Invalid task #")
        return
       
    if delete_task_choice in range(1, len(task_list)+1):
        # remove the task & value in dict 
        deleted_task_title = task_list[delete_task_choice-1]['title']
        del task_list[delete_task_choice-1]
        update_task_list(task_list)
        print(f"{deleted_task_title} has been deleted.")
    else:
        print("Invalid task #")
        return

def run_menu():        
    while True:
        choice = get_choice()
        if choice == "1":
            print(f"You picked : {choice}")
            on_add_task()
        elif choice == "2":
            print(f"You picked : {choice}")
            list_todos()
        elif choice == "3":
            delete_todo()
        elif choice == "4":
            mark_todo_done()
        elif choice == "5":
            break
    
if __name__ == "__main__":
    run_menu()
        


