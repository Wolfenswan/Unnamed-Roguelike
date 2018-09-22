from enum import Enum, auto

from config_files import cfg as cfg, colors

import textwrap

class MessageCategory(Enum):
    COMBAT = auto()
    OBSERVATION = auto()

class MessageType(Enum):
    """ sets the type of the message """
    GENERIC = auto()  # generic information, e.g. picking up an item
    GAME = auto()  # game-related information such as hints
    GOOD = auto()  # information about beneficial events
    BAD = auto()  # information about harmful events
    ALERT = auto()  # alerts about import events, such as health being very low
    COMBAT = auto()
    COMBAT_INFO = auto()
    COMBAT_GOOD = auto()
    COMBAT_BAD = auto()
    FLUFF = auto()  # non-important events, such as monster barks
    SYSTEM = auto()

class Message:
    def __init__(self, text, category = MessageCategory.OBSERVATION, type=MessageType.GENERIC, color=None):
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
        elif self.type == MessageType.COMBAT_INFO:
            return colors.dark_azure
        elif self.type == MessageType.COMBAT_GOOD:
            return colors.dark_cyan
        elif self.type == MessageType.COMBAT_BAD:
            return colors.dark_orange
        else:
            return colors.pink

    def add_to_log(self, game):
        #self.text = f'T{game.turn}: ' + self.text

        if self.category == MessageCategory.COMBAT:
            game.combat_log.add_message(self, game.turn)
        else:
            game.observation_log.add_message(self, game.turn)
            
            
class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message, turn):

        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in reversed(new_msg_lines):
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.height:
                del self.messages[0]

            # Add the new line as a Message object, with the text and the color
            new_message = Message(line, type = message.type, color = message.color)
            new_message.turn = turn
            self.messages.append(new_message)