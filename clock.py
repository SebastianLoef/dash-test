def clock_hands_angle(hour, min_, sec):
    """Func<on should output the angles in degrees,
    between the hands on an analog watch at <me hour:min:sec
    ordered from minimum to maximum.
    As example, input 8,30,0 should return
    75,105,180, as the angle between the hour and minute hand
    is 75 degrees, the angle between hour and second hand is
    105 degrees and the angle between the minute and second
    hand is 180 degrees.
    The input 0,0,0 should return, 0,0,360 as we require angles
    to form a full lap around the watch."""
    if hour == min_ == sec == 0:
        return 0, 0, 360
    hour %= 12
    sec_angle  = 6.  * sec
    min_angle  = 6.  * min_  + sec_angle / 60
    hour_angle = 30. * hour  + min_angle / 12

    # Calculate the absolute differences and ensure they are within 0 to 180 degrees
    sec_min_diff  = min(abs(sec_angle  - min_angle ), 360 - abs(sec_angle  - min_angle))
    min_hour_diff = min(abs(min_angle  - hour_angle), 360 - abs(min_angle  - hour_angle))
    hour_sec_diff = min(abs(hour_angle - sec_angle ), 360 - abs(hour_angle - sec_angle))

    minimum_angle, mid_angle, maximum_angle = sorted(
        [sec_min_diff, min_hour_diff, hour_sec_diff]
    )
    return minimum_angle, mid_angle, maximum_angle


if __name__ == "__main__":
    print(clock_hands_angle(8, 30, 0))
    print(clock_hands_angle(0, 0, 0))
