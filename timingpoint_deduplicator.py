import codecs
import logging
import os

"""A simple script to check osu beatmaps for duplicate timing points.
It tests for multiple timing points at the same offset as well as same velocity after eachother.

To use it, simply place the script alongside a set of .osu files and run it.
Results are written to .txt files with the same name as the .osu"""


def filereader():
    """Find files in current directory that should be parsed."""
    return [i for i in os.listdir(".") if i[-4:] == ".osu"]


def parse_beatmap(bmap):
    """Make the magic happen."""
    with codecs.open(bmap, "r", "utf-8") as beatmap:
        map_lines = beatmap.readlines()

    try:  # Unicode isn't fun
        for i, line in enumerate(map_lines):
            map_lines[i] = line.decode()
    except AttributeError:  # Already decoded
        pass

    # We remove the metadata before the timing point section of the file
    mapobjects = []
    for i, line in enumerate(map_lines):
        if line.startswith("[TimingPoints]"):
            mapobjects = map_lines[i + 1 :]
            break

    if not mapobjects:
        return errorlogging(40, f"Unable to find [TimingPoints] in {bmap}")

    # We clear out the hitobjects which come after timings
    timings = []
    for i, line in enumerate(mapobjects):
        if line.startswith("[HitObjects]"):
            timings = mapobjects[: i - 1]
            break

    if not timings:
        return errorlogging(30, f"{bmap} seems to not be a valid map file.")

    # Check and skip empty lines while splitting each timings data
    points = []
    for timingpoint in timings:
        if timingpoint == "\r\n":
            continue
        data = timingpoint.split(",", 7)
        if int(data[6]) == 0: # Only care about inherited timing points
            points.append([data[0], data[1]])

    if not points:
        return

    points = sorted(points) # Because the list can get unorganized by manually editing the .osu

    timeoutput = []
    velocityoutput = []
    for i, line in enumerate(points):
        if i == 0: # First object cant compare with anything
            continue

        if line[0] == points[i - 1][0]: # If two timing points are at the same ms offset
            timeoutput.append(i)
        elif line[1] == points[i - 1][1]: # If the velocity of the last timing point and current one is the same
            velocityoutput.append(i)

    # Wanted to just return at first but user could be confused why nothing happened
    if not timeoutput or not velocityoutput:
        with open(f"{bmap[:-4]}.txt", "w+") as f:
            f.write(f"{bmap} has no issues.")
        return

    # Write the result to a .txt
    with open(f"{bmap[:-4]}.txt", "w+") as f:
        if timeoutput:
            f.write(
                "[DUPLICATE TIMING]\nThese timings have multiple points on top of each other.\n\n"
            )
            for o in timeoutput:
                f.write(f"{points[o - 1][0]}\n")

            if velocityoutput:
                f.write("\n\n")

        if velocityoutput:
            f.write(
                "[DUPLICATE VELOCITY]\nEach one of these sets follow each other in the map and use the same velocity.\n\n"
            )
            for o in velocityoutput:
                f.write(f"{points[o - 1][0]} | {points[o][0]}\n")


def errorlogging(level, output):
    """if error: log"""
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="errors.log",
    )  # Got no better idea for user interfacing

    logging.log(level, output)


def main():
    """Run our code."""
    if osufiles := filereader():
        for file in osufiles:
            parse_beatmap(file)
    else:
        errorlogging(20, "Found no .osu files in the current directory.")


if __name__ == "__main__":
    main()
