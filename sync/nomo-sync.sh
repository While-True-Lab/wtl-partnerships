#!/bin/bash
# Nomo Meeting Sync Script
# Pulls meetings from Nomo MCP and updates knowledge graph

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
NOMO_API_KEY="${NOMO_API_KEY:-$(grep NOMO_API_KEY ~/.bashrc 2>/dev/null | cut -d'"' -f2)}"
export NOMO_API_KEY

if [ -z "$NOMO_API_KEY" ]; then
    echo "Error: NOMO_API_KEY not found"
    exit 1
fi

echo "🔄 Syncing meetings from Nomo..."

# Get last sync timestamp
LAST_SYNC_FILE="$SCRIPT_DIR/last-sync.json"
if [ -f "$LAST_SYNC_FILE" ]; then
    LAST_SYNC=$(jq -r '.lastSync' "$LAST_SYNC_FILE" 2>/dev/null || echo "1970-01-01T00:00:00Z")
else
    LAST_SYNC="1970-01-01T00:00:00Z"
fi

echo "Last sync: $LAST_SYNC"

# Pull recent completed meetings
cd "$REPO_ROOT"
mcporter call nomomeet.list_meetings \
    status=completed \
    limit=50 \
    --config ~/clawd/config/mcporter.json \
    --output json > /tmp/nomo-meetings.json

# Process each meeting
MEETING_COUNT=$(jq '.meetings | length' /tmp/nomo-meetings.json)
NEW_MEETINGS=0
NEW_ENTITIES=0

echo "Found $MEETING_COUNT meetings"

for i in $(seq 0 $(($MEETING_COUNT - 1))); do
    MEETING=$(jq ".meetings[$i]" /tmp/nomo-meetings.json)
    MEETING_ID=$(echo "$MEETING" | jq -r '.id')
    MEETING_DATE=$(echo "$MEETING" | jq -r '.created_at' | cut -d'T' -f1)
    MEETING_TITLE=$(echo "$MEETING" | jq -r '.title')
    
    # Skip if already processed
    if [ -f "$REPO_ROOT/meetings/$MEETING_DATE/$MEETING_ID.md" ]; then
        continue
    fi
    
    echo "Processing: $MEETING_TITLE"
    
    # Get full meeting details
    mcporter call nomomeet.get_meeting \
        meeting_id="$MEETING_ID" \
        include_action_items=true \
        include_decisions=true \
        --config ~/clawd/config/mcporter.json \
        --output json > /tmp/meeting-detail.json
    
    # Create meeting file
    mkdir -p "$REPO_ROOT/meetings/$MEETING_DATE"
    
    # Extract and format meeting data
    python3 "$SCRIPT_DIR/extract-meeting.py" \
        /tmp/meeting-detail.json \
        "$REPO_ROOT/meetings/$MEETING_DATE/$MEETING_ID.md"
    
    ((NEW_MEETINGS++))
    
    # Update entities (people, companies)
    python3 "$SCRIPT_DIR/update-entities.py" \
        /tmp/meeting-detail.json \
        "$REPO_ROOT/entities/"
    
    # Update pipeline if deal mentioned
    python3 "$SCRIPT_DIR/update-pipeline.py" \
        /tmp/meeting-detail.json \
        "$REPO_ROOT/pipeline/"
done

# Update last sync timestamp
echo "{\"lastSync\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > "$LAST_SYNC_FILE"

echo "✅ Sync complete: $NEW_MEETINGS new meetings, $NEW_ENTITIES new entities"

# Auto-commit if changes exist
if [ "$NEW_MEETINGS" -gt 0 ]; then
    cd "$REPO_ROOT"
    git add meetings/ entities/ pipeline/ sync/
    git commit -m "Auto-sync: $(date +%Y-%m-%d) - $NEW_MEETINGS meetings" || true
    git push origin main || echo "Push failed - may need manual intervention"
fi