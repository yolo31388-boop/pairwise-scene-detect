import pytest
from media import scene_detect as mod

CASES = [
    ("diff", 'm.hist_diff([1, 2], [2, 2]) == 1'),
    ("cut", 'm.cut_threshold(0.5, 0.3) is True'),
    ("gradual", 'm.gradual([0.1, 0.1, 0.1], 3) == approx(0.3)'),
    ("flash", 'm.flash_suppress(0.5, 0.9) is True'),
    ("motion", 'm.motion_comp(-2) == 2'),
    ("slow", 'm.slow_threshold(0.5, 60) == approx(1.0)'),
    ("duplicate", 'm.duplicate(1, 1) is True'),
    ("timecode", 'm.timecode(60, 30) == approx(2.0)'),
    ("reorder", 'm.reorder(5, 3) is False'),
    ("hdr", 'm.hdr_norm(5, 10) == approx(0.5)'),
    ("align", 'm.audio_align(1, 4) == 3'),
    ("min", 'm.min_shot(5, 3) is True'),
    ("adaptive", 'm.adaptive_threshold(0.5, 2) == approx(1.0)'),
    ("cache", 'm.cache_key("p", 1) == "p:1"'),
    ("score", 'm.scene_score(2, 1) == approx(1.0)')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
