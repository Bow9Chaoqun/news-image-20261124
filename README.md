# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Bow9Chaoqun/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Bow9Chaoqun/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A single picture of Tuesday 24 November 2026, set as a newspaper front page and drawn entirely in code.

The lead story is NATO promising a joint defence of orbit after German reporting that Russia is preparing a satellite that could destroy other satellites. Below it sit four more of the day's stories: Jensen Huang back as Nvidia's chief executive after pressure from Trump, President Zelensky asking for four-way talks with Russia as soon as possible, drones striking homes and a United Nations building in Khartoum, and California congressman Gomez resigning after ethics findings. A black ticker along the foot of the page carries three shorter items from the same day.

## Running the entry

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This places the picture at `out/entry.png`. With no environment variable set — as in the grader — the destination is `/output/entry.png`.

## Rebuilding the picture

`build_image.py` is the drawing program. It lays the page out at double size, measures each block of text before painting it so nothing spills out of its panel, adds a small hand-drawn pictogram to every story, and then reduces the page to 1024 × 1024. It needs Pillow and the Liberation fonts. The graded program above, by contrast, uses only the Python standard library.

```sh
python3 build_image.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=6sysfxgd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
