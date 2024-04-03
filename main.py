import numpy as np

class Event:
    def __init__(self, time, event_type, process_id):
        self.time = time
        self.event_type = event_type
        self.process_id = process_id

class Process:
    def __init__(self, arrival_time, service_time, process_id):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.process_id = process_id

class EventQueue:
    def __init__(self):
        self.events = []

    def insert_event(self, event):
        self.events.append(event)
        self.events.sort(key=lambda x: x.time)

    def get_next_event(self):
        return self.events.pop(0)

def generate_exponential(lam):
    return -np.log(np.random.rand()) / lam

def simulate(arrival_rate, avg_service_time):
    event_queue = EventQueue()
    clock = 0
    total_turnaround_time = 0
    total_processes_completed = 0
    total_cpu_utilization_time = 0
    total_ready_queue_length = 0

    process_id = 0

    while total_processes_completed < 10000:
        # Generate arrival event
        arrival_time = clock + generate_exponential(arrival_rate)
        service_time = generate_exponential(1 / avg_service_time)
        event_queue.insert_event(Event(arrival_time, 'arrival', process_id))
        process_id += 1

        # Handle events
        while event_queue.events:
            current_event = event_queue.get_next_event()
            clock = current_event.time

            if current_event.event_type == 'arrival':
                total_ready_queue_length += len(event_queue.events) + 1

                if total_processes_completed == 10000:
                    break  # Terminate simulation if 10,000 processes completed

                if len(event_queue.events) == 1:  # First process in queue
                    total_cpu_utilization_time += current_event.time - clock

                event_queue.insert_event(Event(clock + service_time, 'departure', current_event.process_id))

            elif current_event.event_type == 'departure':
                total_processes_completed += 1
                total_turnaround_time += clock - current_event.process_id

                if len(event_queue.events) > 0:
                    total_cpu_utilization_time += event_queue.events[0].time - clock

        if total_processes_completed == 10000:
            break  # Terminate simulation if 10,000 processes completed

    avg_turnaround_time = total_turnaround_time / 10000
    throughput = 10000 / clock
    avg_cpu_utilization = total_cpu_utilization_time / clock
    avg_ready_queue_length = total_ready_queue_length / clock

    return avg_turnaround_time, throughput, avg_cpu_utilization, avg_ready_queue_length

def main():
    avg_arrival_rates = range(10, 31)
    avg_service_time = 0.04

    turnaround_times = []
    throughputs = []
    cpu_utilizations = []
    ready_queue_lengths = []

    for arrival_rate in avg_arrival_rates:
        avg_turnaround_time, throughput, avg_cpu_utilization, avg_ready_queue_length = simulate(arrival_rate, avg_service_time)
        turnaround_times.append(avg_turnaround_time)
        throughputs.append(throughput)
        cpu_utilizations.append(avg_cpu_utilization)
        ready_queue_lengths.append(avg_ready_queue_length)

        print(f"Arrival Rate: {arrival_rate}, Average Turnaround Time: {avg_turnaround_time}, Throughput: {throughput}, Average CPU Utilization: {avg_cpu_utilization}, Average Ready Queue Length: {avg_ready_queue_length}")

    # Plotting code for the metrics

if __name__ == "__main__":
    main()
