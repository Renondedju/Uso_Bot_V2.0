import sqlalchemy
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

from .database import Base, session


class Beatmap(Base):
    id = Column(Integer, Sequence('beatmap_id_seq'), primary_key=True)
    beatmap_id = Column(Integer)
    beatmapset_id = Column(Integer)

    beatmap_str = Column(String(50))

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
        back_populates="beatmap",
        cascade="save-update, merge, delete, delete-orphan")

    @classmethod
    def getBeatmap(cls, osuId: int, accuracy=None: int, mods=None: str):
        '''
        get or import beatmap by osuId
        TODO: implement prefetch for pps by accuracy and mods
        '''
        beatmap = session \
            .query(cls) \
            .filter(beatmap_id=osuId) \
            .one_or_none()
        return beatmap or import_beatmap(osuId)

    def __str__(self):
        return "{title}[{version}]".format(title=self.title, version=self.version)


class PP(Base):
    id = Column(Integer, Sequence('pp_id_seq'), primary_key=True)
    accuracy = Column(Integer)
    mod = Column(String(6))
    pps = Column(Integer)
    beatmap_id = Column(Integer, ForeignKey('beatmaps.id'))

    beatmap = relationship("Beatmap", back_populates="pps")

    def __str__(self):
        return "{pps} in {mod}".format(pps=self.pps, mod=self.mod)
