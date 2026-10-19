# A Dream of Knots

*How a childhood dream became the starting point for a research project.*

*Disclosure: Sol6.1 (AI) assisted with the structure, wording, and
translation of this article. The dream account and personal motivation
are my own.*

*Draft for Medium · 19 October 2026 · [Deutsche Fassung auf Medium](https://medium.com/@haukeh/ein-traum-von-knoten-9232412d4ff8)*

As a small child, I had a dream. I was flying freely, turned a little, and
got caught in my own flight path. So caught up in it that I eventually
found myself trapped in complex knots.

That moment felt almost like a nightmare. I often found a way out. Once I
was finally free, it would eventually get boring. I would turn a little,
and the whole thing would start again.

That dream was the starting point for what I work on today: a trajectory
with memory. Motion whose past feeds back into what happens next. Later,
this led to questions about interactions and whether persistent
structures could emerge in this way.

This is very personal. It explains my motivation, even though it does not
yet tell us whether the idea holds up scientifically.

## How It Became a Model

We arrived at the current model gradually, through philosophical
questions. One was what we actually mean by the state of a system. Is its
current position enough? Or does its past belong in the description too?

Questions like these brought us to the term “Markovian.” In the model,
the visible position alone generally is not enough to determine the
probability of the next step. The stored past plays a part. Including the
full memory state gives us a Markov description.

That sounds abstract at first. The idea behind it is simpler: a point
moves, leaves a fading trace, and then responds to that trace. In the
computer, we retain a finite number of past positions.

The project is now called **Memory Dynamics**. Its website is
[MemoryDynamics.org](https://memorydynamics.org/). The larger hope has been,
and still is, to learn something about how physical structures arise. It is
easy to start thinking about a “theory of everything.” So far, we have a
mathematical model and a set of results whose scope we need to examine.

## Where We Are

Some initially striking structures in the model can already be explained
by linear relaxation. In a separate branch of the model, there are
computer-assisted local existence certificates for certain prepared
circular orbits. There are also numerical tests in which small
perturbations decay under specified conditions.

These are limited results. They do not yet establish real particles or
physical mass, charge, or spin. A circular orbit is not a topological
knot either. How far the findings extend beyond the initial states and
parameters examined remains to be tested.

The equations, code, and analyses are in the
[GitHub repository](https://github.com/MemoryDynamics/Knoten).

Perhaps I was “only” experiencing my own neurons forming connections in
the dream. That is a personal interpretation I cannot substantiate from
the memory. Still, I find the thought interesting. Perhaps the question
of dynamics with memory could also lead to something useful in AI
development.

That would need its own tasks and comparisons. So far, we have neither
an explanation of the brain nor evidence that the model learns or offers
an advantage for AI. But this question could be pursued even if the
larger hope about physics does not work out.

## Why I Am Writing About It

The project has grown too large for me. And finding people who have time
for a review is becoming more difficult.

So I wonder whether we should open the discussion earlier and more
informally. Perhaps others are driven by similarly personal questions
and recognize something here. Or perhaps someone will look at an equation
and immediately see where it goes wrong. Either would be a good way to
start a conversation.

Specialist journals remain an option for individual results. But I do not
want to wait for the whole project to fit into a finished story before
discussing it.

Nobody needs to work through the entire repository to contribute.
Checking a derivation, following a calculation, or suggesting a simpler
explanation would already help. We have put together
[three manageable starting points](https://github.com/MemoryDynamics/Knoten/blob/main/docs/outreach/contribute_review_en.md).
Feedback can be recorded as a
[GitHub issue](https://github.com/MemoryDynamics/Knoten/issues/new?template=focused_review_en.md).

I would like to find out together how far the idea that grew from the
dream can go.

---

Further reading: [Scientific status](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/docs/status/current_status.md),
[local stability finding](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_g5_component_attempt_3_result_review_2026-09-17.md),
and [internal review](https://github.com/MemoryDynamics/Knoten/blob/35ae7b0eb7d7bb8cc57eaa2c2af80b32d955fb4f/reports/project/meta/reviews/scalar_memory_rotating_wave_horizon_g5_premerge_referee_review_2026-09-17.md).
The internal checks are not an independent external replication. These
technical sources are currently in German.
