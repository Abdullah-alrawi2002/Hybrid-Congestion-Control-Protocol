import socket
import time

PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
INITIAL_WINDOW_SIZE = 1
SLOW_START_THRESHOLD = 64 * PACKET_SIZE
FILE_PATH = "file.mp3"
BASE_RTT = float('inf')
RTT_ALPHA = 1
RTT_BETA = 3
RTT_SMOOTHING_FACTOR = 0.125 
RTT_DEV_FACTOR = 0.25        
adaptive_timeout = 1
with open(FILE_PATH, "rb") as f:
    data = f.read()


total_data_sent = 0
start_time = None
end_time = None
packet_delays = []
jitter_sum = 0
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    udp_socket.bind(("localhost", 5000))
    udp_socket.settimeout(adaptive_timeout)
    RECEIVER_ADDRESS = ("localhost", 5001)

    start_time = time.time()
    seq_id = 0
    congestion_window = INITIAL_WINDOW_SIZE
    duplicate_acks = 0
    last_ack_id = None
    rtt_sample = None
    smoothed_rtt = None
    rtt_dev = None

    while seq_id < len(data):
        window_base = seq_id
        while seq_id < window_base + congestion_window * MESSAGE_SIZE and seq_id < len(data):
            chunk = data[seq_id: seq_id + MESSAGE_SIZE]
            message = int.to_bytes(seq_id, SEQ_ID_SIZE, byteorder='big', signed=True) + chunk
            send_time = time.time()
            udp_socket.sendto(message, RECEIVER_ADDRESS)
            total_data_sent += len(chunk)
            seq_id += MESSAGE_SIZE

        while True:
            try:
                ack, _ = udp_socket.recvfrom(PACKET_SIZE)
                ack_id = int.from_bytes(ack[:SEQ_ID_SIZE], byteorder='big', signed=True)
                ack_time = time.time()
                rtt_sample = ack_time - send_time
                packet_delays.append(rtt_sample)
                if smoothed_rtt is None:
                    smoothed_rtt = rtt_sample
                    rtt_dev = rtt_sample / 2
                else:
                    smoothed_rtt = (1 - RTT_SMOOTHING_FACTOR) * smoothed_rtt + RTT_SMOOTHING_FACTOR * rtt_sample
                    rtt_dev = (1 - RTT_DEV_FACTOR) * rtt_dev + RTT_DEV_FACTOR * abs(rtt_sample - smoothed_rtt)
                adaptive_timeout = smoothed_rtt + 4 * rtt_dev
                udp_socket.settimeout(adaptive_timeout)
                if ack_id >= window_base:
                    if congestion_window < SLOW_START_THRESHOLD:
                        congestion_window += 1 
                    else:
                        actual_throughput = (ack_id - window_base + MESSAGE_SIZE) / rtt_sample
                        expected_throughput = congestion_window / BASE_RTT
                        if actual_throughput < expected_throughput - RTT_BETA:
                            congestion_window -= 1 / congestion_window
                        elif actual_throughput > expected_throughput + RTT_ALPHA:
                            congestion_window += 1 / congestion_window

                    if ack_id == last_ack_id:
                        duplicate_acks += 1
                        if duplicate_acks == 3:
                            congestion_window = max(1, congestion_window / 2)
                            seq_id = ack_id + MESSAGE_SIZE
                    else:
                        duplicate_acks = 0
                    last_ack_id = ack_id
                    if ack_id >= seq_id - MESSAGE_SIZE * congestion_window:
                        break
            except socket.timeout:
                congestion_window = max(1, congestion_window * 0.7)
                seq_id = window_base
                break

    final_packet = int.to_bytes(-1, SEQ_ID_SIZE, byteorder='big', signed=True) + b''
    udp_socket.sendto(final_packet, RECEIVER_ADDRESS)

end_time = time.time()
throughput = total_data_sent / (end_time - start_time)
average_delay = sum(packet_delays) / len(packet_delays) if packet_delays else 0
jitter = sum(abs(packet_delays[i] - packet_delays[i - 1]) for i in range(1, len(packet_delays))) / len(packet_delays) if len(packet_delays) > 1 else 0
performance_metric = 0.2 * (throughput / 2000) + (0.1 / jitter) + (0.8 / average_delay)

print(f"Throughput: {throughput:.7f}, Avg Delay: {average_delay:.7f}, Jitter: {jitter:.7f}, Performance: {performance_metric:.7f}")
