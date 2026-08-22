"""D2R static data — runewords (with mods) + Horadric cube recipes.
Parsed from diablo2.io (D2R v3.2 / Reign of the Warlock data)."""

# (name, runes in order, sockets, item types, required level, patch, mods-per-type)
RUNEWORDS = [
    ('Mania', ('Shael', 'Ko', 'Eld'), 3, ('Weapons',), 39, '3.0', [
        ['5% Chance to cast level 1 Burst of Speed on striking', 'Level 1 Fanaticism Aura When Equipped', '+30% Increased Attack Speed', '+180-200% Enhanced Damage', '+75% Damage to Undead', '+50 to Attack Rating against Undead', '+10 to Dexterity']
    ]),
    ('Hysteria', ('Shael', 'Ko', 'Eld'), 3, ('Body Armor',), 39, '3.0', [
        ['+65% Faster Run/Walk', '+40% Increased Attack Speed', '+20% Faster Hit Recovery', '+6 to Evade', '+10 to Dexterity', '50% Slower Stamina Drain', '+All Resistances +10']
    ]),
    ('Metamorphosis', ('Io', 'Cham', 'Fal'), 3, ('Helms',), 67, '2.6', [
        ['Werewolf strikes grant Mark for 180 seconds', 'Mark of the Wolf:', '+30% Bonus to Attack Rating', 'Increase Maximum Life 40%', 'Werebear strikes grant Mark for 180 seconds', 'Mark of the Bear:', '+25% Attack Speed', 'Physical Damage Received Reduced by 20%', '+5 to Shape Shifting Skills (Druid only)', '+25% Chance of Crushing Blow', '+50-80% Enhanced Defense', '+10 to Strength', '+10 to Vitality', 'All Resistances +10', 'Cannot be Frozen']
    ]),
    ('Ground', ('Shael', 'Io', 'Ort'), 3, ('Helms',), 35, '2.6', [
        ['+20% Faster Hit Recovery', '+75-100% Enhanced Defense', '+10 to Vitality', 'Increase Maximum Life 5%', 'Lightning Resist +40-60%', 'Lightning Absorb +10-15%']
    ]),
    ('Temper', ('Shael', 'Io', 'Ral'), 3, ('Helms',), 35, '2.6', [
        ['+20% Faster Hit Recovery', '+75-100% Enhanced Defense', '+10 to Vitality', 'Increase Maximum Life 5%', 'Fire Resist +40-60%', 'Fire Absorb +10-15%']
    ]),
    ('Hearth', ('Shael', 'Io', 'Thul'), 3, ('Helms',), 35, '2.6', [
        ['+20% Faster Hit Recovery', '+75-100% Enhanced Defense', '+10 to Vitality', 'Increase Maximum Life 5%', 'Cold Resist +40-60%', 'Cold Absorb +10-15%', 'Cannot be Frozen']
    ]),
    ('Cure', ('Shael', 'Io', 'Tal'), 3, ('Helms',), 35, '2.6', [
        ['Level 1 Cleansing Aura when Equipped', '+20% Faster Hit Recovery', '+75-100% Enhanced Defense', '+10 to Vitality', 'Increase Maximum Life 5%', 'Poison Resist +40-60%', 'Poison Length Reduced by 50%']
    ]),
    ('Bulwark', ('Shael', 'Io', 'Sol'), 3, ('Helms',), 35, '2.6', [
        ['+20% Faster Hit Recovery', '+4-6% Life stolen per hit', '+75-100% Enhanced Defense', '+10 to Vitality', 'Increase Maximum Life 5%', 'Replenish Life +30', 'Damage Reduced by 7', 'Physical Damage Received Reduced by 10-15%']
    ]),
    ('Authority', ('Hel', 'Shael', 'Ral'), 3, ('Body Armor',), 29, '3.0', [
        ['2% Chance to cast level 10 Psychic Ward when struck', '10% Chance to cast level 15 Miasma Chain on striking', '+2 to Warlock Skill Levels', '+40-60% Enhanced Damage', 'Requirements -15%', '+20% Faster Hit Recovery', 'Fire Resist +30%']
    ]),
    ('Death', ('Hel', 'El', 'Vex', 'Ort', 'Gul'), 5, ('Swords', 'Axes'), 55, '1.10', [
        ['100% Chance To Cast Level 44 Chain Lightning When You Die', '25% Chance To Cast Level 18 Glacial Spike On Attack', 'Indestructible', '+300-385% Enhanced Damage', '20% Bonus To Attack Rating', '+50 To Attack Rating', 'Adds 1-50 Lightning Damage', '7% Mana Stolen Per Hit', '50% Chance of Crushing Blow', '+(0.5 per Character Level) 0.5-49.5% Deadly Strike (Based on Character Level)', '+1 To Light Radius', 'Level 22 Blood Golem (15 Charges)', 'Requirements -20%']
    ]),
    ('Principle', ('Ral', 'Gul', 'Eld'), 3, ('Body Armor',), 53, '1.11', [
        ['100% Chance To Cast Level 5 Holy Bolt On Striking', '+2 To Paladin Skill Levels', '+50% Damage to Undead', '+100-150 To Life', '15% Slower Stamina Drain', '+5% To Maximum Poison Resist', 'Fire Resist +30%']
    ]),
    ('Infinity', ('Ber', 'Mal', 'Ber', 'Ist'), 4, ('Polearms', 'Spears'), 63, '1.10', [
        ['50% Chance To Cast Level 20 Chain Lightning When You Kill An Enemy', 'Level 12 Conviction Aura When Equipped', '+35% Faster Run/Walk', '+255-325% Enhanced Damage', '-(45-55)% To Enemy Lightning Resistance', '40% Chance of Crushing Blow', 'Prevent Monster Heal', '0.5-49.5 To Vitality (Based on Character Level)', '30% Better Chance of Getting Magic Items', 'Level 21 Cyclone Armor (30 Charges)']
    ]),
    ('Pride', ('Cham', 'Sur', 'Io', 'Lo'), 4, ('Polearms', 'Spears'), 67, '1.10', [
        ['25% Chance To Cast Level 17 Fire Wall When Struck', 'Level 16-20 Concentration Aura When Equipped', '260-300% Bonus To Attack Rating', '+1-99% Damage To Demons (Based on Character Level)', 'Adds 50-280 Lightning Damage', '20% Deadly Strike', 'Hit Blinds Target', 'Freezes Target +3', '+10 To Vitality', 'Replenish Life +8', '1.875-185.625% Extra Gold From Monsters (Based on Character Level)']
    ]),
    ('Treachery', ('Shael', 'Thul', 'Lem'), 3, ('Body Armor',), 43, '1.11', [
        ['5% Chance To Cast Level 15 Fade When Struck', '25% Chance To Cast level 15 Venom: Skill On Striking', '+2 To Assassin Skill Levels', '+45% Increased Attack Speed', '+20% Faster Hit Recovery', 'Cold Resist +30%', '50% Extra Gold From Monsters']
    ]),
    ('Obedience', ('Hel', 'Ko', 'Thul', 'Eth', 'Fal'), 5, ('Polearms', 'Spears'), 41, '1.10', [
        ['30% Chance To Cast Level 21 Enchant When You Kill An Enemy', '40% Faster Hit Recovery', '+370% Enhanced Damage', '-25% Target Defense', 'Adds 3-14 Cold Damage 3 Second Duration', '-25% To Enemy Fire Resistance', '40% Chance of Crushing Blow', '+200-300 Defense', '+10 To Strength', '+10 To Dexterity', 'All Resistances +20-30', 'Requirements -20%']
    ]),
    ('Flickering Flame', ('Nef', 'Pul', 'Vex'), 3, ('Helms',), 55, '2.4', [
        ['Level 4-8 Resist Fire Aura When Equipped', '+3 To Fire Skills', '-10-15% To Enemy Fire Resistance', '+30% Enhanced Defense', '+30 Defense vs. Missile', '+50-75 To Mana', 'Half Freeze Duration', '+5% To Maximum Fire Resist', 'Poison Length Reduced by 50%']
    ]),
    ('Crescent Moon', ('Shael', 'Um', 'Tir'), 3, ('Polearms', 'Axes', 'Swords'), 47, '1.10', [
        ['10% Chance To Cast Level 17 Chain Lightning On Striking', '7% Chance To Cast Level 13 Static Field On Striking', '+20% Increased Attack Speed', '+180-220% Enhanced Damage', "Ignore Target's Defense", '-35% To Enemy Lightning Resistance', '25% Chance of Open Wounds', '+9-11 Magic Absorb', '+2 To Mana After Each Kill', 'Level 18 Summon Spirit Wolf (30 Charges)']
    ]),
    ('Black', ('Thul', 'Io', 'Nef'), 3, ('Clubs', 'Hammers', 'Maces'), 35, None, [
        ['+120% Enhanced Damage', '40% Chance of Crushing Blow', '+200 to Attack Rating', 'Adds 3-14 Cold Damage for 3 seconds', '+10 to Vitality', '15% increased Attack Speed', 'Magic Damage Reduced by 2', 'Level 4 Corpse Explosion (12 charges)', 'Knockback']
    ]),
    ('Doom', ('Hel', 'Ohm', 'Um', 'Lo', 'Cham'), 5, ('Axes', 'Polearms', 'Hammers'), 67, '1.10', [
        ['5% Chance To Cast Level 18 Volcano On Striking', 'Level 12 Holy Freeze Aura When Equipped', '+2 To All Skills', '+45% Increased Attack Speed', '+330-370% Enhanced Damage', '-(40-60)% To Enemy Cold Resistance', '20% Deadly Strike', '25% Chance of Open Wounds', 'Prevent Monster Heal', 'Freezes Target +3', 'Requirements -20%']
    ]),
    ('Faith', ('Ohm', 'Jah', 'Lem', 'Eld'), 4, ('Missile Weapons',), 65, '1.10', [
        ['Level 12-15 Fanaticism Aura When Equipped', '+1-2 To All Skills', '+330% Enhanced Damage', "Ignore Target's Defense", '300% Bonus To Attack Rating', '+75% Damage To Undead', '+50 To Attack Rating Against Undead', '+120 Fire Damage', 'All Resistances +15', '10% Reanimate As: Returned', '75% Extra Gold From Monsters']
    ]),
    ('Heart of the Oak', ('Ko', 'Vex', 'Pul', 'Thul'), 4, ('Maces', 'Staves'), 55, '1.10', [
        ['+3 To All Skills', '+40% Faster Cast Rate', '+75% Damage To Demons', '+100 To Attack Rating Against DemonsAdds 3-14 Cold Damage, 3 sec.Duration', '7% Mana Stolen Per Hit', '+10 To Dexterity', 'Replenish Life +20', 'Increase Maximum Mana 15%', 'All Resistances +30-40', 'Level 4 Oak Sage (25 Charges)', 'Level 14 Raven (60 Charges)']
    ]),
    ('Mist', ('Cham', 'Shael', 'Gul', 'Thul', 'Ith'), 5, ('Missile Weapons',), 67, '2.4', [
        ['Level 8-12 Concentration Aura When Equipped', '+3 To All Skills', '+20% Increased Attack Speed', '+100% Piercing Attack', '+325-375% Enhanced Damage', '+9 To Maximum Damage', '20% Bonus to Attack Rating', 'Adds 3-14 Cold Damage', 'Freezes Target +3', '+24 to Vitality', 'All Resistances +40']
    ]),
    ('Coven', ('Ist', 'Ral', 'Io'), 3, ('Helms',), 51, '3.0', [
        ['5% Chance to cast level 10 Sigil Lethargy when struck', '+1 to All Skills', '+20% Faster Cast Rate', '+30-50% Enhanced Defense', '+1-5 Life after each Kill', '26-40% Better Chance of Getting Magic Items', 'Fire Resist +30%', '+10 to Vitality']
    ]),
    ('Void', ('Thul', 'Zod', 'Ist'), 3, ('Daggers',), 69, '3.0', [
        ['+2 to All Skills', '+40% Faster Cast Rate', '+10-15% to Magic Skill Damage', '+1-3 to Abyss', '+8-12 to all Attributes', 'Level 4 Decrepify (35/35 Charges)', 'Adds 3-14 Cold Damage', 'Indestructible', '30% Better Chance of Getting Magic Items']
    ]),
    ('Eternity', ('Amn', 'Ber', 'Ist', 'Sol', 'Sur'), 5, ('Melee Weapons',), 63, '1.10', [
        ['Indestructible', '+260-310% Enhanced Damage', '+9 To Minimum Damage', '7% Life Stolen Per Hit', '20% Chance of Crushing Blow', 'Hit Blinds Target', 'Slows Target By 33%', 'Regenerate Mana 16%', 'Replenish Life +16', 'Cannot Be Frozen', '30% Better Chance Of Getting Magic Items', 'Level 8 Revive (88 Charges)']
    ]),
    ('Vigilance', ('Dol', 'Gul'), 2, ('Grimoires', 'Shields', 'Shrunken Heads', 'Targes'), 53, '3.0', [
        ['5% Chance to cast level 10 Ring of Fire when struck', '+10% Faster Run/Walk', '+30% Faster Block Rate', '+20-40 to Life', '+20-40 to Mana', 'All Resistances +25-35', '+75-100% Enhanced Defense', 'Replenish Life +7', '+5% to Maximum Poison Resist']
    ]),
    ('Wrath', ('Pul', 'Lum', 'Ber', 'Mal'), 4, ('Missile Weapons',), 63, '1.10', [
        ['30% Chance To Cast Level 1 Decrepify On Striking', '5% Chance To Cast Level 10 Life Tap On Striking', '+375% Damage To Demons', '+100 To Attack Rating Against Demons', '+250-300% Damage To Undead', 'Adds 85-120 Magic Damage', 'Adds 41-240 Lightning Damage', '20% Chance of Crushing Blow', 'Prevent Monster Heal', '+10 To Energy', 'Cannot Be Frozen']
    ]),
    ('Pattern', ('Tal', 'Ort', 'Thul'), 3, ('Katars',), 23, '2.4', [
        ['+30% Faster Block', '+40-80% Enhanced Damage', '10% Bonus to Attack Rating', 'Adds 12-32 Fire Damage', 'Adds 1-50 Lightning Damage', 'Adds 3-14 Cold Damage', '+75 Poison Damage Over 5 Seconds', '+6 Strength', '+6 Dexterity', 'All Resistances +15']
    ]),
    ('Voice of Reason', ('Lem', 'Ko', 'El', 'Eld'), 4, ('Swords', 'Maces'), 43, '1.10', [
        ['15% Chance To Cast Level 13 Frozen Orb On Striking', '18% Chance To Cast Level 20 Ice Blast On Striking', '+50 To Attack Rating', '+220-350% Damage To Demons', '+355-375% Damage To Undead', '+50 To Attack Rating Against Undead', 'Adds 100-220 Cold Damage', '-24% To Enemy Cold Resistance', '+10 To Dexterity', 'Cannot Be Frozen', '75% Extra Gold From Monsters', '+1 To Light Radius']
    ]),
    ('Smoke', ('Nef', 'Lum'), 2, ('Body Armor',), 37, None, [
        ['+75% Enhanced Defense', '+280 Defense vs. Missiles', 'All Resistances +50', '20% Faster Hit Recovery', 'Level 6 Weaken (18 Charges)', '+10 To Energy', '-1 To Light Radius']
    ]),
    ('Stone', ('Shael', 'Um', 'Pul', 'Lum'), 4, ('Body Armor',), 47, '1.10', [
        ['+60% Faster Hit Recovery', '+250-290% Enhanced Defense', '+300 Defense vs. Missile', '+16 To Strength', '+16 To Vitality', '+10 To Energy', 'All Resistances +15', 'Level 16 Molten Boulder (80 Charges)', 'Level 16 Clay Golem (16 Charges)']
    ]),
    ('Honor', ('Amn', 'El', 'Ith', 'Tir', 'Sol'), 5, ('Melee Weapons',), 27, None, [
        ['+160% Enhanced Damage', '+9 to Minimum Damage', '+9 to Maximum Damage', '25% Deadly Strike', '+250 to Attack Rating', '+1 to All Skills', '7% Life Stolen per Hit', '+10 Replenish Life', '+10 to Strength', '+1 to Light Radius', '+2 to Mana per Kill']
    ]),
    ('Ritual', ('Amn', 'Shael', 'Ohm'), 3, ('Daggers',), 57, '3.0', [
        ['13% Chance to cast level 1 Sigil Death when struck', '+40% Increased Attack Speed', '+250-320% Enhanced Damage', '+150-250% Damage to Demons', '+200-260% Bonus to Attack Rating', '+3-5 Life after each Kill', 'Slain Monsters Rest in Peace', '7% Life stolen per hit']
    ]),
    ('Rift', ('Hel', 'Ko', 'Lem', 'Gul'), 4, ('Polearms', 'Scepters'), 53, '1.10', [
        ['20% Chance To Cast Level 16 Tornado On Striking', '16% Chance To Cast Level 21 Frozen Orb On Attack', '20% Bonus To Attack Rating', 'Adds 160-250 Magic Damage', 'Adds 60-180 Fire Damage', '+5-10 To All Stats', '+10 To Dexterity', '38% Damage Taken Goes To Mana', '75% Extra Gold From Monsters', 'Level 15 Iron Maiden (40 Charges)', 'Requirements -20%']
    ]),
    ('Harmony', ('Tir', 'Ith', 'Sol', 'Ko'), 4, ('Missile Weapons',), 39, '1.10', [
        ['Level 10 Vigor Aura When Equipped', '+200-275% Enhanced Damage', '+9 To Minimum Damage', '+9 To Maximum Damage', 'Adds 55-160 Lightning Damage', 'Adds 55-160 Fire Damage', 'Adds 55-160 Cold Damage', '+2-6 To Valkyrie', '+10 To Dexterity', 'Regenerate Mana 20%', '+2 To Mana After Each Kill', '+2 To Light Radius', 'Level 20 Revive (25 Charges)']
    ]),
    ('Last Wish', ('Jah', 'Mal', 'Jah', 'Sur', 'Jah', 'Ber'), 6, ('Swords', 'Hammers', 'Axes'), 65, '1.10', [
        ['6% Chance To Cast Level 11 Fade When Struck', '10% Chance To Cast Level 18 Life Tap On Striking', '20% Chance To Cast Level 20 Charged Bolt On Attack', 'Level 17 Might Aura When Equipped', '+330-375% Enhanced Damage', "Ignore Target's Defense", '60-70% Chance of Crushing Blow', 'Prevent Monster Heal', 'Hit Blinds Target', '+(0.5 per character level) 0.5-49.5% Chance of Getting Magic Items (Based on Character Level)']
    ]),
    ('Insight', ('Ral', 'Tir', 'Tal', 'Sol'), 4, ('Polearms', 'Staves', 'Missile Weapons'), 27, '1.10', [
        ['Level 12-17 Meditation Aura When Equipped', '+35% Faster Cast Rate', '+200-260% Enhanced Damage', '+9 To Minimum Damage', '180-250% Bonus to Attack Rating', 'Adds 5-30 Fire Damage', '+75 Poison Damage Over 5 Seconds', '+1-6 To Critical Strike', '+5 To All Attributes', '+2 To Mana After Each Kill', '23% Better Chance of Getting Magic Items']
    ]),
    ('Edge', ('Tir', 'Tal', 'Amn'), 3, ('Missile Weapons',), 25, '1.10', [
        ['Level 15 Thorns Aura When Equipped', '+35% Increased Attack Speed', '+320-380% Damage To Demons', '+280% Damage To Undead', '+75 Poison Damage Over 5 Seconds', '7% Life Stolen Per Hit', 'Prevent Monster Heal', '+5-10 To All Attributes', '+2 To Mana After Each Kill', 'Reduces All Vendor Prices 15%']
    ]),
    ('Dream', ('Io', 'Jah', 'Pul'), 3, ('Helms', 'Shields'), 65, '1.10', [
        ['10% Chance To Cast Level 15 Confuse When Struck', 'Level 15 Holy Shock Aura When Equipped', '+20-30% Faster Hit Recovery', '+30% Enhanced Defense', '+150-220 Defense', '+10 To Vitality', 'Increase Maximum Life 5% (Helms Only)', '+50 To Life (Shields Only)', '+0.625-61.875 To Mana (Based On Character Level)', 'All Resistances +5-20', '12-25% Better Chance of Getting Magic Items']
    ]),
    ('Oath', ('Shael', 'Pul', 'Mal', 'Lum'), 4, ('Swords', 'Axes', 'Maces'), 49, '1.10', [
        ['30% Chance To Cast Level 20 Bone Spirit On Striking', 'Indestructible', '+50% Increased Attack Speed', '+210-340% Enhanced Damage', '+75% Damage To Demons', '+100 To Attack Rating Against Demons', 'Prevent Monster Heal', '+10 To Energy', '+10-15 Magic Absorb', 'Level 16 Heart of Wolverine (20 Charges)', 'Level 17 Iron Golem (14 Charges)']
    ]),
    ('Enigma', ('Jah', 'Ith', 'Ber'), 3, ('Body Armor',), 65, '1.10', [
        ['+2 To All Skills', '+45% Faster Run/Walk', '+1 To Teleport', '+750-775 Defense', '+ (0.75 Per Character Level) +0-74 To Strength (Based On Character Level)', 'Increase Maximum Life 5%', 'Damage Reduced By 8%', '+14 Life After Each Kill', '15% Damage Taken Goes To Mana', '+ (1 Per Character Level) +1-99% Better Chance of Getting Magic Items (Based On Character Level)']
    ]),
    ('Splendor', ('Eth', 'Lum'), 2, ('Shields',), 37, '1.10', [
        ['+1 To All Skills', '+10% Faster Cast Rate', '+20% Faster Block Rate', '+60-100% Enhanced Defense', '+10 To Energy', 'Regenerate Mana 15%', '50% Extra Gold From Monsters', '20% Better Chance of Getting Magic Items', '+3 To Light Radius']
    ]),
    ('Mosaic', ('Mal', 'Gul', 'Amn'), 3, ('Katars',), 53, '2.6', [
        ['+50% chance for finishing moves to not consume charges', 'When a finisher is executed this way, it now refreshes the expiration timer of the stack', '+2 to Martial Arts (Assassin only)', '+20% Increased Attack Speed', '+200-250% Enhanced Damage', '+20% Bonus to Attack Rating', '7% Life Steal', '+8-15% to Cold Skill Damage', '+8-15% to Lightning Skill Damage', '+8-15% to Fire Skill Damage', 'Prevent Monster Heal']
    ]),
    ('Leaf', ('Tir', 'Ral'), 2, ('Staves',), 19, None, [
        ['Adds 5-30 Fire Damage', '+3 To Fire Skills', '+3 To Fire Bolt (Sorceress Only)', '+3 To Inferno (Sorceress Only)', '+3 To Warmth (Sorceress Only)', '+2 To Mana After Each Kill', '+ (2 Per Character Level) +2-198 To Defense (Based On Character Level)', 'Cold Resist +33%']
    ]),
    ('Rhyme', ('Shael', 'Eth'), 2, ('Shields',), 29, None, [
        ['20% Increased Chance of Blocking', '40% Faster Block Rate', '+25 to All Resistances', 'Regenerate Mana 15%', 'Cannot Be Frozen', '50% Extra Gold From Monsters', '25% Better Chance Of Getting Magic Items']
    ]),
    ('Obsession', ('Zod', 'Ist', 'Lem', 'Lum', 'Io', 'Nef'), 6, ('Staves',), 69, '2.4', [
        ['Indestructible', '24% Chance to cast level 10 Weaken when struck', '+4 To All Skills', '+65% Faster Cast Rate', '+60% Faster Hit Recovery', 'Knockback', '+10 To Vitality', '+10 To Energy', 'Increase Maximum Life 15-25%', 'Regenerate Mana 15-30%', 'All Resistances +60-70', '75% Extra Gold from Monsters', '30% Better Chance of Getting Magic Items']
    ]),
    ('Phoenix', ('Vex', 'Vex', 'Lo', 'Jah'), 4, ('Weapons', 'Shields'), 65, '1.10', [
        ['100% Chance To Cast level 40 Blaze When You Level Up', '40% Chance To Cast Level 22 Firestorm On Striking', 'Level 10-15 Redemption Aura When Equipped', '+350-400% Enhanced Damage', "Ignores Target's Defense", '14% Mana Stolen Per Hit', '-28% To Enemy Fire Resistance', '20% Deadly Strike', '+350-400 Defense Vs. Missile', '+15-21 Fire Absorb'],
        ['100% Chance To Cast level 40 Blaze When You Level Up', '40% Chance To Cast Level 22 Firestorm On Striking', 'Level 10-15 Redemption Aura When Equipped', '+350-400 Defense Vs. Missile', '+350-400% Enhanced Damage', '-28% To Enemy Fire Resistance', '+50 To Life', '+5% To Maximum Lightning Resist', '+10% To Maximum Fire Resist', '+15-21 Fire Absorb']
    ]),
    ('Rain', ('Ort', 'Mal', 'Ith'), 3, ('Body Armor',), 49, '1.11', [
        ['5% Chance To Cast Level 15 Cyclone Armor When Struck', '5% Chance To Cast Level 15 Twister On Striking', '+2 To Druid Skill Levels', '+100-150 To Mana', 'Lightning Resist +30%', 'Magic Damage Reduced By 7', '15% Damage Taken Goes to Mana']
    ]),
    ('Bramble', ('Ral', 'Ohm', 'Sur', 'Eth'), 4, ('Body Armor',), 61, '1.10', [
        ['Level 15-21 Thorns Aura When Equipped', '+50% Faster Hit Recovery', '+25-50% To Poison Skill Damage', '+300 Defense', 'Increase Maximum Mana 5%', 'Regenerate Mana 15%', '+5% To Maximum Cold Resist', 'Fire Resist +30%', 'Poison Resist +100%', '+13 Life After Each Kill', 'Level 13 Spirit of Barbs (33 Charges)']
    ]),
    ('Spirit', ('Tal', 'Thul', 'Ort', 'Amn'), 4, ('Swords', 'Shields'), 25, '1.10', [
        ['+2 To All Skills', '+25-35% Faster Cast Rate', '+55% Faster Hit Recovery', 'Adds 1-50 Lightning Damage', 'Adds 3-14 Cold Damage 3 Second Duration', '+75 Poison Damage Over 5 Seconds', '7% Life Stolen Per Hit', '+250 Defense Vs. Missile', '+22 To Vitality', '+89-112 To Mana', '+3-8 Magic Absorb'],
        ['+2 To All Skills', '+25-35% Faster Cast Rate', '+55% Faster Hit Recovery', '+250 Defense Vs. Missile', '+22 To Vitality', '+89-112 To Mana', 'Cold Resist +35%', 'Lightning Resist +35%', 'Poison Resist +35%', '+3-8 Magic Absorb', 'Attacker Takes Damage of 14']
    ]),
    ('Steel', ('Tir', 'El'), 2, ('Swords', 'Axes', 'Maces'), 13, None, [
        ['20% Enhanced Damage', '+3 To Minimum Damage', '+3 To Maximum Damage', '+50 To Attack Rating', '50% Chance Of Open Wounds', '25% Increased Attack Speed', '+2 To Mana After Each Kill', '+1 To Light Radius']
    ]),
    ('Peace', ('Shael', 'Thul', 'Amn'), 3, ('Body Armor',), 29, '1.11', [
        ['4% Chance To Cast Level 5 Slow Missiles When Struck', '2% Chance To Cast level 15 Valkyrie On Striking', '+2 To Amazon Skill Levels', '+20% Faster Hit Recovery', '+2 To Critical Strike', 'Cold Resist +30%', 'Attacker Takes Damage of 14']
    ]),
    ('Dragon', ('Sur', 'Lo', 'Sol'), 3, ('Shields', 'Body Armor'), 61, '1.10', [
        ['20% Chance to Cast Level 18 Venom: Skill When Struck', '12% Chance To Cast Level 15 Hydra On Striking', 'Level 14 Holy Fire Aura When Equipped', '+360 Defense', '+230 Defense vs. Missile', '+3-5 To All Attributes', '+0.375-37.125 To Strength (Based on Character Level)', 'Increase Maximum Mana 5% (Armor Only)', '+50 To Mana (Shields Only)', '+5% To Maximum Lightning Resist', 'Damage Reduced by 7']
    ]),
    ('Lionheart', ('Hel', 'Lum', 'Fal'), 3, ('Body Armor',), 41, None, [
        ['+20% Enhanced Damage', 'Requirements -15%', '+25 To Strength', '+10 To Energy', '+20 To Vitality', '+15 To Dexterity', '+50 To Life', 'All Resistances +30']
    ]),
    ('Bone', ('Sol', 'Um', 'Um'), 3, ('Body Armor',), 47, '1.11', [
        ['15% Chance To Cast level 10 Bone Armor When Struck', '15% Chance To Cast level 10 Bone Spear On Striking', '+2 To Necromancer Skill Levels', '+100-150 To Mana', 'All Resistances +30', 'Damage Reduced By 7']
    ]),
    ('Plague', ('Cham', 'Shael', 'Um'), 3, ('Swords', 'Katars', 'Daggers'), 67, '2.4', [
        ['20% Chance To Cast Level 12 Lower Resist When Struck', '25% Chance to Cast Level 15 Poison Nova On Striking', 'Level 13-17 Cleansing Aura When Equipped', '+1-2 To All Skills', '+20% Increased Attack Speed', '+220-320% Enhanced Damage', '-23% To Enemy Poison Resistance', '+0.3% (0-29.7) Deadly Strike (Based on Character Level)', '+25% Chance of Open Wounds', 'Freezes Target +3']
    ]),
    ('Beast', ('Ber', 'Tir', 'Um', 'Mal', 'Lum'), 5, ('Axes', 'Scepters', 'Hammers'), 63, '1.10', [
        ['Level 9 Fanaticism Aura When Equipped', '+40% Increased Attack Speed', '+240-270% Enhanced Damage', '20% Chance of Crushing Blow', '25% Chance of Open Wounds', '+3 To Werebear', '+3 To Lycanthropy', 'Prevent Monster Heal', '+25-40 To Strength', '+10 To Energy', '+2 To Mana After Each Kill', 'Level 13 Summon Grizzly (5 Charges)']
    ]),
    ('Hustle', ('Shael', 'Ko', 'Eld'), 3, ('Weapons', 'Armor'), 39, '2.6', [
        ['5% Chance to cast level 1 Burst of Speed on striking', 'Level 1 Fanaticism Aura When Equipped', '+30% Increased Attack Speed', '+180-200% Enhanced Damage', '+75% Damage to Undead', '+50 to Attack Rating against Undead', '+10 to Dexterity'],
        ['+65% Faster Run/Walk', '+40% Increased Attack Speed', '+20% Faster Hit Recovery', '+6 to Evade', '+10 to Dexterity', '50% Slower Stamina Drain', '+All Resistances +10']
    ]),
    ('White', ('Dol', 'Io'), 2, ('Wand',), 35, None, [
        ['Hit Causes Monster To Flee 25%', '+10 To Vitality', '+3 To Poison and Bone Skills (Necromancer Only)', '+3 To Bone Armor (Necromancer Only)', '+2 To Bone Spear (Necromancer Only)', '+4 To Skeleton Mastery (Necromancer Only)', 'Magic Damage Reduced By 4', '20% Faster Cast Rate', '+13 To Mana']
    ]),
    ('Holy Thunder', ('Eth', 'Ral', 'Ort', 'Tal'), 4, ('Scepters',), 21, None, [
        ['+60% Enhanced Damage', '-25% Target Defense', 'Adds 5-30 Fire Damage', 'Adds 21-110 Lightning Damage', '+75 Poison Damage Over 5 Seconds', '+10 To Maximum Damage', 'Lightning Resistance +60%', '+5 To Maximum Lightning Resistance', '+3 To Holy Shock (Paladin Only)', 'Level 7 Chain Lightning (60 Charges)']
    ]),
    ('Sanctuary', ('Ko', 'Ko', 'Mal'), 3, ('Shields',), 49, '1.10', [
        ['+20% Faster Hit Recovery', '+20% Faster Block Rate', '20% Increased Chance of Blocking', '+130-160% Enhanced Defense', '+250 Defense vs. Missile', '+20 To Dexterity', 'All Resistances +50-70', 'Magic Damage Reduced By 7', 'Level 12 Slow Missiles (60 Charges)']
    ]),
    ("Ancients' Pledge", ('Ral', 'Ort', 'Tal'), 3, ('Shields',), 21, None, [
        ['+50% Enhanced Defense', 'Cold Resist +43%', 'Fire Resist +48%', 'Lightning Resist +48%', 'Poison Resist +48%', '10% Damage Goes To Mana']
    ]),
    ('Hand of Justice', ('Sur', 'Cham', 'Amn', 'Lo'), 4, ('Weapons',), 67, '1.10', [
        ['100% Chance To Cast Level 36 Blaze When You Level Up', '100% Chance To Cast Level 48 Meteor When You Die', 'Level 16 Holy Fire Aura When Equipped', '+33% Increased Attack Speed', '+280-330% Enhanced Damage', "Ignore Target's Defense", '7% Life Stolen Per Hit', '-20% To Enemy Fire Resistance', '20% Deadly Strike', 'Hit Blinds Target', 'Freezes Target +3']
    ]),
    ('Kingslayer', ('Mal', 'Um', 'Gul', 'Fal'), 4, ('Swords', 'Axes'), 53, '1.10', [
        ['+30% Increased Attack Speed', '+230-270% Enhanced Damage', '-25% Target Defense', '20% Bonus To Attack Rating', '33% Chance of Crushing Blow', '50% Chance of Open Wounds', '+1 To Vengeance', 'Prevent Monster Heal', '+10 To Strength', '40% Extra Gold From Monsters']
    ]),
    ('Duress', ('Shael', 'Um', 'Thul'), 3, ('Body Armor',), 47, '1.10', [
        ['+40% Faster Hit Recovery', '+10-20% Enhanced Damage', 'Adds 37-133 Cold Damage 2 sec. Duration', '15% Chance of Crushing Blow', '33% Chance of Open Wounds', '+150-200% Enhanced Defense', '-20% Slower Stamina Drain', 'Cold Resist +45%', 'Lightning Resist +15%', 'Fire Resist +15%', 'Poison Resist +15%']
    ]),
    ('Stealth', ('Tal', 'Eth'), 2, ('Body Armor',), 17, None, [
        ['Magic Damage Reduced By 3', '+6 To Dexterity', '+15 To Maximum Stamina', 'Poison Resist +30%', 'Regenerate Mana 15%', '25% Faster Run/Walk', '25% Faster Cast Rate', '25% Faster Hit Recovery']
    ]),
    ('Venom', ('Tal', 'Dol', 'Mal'), 3, ('Weapons',), 49, None, [
        ['Hit Causes Monster To Flee 25%', 'Prevent Monster Heal', "Ignore Target's Defense", '7% Mana Stolen Per Hit', 'Level 15 Poison Explosion (27 Charges)', 'Level 13 Poison Nova (11 Charges)', '+273 Poison Damage Over 6 seconds']
    ]),
    ('Lore', ('Ort', 'Sol'), 2, ('Helms',), 27, None, [
        ['+1 To All Skills', '+10 To Energy', '+2 To Mana After Each Kill', 'Lightning Resist +30%', 'Damage Reduced By 7', '+2 To Light Radius']
    ]),
    ('Wealth', ('Lem', 'Ko', 'Tir'), 3, ('Body Armor',), 43, None, [
        ['300% Extra Gold From Monsters', '100% Better Chance Of Getting Magic Items', '+2 To Mana After Each Kill', '+10 To Dexterity']
    ]),
    ('Malice', ('Ith', 'El', 'Eth'), 3, ('Melee Weapons',), 15, None, [
        ['+33% Enhanced Damage', '+9 To Maximum Damage', '100% Chance Of Open Wounds', '-25% Target Defense', '-100 To Monster Defense per Hit', 'Prevent Monster Heal', '+50 To Attack Rating', 'Drain Life -5']
    ]),
    ('Fury', ('Jah', 'Gul', 'Eth'), 3, ('Melee Weapons',), 65, None, [
        ['+209% Enhanced Damage', '40% Increased Attack Speed', 'Prevent Monster Heal', '66% Chance of Open Wounds', '33% Chance of Deadly Strike', '-25% Target Defense', '20% to Attack Rating', '6% Life Stolen Per Hit', 'Ignores Target Defense', '+5 to Frenzy (Barbarian only)']
    ]),
    ('Call To Arms', ('Amn', 'Ral', 'Mal', 'Ist', 'Ohm'), 5, ('Weapons',), 57, '1.10', [
        ['+1 To All Skills', '+40% Increased Attack Speed', '+250-290% Enhanced Damage', 'Adds 5-30 Fire Damage', '7% Life Stolen Per Hit', '+2-6 To Battle Command', '+1-6 To Battle Orders', '+1-4 To Battle Cry', 'Prevent Monster Heal', 'Replenish Life +12', '30% Better Chance of Getting Magic Items']
    ]),
    ('Chaos', ('Fal', 'Ohm', 'Um'), 3, ('Katars',), 57, '1.10', [
        ['9% Chance To Cast Level 11 Frozen Orb On Striking', '11% Chance To Cast Level 9 Charged Bolt On Striking', '+35% Increased Attack Speed', '+290-340% Enhanced Damage', 'Adds 216-471 Magic Damage', '25% Chance of Open Wounds', '+1 To Whirlwind', '+10 To Strength', '+15 Life After Each Demon Kill']
    ]),
    ('Breath of the Dying', ('Vex', 'Hel', 'El', 'Eld', 'Zod', 'Eth'), 6, ('Weapons',), 69, '1.10', [
        ['50% Chance To Cast Level 20 Poison Nova When You Kill An Enemy', 'Indestructible', '+60% Increased Attack Speed', '+350-400% Enhanced Damage', '+200% Damage To Undead', '-25% Target Defense', '+50 To Attack Rating', '+50 To Attack Rating Against Undead', '7% Mana Stolen per Hit', '12-15% Life Stolen per Hit', 'Prevent Monster Heal', '+30 To All Attributes', '+1 To Light Radius', 'Requirements -20%']
    ]),
    ('Grief', ('Eth', 'Tir', 'Lo', 'Mal', 'Ral'), 5, ('Axes', 'Swords'), 59, '1.10', [
        ['35% Chance To Cast Level 15 Venom: Skill On Striking', '+30-40% Increased Attack Speed', 'Damage +340-400', "Ignore Target's Defense", '-25% Target Defense', '+(1.875 per character level) 1.875-185.625% Damage To Demons (Based on Character Level)', 'Adds 5-30 Fire Damage', '-20-25% To Enemy Poison Resistance', '20% Deadly Strike', 'Prevent Monster Heal', '+2 To Mana After Each Kill', '+10-15 Life After Each Kill']
    ]),
    ('Fortitude', ('El', 'Sol', 'Dol', 'Lo'), 4, ('Weapons', 'Body Armor'), 59, '1.10', [
        ['20% Chance To Cast Level 15 Chilling Armor when Struck', '+25% Faster Cast Rate', '+300% Enhanced Damage', '+9 To Minimum Damage', '+50 To Attack Rating', '20% Deadly Strike', 'Hit Causes Monster To Flee 25%', '+200% Enhanced Defense', '+((8-12)*0.125*CLVL) To Life (Based on Character Level)', 'All Resistances +25-30', '12% Damage Taken Goes To Mana', '+1 To Light Radius'],
        ['20% Chance To Cast Level 15 Chilling Armor when Struck', '+25% Faster Cast Rate', '+300% Enhanced Damage', '+200% Enhanced Defense', '+15 Defense', '+((8-12)*0.125*CLVL) To Life (Based on Character Level)', 'Replenish Life +7', '+5% To Maximum Lightning Resist', 'All Resistances +25-30', 'Damage Reduced By 7', '12% Damage Taken Goes To Mana', '+1 To Light Radius']
    ]),
    ('Ice', ('Amn', 'Shael', 'Jah', 'Lo'), 4, ('Missile Weapons',), 65, '1.10', [
        ['100% Chance To Cast Level 40 Blizzard When You Level Up', '25% Chance To Cast Level 22 Frost Nova On Striking', 'Level 18 Holy Freeze Aura When Equipped', '+20% Increased Attack Speed', '+140-210% Enhanced Damage', "Ignore Target's Defense", '+25-30% To Cold Skill Damage', '-20% To Enemy Cold Resistance', '7% Life Stolen Per Hit', '20% Deadly Strike', '3.125-309.375% Extra Gold From Monsters (Based on Character Level)']
    ]),
    ('Delirium', ('Lem', 'Ist', 'Io'), 3, ('Helms',), 51, '1.10', [
        ['1% Chance To Cast Level 50 Delirium (morph) When Struck', '6% Chance To Cast Level 14 Mind Blast When Struck', '14% Chance To Cast Level 13 Terror When Struck', '11% Chance To Cast Level 18 Confuse On Striking', '+2 To All Skills', '+261 Defense', '+10 To Vitality', '50% Extra Gold From Monsters', '25% Better Chance of Getting Magic Items', 'Level 17 Attract (60 Charges)']
    ]),
    ('Gloom', ('Fal', 'Um', 'Pul'), 3, ('Body Armor',), 47, '1.10', [
        ['15% Chance To Cast Level 3 Dim Vision When Struck', '+10% Faster Hit Recovery', '+200-260% Enhanced Defense', '+10 To Strength', 'All Resistances +45', 'Half Freeze Duration', '5% Damage Taken Goes To Mana', '-3 To Light Radius']
    ]),
    ('Radiance', ('Nef', 'Sol', 'Ith'), 3, ('Helms',), 27, None, [
        ['+75% Enhanced Defense', '+30 Defense Vs. Missile', '+10 To Energy', '+10 To Vitality', '15% Damage Taken Goes To Mana', 'Magic Damage Reduced By 3', '+33 To Mana', 'Damage Reduced By 7', '+5 To Light Radius']
    ]),
    ('Silence', ('Dol', 'Eld', 'Hel', 'Ist', 'Tir', 'Vex'), 6, ('Weapons',), 55, None, [
        ['200% Enhanced Damage', '+75% Damage To Undead', 'Requirements -20%', '20% Increased Attack Speed', '+50 To Attack Rating Against Undead', '+2 To All Skills', 'All Resistances +75', '20% Faster Hit Recovery', '11% Mana Stolen Per Hit', 'Hit Causes Monster To Flee 25%', 'Hit Blinds Target +33', '+2 To Mana After Each Kill', '30% Better Chance Of Getting Magic Items']
    ]),
    ('Melody', ('Shael', 'Ko', 'Nef'), 3, ('Missile Weapons',), 39, None, [
        ['+50% Enhanced Damage', '+300% Damage To Undead', '+3 To Bow and Crossbow Skills (Amazon Only)', '+3 To Critical Strike (Amazon Only)', '+3 To Dodge (Amazon Only)', '+3 To Slow Missiles (Amazon Only)', '20% Increased Attack Speed', '+10 To Dexterity', 'Knockback']
    ]),
    ('Lawbringer', ('Amn', 'Lem', 'Ko'), 3, ('Swords', 'Hammers', 'Scepters'), 43, '1.10', [
        ['20% Chance To Cast Level 15 Decrepify On Striking', 'Level 16-18 Sanctuary Aura When Equipped', '-50% Target Defense', 'Adds 150-210 Fire Damage', 'Adds 130-180 Cold Damage', '7% Life Stolen Per Hit', 'Slain Monsters Rest In Peace', '+200-250 Defense Vs. Missile', '+10 To Dexterity', '75% Extra Gold From Monsters']
    ]),
    ('Destruction', ('Vex', 'Lo', 'Ber', 'Jah', 'Ko'), 5, ('Polearms', 'Swords'), 65, '1.10', [
        ['23% Chance To Cast Level 12 Volcano On Striking', '5% Chance To Cast Level 23 Molten Boulder On Striking', '100% Chance To Cast level 45 Meteor When You Die', '15% Chance To Cast Level 22 Nova On Attack', '+350% Enhanced Damage', "Ignore Target's Defense", 'Adds 100-180 Magic Damage', '7% Mana Stolen Per Hit', '20% Chance Of Crushing Blow', '20% Deadly Strike', 'Prevent Monster Heal', '+10 To Dexterity']
    ]),
    ('Chains of Honor', ('Dol', 'Um', 'Ber', 'Ist'), 4, ('Body Armor',), 63, '1.10', [
        ['+2 To All Skills', '+200% Damage To Demons', '+100% Damage To Undead', '8% Life Stolen Per Hit', '+70% Enhanced Defense', '+20 To Strength', 'Replenish Life +7', 'All Resistances +65', 'Damage Reduced By 8%', '25% Better Chance of Getting Magic Items']
    ]),
    ('Wisdom', ('Pul', 'Ith', 'Eld'), 3, ('Helms',), 45, '2.4', [
        ['+33% Piercing Attack', '+15-25% Bonus to Attack Rating', '4-8% Mana Stolen Per Hit', '+30% Enhanced Defense', '+10 Energy', '15% Slower Stamina Drain', 'Cannot Be Frozen', '+5 Mana After Each Kill', '15% Damage Taken Goes to Mana']
    ]),
    ('Exile', ('Vex', 'Ohm', 'Ist', 'Dol'), 4, ('Paladin Shields',), 57, '1.10', [
        ['15% Chance To Cast Level 5 Life Tap On Striking', 'Level 13-16 Defiance Aura When Equipped', '+2 To Offensive Auras (Paladin Only)', '+30% Faster Block Rate', 'Freezes Target', '+220-260% Enhanced Defense', 'Replenish Life +7', '+5% To Maximum Cold Resist', '+5% To Maximum Fire Resist', '25% Better Chance Of Getting Magic Items', 'Repairs 1 Durability in 4 Seconds']
    ]),
    ('Wind', ('Sur', 'El'), 2, ('Melee Weapons',), 61, '1.10', [
        ['10% Chance To Cast Level 9 Tornado On Striking', '+20% Faster Run/Walk', '+40% Increased Attack Speed', '+15% Faster Hit Recovery', '+120-160% Enhanced Damage', '-50% Target Defense', '+50 To Attack Rating', 'Hit Blinds Target', '+1 To Light Radius', 'Level 13 Twister (127 Charges)']
    ]),
    ('Brand', ('Jah', 'Lo', 'Mal', 'Gul'), 4, ('Missile Weapons',), 65, '1.10', [
        ['35% Chance To Cast Level 14 Amplify Damage When Struck', '100% Chance To Cast Level 18 Bone Spear On Striking', '+260-340% Enhanced Damage', "Ignores Target's Defense", '20% Bonus to Attack Rating', '+280-330% Damage To Demons', '20% Deadly Strike', 'Prevent Monster Heal', 'Knockback', 'Fires Explosive Arrows or Bolts [level 15]']
    ]),
    ('Memory', ('Lum', 'Io', 'Sol', 'Eth'), 4, ('Staves',), 37, None, [
        ['+3 to Sorceress Skill Levels', '33% Faster Cast Rate', 'Increase Maximum Mana 20%', '+3 Energy Shield (Sorceress Only)', '+2 Static Field (Sorceress Only)', '+10 To Energy', '+10 To Vitality', '+9 To Minimum Damage', '-25% Target Defense', 'Magic Damage Reduced By 7', '+50% Enhanced Defense']
    ]),
    ('Strength', ('Amn', 'Tir'), 2, ('Melee Weapons',), 25, None, [
        ['35% Enhanced Damage', '25% Chance Of Crushing Blow', '7% Life Stolen Per Hit', '+2 To Mana After Each Kill', '+20 To Strength', '+10 To Vitality']
    ]),
    ('Myth', ('Hel', 'Amn', 'Nef'), 3, ('Body Armor',), 25, '1.11', [
        ['3% Chance To Cast Level 1 Howl When Struck', '10% Chance To Cast Level 1 Taunt On Striking', '+2 To Barbarian Skill Levels', '+30 Defense Vs. Missile', 'Replenish Life +10', 'Attacker Takes Damage of 14', 'Requirements -15%']
    ]),
    ('Unbending Will', ('Fal', 'Io', 'Ith', 'Eld', 'El', 'Hel'), 6, ('Swords',), 41, '2.4', [
        ['18% Chance to Cast Level 18 Taunt On Striking', '+3 to Combat Skills (Barbarian Only)', '+20-30% Increased Attack Speed', '+300-350% Enhanced Damage', '+9 to Maximum Damage', '+50 to Attack Rating', '+75% Damage To Undead', '+50 Attack Rating Against Undead', '8-10% Life Stolen Per Hit', 'Prevent Monster Heal', '+10 To Strength', '+10 To Vitality', 'Damage Reduced by 8', '+1 To Light Radius', 'Requirements -20%']
    ]),
    ('Famine', ('Fal', 'Ohm', 'Ort', 'Jah'), 4, ('Axes', 'Hammers'), 65, '1.10', [
        ['30% Increased Attack Speed', '+320-370% Enhanced Damage', "Ignore Target's Defense", 'Adds 180-200 Magic Damage', 'Adds 50-200 Fire Damage', 'Adds 51-250 Lightning Damage', 'Adds 50-200 Cold Damage', '12% Life Stolen Per Hit', 'Prevent Monster Heal', '+10 To Strength']
    ]),
    ('Nadir', ('Nef', 'Tir'), 2, ('Helms',), 13, None, [
        ['+50% Enhanced Defense', '+10 Defense', '+30 Defense vs. Missile', 'Level 13 Cloak of Shadows (9 Charges)', '+2 To Mana After Each Kill', '+5 To Strength', '-33% Extra Gold From Monsters', '-3 To Light Radius']
    ]),
    ('Passion', ('Dol', 'Ort', 'Eld', 'Lem'), 4, ('Weapons',), 43, '1.10', [
        ['+25% Increased Attack Speed', '+160-210% Enhanced Damage', '50-80% Bonus To Attack Rating', '+75% Damage To Undead', '+50 To Attack Rating Against Undead', 'Adds 1-50 Lightning Damage', '+1 To Berserk', '+1 To Zeal', 'Hit Blinds Target +10', 'Hit Causes Monster To Flee 25%', '75% Extra Gold From Monsters', 'Level 3 Heart of Wolverine (12 Charges)']
    ]),
    ('Enlightenment', ('Pul', 'Ral', 'Sol'), 3, ('Body Armor',), 45, '1.11', [
        ['5% Chance To Cast Level 15 Blaze When Struck', '5% Chance To Cast level 15 Fire Ball On Striking', '+2 To Sorceress Skill Levels', '+1 To Warmth', '+30% Enhanced Defense', 'Fire Resist +30%', 'Damage Reduced By 7']
    ]),
    ('Prudence', ('Mal', 'Tir'), 2, ('Body Armor',), 49, '1.10', [
        ['+25% Faster Hit Recovery', '+140-170% Enhanced Defense', 'All Resistances +25-35', 'Damage Reduced by 3', 'Magic Damage Reduced by 17', '+2 To Mana After Each Kill', '+1 To Light Radius', 'Repairs Durability 1 In 4 Seconds']
    ]),
    ('Zephyr', ('Ort', 'Eth'), 2, ('Missile Weapons',), 21, None, [
        ['+33% Enhanced Damage', '+66 To Attack Rating', 'Adds 1-50 Lightning Damage', '-25% Target Defense', '+25 Defense', '25% Faster Run/Walk', '25% Increased Attack Speed', '7% Chance To Cast Level 1 Twister When Struck']
    ]),
    ("King's Grace", ('Amn', 'Ral', 'Thul'), 3, ('Swords', 'Scepters'), 25, None, [
        ['+100% Enhanced Damage', '+100% Damage To Demons', '+50% Damage To Undead', 'Adds 5-30 Fire Damage', 'Adds 3-14 Cold Damage - 3 Second Duration', '+150 To Attack Rating', '+100 To Attack Rating Against Demons', '+100 To Attack Rating Against Undead', '7% Life Stolen Per Hit']
    ]),
]

