# Hybrid-Congestion-Control-Protocol
This project implements an optimized congestion control protocol for UDP communication, designed to maximize throughput while minimizing average packet delay and jitter. By combining the proactive congestion detection of Vegas with the fairness and robustness of CUBIC, the protocol ensures stable performance across varying network conditions.
Project Overview
Modern congestion control protocols face challenges in balancing throughput, latency, jitter, and fairness, especially in dynamic and competitive network environments.
This project addresses these challenges by combining the strengths of two popular congestion control algorithms:

Vegas for proactive delay-aware adjustments.
CUBIC for fairness and robustness under packet loss.
This hybrid protocol provides optimized performance for real-time applications, streaming, and other bandwidth-sensitive use cases.

Features
Proactive Congestion Detection: Avoids congestion by monitoring throughput and delay metrics.
CUBIC Growth and Recovery: Ensures fairness and stable throughput, especially under packet loss.
Smoothed RTT Estimation: EWMA-based RTT calculations for adaptive timeout handling.
Gentle Timeout Handling: Gradual congestion window reduction to maintain throughput stability.
Real-Time Jitter Optimization: Reduces delay variability, ensuring consistent performance.
How It Works
The protocol integrates:

Vegas Metrics:

Measures the difference between expected throughput and actual throughput.
Adjusts congestion window size to maintain low delays and avoid congestion.
CUBIC Function:

Manages window growth using a cubic function for fairness and stability.
Handles recovery after packet loss more efficiently than traditional algorithms.
RTT and Jitter:

Real-time RTT smoothing using EWMA for dynamic timeout adjustments.
Jitter computation ensures steady performance across varying network conditions.
