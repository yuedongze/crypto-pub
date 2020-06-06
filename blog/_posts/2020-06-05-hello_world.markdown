---
layout: post
title:  "Hello World"
---
After writing tech blogs on [Medium] for a little less than 2 years. I realized that it's very hard to write technical deep dives on the platform. The topics on the main page are all catchphrases that are like click-baits. The metered paywalls are another functionality that got me - I couldn't really share my ideas with the entire public and people need to pay to see it.


Despite Medium's great writing experience, I decided that I shall not write more posts on theoretical and technical posts (especially about Cryptography).


Therefore, I'm trying out Jekyll (and hosting it myself). Hopefully, it could be a nicer place for me to write down more organized thoughts.


A little background on crypto though - I'm deeply attracted by this field ever since I took CS251 with Prof. Dan Boneh last fall. It's a deep, dense, and theoretical field, yet it also has a branch that focuses on realistic real-world implementations. The two branches intertwine and are both important at all times. There are countless mesmerizing technologies that I can never stop talking about:
- Zero-Knowledge Proofs (zkSNARK, STARK, etc.)
- Multi-Party Computation (Oblivious Transfer, Yao's Garbled Circuits, Shamir Secret Sharing, etc.)
- Privacy-Preserving Technologies (Private Information Retrieval)
- Fully Homomorphic Encryption (Lattice-based Crypto)
- ...


This list goes on and on. I'll try to formate these ideas into words and write them down here in the future.


Plus, I get to do all kinds of cool features here:

{% mermaid %}
stateDiagram-v2
    [*] --> Sleeping
    Sleeping --> [*]

    Sleeping --> Awake
    Awake --> Sleeping
    Awake --> Eating
    Eating --> [*]
{% endmermaid %}

[Medium]: https://medium.com/@stevenyue
