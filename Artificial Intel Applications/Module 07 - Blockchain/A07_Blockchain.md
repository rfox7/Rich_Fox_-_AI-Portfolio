A07 Blockchain

Rich Fox\
ITAI 2372\
June 27, 2026

# Industry Overview

At its core, blockchain is a ledger that lives on thousands of computers
at once instead of sitting on one company\'s server. Transactions get
bundled into \"blocks,\" and each block locks onto the one before it
using cryptography. Try to change something after the fact and you\'d
have to rewrite everything that came after it too, which, in practice,
nobody can pull off. That\'s why people trust the data without needing a
bank or some other middleman to sign off on it.

This is what makes decentralized exchange possible, moving money,
assets, anything of value, without a central referee. Ethereum took it a
step further with smart contracts, little pieces of code that execute
automatically once certain conditions are met. No more chasing down
signatures or reconciling spreadsheets by hand, and a lot less room for
someone to quietly tip the scales.

You see this play out across industries because the same problem keeps
popping up: how do you trust shared information when there\'s no single
party in charge of it? Banks use blockchain to settle transactions
faster and flag fraud sooner. Walmart runs it for food traceability, so
if there\'s a contamination issue, they can trace it back to the source
in minutes instead of days. Governments are testing it for voting
systems that are harder to tamper with, and hospitals are looking at it
as a way to let patients control their own records instead of leaving
that power with whoever\'s storing the file.

The bigger reason any of this matters right now is trust. As more of the
economy moves online, there\'s a real need for systems where you don\'t
have to take someone\'s word for it, the structure itself proves things
are legitimate. That\'s a meaningful cost saver for companies too: fewer
intermediaries, less manual cleanup. And blockchain is quietly becoming
the backbone for other technologies as well, keeping IoT data honest and
giving AI systems a way to show their work in a way people can actually
verify.

# Current AI Trends

AI and blockchain aren\'t just sitting next to each other anymore,
they\'re starting to merge in ways that pair airtight, transparent data
with the kind of intelligent analysis that data alone can\'t provide. A
few examples show where this is already playing out.

## Patent Management: IPwe

IPwe built something called the Global Patent Registry, which tackles a
problem most people outside the patent world don\'t realize is so messy:
tracking who owns what, and what it\'s actually worth. The blockchain
piece keeps an immutable record of every patent, so there\'s no
ambiguity about ownership or history. AI layers on top of that,
crunching the data to flag market trends, estimate value, and surface
risk. Patent management used to be slow and frustratingly opaque, this
setup speeds it up and makes it a lot harder to fake ownership or slip
fraud through the cracks.

## Supply Chain: Walmart

Walmart\'s approach splits the labor between the two technologies.
Blockchain handles traceability, where food came from, what route it
took to the shelf, which means a contamination issue that used to take
days to trace back can now be pinned down in seconds. AI handles the
demand side, watching sales patterns to keep shelves stocked without
overordering. Together, they\'re chipping away at two stubborn problems:
food waste and the guesswork that comes with predicting what people will
actually buy.

## Financial Fraud Detection

This one\'s more about infrastructure than any single company.
Blockchain gives financial institutions a single, trustworthy version of
the data, no disputes about what happened or when. AI then builds its
fraud models on top of that reliable foundation, and because blockchain
keeps an audit trail, you can actually trace why the AI flagged
something instead of just trusting a black box. It\'s a two-way fix: AI
gets cleaner data to learn from, since the records can\'t be quietly
altered, and humans get a paper trail to check the AI\'s reasoning
against.

Beyond these, a couple of trends are worth watching. Decentralized AI
marketplaces are emerging, where people can buy and sell AI models and
datasets without a centralized platform taking a cut or controlling
access. And federated learning on blockchain is gaining traction too, it
lets multiple parties train a shared AI model together without ever
actually handing over their raw data, which solves a privacy problem
that\'s been a major sticking point for collaborative AI work.

# Ethical Implications

Mixing AI and blockchain doesn\'t just create new capabilities, it
creates new headaches, most of them rooted in one core tension:
blockchain wants to be radically transparent, but plenty of the data
running through it needs to stay private.

## **Privacy vs. Transparency**

Here\'s the awkward part: blockchain\'s whole selling point is that
it\'s an open, permanent record everyone can verify. That\'s great for
trust, less great when the data in question is someone\'s personal
information. The industry\'s response has been things like cryptographic
techniques to mask sensitive data, plus federated learning, which lets
AI models train on local devices without the raw data ever leaving its
source. There\'s actually an interesting counterargument floating around
too, that blockchain\'s security might make people more willing to share
personal data, not less, since they\'d trust it\'s actually protected.

## **Bias and Data Integrity**

AI running on blockchain gets pitched as a fix for algorithmic bias, and
there\'s something to that, if the underlying data can\'t be tampered
with, you at least know the AI isn\'t learning from corrupted or
manipulated inputs. You can also audit the trail and see how a model
landed on a given answer. But here\'s the catch: blockchain can
guarantee data hasn\'t been *altered*, it can\'t guarantee the data was
*fair* to begin with. If the original records carry historical bias,
locking them onto an immutable ledger doesn\'t un-bias them, it just
makes the bias permanent and harder to quietly fix later.

