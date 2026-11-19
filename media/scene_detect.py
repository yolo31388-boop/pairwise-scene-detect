"""第 63 批：同一场戏切了三个机位，检测把每个机位切换都当成广告，慢动作片段整..."""

def hist_diff(a, b):
    """直方图差分。"""
    raise NotImplementedError("TODO: hist_diff")

def cut_threshold(diff, threshold):
    """硬切判定。"""
    raise NotImplementedError("TODO: cut_threshold")

def gradual(diffs, window):
    """渐变检测。"""
    raise NotImplementedError("TODO: gradual")

def flash_suppress(diff, prev):
    """闪光抑制。"""
    raise NotImplementedError("TODO: flash_suppress")

def motion_comp(shift):
    """运动补偿。"""
    raise NotImplementedError("TODO: motion_comp")

def slow_threshold(base, fps):
    """慢动作阈值。"""
    raise NotImplementedError("TODO: slow_threshold")

def duplicate(a, b):
    """重复帧。"""
    raise NotImplementedError("TODO: duplicate")

def timecode(frame, fps):
    """时间码。"""
    raise NotImplementedError("TODO: timecode")

def reorder(presentation, decode):
    """B 帧顺序。"""
    raise NotImplementedError("TODO: reorder")

def hdr_norm(value, maximum):
    """HDR 归一。"""
    raise NotImplementedError("TODO: hdr_norm")

def audio_align(video_start, audio_start):
    """音频对齐。"""
    raise NotImplementedError("TODO: audio_align")

def min_shot(length, min_length):
    """最短镜头。"""
    raise NotImplementedError("TODO: min_shot")

def adaptive_threshold(base, luma):
    """自适应阈值。"""
    raise NotImplementedError("TODO: adaptive_threshold")

def cache_key(path, mtime):
    """缓存失效。"""
    raise NotImplementedError("TODO: cache_key")

def scene_score(diff, motion):
    """镜头分数。"""
    raise NotImplementedError("TODO: scene_score")
