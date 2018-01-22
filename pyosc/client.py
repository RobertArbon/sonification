import numpy as np
import time
import argparse
import math
from os.path import join


# from pythonosc import osc_message_builder
# from pythonosc import udp_client

root_dir = '/Users/robert_arbon/Google Drive/Research/Sonification/'
data_dir = join(root_dir, 'Data/Chodera_data/Processed')

# Trajectories
entropy = np.load(join(data_dir, 'shannon_entropy_traj_lag1.0ps.npy'))
fast_modes = np.load(join(data_dir, 'fast_modes_lag1.0ps.npy'))
hmm_traj = np.load(join(data_dir, 'probabilistic_traj_lag1.0ps.npy'))

# Static properties
properties = np.load(join(data_dir, 'static_properties_max_scale.pickle'))

# Take derivatives
dfast_modes = fast_modes[:-1]-fast_modes[1:]
hmm_traj = hmm_traj[1:]
entropy = entropy[1:]

Nsteps = hmm_traj.shape[1]

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
            client.send_message("/properties/{0}/state{1}".format(k,i), float(x))

    for i in range(Nsteps):

        for j in range(hmm_traj.shape[1]):
            client.send_message("/state{}".format(j+1), float(hmm_traj[i][j]))

        client.send_message("/entropy", float(entropy[i]))

        for j in range(dfast_modes.shape[1]):
            client.send_message("/fast{}".format(j+1), float(dfast_modes[i,j]))

        time.sleep(.05)
