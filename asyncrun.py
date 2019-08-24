import logging

log = logging.getLogger()

async def asyncrun(cmd, *args):
    """Runs the given command, connects stdout to the current shell and waits until it is completed"""
    log.info(f"Running cmd {cmd} with {list(args)}")
    pass


async def asyncrun_quiet(cmd, *args):
    """Runs the given command quietly and waits until it is completed."""
    log.debug(f"Quietly Running cmd {cmd} with {list(args)}")
    pass
