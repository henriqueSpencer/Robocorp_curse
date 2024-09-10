from robocorp.tasks import task

from Curse_Level_I import curse_level_I_tasks
from Curse_Level_II import curse_level_II_tasks
from Curse_Level_III import curse_level_III_tasks


@task
def minimal_task():
    """ This is a minimal task. """
    #curse_level_I_task()
    curse_level_II_tasks()
