# Module 4: Backpropagation, "How Robo Learns From Mistakes"

**Course:** ITAI 2376, Deep Learning | **Assignment:** A04

---

## What this module covers

How a neural network learns from its mistakes. The assignment was to explain backpropagation to a general audience, so I made a kid-friendly slide deck that follows a robot named Robo learning to tell cats from dogs.

## Files

| File | What it is |
|---|---|
| `A04_RichFox_ITAI2376.pptx` | 15-slide presentation with speaker notes |

## The five steps (as Robo tells it)

| Step | Kid version | Real term |
|---|---|---|
| 1 | Robo looks at a picture and makes a guess | Forward pass |
| 2 | Robo gives itself an "Oops Score" for how wrong it was | Loss function |
| 3 | Robo passes the blame backward, from the answer back toward the eyes | Backpropagation |
| 4 | Robo turns each knob a tiny bit, more for the helpers that were more to blame | Gradient descent with a learning rate |
| 5 | Repeat, many times | Training |

**The chant:** "Guess it, check it, pass it back, nudge the knobs and stay on track!"

## Key ideas

- A neural network is a team of helpers in rows. Every connection has a knob (a **weight**). Learning means setting the knobs.
- Training pictures come with the right answer on the back, like flash cards (**labels**). Without them Robo could not tell it made a mistake.
- Blame is fair: a helper that shouted the wrong answer through a strong knob gets a big fix, a quiet one gets a tiny fix, and a helper that pushed toward the right answer gets turned up.
- Turns are tiny on purpose. Cranking a shower handle all the way swings from freezing to scalding. Small turns get you to "just right."
- **Cookie robot example:** 4 friends need 2 cookies each (8 total) and Robo has one knob (cookies = knob x 4). Starting at 1, the knob goes 1 -> 1.5 -> 1.75 -> 1.875, and the miss shrinks 4 -> 2 -> 1 -> 0.5 cookies. Bigger mistake, bigger fix.
- Backpropagation was made famous in 1986 by Rumelhart, Hinton, and Williams.

## For the grown-ups

Backpropagation is only the gradient calculation: it applies the chain rule backward from the loss to get the effect of every weight and bias on the error, reusing each layer's result for the layer before it, so it costs about one extra forward pass. **Gradient descent** is the separate step that uses those gradients to update the weights.

## Takeaways

- Backpropagation works out who is to blame for the error. Gradient descent is the separate step that fixes it.
- Everyday apps like photo search, voice assistants, and translators are trained with this loop.

---

*[Back to Deep Learning](../README.md)*
