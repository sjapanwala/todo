import json
import sys
import os

FILE_DATA = ".tasks.json"
actions_allowed = ['-at','-rt','-tt','-cp','-tldr','-h','-sb','--wipetasks','--init']

def help_sec():
    print("""
    Usage: td [ACTIONS] [input1] [input2] [input3] [input4]

    ACTIONS,
    -h,         -> help section
    -tldr       -> tldr of a command
    -at,        -> adds tasks, requires [input1:task name] [input2:state]
    -rt,        -> removes a task, requires [input1:tasknum or taskname]
    -tt,        -> toggles a task status, requires [input1: tasknum or taskname]
    -cp,        -> changes the progress of a task, requires...
    -sb,        -> sorts the tasks by a selected attribute, requires [input1:an attribute]
    --init      -> initialize the tasks database for the current dir
    --wipetasks -> removes all tasks in database, will ask for confirmation
          """)
def tldr(action_name):
    if action_name not in actions_allowed:
        print(f"\033[31merror: \033[0m'{action_name}' is not a recognized command.")
        help_sec()
        exit()
    elif action_name in actions_allowed:
        if action_name == "-tldr":
            print(f"""
            TLDR for {action_name}

            -tldr is the command provided to view the function of a command in a simpler way.
            this command is mainly used for formatting help to help with the usage of other commands
                  """)
            exit()
        elif action_name == '-at':
            print(f"""
            TLDR for {action_name}

            -at is the command used to add tasks, requiring 3 arguements, and one optional.
            the 3 arguements consist of, 'Taskname', 'Task Priority', 'Task State'.
            with 1 optional arguement which is ComLink, can consist of either a comment, or an external link.

            How To Use

            $: td -at "taskname" priority˟ state˟ comlink
            NOTE: priority and state need to be from the following tagse

            Priority: High, Medium, Low, None
            State:    Pending, Working, Completed

            Example,

            $: td -at "Fix Bug #7" medium pending "see info in appname/info.txt"
            
            Output:
                >> \033[92mSuccessfully Added Task!\033[0m
                >> TaskName: Fix Bug #7
                >> Status: Pending
                >> Priority: Medium

            If error has occured, you will be notified and how to fix it.
                  """)
        else:
            print('No TLDR Entry\n🚂 - - - - - - 💨')

def get_file_id(filename):
    """
    This method checks if the file needed exists in the current directory. If the file does not exist,
    returns False; if it does, it returns True.
    
    in:
        filename (str) -> where the tasks are stored
    out:
        bool -> returns the state of the file
    """
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    just_dirname = current_dir.rfind("/")
    just_dirname = current_dir[just_dirname+1:]
    
    if os.path.isfile(file_path):
        return True
    else:
        #print(f"\033[35mNo Tasks Have Been Created For '\033[95m{just_dirname}\033[35m'\033[37m.\nAdd Tasks With '-at' or try '-h'\033[0m")
        return False
    
def init_db(filename):
    """
    Check if the file exists. If not, create the file and add the initial structure.
    """
    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            json.dump({"tasks": []}, file, indent=4)
        print('Database Has Been Initialized!')
    else:
        print("DataBase Already Exists")

def wipe_all_tasks(filename):
    current_dir = os.getcwd()
    id = highest_id(filename)
    print('\033[91mPLEASE READ THIS CAREFULLY!\033[97m')
    print(f'You are attempting to wipe all tasks in \033[91m{current_dir}\033[97m')
    print(f"You will be erasing \033[91m{id}\033[97m Task's\n")
    confirm = str(input('Please Type The Current Directories Full Path To Continue \n\033[0m(entering anything else will cancel this process)\n> \033[91m'))
    if confirm == current_dir:
        print(f'\033[92m{id} Tasks Were Erased\033[0m')
        with open(filename, 'w') as file:
            json.dump({"tasks": []}, file, indent=4)
        exit()
    else:
        print('\033[92mNo Tasks Were Erased\033[0m')
        exit()


def highest_id(filename):
    highest = 0
    with open(filename, 'r') as db:
        content =  json.load(db)
        inter_tasks = content.get('tasks', [])
        for tasks in inter_tasks:
            id_num = tasks['id']
            if id_num > highest:
                highest = id_num
        return highest

