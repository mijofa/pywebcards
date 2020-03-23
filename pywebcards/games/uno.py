# https://en.wikipedia.org/wiki/Uno_(card_game)#Official_rules

from .. import base_classes


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
    Wild = 'wild'
    WildDrawFour = '+4'
    Skip = 'skip'
    DrawTwo = '+2'
    Reverse = 'reverse'


class Card(base_classes.BaseCard):
    pass


class GameDeck(base_classes.BaseGameDeck):
    def __init__(self):
        super().__init__()
        for colour in Suits:
            # Black is only wilds
            if colour != Suits.Black:
                # Add one of everything except wilds because wilds are only black
                self.extend((
                    Card(face=face, suit=colour, can_be_played_on=[face, colour])
                    for face in Faces
                    if face not in (Faces.Wild, Faces.WildDrawFour)
                ))
                # And again because there's only 1 of each zero but 2 of everything else
                self.extend((
                    Card(face=face, suit=colour, can_be_played_on=[face, colour])
                    for face in Faces
                    if face not in (Faces.Wild, Faces.WildDrawFour, Faces.Zero)
                ))

        # There's 4 of each black/wild
        self.extend((
            Card(face=Faces.Wild, suit=Suits.Black, can_be_played_on=list(Faces) + list(Suits)) for i in range(0, 4)
        ))
        self.extend((
            Card(face=Faces.WildDrawFour, suit=Suits.Black, can_be_played_on=list(Faces) + list(Suits)) for i in range(0, 4)
        ))

        # An Uno deck has 108 cards in it
        assert len(self) == 108


class Stack(base_classes.BaseStack):
    pass


class Hand(base_classes.BaseHand, Stack):
    pass


class Player(base_classes.BasePlayer):
    pass


class Game(base_classes.BaseGame):
    pass
