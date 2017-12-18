# -*- coding: utf-8 -*-
"""

    Presets library for R Algo
    By Renondedju and Jamu

"""
import os
import sys
sys.path.append(os.path.realpath('../'))

from libs.user import User
from libs.mods import Mods

class Preset:
    """ Preset class """

    def __init__(self, player:User, mode:str = 'default', power:float = 1.05):
        """ Init """

        self.user = player
        self.reset()

        self.mode = 'default'

        #Calling the method corresponding to the mode specified
        handler = getattr(self, 'set_%s_mode' % mode, None)
        if handler:
            
            self.mode = mode

            handler_kwargs = {'power': power}
            response = handler(**handler_kwargs)
            
    
    def reset(self):
        """ Resets the preset to regular mode """

        self.pp         = self.user.pp_average
        self.acc        = self.user.accuracy_average
        self.bpm        = self.user.bpm_average
        self.len        = self.user.len_average

        self.playstyle  = self.user.playstyle

        self.od         = self.user.od_average
        self.ar         = self.user.ar_average
        self.cs         = self.user.cs_average

        self.mods       = {
            'Nomod'   : self.user.Nomod_playrate,
             'HR'     : self.user.HR_playrate,
             'HD'     : self.user.HD_playrate,
             'DT'     : self.user.DT_playrate,
             'DTHD'   : self.user.DTHD_playrate,
             'DTHR'   : self.user.DTHR_playrate,
             'HRHD'   : self.user.HRHD_playrate,
             'DTHRHD' : self.user.DTHRHD_playrate}

    def set_training_mode(self, power:float):
        """ --- Set the preset to gereral training mode

            Training mode is a bit harder than regular mode pp wise.
            Nothing is changed in the others stats.
        """
        self.reset()
        self.pp = self.user.pp_average * power

        return

    def set_stamina_mode(self, power:float):
        """ --- Set the preset to stamina mode

            Stamina training mode is harder on the bpm speed as well
            as the length of the map.
        """

        self.reset()
        self.bpm = self.user.bpm_average * power
        self.len = self.user.len_average * power 

        return

    def set_chill_mode(self, power:float):
        """ --- Set the preset to chill mode

            Chill mode slows down the bpm and decreases the pp
            amount of the map
        """

        self.reset()
        self.bpm = self.user.bpm_average / power
        self.pp  = self.user.pp_average  / power

        return

    def set_stream_mode(self, power:float):
        """ --- Set the preset to streaming mode

            Increases the playstyle to increase the streaming difficulty
        """

        self.playstyle = self.user.playstyle * power

    def set_jump_mode(self, power:float):
        """ --- Set the preset to jump mode

            Decreases the playstyle to increase the jumping difficulty
        """

        self.playstyle = self.user.playstyle / power

    def select_mods(self, mods:int):
        """ Selects a mod for the preset """

        selected_mods = 'Nomod'

        if mods == Mods.HardRock:
            selected_mods = 'HR'
        elif mods == Mods.Hidden:
            selected_mods = 'HD'
        elif mods == Mods.DoubleTime:
            selected_mods = 'DT'
        elif mods == Mods.DoubleTime | Mods.Hidden:
            selected_mods = 'DTHD'
        elif mods == Mods.DoubleTime | Mods.HardRock:
            selected_mods = 'DTHR'
        elif mods == Mods.HardRock | Mods.Hidden:
            selected_mods = 'HRHD'
        elif mods == Mods.DoubleTime | Mods.HardRock | Mods.Hidden:
            selected_mods = 'DTHRHD'

        for mod in self.mods:
            if (mod == selected_mods):
                self.mods[mod] = 100.0
            else:
                self.mods[mod] = 0.0

        return

if __name__ == '__main__':
    #Just some test lines 

    peppy = User(2)
    preset = Preset(peppy, 'stream', 1.05)
    print (preset.mode)
    print (peppy.playstyle)
    print (preset.playstyle)
    preset.select_mods(Mods.Hidden)
    print (preset.mods['HD'])