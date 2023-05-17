import os
import numpy as np
import enterprise.signals.parameter as parameter
import src.models_utils as aux

name = 'fundamental' # name of the model 

smbhb = True # set to True if you want to overlay the new-physics signal to the SMBHB signal

parameters = {
    'log10_Gmu' : parameter.Uniform(-14, -6)('log10_Gmu'),
    }

group = ['log10_Gmu']   

cwd = os.getcwd()
log_spectrum = aux.spec_importer(cwd +'/inputs/models/models_data/stable_m.h5')

def spectrum(f, log10_Gmu):
    return 10**log_spectrum(np.log10(f), log10_Gmu=log10_Gmu)
