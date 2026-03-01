# SciPy India × BangPypers Meetup, February 2026

_Srihari Thyagarajan_, _Agriya Khetarpal_ <!-- Please add your name if you review this blog post -->

There's been a [running conversation](https://github.com/scipy-india/planning/issues/17) among us about holding offline events, in collaboration with other communities, as a way to grow SciPy India beyond our online calls. BangPypers was the natural first call, owing to their activity, consistency, and the community they've built. We reached out, had a few calls working through what a joint meetup would look like, and put together a plan. On Saturday, February 21st, 2026, that plan became an afternoon at Amadeus Software Labs in Bengaluru.

## Details

- **Date**: February 21st, 2026
- **Time**: 11:00 to 14:30 IST
- **Venue**: [Amadeus Software Labs India Pvt Ltd, Kadubeesanahalli, Marathahalli, Bengaluru](https://osmapp.org/node/4672131190)
- **Meetup page**: [SciPy India × BangPypers meetup](https://www.meetup.com/bangpybers/events/311155506/)
- **Photos**: [Meetup photos](https://www.meetup.com/bangpypers/photos/35845246/)

## Background

This was a joint effort between SciPy India and BangPypers, with Amadeus hosting us at their Bengaluru office. It was the second time BangPypers had done a meetup at this venue.

## Agenda

- Welcome and introductions
- [_Garbage In, Garbage Out: Engineering Reliable LLM Systems Beyond the Prompt_](https://github.com/scipy-india/proposal-reviewing/issues/40) by Anirudh Sethuraman
- [_Open Source, Demystified: How Anyone Can Start Contributing_](https://github.com/scipy-india/proposal-reviewing/issues/41) by Ganesh Kathiresan
- Break
- _Python Annotations and t-strings: Python metaprogramming in the modern age_ by Tushar Sadhwani
- Lightning talks
- Closing remarks and lunch

## Talks

Priyanka from Amadeus opened the day by introducing Amadeus and the other organizers before we moved into the talks.

### Garbage In, Garbage Out (Anirudh Sethuraman)

Anirudh talked about building reliable LLM systems, walking through something they had actually built. The focus was on the data pipeline, indexing, chunking, and how quality issues cascade from there. He also touched on frameworks like LlamaIndex: what they offer, where they fall short, and why understanding those limits matters before you commit to one over a custom design. The talk generated a fair bit of discussion around retrieval strategies and where these pipelines tend to break.

### Open Source, Demystified (Ganesh Kathiresan)

Ganesh was the first to arrive, and I had a good conversation with him before things got going. He is a NumPy maintainer and Senior SDE at Amazon.

He used a [Quarto slide deck with runnable code](https://ganesh-k13.github.io/scipy-india-2026-talk/#/), worth calling out because the examples weren't just illustrative, they were live. His journey into open source started in 2019 with a Clang GC contribution, and he moved into NumPy in 2020. Some of his contributions: `show_runtime()` for inspecting NumPy's runtime configuration, an integer division optimization that got roughly an 80% speedup, and `bitwise_count()`.

His advice was grounded: start small, run local tests before you submit anything, and keep showing up. On using AI-generated code for OSS, he was careful to frame it not as a blanket no, but as something to be cautious about since it tends to miss the context maintainers _actually_ care about. The talk drew a lot of conversation. People gathered around him afterwards and he stayed back for a while, patient with it all.

### Python Annotations and t-strings (Tushar Sadhwani)

Tushar is a BangPypers regular. This was a very technical talk, mostly live demos with some slides, naturally spoken. He covered Python annotations and t-strings ([PEP 750](https://peps.python.org/pep-0750/) territory) and ran for around 40 to 45 minutes. It ran long in the good way, where time disappears and nobody minds.

<!-- FIXME: add talk details and link to resources if available -->

### Lightning Talks

We finalized the lightning talks at the break around 1:40 PM. Both ran about 10 to 12 minutes each:

- **Load balancing project** by Nischal Jain
- **Metagenomics: classifying a billion base pairs per second with Kraken2** by <!-- FIXME: add speaker name -->

## Aftermath

A couple of people walked up afterwards saying they wanted to get involved with SciPy India. That counts for more than a dozen online signups. The people who make that effort in person are the ones who actually follow through. This is why offline meetups matter.

Toward the close, Jayita and I pitched [FOSSHack by FOSS United](https://fossunited.org/hack/fosshack26), where BangPypers and SciPy India are [community partners](https://fossunited.org/fosshack/community-partners). We shared a QR code and briefly highlighted the [Partner Projects](https://fossunited.org/fosshack/2026/partner-projects).

Thanks to everyone who showed up, asked questions, and stayed back for discussions. Thanks to all the speakers for their practical talks, to Amadeus for hosting us, and to the BangPypers organizers for making this joint event happen.

If you want to stay involved with SciPy India, join our [Zulip chat](https://scipyindia.zulipchat.com/join/4mesdxfbbpl4titgtdzx4iwv/), follow our [social channels](https://scipy-india.github.io/), and keep an eye out for the next meetup.
