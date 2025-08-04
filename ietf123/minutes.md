## IETF-121 QUIC WG Agenda

## Thursday, July 24, 2025

14:30-16:30 Thursday, Session III

### Administrivia

Chairs: Lucas Pardue, Matt Joras

Note takers: Marco Munizaga

Slides: https://github.com/quicwg/wg-materials/blob/main/ietf123/chairs.pdf

#### June Interim recap

(See slides)

Kazuho will present possible solutions

Gory F: Recap sounds correct

Christian H: On the charter text, I would like to see the charter text say secure as well as reliable. I'm worried QMux is a way to repeat the disaster of NSA(hard to hear?). it breaks encryption of QUIC. I would like the text to say "reliable, secure, and bidirectional byte stream"

Gory F: The next sentence says TLS will be the default if not secure.

Christian H: If that's how others read it, that is fine. It's much easier to be part of the consensus if it doesn't lower the security of quic.

## WG Items

### 15 min - multipath QUIC

#### #557
Lucas P: as an individual, What is APPLICATION_ABANDON?

Mirja: This is the non-error closure case.

Lucas P: I'll take a task to follow up.

Christian H: APPLICATION_ABANDON is the normal case. Why did we close this path? Because the app said so.

Lucas P: Having PATH in the name helps. Thanks

#### #558

Christian H: If anything is controversial and not necessary, we should remove it. In part because I think the draft is too long.

Ted H: I'm not sure why you need standard behavior here. We should take it out

Alessandro G: As an implementor, I'm not sure what I would do with this. Take it out

Christian H: ..Describe the history for the text...

#### #550

Kazuho O: Is there new information since we published RFC 9000 that makes us reconsider? We explicitly allowed the server to send tokens containing multiple IP Addresses. I don't think the situation has changed, so I think we don't have new information.

Mirja: Martin T had some comments here, but not currently present.

Lucas P: Speaking on behalf of authors, do you have answers you're looking for?

Mirja: If we don't have new input the current solution stands. We should follow up with martin T.

Tilmann Zäschke: The token is too big and there are too many tokens. Would be good to limit the size of the tokens.

Mirja: It should be up to the server to distribute the tokens

---

Lucas P: We'll have a last wglc once we hit issue 0.

### extended key update

Viktor Dukhovni: Seeing the same slides in TLS, does it make sense to do this first in TLS, then bring it here?

Yaroslav: That's what we're trying to do

Viktor: What about timing? Does it make sense to implement here?

Yaroslav: TLS stacks aren't QUIC specific for this, so it makes sense to work on it in parallel here.

Christian H: How far are we from getting the verification and proof that this is secure? (formal analysis process)

Yaroslav: It's in the queue, but I don't have time frames we can share. Ongoing work. Depends on initial implementations.

Christian H: I would not want to do implementation process on my side until the TLS process has been completed. It seems odd requirement since you'll be compromised in the middle, but not compromised at the end.

Yaroslav: The TLS draft is a requirement for this draft, so this can not progress faster.

Sean Turner: We did send the TLS document to the formal analysis process, so it has kicked off.

Kazuho: As an implementor who works on a TLS stack for both TCP and QUIC, it helps to have this brought here.

Lucas P: Sounds like we don't need to spend too much time here if there are no updates. Seems like we are at a good balance. No need to worry about being in tight lockstep.

### address discovery

we're ready for wglc.

Lucas P: Please read the draft.

### ACK frequency

#### #321

Ian S: Kazuho, do you have proposed text?


Mirja K: It's not just about retransmitting, but also about congestion control.

Ian S: This lets you make the "undo" happen earlier

Kazuho: I think it would be better to have a SHOULD because it prevents mistakes. I've updated my patch now.

Mirja K: I want to highlight that we previously chose to keep RFC 9000 behavior, but now we are changing it.

Ian S: This change came from clarification of what exactly we were trying to do. Please

Jana I: The whole point of the ack frequency was to reduce the number of acks. In this case did the receiver communicate the gap?

Ian S: The receiver must have communicated a gap before this applies.

Jana I: ok, I understand

Gorry F: As an individual, what are we optimizing for? What are we making less robust?

Ian S: Would it be helfpul to run simulations to see how bad it is?

Gorry F: How bad is it when it goes right? And how bad is it when we lose some acks. We should make a decision so we could move on.

Mirja K: I'm confused now. The second case can lead to problems if you have a large reordering threshold and never send an ack.

Ian S: Second case you think it's lost

Mirja K: You should send an ack to tell the other end it wasn't lost. I thought we were only discussing the first case.

Ian S: I believe the draft already mentions that if we don't send an ack we shouldn't send this ack, as it doesn't matter.

Mirja K: I don't think the current draft does.

Jana I: Example case: you receive 1, 11, you don't report ack. You get 2 and now you report an ack, you get a 3 you report an ack. This isn't what we want. It's also somewhat common case.

For the second case, I don't care much about. keep it simple.

Mirja K: Second one is a change in the decision we made in RFC 9000 that I don't think we need to change.

