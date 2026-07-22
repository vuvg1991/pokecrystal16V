#!/usr/bin/env python3
"""
Complete Pokémon activation and wild encounter integration
- Uncomments all disabled Pokémon (excluding legendaries)
- Adds them to appropriate routes/caves
- Skips Pokémon already in a location
"""

import os
import re
import sys

# Legendaries to SKIP (won't uncomment or add to encounters)
LEGENDARIES = {
    'KYOGRE', 'RAYQUAZA', 'JIRACHI',
    'ROTOM', 'UXIE', 'MESPRIT', 'AZELF', 'DIALGA', 'PALKIA', 'REGIGIGAS', 'GIRATINA', 'CRESSELIA', 'SHAYMIN',
    'XERNEAS', 'YVELTAL', 'ZYGARDE', 'VOLCANION',
    'GROOKEY', 'THWACKEY', 'RILLABOOM', 'ROOKIDEE', 'CORVSQUIRE', 'CORVKNIGHT',
    'BLIPBUG', 'DOTTLER', 'ORBEETLE', 'PIKIPEK', 'TRUMBEAK', 'TOUCANNON',
    'WOOLOO', 'DUBWOOL', 'ROLYCOLY', 'CARKOL', 'COALOSSAL',
    'GLIMMET', 'GLIMMORA', 'JANGMO_O', 'HAKAMO_O', 'KOMMO_O',
    'NIHILEGO', 'BUZZWOLE', 'PHEROMOSA', 'XURKITREE', 'CELESTEELA', 'KARTANA', 'GUZZLORD',
    'MAGEARNA', 'STAKATAKA', 'BLACEPHLON', 'TYPE__NULL', 'SILVALLY', 'KOMALA',
    'MAREANIE', 'TOXAPEX', 'MUDBRAY', 'MUDSDALE', 'PASSIMIAN',
    'ESPURR', 'MEOWSTIC', 'HONEDGE', 'DOUBLADE', 'AEGISLASH', 'SWIRLIX', 'SLURPUFF',
    'PETILIL', 'LILLIGANT', 'SAWSBUCK', 'DEERLING', 'FRILLISH', 'JELLICENT',
    'SEWADDLE', 'SWADLOON', 'LEAVANNY', 'ARCHEN', 'ARCHEOPS', 'CHATOT', 'SPIRITOMB',
    'MARACTUS', 'GOLETT', 'GOLURK', 'PAWNIARD', 'BISHARP', 'DEINO', 'ZWEILOUS', 'HYDREIGON',
    'LARVESTA', 'VOLCARONA', 'KLEFKI', 'FALINKS', 'STONJOURNR',
    'TOXEL', 'TOXTRICITY_AMPED', 'TOXTRICITY_LOWKEY',
    'DRACOZOLT', 'ARCTOZOLT', 'DRACOVISH', 'ARCTOVISH', 'DURALUDON',
    'REGIELEKI', 'REGIDRAGO', 'WO_CHIEN',
    'REGIROCK', 'REGICE', 'REGISTEEL',
}

# Pokémon placement: location -> [(pokemon, level_morn, level_day, level_night), ...]
POKEMON_ENCOUNTERS = {
    'ROUTE_32': [
        ('POOCHYENA', 5, 5, 5),
    ],
    'ROUTE_33': [
        ('ELECTRIKE', 9, 9, 9),
    ],
    'ROUTE_34': [
        ('MINUN', 12, 12, 12),
        ('PLUSLE', 13, 13, 13),
    ],
    'ROUTE_35': [
        ('TORKOAL', 14, 14, 14),
    ],
    'ROUTE_36': [
        ('SPOINK', 15, 15, 15),
    ],
    'ROUTE_37': [
        ('CACNEA', 16, 16, 16),
    ],
    'ROUTE_38': [
        ('MIGHTYENA', 18, 18, 18),
    ],
    'ROUTE_39': [
        ('GRUMPIG', 19, 19, 19),
    ],
    'UNION_CAVE_1F': [
        ('RELICANTH', 12, 12, 12),
    ],
    'UNION_CAVE_B1F': [
        ('BELDUM', 13, 13, 13),
    ],
    'UNION_CAVE_B2F': [
        ('METANG', 24, 24, 24),
    ],
    'MOUNT_MORTAR_1F_INSIDE': [
        ('CACTURNE', 18, 18, 18),
    ],
    'MOUNT_MORTAR_2F_INSIDE': [
        ('METAGROSS', 36, 36, 36),
    ],
    'BURNED_TOWER_B1F': [
        ('SHUPPET', 17, 17, 17),
    ],
    'ILEX_FOREST': [
        ('BANETTE', 12, 12, 12),
    ],
    'ICE_PATH_1F': [
        ('LILLIPUP', 27, 27, 27),
    ],
    'ICE_PATH_B1F': [
        ('HERDIER', 28, 28, 28),
    ],
    'ICE_PATH_B3F': [
        ('STOUTLAND', 31, 31, 31),
    ],
}

def should_skip_pokemon(pokemon_name):
    """Check if Pokémon is legendary and should be skipped."""
    return pokemon_name in LEGENDARIES

