# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Bow9Chaoqun/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Bow9Chaoqun/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image that sums up the world news of Tuesday 24 November 2026, drawn in code as a newspaper front page: NATO vowing a space defence after reports that Russia is readying a nuclear satellite, Nvidia bringing back Jensen Huang as CEO after a push from Trump, Zelensky calling for four-way talks with Russia, drone strikes on homes and a UN building in Khartoum, and a US congressman resigning after ethics findings — with the day's smaller stories in the ticker along the bottom.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes the entry image to `out/entry.png`. In the grader's sandbox
`main.py` runs with no `MAKEFUN_OUTPUT_DIR` set and writes `/output/entry.png`.

## How the image is made

`build_image.py` draws the front page with Pillow — masthead, five story
panels with hand-drawn icons, and the ticker — measuring every text block
before drawing it so nothing overflows, then downsamples from 2x for clean
edges. It needs Pillow and the Liberation fonts, and is only used to build
`entry.png`; the entry itself (`main.py`) is standard library only.

```sh
python3 build_image.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=6sysfxgd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