def add_tasks(filename, taskname, priority, status, linkfile):
    # Get highest id
    id = highest_id(filename)

    # Format the capitalization for the taskname for aesthetics
    taskname_inter = taskname.split()
    
    # Capitalize the first letter of each word
    if len(taskname_inter) == 1:
        taskname = taskname.capitalize()
    else:
        taskname = " ".join([item.capitalize() for item in taskname_inter])

    # Check priority tags
    priority_tags = ['High', 'Medium', 'Low', 'None']
    if priority.capitalize() not in priority_tags:
        print(f"\033[31mERR!\033[0m: '{priority}' does not exist in the priority tags, Please Review TLDR Section")
        return False

    # Check status tags
    status_tags = ['Pending', 'Working', 'Completed']
    if status.capitalize() not in status_tags:
        print(f"\033[31mERR!\033[0m: '{status}' does not exist in the status tags, Please Review TLDR Section")
        return False

    # Handle linked files
    if linkfile == "":
        linkfile = None

    # Define the new task
    new_task = {
        "id": id + 1,
        "taskname": taskname,
        "priority": priority.capitalize(),
        "status": status.capitalize(),
        "filelink": linkfile
    }

    # Read existing tasks from the file
    with open(filename, 'r') as file:
        content = json.load(file)
        tasks = content.get('tasks', [])

    # Append the new task to the existing list of tasks
    tasks.append(new_task)

    # Write the updated list of tasks back to the file
    with open(filename, 'w') as file:
        json.dump({"tasks": tasks}, file, indent=4)
        print(f"\033[92mSuccessfully Added Task!\033[0m     \nTaskName: \033[97m{new_task['taskname']}      \n\033[0mStatus: \033[97m{new_task['status']}       \n\033[0mPriority: \033[97m{new_task['priority']}")

def color_attr(attribute):
    """
    colours an attribute based on its status / priority
    """
    status_tags = ['Pending', 'Working', 'Completed']
    priority_tags = ['High', 'Medium', 'Low', 'None']
    if attribute in status_tags:
        # means its a status attribute
        if attribute == 'Pending':
            return '\033[33mPending'
        elif attribute == 'Working':
            return '\033[34mWorking'
        elif attribute == 'Completed':
            return '\033[32mCompleted'
    elif attribute in priority_tags:
        # means it a priority attribute
        if attribute == 'High':
            return '\033[91mHigh'
        elif attribute == 'Medium':
            return '\033[93mMedium'
        elif attribute == 'Low':
            return '\033[94mLow'
        elif attribute == 'None':
            return '\033[90mNone'

def build_tasks(filename):
    """
    listing tasks without formatting it
    """
    formatted_tasks = []
    with open (filename,'r') as tasks_db:
        content =  json.load(tasks_db)
        task_list = content.get('tasks', [])
        if not task_list:
            print('You Shouldnt Even Be Here... How did You Bypass The Errors')
            exit()
        task_len = 0 # so spacing can be evenly made
        priority_len = 0 #for spacing
        status_len = 0 # for spacing
        id_space = 0
        for tasks in task_list:
            if len(tasks['taskname']) > task_len:
                task_len = len(tasks['taskname'])
            if len(tasks['priority']) > priority_len:
                priority_len = len(tasks['priority'])
            if len(tasks['status']) > status_len:
                status_len = len(tasks['status'])

            
        # calculate the spacing between everything
        # spacing for tasks and priority
        spacing_const_task = task_len + 5
        spacing_const_prio = priority_len + 5
        spacing_const_stat = status_len + 3
        low = []
        med = []
        high = []
        total = 0
        for tasks in task_list:
            total +=1
            priority = color_attr(tasks['priority'])
            status = color_attr(tasks['status'])
            task_space = spacing_const_task - len(tasks['taskname'])
            prio_space = spacing_const_prio - len(tasks['priority'])
            stat_space = spacing_const_stat - len(tasks['status'])
            if tasks['filelink'] == None:
                filelink = f'\033[36mNo Links'
            else:
                filelink = f'\033[36m{tasks['filelink']}'
            if len(str(tasks['id'])) == 1:
                id_space = 4
            else:
                id_space = 3
            #if tasks['status'] == 'Completed':
            #    result = f'\033[9m\033[31m{tasks['id']}{id_space * " "}\033[97m{tasks['taskname']}{task_space * " "}{priority}{prio_space * " "}{status}{stat_space * " "}{filelink}\033[0m'
            #else:
            result = f'\033[31m{tasks['id']}{id_space * " "}\033[97m{tasks['taskname']}{task_space * " "}{priority}{prio_space * " "}{status}{stat_space * " "}{filelink}\033[0m'
            if tasks['priority'] == 'High':
                high.append(result)
            elif tasks['priority'] == 'Medium':
                med.append(result)
            elif tasks['priority'] == 'Low':
                low.append(result) 
        formation = high + med + low
        print(f'total: {total}')
        print(f'\033[4mID\033[0m{(id_space-1) * " "}\033[4mTask Name\033[0m{(task_len-4 ) * " "}\033[4mPriority\033[0m{(priority_len-3) * " "}\033[4mStatus\033[0m{(status_len-3) * " "}\033[4mComLinks\033[0m')
        for lines in formation:
            print(lines)
        return formation

