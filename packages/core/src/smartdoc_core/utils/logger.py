# logger.py - Centralized logging system for SmartDoc
import datetime


class SystemLogger:
    def __init__(self, logfile_path="conversation_log.txt"):
        self.logfile_path = logfile_path
        try:
            # Ensure we can write to the log file, create if not exists
            with open(self.logfile_path, "a", encoding="utf-8") as f:
                f.write(
                    f"\n--- Log Session Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n"
                )
            print(f"Logging interactions to: {self.logfile_path}")
        except IOError as e:
            print(
                f"Error: Could not open or write to log file {self.logfile_path}. Logging will be disabled. Error: {e}"
            )
            self.logfile_path = None  # Disable logging if file can't be accessed

    def log_interaction(
        self,
        student_input,
        vsp_response,
        dm_state=None,
        nlu_intent=None,
        nlu_score=None,
    ):
        if not self.logfile_path:
            return  # Logging is disabled

        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}]\n"
            if dm_state:
                log_entry += f"  DM State: {dm_state}\n"
            if nlu_intent:
                log_entry += f"  NLU Intent: {nlu_intent} (Score: {nlu_score:.4f})\n"
            log_entry += f"  Student: {student_input}\n"
            log_entry += f"  SmartDoc: {vsp_response}\n"
            log_entry += "-" * 20 + "\n"

            with open(self.logfile_path, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except IOError as e:
            print(f"Error writing to log file: {e}")
            # Optionally disable further logging attempts
            # self.logfile_path = None

    def log_system(self, level, message):
        """
        Logs a system-level message (info, error, debug, etc.).
        """
        if not self.logfile_path:
            return

        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{level.upper()}] {message}\n"
            with open(self.logfile_path, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except IOError as e:
            print(f"Error writing to log file: {e}")


# Singleton instance for system logs
sys_logger = SystemLogger(logfile_path="system_log.txt")


def info(message):
    sys_logger.log_system("info", message)


def error(message):
    sys_logger.log_system("error", message)


def debug(message):
    sys_logger.log_system("debug", message)


def warning(message):
    sys_logger.log_system("warning", message)


def critical(message):
    sys_logger.log_system("critical", message)
