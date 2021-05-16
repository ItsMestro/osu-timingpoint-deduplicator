# osu! Timingpoint De-Duplicator

This is a tool meant to help modders and mappers of sv maps, find unnecessary duplicate timings. I have provided a .exe version of the script in the [releases](https://github.com/ItsMestro/osu-timingpoint-deduplicator/releases) section.

## Usage

Place the script in a folder alongside a set of .osu files and run it.
Output will be written to text files in the same folder using the same name as the .osu

## Example Output

This example was generated using the .osu file provided under the [releases](https://github.com/ItsMestro/osu-timingpoint-deduplicator/releases).

```text
[DUPLICATE TIMING]
These timings have multiple points on top of each other.

20054
22361
39669


[DUPLICATE VELOCITY]
Each one of these sets follow each other in the map and use the same velocity.

23610 | 23611
23800 | 23804
44957 | 44968
56592 | 56662
61159 | 61168
```
