from data.shared_data.types_data import Material, Craftsmanship

# Default string for a missing description
MISSING_DESCR = ('(Craftsmanship description missing)',)

POOR_DESCR = ('It seems to be the work of an amateur.',
              'A very untalented child appears to be the creator.')

craft_name_data = {
    Craftsmanship.POOR: 'shoddy',
    Craftsmanship.GOOD: 'refined',
    Craftsmanship.LEGENDARY: 'bespoke'
}

craft_descr_data = {
    Material.OAK: {
        Craftsmanship.POOR: POOR_DESCR,
        Craftsmanship.NORMAL: MISSING_DESCR,
        Craftsmanship.GOOD: MISSING_DESCR,
        Craftsmanship.LEGENDARY: MISSING_DESCR
    },
    Material.LINEN: {
        Craftsmanship.POOR: POOR_DESCR,
        Craftsmanship.NORMAL: MISSING_DESCR,
        Craftsmanship.GOOD: MISSING_DESCR,
        Craftsmanship.LEGENDARY: MISSING_DESCR
    },
    Material.LEATHER: {
        Craftsmanship.POOR: POOR_DESCR,
        Craftsmanship.NORMAL: MISSING_DESCR,
        Craftsmanship.GOOD: MISSING_DESCR,
        Craftsmanship.LEGENDARY: MISSING_DESCR
    },
    Material.IRON: {
        Craftsmanship.POOR: POOR_DESCR,
        Craftsmanship.NORMAL: MISSING_DESCR,
        Craftsmanship.GOOD: MISSING_DESCR,
        Craftsmanship.LEGENDARY: MISSING_DESCR
    },
    Material.STEEL: {
        Craftsmanship.POOR: POOR_DESCR,
        Craftsmanship.NORMAL: MISSING_DESCR,
        Craftsmanship.GOOD: MISSING_DESCR,
        Craftsmanship.LEGENDARY: MISSING_DESCR
    }
}