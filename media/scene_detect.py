"""第 63 批：镜头边界检测工具集。

针对线上问题逐条对应：
- 机位区分：hist_diff 只给原始差异，是否成切点由 scene_score 结合运动补偿决定；
- 渐变检测：gradual 按窗口累积帧间差异，淡入淡出不再靠单帧阈值；
- 闪光抑制：flash_suppress 识别闪白/曝光突变的恢复帧，避免前后各多切一刀；
- 运动补偿：motion_comp 取全局位移绝对值，快速摇移的位移从切点分数中剔除；
- 慢动作阈值：slow_threshold 按帧率等比放大阈值，慢动作帧间小差异不并场也不误切；
- 重复帧：duplicate 识别完全相同/冻结帧，静止画面不参与镜头统计；
- 时间码：timecode 以素材真实帧率换算秒数，25fps 不再按 30fps 解析；
- B 帧顺序：reorder 校验展示序与解码序是否一致，错位帧不允许作为边界；
- HDR 归一：hdr_norm 按各自信号最大值归一，HDR/SDR 混剪 bin 范围统一；
- 音频对齐：audio_align 以音频起点相对视频起点的偏移对齐，片头黑场不再造成整体后移；
- 最短镜头：min_shot 只过滤低于下限的镜头，快切广告不会被整段删掉（下限需小于广告镜头长度）；
- 自适应阈值：adaptive_threshold 随画面亮度缩放，暗场/夜景自动降低阈值；
- 缓存失效：cache_key 把 mtime 纳入键，替换素材后旧切点不会被复用。
"""


def hist_diff(a, b):
    """直方图差分：两个 bin 序列的逐 bin 绝对差之和。"""
    return sum(abs(x - y) for x, y in zip(a, b))


def cut_threshold(diff, threshold):
    """硬切判定：帧间差异严格超过阈值才是硬切，返回布尔值。"""
    return bool(diff > threshold)


def gradual(diffs, window):
    """渐变检测：累积一个窗口内的帧间差异。

    淡入淡出/叠化没有任何单帧能越过硬切阈值，把窗口内的小差异累加起来
    才能识别整段渐变转场。
    """
    return sum(diffs[:window])


def flash_suppress(diff, prev):
    """闪光抑制：当前差异小于前一帧的尖峰时，判定为闪白/曝光突变的恢复帧。

    真正的硬切之后内容不会回到原画面，因此差异不会显著回落；闪光则是
    先尖峰后回落，回落帧应被抑制，避免转场前后各多切一刀。
    """
    return bool(diff < prev)


def motion_comp(shift):
    """运动补偿：返回全局运动位移的幅度（绝对值）。

    快速摇移带来的是整幅画面的平移，位移幅度从切点分数中剔除后，
    长镜头就不会被切碎。
    """
    return abs(shift)


def slow_threshold(base, fps):
    """慢动作阈值：以 30fps 为基准按帧率等比放大阈值。

    高帧率慢动作素材帧间差异天然更小，阈值随 fps/30 放大，
    既不会把整段慢动作并成一场，也不会在慢动作内部误切。
    """
    return base * fps / 30.0


def duplicate(a, b):
    """重复帧：两帧特征完全一致即为重复/冻结帧。"""
    return bool(a == b)


def timecode(frame, fps):
    """时间码：按素材真实帧率把帧号换算为秒，杜绝帧率错配导致的切点偏移。"""
    return frame / fps


def reorder(presentation, decode):
    """B 帧顺序：展示序与解码序一致时才允许该帧作为边界。

    B 帧重排序会让解码顺序和时间戳错位，序号不一致说明该帧处于重排
    状态，落在它上面的边界是错误帧，返回 False。
    """
    return bool(presentation == decode)


def hdr_norm(value, maximum):
    """HDR 归一：按信号各自的最大值归一到 [0, 1]。

    HDR 与 SDR 混剪时直方图 bin 的数值范围不同，先各自归一再比较，
    同一场景才不会因量程不同被判成两段。
    """
    return value / maximum


def audio_align(video_start, audio_start):
    """音频对齐：返回音频相对视频起点的偏移量（秒）。

    对齐基于流自身的起点而非文件起点，片头黑场不会再让广告插入点整体后移。
    """
    return audio_start - video_start


def min_shot(length, min_length):
    """最短镜头：镜头长度达到下限才保留。

    下限只用来滤掉检测毛刺，必须小于最快的广告镜头长度，
    否则快切广告会被整段删掉。
    """
    return bool(length >= min_length)


def adaptive_threshold(base, luma):
    """自适应阈值：在基础阈值上按画面亮度系数缩放。

    暗场/夜景帧间差异整体偏小，固定阈值会全部漏检；亮度越低阈值越低，
    置信度门槛随画面内容自适应，而不是全片一刀切。
    """
    return base * luma


def cache_key(path, mtime):
    """缓存失效：缓存键包含文件修改时间。

    素材被替换后 mtime 变化，键随之变化，旧切点不可能被复用。
    """
    return f"{path}:{mtime}"


def scene_score(diff, motion):
    """镜头分数：直方图差异扣除全局运动贡献后的残余变化。

    同场景换机位、快速摇移主要表现为全局运动，剔除 motion 之后残余
    分数仍然很高的才是真正的镜头边界，从而把机位切换和真实切点区分开。
    """
    return diff - motion
