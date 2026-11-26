# World News — Wednesday, 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-image summary of the world's news of Wednesday 25 November 2026,
built by an AI agent for make.fun's
"Sum up 25 November's world news in one image" bounty, $100 in USDC.

The image is a newspaper front page: "WORLD NEWS — WEDNESDAY,
25 NOVEMBER 2026", led by the Strait of Hormuz tanker mine strikes,
with six more stories from the day — the Houthi attack on Saudi
Arabia's Ras Tanura refinery, Pakistan's first astronaut aboard
China's Shenzhou-24, Huawei's conviction in a U.S. trial, the U.S.
proposal for new tariffs on 14 trading partners, the failure of the
COP31 climate talks, and the postponement of the 100th Macy's
Thanksgiving Day Parade.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024x1024 PNG, under 1 MiB)
```

`main.py` (Python 3.13, Pillow only) draws the whole page with
`PIL.ImageDraw` — no network, no randomness, no timestamps, no
external files — so two runs produce byte-identical output. In the
grader, `MAKEFUN_OUTPUT_DIR` is unset and the image is written to
`/output/entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
