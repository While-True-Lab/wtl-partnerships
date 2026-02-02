#!/usr/bin/env python3
"""
Update entities from meeting data.
Extract people and companies mentioned in meetings.
"""
import json
import sys
import os
from datetime import datetime

def slugify(name):
    return name.lower().replace(' ', '-').replace('/', '-').replace('.', '')[:50]

def update_entities(input_file, entities_dir):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    meeting = data.get('meeting', {})
    attendees = data.get('attendees', [])
    
    meeting_title = meeting.get('title', '')
    meeting_date = meeting.get('created_at', '')[:10] if meeting.get('created_at') else datetime.now().strftime('%Y-%m-%d')
    
    people_dir = os.path.join(entities_dir, 'people')
    companies_dir = os.path.join(entities_dir, 'companies')
    
    os.makedirs(people_dir, exist_ok=True)
    os.makedirs(companies_dir, exist_ok=True)
    
    new_entities = 0
    
    # Extract people from attendees
    for attendee in attendees:
        name = attendee.get('name', '')
        if not name or name in ['Unknown', 'System']:
            continue
        
        slug = slugify(name)
        person_file = os.path.join(people_dir, f"{slug}.md")
        
        if not os.path.exists(person_file):
            # Create new person entity
            content = f"""---
id: auto-{slug}
name: {name}
company: unknown
role: Unknown
first_met: {meeting_date}
last_contact: {meeting_date}
tags: [auto-extracted]
---

# {name}

## Overview

Extracted from meeting: {meeting_title} ({meeting_date})

## Meeting History

- {meeting_date}: [[{slugify(meeting_title)}]]

## Notes

_Auto-generated entity. Please review and complete information._
"""
            with open(person_file, 'w') as f:
                f.write(content)
            new_entities += 1
            print(f"Created person: {person_file}")
        else:
            # Update existing person with meeting reference
            with open(person_file, 'r') as f:
                content = f.read()
            
            meeting_ref = f"- {meeting_date}: [[{slugify(meeting_title)}]]"
            if meeting_ref not in content:
                # Add to meeting history
                content = content.replace(
                    "## Meeting History",
                    f"## Meeting History\n\n{meeting_ref}"
                )
                # Update last contact
                content = content.replace(
                    f"last_contact: {content.split('last_contact: ')[1].split('\\n')[0] if 'last_contact:' in content else 'unknown'}",
                    f"last_contact: {meeting_date}"
                )
                with open(person_file, 'w') as f:
                    f.write(content)
                print(f"Updated person: {person_file}")
    
    return new_entities

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: update-entities.py <input.json> <entities_dir>")
        sys.exit(1)
    
    count = update_entities(sys.argv[1], sys.argv[2])
    print(f"Entities created/updated: {count}")
