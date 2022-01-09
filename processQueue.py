from RPA.Robocorp.WorkItems import WorkItems, State



def minimal_task():
    
    queue = WorkItems()
    for i in range(3):
        queue.get_input_work_item()
        payload = queue.get_work_item_payload()
        print(payload)
        queue.release_input_work_item(state= State.DONE)


if __name__ == "__main__":
    minimal_task()