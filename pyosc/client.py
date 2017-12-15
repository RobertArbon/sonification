import numpy as np
import time
import argparse
import math

from pythonosc import osc_message_builder
from pythonosc import udp_client

res_1 = np.load("/Users/Ajj/Google Drive/Data/hmm_trajectories/traj-0.npy")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="192.168.1.7",
                        help="")
    parser.add_argument("--port", type=int, default=5005,
                        help="")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    for x in res_1:
        print(x)
        client.send_message("/state1", float(x[0]))
        client.send_message("/state2", float(x[1]))
        client.send_message("/state3", float(x[2]))
        time.sleep(.1)
