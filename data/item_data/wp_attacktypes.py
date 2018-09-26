from data.data_types import AttackType

wp_attacktypes_data = {
    AttackType.NORMAL : {},
    AttackType.HEAVY: {
      'block_sta_dmg_multipl': 2
    },
    AttackType.QUICK: {
        'block_def_multipl': 0
    }
}