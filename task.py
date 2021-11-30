import sys

__TASK_FILE__ = "task.txt"
__COMPLETED_FILE__ = "completed.txt"

def main():
    args = sys.argv[1:]
    if len(args) == 0 or len(args) == 1 and args[0] == "help" :
        help()
    elif args[0] == "add":
        if len(args) < 3:
            print("Error: Missing tasks string. Nothing added!")
        else:
            add(args[1], ' '.join(args[2:]))
    elif args[0] == "ls":
        ls()
    elif args[0] == "del":
        if len(args) < 2:
            print("Error: Missing NUMBER for deleting tasks.")
        else:
            delete(args[1])
    elif args[0] == "done":
        if len(args) < 2:
            print("Error: Missing NUMBER for marking tasks as done.")
        else:
            done(args[1])
    elif args[0] == "report":
        report()
    elif args[0] == 'clear':
        __clear__()
    else:
        print("Error: Unknown command. Use `$ ./task help` to see usage.")


def help():
    '''
    Executing the command without any arguments, or with a single argument help prints the CLI usage.
    '''
    print("Usage :-")
    print("$ ./task add 2 hello world     # Add a new item with priority 2 and text \"hello world\" to the list")
    print("$ ./task ls                    # Show incomplete priority list items sorted by priority in ascending order")
    print("$ ./task del NUMBER   # Delete the incomplete item with the given priority number")
    print("$ ./task done NUMBER  # Mark the incomplete item with the given PRIORITY_NUMBER as complete")
    print("$ ./task help                  # Show usage")
    print("$ ./task report                # Statistics")


def ls():
    '''
    Show pending tasks sorted by priority.
    '''
    tasks = __fetch__(__TASK_FILE__)

    if len(tasks) == 0:
        print('There are no pending tasks!')
        return

    for i in range(len(tasks)):
        # -1 for the `\n` at the end of each line
        task = tasks[i][:-1].split(' ')
        print(str(i+1) + ". " + ' '.join(task[1:]) + " ["  + task[0] + "]")


def add(priority, task):
    '''
    Add a new item with priority PRIORITY and text TEXT to the list.
    '''
    if not priority.isdigit() or int(priority) < 0:
        print("Error :- Invalid priority. It should be an integer greater than 0")
        return

    tasks = __fetch__(__TASK_FILE__)
    
    for i in range(len(tasks)+1):
        if i == len(tasks) or int(tasks[i].split(' ')[0]) > int(priority):
            tasks.insert(i, priority + " " + task + "\n")
            break
    
    __dump__(__TASK_FILE__, tasks)

    print("Added task: \"" + task + "\" with priority " + priority)


def delete(index):
    '''
    Delete an item at index `index`.
    '''
    tasks = __fetch__(__TASK_FILE__)
    
    if not index.isdigit() or int(index) > len(tasks) or int(index) < 1:
        print("Error: task with index #" + index + " does not exist. Nothing deleted.")
        return
    
    tasks.pop(int(index) - 1)
    print("Deleted task #" + index)

    __dump__(__TASK_FILE__, tasks)


def done(index):
    '''
    Marks the task at index `index` as completed, moving it to the completed list.
    '''
    tasks = __fetch__(__TASK_FILE__)

    if not index.isdigit() or int(index) <= 0 or int(index) > len(tasks):
        print('Error: no incomplete item with index #' + index + ' exists.')
        return

    completed = __fetch__(__COMPLETED_FILE__)
    completed.append(tasks.pop(int(index)-1))

    __dump__(__TASK_FILE__, tasks)
    __dump__(__COMPLETED_FILE__, completed)

    print('Marked item as done.')


def report():
    '''
    Shows the number of complete and incomplete items in the list.
    '''
    tasks = __fetch__(__TASK_FILE__)
    completed = __fetch__(__COMPLETED_FILE__)

    print("Pending : " + str(len(tasks)))
    if len(tasks) > 0:
        ls()

    print()

    print("Completed : " + str(len(completed)))
    for i in range(len(completed)):
        # -1 for the `\n` at the end of each line
        task = completed[i][:-1].split(' ')
        print(str(i+1) + ". " + ' '.join(task[1:]))


def __clear__():
    '''
    Clears `__TASK_FILE__` and `__COMPLETED_FILE__`.
    '''
    __dump__(__TASK_FILE__, [])
    __dump__(__COMPLETED_FILE__, [])


def __fetch__(filename):
    '''
    Fetch the list of tasks from the file `filename`. Creates the file if it does not exist.
    '''

    data = []
    try:
        with open(filename, 'r') as fp:
            data = fp.readlines()
    except:
        open(filename, 'x')
    return data


def __dump__(filename, tasks):
    '''
    Dumps the list of tasks to the file `filename`. Creates the file if it does not exist.
    '''
    with open(filename, 'w') as fp:
        fp.writelines(tasks)


if __name__ == "__main__":
    main()
