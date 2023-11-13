
# IETF-118 QUIC WG meeting

## Wednesday, November 8, 2023

14:30-16:30 Wednesday, Session III

Chair: Lucas Pardue

Notes: Brian Trammell + Robin Marx (for moral support) + Spencer Dawkins

### Administrivia

5 min total


### Chair Updates
* 10 min - General updates about the WG [slides](https://github.com/quicwg/wg-materials/blob/main/ietf118/chairs.pdf)

**Lucas Pardue [LP]**: Ack frequency to WGLC. One issue that needs discussion, but not today (see online). Ready for interop/implementation experience.

**LP**: Discussion on QUIC demuxing from other UDP-based protocols; see slides for more info. Several proposed solutions on the mailing lists. 1) Change RFC 9000 to remove subclause. 2) change RFC 9443 (more effort because not QUIC document) 3) Change RFC9000 unless OOB knowledge (SHOULD -> MUST) 4) Change RFC9000 to provide more info to implementers/leave risks up to them. If anyone has strong opinions on an option, speak now (or forever hold your peace).

**Mirja Kühlewind [MK]**: No strong opinion. But four.

**Kazuho Oku [KO]**: We thought demuxing was a smaller? concern but thought the version negotiaton was going to take a long time ...

**Martin Duke [MD]**: Just for VNEG packets? LP: yes. MD: then probably nr 3, but any of these are fine.

**Alessandro Ghedini [AG]**: Do we need to do anything? Isn't saying QUIC might be multiplexed equivalent to option 4?

**Christian Huitema [CH]**: I'm for four as well, if we have to do something. Version negotiation as defined is probably a mistake because it is a great attack vector to take down an ongoing connection

**Marten Seemann [MS]**: Lots of ways to bring QUIC handshake down in early stages; not sure we need to fix vneg in particular. Strong pref for option 3. 4 sounds like if you're running implementation you don't need to do anything, but you DO. If you run public QUIC server, you don't know what the client is demuxing on the same socket.

**David Schinazi [DS]**: (QUIC enthusiast) Changing RFCs is great and all but that doesn't change implementations. Do we have data on what servers are doing? This is relevant for a P2P app with mux on both sides. If they're doing that they're not going to care what the RFC says. What's the motivation for doing the change?

**LP**: Not as chair: we want uncoordinated endpoints to be able to work on the internet and this could be an issue. Changes are just clarifying an intent that we probably had. Asking for data is a good point, but don't want to block this on that.

**Jonathan Lennox [JL]**: Nobody's recommended it. Not 2 please. Timestamp problems with p=2^-32. When you're not muxing but your peer is -- because 9xxx says you need to pay attention to 5-tuple. Only need to worry about this on the same 5-tuple.

**LP**: If my recollection is correct: client is listening on same port and server can't know.

**JL** : still knows on what IP+port it got QUIC from, which it got RTP from etc.

**LP**: If using same source port for both, you could end upt forwarding to the wrong thing. Let's consider and take discussion to the list.

