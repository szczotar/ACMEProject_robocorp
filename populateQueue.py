"""Template robot with Python."""

from RPA.Robocorp.WorkItems import WorkItems

listAge = ["30", "28", "15"]
def queueAcme():
    queue = WorkItems()
    queue.get_input_work_item()
   
    for name in listAge:
              
        queue.create_output_work_item()
        queue.set_work_item_variable("Age", name)
        queue.set_work_item_variable("Name", "Artur")
        print(queue.list_work_item_variables())
        queue.save_work_item()
    
def minimal_task():
    print("Done.")
    queue = WorkItems()

    
    for i in range(3):
        queue.get_input_work_item()
        payload = queue.get_work_item_payload()
        print(payload)

if __name__ == "__main__":
    queueAcme()
    # minimal_task()
