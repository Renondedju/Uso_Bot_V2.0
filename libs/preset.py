# -*- coding: utf-8 -*-
"""

    Presets library for R Algo
    By Renondedju and Jamu

"""
import os
import sys
sys.path.append(os.path.realpath('../'))

from user import User

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

        self.mods = None

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
            as the lenght of the map.
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

if __name__ == '__main__':
    peppy = User(2)
    preset = Preset(peppy, 'stream', 1.05)
    print (preset.mode)
    print (peppy.playstyle)
    print (preset.playstyle)