def main():
    if len(sys.argv) < 2:
        """
        for displaying defaults
        """
        if get_file_id(FILE_DATA) == False:
            print(f"\033[31mERR!\033[0m: Database Has Not Been Initialized, Please Type 'td --init' to Continue")
            exit()
        build_tasks(FILE_DATA)
    elif sys.argv[1] not in actions_allowed:
        """
        When a command is not recognized
        """
        print(f"\033[31mERR!\033[0m: '{sys.argv[1]}' Is Not Recognized As A Command, Refer to '-h' For Help")
        #help_sec()
        exit()
    elif sys.argv[1] == '-tldr':
        """
        THIS IS FOR TLDR SECTIONS
        """
        if len(sys.argv) < 3:
            print(f"\033[31mERR!\033[0m: [INPUT1] Not Given")
            exit()
        elif sys.argv[2] not in actions_allowed:
            print(f"\033[31mERR!\033[0m: '{sys.argv[2]}' Is Not Recognized As A Command")
        else:
            tldr(sys.argv[2])
    elif sys.argv[1] == '--init':
        init_db(FILE_DATA)
    elif sys.argv[1] == '-h':
        """
        THIS IS FOR HELP SECTIONS
        """
        help_sec()
        exit()
    elif sys.argv[1] == '-at':
        """
        THIS SECTION IS TO ADD TASKS
        """
        if get_file_id(FILE_DATA) == False:
            print(f"\033[31mERR!\033[0m: Database Has Not Been Initialized, Please Type 'td --init' to Continue")
            exit()
        if len(sys.argv) < 3:
            # task name
            print(f"\033[31mERR!\033[0m: Task Name Not Given\nRefer To TLDR Section For Help With Adding Tasks '-tldr -at'")
            pass
        elif len(sys.argv) < 4:
            # priority
            print(f"\033[31mERR!\033[0m: Priority Attr Not Given\nRefer To TLDR Section For Help With Adding Tasks '-tldr -at'")
            pass
        elif len(sys.argv) < 5:
            # status
            print(f"\033[31mERR!\033[0m: Status Attr Not Given\nRefer To TLDR Section For Help With Adding Tasks '-tldr -at'")
        linkfile = sys.argv[5] if len(sys.argv) > 5 else ""
        add_tasks(FILE_DATA,sys.argv[2],sys.argv[3],sys.argv[4],linkfile)
    elif sys.argv[1] == '-rt':
        print('remove task')
    elif sys.argv[1] == '-tt':
        print('toggle task state')
    elif sys.argv[1] == '-cp':
        print('change progress')
    elif sys.argv[1] == '--wipetasks':
        wipe_all_tasks(FILE_DATA)
    

    #file_stat = get_file_id(FILE_DATA)
    ##help_sec()
    #init_db(FILE_DATA)
    #add_tasks(FILE_DATA,"a task name 12","low","pending","www.google.com")

if __name__ == "__main__":
    main()
