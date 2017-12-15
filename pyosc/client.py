import numpy as np
import time
import argparse
import math

from pythonosc import osc_message_builder
from pythonosc import udp_client

res_1 = np.load("/users/ajj/google drive/data/ala-dihed.npy")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="")
    parser.add_argument("--port", type=int, default=5005,
                        help="")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    for x in res_1:
        print(x)
        client.send_message("/psi", float(x[0]))
        client.send_message("/phi", float(x[1]))

        time.sleep(.05)
