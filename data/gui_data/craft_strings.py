from data.data_types import Material, Craftsmanship

# Default description strings
default_descr = {
    'poor': ('It seems to be the work of an amateur.',
              'It is very possbile that it was created by an untalented child.'),
    'normal': (),
    'good': (),
    'legend': ()
}


craft_name_data = {
    Craftsmanship.POOR: 'shoddy',
    Craftsmanship.GOOD: 'refined',
    Craftsmanship.LEGENDARY: 'bespoke'
}


craft_descr_data = {
    Material.OAK: {
        Craftsmanship.POOR: default_descr['poor'],
        Craftsmanship.NORMAL: (),
        Craftsmanship.GOOD: (),
        Craftsmanship.LEGENDARY: ()
    },
    Material.LINEN: {
        Craftsmanship.POOR: default_descr['poor'],
        Craftsmanship.NORMAL: (),
        Craftsmanship.GOOD: (),
        Craftsmanship.LEGENDARY: ()
    },
    Material.LEATHER: {
        Craftsmanship.POOR: default_descr['poor'],
        Craftsmanship.NORMAL: (),
        Craftsmanship.GOOD: (),
        Craftsmanship.LEGENDARY: ()
    },
    Material.IRON: {
        Craftsmanship.POOR: default_descr['poor'],
        Craftsmanship.NORMAL: (),
        Craftsmanship.GOOD: (),
        Craftsmanship.LEGENDARY: ()
    },
    Material.STEEL: {
        Craftsmanship.POOR: default_descr['poor'],
        Craftsmanship.NORMAL: (),
        Craftsmanship.GOOD: (),
        Craftsmanship.LEGENDARY: ()
    }
}