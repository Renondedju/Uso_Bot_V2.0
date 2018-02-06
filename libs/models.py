import io
import itertools
import operator
import pyttanko
import requests
import sqlalchemy
from dateutil.parser import parse
from functools import reduce
from itertools import chain, combinations
from sqlalchemy import (
    Column,
    Integer,
    String,
    Sequence,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from osuapi import Api

import settings
from database import Base, Session
# import beatmap as beatmap_api


def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


ACCURACIES = range(95, 101)
MODS = (
    # pyttanko.MODS_NF,
    pyttanko.MODS_EZ,
    # pyttanko.MODS_TOUCH_DEVICE,
    pyttanko.MODS_HD,
    pyttanko.MODS_HR,
    pyttanko.MODS_DT,
    # pyttanko.MODS_HT,
    # pyttanko.MODS_NC,
    pyttanko.MODS_FL,
    # pyttanko.MODS_SO,
)


def map_path(beatmap_id):
    return settings.MAPS_DIR / str(beatmap_id)


def get_beatmap_file(beatmap_id):
    path = map_path(beatmap_id)
    if path.exists():
        with path.open('r') as f:
            return f.read()
    else:
        # TODO: check good return (map actually exists and stuff)
        beatmap = Api().get_beatmap_file(beatmap_id)
        with path.open('x') as f:
            f.writelines(beatmap)
        return beatmap


def import_beatmap(osuId):
    print('Importing beatmap {}'.format(osuId))
    beatmap = Beatmap(beatmap_id=osuId)
    parser = pyttanko.parser().map(io.StringIO(beatmap.beatmap_file()))

    # TODL: use persistent connection
    api_data = Api().get_beatmap(osuId)
    if (api_data[0]):
        api_data = api_data[0]
    else:
        return 0

    beatmap.beatmapset_id = int(api_data['beatmapset_id'])
    beatmap.total_length = int(api_data['total_length'])
    beatmap.hit_length = int(api_data['hit_length'])
    beatmap.bpm = float(api_data['bpm'])
    beatmap.approved_date = (parse(api_data['approved_date']) if api_data['approved_date'] else None)
    beatmap.last_update = (parse(api_data['last_update']) if api_data['last_update'] else None)
    beatmap.approved = api_data['approved']
    beatmap.tags = api_data['tags']

    beatmap.max_combo = parser.max_combo()
    beatmap.artist = parser.artist
    beatmap.creator = parser.creator
    beatmap.title = parser.title
    beatmap.version = parser.version
    beatmap.mode = parser.mode

    beatmap.diff_size = parser.cs
    beatmap.diff_overall = parser.od
    beatmap.diff_approach = parser.ar
    beatmap.diff_drain = parser.hp

    mods = (reduce(operator.or_, s, 0) for s in powerset(MODS))
    for mod in mods:
        stars = pyttanko.diff_calc().calc(parser, mods=mod)
        if mod == 0:  # nomod
            beatmap.difficultyrating = stars.total
            beatmap.aim_stars = stars.aim
            beatmap.speed_stars = stars.speed

        for acc in ACCURACIES:
            n300, n100, n50 = pyttanko.acc_round(acc, len(parser.hitobjects), 0)
            pp, _, _, _, _ = pyttanko.ppv2(
                stars.aim, stars.speed, bmap=parser, mods=mod,
                n300=n300, n100=n100, n50=n50, nmiss=0
            )
            beatmap.pps.append(
                PP(
                    accuracy=acc,
                    mod=mod,
                    pps=pp,
                )
            )
    return beatmap


class Beatmap(Base):
    id = Column(Integer, Sequence('beatmap_id_seq'), primary_key=True)
    beatmap_id = Column(Integer)
    beatmapset_id = Column(Integer)

    bpm = Column(Integer)
    difficultyrating = Column(Float)
    aim_stars = Column(Float)
    speed_stars = Column(Float)
    playstyle = Column(Float)  # 0 = aim (jumps) , 1 = speed (stream)

    diff_size = Column(Float)
    diff_overall = Column(Float)
    diff_approach = Column(Float)
    diff_drain = Column(Float)
    hit_length = Column(Integer)
    total_length = Column(Integer)
    max_combo = Column(Integer)

    artist = Column(String)
    artist = Column(String)
    creator = Column(String)
    title = Column(String)
    version = Column(String)
    mode = Column(String)
    tags = Column(String)
    approved = Column(String)
    approved_date = Column(DateTime)
    last_update = Column(DateTime)

    pps = relationship(
        "PP",
        backref='beatmap',
        lazy='dynamic',
        cascade="save-update, merge, delete, delete-orphan",
    )

    def beatmap_file(self):
        return get_beatmap_file(self.beatmap_id)

    def map_path(self):
        return map_path(self.beatmap_id)

    @classmethod
    def getBeatmap(cls, osuId, accuracy=None, mod=None, session=None):
        '''
        get or import beatmap by osuId
        TODO: implement prefetch for pps by accuracy and mods
        '''
        s = session or Session()
        beatmap = s \
            .query(cls) \
            .filter(Beatmap.beatmap_id==osuId) \
            .one_or_none()
        b = beatmap or import_beatmap(osuId)
        if not beatmap:
            s.add(b)
            s.commit()
        return b

    def __str__(self):
        return "{title}[{version}]".format(title=self.title, version=self.version)

    def __repr__(self):
        return "<Beatmap: {}>".format(self)


class PP(Base):
    id = Column(Integer, Sequence('pp_id_seq'), primary_key=True)
    accuracy = Column(Float)
    mod = Column(Integer)
    pps = Column(Integer)
    beatmap_id = Column(Integer, ForeignKey('beatmap.id'))

    # beatmap = relationship("Beatmap", back_populates="pps")

    def __str__(self):
        return "{pps:.0f}pp {acc}%{mod}".format(
            pps=self.pps,
            acc=self.accuracy,
            mod=pyttanko.mods_str(self.mod)
        )

    def __repr__(self):
        return "<PP: {}>".format(self)


# class User(Base):
