PY ?= python3
export PYTHONPATH := src
export TZ := Asia/Hong_Kong

.PHONY: install smoke funds news news-prep weekly-build scorecard check-digest maintenance test brief brief-images

install:      ; $(PY) -m pip install -r requirements.txt
smoke:        ; $(PY) -m cfa.smoke_test
funds:        ; $(PY) -m cfa.collect_funds
news:         ; $(PY) -m cfa.collect_news
news-prep:    ; $(PY) -m cfa.news_prep
weekly-build: ; $(PY) -m cfa.weekly_build
scorecard:    ; $(PY) -m cfa.scorecard
check-digest: ; $(PY) -m cfa.check_digest
maintenance:  ; $(PY) -m cfa.maintenance
test:         ; $(PY) -m pytest -q tests
brief:        ; $(PY) -m cfa.brief $(T)    # make brief T=news|morning|weekly|themes
brief-images: ; $(PY) -m cfa.brief_images  # needs playwright + chromium; Actions runs it
