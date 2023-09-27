import psutil
import requests
import time
import matplotlib
matplotlib.use("TkAgg")  # Specify the backend before importing pyplot
import matplotlib.pyplot as plt

# Replace with your server's URL
SERVER_URL = "http://52.22.126.173"

# Lists to store historical data
cpu_data = []
memory_data = []
time_data = []

def get_server_stats():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    return {"cpu_percent": cpu_percent, "memory_percent": memory_percent}

def send_data_to_server(data):
    try:
        response = requests.post(f"{SERVER_URL}/", json=data)
        response.raise_for_status()
        print("Data sent successfully!")
    except Exception as e:
        print(f"Failed to send data: {str(e)}")

if __name__ == "__main__":
    while True:
        server_stats = get_server_stats()
        send_data_to_server(server_stats)
        
        # Store data for plotting
        cpu_data.append(server_stats["cpu_percent"])
        memory_data.append(server_stats["memory_percent"])
        time_data.append(time.strftime("%H:%M:%S"))
        
        # Plot the data
        plt.figure(figsize=(10, 5))
        plt.plot(time_data, cpu_data, label="CPU %", marker='o')
        plt.plot(time_data, memory_data, label="Memory %", marker='x')
        plt.xlabel("Time")
        plt.ylabel("Usage %")
        plt.title("Server Usage")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        time.sleep(60)  # Send data every minute
