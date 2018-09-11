from data.data_types import Material, ItemType, Condition

item_descr_data = {
    ItemType.WEAPON: {
        Material.OAK: {
            Condition.POOR: {
                'descr': (
                    'You are worried it might snap at any second.',
                    "It is terribly splintered, but at least the enemy might loose an eye when it breaks."
                        )
            },
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.LEATHER: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.COTTON: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.LINEN: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.IRON: {
            Condition.POOR:{'descr':(
                'If you are lucky, all that rust might poison the enemy',
                'It is so rusted, you are not sure if using wood would be sturdier.'
                                     )},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.STEEL: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        }
    },
    ItemType.BELT : {
        Material.LEATHER: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.COTTON: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.LINEN: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.IRON: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.STEEL: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        }},
    ItemType.ARMOR: {
        Material.OAK: {
            Condition.POOR: {
                'descr': ('You are worried it might snap at any second.',
                          "It is terribly splintered, but at least the enemy might loose an eye when it breaks."
                        )
            },
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.LEATHER: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.COTTON: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.LINEN: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.IRON: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.STEEL: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        }},
    ItemType.OFFHAND: {
        Material.OAK: {
            Condition.POOR: {
                'descr': ('However, calling this worm-riddled plank a "shield" is rather generous.',
                          "You wonder if the splinters in your hand are worth the dubious protection it offers."
                        )
            },
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.LEATHER: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.COTTON: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.LINEN: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.IRON: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        },
        Material.STEEL: {
            Condition.POOR:{'descr':('No description',)},
            Condition.NORMAL:{'descr':('No description',)},
            Condition.GOOD: {'descr':('No description',)},
            Condition.LEGENDARY: {'descr':('No description',)}
        }}
}