### Multipath QUIC
* 25 min - Open issues, updates to [multipath QUIC](https://datatracker.ietf.org/doc/html/draft-ietf-quic-multipath). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf118/multipath.pdf). **Yanmei Liu** and **Mirja Kühlewind**

**MK**: (Issues 179/214 on Path ID) How important are these isues?

**KO**: discussed 214 previously. Seem to be more arguments against, haven't made any progress yet. How can we progress without closing issue?

**MK**: exactly the problem. Seem to be split, not sure how forward; Maybe we do a hum today. Either change draft or do nothing? changing draft is a bit of extra work.

**Christian Huitema [CH]**: Firmly in the do nothing camp. The CID rotation hole is by design. New stream cannot be correlated with the previous one. You need some distance between the paths to get that property. Doing this quickly causes linkability; you need a long silence. This is by design. Let's do nothing and publish.

**MK**: Want to correct  myself. Still need to solve 118. Not protocol change, just clarification needed.

**MS**: CID rotation not the only problem here. Number of other issues described in 214. Haven't implemented multipath but have thought about it. The easier way to implement wouldP be explicit path IDs, so strongly in favor of making the change here.

**MK**: Think it depends on how your implementation works if it's easy or not.

**Ian Swett [IS]**: Prefer without path IDs. Do agree the CID rotation is annoying, though last change is implementation-dependent. If change CID but same path, can choose to keep loss detection the same. Encryption/decryption thing isn't an issue unless you have tons of CIDs in flight. Personal opinion.

**MD**: (Connection ID Enthusiast) We need rotation, not just for privacy, can also break routing when there is a LB on the path

**MK**: You can close issue #273

**LP** to close [#273](https://github.com/quicwg/multipath/issues/273)

**KO**: Path ID proposal makes some things easier. OTOH it changes the data structure more from what we have, because two layers or path -- PID and CID. Will be pain for existing implementations.

**Mike Bishop [MB]**: The slide is probably a more useful way to think about this, proposal to separate PID from CID. For the PID we already have, do you have one or many CIDs? PID -> many CIDs seems like needless complexity. I believe we already have path ID, which is CID seq nr. Do nothing

**CH**: Agree with what MK said. Cannot do away with CID rotation. I disagree that the problem of having simultaneous NAT rebinding and CID rebinding is extremely rare if sending packets back-to-back. The NAT isn't going to change the binding in between two packets. Only changes when NAT reboots or when big silence. If latter, then effective new path. Also true that Congestion Control should change. Loss recovery is then also irrelevant, because no packets in transit. So no problem with current solution.

**MK**: I agree. Still need to solve the problem where you're not sending for a while, you might end up with two paths, the new path, and the old path that won't work anymore. There could be recommendation work to detect this quickly.

**CH**: If this is a problem in practice, can do extension with new Frame that says: this path is continuation of previous one. Don't beleive this will be a problem in practice though.

**MS**: Without PID we don't have an explicit limit on the number of paths, the number of CIDs is probably higher than the paths you want to allow. Resource management is strictly worse. You can also get a path status frame with a CID seq you already retired, i.e., that you cleaned up state in the stack. Not clear how you can make this work without the PID, because otherwise you need to keep CID seq state due to arbitrary in-net delay. 9002 LR is tied to PN space. We all agree that LR is per-path, if you rotate CID and end up with new PN space, LR becomes a lot more complicated. You need to link PN spaces with math.

**MK**: You can track both for a while, or just lose a couple of packets, not a huge problem.

**CH**: Marten: when you remove state in impl, it's actually a sleight of hand. remove state at cost of maintaining more state for the path besides that, so think that's equivalent.

**MS**: (silent head shake)

**MK**: chairs, what do we do?

**LP**: hearing tradeoffs. Let's do a show of hands to see how people feel. Need to phrase question correctly.

**YL**: might have interim meeting before next IETF. Maybe need more implementation experience for tradeoff between two solutions?

**MK**: want to get sense of where WG stands. Only heard some voices, want to get broader idea.

**KO**: If show hands, point out that path ID proposal isn't even a PR, so don't know the details yet. Needs to be phrased as "interest in Y" instead of "choose between X and Y".

**Brian Trammell [BT]**: What I'm hearing is a lot of the opinions one way or the other are from implementers who are actually trying to make this work. For me putting my hand up that's gong to be based on an arbitrary sense of the complexity. This is something we need to test.

**MK**: who would be willing to implement the proposal then? Ask that as well.

**LP**: Let's ask those two questions then. (__aah !#&@__)

**LP**: Are you interested in exploring Path IDs further? y/n? => 20:11 (out of 134, 103 without opinion)

**LP**: Do you have interest in participating in an interim/interop to explore path IDs? y/n? => 9:19 (110 no opinion) + yes speakers. Seems like a sizeable number of people interested in implementing / meeting in interim.

**MB**: second question conflated interim and interop. More people can show up to an interim than will interop.

**LP**: in the room show of hands for interOP: not seeing any hands. Half an arm + MK. So action for authors is to first have proposal to see if people want to implement it, but chicken/egg problem... can folks who care about this deeply meet for a coffee later so we can make progress?

**MK**: more people at the mic to say why they voted yes on the first question?

**BT**: (YES enthusiast). My judgement about whether I am for or against the path id thing is based of conceptual complexity rather than implementation complexity. PIDs are explicit. I like explicit signaling. Advice from the peanut gallery: Say we'll do nothing, and if people appeal you'll know you have strong opinions in the room.

**CH**: voted no. Strong opinion. Proposal to split Path ID and CID makes decryption/encryption harder, specifically decryption. Requirement right now is that decryption engine, which is often offloaded, just needs to know CID number corresponding to a given CID. Easy to do unilaterally. If you disconnect the two, then you need negotation/state and push that to your decrypting hardware. Sizeably more complex than whatever datastructure you have in your code. Strong reason to NOT have this complexity.

**Ted Hardie (TH)**: Explicit signaling enthusiast. I'd like to explore this further because the sequence number and path ID do the same thing. I'd like to see a PR that treats this as a tuple. What happens when you need to change one and not the other, how does that work? Treating these as an identifier in the form of a tuple might get past some of that complexity.

**MS**: (in chat) I'd be happy to work on a PR

**LP**: Good input. MK: don't have PR right now because would touch the whole draft. LP: who would like to explore this further, please help with the PR.

**BT**: Would it make sense to write up what this type of tuple-based system would look like without touching the draft? Just a 3-pager that explains the reasons. Don't want the reason NOT to do this just to be not wanting to touch the draft.

**MK**: MS seems to have the description of this in 214, so we have that. Do need PR to know what -exactly- this will touch.

**LP**: _somebody_ has a task there to do a PR. Looking at MS? He's nodding, so great :)


### Reliable Stream Resets
* 15 min - Open issues, updates to [Reliable Stream Resets](https://datatracker.ietf.org/doc/draft-ietf-quic-reliable-stream-reset/). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf118/reliable-resets.pdf). **Marten Seemann**

_Marten is upping his game in terms of slide layout. Robin is getting scared._

**MS**: seeing thumbs up for naming bikeshed RESET_STREAM_AT. thanks!

**MS**: Thoughts on STOP_SENDING_AT?

**JL**: Receiver has to know what's in the stream it didn't receive. Works for fixed-size headers only.

**MS**: In Webtransport it's a varint, so eight octets

**MK**: If you know the length, how can you know which stream?

**MS**: You're draining the whole connection.

**MB**: You're sending STOP_SENDING when you don't need any more. The data STOP_SENDING_AT points at is probably already in flight.

MS : I think the use case is not as clear cut as the reset stream . Restores symmetry to the draft.

**Victor Vasiliev [VV]**: same concern. Answer is that STOP_SENDING already acts as enough. Nothing preventing you from replying to stop-ending to reset stream if you know there's some contraints like "it's a webtransport data stream" (_notetaker note: probably misunderstood some of this_)

**LP**: I do like the symmetry. IIRC AVTCORE in RTP over QUIC has asked about this feature. Maybe not having this feature (or not having a decision) is blocking RTPCORE. Don't understand how much additional complexity? Doesn't seem like that much?

**DS**: (QUIC enthousiast) Symmetry is nice. We don't care. We don't make pretty protocols. We make protocols that work. Looks good = not a good reason to put it in a draft. Unless someone has a clear use case, strongly object to putting it in.

**MK**: Everything DS said, and if you really need this you can just have another extension and just do it.

**KO**: Application protocols that need this complexity can do it in app space.

**Mo Zanaty [MZ]**: Concrete use cases do come to mind. Deliver headers you know are important without payloads are useful in media applications. e.g,. MOQ when you know you don't get all segments you intended to, but do want headers that are critical to keep decoding data you need to. Useful to at least get first chunk that's critical for later steps.

**MB**: if we don't do this, i would support a text change to point out that STOP_SENDING can elicit a RESET_STREAM or RESET_STREAM_AT

**LP**: Optimizations at the cost of protocol complexity don't set well with me (individual).

**MS**: confused here. Getting mixed feedback. Would like to ship new draft and enter WGLC soon. Need to resolve this one way or another. Would love decision now. Show of hands?

**DS**: STOP_SENDING has an app layer error code. You could stuff the "please reset stream at" semantics in the app error codes.

**LP**: Do you want STOP_SENDING_AT in this draft? y/n? => 2/30 (110 no opinion). Clear result.

**MS**: second issue then.

**MD**: How can you guarantee that the reduction arrives in the order? Could you end up increasing?

**MS**: Same as with flow control updates.

**MD**: Act upon the lowest then? cool.

**VV**: That makes sense. RESET_STREAM is RESET_STREAM_AT(0). Will complain if I can't implement this.

**MD**: We can cut a new draft now, are we starting WGLC?

**LP**: That seems reasonable, need to confirm with co-chair. Not this week. Pleased we've been able to adopt and turn this around quicly.

**DS**: as Webtransport chair, +1, thanks for doing this quicly.

### qlog

* 15 min - Open issues, updates to [qlog](https://datatracker.ietf.org/doc/html/draft-ietf-quic-qlog-main-schema). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf118/qlog.pdf). **Robin Marx**

**Robin Marx [RM]**: This is the oppenheimer update. Large bomb. Need input on non-merged issues.

**LP**: As an author, reiterate that "move" doesn't mean text we have will go into a new doc. Text was in the adopted document so we're asking the WG.

**Alan Frindell [AF]**: QPACK enthusiast. I had commented on the issue about what high-level events would look like, did that not turn into a PR?

**LP** That made it to us, but having a PR is just step one. We'd need more work to make this correct for multiple implementations. Not seeing implementers wanting this.

**AF**: has used bespoke logging for QPACK debugging. Don't really have time to drive this forward, if this is blocking.

**BT**: nuke it.

**Q Misell [QM]**: QPACK is its own RFC. Its own specification for QLog makes sense. Do it.

**MK**: on ECN, editorial issue: capable does not equal "now sending with ct(0)". Not correct for L4S.

**LP** Hearing no QPACK removal objections.

**RM**: (path proposal [#336](#) (without multipath enthusiasm)

**MK**: by adding a path ID you can cover the migration case where connection changes but same path, a field for any kind of path information also needs CID, because otherwise packet number doesn't make sense.

**RM**: You can associate mutliple connection ids with a single path ID.

**MK**: ACK received has a path ID and a packet number and that's not suffcient to actually identify where it belongs.

**LP**: Could we do some offline experimentation with Quentin? Might come back to Mirja with questions. Big step in the right direction.


### QUIC Address Discovery

* xx min [slides](https://datatracker.ietf.org/meeting/118/materials/slides-118-quic-address-discovery) **Marten Seemann**

**MS**: is there WG interest in this work?

**KO**: thanks! this is fairly easy to implement. current request/repsonse protocol without flow control has H2 rapid reset problem. frame doesn't have to be defined as a probing frame, can always send on the path already known to work.

**Colin Perkins [CP]**: You can clearly do this and it will clearly work, and in many ways I think it's a good idea. Currently we have one way of doing NAT trav which is widely used and I'm worried about fragmenting, because it reduces the cost of blocking one method or the other. We should think about the implications of this.

**MB**: Agree that request frame not good here, separate setting into in "interested in getting observed address when my address changes".

**Peter Thatcher [PT]**: Does this happen before or after the handshake? This happens during the lifetmie of the connection and during the lifetime of half. Without 0RTT in the one RTT case you'd have an extra round trip comared to STUN, is that correct?

**MS**: yes, no replacement for STUN. Mre if running P2P node that's running QUIC traffic anyway and now using that to also learn about address

**PT**: That's the whole reason for STUN... recreating over QUIC. That's fine, just want to understand. Additional point: STUN has authentication mechanism. Will that be in here as well?

**LP** let's not get bogged down on technical details on a non-WG draft.

### NAT Traversal
* 20 min - [QUIC NAT Traversal](https://datatracker.ietf.org/doc/draft-seemann-quic-nat-traversal/) [slides](https://github.com/quicwg/wg-materials/blob/main/ietf118/nat-traversal.pdf). **Marten Seemann**

_Marten Seemann is turning out the be the new Martin Thomson in terms of productivity_

**PT**: on the "we don't do ICE" slide, a better way of saying this would be you're doing ICE, you're just using QUIC packets instead of using STUN packets. Fun thing to explore. But a lot of work. Need to understand benefits of replacing STUN with QUIC.

**Jonathan Lennox [JL]**: In most WebRTC use cases you still need a rendezvous server since server won't have a CA-signed cert. Self-signed needs fingerprint exchange. Not having a signaling server then seems moot. Requiring that the server maintain a publicly routable address... will follow up offline.

**CP**: I agree with PT. ICE works because of the multi-RTT behavior and matching algo. Will be hard to beat by just doing it in QUIC.

**MS** : So in the very first version of this draft in SF we were basically replicating ICE, this draft is not doing that. All error handling happens on the client side.

**CP**: Check that thatW werorks ''very throroughly. We found corner cases months after initial spec.

**Luke Curley [LC]**: Is this an extension, or can we just use STUN?

**LP** Is there sufficient interest to do NAT-related work in the WG, would like a clear signal of interest. Show of hands: 20:11 130 no-opinion.

### ACK Receive Timestamps
* 10 min - QUIC ACK receive timestamps [slides](https://github.com/quicwg/wg-materials/blob/main/ietf118/timestamps.pdf) **Sharad Jaiswal [SJ]**


__From chat__: LC: Speaking of WebRTC-over-QUIC, we absolutely need this extension to reach parity with WebRTC (to implement GCC)

LP: people interested in this should discuss more and bring experiments etc to the list.

### BDP Frame
* 5 min - [QUIC BDP frame](https://datatracker.ietf.org/doc/draft-kuhn-quic-bdpframe-extension/) [slides](https://github.com/quicwg/wg-materials/blob/main/ietf118/bdp-frame.pdf). **Gorry Fairhurst**

***(no time remaining, not presented)***

**LP**: apologies, will do this next meeting.

### FEC Results
* 10 min - FEC results (François Michel) [slides](https://github.com/quicwg/wg-materials/blob/main/ietf118/michel-fec.pdf). **Francois Michel**

***(no time remaining, not presented)***

**LP**: apologies, see MoQ.
