import os
import numpy as np
import enterprise.signals.parameter as parameter
import src.models_utils as aux

name = 'string_stable' # name of the model 

smbhb = False # set to True if you want to overlay the new-physics signal to the SMBHB signal

parameters = {
    'log10_mu' : parameter.Uniform(-14, -3)('log10_mu'),
    }

group = ['log10_mu']

cwd = os.getcwd()
log_spectrum = aux.spec_importer(cwd +'/inputs/models/models_data/stable.h5')


def spectrum(f, log10_mu):
    return 10**log_spectrum(np.log10(f), log10_mu=log10_mu)
