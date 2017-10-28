# -*- coding: utf-8 -*-
"""

    Presets library for R Algo
    By Renondedju and Jamu

"""
import os
import sys
sys.path.append(os.path.realpath('../'))

from lib.user import User

class Prest:
    """ Preset class """

    def __init__(self, player:User):
        """ Init """

        self.user = player

        self.reset()        
    
    def reset(self):
        """ Resets the preset to regular mode """

        self.pp   = self.user.pp_average
        self.acc  = self.user.accuracy_average
        self.bpm  = self.user.bpm_average
        self.len  = self.user.len_average

        self.od   = self.user.od_average
        self.ar   = self.user.ar_average
        self.cs   = self.user.cs_average

        self.mods = None

    def set_training_mode(self, power:float = 1.05):
        """ --- Set the preset to gereral training mode

            Training mode is a bit harder than regular mode pp wise.
            Nothing is changed in the others stats.
        """
        self.reset()
        self.pp = self.user.pp_average * power

        return

    def set_stamina_mode(self, power:float = 1.05):
        """ --- Set the preset to stamina training mode

            Stamina training mode is harder on the bpm speed as well
            as the lenght of the map.
        """

        self.reset()
        self.bpm = self.user.bpm_average * power
        self.len = self.user.len         * power 

        return

    def set_chill_mode(self, power:float = 1.05):
        """ --- Set the preset to chill mode

            Chill mode slows down the bpm and decreases the pp
            amount of the map
        """

        self.reset()
        self.bpm = self.user.bpm_average / power
        self.pp  = self.user.pp_average  / power

        return