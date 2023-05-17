from enterprise.signals.parameter import function
import enterprise.signals.parameter as parameter
import numpy as np
import src.models_utils as aux

name = 'uldm_vecBL_unc' # name of the model

smbhb = True # set to True if you want to overlay the new-physics signal to the SMBHB signal

parameters ={
    "log10_A_dm" : parameter.Uniform(-9, -4)('log10_A_dm'),
    "log10_f_dm" : parameter.Uniform(-10, -5.5)('log10_f_dm'),
    "gamma_p" : parameter.Uniform(0, 2 * np.pi),
    "gamma_e1" : parameter.Uniform(0, 2 * np.pi)('gamma_e1'),
    "gamma_e2" : parameter.Uniform(0, 2 * np.pi)('gamma_e2'),
    "gamma_e3" : parameter.Uniform(0, 2 * np.pi)('gamma_e3'),
    "A_hat_sq_p" : aux.Gamma(1,0,1),
    "A_hat_sq_e1" : aux.Gamma(1,0,1)('A_hat_sq_e1'),
    "A_hat_sq_e2" : aux.Gamma(1,0,1)('A_hat_sq_e2'),
    "A_hat_sq_e3" : aux.Gamma(1,0,1)('A_hat_sq_e3')
}

group = ['log10_A_dm', 'log10_f_dm']

def pulsar_signal(toas, log10_A_dm, log10_f_dm, gamma_p, A_hat_sq_p):
    
    A = 10**log10_A_dm
    f = 10**log10_f_dm

    # return timing residual in seconds
    return A * np.sqrt(A_hat_sq_p) * np.sin(2 * np.pi * f * toas + gamma_p)

def earth_signal(toas, pos, log10_A_dm, log10_f_dm, gamma_e1, gamma_e2, gamma_e3, A_hat_sq_e1, A_hat_sq_e2, A_hat_sq_e3):
    
    A = 10**log10_A_dm
    f = 10**log10_f_dm

    # return timing residual in seconds
    return 0.5 * A * (np.sqrt(A_hat_sq_e1)*pos[0] * np.sin(2 * np.pi * f * toas + gamma_e1 * pos[0]) +
                      np.sqrt(A_hat_sq_e2)*pos[1] * np.sin(2 * np.pi * f * toas + gamma_e2 * pos[1]) +
                      np.sqrt(A_hat_sq_e3)*pos[2] * np.sin(2 * np.pi * f * toas + gamma_e3 * pos[2]))


def signal(toas, pos, log10_A_dm, log10_f_dm, gamma_p, gamma_e1, gamma_e2, gamma_e3, A_hat_sq_p, A_hat_sq_e1, A_hat_sq_e2, A_hat_sq_e3):
    """
    Function that calculates the pulsar + earth signal generated by vector
    ultralight dark matter in the uncorrelated limit 
    :param toas: pulsar Time-of-arrival measurements [s]
    :param pos: pulsar position vector
    :param log10_A_dm: log10 of signal amplitude
    :param log10_f_dm: log10 of signal frequency
    :param gamma_p: Pulsar-term phase (projected on pulsar direction)
    :param gamma_e[1,2,3]: Earth-term vector phase
    :param A_hat_sq_p: dm density fluctuation at the pulsar position (projected on pulsar direction)
    :param A_hat_sq_e[1,2,3]: dm density fluctuation vector at the Earth position
    :return: the waveform as induced timing residuals (seconds)
    """

    p_s = pulsar_signal(toas, log10_A_dm, log10_f_dm, gamma_p, A_hat_sq_p)
    e_s = earth_signal(toas, pos, log10_A_dm, log10_f_dm, gamma_e1, gamma_e2, gamma_e3, A_hat_sq_e1, A_hat_sq_e2, A_hat_sq_e3)

    # return timing residual in seconds
    return p_s + e_s
