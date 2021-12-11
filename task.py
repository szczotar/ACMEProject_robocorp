"""Template robot with Python."""

from RPA.Robocorp.WorkItems import WorkItems

def queueAcme(item_id):
    queue = WorkItems()
    queue.create_output_work_item()
    queue.set_work_item_variable("Age","28")
    queue.save_work_item()


def minimal_task():
    print("Done.")


if __name__ == "__main__":
    queueAcme(1)
    minimal_task()
