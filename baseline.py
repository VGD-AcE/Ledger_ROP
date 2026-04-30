import gdb

class BaselineTimer(gdb.Command):
    """
    Baseline GDB command for running the target program without any defense mechanism.

    This command runs the target binary from the entry point (_start)
    directly until program completion, without stepping through instructions
    or applying any runtime verification logic.
    """

    def __init__(self):
        super(BaselineTimer, self).__init__("baseline", gdb.COMMAND_USER)
        print("✅ baseline_timer.py loaded. Command 'baseline' has been registered.")

    def invoke(self, arg, from_tty):
        """
        Entry point for the 'baseline' GDB command.
        Runs the target program without applying defense checks.

        Args:
            arg (str): Command-line arguments passed to GDB (unused).
            from_tty (bool): True if command was typed interactively in GDB.
        """
        # Execute the program without any defense
        gdb.execute("run")

        # Once execution finishes, exit GDB automatically
        print("[INFO] Program execution finished. Exiting GDB.")
        gdb.execute("quit")


# Register the custom GDB command
BaselineTimer()
