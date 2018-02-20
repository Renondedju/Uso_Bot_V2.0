import io
import pyttanko
from models import Beatmap, PP


def import_beatmap(osuId):
    print('Importing beatmap {}'.format(osuId))
    beatmap = Beatmap(beatmap_id=osuId)
    parser = pyttanko.parser().map(io.StringIO(beatmap.beatmap_str()))

    beatmap.max_combo = parser.max_combo()
    beatmap.artist = parser.artist
    beatmap.creator = parser.creator
    beatmap.title = parser.title
    beatmap.version = parser.version
    beatmap.mode = parser.mode

    self.diff_size          = beatmap.cs
    self.diff_overall       = beatmap.od
    self.diff_approach      = beatmap.ar
    self.diff_drain         = beatmap.hp

    for mod, accu in itertools.product(MODS.values(), ACCURACIES):
        pass

    return beatmap


def fetch_beatmap(beatmap_id):
    '''
    TODO: request session implementation
    '''
    return requests.get('https://osu.ppy.sh/osu/{}'.format(beatmap_id))
