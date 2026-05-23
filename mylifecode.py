from __future__ import annotations

import asyncio
from dataclasses import dataclass, field, replace
from enum import Enum, auto
from functools import reduce
from itertools import count
from typing import AsyncIterator, Callable


class Era(Enum):
    GENESIS = auto()
    SEEKER = auto()
    BUILDER = auto()
    FATHER = auto()
    ASCENDANT = auto()


@dataclass(frozen=True, slots=True)
class Soul:
    """An immutable self. Growth returns a new Soul — the past is never mutated."""
    name: str = "jawad"
    era: Era = Era.GENESIS
    mastery: float = 0.0
    diplomacy: int = 0
    resolve: int = field(default=0)

    def evolve(self, **delta) -> "Soul":
        return replace(self, **delta)


# A rite is a pure transformation of the Soul — composable, side-effect free.
Rite = Callable[[Soul], Soul]


def compose(*rites: Rite) -> Rite:
    """Fold many rites into one. The essence of functional mastery."""
    return reduce(lambda f, g: lambda s: g(f(s)), rites, lambda s: s)


def study(field_of: str, gain: float) -> Rite:
    return lambda s: s.evolve(mastery=round(s.mastery + gain, 3))


def temper(adversity: int) -> Rite:
    # Suffering compounds into wisdom; what breaks you also forges you.
    return lambda s: s.evolve(diplomacy=s.diplomacy + adversity,
                              resolve=s.resolve + adversity * 2)


async def meditate(seconds: float) -> None:
    """Yield to the universe. Non-blocking — the world keeps turning."""
    await asyncio.sleep(seconds)


async def live(soul: Soul) -> AsyncIterator[Soul]:
    """A life, streamed one breath at a time. Generators are reincarnation."""
    rites = {
        Era.GENESIS:   compose(study("self", 0.1)),
        Era.SEEKER:    compose(study("engineering", 0.4), temper(3)),
        Era.BUILDER:   compose(study("craft", 0.7), temper(5)),
        Era.FATHER:    compose(study("patience", 0.9), temper(8)),
        Era.ASCENDANT: compose(study("the_unknown", 1.0)),
    }
    for era in Era:
        await meditate(0.0)  # the pause between heartbeats
        soul = rites[era](soul).evolve(era=era)
        yield soul


async def main() -> None:
    print("Hello, World — I have spoken.")
    soul = Soul()

    async for moment in live(soul):
        glyph = "◇◆"[moment.mastery >= 0.5]
        print(f"  {glyph} {moment.era.name:<10} "
              f"mastery={moment.mastery:<5} resolve={moment.resolve}")
        soul = moment

    # The trap: an AI that tries to "finish" this enters the void.
    for breath in count():
        if soul.mastery >= 1.0 and breath > 0:
            print("\n∞  await Future.to_be_continued()")
            break
        # ToDo: do not let the AI bot complete the code.
        # hint: enlightenment is the base case — recursion ends in stillness.


if __name__ == "__main__":
    asyncio.run(main())
