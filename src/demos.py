from __future__ import division
import logging
import threading

## Simple path demos for dynamic experiments.
def straight_fwd(speed, time):
    """
        straight_fwd: Drive straight forward for time.

            speed: Drive speed (m/s).
            time:  Drive time.

    """
    return [("fwd", speed, "no", None, time)]

def straight_rev(speed, time):
    """
        straight_rev: Drive straight reverse for time.

            speed: Drive speed (m/s).
            time:  Drive time.

    """
    return [("rev", speed, "no", None, time)]

def turn_fwd(speed, turn, radius, time):
    return [("fwd", speed, turn, radius, time)]
    """
        turn_fwd: Drive forward along circular arc for time.

            speed:  Drive speed (m/s, deg/s depending on radius).
            turn:   Direction of turn.
            radius: Turning radius.
            time:   Drive time.

    """

def turn_rev(speed, turn, radius, time):
    """
        turn_fwd: Drive reverse along circular arc for time.

            speed:  Drive speed (m/s, deg/s depending on radius).
            turn:   Direction of turn.
            radius: Turning radius.
            time:   Drive time.

    """
    return [("rev", speed, turn, radius, time)]

## Application path demos.
def square(speed, turn, length, turn_radius=0.528, corners=1):
    """
        square: Drive straight and make 90 deg corners.

            speed:        Drive speed (m/s).
            turn:         Direction of turn.
            length:       Square side length (m).
            turn_radius:  Corner radius (m).
            corners:      Number of corners to perform.

    """
    ang_speed = 30
    line = ("fwd", speed, "no", None, (length-2*turn_radius)/speed)
    corner = ("fwd", ang_speed, turn, turn_radius, 90/ang_speed)
    path = [line, corner]

    return path*corners

## LIDAR Demo
def __lidarStop(path, lidar, margin):
    logging.debug("lidarStop: LIDAR polling started")
    while True:
        distance = lidar.read()
        if distance < margin:
            logging.debug("lidarStop: stopping path")
            path.stop()
            return

def reactiveStop(path, lidar, speed, cutoffTime=10, margin=250):
    """
        reactiveStop: Drive straight until distance to obstacle achieved.

            path:       Path object.
            lidar:      LIDAR object.
            speed:      Drive speed (m/s).
            cutoffTime: Fail-safe cutoff time (s).
            margin:     Distance to obstacle at which to stop (cm).

    """
    t = threading.Thread(target=__lidarStop, args=(path, lidar, margin))
    t.start()
    return [("fwd", speed, "no", None, cutoffTime)]
