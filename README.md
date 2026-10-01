# Khalid's Treasure Hunt

A children's treasure-hunt game set inside a 3D village house — and the house plan it was built from.
Walk through the rooms, the verandah and the yard with Khalid and his dog Bhulu, and find his favourite
things before the clock runs away with your points. Plays in any browser, in **English and Bengali**, and
ships as a small offline Android app.

**By Md. Khalid Hasan Milu** — Department of Agroforestry and Environment, Gazipur Agricultural University.

## Play it

- **Browser:** https://milukhalidhasan.github.io/khalids-hunt/ (or open `index.html`)
- **Android:** install [`releases/Khalids-Hunt.apk`](releases/Khalids-Hunt.apk) — 229 KB, plays completely offline.

### Controls

| | Keyboard | Touch |
|---|---|---|
| Walk | W A S D or arrow keys (Shift = slowly) | Joystick — push further to run |
| Turn | Q / E, or drag | Drag |
| Pick a thing up | Click it | Tap it |
| Hint | H (costs 40 points) | The bulb button |
| Pause | Esc | Pause button |

Each find is worth 100–200 points plus up to 135 for speed. Pick up the wrong thing and Bhulu barks.
Best score is saved on the device, and the language button switches between English and বাংলা.

## The house plan

The game is built on a real floor plan: a one-storey village house, 35 × 37 ft, front facing west, four
bedrooms in the four corners. It started as a hand-drawn sketch and became a measured plan.

| File | What it is |
|---|---|
| [`house-sketch-original.jpeg`](house-sketch-original.jpeg) | the original hand-drawn sketch |
| [`plan-review-notes.md`](plan-review-notes.md) | what the sketch did well, what changed and why |
| [`village-house-plan.html`](village-house-plan.html) / [`-bn`](village-house-plan-bn.html) | the full plan page, English and Bengali |
| `village-house-plan.pdf` / `-bn.pdf` | the same, for printing |
| `village-house-plan-drawing.png` / `-bn.png` | just the floor-plan drawing, for sharing |
| [`village-house-3d.html`](village-house-3d.html) | the 3D model of the house you can walk around |

## How it is built

No game engine and no build system — three.js plus two Python scripts that write the pages.

```
index.html              the game (generated: do not edit by hand)
source/
  gen_plan.py           draws the floor plan in inches and writes the plan pages, English + Bengali
  make_game.py          takes the 3D house from artifact-3d.html and builds the game on top of it
  artifact-*.html       pages meant for embedding
  lib/                  three.js r128, OrbitControls, BufferGeometryUtils (MIT)
  android/              the Android app: manifest, WebView activity, build_apk.py
releases/               the signed APK
```

Rebuild after changing `make_game.py`:

```bash
python source/make_game.py
```

It rewrites `index.html` (three.js from a CDN) and `source/android/assets/index.html` (three.js built in,
so the app works offline). Then rebuild the app:

```bash
python source/android/build_apk.py
```

That needs the Android SDK from Android Studio — no Gradle. It writes `releases/Khalids-Hunt.apk`.

### The signing key

`source/android/rafi-hunt.keystore` signs the app. It is **not** in this repository (`.gitignore` keeps it
out) and must stay private — anyone holding it can publish updates as this app. Back it up; without it you
cannot update an installed app under the same key. Its password lives next to it in
`source/android/keystore-password.txt`, which is ignored by git as well - back up both together. On a machine
that has neither, the build script generates a fresh key and password and tells you where it put them; you
can also pass the password in the `HUNT_KEYSTORE_PASS` environment variable.

The Android package id is still `com.milu.rafihunt`, from the game's first version, so that existing
installs keep updating normally.

## Credits and license

Game, plan and code: © 2026 Md. Khalid Hasan Milu — [MIT license](LICENSE).
[three.js](https://threejs.org/) r128 (`source/lib/`) is MIT. The game loads the *Baloo Da 2* and
*Hind Siliguri* fonts from Google Fonts, which are under the SIL Open Font License.

Contact: khalid.official.98@gmail.com
