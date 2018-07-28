class Item:
    def __init__(self, use_function = None, targeting=False, on_use_msg=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.on_use_msg = on_use_msg
        self.function_kwargs = kwargs