# (title, category, [(qty, ingredient)...], [(qty, output)...])
RECIPES = [
    ('Blood Ring', 'Crafting', [(1, 'Any Magic Ring'), (1, 'Sol'), (1, 'Perfect Ruby'), (1, 'Any Jewel')], [(1, 'Blood Ring')]),
    ('Cham', 'Rune upgrading', [(2, 'Jah'), (1, 'Flawless Ruby')], [(1, 'Cham')]),
    ('Renewed Flame Rift', 'Quest & special', [(1, 'Perfect Ruby'), (1, 'Io'), (1, 'Deep Worldstone Shard')], [(1, 'Renewed Flame Rift')]),
    ('Renewed Cold Rupture', 'Quest & special', [(1, 'Perfect Sapphire'), (1, 'Lum'), (1, 'Eastern Worldstone Shard')], [(1, 'Renewed Cold Rupture')]),
    ('Renewed Rotting Fissure', 'Quest & special', [(1, 'Perfect Emerald'), (1, 'Ko'), (1, 'Western Worldstone Shard')], [(1, 'Renewed Rotting Fissure')]),
    ('Renewed Crack of the Heavens', 'Quest & special', [(1, 'Perfect Topaz'), (1, 'Fal'), (1, 'Southern Worldstone Shard')], [(1, 'Renewed Crack of the Heavens')]),
    ('Renewed Black Cleft', 'Quest & special', [(1, 'Perfect Diamond'), (1, 'Mal'), (1, 'Southern Worldstone Shard'), (1, 'Deep Worldstone Shard'), (1, 'Northern Worldstone Shard')], [(1, 'Renewed Black Cleft')]),
    ('Renewed Bone Break', 'Quest & special', [(1, 'Perfect Amethyst'), (1, 'Pul'), (1, 'Northern Worldstone Shard')], [(1, 'Renewed Bone Break')]),
    ('Magic Shield of Spikes', 'Quest & special', [(1, 'Any Magic Shield'), (1, 'Spiked Club'), (2, 'Any Skull')], [(1, 'Magic Shield of Spikes')]),
    ('Socketed Magic Weapon ilvl 25', 'Socketing', [(3, 'Any Chipped Gem'), (1, 'Any Magic Weapon')], [(1, 'Socketed Magic Weapon (ilvl 25)')]),
    ('Prismatic Amulet', 'Quest & special', [(6, 'Perfect Gems (One of Each Type)'), (1, 'Any Magic Amulet')], [(1, 'Prismatic Amulet')]),
    ('Fully Repaired Armor', 'Repair & recharge', [(1, 'Ral'), (1, 'Armor to be repaired')], [(1, 'Fully Repaired Armor')]),
    ('Add Sockets to Normal Weapon', 'Socketing', [(1, 'Ral'), (1, 'Amn'), (1, 'Perfect Amethyst'), (1, 'Any Normal Weapon')], [(1, 'Normal Weapon with 1-6 Sockets')]),
    ('Portal to the Secret Cow Level', 'Quest & special', [(1, 'Tome of Town Portal'), (1, "Wirt's Leg")], [(1, 'Portal to the Secret Cow Level')]),
    ('Portal to Colossal Summit', 'Quest & special', [(1, "Talic's Anguish"), (1, "Korlic's Pain"), (1, "Madawc's Ire"), (1, "Bul-Kathos' Nightmare"), (1, "Worusk's End")], [(1, 'Portal to Colossal Summit')]),
    ('Exceptional Version of Unique Armor', 'Item upgrading', [(1, 'Tal'), (1, 'Shael'), (1, 'Perfect Diamond'), (1, 'Normal Unique Armor')], [(1, 'Exceptional Version of Armor')]),
    ('Blood Gloves', 'Crafting', [(1, 'Nef'), (1, 'Perfect Ruby'), (1, 'Any Jewel')], [(1, 'Blood Gloves')]),
    ('Caster Weapon', 'Crafting', [(1, 'Tir'), (1, 'Perfect Amethyst'), (1, 'Any Jewel')], [(1, 'Caster Weapon')]),
    ('Add Sockets to Normal Body Armor', 'Socketing', [(1, 'Tal'), (1, 'Thul'), (1, 'Perfect Topaz'), (1, 'Any Normal Body Armor')], [(1, 'Normal Body Armor with 1-4 Sockets')]),
    ('Hit Power Weapon', 'Crafting', [(1, 'Tir'), (1, 'Perfect Sapphire'), (1, 'Any Jewel')], [(1, 'Hit Power Weapon')]),
    ('Socketed Magic Weapon of Same Type', 'Socketing', [(3, 'Any Normal Gem'), (1, 'Any Socketed Weapon')], [(1, 'Socketed Magic Weapon of Same Type')]),
    ('Token of Absolution', 'Quest & special', [(1, 'Twisted Essence of Suffering'), (1, 'Charged Essence of Hatred'), (1, 'Burning Essence of Terror'), (1, 'Festering Essence of Destruction')], [(1, 'Token of Absolution')]),
    ('Low Quality Rare Item of Same Type', 'Quest & special', [(6, 'Perfect Skull'), (1, 'Any Rare Item')], [(1, 'Low Quality Rare Item of Same Type')]),
    ('Elite Version of Unique Armor', 'Item upgrading', [(1, 'Ko'), (1, 'Lem'), (1, 'Perfect Diamond'), (1, 'Exceptional Unique Armor')], [(1, 'Elite Version of Armor')]),
    ('Random Magic Item of Same Type', 'Rerolling', [(3, 'Perfect Gems'), (1, 'Any Magic Item')], [(1, 'Random Magic Item of Same Type')]),
    ('Elite Version of Unique Weapon', 'Item upgrading', [(1, 'Lum'), (1, 'Pul'), (1, 'Perfect Emerald'), (1, 'Exceptional Unique Weapon')], [(1, 'Elite Version of Weapon')]),
    ('Elite Version of Set Armor', 'Item upgrading', [(1, 'Ko'), (1, 'Lem'), (1, 'Perfect Diamond'), (1, 'Exceptional Set Armor')], [(1, 'Elite Version of Set Armor')]),
    ('Elite Version of Set Weapon', 'Item upgrading', [(1, 'Lum'), (1, 'Pul'), (1, 'Perfect Emerald'), (1, 'Exceptional Set Weapon')], [(1, 'Elite Version of Set Weapon')]),
    ('Exceptional Version of Rare Weapon', 'Item upgrading', [(1, 'Ort'), (1, 'Amn'), (1, 'Perfect Sapphire'), (1, 'Normal Rare Weapon')], [(1, 'Exceptional Rare Weapon')]),
    ('Exceptional Version of Rare Armor', 'Item upgrading', [(1, 'Ral'), (1, 'Thul'), (1, 'Perfect Amethyst'), (1, 'Normal Rare Armor')], [(1, 'Exceptional Rare Armor')]),
    ('Exceptional Version of Unique Weapon', 'Item upgrading', [(1, 'Ral'), (1, 'Sol'), (1, 'Perfect Emerald'), (1, 'Normal Unique Weapon')], [(1, 'Exceptional Version of Weapon')]),
    ('Elite Version of Rare Weapon', 'Item upgrading', [(1, 'Fal'), (1, 'Um'), (1, 'Perfect Sapphire'), (1, 'Exceptional Rare Weapon')], [(1, 'Elite Rare Weapon')]),
    ('Elite Version of Rare Armor', 'Item upgrading', [(1, 'Ko'), (1, 'Pul'), (1, 'Perfect Amethyst'), (1, 'Exceptional Rare Armor')], [(1, 'Elite Rare Armor')]),
    ('Exceptional Version of Set Weapon', 'Item upgrading', [(1, 'Ral'), (1, 'Sol'), (1, 'Perfect Emerald'), (1, 'Normal Set Weapon')], [(1, 'Exceptional Version of Set Weapon')]),
    ('Exceptional Version of Set Armor', 'Item upgrading', [(1, 'Tal'), (1, 'Shael'), (1, 'Perfect Diamond'), (1, 'Normal Set Armor')], [(1, 'Exceptional Version of Set Armor')]),
    ('Savage Polearm Class Weapon', 'Quest & special', [(1, 'Any Diamond'), (1, 'Any Staff'), (1, 'Kris'), (1, 'Belt')], [(1, 'Savage Polearm Class Weapon')]),
    ('Normal Quality Weapon of Same Type', 'Quest & special', [(1, 'Eld'), (1, 'Any Chipped Gem'), (1, 'Low Quality Weapon')], [(1, 'Normal Quality Weapon of Same Type')]),
    ('Normal Quality Armor of Same Type', 'Quest & special', [(1, 'El'), (1, 'Any Chipped Gem'), (1, 'Low Quality Armor')], [(1, 'Normal Quality Armor of Same Type')]),
    ('High Quality Rare Item of Same Type', 'Quest & special', [(1, 'Perfect Skull'), (1, 'Any Rare Item')], [(1, 'High Quality Rare Item of Same Type')]),
    ('Blood Weapon', 'Crafting', [(1, 'Ort'), (1, 'Perfect Ruby'), (1, 'Any Jewel')], [(1, 'Blood Weapon')]),
    ('Safety Weapon', 'Crafting', [(1, 'Sol'), (1, 'Perfect Emerald'), (1, 'Any Jewel')], [(1, 'Safety Weapon')]),
    ('Add 1 Socket to a Rare Item', 'Socketing', [(3, 'Perfect Skull'), (1, 'Any Rare Item')], [(1, 'Rare Item with 1 Socket')]),
    ('Remove All Items from Sockets', 'Socketing', [(1, 'Hel'), (1, 'Scroll of Town Portal'), (1, 'Any Socketed Item')], [(1, 'All Items Removed from Sockets')]),
    ('Caster Amulet', 'Crafting', [(1, 'Any Magic Amulet'), (1, 'Ral'), (1, 'Perfect Amethyst'), (1, 'Any Jewel')], [(1, 'Caster Amulet')]),
    ('Safety Shield', 'Crafting', [(1, 'Nef'), (1, 'Perfect Emerald'), (1, 'Any Jewel')], [(1, 'Safety Shield')]),
    ('Portal to Uber Tristram', 'Quest & special', [(1, "Mephisto's Brain"), (1, "Baal's Eye"), (1, "Diablo's Horn")], [(1, 'Portal to Uber Tristram')]),
    ('Hit Power Belt', 'Crafting', [(1, 'Tal'), (1, 'Perfect Sapphire'), (1, 'Any Jewel')], [(1, 'Hit Power Belt')]),
    ('Safety Belt', 'Crafting', [(1, 'Tal'), (1, 'Perfect Emerald'), (1, 'Any Jewel')], [(1, 'Safety Belt')]),
    ('Caster Belt', 'Crafting', [(1, 'Ith'), (1, 'Perfect Amethyst'), (1, 'Any Jewel')], [(1, 'Caster Belt')]),
    ('Blood Belt', 'Crafting', [(1, 'Tal'), (1, 'Perfect Ruby'), (1, 'Any Jewel')], [(1, 'Blood Belt')]),
    ('Hit Power Boots', 'Crafting', [(1, 'Ral'), (1, 'Perfect Sapphire'), (1, 'Any Jewel')], [(1, 'Hit Power Boots')]),
    ('Caster Boots', 'Crafting', [(1, 'Thul'), (1, 'Perfect Amethyst'), (1, 'Any Jewel')], [(1, 'Caster Boots')]),
    ('Safety Boots', 'Crafting', [(1, 'Ort'), (1, 'Perfect Emerald'), (1, 'Any Jewel')], [(1, 'Safety Boots')]),
    ('Blood Boots', 'Crafting', [(1, 'Eth'), (1, 'Perfect Ruby'), (1, 'Any Jewel')], [(1, 'Blood Boots')]),
    ('Caster Gloves', 'Crafting', [(1, 'Ort'), (1, 'Perfect Amethyst'), (1, 'Any Jewel')], [(1, 'Caster Gloves')]),
    ('Hit Power Gloves', 'Crafting', [(1, 'Ort'), (1, 'Perfect Sapphire'), (1, 'Any Jewel')], [(1, 'Hit Power Gloves')]),
    ('Safety Gloves', 'Crafting', [(1, 'Ral'), (1, 'Perfect Emerald'), (1, 'Any Jewel')], [(1, 'Safety Gloves')]),
    ('Safety Ring', 'Crafting', [(1, 'Any Magic Ring'), (1, 'Amn'), (1, 'Perfect Emerald'), (1, 'Any Jewel')], [(1, 'Safety Ring')]),
    ('Hit Power Ring', 'Crafting', [(1, 'Any Magic Ring'), (1, 'Amn'), (1, 'Perfect Sapphire'), (1, 'Any Jewel')], [(1, 'Hit Power Ring')]),
    ('Caster Ring', 'Crafting', [(1, 'Any Magic Ring'), (1, 'Amn'), (1, 'Perfect Amethyst'), (1, 'Any Jewel')], [(1, 'Caster Ring')]),
    ('Blood Amulet', 'Crafting', [(1, 'Any Magic Amulet'), (1, 'Amn'), (1, 'Perfect Ruby'), (1, 'Any Jewel')], [(1, 'Blood Amulet')]),
    ('Safety Amulet', 'Crafting', [(1, 'Any Magic Amulet'), (1, 'Thul'), (1, 'Perfect Emerald'), (1, 'Any Jewel')], [(1, 'Safety Amulet')]),
    ('Hit Power Amulet', 'Crafting', [(1, 'Any Magic Amulet'), (1, 'Thul'), (1, 'Perfect Sapphire'), (1, 'Any Jewel')], [(1, 'Hit Power Amulet')]),
    ('Socketed Magic Weapon ilvl 30', 'Socketing', [(3, 'Any Flawless Gem'), (1, 'Any Magic Weapon')], [(1, 'Socketed Magic Weapon (ilvl 30)')]),
    ("Portal to Matron's Den", 'Quest & special', [(1, 'Key of Hate'), (1, 'Key of Terror'), (1, 'Key of Destruction')], [(1, "Portal to Matron's Den")]),
    ('Portal to Furnace of Pain', 'Quest & special', [(1, 'Key of Hate'), (1, 'Key of Terror'), (1, 'Key of Destruction')], [(1, 'Portal to Furnace of Pain')]),
    ('Portal to Forgotten Sands', 'Quest & special', [(1, 'Key of Hate'), (1, 'Key of Terror'), (1, 'Key of Destruction')], [(1, 'Portal to Forgotten Sands')]),
    ('Caster Helm', 'Crafting', [(1, 'Nef'), (1, 'Perfect Amethyst'), (1, 'Any Jewel')], [(1, 'Caster Helm')]),
    ("Khalim's Will", 'Quest & special', [(1, "Khalim's Eye"), (1, "Khalim's Brain"), (1, "Khalim's Heart"), (1, "Khalim's Flail")], [(1, "Khalim's Will")]),
    ('Horadric Staff', 'Quest & special', [(1, 'Amulet of the Viper'), (1, 'Staff of Kings')], [(1, 'Horadric Staff')]),
    ('Blood Helm', 'Crafting', [(1, 'Ral'), (1, 'Perfect Ruby'), (1, 'Any Jewel')], [(1, 'Blood Helm')]),
    ('Safety Body', 'Crafting', [(1, 'Eth'), (1, 'Perfect Emerald'), (1, 'Any Jewel')], [(1, 'Safety Body')]),
    ('Safety Helm', 'Crafting', [(1, 'Ith'), (1, 'Perfect Emerald'), (1, 'Any Jewel')], [(1, 'Safety Helm')]),
    ('Caster Body', 'Crafting', [(1, 'Tal'), (1, 'Perfect Amethyst'), (1, 'Any Jewel')], [(1, 'Caster Body')]),
    ('Caster Shield', 'Crafting', [(1, 'Eth'), (1, 'Perfect Amethyst'), (1, 'Any Jewel')], [(1, 'Caster Shield')]),
    ('Blood Body', 'Crafting', [(1, 'Thul'), (1, 'Perfect Ruby'), (1, 'Any Jewel')], [(1, 'Blood Body')]),
    ('Blood Shield', 'Crafting', [(1, 'Ith'), (1, 'Perfect Ruby'), (1, 'Any Jewel')], [(1, 'Blood Shield')]),
    ('Hit Power Body', 'Crafting', [(1, 'Nef'), (1, 'Perfect Sapphire'), (1, 'Any Jewel')], [(1, 'Hit Power Body')]),
    ('Hit Power Shield', 'Crafting', [(1, 'Eth'), (1, 'Perfect Sapphire'), (1, 'Any Jewel')], [(1, 'Hit Power Shield')]),
    ('Hit Power Helm', 'Crafting', [(1, 'Ith'), (1, 'Perfect Sapphire'), (1, 'Any Jewel')], [(1, 'Hit Power Helm')]),
    ('Cobalt Ring', 'Quest & special', [(1, 'Any Magic Ring'), (1, 'Perfect Sapphire'), (1, 'Thawing Potion')], [(1, 'Cobalt Ring')]),
    ('Coral Ring', 'Quest & special', [(1, 'Any Magic Ring'), (1, 'Perfect Topaz'), (1, 'Rejuvenation Potion')], [(1, 'Coral Ring')]),
    ('Garnet Ring', 'Quest & special', [(1, 'Any Magic Ring'), (1, 'Perfect Ruby'), (1, 'Exploding Potion')], [(1, 'Garnet Ring')]),
    ('Jade Ring', 'Quest & special', [(1, 'Any Magic Ring'), (1, 'Perfect Emerald'), (1, 'Antidote Potion')], [(1, 'Jade Ring')]),
    ('Add Sockets to Normal Shield', 'Socketing', [(1, 'Tal'), (1, 'Amn'), (1, 'Perfect Ruby'), (1, 'Any Normal Shield')], [(1, 'Normal Shield with 1-4 Sockets')]),
    ('Add Sockets to Normal Helm', 'Socketing', [(1, 'Ral'), (1, 'Thul'), (1, 'Perfect Sapphire'), (1, 'Any Normal Helm')], [(1, 'Normal Helm with 1-3 Sockets')]),
    ('Fully Repaired and Recharged Armor', 'Repair & recharge', [(1, 'Ral'), (1, 'Any Flawed Gem'), (1, 'Armor to be repaired')], [(1, 'Fully Repaired and Recharged Armor')]),
    ('Fully Repaired and Recharged Weapon', 'Repair & recharge', [(1, 'Ort'), (1, 'Any Chipped Gem'), (1, 'Weapon to be repaired')], [(1, 'Fully Repaired and Recharged Weapon')]),
    ('Random Magic Ring', 'Rerolling', [(3, 'Magic Amulet')], [(1, 'Magic Ring')]),
    ('Random Magic Amulet', 'Rerolling', [(3, 'Magic Ring')], [(1, 'Magic Amulet')]),
    ('Magic Sword of the Leech', 'Quest & special', [(4, 'Any Healing Potion'), (1, 'Any Ruby'), (1, 'Any Magic Sword')], [(1, 'Magic Sword of the Leech')]),
    ('Full Rejuvenation Potion (Alternative)', 'Quest & special', [(3, 'Any Healing Potion'), (3, 'Any Mana Potion'), (1, 'Any Normal Gem')], [(1, 'Full Rejuvenation Potion')]),
    ('Rejuvenation Potion', 'Quest & special', [(3, 'Any Healing Potion'), (3, 'Any Mana Potion'), (1, 'Any Chipped Gem')], [(1, 'Rejuvenation Potion')]),
    ('Antidote Potion', 'Quest & special', [(1, 'Strangling Gas Potion'), (1, 'Any Healing Potion')], [(1, 'Antidote Potion')]),
    ('Throwing Axe', 'Quest & special', [(1, 'Axe'), (1, 'Dagger')], [(1, 'Throwing Axe')]),
    ('Javelin', 'Quest & special', [(1, 'Spear'), (1, 'Arrows')], [(1, 'Javelin')]),
    ('Arrows', 'Quest & special', [(2, 'Bolts')], [(1, 'Arrows')]),
    ('Bolts', 'Quest & special', [(2, 'Arrows')], [(1, 'Bolts')]),
    ('Zod', 'Rune upgrading', [(2, 'Cham'), (1, 'Flawless Emerald')], [(1, 'Zod')]),
    ('Jah', 'Rune upgrading', [(2, 'Ber'), (1, 'Flawless Sapphire')], [(1, 'Jah')]),
    ('Ber', 'Rune upgrading', [(2, 'Sur'), (1, 'Flawless Amethyst')], [(1, 'Ber')]),
    ('Sur', 'Rune upgrading', [(2, 'Lo'), (1, 'Flawless Topaz')], [(1, 'Sur')]),
    ('Lo', 'Rune upgrading', [(2, 'Ohm'), (1, 'Diamond')], [(1, 'Lo')]),
    ('Ohm', 'Rune upgrading', [(2, 'Vex'), (1, 'Emerald')], [(1, 'Ohm')]),
    ('Vex', 'Rune upgrading', [(2, 'Gul'), (1, 'Ruby')], [(1, 'Vex')]),
    ('Gul', 'Rune upgrading', [(2, 'Ist'), (1, 'Sapphire')], [(1, 'Gul')]),
    ('Ist', 'Rune upgrading', [(2, 'Mal'), (1, 'Amethyst')], [(1, 'Ist')]),
    ('Mal', 'Rune upgrading', [(2, 'Um'), (1, 'Topaz')], [(1, 'Mal')]),
    ('Um', 'Rune upgrading', [(2, 'Pul'), (1, 'Flawed Diamond')], [(1, 'Um')]),
    ('Pul', 'Rune upgrading', [(3, 'Lem'), (1, 'Flawed Emerald')], [(1, 'Pul')]),
    ('Lem', 'Rune upgrading', [(3, 'Fal'), (1, 'Flawed Ruby')], [(1, 'Lem')]),
    ('Fal', 'Rune upgrading', [(3, 'Ko'), (1, 'Flawed Sapphire')], [(1, 'Fal')]),
    ('Ko', 'Rune upgrading', [(3, 'Lum'), (1, 'Flawed Amethyst')], [(1, 'Ko')]),
    ('Io', 'Rune upgrading', [(3, 'Hel'), (1, 'Chipped Diamond')], [(1, 'Io')]),
    ('Hel', 'Rune upgrading', [(3, 'Dol'), (1, 'Chipped Emerald')], [(1, 'Hel')]),
    ('Dol', 'Rune upgrading', [(3, 'Shael'), (1, 'Chipped Ruby')], [(1, 'Dol')]),
    ('Shael', 'Rune upgrading', [(3, 'Sol'), (1, 'Chipped Sapphire')], [(1, 'Shael')]),
    ('Sol', 'Rune upgrading', [(3, 'Amn'), (1, 'Chipped Amethyst')], [(1, 'Sol')]),
    ('Ral', 'Rune upgrading', [(3, 'Tal')], [(1, 'Ral')]),
    ('Ith', 'Rune upgrading', [(3, 'Eth')], [(1, 'Ith')]),
    ('Eth', 'Rune upgrading', [(3, 'Nef')], [(1, 'Eth')]),
    ('Nef', 'Rune upgrading', [(3, 'Tir')], [(1, 'Nef')]),
    ('Tir', 'Rune upgrading', [(3, 'Eld')], [(1, 'Tir')]),
    ('Eld', 'Rune upgrading', [(3, 'El')], [(1, 'Eld')]),
    ('Perfect Topaz', 'Gem upgrading', [(3, 'Flawless Topaz')], [(1, 'Perfect Topaz')]),
    ('Perfect Diamond', 'Gem upgrading', [(3, 'Flawless Diamond')], [(1, 'Perfect Diamond')]),
    ('Perfect Ruby', 'Gem upgrading', [(3, 'Flawless Ruby')], [(1, 'Perfect Ruby')]),
    ('Perfect Emerald', 'Gem upgrading', [(3, 'Flawless Emerald')], [(1, 'Perfect Emerald')]),
    ('Perfect Amethyst', 'Gem upgrading', [(3, 'Flawless Amethyst')], [(1, 'Perfect Amethyst')]),
    ('Perfect Skull', 'Gem upgrading', [(3, 'Flawless Skull')], [(1, 'Perfect Skull')]),
    ('Flawless Topaz', 'Gem upgrading', [(3, 'Topaz')], [(1, 'Flawless Topaz')]),
    ('Flawless Diamond', 'Gem upgrading', [(3, 'Diamond')], [(1, 'Flawless Diamond')]),
    ('Flawless Ruby', 'Gem upgrading', [(3, 'Ruby')], [(1, 'Flawless Ruby')]),
    ('Flawless Emerald', 'Gem upgrading', [(3, 'Emerald')], [(1, 'Flawless Emerald')]),
    ('Flawless Sapphire', 'Gem upgrading', [(3, 'Sapphire')], [(1, 'Flawless Sapphire')]),
    ('Flawless Amethyst', 'Gem upgrading', [(3, 'Amethyst')], [(1, 'Flawless Amethyst')]),
    ('Flawless Skull', 'Gem upgrading', [(3, 'Skull')], [(1, 'Flawless Skull')]),
    ('Topaz', 'Gem upgrading', [(3, 'Flawed Topaz')], [(1, 'Topaz')]),
    ('Diamond', 'Gem upgrading', [(3, 'Flawed Diamond')], [(1, 'Diamond')]),
    ('Ruby', 'Gem upgrading', [(3, 'Flawed Ruby')], [(1, 'Ruby')]),
    ('Emerald', 'Gem upgrading', [(3, 'Flawed Emerald')], [(1, 'Emerald')]),
    ('Sapphire', 'Gem upgrading', [(3, 'Flawed Sapphire')], [(1, 'Sapphire')]),
    ('Amethyst', 'Gem upgrading', [(3, 'Flawed Amethyst')], [(1, 'Amethyst')]),
    ('Skull', 'Gem upgrading', [(3, 'Flawed Skull')], [(1, 'Skull')]),
    ('Flawed Diamond', 'Gem upgrading', [(3, 'Chipped Diamond')], [(1, 'Flawed Diamond')]),
    ('Flawed Ruby', 'Gem upgrading', [(3, 'Chipped Ruby')], [(1, 'Flawed Ruby')]),
    ('Flawed Emerald', 'Gem upgrading', [(3, 'Chipped Emerald')], [(1, 'Flawed Emerald')]),
    ('Flawed Sapphire', 'Gem upgrading', [(3, 'Chipped Sapphire')], [(1, 'Flawed Sapphire')]),
    ('Flawed Amethyst', 'Gem upgrading', [(3, 'Chipped Amethyst')], [(1, 'Flawed Amethyst')]),
    ('Flawed Skull', 'Gem upgrading', [(3, 'Chipped Skull')], [(1, 'Flawed Skull')]),
    ('Fully repaired weapon', 'Repair & recharge', [(1, 'Weapon to be repaired'), (1, 'Ort')], [(1, 'Fully repaired weapon')]),
    ('Lum', 'Rune upgrading', [(3, 'Io'), (1, 'Flawed Topaz')], [(1, 'Lum')]),
    ('Full Rejuvenation Potion', 'Quest & special', [(3, 'Rejuvenation Potion')], [(1, 'Full Rejuvenation Potion')]),
    ('Perfect Sapphire', 'Gem upgrading', [(3, 'Flawless Sapphire')], [(1, 'Perfect Sapphire')]),
    ('Flawed Topaz', 'Gem upgrading', [(3, 'Chipped Topaz')], [(1, 'Flawed Topaz')]),
    ('Amn', 'Rune upgrading', [(3, 'Thul'), (1, 'Chipped Topaz')], [(1, 'Amn')]),
    ('Ort', 'Rune upgrading', [(3, 'Ral')], [(1, 'Ort')]),
    ('Thul', 'Rune upgrading', [(3, 'Ort')], [(1, 'Thul')]),
    ('Tal', 'Rune upgrading', [(3, 'Ith')], [(1, 'Tal')]),
]


