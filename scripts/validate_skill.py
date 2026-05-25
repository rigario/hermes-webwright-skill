#!/usr/bin/env python3
"""Validate the packaged Hermes Webwright skill."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/dogfood/webwright/SKILL.md'
MAX_DESCRIPTION = 1024
MAX_CONTENT = 100_000
REQUIRED_SECTIONS = [
    '## Overview',
    '## When to Use',
    '## Decision Ladder',
    '## Workflow',
    '## Common Pitfalls',
    '## Verification Checklist',
]


def main() -> None:
    content = SKILL.read_text()
    assert content.startswith('---'), 'SKILL.md must start with YAML frontmatter at byte 0'
    match = re.search(r'\n---\s*\n', content[3:])
    assert match, 'SKILL.md must close YAML frontmatter with ---'
    frontmatter = yaml.safe_load(content[3:3 + match.start()])
    assert isinstance(frontmatter, dict), 'frontmatter must be a YAML mapping'
    assert frontmatter.get('name') == 'webwright', 'name must be webwright'
    description = frontmatter.get('description') or ''
    assert description.startswith('Use when '), 'description should start with "Use when"'
    assert len(description) <= MAX_DESCRIPTION, 'description too long'
    for key in ['version', 'author', 'license', 'metadata']:
        assert key in frontmatter, f'missing frontmatter key: {key}'
    assert len(content) <= MAX_CONTENT, 'SKILL.md exceeds content limit'
    body = content[3 + match.end():]
    assert body.strip(), 'body must be non-empty'
    for section in REQUIRED_SECTIONS:
        assert section in content, f'missing required section: {section}'
    print('Skill validation passed')
    print(f'Path: {SKILL}')
    print(f'Chars: {len(content)}')
    print(f'Description chars: {len(description)}')


if __name__ == '__main__':
    main()
