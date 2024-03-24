import csv
import time

# Initialize cwnd, ssthresh, and recovery_flag
cwnd = 1
ssthresh = 400
recovery_flag = False
time_gone=0
# Open a new CSV file in write mode
with open('congestion_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(["time", "cwnd"])

    # Start time
    start_time = time.time()

    # Loop for 2 seconds
    while time.time() - start_time < 2:
        # Calculate current time and cwnd value
        current_time = time.time() - start_time
        if cwnd < ssthresh:
            # Slow start phase: exponential growth
            cwnd *= 2
        else:
            # Congestion avoidance phase: linear growth
            cwnd += 1
            # Simulate fast recovery for 3 to 4 times
            if cwnd % 4 == 0:
                ssthresh = cwnd // 2
                cwnd = ssthresh + 3
                recovery_flag = True
                time_gone = current_time
            elif recovery_flag:
                # New Reno: continue fast recovery until a packet sent after the start of the recovery phase is acknowledged
                cwnd = ssthresh

                if current_time -time_gone > .4 :
                    recovery_flag = False


        # Write time and cwnd value to CSV file
        writer.writerow([format(current_time*1000,'.2f'), cwnd])

        # Wait for 100 ms
        time.sleep(0.1)