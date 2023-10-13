from scheduler import scheduler
import wpilib
from enum import Enum

class State(Enum):
    Disabled = 0
    Autonomous = 1
    Teleop = 2
    Test = 3

    # Special states
    Current = 4

class ScheduleException(Exception):
    pass

class GreenRobot(wpilib.TimedRobot):
    schedulers = [None,None,None,None]
    configured_state = State.Disabled

    def robotInit(self):
        GreenRobot.schedulers = [scheduler(),scheduler(),scheduler(),scheduler()]

    def current_state():
        state = None
        if wpilib.RobotState.isDisabled():
            state = State.Disabled
        elif wpilib.RobotState.isAutonomous():
            state = State.Autonomous
        elif wpilib.RobotState.isTeleop():
            state = State.Teleop
        elif wpilib.RobotState.isTest():
            state = State.Test
        else:
            raise ScheduleException()

        return state

    def schedule(state, routine, callvalue=None):
        if state == State.Current:
            return GreenRobot.schedulers[GreenRobot.current_state().value].add(routine, callvalue, temp=True)
        else:
            return GreenRobot.schedulers[state.value].add(routine, callvalue)

    def schedule_front(state, routine, callvalue=None):
        if state == State.Current:
            return GreenRobot.schedulers[GreenRobot.current_state().value].add_front(routine, callvalue, temp=True)
        else:
            return GreenRobot.schedulers[state.value].add_front(routine, callvalue)

    # Remove routine_index from current scheduler
    def remove(routine_index):
        GreenRobot.schedulers[GreenRobot.configured_state.value].remove(routine_index)

    def is_alive(routine_index):
        return GreenRobot.schedulers[GreenRobot.configured_state.value].is_alive(routine_index)

    # Static function
    def run():
        state = GreenRobot.current_state()

        if GreenRobot.configured_state != state:
            # Reset the configured state
            print(f"Reset state for: {GreenRobot.configured_state}")
            GreenRobot.schedulers[GreenRobot.configured_state.value].reset()
            GreenRobot.configured_state = state
        
        GreenRobot.schedulers[state.value].run()
    
    def getTickCount():
        return GreenRobot.schedulers[GreenRobot.configured_state.value].getTickCount()
