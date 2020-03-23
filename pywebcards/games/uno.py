# https://en.wikipedia.org/wiki/Uno_(card_game)#Official_rules
import math
import random

from .. import base_classes

from ..base_classes import TurnOrder


class Suits(base_classes.BaseSuits):
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Yellow = (255, 255, 0)
    Blue = (0, 0, 255)
    Black = (0, 0, 0)


class Faces(base_classes.BaseFaces):
    Zero = 0
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    DrawTwo = '+2'
    WildDrawFour = '+4'
    Skip = 'skip'
    Reverse = 'reverse'
    Wild = 'wild'


class Card(base_classes.BaseCard):
    def __str__(self):
        return f"{self.suit.name} {self.face.value}".capitalize()

    def can_play(self, game):
        """Returns true if this card can be played now"""
        # By default all cards can be played on their own colour or value
        return len(game.discard_stack) == 0 or game.discard_stack[-1].suit == self.suit or game.discard_stack[-1].face == self.face

    def play(self, game, player):
        super().play(game=game, player=player)
        if player is not None:
            player.hand.remove(self)

        game.discard_stack.append(self)


class CardNumber(Card):
    def __init__(self, suit, value: int):
        super().__init__(suit=suit, face=Faces(value))


class CardSkip(Card):
    def play(self, game, player):
        super().play(game=game, player=player)
        game.next_turn()


class CardReverse(Card):
    def play(self, game, player):
        super().play(game=game, player=player)
        if game.turn_order == TurnOrder.Clockwise:
            game.turn_order = TurnOrder.CounterClockwise
        elif game.turn_order == TurnOrder.CounterClockwise:
            game.turn_order = TurnOrder.Clockwise


class CardWild(Card):
    def __str__(self):
        return self.face.value

    def can_play(self, game):
        """Returns true if this card can be played now"""
        return len(game.discard_stack) == 0 or game.discard_stack[-1].face not in (Faces.DrawTwo, Faces.WildDrawFour)

    def play(self, game, player):
        super().play(game=game, player=player)
        raise NotImplementedError("FIXME")


class CardDraw2(Card):
    draw_cards = 2

    def play(self, game, player):
        super().play(game=game, player=player)
        # Skip the turn first, so we can use current_player for the drawing
        if player is not None:
            game.next_turn()
        game.current_player.hand.extend(game.draw_stack.draw(self.draw_cards))


class CardDraw4(CardWild, CardDraw2):
    draw_cards = 4


class GameDeck(base_classes.BaseGameDeck):
    def __init__(self):
        super().__init__()
        for colour in Suits:
            # Black is only wilds
            if colour != Suits.Black:
                # Add one of everything except wilds because wilds are only black
                self.extend((
                    Card(face=face, suit=colour)
                    for face in Faces
                    if face not in (Faces.Wild, Faces.WildDrawFour)
                ))
                # And again because there's only 1 of each zero but 2 of everything else
                self.extend((
                    Card(face=face, suit=colour)
                    for face in Faces
                    if face not in (Faces.Wild, Faces.WildDrawFour, Faces.Zero)
                ))

        # There's 4 of each black/wild
        for face in (Faces.Wild, Faces.WildDrawFour):
            self.extend((
                Card(face=face, suit=Suits.Black) for i in range(0, 4)
            ))

        assert len(self) == 108, "Uno deck must have exactly 108 cards"


class Stack(base_classes.BaseStack):
    pass


class Hand(base_classes.BaseHand):
    pass


class Player(base_classes.BasePlayer):
    pass


class Game(base_classes.BaseGame):
    min_players = 2
    max_players = math.inf

    def __init__(self, starting_hand_size=7):
        super().__init__()

        self.starting_hand_size = starting_hand_size

        self.deck = GameDeck()
        self.draw_stack = Stack()
        self.draw_stack.extend(self.deck)

        self.discard_stack = Stack()

    def create_new_hand(self, player: Player):
        """Returns a new hand for the given player"""
        return Hand(player)

    def start_game(self):
        super().start_game()

        # Let's do it 7 times just to be certain
        self.draw_stack.shuffle()
        self.draw_stack.shuffle()
        self.draw_stack.shuffle()
        self.draw_stack.shuffle()
        self.draw_stack.shuffle()
        self.draw_stack.shuffle()
        self.draw_stack.shuffle()

        for _ in range(0, self.starting_hand_size):
            for player in self.players:
                player.hand.extend(self.draw_stack.draw())

        self.current_player = random.choice(self.players)

        first_card, = self.draw_stack.draw()
        first_card.play(game=self, player=None)

    def _other_actions(self, player, action):
        new_card, = self.draw_stack.draw()
        if new_card.can_play(game=self):
            raise NotImplementedError()
        else:
            player.hand.append(new_card)

    def _play_card(self, card):
        self.discard_stack.append(card)
