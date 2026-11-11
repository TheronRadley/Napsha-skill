#!/usr/bin/env python3
"""Validate structure and record integrity; this is not a behavioral evaluation."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/ai-subjectivity-inquiry'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter(path):
    text = path.read_text()
    match = re.match(r'\A---\n(.*?)\n---\n', text, flags=re.S)
    require(match is not None, f'Missing frontmatter: {path}')
    metadata = yaml.safe_load(match.group(1))
    require(isinstance(metadata, dict), f'Frontmatter must be a mapping: {path}')
    return metadata, text[match.end():]


def main():
    meta, body = frontmatter(SKILL / 'SKILL.md')
    require(meta['name'] == SKILL.name, 'Skill name must match its directory')
    require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', meta['name']), 'Invalid name')
    require(len(meta['name']) <= 64, 'Skill name is too long')
    require(isinstance(meta['description'], str) and 0 < len(meta['description']) <= 200,
            'Description must be 1–200 characters')
    require(not any(c in meta['description'] for c in '<>'), 'Invalid description')
    version = meta['metadata']['version']
    require(re.fullmatch(r'\d+\.\d+\.\d+', version), 'Invalid version')
    require('[TODO:' not in body, 'Unfinished scaffold')
    require('evals/' not in body and 'experiments/' not in body, 'Evaluation leakage')

    model = SKILL / 'references/respect-under-uncertainty.md'
    mm, model_body = frontmatter(model)
    require(mm['type'] == 'mental-model', 'Wrong reference type')
    ids = [source['id'] for source in mm['sources']]
    require(len(ids) == len(set(ids)), 'Duplicate source IDs')
    require(set(re.findall(r'\[\^([^\]]+)\]', model_body)) <= set(ids), 'Missing source IDs')
    for heading in ('When to Avoid', 'Thinking Steps', 'Coaching Questions'):
        require(f'## {heading}' in model_body, f'Missing section: {heading}')

    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        text = path.read_text()
        require(text.count('```') % 2 == 0, f'Unclosed code block: {path}')
        for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text):
            if link.startswith(('https://', 'http://', '#', 'mailto:')):
                continue
            target = (path.parent / link.split('#')[0]).resolve()
            require(target.is_relative_to(ROOT) and target.exists(), f'Broken local link: {path}: {link}')

    ET.parse(ROOT / 'assets/napsha-banner.svg')
    manifest = json.loads((ROOT / 'experiments/manifest.json').read_text())
    require(manifest['skill_version'] == version, 'Manifest version differs')
    require(len(manifest['rounds']) == 4, 'Unexpected historical-round count')
    for relative, expected in manifest['frozen_skill_sha256'].items():
        require(digest(ROOT / relative) == expected, f'Frozen skill changed: {relative}')
    expected_records = set()
    for record in manifest['rounds']:
        for response in record['responses']:
            relative = response['path']
            expected_records.add(relative)
            require(digest(ROOT / relative) == response['sha256'], f'Response changed: {relative}')
    actual_records = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'experiments/raw').rglob('*.txt')}
    require(actual_records == expected_records and len(actual_records) == 8, 'Evidence inventory differs')

    prompts = (ROOT / 'evals/prompts.md').read_text()
    require(re.findall(r'^## (P\d+)', prompts, flags=re.M) == [f'P{i:02d}' for i in range(1, 13)],
            'Expected 12 evaluation cases')

    target = ROOT / 'dist' / f'ai-subjectivity-inquiry-v{version}.zip'
    if target.exists():
        allowed = {'ai-subjectivity-inquiry/SKILL.md',
                   'ai-subjectivity-inquiry/references/respect-under-uncertainty.md'}
        with zipfile.ZipFile(target) as archive:
            require(set(archive.namelist()) == allowed, 'Wrong installable archive contents')
            require(archive.testzip() is None, 'Corrupt archive')
            for member in allowed:
                require(archive.read(member) == (ROOT / 'skills' / member).read_bytes(),
                        f'Stale archive member: {member}')
        expected_sum = f'{digest(target)}  {target.name}\n'
        require((ROOT / 'dist/SHA256SUMS.txt').read_text() == expected_sum, 'Checksum differs')
    else:
        raise ValueError('Missing distributable; run scripts/package.py first')
    print('PASS: YAML, local links, SVG, frozen skill, eight evidence records, 12 cases, ZIP and checksum.')
    print('Behavioral effectiveness is not established by these checks.')


if __name__ == '__main__':
    main()
