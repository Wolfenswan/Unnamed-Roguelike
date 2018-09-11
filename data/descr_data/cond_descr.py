from data.shared_data.types_data import Material, ItemType, Condition


# Default description strings
default_descr = {
    'poor': (),
    'normal': ('It is in a fairly ordinary condition.',
                'There is nothing remarkable about its condition.'),
    'good': (),
    'legend': ()
}


cond_descr_data = {
    ItemType.WEAPON: {
        Material.OAK: {
            Condition.POOR: (
                'You are worried it might snap at any second.',
                "It is terribly splintered, but at least the enemy might loose an eye when it breaks."
            ),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (
                'The wood seems sturdy and in good condition.',
                'The wood has been spared by worms and is in nearly mint condition.'
            ),
            Condition.LEGENDARY: ()
        },
        Material.IRON: {
            Condition.POOR:(
                'If you are lucky, all that rust might poison the enemy.',
                'It is so rusted, you are not sure if using wood would be sturdier.'
            ),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (
                'It is well honed and the edges are still sharp.',
                'You reckon it will fell your foes easily.'
            ),
            Condition.LEGENDARY: ()
        },
        Material.STEEL: {
            Condition.POOR:(
                'If you are lucky, all that rust might poison the enemy.',
                'It is so rusted, you are not sure if using wood would be sturdier.'
            ),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (
                'It is well honed and the edges are still sharp.',
                'You reckon it will fell your foes easily.'
            ),
            Condition.LEGENDARY: ()
        }
    },
    ItemType.ARMOR: {
        Material.OAK: {
            Condition.POOR: (
                'You are worried it might snap at any second.',
                "It is terribly splintered, but at least the enemy might loose an eye when it breaks."
            ),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: ()
        },
        Material.LEATHER: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: ()
        },
        Material.LINEN: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: ()
        },
        Material.IRON: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: ()
        },
        Material.STEEL: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: ()
        }},
    ItemType.SHIELD: {
        Material.OAK: {
            Condition.POOR: (
                'However, calling this worm-riddled plank a "shield" is rather generous.',
                "You wonder if the splinters in your hand are worth the dubious protection it offers."
            ),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: ()
        },
        Material.LEATHER: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: ()
        },
        Material.IRON: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: ()
        },
        Material.STEEL: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: ()
        }}
}

# Old name list #
# 'names': {
        #     Material.OAK: 'splintered',
        #     Material.LINEN: 'frayed',
        #     Material.WOOL: 'frayed',
        #     Material.LEATHER: 'brittle',
        #     Material.IRON: 'rusty',
        #     Material.STEEL: 'rusty'
        # },
# 'names': {
        #     Material.OAK: 'sturdy',
        #     Material.LINEN: 'well fitting',
        #     Material.WOOL: 'well fitting',
        #     Material.LEATHER: 'hardened',
        #     Material.IRON: 'well honed',
        #     Material.STEEL: 'well honed'
        # },