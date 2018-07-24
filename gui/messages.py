from enum import Enum, auto

from config_files import cfg as cfg

import textwrap

class MessageType(Enum):
    """ sets the type of the message """
    INFO_GENERIC = auto()  # generic information, e.g. picking up an item
    INFO_GAME = auto()  # game-related information such as hints
    INFO_GOOD = auto()  # information about beneficial events
    INFO_BAD = auto()  # information about harmful events
    FLUFF = auto()  # non-important events, such as monster barks
    ALERT = auto()  # alerts about import events, such as health being very low

class Message:
    def __init__(self, text, msg_type=MessageType.INFO_GENERIC, color=None):
        self.text = text
        self.msg_type = msg_type
        self.color = color if color is not None else self.set_color()
        
    def set_color(self):
        if self.msg_type == MessageType.INFO_GENERIC:
            return cfg.MSG_COLOR_INFO_GENERIC
        elif self.msg_type == MessageType.INFO_GAME:
            return cfg.MSG_COLOR_INFO_GAME
        elif self.msg_type == MessageType.INFO_GOOD:
            return cfg.MSG_COLOR_INFO_GOOD
        elif self.msg_type == MessageType.INFO_BAD:
            return cfg.MSG_COLOR_INFO_BAD
        elif self.msg_type == MessageType.FLUFF:
            return cfg.MSG_COLOR_FLUFF
        elif self.msg_type == MessageType.ALERT:
            return cfg.MSG_COLOR_ALERT
        else:
            return cfg.MSG_COLOR_INFO_GENERIC


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.msg_type, message.color))