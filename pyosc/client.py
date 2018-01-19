import numpy as np
import time
import argparse
import math

from pythonosc import osc_message_builder
from pythonosc import udp_client

phipsi = np.load("/users/ajj/google drive/data/hmm_trajectories/traj-0.npy")
entropy = np.load("/users/ajj/google drive/data/hmm_trajectories/entropy-0.npy")
tica = np.load("/users/ajj/google drive/data/tica_trajectories/traj-0.npy")
properties = np.load("/users/ajj/google drive/data/static_properties_max_scale.npy")
properties = np.load("/users/ajj/google drive/data/static_properties_01_scale.npy")


#
dtica = tica[:-1]-tica[1:]
phipsi = phipsi[1:]
entropy = entropy[1:]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="")
    parser.add_argument("--port", type=int, default=5005,
                        help="")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    for k, v in properties.items():
        for i, x in enumerate(v):
            client.send_message("/properties/{0}/state{1}".format(k,i), float(v))

    for i, x in enumerate(phipsi):
        print(x)
        client.send_message("/state1", float(x[0]))
        client.send_message("/state2", float(x[1]))
        client.send_message("/state3", float(x[2]))
        client.send_message("/entropy", float(entropy[i]))
        for j in range(dtica.shape[1]):
            client.send_message("/tica{}".format(j+1), float(dtica[i,j]))
        time.sleep(.05)
