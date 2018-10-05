# QUIC Working Group Interim Meeting Minutes

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

  - [September 19, 2018](#september-19-2018)
    - [Topic 1: Spin Bit](#topic-1-spin-bit)
      - [Alexandre Ferrieux (Orange) --  Spin bit and Beyond](#alexandre-ferrieux-orange-----spin-bit-and-beyond)
      - [Marcus Ilhar (Ericsson)](#marcus-ilhar-ericsson)
      - [Brian Trammell (ETH) -- Intraflow Diagnostics](#brian-trammell-eth----intraflow-diagnostics)
    - [Speed Dating - Martin Thomson](#speed-dating---martin-thomson)
    - [Interop Results - Christian Huitema](#interop-results---christian-huitema)
    - [QPACK index wrapping - Alan Frindell](#qpack-index-wrapping---alan-frindell)
    - [Connection ID DT - Mike Bishop](#connection-id-dt---mike-bishop)
    - [First octet - Martin Thomson](#first-octet---martin-thomson)
    - [End of early data - Martin Thomson](#end-of-early-data---martin-thomson)
    - [1570](#1570)
  - [September 20, 2018](#september-20-2018)
    - [ACK ECN - Ian](#ack-ecn---ian)
    - [Retry - Martin Thomson](#retry---martin-thomson)
    - [Load balancing document](#load-balancing-document)
    - [Handshake deadlock (issue #1764)](#handshake-deadlock-issue-1764)
    - [Max_bytes_before_ack - Ian/Jana](#max_bytes_before_ack---ianjana)
    - [Flow control gotchas - Mike Bishop](#flow-control-gotchas---mike-bishop)
    - [Planning stuff](#planning-stuff)
    - [QUIC next generation](#quic-next-generation)
    - [PR from EKR (PR #1755)](#pr-from-ekr-pr-1755)
    - [QUIC transport interface - eric kinnear](#quic-transport-interface---eric-kinnear)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
    
## September 19, 2018

### Topic 1: Spin Bit

#### Alexandre Ferrieux (Orange) --  Spin bit and Beyond

Demonstration of the spin bit graph

Discussion of the graphs -- these just show the output of the spin bit measurement, but they don’t compare to any ground truth

Orange is experimenting with three bits (spin bit for RTT + two bits for segmental loss), but QUIC has only done privacy analysis of the single Spin Bit. That privacy analysis was done by a design team and then accepted by the working group - the other two bits must also be analyzed and accepted in order to go forward

Plan A: work with a partner to take E2# measurements

Plan B: work without a partner (simulate a spin bit using TTL hacks)

General suggestions for future experiments: experiments for RTT measurement must compare to some other view of RTT:
* TCP-derived RTT
* ICMP-derived RTT
* Endpoint RTT estimate

Experiments need to have enough runs to be significant, and probe the “edges” of the parameter space -- what network conditions make it break?

Lars: also wants anecdotal evidence that this provides equivalent information to TCP-based measurement techniques on real networks.

Spencer: please let the WG know what you’re proposing for experiments before you spend a lot of time on it… comparing to endpoint-based measurements isn't the same as comparing to ICMP-based measurements, for instance.

Jana: Also consider malicious endpoints.

Christian: QUIC is an application-level transport, so spin measures application RTT. Are there implications here? (Zahed +1)

Alexandre: This is equivalent to TCP. Kernel on a loaded CPU doesn't run faster than userland.

Christian: when you present in Bangkok please present data about how much noise is injected by the application layer.

Jana: We do expect this to be noisy.

#### Marcus Ilhar (Ericsson)

(clarifies that he is not for or against any bits beyond one bit spin)

Discussion of heuristics for using the spin bit

EKR: What does the most trivial experiment show? Put a probe directly adjacent to one device. Answer: we haven’t done it.

Lars: Have you measured reordering in space, not time. Answer, no, it’s hard.

Ian: 10% reordering is very high.

Lars: As you’re going toward LTE, have a realistic topology with realistic delays.

Jana: I care more about how the mechanism works and what the boundaries are, less about “real networks”. So what happens when one or both endpoints are scrambling.

ekr: the argument is that people have real world diagnostic problems, and I don’t know how to evaluate that independently. Can you wak through how you normally diagnose and how this fits in.

Christian: for the real networks, you can get pcap samples where there actually are problems, then see if you can inject the signal on top of it. For a realistic setup, I’d have the middlebox observe several paths, and have one path randomly misbehave, and see if you can find it.

Lars: Another type of useful information is what density of bits need to be spinning to be useful for operational purposes?

Marcus: very interesting question, no simple answer.

Brian: Depends on the size of the aggregate.

Mike: Multiple versions of QUIC, how to identify which bits are spinning.

Spencer: "how many packets need to give you useful spin bit signals" pushes on incentives for deployment. Are non-participants freeriding? This is an interesting question to talk about, but not now :-) Lars

#### Brian Trammell (ETH) -- Intraflow Diagnostics 

Demonstration of how to use TCP tools to diagnose TCP problems

Brian argues that we would like to have those similar tools for QUIC.

Lars: how often does this happen with network-oriented diagnosis versus midlebox-oriented diagnosis.

Jana: +1, motivate why we need this in the middle, as opposed to at the edge.

Brian: see draft-trammell-why-measure-rtt

Ted: we don’t want to have to decrypt the whole flow. what parts of the current encrypted part of the system would need to be decrypted and sent to the operator. 

Mark: quic-trace

ekr: what I want: demonstration of long-term fidelity of spin against other measurements. two worked examples: diagnosing from endpoint perspective, diagnosing from midpoint perspective. scenarios: with or without endpoint cooperation.

Spencer asked whether we needed to make a decision about the spin bit in order to send the invariants draft for Last Call, and Lars reminded Spencer that we do have bits that could be used for things like this in the invariants draft, although those bits are greased now. 

Lars: what I am going to be looking for is that people will have interest in shipping. 

### Speed Dating - Martin Thomson

We have issues that need attention, or need to be killed. Three minutes per issue, identify proponents (authors) and timeline for resolution. No proponent, issue closes.  List is available:
* https://github.com/quicwg/wg-materials/blob/master/interim-18-09/speed-dating.pdf 
* https://github.com/quicwg/base-drafts/issues/1668 - close this issue, but this is less useful that fullly exercising VN. ekr to open issue for his PR
* https://github.com/quicwg/base-drafts/issues/1620 -  can close with no action, but if SETTINGS changes with an non-varint encoding then [unintelligible]
* https://github.com/quicwg/base-drafts/issues/1608 - marten to drive discussion in list and write a PR.
* https://github.com/quicwg/base-drafts/issues/1600 - close with no action
* https://github.com/quicwg/base-drafts/issues/1579 - close with no action
* https://github.com/quicwg/base-drafts/issues/1578 - substantial objections to making this change, so close with no action
* https://github.com/quicwg/base-drafts/issues/1575 - ekr to run to ground with DavidS in two weeks (from 9/18)
* https://github.com/quicwg/base-drafts/issues/1570 - Review this later in the agenda
* https://github.com/quicwg/base-drafts/issues/1513 - close with no action, may take to list

### Interop Results - Christian Huitema

[Transport Interoperability](https://docs.google.com/spreadsheets/d/1D0tW89vOoaScs3IY9RGC0UesWGAwE6xyLk0l4JtvTVg/edit#gid=1897717037)

ekr: lots of changes recently, takes a while to get it to work.  Even once it works, there’s a lot of work to fill in this matrix. Can we make it simpler?

Christian: lots of implementations trip on the same kinds of changes, e.g. initial flow control window in transport parameters. default to zero, nothing gets sent. bug of the week.

Christian. We’re almost back to where we were back in april. Good news: picoquic + quant, picoquic + ATS can now do migration. Testing migration on client side was a 20-commit PR. Other implementations are probably server-side only, need more trials of this feature in next interop. We need more Ms to approve that part of the spec

Jana: Should also try make after break. Christian: That’s what we tried. You can’t do break-after-make by changing ports.

Martin T: Not much HTTP here either. Two extant implementations that haven’t tried to talk to each other.  Two more which are mostly complete but don’t have current versions of the transport.

Christian: There’s also no key rotation. So we’re specifying something with no code at all behind it.

Lars: We also need to fix some flow control cruft around stream open. 

ekr: quasi-cosmetic changes interfere with updating functionality.

Christian: Yep. We’re making changes that are incremental improvements.

Jana: Going forward, more changes should be driven by implementation experience.

ekr: We should just do -14 for Bangkok.

Christian: maybe fix three bugs.

[QPACK Interoperability Spreadsheet](https://docs.google.com/spreadsheets/d/1zpOWVNd_t8iEYsQJD8MEMHOkkJ3U1w7yx6furjw3iTw/edit?usp=sharing)

Shout out to Dmitri!

### QPACK index wrapping - Alan Frindell

https://github.com/quicwg/wg-materials/blob/master/interim-18-09/qpack%20wrapping.pdf

Ian: If I never get to the point where I wrap are there any savings from changing LR to be non-absolute?

Alan: No.

Ian: Defaults are 64k?

No default.

Dmitri: http is not just for web -- long lived connections or connections with high volume of requests (or both) may show significant degradation in compression performance.  I ran a simulation of a scenario wherein server reply contains three headers -- never-changing :status and content-type and cookie that changes every ten requests.  10,000 responses have 0.13 compression ratio when absolute index wraps versus 0.15 when it does not (14% worse).  100,000 responses is 0.13 compression ratio versus 0.16 for 19% deterioration.  So the difference is not insignificant at all.

Kazuho: option 2 and option 3 are basically just an editorial difference?

Alan: yes, we could also do two, plus an appendix that says “hey you can implement this a ring buffer?”

Kazuho:  Prefer to do something, and leave editorial decisions to editors

Brian:  Modulo reservations about compression in general, this seems like minor incremental complexit. Like the efficiency win (especially for pathological, non-web cases) and describing this as a ring buffer.

MT: Willing to live with do nothing

Jana: Willing to live with do nothing. It’s simpler. In the larger scheme, this doesn’t seem like a big win.

Subodh: Willing to live with do nothing.  xDoes this preclude further optimizations along the lines of independent-stream updates a la QCRAM?

Alan: need to think about it.

Jana: For context, new connections are cheap, especially if you’re doing so once a day.

Dmitri: data structure is sorted by largest ref. ring buffers are easier here.

Alan: we also use a ring, can mod LR…

Brian, Jana, others:  QPACK is already complicated enough, but that could be used to argue either direction.

Coin flip?  No -- hum.  Result:  NO ONE CARES.

hum for do nothing / do something: first hum was louder but fewer, second hum was more people but louder. no violent disagreement.

ekr: if the yankees win, do nothing

Resolution:  Do option #2 or #3.  Alan Frindell will decide which one.


### Connection ID DT - Mike Bishop

https://github.com/quicwg/wg-materials/blob/master/interim-18-09/CIDdt.pdf

Subodh: what happens if the client only has one and wants to retire it?

Martin T: that’s connection close. core observation is you need to provide more than your peer needs.

Christian: We might want to write down the edge case

Mike B: the other side can force feed you. we recommend 8, but other side can force 256 on you.

MT: if I give you 256 and you only want to remember 8, you can just throw them away. 

Eric: if you get all the way down to one then you’re saying you only want one. re force feeding: you don’t want to churn retirements. by throwing out 252 of 256, you’re basically saying you want 4…

Brian: did you consider flow control?

MT: yes.

marten: why don’t we have a transport parameter? 

MT: expectation 1 is that the number of CIDs you need during the lifetime of a connection is fairly stable. if someone wants to forcefeed you, yes, but they can also force you to expend state in other ways. so no need to defend against it. didn’t rule out transport parameter, just did not think it was baked.

kazuho: we thought 8 was sufficient… WRT too many, as peer retires CIDs, endpoint should send new CID....

marten: that’s a SHOULD? kazuho: yes.

subodh: I like this better than flow control approach… if you have a reversible function [please fill in]

ted: if recipient retires a CID, can respondent refresh with the same CID?

MT: not recommended, you’re doing this for non-linkability. causes RTX and retirement issues. we rely on uniqueness.

marten: what if we decide a value and then every implementation needs to defend. defense is retire-immediate. then we recommend more. then you get retirement cascade

MT: idea is you have to ignore CIDs you don’t want.

Jana: the replacement semantic is important. so how about we call this replacement request.

eric: idea behind TP is to say “please give me X” but other end can always ignore. 

marten: suggest a cap as well. possibly a TP.

mike: reordering could cause appearance of cap exceeded?

subodh: cap conflates DoS protection with how many the server is willing to send you. doesn’t really seem analogous to flow control. there’s a request frame, but server can send whenever it wants.

kazuho: a hard cap is dangerous. need a soft cap of course. it’s easier too.

marten: if we rename the frame, or make it explicit that retire always gives you a new one, then we don’t need a hard cap.

igor: retire frame is not idempotent.

MT: text in the PR deals for how long you need to remember CIDs you may have already retired

mike: 3RTO for deduping all of this.

kazuho: assuming we use a 5tuple-set for multiple connections, if you change everything at once you break linktability

ekr: how do you avoid looping? i want to hear an algorithm.

MT: it’s a level trigger, not an edge trigger

Christian: the first packet that comes back on a new CID contains a path challenge response. new CID always has path challenge/

ekr: no, why?

MT: if you’ve been idle for some period of time then you just use a new CID.

Christian: server will typically then send a path challenge...

ekr: when we did this for TLS, we had a lot of counting-to-infinity. 

MT: there is a task for someone to work this out.

Christian: in this case, we’re creating a new path, and need a 3whs on that path.

Jana: on the port change, won’t you have the same problem?

Mike: in v1 only the client is allowed to migrate. we will need something better for multipath.

Brian: suggest we look at Christian’s “new path” primitive moving forward.

Eric: migration explicitly leaves open a couple of cases for endpoints that need to migrate in a hurry, e.g. preprobing. we need to run those down.

Jana: re retiring CID while stateless reset in flight, we should specify a timeout here.

some discussion during break, Eric will capture in open PR.


### First octet - Martin Thomson

https://github.com/quicwg/wg-materials/blob/master/interim-18-09/first-octet.pdf

ekr: don’t see a lot of value in DTLS/QUIC demux. SRTP is different, where you use QUIC to establish keys then exfiltrate to SRTP. 

ekr: oh, wait, we do need to demux DTLS…

kazuho: we don’t need keyphase in long header, so we can bring it back for demux. possibly 0x40 bit for demux. i.e. 0b1101 == retry, 0b1100 == 0RTT, 0b1110 == initial, 0b1111 == handshake.

brian: given the short header demux, that would mean that !(first_byte & 0x40) == not QUIC. that probably becomes an invariant whether we 

martin d: what is the implication of encrypt zero versus encrypt random? 

lars: i would prefer must ignore.

MT: i will write up a PR for this one.

jana: i’m concerned about the quic bit.

kazuho: clients that don’t want to demux can set second bit to random.

martin d: does the client/server always know this?

MT: I think so, this is in pre-negotiated.

ekr: where this matters is where p2p UDP connection establishment is expensive.

Jana: can the client always set to one, then the server can set it to what it wants…

ekr: do I care about avoiding ossification about this one bit?

Christian: when do we expect a PR?

Lars: we need a timeline for next implementation draft, and this should be in there.

### End of early data - Martin Thomson

https://github.com/quicwg/wg-materials/blob/master/interim-18-09/eoed.pdf

now talking about handshake routing (last slide)

Igor: I would prefer not to route just on five-tuple, you might end up with large mux. If CID is changing, I don’t know how, and I don’t want to keep state.

MT: this maintains uncertainty about value of CID for long header

Mike: Not consistent across all zero RTT packets, so you really don’t have anything except the 5-tuple

Subodh: you could encode something about “this is my CID” in the CID itself…

ekr: the server should choose a CID for subsequent packets that routes the same as the CCID. 

Igor: server ID is the last N bits of the SCID. doesn’t work if I have a CCID

ekr: use consistent hashing…

Jana: you have logic based on CID / packet type… hash on 5-tuple

Christian: we have a limitation that we will only ever have one ongoing handshake on any given 5-tuple.

kazuho: can we use connid length to differentiate SCID and CCID?

igor: it’s a probability game.

Jana: you can choose an SCID that maps to the same route as the CCID CCID (as ekr says).

Igor: it needs two properties: it routes the same way, and when it is just used by itself…
mike: do this in a prefix.

martin d: we already have this problem with the initial ack.

[name not known]: why not have a random cid bit?

MT: don’t we have the bits? we could reuse the QUIC bit.

Jana: why can’t we do 5-tuple hashing for all handshake packets?

Christian: do 5-tuple, if you want to be smarter, do so. can be more constrained on initial CCID. 

MT: I’d like to be able to grease the length.

Martin D: If everyone uses 5-tuple switching then stakes for CCID are low.

Jana: we have a way forward. 

MT: yes, the real rule we have for coalescing is that they are intended for the same connection, does not need to be same CID. this is just a reasonable change independent.

### 1570

https://github.com/quicwg/base-drafts/issues/1570 

ekr: we did this on purpose, we wanted not to allow short CIDs in order to avoid birthday problems. if nobody cares, we can change it back.

kazuho: reusing a CID is hard, since CID is tied to stateless reset token.

marten: depends on key rotation period and incoming rate

ian: this is only for client-side CIDs, or for P2P? no server wants to do this.

MT: you’re trying to overload ephemeral ports? 

Ted: the consequence of connid retirement is you need to keep track of the burned ones… may force a rollover. 

Jana: Small connection IDs makes it possible to enumerate stateless resets, which is a problem.

subodh: smaller CIDs also don’t support migration.

Jana: this is for muxing a small number of connections.

Christian: but P2P is one of those things for which you want migration

ekr: there you want ICE migration, not QUIC migration.

MT: dumb suggestion: put a shim in. 

marten: this is invariant, but most arguments against are v1-specific.

kazuho: you can do a split design by putting small CIDs in 

Jana: given that invariants are what’s on the wire, if we want to use 1,2,3 bytes, we can encode that, but we can prohibit them in V1.

christian: do handshake with 8-bytes, use transport parameters to only use smaller number of bytes. fits fully within the invariants.

ekr: short header is the only thing that matters, and we can have short connids on short packets anyway, having the encoding limitation in the spec is not very useful.

ted: if we agree that some of these values are uncommon, this is separable from the how-small question. let’s separate it then. 

subodh: fan of the current encoding. don’t want to lose it. +3 is very simple. no restriction on short cids in future for short headers. leave long header as in, introduce change via transport param and/or new version.

MT: I can change the invariants section 4.3 to say that CIDs are arbitrary length. in the long header, only the following lengths can be encoded. maintain restriction on < 4 byte CIDs in V1.


## September 20, 2018

### ACK ECN - Ian

https://github.com/quicwg/wg-materials/blob/master/interim-18-09/ack-ecn.pdf

Drawbacks of current design: counters increase indefinitely, does not indicate what packets were marked, ACK and ACK_ECN often overlap.

Could (1) leave as-is, (2) encode ECN/not ECN in ack blocks, (3) bitvector for acked packets

Kazuho: (2) and (3) work for any kind of marking scheme

Martin T: the bitvector doesn’t need a length field; it’s for all acked packets.

Brian: bitvector is way easier for debugging

ekr: why not split the bitvector out into a separate frame, could put a largest ack in a separate ack/ecn frame.

Christian: that would require a new error condition

Ekr: That’s not true. the largest ack field can resolve the inconsistencies.

MT: what about ACK, then ACK_ECN, the former has no bitvector, the latter has a bitvector. 

Ian: To be clear, in option 3, the bitvector only replaces the counter. has anyone does size analysis on the vector?

Christian: The bitvector size scales with the congestion window.  

Subodh: common case is whole flight is acked

Christian: Not if you use L4S. multiple feedback per RTT means there are different ECN marks on each packet. 

MartinD: Does this imply having to build a whole new receiver data structure? 

Ian: Yes. Crap. You have to keep the bitvector around, compute gets hairy.

Christian: just make the editorial change in the text, but leave it as it is and fix it in v2 if necessary.

Igor: could encode delta from largest ack

Lars: that may not save you any bytes if the count is low.

Brian: We might be tipping over to where ECN becomes more popular.

Ian: option 4: optimize status quo. Just merge the ack frames with a type bit. I don’t think bitvector is viable with big congestion windows.

Jana: Regardless of marking, bitvector bloats ack size

Lars: does anyone want to move away from the status quo?

Group: no. This leaves options 1 or 4.

ekr: we should not burden everyone for ECN geeks

jana: ECN is used, though not widely. we need to be ready if it’s deployed soon.

Lars: Operators worried about QUIC. ECN gives you a way to more finely control QUIC traffic.

Jana: Let’s not relitigate ECN here.

Martin T: There are 3 values in the ACK/ECN frames: ECN(0), ECN(1), ECN-CE. Do we want to change that? (get rid of CE)

Brian: no. Because of L4S.

MT: Make unmarked a counter instead of ECN(0). In case of a new path.

Christian: we are not doing multipath in v1.

Martin D: should we flush counters when we migrate?

MT: no: some counts will be unusable due to packets on both paths. on new path, we’re diffing from the point where this settles.

Lars: we can’t you start at zero?

Christian: we don’t know when to set to zero.

MT: unmarked would impose a burden on more people. means more ACK_ECN because counters change continuously.

Jana; drop a counter and infer the others based on Largest acked.

Brian: when will v2 happen? (not basic fixes, the next big feature add)

Jana: if L4S happens, let’s do v2 then.

Ian: consensus: Option 4?

Kazuho: keep counters separate. one is usually 0, so not much cost. Spec should be easy to implement. (FTW)

MT: ACK and ACK/ECN will occupy two adjacent code points and they will have the same name. Counters remain the same.

(general agreement)

Zahed: 5G has an L4S option.

### Retry - Martin Thomson

https://github.com/quicwg/wg-materials/blob/master/interim-18-09/retry.pdf

CID authentication: sort-of for handshake, not at all for Initial/Retry. Could tweak it to treat part of CID as the packet number.

Client Initial: messing with CID will break routing and/or keys; no problem here

Server Initial: change SCID? Maybe, but would have to modify HS. Think about it more.

Middlebox can spoof Retry and strip token out in following CI. This affects the DCID for all incoming connections! Thus we have all the Initial Keys, which could be a single one.

Christian: Retry is designed for middleboxes (load balancers) to do stuff like this.

Kazuho: Could lead to ossification, if other versions don’t allow Retry.

Ekr: could direct to a specific endpoint, which is by design

MT: design requirements: middleboxes should be able to do retry for DoS, etc. But we’d also like to authenticate that Retry

Ekr: this involves sharing some key material. Is this per-connection or configuration coordination between middlebox and server?

MT: simplest answer is to add transport params (e.g. hash or excerpt of retry packets)

subodh/ekr: authenticate in the token.

Nick: Azure won’t deploy shared state between DoS device and servers.
Bishop: Toggle on back end server to report if I expect retries.

Christian: Server could echo token it it s parameters

Subodh: this protects against key manipulation, not DoS

Kazuho: We need to know the original DCID. could encode it in the token.

MT: token is self-authenticating if it gets through. Add client transport parameter: “I received a Retry for this original DCID”

Igor: could report the number of RETRYs in the transport parameter.

Martin S: Almost everyone is behind a DoS box. So we’ll ossify around not being protected.

MT: Maybe allow only one Retry.

Martin D: what if I inject retries? Does this turn off DoS boxes?

Ian: No, I can just pick one. Something is probably legitimate, and I can safely ignore the others with this change.

Nick: what if server has large certificate, and a DoS device might be there? The server might try to send a Retry too.

Ian: TCP only gives you one syncookie

Igor: similar point to Nick

Jana: maybe we should tell them not to do that.

Ekr: Point of QUIC is to be more end-to-end.

Martin D: DoS middleboxes will ossify around QUICv1.

Nick: What we trying to protect with one retry?

Ian: this system (with multiple retries) may be impossible to understand

Jana: let’s move forward. we understand what happens with one retry with and without coordination. We don’t understand multiple retries. But they might happen! Does the server care about the middlebox?

Jana cont’d: If we care about authenticating retries, we only care about one.

Martin S. but then we can’t prevent middleboxes from doing everything. Independent middleboxes should be impossible

Nick: Azure can’t support that.

MT: We could disallow stripping of the token so we know there’s a middlebox.

Christian: we don’t want coordination, but server should know it’s an expected middlebox.

Martin S. How do I know there’s a DoS server from my provider? We should force there to be coordination (key sharing)

Brian: how about sharing a secret?

Ian: Unknown tokens tell you there’s a box there.

ekr: what are we trying to do here? (1) there should not be a middlebox that rewrites anything without server consent/knowledge; and (2) there must not be any coordination. This a conflict.

Nick: shared knowledge vs. shared key -- know

DKG: we must know not only there is a middlebox, but a particular identity

MT: uncoordinated has a problem. two tokens come: previous conn, or retry. if not coordinated, the boxes can’t handle each other’s tokens.

Martin D.: won’t DoS box drop 0RTT tokens?

Nick: Not in path unless under load.

Brian: Cloud providers not that great about providing network information. We seem to be talking about levels of coordination that some of the deployment models for QUIC are simply not prepared for.

Jana: what do we specify, what is a reasonable deployment? Is server Retry authentication a MUST or a MAY?

Lars: are we closer to something?

ekr: same tension, allow uncoordinated interference or not? this is really complicated.

lars: can we do something in v1? this doesn’t affect invariants

Brian: do one retry - proposal on the slide.

DKG: adding coordination makes it a 3-party protocol. cloud doesn’t mean trust is not a problem.

brian: I agree. do not allow flip bits in-line.

ekr: YANG!

christian.QUIC-aware untrusted middleboxes are not good.

MT: Proposal is not sufficient. I can differentiate my own retry and new_token tokens. if a middlebox generates retry token, it will be rejected if it appears to be retry token, ignored if new_token token. This token has to be explicit.

kazuho: i object. no more moving pieces.

christian: explicit communication where middlebox requests a token.

kazuho: if so, move it out of the WG.

break for lunch.

After lunch, it was concluded that in some scenarios (e.g., clouds) to assume that they do not have one of these DoS prevention boxes in front.  THe comms between the load balancer and DoS Box is going to get done later.  In the transport draft we’ll put something that mandate a set of behaviors on servers and clients. Server will have to offer some sort of proof that it knew that there was a retry going on and the client will have to check it. Only single retry will be done which was agreed on. Some configuration will have to be done to tell the end server of the presence of the DoS box. @mt to write this up with all of the mart*s.

### Load balancing document

We have have a discussion of whether or not to make it a WG document. 

Martin - it might be painful to deploy in cloud without lb doc

Lars - if DT has achieved consensus, we can discuss in Bangkok. Once we know what the transport draft says about connection ids, we can talk about the lb draft

### Handshake deadlock (issue #1764)

https://github.com/quicwg/wg-materials/blob/master/interim-18-09/Handshake%20deadlock%20%252F%20DoS%20mitigation%20(%231764).pdf

Server must not send 3x unvalidated bytes. Current text incorrectly described as 3 packets, needs fixing.
If the server sends a flight of data, with an ack of the client finished and the handshake packets in the first flight is lost or the server flight is larger than 3 packets, then the server gets into a deadlock. 

Ekr -> server reliability is normally driven by RTO, however in this particular case this is not okay. The amplification factor is 3x number of times you will retransmit these packets.

Jana -> Server sends the packets after a period of time and not immediately

Ekr -> Attacker could space out the attack

Christian -> aren’t we redoing IW 10 discussion

Room -> no

Ekr -> IW 10 is sent after you validated the path, and not before. What is the number you can allow until validation? If 30 then that solves the issue
Jana -> If you do TFO then the server will send the data

Ekr -> In TFO you “theoretically” have address validation. 

Christian -> clarified

Ekr:  the analog in QUIC is token

Jana: If you want to do exactly what tcp does, you would allow handshake packet and set timer

Ekr: We had previously agreed that factor was 3, but we could say that it could be much larger
Martin: Doesn’t work
Ekr: Jana’s suggestion might cause every normal connection to take longer.

Martin: We could have a budget or allow timer to bypass limit

Lars: we could ack every packet

Jana: Server can’t assume that we’re going to get an ack every packet.

Ekr: what happens if entire server flight is lost. We spent a lot of time  on this, unless we have a way for the client to retransmit, we’re going to be in this situation

Victor: Can we have client garbage collect connection and retry

Mt: Its probably cheaper to fix this connection than create a new one.

Kazuho: Amplification is about size of the packet and not about the packets. 

Approach 1: client keeps sending

Ian - One approach is for clients to keep sending even if server hello is recvd or not. 

Mt- once you know server has validated the path, the client can stop this behavior.

ekr- You are going to send your own finished.

Ian - client has to make sure that something retransmittable is on the wire

Mt - if you get an ack on the handshake keys, you can also validate the path. When the client knows that the server knows that the path is validated, it can stop doing retransmissions.

Jana - the idea is that you’re retransmitting things because the server cannot move forward

Christian- this is like a keepalive for the handshake until you have handshake keys

Jana- does this incentivize the client to send a large number of packets?

Ian - another idea to use the token field in the ack of the server hello to used as path validation.

Mike - why wouldnt you use path challenge?

Ekr-  because we already have a mechanism in the right place.

Ekr - this approach seems like a v2 thing. We can do this when we see if this is an issue. We should not do this

Kazhuo - why wouldn’t it work if it sent this token on every initial packet? Validation of initial packet becomes simple

Ekr - if the clients acks are always lost, then not good. The case has to be big server hello.

Mike - if the server knows that it has a big server hello it can put path challenge in there.

Martin - can we un-disallow path challenge in initial packet. Big shlo problem is theoretical.

Jana - we excluded it but its flip-flopped.

Some discussion on using HRR. People didn’t like it. 

@ekr, @ianswett writing this up. Agreed to write up client keeps sending approach.


### Max_bytes_before_ack - Ian/Jana

https://github.com/quicwg/wg-materials/blob/master/interim-18-09/ack-delay.pdf

Ian - How much to delay acks? Some congestion controllers need frequent feedback like reno and max ack delay influences RTO timers, so ack delay matters. The less frequently the receiver send acks, if the sender doesn’t have pacing enabled, it’s going to cause bursts.

Option 1: 1- size fits all

Mt - all 3 of those variables we suggest a cap on it.

Martin - packets vs mss?

Ian - good point. Needs resolution. Most people prefer packets based on feedback received.

Ian: only concern is reno throughput decreases with these settings.

Jana: Point is that these are only recommended values

Brian: We shouldn’t recommend something slow

Option 2: Sender dictates receiver behavior

Ian - if receiver is  not going to respect the properties?

Option 3: Receiver dictates its own behavior

Ian - tells the sender its policy

Lars - Brings up charter. Is this the same as working on congestion controller which is out of charter?

Mt - ack delay is input to the controller

There has been some experimentation with Max ack delay

Spencer - Congestion control was out of scope mostly to keep discussion focussed. Would not discourage anyone to think about these things.

Lars - can we do something simple?

Option 4: Sender and receiver have control 

Lars - No 

Jana - not as complicated. Let’s not stipulate the timer granularity of the receiver.

Brian - if we are going to say option 5, QUIC is going to ack similar to tcp then mobile networks might get overloaded

Lars - option 1?

Brian - Before we go to this, I want to see that performance doesnt suck in naive implementations.

Jana - it will be lower under netem. Should we tolerate change

Victor - does 10 packets with reno actually work?

Jana - the ¼ rtt is there

Mt - i think option 1 is fine. We have a bunch of max ack delay in the doc. I think we need option 1 + 3. The measurement doesn’t work.

Jana - i think explicit makes sense. Would propose something more conservative because we dont full grok the changes to reno to make perf changes to match. In absence of changing the controller, you can ack every 2 but you can experiment with > 2. Worried about the same concerns as Brian. 

Mike - if we can do something simple to get it out the door, expressing additional info sounds like an extension

Jana - key issue is around ack loss around measuring max ack delay implicitly. 

Mt - concerned about not being able to do  ack coalescing. We’re making a recommendation, do we have to go all the way back to 2?

Ian - If you had a slow receiver, you would naturally ack more than 2. 

Jana - For a dumb receiver, if you have good reason that more packets are coming, then you can wait, otherwise ack every 2. Aggregation for TCP is based on heuristics. 

Mt - we’ve seen in TCP that people implement coalescing in drivers. Why are we going to be advising people to send acks at a higher level than the network can tolerate

Ian - what is size of tcp vs quic acks? 

Jana - TCP is 40 bytes

Christian - at least 66 bytes for QUIC

Jana - In terms of CPU they are more expensive. Old constant based on arbitrary?

Christian - Simulations for TCP acks done on T1 lines.

Mt - we can put 2 as a number, and go to iccrg and ask them for a better number

Lars - its a bad idea to wait for the iccrg for anything.

Consensus seems like we are going to do max ack delay, the ack threshold is still an open question.

### Flow control gotchas - Mike Bishop

https://github.com/quicwg/wg-materials/blob/master/interim-18-09/flowcontrol.pdf

Mike - don’t wait for all bytes to arrive before reading

Mt- I don’t even write the entire data if I don’t have flow control to write it.

Dimitri - you should make your frame smaller

Roy - should we have a default limit? Can we go over?

Mt - we can still run into this issue

Alan - echos mt. You might never be able to send your request at all

Mt - yes that is possible

Jana - flow control happens at so many levels. At quic level, it does not know relationship between streams. Application is the one that knows how to deal with this situation and it is not a choice that quic can make. 

Alan - dont put data in qpack encoder stream if you know you dont have flow control

Mt - what advice can we provide?

Christian - data is not injected in the network faster than the app can read it.

Subodh: api can be more complicated

Chrisitan: footgun. Can consider priorities in flow control

Jana: This is not a deadlock if the application reads.

Alan : The receiver could have not chosen to send a flow control update.

Kazhuo: What happens if the sender is blocked on QPACK encoder stream.

Alan: Melbourne we decided to say “dont do that”. Pretend that the dynamic table size is 0 and not compress headers so that you don’t end up with HoLB.

Mike: we need text about edge cases. Encourage apps not to leave stuff in size buffers for various reasons. Don’t let a request go out on a stream which depends on something hasn’t been sent on a control stream.

Jana: could be noted in API documents on applicability docs

Sean: List should be exhaustive for IESG.


### Planning stuff

Hackathon 

2 meetings at IETF, no sessions on friday. Lars’ wife expects him to come home a day early

Would like to get 2 drafts out by Bangkok. One with resolutions to all the issues and second to structure. 

Lars: Do we want to do draft-14 or the next one?

Ekr: one option to expand feature set of 14. Or keep same features and go to 15. Prefers going to 15 and then expand feature set later.

Lars: Prefers -14. Feels like it might be a moving target.

Alan: Freeze transport since it pushes HTTP back. Argues for keeping draft-14.

Eric: Prefers going to -15. 

Martin: traveling and vacation.

Jana: next 3 weeks on issues done and shipped.

Mark: We should probably interop on what we’ve got. Draft deadline is in 4 weeks.

Ekr: would still prefer updating to -15.

Mark: lets give till mid october for -15.

Draft version should not block HQ interop. 

Mt: people should probably track the editors copy and then when -15 drops then it should be quick.

Looks like consensus is on working on -15. 

Bangkok plan: hackathon, Spin bit, and discuss changes that have happened.

Mark: I would like to decide on spin bit at bangkok. 

January interim+interop. Akamai or Google campus? Tokyo

We might need to update our milestones. 

### QUIC next generation 

What do we want working group to become once V1 is done. Partial reliability, FEC, etc. 

Jana: We should wait till we have mature deployment, implementations so that we know the problems.

Mark: We don’t have mature deployments yet

Martin: Currently the deployment of ietfish QUIC is FB right?

Jana: Google is also ietf quic ish.

Ekr: don’t want to start working on v2 during last call for v1.

Lars: We should leave it to implementers to meetup to decide on the features

Brian: Concerned that version number greasing is aspirational in defending version negotiation mechanism and get v2 out just to exercise it.

Mt: Take some of david benjamins ideas from TLS and apply them to QUIC

Martin: Bunch of drafts floating around. Should probably work on them. For example, Applicability and management, QUIC LB

Ted: Concerned that groups championing stuff like partial reliability will go off and do their own thing if the WG doesn’t do something about it in 6-9 months.

Mark: We’re communicating with these groups

Ted: The QUIC WG should allow work on QUIC to go to other places in the IETF that want to do work with QUIC.

Ekr: The question is whether QUIC is ready to be adapted to these protocols. 

Ted: If they don’t get to talk about it in 6 months then the decision will be made in not the IETF setting.

Jana: Experimental versions can allow such experimentation

Mt: If those people have requirements that the QUIC WG have to do work on, we need to be careful. Happy for other groups to start building on top of the protocol.

Roni: other groups can bring their requirements to QUIC WG while the usage will be defined in other WG, for example going through dispatch WG.

Mark: What is the label on box and how it can be used

Victor: no problem with people building on top of quic. 

Mt: Wouldn't want to ship something on quic until its done. There are some debates that need to happen if QUIC might affect the ecosystem of the web platform if something that depends on QUIC is shipped.

### PR from EKR ([PR #1755](https://github.com/quicwg/base-drafts/pull/1755))

Motivation: Reduce rtts for moving from QUIC v1 -> v2.

Ekr proposed tweak to version negotiation. 

Conceptually 2 version numbers: 1 is for complete incompatibility, second is for 2 versions which have the same handshake protocol. The client could offer up the set of versions it supports in the initial packet and then the server can select one of them.

Victor: Will limit your handshake format, but also limits zero rtt handling.

Christian: Allows greasing of version bit

Ekr: similar to TLS in negotiation vs current QUIC.

Mike: removes the need for client’s choice of the lowest of highest version it supports.

Victor: is this necessary for v1 or when we have a version that supports this?

Ekr: makes it easier to rollout the next version

Mt: Answers victor’s question. In the PR the client provides list of versions in transport parameters

Mt: needs sense of room of whether the PR is okay with people.

ekr:  Happy to have WG take it or reject it. Doesn’t want to lobby for it, but can work on it

Looked like no conclusion. But no opposition either.

### QUIC transport interface - eric kinnear

https://github.com/quicwg/wg-materials/blob/master/interim-18-09/quic-transport-interface.pdf

Should we expose the connection as a quic connection or transport connection as a quic stream.

Transport as QUIC connection

Ekr: are these alternative, or would we support both?

Eric: We could do either. Do you see a utility in one but not the other.

Ekr: How do you handle streaming data?

Eric: Well suited to atomic messages. 

Subodh: control stream un-ending sequence of bytes, not really a message

Eric: Is TCP a very long message?

Christian: Not true, you send a message get a reply. 

Jana: The idea of streams in QUIC straddles this space. API shouldn’t limit the use of streams. 

Transport connection is a stream

Christian: It is not. You will need to expose the property of all the streams change at the same time.

Jana: I don’t like this at all. Lot of stuff is shared, like flow control, congestion control, etc.

Mt: at the app layer, how much does this matter.

Jana: it matters for example how do we decide to share the security context?

Eric: Applications can specify some sort of policy. 

Subodh: Who is the user of this? HTTP has to have the context of all the streams that are open.

Brian: should schedule something in TAPS

Mt: Wanted some discussion about what roberto and jeff wrote up.

Mark: we didn’t continue that.

Jana: The problem is that QUIC does not fit into those boxes. Would rather map abstractions to reality rather than what exists. Strongly recommend we try to build something that exposes that stream can be exposed as a message (or something else, couldn’t catch this).

Eric: Main question is what is the piece that is missing, example objects? Can we have an early thoughts about what is missing.

Mike: 2nd diagram are the right blocks. Explain the concept of a connection that holds multiple read write streams. We’re losing information by using existing concepts.

Lars: There is an assumption that TAPS vocabularily is expressive enough to express what QUIC is capable of. What about multipath?

Brian: Something about postsockets that we might have to bring back.

Mark: Where should this discussion go? Eric got some feedback.

Lars: Would be happy for someone to pick up the pen of the document roberto and jeff had. Lars doesn’t care about TAPS. There is less value in keeping TAPS vocabulary.
