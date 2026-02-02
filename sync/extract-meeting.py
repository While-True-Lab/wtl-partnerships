#!/usr/bin/env python3
"""
Extract meeting data from Nomo MCP response and create markdown file.
"""
import json
import sys
from datetime import datetime

def extract_meeting(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    meeting = data.get('meeting', {})
    action_items = data.get('action_items', [])
    decisions = data.get('decisions', [])
    attendees = data.get('attendees', [])
    
    meeting_id = meeting.get('id', '')
    title = meeting.get('title', 'Untitled Meeting')
    date = meeting.get('created_at', '')[:10] if meeting.get('created_at') else datetime.now().strftime('%Y-%m-%d')
    duration = meeting.get('duration_minutes', 0)
    
    # Create filename-friendly slug
    slug = title.lower().replace(' ', '-').replace('/', '-')[:50]
    
    content = f"""---
id: {meeting_id}
title: {title}
date: {date}
duration: {duration} minutes
source: nomo
---

# {title}

**Date:** {date}  
**Duration:** {duration} minutes  
**ID:** {meeting_id}

---

## Attendees

"""
    
    for attendee in attendees:
        name = attendee.get('name', 'Unknown')
        role = attendee.get('role', 'participant')
        content += f"- **{name}** ({role})\n"
    
    content += "\n---\n\n## Decisions\n\n"
    
    if decisions:
        for decision in decisions:
            d_text = decision.get('decision', '')
            d_maker = decision.get('decision_maker_name', 'Unknown')
            d_status = decision.get('status', '')
            d_impact = decision.get('impact_level', '')
            content += f"- **{d_text}**\n"
            content += f"  - Decision maker: {d_maker}\n"
            content += f"  - Status: {d_status}\n"
            if d_impact:
                content += f"  - Impact: {d_impact}\n"
            content += "\n"
    else:
        content += "_No decisions recorded_\n"
    
    content += "\n---\n\n## Action Items\n\n"
    
    if action_items:
        for item in action_items:
            title_item = item.get('title', '')
            assignee = item.get('assignee_name', 'Unassigned')
            status = item.get('status', '')
            priority = item.get('priority', '')
            content += f"- [ ] **{title_item}**\n"
            content += f"  - Assignee: {assignee}\n"
            content += f"  - Status: {status}\n"
            if priority:
                content += f"  - Priority: {priority}\n"
            content += "\n"
    else:
        content += "_No action items recorded_\n"
    
    content += f"\n---\n\n*Auto-generated from Nomo MCP | {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    print(f"Created: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: extract-meeting.py <input.json> <output.md>")
        sys.exit(1)
    
    extract_meeting(sys.argv[1], sys.argv[2])
