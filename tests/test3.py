import pyphi
import numpy as np

network = pyphi.examples.fig6()
state = (1,0,0)

subsystem = pyphi.Subsystem(network, state)
ABC = subsystem.node_indices

mip_c = subsystem.cause_mip(ABC, ABC)
mip_e = subsystem.effect_mip(ABC, ABC)

# print(mip_c.phi)
# print(mip_c.partition)
print(mip_e.phi)
print(mip_e.partition)

ces = pyphi.compute.ces(subsystem)
print(ces.labeled_mechanisms)
