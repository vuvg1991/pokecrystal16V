#!/usr/bin/env python3
"""
Activate disabled Pokémon in pokecrystal16V
This script uncomments all disabled Pokémon entries in:
- constants/pokemon_constants.asm
- data/pokemon/dex_entry_pointers.asm
- data/pokemon/names.asm
- data/pokemon/base_stats_*.asm files
"""

import os
import re
import sys

def uncomment_lines(content):
    """
    Uncomment lines that start with '; const ', '; db ', or '; INCLUDE '
    while preserving the structure and comments.
    """
    lines = content.split('\n')
    modified = False
    result = []
    
    for line in lines:
        # Match commented-out const definitions
        if re.match(r'^\s*;\s*(const\s+\w+)', line):
            # Remove leading comment character and semicolon
            uncommented = re.sub(r'^\s*;\s*', '', line)
            result.append(uncommented)
            modified = True
        # Match commented-out dba (Pokédex entries) or db (names)
        elif re.match(r'^\s*;\s*(dba|db)\s+', line):
            uncommented = re.sub(r'^\s*;\s*', '', line)
            result.append(uncommented)
            modified = True
        # Match commented-out INCLUDE statements for base stats
        elif re.match(r'^\s*;\s*INCLUDE\s+', line):
            uncommented = re.sub(r'^\s*;\s*', '', line)
            result.append(uncommented)
            modified = True
        else:
            result.append(line)
    
    return '\n'.join(result), modified

def process_file(filepath):
    """Process a single file and uncomment disabled Pokémon entries."""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, was_modified = uncomment_lines(content)
    
    if was_modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Updated: {filepath}")
        return True
    else:
        print(f"- No changes needed: {filepath}")
        return False

def main():
    """Main function to process all relevant files."""
    files_to_process = [
        'constants/pokemon_constants.asm',
        'data/pokemon/dex_entry_pointers.asm',
        'data/pokemon/names.asm',
        'data/pokemon/base_stats_1.asm',
        'data/pokemon/base_stats_2.asm',
        'data/pokemon/base_stats_3.asm',
        'data/pokemon/base_stats_4.asm',
    ]
    
    print("=" * 60)
    print("Pokémon Activation Script")
    print("=" * 60)
    print()
    
    updated_count = 0
    
    for filepath in files_to_process:
        if process_file(filepath):
            updated_count += 1
    
    print()
    print("=" * 60)
    print(f"Summary: Updated {updated_count}/{len(files_to_process)} files")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Build the ROM with: make")
    print("2. Test in an emulator")
    print("3. If build fails, check the error messages and address them manually")
    print()
    print("To rollback changes, use: git checkout activate-disabled-pokemon")
    print()

if __name__ == '__main__':
    main()
