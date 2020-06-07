---
layout: post
title:  "[Mirror] Mesmerizing Chameleon Signatures"
---
*This is a mirror of my post at https://medium.com/@stevenyue/mesmerizing-chameleon-signatures-4cdb3c8ab1c3.*

*For the past year, I having been taking classes at Stanford under Professor Dan Boneh and learning about different topics in the field of Cryptography. It has truly become an amazing journey. There are so many marvelous ideas in this field and a lot of them essentially reshaped the world.*

*Therefore I decided to start writing about what I have learned in a series of posts. This first post is actually a summary of an old paper that I recently read.*

![](https://miro.medium.com/max/1890/0*egETJA4QhkH-yqQN)

## Preface

**Signature schemes** are essential to our daily lives. Before computers have existed, we have been signing off papers and documents with our names for a long time. **A proper signature simply represents identity and authenticity.** Digital Signature is essentially the same idea but in the world of computers. A signature proves the validity of what we say.

Aside from signatures, there’s also this idea of a [Commitment scheme](https://en.wikipedia.org/wiki/Commitment_scheme). A hash function is a commitment scheme, as long as it’s hard to produce collisions. Similar to signatures, a commitment proves that we are “committed” to some value. But on the other hand, it also hides the value of it. A valid commitment scheme should satisfy two properties:

- **Binding**: A commitment can only bind to one value. It’s impossible to produce another value that also aliases to the same commitment.
- **Hiding**: A commitment should hide its committed value. By just looking at the commitment itself, the observer should have no way to regain knowledge of the committed value.

Signatures and commitments are equally important in our digital lives. Today I want to talk about a special kind of signatures that leverages a beautiful commitment scheme — **Chameleon Signatures**.

## Digital Signatures

Chameleon Signatures are a very special (and beautiful) type of digital signatures. Like its name, these signatures ***do act like chameleons***.

Before talking about what it is, let’s think about a typical scenario where we use digital signatures.

### Online Auction

Imagine that Alice participated in an online auction and bid 100 dollars for a painting that she really likes. In order to make sure that she is “committed” to pay 100 dollars when she wins the auction, usually, we would ask Alice to sign a digital signature on her bidding.

In order to perform a signature, Alice would need to first generate a pair of keys pk, sk that correspond to the public and the private key. Given her bidding message `m_bid = "100 USD"` , Alice will need to produce a signature:

```
sig = Sign(sk, m_bid)
```

Then Alice can send this signature along with her public key to the auction platform. In order to verify the signature, the auction platform simply uses the verify function to check its validity:

```
is_valid = Verify(pk, m_bid, sig)
```

The auction platform only accepts this bidding if the verify function passes. Sounds pretty straight-forward, right?

### Problems

However, this is just a toy protocol that demonstrates how digital signature works. In the real world, **things get dirty real quick**.

In the protocol above, Alice uses the pk that she sends out to let the platform identify herself. However, why would the platform trust the pk — which is essentially a sequence of meaningless numbers actually represents Alice. Moreover, **how would the platform make sure that the person behind this identity really can afford the bidding if they win the auction**?

A lot of these problems can be handled by introducing more constructions and nuances into the protocol — such as verifying Alice’s identity/SSN/Credit card info before accepting anything from her. Eventually, if things don’t work, we can always go to court and let the judge/jury figure out who did the wrong thing.

However, today I don’t want to talk too much about these identity protocols. (although they are really interesting!) Instead, I want to talk about the problems with the signature itself.

### Signatures destroy secrecy

So what’s wrong with these signatures? The answer is — **not only the platform can verify these signatures**, but it can also send the signature to anyone else and they can verify the validity of Alice’s bidding.

You might ask — wait, isn’t this an indented feature for digital signatures so that anyone could verify? You are right, but in this case, Alice might not be so happy if the platform can actually do that.

Imagine that Alice was actually bidding for **Sunflowers by Vincent van Gogh**, and she bid 100 dollars because that’s how much **she can really afford**. Let’s say that she lost the auction to some billionaire. All of sudden, the platform could share Alice’s signatures with other people and reveal her bid. This could be really embarrassing because she could only afford 100 dollars! Now everyone knows that Alice tried to bid 100 dollars for Sunflowers and laughs at her. You get the idea.

Basically what’s wrong with the protocol is — **it allows parties other than the platform to learn about information (and its validity) while Alice only wanted to show it to the platform**. Publically verifiable signatures destroy the secrecy of a message’s validity.

If we use traditional signature schemes, once the signature is out, it’s always publically verifiable. This means that Alice can only trust the platform not disclosing the bidding to other people (using legal terms of service agreements).

However, this is no good in the crypto world and we want to do better. We want to have something that can **only be verified by a designated party but nobody else**.

And here comes Chameleon Signatures.

![](https://miro.medium.com/max/1890/0*kAItrKhYGxQeXk1L)

## Chameleon Signatures to the rescue

In 1997, [Krawczyk and Rabin](https://pdfs.semanticscholar.org/1c29/4428c76ba7d1d0bb5e1d1bc931138c092453.pdf) came up with the Chameleon Signature scheme. It allows the signer to **only disclose the validity to the intended recipient**. If the recipient tries to send this signature to some other party, the signature itself immediately loses its validity.

By just looking at the problem they tried to solve, it almost sounds impossible. But they offered another perspective: Instead of thinking about how to make Alice’s signature unverifiable to the public, what if we can somehow make the platform look untrustworthy to other parties?

To be a bit more clear — **if the platform is believed to have to power to forge any arbitrary signatures, then no one will trust anything the platform says**. Imagine the platform sends Alice’s signature of her 100-dollar bidding to Bob. Bob will say: I cannot trust you, because you can just make all of this up.

So to summarize it all together, we want to build a **signature+commitment scheme** that’s unforgeable for Alice — so we all know that she cannot make things up or explain her signature with different messages (basically she can’t break the hiding and binding property). However, we also want to enable the designated verifier to have the **full power to forge any signatures as they like** so it discourages leaking information. If we can achieve such a scheme, then Alice will be very happy and continue bidding for more gadgets on the auction platform.

### The Structure

The overall structure of the Chameleon Signature scheme is like the following:

1. Both parties go through a **Setup** phase and it spits out some parameters for the signer and the recipient.
2. Then the signer uses the public parameters to create **a commitment to her message**. Since she only has the public parameters to this commitment, it will be impossible for her to break the binding property of this commitment (i.e. aliasing this commitment to a different message).
3. The signer then signs the commitment using a **normal signature scheme**. She passes it along with the original message and the verifying key to the recipient.
4. The recipient verifies the validity of the signature by recomputing the commitment using the message plaintext and using the verify function of the normal signature scheme to check if the signature on the commitment is valid.

These four steps are how the protocol works for normal usage.

In the case where the recipient tries to share Alice’s signature with a third party Bob, **Bob is only going to see Alice’s signature on some random-looking commitment string** (because of its hiding property). Let’s say that the recipient shows an opening of the commitment to Bob (for example, “100 USD”). Since the Chameleon Signature scheme gives the recipient the power to break the binding property of the commitment, **Bob won’t trust anything the recipient says**.

The other case we need to consider is when the auction closes, the platform says Alice bid 1 million dollars and ask her to pay. She clearly doesn’t have the money and they go to court.
The judge will then ask the platform to provide Alice’s signature along with the message and commitment. First, the judge performs a sanity check to verify that Alice actually signed the commitment. Then the judge presents the commitment along with the opening (the message provided by the platform) to Alice. Alice can either accept the opening or deny it.

If Alice wants to accept the opening, she doesn’t have to do anything. However, if she wants to deny the opening, she will need to supply another valid opening to this commitment. Since Alice cannot break the binding property of the commitment scheme, she couldn’t have forged the opening she provided maliciously. This must mean that the opening provided by the platform is bogus, and the judge can then give his verdict.

There are more nuances to this protocol, which we will come back to later. Now let’s see how this signature scheme actually works.

### Chameleon Hash Function

The secret sauce behind Chameleon Signatures is creating **a commitment scheme that satisfies the property** that I mentioned before — Alice cannot produce forgeries while the platform can trivially produce arbitrary openings to a given commitment. What the authors came up with was called **the Chameleon Hash Function**.

Basically this Chameleon Hash Function takes in a message, randomly samples a nonce, and outputs a commitment to the message. This commitment is binding and hiding just like other kinds of commitment schemes — Alice cannot come up with two different message-nonce pairs that arrive at the same commitment.

```
Alice() -> (m_0, r_0), (m_1, r_1)
Prob[ChamHash(m_0, r_0) = ChamHash(m_1, r_1)] ~= 0
```

However, there’s also a **trapdoor** (or the secret key) to this function that allows whoever knows the trapdoor to **arbitrary open this commitment into any kind of message-nonce pairs as they like**.

The way Chameleon Hash Functions achieve this mesmerizing property is through using [Claw-free Trapdoor Permutations](https://en.wikipedia.org/wiki/Claw-free_permutation).

![](https://miro.medium.com/max/1890/0*wvtwdHZcBjtzTSmO)

### Claw-free Trapdoor Permutations

Don’t be scare of its name. I’ll explain it shortly.

**Permutation** in Cryptography is a bit different from what we learned in Combinatorics. Here a permutation means a function that maps an input x to output y and both x and y are of the same size. Namely:

```
sizeof(x) == sizeof(y)
```

Another property required for this permutation function is that it needs to be [bijective](https://en.wikipedia.org/wiki/Bijection). What it really means that the mapping between input and output pairs is one-to-one. Let’s say if we have a permutation of numbers within 1–4. This is a valid permutation:

```
1 - 3
2 - 4
3 - 3
4 - 1
```

And this is not, because 3 is mapped twice as the output:

```
1 - 3
2 - 3
3 - 1
4 - 4
```

Normally, these permutation sizes are really large — something around 256-bit integers. But the basic idea is that no input or output can get mapped twice.

So what does **claw-free** mean? It’s really just another jargon. If we have two permutations $$F_0$$ and $$F_1$$. If there’s no efficient way to find a collision, namely find x and y such that $$F_0(x) = F_1(y)$$, then we call these two permutations a claw-free pair.

If we quickly picture these permutations in our minds, they are basically like really messy intertwined lines that map nodes in one set to nodes in another set. If we want to find a collision in the output between two mappings, we can’t help but have to brute-force every line to look for collisions.

Finally, let’s add in the last property to this thing — a **trapdoor**.

Normally just by looking at an output of a permutation, it will be very hard to reverse the permutation and obtain the input. It almost feels like that we can only go from input to output, but not backward (such property is also called a **One-Way Function/Permutation**). However, having a trapdoor enables us to trivially go from the output back to the input very efficiently. With a trapdoor permutation $$F$$, we can almost think that once we have the knowledge of its trapdoor, we will have access to its inverse function $$F^{-1}$$.

Now putting it all together —To construct the Chameleon Hash, we will need a Claw-free pair of Trapdoor Permutations. So let’s get into it.

### Building the Chameleon Hash Function

Once we have the Claw-free pair of Trapdoor Permutations (TDP), we are ready to build our Chameleon Hash Function.

**The Setup Phase**: Basically we find the Claw-free pair of TDP $$F_0$$ and $$F_1$$. The public parameters $$pk = (F_0, F_1)$$ and the secret parameters $$sk = (F_0^{-1}, F_1^{-1})$$.

**Hash**: In order to hash some fixed length message m, here is how we will do it:

1. First, we will write m in terms of a sequence of $$k$$ bits $$m[1]...m[k]$$.
2. Then, we sample a random nonce $$r$$ from the permutation space.
3. Starting from the first bit of $$m$$, if $$m[1] = 0$$, then we apply $$F_0$$ to r. If $$m[1] = 1$$, then we apply $$F_1$$ to $$r$$. We keep doing this for all the $$k$$ bits of m and obtain the final Chameleon Hash.

If we write the hash down more clearly, it will look like:

```
ChamHash(m, r) = F_m[k](...(F_m[2](F_m[1](r)))...)
```

Pretty neat right? To follow the tradition of Cryptography, after introducing a new construction, we need to prove it.

Since the Chameleon Hash Function is a commitment scheme, we will need to prove two properties: **hiding** and **binding**.

**Hiding**: It’s kind of trivial in this case given that one cannot really reverse the permutation given the output (without knowledge of the trapdoor).

**Binding**: This is the interesting part to prove. Assuming that Alice can find m_0, r_0, m_1, r_1 such that the two message-nonce pairs result in the same commitment. We can visualize these two messages:

```
m_0 = 0 1 1 0 0 ... 0 1 0 1
m_1 = 1 0 1 0 1 ... 1 1 0 1                    
      1         ...   i   k
```

Let i be the index where all the bits in $$m_0$$ and $$m_1$$ after i are the same (including i). We can basically “strip away” the permutations that we apply in the Chameleon Hash for bits $$i+1 ... k$$, because they are the same. Eventually, we will end up with something like:

```
F_m0[i](F_m0[i-1](...(r_0)...)) = F_m1[i](F_m1[i-1](...(r_1)...))
```

Since the bits start to differ on the $$i-1$$ bit, we can rewrite the equation as:

```
F_m0[i](r_0') = F_m1[i](r_1')
```

Here the $$r_0'$$ and $$r_1'$$ stand for the stuff inside the original equation. Since we know for sure that these two values are going to differ (at a very high probability), it means that we have found a claw! This breaks the claw-free assumption of the permutations. Therefore, Alice couldn’t come up with two different message-nonce pairs that result in the same commitment!

**Q.E.D.**

Once we prove the security of this construction, next I’m going to show how the trapdoor works.

From the previous section, we all know that the trapdoor to this commitment is simply the inverse permutation $$F_0^{-1}$$, $$F_1^{-1}$$. Once the receiver receives the message, he can simply apply the inverse permutation in the reverse order and get back the nonce $$r$$ that Alice created.

```
r = F_m[k]^-1(F_m[k-1]^-1(...(ChamHash(m, r))...))
```

So how does the recipient forge another valid opening? He can basically choose **any arbitrary bogus message** $$m'$$ and then do the reverse permutation based on the new message! Then he will obtain some other $$r'$$ that works for this opening.

```
r' = F_m'[k]^-1(F_m[k-1]^-1(...(ChamHash(m,r))...))
```

This new pair $$m', r'$$ is perfectly valid, because anyone else could apply the permutations in the forward direction and obtain the original commitment! But if the recipient has the power to produce any valid opening pairs… No one will trust what the recipient says! Yay, that’s **almost** our signature scheme.

In order to make it into a full signature scheme, we need to **combine the commitment/hash scheme with a normal signature scheme** (RSA, ECDSA, etc). But before getting into that, I would like to talk about how to actually build these amazing hash functions.

![](https://miro.medium.com/max/1890/0*f8kUglx9BH6QlTqW)

### The Construction — Factoring based

In order to build a Chamaleon Hash Function, we know that we just need to build a Claw-free pair of Trapdoor Permutations. The paper briefly introduced two candidates that have this property. The first one is **factoring based**.

If you know RSA, then you know that RSA is based on the assumption that it’s very hard to factor a large integer N into two prime factors $$N = pq$$.

Here we will use the same idea: We basically set a large integer $$N = pq$$ where $$p$$ and $$q$$ are prime numbers. We set the permutation functions $$F_0, F_1$$ to be the following:

```
F_0(x) = x^2 mod N
F_1(x) = 4x^2 mod N
```

Pretty simple, right? And actually, assuming that large integer factoring is hard, this is proven to be claw-free!

But what’s the trapdoor to this? The trapdoor is just the knowledge of primes $$p$$ and $$q$$. If you know them, then you can very efficiently compute the square root when inverting them. **If you don’t know $$p$$ and $$q$$, then it will be very hard to compute the permutations in the reverse direction**.

### The Construction — Discrete-log based

If you are familiar with other Crypto algorithms, you should be expecting this section to come.

Whenever we build some generic algorithm, we can always fill in the blank with a set of candidates. Integer factoring being one of them, and the other one is **Discrete-log based groups**.

I’ll probably write another post about how groups work, but basically it’s like the following:

Imagine if there’s a **field of numbers**, and all these numbers **sit in a ring**. If a number goes too high and reaches the max, then it **falls back to 0 and starts over again**. We call numbers (or generally speaking, elements) that have this property a group.

If you are picturing something like a 32-bit unsigned integer that overflows back to 0, you are on the right track. 

The simplest group is a finite field of integers. For example, all uint32 values form a group of size $$2^{32}$$. There’s also a special notation for a group $$G$$ with size $$q$$: $$Z_q$$. Usually, we want this $$q$$ to be a prime because everything works elegantly when there are prime numbers around.

In every group, we can find some element $$g$$ that’s called the **generator** of this group. What it means is that if we repeated multiply this element $$g$$ by itself, we can **obtain every single number in this group**. Here we gave a very simple example where generator $$g = 3$$ and group size $$q = 5$$.

```
Group = {0, g, g^2, g^3, ..., g^q}
{0, 3, 3^2 mod 5, 3^3 mod 5, 3^4 mod 5} = {0, 3, 4, 2, 1} 
```
Once we understand these fundamental ideas of how groups work (although there are many more nuances), we can directly use these groups to create Chameleon Hash Functions.

During set up, both parties need to first agree on what **group** they will be using and they need to fix a **generator** $$g$$ of the group. The recipient will randomly sample an element $$x$$ from the group $$Z_q$$. Then he simply sends the generator raised to the order of $$x$$ — $$g^x$$ to the signer. We denote this term as $$y$$.

So how does the signer create a valid commitment? First, she needs to sample a random nonce $$r$$, and then she simply computes:

```
ChamHash(m,r) = g^m * y^r
```

Pretty simple construction right? Now we should prove that this scheme is indeed hiding and binding.

Before getting to the proof, we need to take a look at the famous discrete-log assumption: **Computational Diffie-Hellman Assumption/CDH**.

The CDH assumption stemmed from the Diffie-Hellman key exchange protocol. Basically, it says that performing integer logarithms on group elements is hard. Namely, if we have $$g$$ and $$g^x$$ in some good group $$G$$, it’s computationally infeasible to get $$x$$ just by looking at these two given elements. In our case, by looking at the $$y$$ from the recipient, the signer will have no idea what the random $$x$$ actually is.

Now let’s see the proof.

**Hiding**: The hiding property here is actually based on the assumption that if you don’t know the exponents $$(m, r, x)$$ to the generators, then the output will just look like a random number to you. Because of CDH, one cannot extract any valuable information given the output and the generator.

**Binding**: This scheme is binding because of CDH. Since the signer has knowledge of the value $$x$$, she cannot really produce another pair $$m', r'$$ that opens the hash commitment. I won’t show the detailed proof here, but basically, if the signer is able to produce such a pair, then she can efficiently recover the original $$x$$ the signer chose.

Finally, let’s see how would the recipient forge an arbitrary opening. If the recipient wants to open the commitment into a desired bogus message $$m'$$, then he will need to produce $$m', r'$$ that satisfies the following equation:

```
g^m * h^r = g^m' * h^r'
g^m * (g^x)^r = g^m' * (g^x)^r'
m + xr = m' + xr'
```

Since the recipient already knows $$x$$, he can simply obtain the necessary $$r'$$ by $$(m + xr — m')/x$$.

And now we are done! If you made it through here, you already understand two valid constructions of the Chameleon Hash Function. The next is just to combine it together and make it a valid signature scheme.

### Putting it all together

Since we already discussed how the signature scheme works at a higher level, I’ll briefly recap the signature scheme here. Assume we use the discrete-log based construction.

1. During the setup phase, Alice and the platform agree on some certain group $$G$$ and its generator $$g$$. Then the platform will randomly sample an element x and pass along $$y = g^x$$ to Alice. Alice will also generate a signing key and a verifying key for a normal signature scheme (like ECDSA).
2. Alice will then make her bid (let’s say her bid is 100) and sample some random nonce r. She will produce a Chameleon Hash $$hash = g^{100} * y^r$$. Then she can sign the hash with a regular signature scheme to obtain the signature $$sig = Sign(sign_key, hash)$$. Finally, Alice sends the signature along with the hash and the bidding to the platform.
3. The platform verifies the validity of the hash by running $$Verify(verify_key, hash, sig)$$.

Again, if the signature and the hash are leaked to other parties, people will only see that Alice signed on some random garbage stream of bytes. If the platform tries to provide a valid opening to this hash, **no one will believe him because he has the power to forge anything he’d like to**. This ensures the secrecy of Alice’s bidding.

Problem solved. Now we have a pretty cool signature scheme that we can choose to only disclose our signatures to designated parties. Alice is now happy.

### Further Enhancements

In the original paper, the authors didn’t just stop right here. They also elaborated on how to enhance this protocol even further. I’m going to talk about two interesting ones.

**Recipient’s Identity**: Right now, in this scheme, Alice didn’t really specify whom she wanted to disclose her signature to in the signature. This empowers Alice so she can deny any signature if she doesn’t feel like accepting them. She can simply say — Oh this signature was intended for someone else, not you — to get around the legal disputes every time.

The way to fix it is to also let Alice sign the intended recipient’s name in her normal signature. Then Alice couldn’t lie about it anymore.

**Exposure-freeness**: The other concern is that in the case of legal dispute, it seems like Alice has to provide her $$m, r$$ pair in order to prove a collision to the judge. This will, unfortunately, leak Alice’s original message m to the public. Maybe Alice will be too embarrassed to reveal her message in court.

The way to get around the problem is also very cool. The fact is if the recipient ever presented a forged $$m', r'$$ pair to the court, Alice can use the information of the $$m, r, m', r'$$ pairs to **totally recover the original $$x$$**! Then she can simply use the trapdoor to forge any arbitrary collision she wants. I won’t go in detail about how this works here, but feel free to check out the [paper](https://pdfs.semanticscholar.org/1c29/4428c76ba7d1d0bb5e1d1bc931138c092453.pdf) if you are interested.

![](https://miro.medium.com/max/1890/0*7FYUjXbDxKp4t2-q)

## Afterthought

Woah, I didn’t realize that I have written this long in this post. But this was a pretty interesting idea to think and write about.

Before finishing up, I also want to talk about possible applications.

### Potential Use Cases

**Privacy-Preserving Auction**: This was Alice’s example I gave in the post. We can also extend this to a lot of other scenarios such as in submitting trades in a stock market and participating in a business contract. And of course, this could be written into a **smart contract**!

**Designated-Recipient Messaging**: This could be a cool extension to our messaging systems. Since infosec is such a hot topic right now, and the Internet is like a hodgepodge of malicious parties, we want to make sure that what we say on the Internet is only sent to the groups that we trust. Although this could already be done on Facebook or Twitter, there’s no mechanism that prevents them from spreading our secret information to other people. Having these designated validation schemes will definitely empower us to have a more privacy-preserving digital life.

**Data Lifecycle Management**: We want to see where trusted data are generated and how do they propagate in the cloud pipelines. We want to make sure every bit of data we see comes from a valid source and channel. This might sound impossible to do at this point, but with this kind of protocol, we can at least prevent the spread of data to unwanted places and limit trusted data to only flow in designated channels.

### What comes after

Chameleon Signature wasn’t the first signature scheme that has this interesting designated-verifier property. In fact, there was this Undeniable Signature in the 90s that has a similar idea but uses a heavier Zero-knowledge construction.

After Chameleon Signature, there are a lot more interesting signature or commitment schemes. Mercurial Commitment that came out in 2005 was another great idea that gives the signer the power to “choose” at signing time whether this signature could be opened in the future. Later in 2012, Vector Commitments came out and it was another fascinating idea. Instead of committing to single messages, we can actually commit to multiple messages in a set and prove the validity and position of a message in it.

There are so many fascinating ideas and algorithms in the world of Cryptography that I just don’t have enough time to read about everything and formulate them into actual blog posts. But I’ll keep doing these blog posts and share interesting things along the way of my adventure.
