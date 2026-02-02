#!/usr/bin/env python3
"""
Update pipeline from meeting data.
Check for mentions of deals and update stage if needed.
"""
import json
import sys
import os
import re

def update_pipeline(input_file, pipeline_dir):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    meeting = data.get('meeting', {})
    transcript = data.get('transcript', {}).get('text', '')
    
    meeting_title = meeting.get('title', '')
    
    active_dir = os.path.join(pipeline_dir, 'active')
    closed_dir = os.path.join(pipeline_dir, 'closed')
    
    os.makedirs(active_dir, exist_ok=True)
    os.makedirs(closed_dir, exist_ok=True)
    
    # Check for deal mentions in meeting title or transcript
    # This is a simple keyword-based approach
    deal_keywords = {
        'trueva': 'trueva-dbs',
        'dbs': 'trueva-dbs',
        'astra': 'dearezt-astra',
        'dearezt': 'dearezt-astra',
        'cimb': 'cimb-1rm-vr',
        '1rm': 'cimb-1rm-vr',
        'talenta': 'talenta-integration',
        'mekari': 'talenta-integration',
        'humani': 'humani-santika-onboarding',
        'santika': 'humani-santika-onboarding',
        'dayalima': 'dayalima-bpjs-case-study',
        'bpjs': 'dayalima-bpjs-case-study',
    }
    
    mentioned_deals = set()
    text_to_check = (meeting_title + ' ' + transcript).lower()
    
    for keyword, deal_file in deal_keywords.items():
        if keyword in text_to_check:
            mentioned_deals.add(deal_file)
    
    for deal_file in mentioned_deals:
        # Check if deal exists in active or closed
        active_path = os.path.join(active_dir, f"{deal_file}.md")
        closed_path = os.path.join(closed_dir, f"{deal_file}.md")
        
        deal_path = active_path if os.path.exists(active_path) else closed_path if os.path.exists(closed_path) else None
        
        if deal_path and os.path.exists(deal_path):
            with open(deal_path, 'r') as f:
                content = f.read()
            
            # Add meeting reference if not already there
            meeting_date = meeting.get('created_at', '')[:10] if meeting.get('created_at') else 'unknown'
            meeting_slug = meeting_title.lower().replace(' ', '-').replace('/', '-')[:50]
            meeting_ref = f"- {meeting_date}: [[{meeting_slug}]]"
            
            if '## Meeting History' in content and meeting_ref not in content:
                content = content.replace(
                    '## Meeting History',
                    f'## Meeting History\n\n{meeting_ref}'
                )
                with open(deal_path, 'w') as f:
                    f.write(content)
                print(f"Updated deal: {deal_path}")
    
    return len(mentioned_deals)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: update-pipeline.py <input.json> <pipeline_dir>")
        sys.exit(1)
    
    count = update_pipeline(sys.argv[1], sys.argv[2])
    print(f"Deals updated: {count}")
