.PHONY: index lint search log

index:
	python3 tools/wiki.py index

lint:
	python3 tools/wiki.py lint

search:
	python3 tools/wiki.py search "$(q)"

log:
	python3 tools/wiki.py log "$(kind)" "$(title)" --body "$(body)"

feishu:
	python3 tools/feishu_sync.py fetch "$(url)" --title "$(title)"
