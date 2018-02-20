# -*- coding: utf-8 -*-
"""

Mods and modes enums

"""


class Mods():
    """Enums of the mods"""

    none = 0
    NoFail = 1
    Easy = 2
    NoVideo = 4  # Not used anymore, but can be found on old plays like Mesita on b/78239
    Hidden = 8
    HardRock = 16
    SuddenDeath = 32
    DoubleTime = 64
    Relax = 128
    HalfTime = 256
    Nightcore = 512  # Only set along with DoubleTime. i.e: NC only gives 576
    Flashlight = 1024
    Autoplay = 2048
    SpunOut = 4096
    Relax2 = 8192  # Autopilot?
    Perfect = 16384  # Only set along with SuddenDeath. i.e: PF only gives 16416
    Key4 = 32768
    Key5 = 65536
    Key6 = 131072
    Key7 = 262144
    Key8 = 524288
    keyMod = (32768 | 65536 | 131072 | 262144 | 524288)
    FadeIn = 1048576
    Random = 2097152
    LastMod = 4194304
    FreeModAllowed = (1 | 2 | 8 | 16 | 32 | 1024 | 1048576 | 128 | 8192 | 4096 | (
        32768 | 65536 | 131072 | 262144 | 524288))
    Key9 = 16777216
    Key10 = 33554432
    Key1 = 67108864
    Key3 = 134217728
    Key2 = 268435456


class Mode():
    """Enum of the modes"""
    Osu = 0
    Taiko = 1
    Ctb = 2
    Mania = 3

def Mode_to_str(mode: Mode):
    if mode == Mode.Osu:
        return "osu"
    if mode == Mode.Taiko:
        return "taiko"
    if mode == Mode.Ctb:
        return "ctb"
    if mode == Mode.Mania:
        return "mania"

def mod_emoji(mods:str):
    """ Because emoji >= letters? """
    # No but carry on :^) -Jamu
    # Emojis >> all       -Renon
    mods = mods.replace("SD", "<:mod_suddendeath:327800921113231361>")
    mods = mods.replace("FL", "<:mod_flashlight:327800804037885962>" )
    mods = mods.replace("DT", "<:mod_doubletime:327800759741579265>" )
    mods = mods.replace("NC", "<:mod_nightcore:327800859989901312>"  )
    mods = mods.replace("HR", "<:mod_hardrock:327800817711054858>"   )
    mods = mods.replace("SO", "<:mod_spunout:327800910249984001>"    )
    mods = mods.replace("PF", "<:mod_perfect:327800879019458571>"    )
    mods = mods.replace("HD", "<:mod_hidden:328172007931904002>"     )
    mods = mods.replace("NF", "<:mod_nofail:327800869523554315>"     )
    mods = mods.replace("RL", "<:mod_relax:327800900318134273>"      )
    mods = mods.replace("EZ", "<:mod_easy:327800791631134731>"       )
    mods = mods.replace("AP", "<:mod_auto:327800780444794880>"       )
    
    return mods