**Transparency / Explainability**

One of AI\'s biggest credibility issues is that it\'s hard to know why a
model made a particular call. Blockchain helps here by creating a
permanent audit trail of the decision-making process, which means
there\'s an actual record to check instead of just trusting the output.
That kind of accountability matters a lot if automated systems are going
to be trusted with anything consequential. In this case, we are actually
resolving an ethical concern.

## **Jobs and the Skills Gap**

Other industries, smart cities, for instance, are mostly worried about
AI replacing jobs outright. Blockchain\'s problem looks a bit different:
it\'s less about disappearing jobs and more about a skills gap.
Something like 49% of supply chain managers say a lack of blockchain
expertise is one of their biggest operational headaches. The ethical
wrinkle is access, as roles shift from doing manual work to overseeing
complex automated systems, the people without access to the right
training risk getting left behind, widening the gap between who benefits
from this tech and who gets squeezed out by it.

# Future Trends

Looking out five to ten years, AI and blockchain are expected to stop
being experimental side projects and start acting like actual economic
infrastructure. The numbers being thrown around are big --- blockchain
alone is projected to generate over \$3.1 trillion in business value by
2030, with some forecasts tying that to a 14% bump in global GDP. The
shorthand for where this is headed is a \"blockchain economy\" --- one
where humans and machines handle business processes and trade value
directly, without the usual layer of intermediaries in between.

## What\'s Coming

A handful of technologies are expected to mature in this window.
Decentralized AI marketplaces will let people buy and sell AI models and
datasets directly, with data providers keeping ownership instead of
handing it over the moment someone wants to use it. Federated learning
on blockchain solves a problem that\'s dogged AI for years --- training
models on data from multiple sources without ever moving the raw data
itself, since only the learned patterns get shared, not the underlying
private information. There\'s also work on using AI to fix blockchain\'s
own bottleneck: the consensus and verification processes that currently
make networks slow are expected to get a lot more efficient once AI is
steering them. And some people are betting on public blockchain
infrastructure becoming as invisible and ubiquitous as the internet
itself --- baked into search engines and everyday tools without anyone
really noticing it\'s there.

## Opportunities Worth Watching

A few shifts could open real strategic advantages. Because blockchain
offers a tamper-proof version of the truth, people may end up more
willing to share personal data than they are now, simply because they
trust it\'s actually protected --- which would hand AI systems a much
richer pool of high-quality data to learn from. Blockchain\'s audit
trails also chip away at AI\'s black-box reputation, since you can trace
exactly how a decision got made instead of just trusting the output. And
pushing AI computation out to the edge --- onto local devices, secured
by blockchain --- should cut latency for things that can\'t afford
delay, like self-driving cars or high-frequency trading.

## What Could Go Wrong

The most immediate problem is a skills shortage --- about 49% of supply
chain managers already say a lack of blockchain expertise is one of
their biggest obstacles, and that gap isn\'t closing on its own. Closing
it will take real investment in retraining workers to move from manual
tasks to overseeing automated systems. There\'s also a governance
vacuum: little global consensus yet on how to handle data rights, who\'s
liable when an algorithm gets something wrong, or how decentralized
autonomous organizations should even be classified legally. And while
this shift will create high-skill jobs for engineers and data
scientists, it\'s also going to automate a lot of repetitive work in
finance, logistics, and manufacturing --- meaning the gains and the
losses won\'t be evenly distributed.

The throughline for the next decade is something people are calling
Industry 5.0 --- less about replacing humans outright, more about
figuring out how humans and machines actually work well together,
without sacrificing efficiency on one side or well-being on the other.

# Your Reflections

What stands out most to me from this research isn\'t really tied to any
one flashy use case, it\'s more that I don\'t think of this as an
\"industry\" at all. It feels more like a better *way of doing things*,
a method that happens to be getting bolted onto industries that already
exist, rather than some new sector standing on its own.

What actually surprises me is how *underused* it still is in situations
where verification should be non-negotiable. Take military
communications, if orders are being sent electronically, why wouldn\'t
you want a way to confirm, with certainty, that nothing got intercepted,
altered, or spoofed along the way? That\'s exactly the kind of problem
blockchain is built to solve: an immutable, verifiable record that
proves a piece of data arrived exactly as it left, with no quiet edits
in between. It seems like an obvious fit for any high-stakes
transmission where the cost of tampering, or even just the *suspicion*
of tampering, could be catastrophic.

That\'s really the throughline for me. The appeal isn\'t \"I want to
work in blockchain\" so much as \"this is a tool that should already be
standard in places where trust and integrity matter most\", defense
communications, financial transactions, supply chains, anywhere a
corrupted or altered record could cause real damage. The fact that it\'s
still mostly confined to finance and a handful of retail pilots, rather
than being baked into critical infrastructure and government systems, is
the surprising part.

The concerns are still real, though, legal frameworks are thin, the
skills gap is wide, and there\'s a genuine risk that the people who\'d
benefit most from this tech are the ones least likely to have access to
the training needed to implement or maintain it. But I\'d frame my
interest less as \"joining an industry\" and more as wanting to push
this approach into the places where it\'s conspicuously absent,
particularly anywhere data integrity is a matter of life and death
rather than just operational efficiency.