# The 33 runes in the order the D2R runes tab shows them (row-major, 9 per row)
RUNES = [
    "El", "Eld", "Tir", "Nef", "Eth", "Ith", "Tal", "Ral", "Ort",
    "Thul", "Amn", "Sol", "Shael", "Dol", "Hel", "Io", "Lum", "Ko",
    "Fal", "Lem", "Pul", "Um", "Mal", "Ist", "Gul", "Vex", "Ohm",
    "Lo", "Sur", "Ber", "Jah", "Cham", "Zod",
]


# Guaranteed ("fixed") properties the craft always rolls, keyed by recipe
# title. On top of these, every craft also gets 1-4 random affixes from
# the magic/rare pool — how many depends on the output item level
# (ilvl 1-30: up to 4, ilvl 31+: 3-4, ilvl 71+: always 4; max 3 prefixes
# and 3 suffixes).
CRAFT_ROLLS = {
    # ---- Blood (Perfect Ruby) -------------------------------------
    'Blood Weapon':   ['+35-60% Enhanced Damage',
                       '1-4% Life Stolen Per Hit', '+10-20 To Life'],
    'Blood Shield':   ['1-3% Life Stolen Per Hit', '+10-20 To Life',
                       'Attacker Takes Damage of 4-7'],
    'Blood Helm':     ['1-3% Life Stolen Per Hit', '5-10% Deadly Strike',
                       '+10-20 To Life'],
    'Blood Body':     ['1-3% Life Stolen Per Hit', '+10-20 To Life',
                       '+1-3 Life After Each Demon Kill'],
    'Blood Gloves':   ['1-3% Life Stolen Per Hit', '5-10% Chance of Crushing Blow',
                       '+10-20 To Life'],
    'Blood Belt':     ['1-3% Life Stolen Per Hit', '5-10% Chance of Open Wounds',
                       '+10-20 To Life'],
    'Blood Boots':    ['1-3% Life Stolen Per Hit', '+10-20 To Life',
                       'Replenish Life +5-10'],
    'Blood Amulet':   ['+5-10% Faster Run/Walk', '1-4% Life Stolen Per Hit',
                       '+10-20 To Life'],
    'Blood Ring':     ['1-3% Life Stolen Per Hit', '+1-5 To Strength',
                       '+10-20 To Life'],
    # ---- Caster (Perfect Amethyst) ---------------------------------
    'Caster Weapon':  ['Increase Maximum Mana 1-5%', 'Regenerate Mana 4-10%',
                       '+10-20 To Mana'],
    'Caster Shield':  ['+5-10% Increased Chance of Blocking',
                       'Regenerate Mana 4-10%', '+10-20 To Mana'],
    'Caster Helm':    ['1-4% Mana Stolen Per Hit', 'Regenerate Mana 4-10%',
                       '+10-20 To Mana'],
    'Caster Body':    ['Regenerate Mana 4-10%', '+10-20 To Mana',
                       '+1-3 Mana After Each Kill'],
    'Caster Gloves':  ['Regenerate Mana 4-10%', '+10-20 To Mana',
                       '+1-3 Mana After Each Kill'],
    'Caster Belt':    ['+5-10% Faster Cast Rate', 'Regenerate Mana 4-10%',
                       '+10-20 To Mana'],
    'Caster Boots':   ['Increase Maximum Mana 2-5%', 'Regenerate Mana 4-10%',
                       '+10-20 To Mana'],
    'Caster Amulet':  ['+5-10% Faster Cast Rate', 'Regenerate Mana 4-10%',
                       '+10-20 To Mana'],
    'Caster Ring':    ['+1-5 To Energy', 'Regenerate Mana 4-10%',
                       '+10-20 To Mana'],
    # ---- Hit Power (Perfect Sapphire) ------------------------------
    'Hit Power Weapon': ['5% Chance to Cast Level 4 Frost Nova When Struck',
                         '+35-60% Enhanced Damage',
                         'Attacker Takes Damage of 3-7'],
    'Hit Power Shield': ['5% Chance to Cast Level 4 Frost Nova When Struck',
                         '+5-10% Increased Chance of Blocking',
                         'Attacker Takes Damage of 3-10'],
    'Hit Power Helm':   ['5% Chance to Cast Level 4 Frost Nova When Struck',
                         '+25-50 Defense vs. Missile',
                         'Attacker Takes Damage of 3-7'],
    'Hit Power Body':   ['5% Chance to Cast Level 4 Frost Nova When Struck',
                         '+10-20% Faster Hit Recovery',
                         'Attacker Takes Damage of 3-10'],
    'Hit Power Gloves': ['5% Chance to Cast Level 4 Frost Nova When Struck',
                         'Knockback', 'Attacker Takes Damage of 3-7'],
    'Hit Power Belt':   ['5% Chance to Cast Level 4 Frost Nova When Struck',
                         'Attacker Takes Damage of 3-7',
                         '5-10% Damage Taken Goes to Mana'],
    'Hit Power Boots':  ['5% Chance to Cast Level 4 Frost Nova When Struck',
                         '+25-50 Defense vs. Missile',
                         'Attacker Takes Damage of 3-7'],
    'Hit Power Amulet': ['5% Chance to Cast Level 4 Frost Nova When Struck',
                         'Hit Causes Monster to Flee 3-11%',
                         'Attacker Takes Damage of 3-10'],
    'Hit Power Ring':   ['5% Chance to Cast Level 4 Frost Nova When Struck',
                         '+1-5 To Dexterity', 'Attacker Takes Damage of 3-6'],
    # ---- Safety (Perfect Emerald) ----------------------------------
    'Safety Weapon':  ['+5-10% Enhanced Defense', 'Magic Damage Reduced by 1-2',
                       'Damage Reduced by 1-4'],
    'Safety Shield':  ['+10-30% Enhanced Defense', 'Magic Resist +5-10%',
                       'Magic Damage Reduced by 1-2', 'Damage Reduced by 1-4'],
    'Safety Helm':    ['+10-30% Enhanced Defense', 'Lightning Resist +5-10%',
                       'Magic Damage Reduced by 1-2', 'Damage Reduced by 1-4'],
    'Safety Body':    ['+10-30% Enhanced Defense', 'Magic Damage Reduced by 1-2',
                       'Damage Reduced by 1-4', 'Half Freeze Duration'],
    'Safety Gloves':  ['+10-30% Enhanced Defense', 'Cold Resist +5-10%',
                       'Magic Damage Reduced by 1-2', 'Damage Reduced by 1-4'],
    'Safety Belt':    ['+10-30% Enhanced Defense', 'Poison Resist +5-10%',
                       'Magic Damage Reduced by 1-2', 'Damage Reduced by 1-4'],
    'Safety Boots':   ['+10-30% Enhanced Defense', 'Fire Resist +5-10%',
                       'Magic Damage Reduced by 1-2', 'Damage Reduced by 1-4'],
    'Safety Amulet':  ['+1-10% Increased Chance of Blocking',
                       'Magic Damage Reduced by 1-2', 'Damage Reduced by 1-4'],
    'Safety Ring':    ['+1-5 To Vitality', 'Magic Damage Reduced by 1-2',
                       'Damage Reduced by 1-4'],
}
