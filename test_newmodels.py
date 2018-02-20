#!/usr/bin/env python3

from libs.database import Session, initDB
from libs.models import Beatmap, PP, import_beatmap


if __name__ == '__main__':
    initDB()
    # session = Session()
    # Beatmap.getBeatmap(37173)
    # Beatmap.getBeatmap(75)
    # Beatmap.getBeatmap(80)
    # Beatmap.getBeatmap(87)
    # Beatmap.getBeatmap(88)
    # Beatmap.getBeatmap(100)
    # Beatmap.getBeatmap(132)
    # Beatmap.getBeatmap(148)
    # Beatmap.getBeatmap(152)
    # Beatmap.getBeatmap(153)

    Beatmap.get_beatmap(165)  # airman !!!!
    Beatmap.get_beatmap(180)
    # Beatmap.getBeatmap(181)
    # Beatmap.getBeatmap(182)
    # Beatmap.getBeatmap(186)
    # Beatmap.getBeatmap(193)
    # Beatmap.getBeatmap(194)
    # Beatmap.getBeatmap(208)
    # Beatmap.getBeatmap(213)
    # Beatmap.getBeatmap(214)
    # session.save()

    b = Beatmap.get_beatmap(165)
    print(b)
    print(b.pps.filter(PP.mod==0).all())
