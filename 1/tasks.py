import datetime
import time
import threading
from queue import Queue

class Server:
    def __init__(self, id):
        self.id = id
        self.remaining_time = 0
        self.queue = Queue()

    def assign_task(self, task):
        if self.is_idle():
            self.remaining_time = task
        else:
            self.queue.put(task)

    def tick(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
        if self.remaining_time == 0 and not self.queue.empty():
            self.remaining_time = self.queue.get()

    def is_idle(self):
        return self.remaining_time == 0
    
    def total_load(self):
        return self.remaining_time + sum(list(self.queue.queue))
    
class System:
    def __init__(self, servers_count):
        self.servers = [Server(i) for i in range(servers_count)]

    def add_task(self, task):
        server = min(self.servers, key = lambda s: s.total_load())
        server.assign_task(task)
        print(f"Task with duration {task}s assigned to Server {server.id}.")

    def tick(self):
        for server in self.servers:
            server.tick()

    def status(self):
        print(f"\nServer status at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:")
        for server in self.servers:
            if server.is_idle():
                print(f"Server {server.id}: Idle")
            else:
                print(f"Server {server.id}: Working on task (remaining time: {server.remaining_time}s)")
            print(f"Queue: {list(server.queue.queue) or 'Empty'}")
    
def main():
    print("Welcome to the Distributed System Simulator.")
    servers_count = int(input("Enter the number of servers: "))
    system = System(servers_count)

    def run_simulation():
        while True:
            system.tick()
            time.sleep(1)

    threading.Thread(target=run_simulation, daemon=True).start()

    while True:
        command = input("Enter command(add <seconds>, status or exit): ").strip().lower()
        if command == "exit":
            print("Exiting")
            break
        if command == "status":
            system.status()
        elif command.startswith("add"):
            try:
                _, task = command.split()
                system.add_task(int(task))
            except ValueError:
                print("Invalid input. Use 'add <seconds>' or 'exit'.")
        else:
            print("Invalid input. Use 'add <seconds>' or 'exit'.")


if __name__ == "__main__":
    main()
