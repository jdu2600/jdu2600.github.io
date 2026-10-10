# jdu2600.github.io

Source for https://jdu2600.github.io/, a list of my talks, articles and projects.

- Content lives in `_data/entries.yml`; venue logos in `_data/venues.yml` and `assets/logos/`.
- Slide decks and article PDFs live in [conference_talks](https://github.com/jdu2600/conference_talks)
  and are served at `https://jdu2600.github.io/conference_talks/`.
- GitHub Pages builds the site with Jekyll on every push to `main`.

To preview locally (expects `conference_talks` checked out alongside this repo for the PDF links):

```
pip install python-liquid pyyaml
python _preview.py
```
