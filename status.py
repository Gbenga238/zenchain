import subprocess
from datetime import datetime, timedelta

CONTAINER_NAME = "zenchain"

class ValidatorMonitor:
    def __init__(self):
        self.log_process = self.start_log_stream()
        self.blocks_validated = 0
        self.last_validated_block = None
        self.last_validation_time = None

    def start_log_stream(self):
        return subprocess.Popen(
            ['docker', 'logs', '-f', CONTAINER_NAME],  # Corrigé ici : '-f' au lieu de -f
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

    def monitor_logs(self):
        try:
            while True:
                line = self.log_process.stdout.readline()
                if not line:
                    break
                if "Prepared block for proposing at" in line:
                    self.process_validated_block(line)
        except Exception as e:
            print(f"\nError reading logs: {e}")

    def process_validated_block(self, log_line):
        current_time = datetime.now()
        block_number = log_line.split('Prepared block for proposing at')[1].split(',')[0].strip()
        
        self.blocks_validated += 1
        self.last_validated_block = block_number
        
        if self.last_validation_time:
            time_since_last = (current_time - self.last_validation_time).total_seconds()
        else:
            time_since_last = 0
        
        self.last_validation_time = current_time

        print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} 🟢 Validated Block: {block_number} | "
              f"Total Validated: {self.blocks_validated} | "
              f"Time Since Last: {time_since_last:.0f}s")

    def run(self):
        print("Starting Zenchain Validator Monitor...")
        print("Waiting for block validations...")
        try:
            self.monitor_logs()
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
        finally:
            if self.log_process:
                self.log_process.terminate()

if __name__ == "__main__":
    monitor = ValidatorMonitor()
    monitor.run()
