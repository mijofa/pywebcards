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


class TurnOrder(enum.IntEnum):
    """Turn Order, it shouldn't really need subclassing"""
    # Player 0, 1, 2, 3
    Clockwise = 1
    Forward = 1
    Ascending = 1
    # Player 3, 2, 1, 0
    CounterClockwise = -1
    Backward = -1
    Descending = -1


@dataclasses.dataclass
class BaseCard:
    """Cards used to make up the deck"""
    face: str
    suit: str

    @abc.abstractmethod
    def __str__(self):
        # Some decks would call it "{face} of {suit}" others might call it "{suit} {face}" so just leave that for the subclass
        super().__str__()

    @abc.abstractmethod
    def can_play(self, game):
        """Returns true if this card can be played now"""
        pass

    @abc.abstractmethod
    def play(self, game, player):
        if not self.can_play(game=game):
            raise NotImplementedError()


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

    def __str__(self):
        return f"Stack of {len(self)} cards"


class BaseHand(BaseStack):
    def __init__(self, player):
        # FIXME: Should player hands always start empty?
        super().__init__()

        self.player = player

    def __str__(self):
        return f"{self.player.nickname}'s hand containing {len(self)} cards"


class BasePlayer(object):
    """Base player/user object, shouldn't actually need much changes for different game rules"""
    def __init__(self, nickname):
        self.nickname = nickname
        self.uid = uuid.uuid4()

        self.hand = None

    def __repr__(self):
        return f"<{self.__class__.__module__}.{self.__class__.__name__} object for '{self.nickname}'>"


class BaseGame(object):
    """Base game object, this is where all the game rules logic goes"""
    ## Static game rule variables
    # Minimum number of players required for a match
    min_players = None
    # Maximum number of players allowed per match
    # NOTE: use math.inf if there is no limit
    max_players = None

    def __init__(self):

        ## Active game variables
        # player objects for each player currently in match
        self.players = []
        # Who's turn is it
        self.current_player = None
        # Current turn order
        self.turn_order = TurnOrder.Clockwise
        # Pile of cards that haven't been played
        self.unplayed_stack = None
        # Pile of cards that have been played
        # NOTE: Must remain ordered
        self.played_stack = None

    @abc.abstractmethod
    def _create_new_hand(self, player: BasePlayer):
        """Returns a new hand for the given player"""
        return BaseHand(player)

    @abc.abstractmethod
    def _deal_hands(self):
        """Deal player's hands out"""
        pass

    @abc.abstractmethod
    def _other_actions(self, player, action):
        """Perform an action that isn't a card from the deck"""
        pass

    def add_player(self, player: BasePlayer):
        # Don't add more than the max players
        if (len(self.players) + 1) <= self.max_players:
            self.players.append(player)
            player.hand = self._create_new_hand(player)
        else:
            raise NotImplementedError('FIXME')

    def drop_player(self, player: BasePlayer):
        raise NotImplementedError('FIXME')

    @abc.abstractmethod
    def start_game(self):
        if not self.min_players <= len(self.players) <= self.max_players:
            raise NotImplementedError("FIXME")

    def next_turn(self):
        # Add the turn_order value to the current player number
        print("Going to next player")
        # Make the index wraparound
        next_player_num = (self.players.index(self.current_player) + self.turn_order.value) % len(self.players)
        self.current_player = self.players[next_player_num]

    def play_turn(self, player, card):
        assert player == self.current_player
        assert card in player.hand
        assert card.can_play(game=self)

        if isinstance(card, BaseCard):
            card.play(game=self, player=player)
        else:
            self._other_actions(player=player, action=card)

        self.next_turn()
