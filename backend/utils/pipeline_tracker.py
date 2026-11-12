from datetime import datetime


class PipelineTracker:

    def __init__(self):

        self.steps = []

        self.step_number = 0

    def add(self, step: str):

        self.step_number += 1

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log_entry = {
            "step_number": self.step_number,
            "timestamp": timestamp,
            "message": step
        }

        self.steps.append(log_entry)

        print(
            f"[STEP {self.step_number}] "
            f"{timestamp} | "
            f"{step}"
        )

    def get_steps(self):
        return self.steps

    def get_step_count(self):
        return len(self.steps)

    def clear(self):
        self.steps.clear()
        self.step_number = 0