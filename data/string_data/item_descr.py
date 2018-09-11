from data.data_types import Material, ItemType, Condition

MISSING_DESCR = '(Quality description missing)'

item_descr_data = {
    ItemType.WEAPON: {
        Material.OAK: {
            Condition.POOR: (
                    'You are worried it might snap at any second.',
                    "It is terribly splintered, but at least the enemy might loose an eye when it breaks."
                        ),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.LEATHER: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.COTTON: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.LINEN: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.IRON: {
            Condition.POOR:(
                'If you are lucky, all that rust might poison the enemy.',
                'It is so rusted, you are not sure if using wood would be sturdier.'
                                     ),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.STEEL: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        }
    },
    ItemType.BELT : {
        Material.LEATHER: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.COTTON: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.LINEN: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.IRON: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.STEEL: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        }},
    ItemType.ARMOR: {
        Material.OAK: {
            Condition.POOR: ('You are worried it might snap at any second.',
                          "It is terribly splintered, but at least the enemy might loose an eye when it breaks."
                        ),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.LEATHER: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.COTTON: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.LINEN: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.IRON: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.STEEL: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        }},
    ItemType.SHIELD: {
        Material.OAK: {
            Condition.POOR: ('However, calling this worm-riddled plank a "shield" is rather generous.',
                          "You wonder if the splinters in your hand are worth the dubious protection it offers."
                        ),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.LEATHER: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.COTTON: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.LINEN: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.IRON: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        },
        Material.STEEL: {
            Condition.POOR:(MISSING_DESCR,),
            Condition.NORMAL:(MISSING_DESCR,),
            Condition.GOOD: (MISSING_DESCR,),
            Condition.LEGENDARY: (MISSING_DESCR,)
        }}
}