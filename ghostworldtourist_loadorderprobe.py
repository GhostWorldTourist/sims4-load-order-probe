"""Load Order Probe - logs which mod's copy of contested tuning the game kept.

Read-only diagnostic. Once tuning has loaded it writes, for a few resources that
several installed mods each ship a copy of, what the game actually holds, so
it can be matched against each mod's file. Logs to
Mods/GhostWorldTourist_LoadOrderProbe.log. Remove after one launch.

Author: GhostWorldTourist
"""
import os
import services
import sims4.resources

_LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    'GhostWorldTourist_LoadOrderProbe.log')


def _write(line):
    with open(_LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def _computer(manager):
    cls = manager.get(34682)
    if cls is None:
        _write('object_Computer_High: not loaded')
        return
    ids = sorted(a.guid64 for a in getattr(cls, '_super_affordances', ()) if a is not None)
    _write('object_Computer_High super_affordances %d: %s' % (len(ids), ' '.join(map(str, ids))))


def _swim(manager):
    cls = manager.get(2697192290)
    if cls is None:
        _write('chingyu_ActivityLotBG_BuffSwim: not loaded')
        return
    gem = getattr(cls, 'game_effect_modifier', None)
    for m in getattr(gem, '_game_effect_modifiers', ()):
        _write('BuffSwim modifier %s: %r' % (type(m).__name__,
               {k: v for k, v in vars(m).items() if 'score' in k or 'static' in k}))


def _guard(fn):
    def run(manager):
        try:
            fn(manager)
        except Exception as e:
            _write('%s failed: %r' % (fn.__name__, e))
    return run


try:
    open(_LOG, 'w').close()
    services.get_instance_manager(sims4.resources.Types.OBJECT).add_on_load_complete(_guard(_computer))
    services.get_instance_manager(sims4.resources.Types.BUFF).add_on_load_complete(_guard(_swim))
    _write('probe registered')
except Exception as e:
    _write('probe failed to register: %r' % (e,))
