#!/bin/bash
# Setup cron job for daily partnership sync
# Run this manually to install the cron job

CRON_LINE="0 6 * * * cd ~/repos/wtl-partnerships && ./sync/nomo-sync.sh >> ~/repos/wtl-partnerships/sync/sync.log 2>&1"

# Add to crontab if not already present
(crontab -l 2>/dev/null | grep -v "nomo-sync.sh"; echo "$CRON_LINE") | crontab -

echo "Cron job installed. Daily sync at 6:00 AM."
echo "Current crontab:"
crontab -l | grep nomo-sync
