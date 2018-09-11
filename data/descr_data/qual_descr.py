from data.data_types import Material, ItemType, Condition

# Default string for a missing description
MISSING_DESCR = ('(Quality description missing)',)

# Default description for normal condition
NORMAL_DESCR =  (
                'It is in a fairly ordinary condition.',
                'There is nothing remarkable about its condition.'
                )

qual_descr_data = {
    ItemType.WEAPON: {
        Material.OAK: {
            Condition.POOR: (
                'You are worried it might snap at any second.',
                "It is terribly splintered, but at least the enemy might loose an eye when it breaks."
            ),
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: (
                'The wood seems sturdy and in good condition.',
                'The wood has been spared by worms and is in nearly mint condition.'
            ),
            Condition.LEGENDARY: MISSING_DESCR
        },
        Material.IRON: {
            Condition.POOR:(
                'If you are lucky, all that rust might poison the enemy.',
                'It is so rusted, you are not sure if using wood would be sturdier.'
            ),
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: (
                'It is well honed and the edges are still sharp.',
                'You reckon it will fell your foes easily.'
            ),
            Condition.LEGENDARY: MISSING_DESCR
        },
        Material.STEEL: {
            Condition.POOR:(
                'If you are lucky, all that rust might poison the enemy.',
                'It is so rusted, you are not sure if using wood would be sturdier.'
            ),
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: (
                'It is well honed and the edges are still sharp.',
                'You reckon it will fell your foes easily.'
            ),
            Condition.LEGENDARY: MISSING_DESCR
        }
    },
    ItemType.ARMOR: {
        Material.OAK: {
            Condition.POOR: (
                'You are worried it might snap at any second.',
                "It is terribly splintered, but at least the enemy might loose an eye when it breaks."
            ),
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: MISSING_DESCR,
            Condition.LEGENDARY: MISSING_DESCR
        },
        Material.LEATHER: {
            Condition.POOR:MISSING_DESCR,
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: MISSING_DESCR,
            Condition.LEGENDARY: MISSING_DESCR
        },
        # Material.WOOL: {
        #     Condition.POOR:MISSING_DESCR,
        #     Condition.NORMAL: NORMAL_DESCR,
        #     Condition.GOOD: MISSING_DESCR,
        #     Condition.LEGENDARY: MISSING_DESCR
        # },
        Material.LINEN: {
            Condition.POOR:MISSING_DESCR,
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: MISSING_DESCR,
            Condition.LEGENDARY: MISSING_DESCR
        },
        Material.IRON: {
            Condition.POOR:MISSING_DESCR,
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: MISSING_DESCR,
            Condition.LEGENDARY: MISSING_DESCR
        },
        Material.STEEL: {
            Condition.POOR:MISSING_DESCR,
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: MISSING_DESCR,
            Condition.LEGENDARY: MISSING_DESCR
        }},
    ItemType.SHIELD: {
        Material.OAK: {
            Condition.POOR: (
                'However, calling this worm-riddled plank a "shield" is rather generous.',
                "You wonder if the splinters in your hand are worth the dubious protection it offers."
            ),
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: MISSING_DESCR,
            Condition.LEGENDARY: MISSING_DESCR
        },
        Material.LEATHER: {
            Condition.POOR:MISSING_DESCR,
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: MISSING_DESCR,
            Condition.LEGENDARY: MISSING_DESCR
        },
        Material.IRON: {
            Condition.POOR:MISSING_DESCR,
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: MISSING_DESCR,
            Condition.LEGENDARY: MISSING_DESCR
        },
        Material.STEEL: {
            Condition.POOR:MISSING_DESCR,
            Condition.NORMAL: NORMAL_DESCR,
            Condition.GOOD: MISSING_DESCR,
            Condition.LEGENDARY: MISSING_DESCR
        }}
}