Martin D: If you get 10, and then 1-9 that's 10 acks in RFC 9000. That's not what we want. If using this draft currently we would send 9, would be nice to do better.

I find it hard to reason about the case where there is high reordering threshold and high ack frequency. Should there be guidance in the document?

Martin D: If you had low ack frequency and if there are lots of individual pack losses, you might drop certain ack ranges.

Ian S: I think we should keep the behavior of 9000 that everything is ackd at least once.

Martin D: I think there's still an edge case here that happens in this draft and not 9000.

Matt J: Should we make an issue for this?

Martin D: I think it's one of the open issues. And there's some other thinking around this and some others need to think about what happens when we use large numbers here.


### QUIC Ack Receive Timestamps / Extended ACKs/

#### #19

Jonathon Lennox: Can we have an IANA registry for a total order?

Ian S: Possible. Is that better than putting it in the draft?

Jonathon Lennox: What happens if we have multiple drafts in flight? Or private extensions?

Ian S: the latter is more concerning to me.

Jonathon Lennox: Can qlog handle this? Can they interpret this without a lot of help?

Matt J: Why would this be special?

Jonathon Lennox: Should we have a recursive type?

Matt J: That's one thing that was removed from this last draft.

Jonathon Lennox: then I would prefer iana registry.

Kazuho O: Do we need an order?

Ian S: We don't now

Kazuho: Even tls extensions don't have order and we're fine. I think we should strike the order prescription text.

Mirja: I thought last time we discussed just using a new frame.

Jana I: I'll agree with striking the RFC number here, and leave the problem to future proposals. We shouldn't worry about the general extensibility problem here.

Lucas P: One draft I'm working on is extensibility and evolution of a protocol for the IAB. I'm worried about this work.
In QUIC we are strict on negotiating of the protocol. No specific suggestions, but noting that I'm worried.

Ian S: I believe the current format is compatible with MP-QUIC.

Jonathon Lennox: Concern about saying that all new ACK stuff must go into new frames.

Ian S: We've been concious about putting things in the ACK frame that are relevant to the congestion controller

Mirja: This information is independent relative to each other.

Ian S: how you process it is somewhat dependent.

Mirja: Timestamp can be given to the congestion controller independently.

Christian H: First, I like the timestamps. Second, please don't call anything MP-QUIC. Prefer QUIC multipath or Multipath extension to QUIC.

Lucas P: On the note of having multiple frames, it seems resolvable to me since the sender controls how frames are packed into a datagram.

Ian S: We're going to remove the RFC ordering, and we'll talk about how it integrates with QUIC multipath.

Mirja: I would like to redesign the frame. I want it to be compatible in a different way.

### QUIC stream multiplexing - comparing wire protocols

4 Approaches to how we do qmux. See table from slides.

Tommy P: Do you imagine there would be a CID somewhere to recognize session migration?

Kazuho O: Interesting to see the option to migrate from tcp -> udp

Tommy P: the packetization version seems the only possible one to migrate.

Kazuho: I think either packets or v1 frames could be migrated.

Alessandro: From an implementors perspective, the capsule implementation might not be easier. You still have to implement the QUIC framing from scratch. Using v1 frames seems straightforward and require fewer changes.

I rather we didn't change the packet header or omit fields. It's easier to skip things, but slightly tweaking formats is a bit tricky.

Ben S: 1. We should make sure option D is in the new charter. I think Option B from a webtransport perspoective would be trivial.

Kazuho: Option D seems out of charter currently, I'd like to keep it in charter.

Jana I: I think C is best. It's important to present what problem we are solving here. An initial motiviation was to get h3 on top of tcp without a lot of new code.

Alan F: I agree with Ben, it would be easier to build from h2 if I have a WT over h2.

Ian S: I care about performance. I'm willing to reimplement my quic parser. Code reuse is nice but not critical. At the h3 layer, qpack and such code reuse is critical. Being reasonable on the perf tradeoff is important.


Mirja: Should we use frames or capsules? I think we should use frames since this is the quic wg. My question is for solution a, (not arguing for it), we are nearly there. What are we missing there?

Kazuho: wt-over-h2 only talks about h2, we still need to talk about how to do it over h1.

Victor V: first observation is that the problem with d. You can't multiplex it with other tcp/tls applications. My personal perspective is that the logic is how to multiplex multiple flow control streams over another flow control stream. Most of the logic I had to write was about buffer and prioritization.

Christian H: We need a solution where we are running an application based on quic, but the local network will not less us use udp. Then qmux over tcp/tls. Running QMUX over tcp tls over HTTP connect would be nice

Marco M: Preference for C

### As time permits

#### Deadline-Aware Streams for QUIC/QUIC-Multipath - Tony John

#### 10 min - QUIC optimistic ACK - Louis Navarre

Lars: You need to generate acks for packets that are sent. There is a window here and how tricky is to generate the correct window. It was not that difficult.

#### 5 min - preview of Instant Acknowledgments in QUIC Handshakes - Jonas Muecke