def uncomment_lines(content):
    """Uncomment disabled Pokémon lines, but skip legendaries."""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # Check if line is commented and contains a legendary
        is_legendary = any(leg in line for leg in LEGENDARIES)
        
        if is_legendary and line.strip().startswith(';'):
            # SKIP legendary Pokémon - keep them commented
            result.append(line)
        elif re.match(r'^\s*;\s*(const|dba|db|INCLUDE)\s+', line):
            # Uncomment non-legendary Pokémon
            uncommented = re.sub(r'^\s*;\s*', '', line)
            result.append(uncommented)
        else:
            result.append(line)
    
    return '\n'.join(result)

def process_file(filepath):
    """Process and uncomment a file."""
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = uncomment_lines(content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Updated: {filepath}")
        return True
    else:
        print(f"- No changes: {filepath}")
        return False

def add_pokemon_to_route(content, location, pokemon_list):
    """Add Pokémon to a specific route/location."""
    
    # Find the location block
    pattern = f'def_grass_wildmons {location}(.*?)end_grass_wildmons'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"  ⚠️  Location '{location}' not found in file")
        return content
    
    location_block = match.group(0)
    new_block = location_block
    added_count = 0
    
    for pokemon, level_m, level_d, level_n in pokemon_list:
        # Check if already present
        if f', {pokemon}' in location_block or f',{pokemon}' in location_block:
            print(f"    ⚠️  {pokemon} already in {location}, skipping")
            continue
        
        # Insert into morn section
        morn_match = re.search(r'(\; morn\s*\n(.*?))(\; day)', new_block, re.DOTALL)
        if morn_match:
            morn_section = morn_match.group(1)
            # Insert before the last dbw in morn section
            lines = morn_section.split('\n')
            insert_idx = len(lines) - 1
            while insert_idx > 0 and 'dbw' not in lines[insert_idx]:
                insert_idx -= 1
            lines.insert(insert_idx + 1, f'\tdbw {level_m}, {pokemon}')
            new_block = new_block.replace(morn_section, '\n'.join(lines))
        
        # Insert into day section
        day_match = re.search(r'(\; day\s*\n(.*?))(\; nite)', new_block, re.DOTALL)
        if day_match:
            day_section = day_match.group(1)
            lines = day_section.split('\n')
            insert_idx = len(lines) - 1
            while insert_idx > 0 and 'dbw' not in lines[insert_idx]:
                insert_idx -= 1
            lines.insert(insert_idx + 1, f'\tdbw {level_d}, {pokemon}')
            new_block = new_block.replace(day_section, '\n'.join(lines))
        
        # Insert into nite section
        nite_match = re.search(r'(\; nite\s*\n(.*?))(end_grass)', new_block, re.DOTALL)
        if nite_match:
            nite_section = nite_match.group(1)
            lines = nite_section.split('\n')
            insert_idx = len(lines) - 1
            while insert_idx > 0 and 'dbw' not in lines[insert_idx]:
                insert_idx -= 1
            lines.insert(insert_idx + 1, f'\tdbw {level_n}, {pokemon}')
            new_block = new_block.replace(nite_section, '\n'.join(lines))
        
        added_count += 1
        print(f"    ✓ Added {pokemon} (L{level_m}/L{level_d}/L{level_n})")
    
    if added_count > 0:
        content = content.replace(location_block, new_block)
    
    return content

def add_encounters(grass_file):
    """Add Pokémon to wild encounters."""
    
    if not os.path.exists(grass_file):
        print(f"⚠️  File not found: {grass_file}")
        return False
    
    with open(grass_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for location, pokemon_list in POKEMON_ENCOUNTERS.items():
        print(f"  📍 {location}")
        content = add_pokemon_to_route(content, location, pokemon_list)
    
    if content != original_content:
        with open(grass_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    print("=" * 70)
    print("POKÉMON COMPLETE ACTIVATION & ENCOUNTER INTEGRATION")
    print("=" * 70)
    print()
    
    core_files = [
        'constants/pokemon_constants.asm',
        'data/pokemon/dex_entry_pointers.asm',
        'data/pokemon/names.asm',
        'data/pokemon/base_stats_1.asm',
        'data/pokemon/base_stats_2.asm',
        'data/pokemon/base_stats_3.asm',
        'data/pokemon/base_stats_4.asm',
    ]
    
    print("🔓 Step 1: Uncommenting disabled non-legendary Pokémon...\n")
    
    uncommented = 0
    for filepath in core_files:
        if process_file(filepath):
            uncommented += 1
    
    print(f"\n✓ Updated {uncommented}/{len(core_files)} files\n")
    
    print("🌍 Step 2: Adding Pokémon to wild encounters...\n")
    
    encounter_files = [
        'data/wild/johto_grass.asm',
    ]
    
    for grass_file in encounter_files:
        print(f"\n📄 Processing: {grass_file}")
        if add_encounters(grass_file):
            print(f"✓ Updated: {grass_file}\n")
        else:
            print(f"⚠️  No changes made to: {grass_file}\n")
    
    print("=" * 70)
    print("✅ ACTIVATION & INTEGRATION COMPLETE!")
    print("=" * 70)
    print()
    print("📋 Next steps:")
    print("  1. Review changes:  git diff")
    print("  2. Build ROM:       make")
    print("  3. Test in emulator")
    print("  4. If issues:       git checkout activate-disabled-pokemon")
    print()

if __name__ == '__main__':
    main()
