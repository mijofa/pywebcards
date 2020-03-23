import abc
import collections
import dataclasses
import random
import uuid
import enum


class BaseSuits(enum.Enum):
    """Suits available in the game deck"""
    pass


class BaseFaces(enum.Enum):
    """Faces available in the game deck"""
    pass


@dataclasses.dataclass
class BaseCard:
    """Cards used to make up the deck"""
    face: str
    suit: str
    can_be_played_on: list = None

    def __str__(self):
        raise NotImplementedError("Must be defined for the specific game cards")


class BaseGameDeck(collections.UserList):
    """Base object for the entire game deck"""
    @abc.abstractmethod
    def __init__(self):
        """Must be overridden to populate the base deck with a bunch of cards, but must call super().__init__() FIRST"""
        super().__init__()


class BaseStack(collections.UserList):
    """Base object used for the pile of used and unused cards"""
    def __init__(self, starting_deck: BaseGameDeck = None):
        """If this is the unplayed stack, specify the game deck as the first argument"""
        super().__init__()
        if starting_deck is not None:
            self += starting_deck

    def shuffle(self):
        """Shufle the stack"""
        random.shuffle(self)

    def draw(self, amount: int = 1):
        """Draw a number of cards off the stack equal to amount (default 1)"""
        for i in range(0, amount):
            yield self.pop()


class BaseHand(BaseStack):
    pass


class BasePlayer(object):
    """Base player/user object, shouldn't actually need much changes for different game rules"""
    def __init__(self, nickname):
        self.nickname = nickname
        self.uid = uuid.uuid4()

        # Cards currently in hand
        self.current_hand = None


class BaseGame(object):
    """Base game object, this is where all the game rules logic goes"""
    def __init__(self):
        ## Static game rule variables
        # Minimum number of players required for a match
        self.min_players = None
        # Maximum number of players allowed per match
        # NOTE: use math.inf if there is no limit
        self.max_players = None

        ## Active game variables
        # player objects for each player currently in match
        self.players = []
        # Number of players currently in match
        # Should equal len(self.players)
        self.num_players = 0
        # Who's turn is it
        self.current_player = None
        # Pile of cards that haven't been played
        self.unplayed_stack = None
        # Pile of cards that have been played
        # NOTE: Must remain ordered
        self.played_stack = None

    def add_player(self, player: BasePlayer):
        # Don't add more than the max players
        if (self.num_players + 1) <= self.max_players:
            self.players.append(player)
            self.num_players += 1

            assert len(self.players) == self.num_players

            return True
        else:
            raise NotImplementedError('FIXME')

    def drop_player(self, player: BasePlayer):
        raise NotImplementedError('FIXME')
