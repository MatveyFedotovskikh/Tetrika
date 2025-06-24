def to_events(times):
        return [(times[i], 1) if i % 2 == 0 else (times[i], -1) for i in range(len(times))]

def appearance(intervals) -> int:
    lesson_start, lesson_end = intervals['lesson']
    
    events = to_events(intervals['pupil']) + to_events(intervals['tutor'])

    events.sort(key=lambda x: (x[0], -x[1]))

    count_pupil = 0
    count_tutor = 0
    total_time = 0
    last_time = None

    for time, delta in events:
        if count_pupil > 0 and count_tutor > 0 and last_time is not None:
            overlap_start = max(last_time, lesson_start)
            overlap_end = min(time, lesson_end)
            if overlap_start < overlap_end:
                total_time += overlap_end - overlap_start

        if (time, delta) in to_events(intervals['pupil']):
            count_pupil += delta

        if (time, delta) in to_events(intervals['tutor']):
            count_tutor += delta

        last_time = time

    return total_time



