import numpy as np
import os.path
from shutil import copyfile
import mdtraj as md


outdir = 'Trajectories'
indir = '/Users/robert_arbon/Google Drive/Research/Ala2/shoot-302K-100ps/state'
i=0
for j in range(1,11):
    inpath = os.path.join(indir, '{0}/{1}/md.trj'.format(i+1,j))
    if os.path.isfile(inpath):
        copyfile(inpath, os.path.join(outdir,'{0}-{1:04d}.mdcrd'.format(i+1,j)))

paths = [os.path.join(outdir, '{0}-{1:04d}.mdcrd'.format(i+1,j)) for j in range(1,11)]

traj = md.load(paths, top='a1e-solute.pdb', discard_overlapping_frames=True)
traj.save(os.path.join(outdir,'{0}.xtc'.format(i+1)))
