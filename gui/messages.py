from enum import Enum, auto

from config_files import cfg as cfg, colors

import textwrap

class MessageCategory(Enum):
    EVENT = auto()
    OBSERVATION = auto()

class MessageType(Enum):
    """ sets the type of the message """
    GENERIC = auto()  # generic information, e.g. picking up an item
    GAME = auto()  # game-related information such as hints
    GOOD = auto()  # information about beneficial events
    BAD = auto()  # information about harmful events
    ALERT = auto()  # alerts about import events, such as health being very low
    COMBAT = auto()
    FLUFF = auto()  # non-important events, such as monster barks
    SYSTEM = auto()

class Message:
    def __init__(self, text, category = MessageCategory.EVENT, type=MessageType.GENERIC, color=None):
        self.text = text
        self.category = category
        self.type = type
        self.color = color if color is not None else self.set_color()
        
    def set_color(self):
        if self.type == MessageType.GENERIC:
            return colors.light_amber
        elif self.type == MessageType.GAME:
            return colors.turquoise
        elif self.type == MessageType.GOOD:
            return colors.green
        elif self.type == MessageType.BAD:
            return colors.dark_flame
        elif self.type == MessageType.FLUFF:
            return colors.desaturated_red
        elif self.type == MessageType.ALERT:
            return colors.red
        elif self.type == MessageType.COMBAT:
            return colors.dark_azure
        
    def add_to_log(self, game):
        #self.text = f'T{game.turn}: ' + self.text

        if self.category == MessageCategory.EVENT:
            game.event_log.add_message(self)
        else:
            game.observation_log.add_message(self)
            
            
class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):

        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in reversed(new_msg_lines):
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, type = message.type, color = message.color))