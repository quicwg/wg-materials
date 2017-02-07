# Minutes: QUIC Working Group 25-01-17

* Chairs: Mark Nottingham, Lars Eggert
* Scribes: Ted Hardie, Brian Trammell

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
  - [Administrivia](#administrivia)
  - [TLS Overview](#tls-overview)
  - [TLS Issues](#tls-issues)
    - [Issue 167](#issue-167)
    - [Issue 97](#issue-97)
    - [Issue 87](#issue-87)
    - [Issue 12](#issue-12)
  - [HTTP Overview](#http-overview)
  - [HTTP Issues](#http-issues)
    - [Issue #95 / #202 - CONNECT](#issue-95--202---connect)
    - [Issue #165 - Resetting Streams](#issue-165---resetting-streams)
  - [Transport Issues (resumed)](#transport-issues-resumed)
    - [Issue 175](#issue-175)
    - [Issue 66: Remove STOP_WAITING](#issue-66-remove-stop_waiting)
    - [Issues 104 and 114 on Priority and Retransmission Priority](#issues-104-and-114-on-priority-and-retransmission-priority)
    - [Issue 115 Connection migration](#issue-115-connection-migration)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Prior to starting the meeting, Brian attempts to convince the crowd that 62bit integers are the bomb.  Folks counter that putting the length indicator into the public flags instead, so that you can identify the offset from examining just one thing.  Rapidly, things devolve into a question of what gets encrypted.  Folks determine that with infinite memory, hpack and full encryption are trivial problems.  Ian suggests that we have a “bad idea fairy” bake off later in the day.

## Administrivia

9:31 starting with a review of the Note Well

Starting the blue sheets around again.

Brian takes scribe duties for the first afternoon session.

Went back through introductions.

Mark: yesterday was transport issues.  This morning is TLS, followed by HTTP. Martin will focus on TLS, Mike on HTTP. These sessions will let people know what is going on with those drafts, and then we can check the issues lists to see if there is low-hanging fruit.  After that, we will return to the transport issues in the afternoon.  Try not to rathole (understood that this will be difficult).

## TLS Overview

[Martin’s slides](https://github.com/quicwg/wg-materials/blob/master/interim-17-01/keyphases.pdf)

Martin:  one of the things we set out to do was to make sure there was no trial decryption, which is something that QUIC crypto does.  That doesn’t work in some TLS implementations.  We stole one of the bits that was being used for diversification and use it to indicate which key is in use.  This set of messages includes a certificate and thus the set tends to gets pretty big.  This is encryption in stream 1, but that is not visible to QUIC.  And now, the wrinkle:  because of reordering and retransmission, there are potentially three different versions of keys that might be sent from client to server.  (See slide 2)  Now you have a problem at the server, as you have one bit of information to distinguish among three things.  Suggestion to use version bit.

Mirja:  why do you need to acknowledgements prior to get the 1RTT key?

Martin:  to allow the server to repair loss of server messages used to set up the connection (packets containing certificate etc.)  Jana: are the acks going back to the server encrypted?

Martin:  they have to be clear text because the client doesn’t have the server messages, so it has no salient keys.  Possibly it could use 0RTT keys, but it doesn’t know that the server is accepting 0RTT.

The significance of using the version to distinguish among these packets is that you must wait for all the version information from the server.

Jana:  this changes the current behavior which stops when any version arrives; now you must wait until all version information arrives.  Martin: that’s right.

Jana: there is an issue here: this has a key schedule that is defined in terms of 0RTT.

Martin: In the situation that you have some other handshake, like one primed out of band, you would not use any of this machinery (or have any cleartext).

Mike:  would it simplify if we said that you always have a zero and one rtt key, but they are sometimes the same?  No, that likely doesn’t help as now you don’t know what transitions state.

Ekr asks how this is different from the 1RTT key exchange?  (Folks seem to agree).  Ian says that this appears to be a way to encode these three things unambiguously.

Jana:  but when do you stop sending version info?  Mike suggests that you can stop sending version info when you have both 1RTT and an agreement with server on a version.

MartinD: it might be helpful to clarify that some of these are in the clear, like retransmissions of ClientHellos.   Mirja:  do even want to allow it to send clear text data.

Martin: this isn’t “data”, this is the crypto bootstrap.  (Stream 1 data, not application data).

Lucas:  we have three bits in the public header that indicate the kind of packet, but we are treating them orthogonally.  Might it make sense to rationalize this and treat these as 8 different packet types?  That would allow you to capture some of the states that are not currently used.

MartinT and MartinD note that some of these may get used in key phase changes.

Question:  the server hello and the ack for the client hello can come in two different packets, right?  Yes.  Is there an encrypted silly state there?  The Server doesn’t have to acknowledge that ClientHello.  But if you don’t acknowledge them, then the QUIC layer doesn’t know what is being sent and so would generally ACK.

MartinD:  what if you have a multiple-packet ClientHello?

Lots of badness will occur. Folks tend to agree that keeping ClientHello to one packet would be usefully required.

Subodh asks if there is any case where a new variation of handshake will be invented in the future where the state machinery starts before ClientHello?  Would that require them to invent their own versioning mechanism?  (We are piggybacking on version negotiation because it and crypto handshake happen at the same time; what if that changes?)

Mirja suggests that the split of bits resolves the ambiguity because you are using one bit for version and one bit for negotiation.  Responds it that this may not be the case.  Perhaps it would be less ambiguity if we had two key bits.

Ekr:  there is another way to do this, following STUN:  use distinctive pattern rather than use a bit that we have to carry in every packet.

Martin:  let’s table that until the discussion on header patterns which is later in the meeting.

Jana:  I think if we simply treat this as 3 bits encoding 8 values, this is not problem.

Martin:  if we can do this only during negotiation phase, that would be better.  This works for now, and we can squeeze bits out later.

Martin and Jana agree that adopting Mike’s friendly amendment (use this until you 1RTT keys and version negotiation is complete).

Igor: we did talk about this yesterday. What happens if there is reordering of the 0RTT data?  Servers can drop straight on the floor or sit on it and wait for reordered data to arrive.  You can run this as a general pool of space across connections.  Brian: do you have enough information to know its not garbage?

Ekr and Martin say that no, only the version information is not gibberish.

Brian:  unless you have other ways of detecting and rejecting backscatter, this is your backscatter data.

MartinD you could have a source address token.

Ekr that would have to be in a cleartext section, which doesn’t currently exist.  Ian notes that this would likely work, but it wouldn’t really be worth it in the common case.

Brian:  I’m just trying to avoid the background radiation of UDP garbage from using up this space.

Ian/Jana: it’s totally okay for this pool to be small.

MartinD: do we want consensus call on this approach

Jana: maybe not yet, until we have the 3 bits phase of the discussion.

Shift to the TLS issues after Jana’s question, which sparks a discussion why we don't need AEAD data that includes the header.  Every time we add a flag bit, we will have to redo the analysis of whats in the public header.

Ian notes that if we have an extended discussion of the public header, then that may inform this.

Putting everything under AEAD would be simpler from a hardware crypto perspective (martinD).

Brian:  don’t see the value of being picky.

Jana:  if there is anything within this that we do want to authenticate, if so we should do everything.  Discussion about whether we should put everything under AEAD now, on the theory that later use is better protected  with that.

Jim points out that the unused flag bit might be better protected now if the AEAD covered it.  Before finalizing this, we’ll have the header format discussion.

## TLS Issues

### [Issue 167](https://github.com/quicwg/base-drafts/issues/167)

This was originally used for eliminating corrupted traffic.

Ekr:  Three things are being detected here: quic/not quic; directionality; corruption detection.  QUIC/QUIS handles both of the first two.  Doesn’t believe that the final use case is worth this, as it is used only for random corruption before encryption is started.  Better to detect via UDP checksum and/or ClientHello failure.  This is also substantially slower to evaluate than magic pattern (QUIC/QUIS).

Brian:  there is a second thing here, distinguishing between random garbage and garbage spewed at the server to get it to do work.  This is useful for that in one way, but it is also a computational work attack vector.

MartinD:  if we are counting on UDP checksum to verify integrity, that many of our issues are resolved.  Implication is that we should have a MUST for UDP checksum.

Igor: most UDP checksum is now done by hardware, so it is not expensive.

Lars: is there a way to check this?  Yes, but it is terribly annoying.  In general, this is hard for the app to tell.

Patrick:  this may be a requirement only on the ClientHello.  Ted:  socket option to set it doesn’t really let you turn it only partially.

Jana:  there is real corruption and having a check for it is useful.

Igor:  generally this is checked if present, so making the client do it, it will usually get checked.

Lars:  the problem is that it is generally a system wide setting to check this, and we don’t really want to require a system setting changes.

Mark: this work will move the needle, so that may not be an issue.

Mark: what’s the worst case scenario?

MartinD:  if you get unlucky corruption, you get a ClientHello failure, then it fails, you have an expensive restart.  The insurance policy here avoid that, but at the cost of computational expense in checking the hash.

Jim:  the original crypto hash is too expensive to check, but that a cheaper hash to guard against DDoS and bugs on the network was worth it.

Igor:  if you do the hash, you can generate this once and use it many times.  So low impact on a client but higher on the server.

Igor:  for a server to remember bad connection ID is a different vector.  The client can generate trash without actually having a valid hash.

EKR:  if the only cost to adding a checksum here is computational complexity, we can pick a low-cost, fast hash function and use that.    Sean: we can do this at line card rates; would it be simpler to say that we encrypt derived from something that can be derived from randomized packet number or something similar?  We could fix the key (AEAD encrypt using a fixed key).

Lucas: that would make it much harder for middle boxes to ossify.  Middleboxes could also derive it, so this doesn’t actually buy much.

Marked as ready for editorial action, with decision on hash function to follow.

Next up:  confirm consensus issues

### [Issue 97](https://github.com/quicwg/base-drafts/issues/97)

Mike reviews this; Martin says that the pull request we discussed yesterday reads on this.  The version negotiation has integrity protection on the handshake.

Ekr:  flow chart.  Do version negotiation, then do ALPN token processing.  There are cases where you get an ALPN token you wouldn’t do with that version, so you have to rewind to version negotiation.

Martin:  this is a case where you narrow from version negotiation to show only ALPNs that you would do with that negotiated version.  If there is none acceptable in that, the connection terminates.

Martin: theoretically, if you hadn’t done version negotiation, you could use ALPN tags to make decisions on this, but that is more fragile than this.

Marked editor ready, consensus will be assessed on the PR.

### [Issue 87](https://github.com/quicwg/base-drafts/issues/87)

Deferred to HTTP discussion.

### [Issue 12](https://github.com/quicwg/base-drafts/issues/12)

Same issue as #97, so closed as a dupe.

Martin:  currently the TLS document talks about TLS and what the transport provides to allow that to happen.  That should go into the transport document, so it will be moved into the transport document and the transport document will say “it’s the crypto’s responsibility to hand you the following keys” and then the TLS document will document how to generate them.

Ekr:  this means that QUIC will always use the same packet protection functions, no matter what the crypto.  The implication is that padding function has to be sorted, since it is both part of QUIC and part of TLS.  Which ones pads?  Is it a crypto function or a transport function?  If we want to use this structure, then this function should move into packet protection functions in the QUIC transport.

Jana: this makes sense to make.

Marten:  if we want to use this to defeat traffic analysis, you’d need a mechanism to call the function.  (Mirja asks whether you currently pad the cleartext before handing to TLS, or it pads after encryption; in current system, you send cleartext and say what length you want it pad it to).  Shifting this to packet protection means you would pad cleartext and send that to TLS, which encryption layer uses to create ciphertext.

Lars: we are always padding it before the encryption layer?

Ekr:  I thought we’d agreed that the rules for taking an unencrypted packet and send it to the encryption layer were going to live in QUIC transport.  (Folks agree).

Ekr believes that the function that creates the packet buffer to send it to the encryption layer should handle the padding.  Note that: inter-frame padding is orthogonal.

Action item:  ekr will raise an issue and make a proposal.

Closing the TLS discussion, moving to HTTP.


## HTTP Overview

[Mike’s slides](https://github.com/quicwg/wg-materials/blob/master/interim-17-01/HTTP.pdf)

Reviewing the change in stream structure between 00 and 01.  3-connection control, request occupies two streams, message header control stream and unframed data stream.  No muxing in HTTP-layer framing, but there are still frame inside of frames; Martin’s point about needing terminology change to make this clearer.

HPACK data now has a sequence number, so that they can be consumed in order; no better on head of line blocking than before, but not worse.  Allows us to continue with HPACK while discussions continue.

Moved from alpn “quic” to hq-xx convention imported from h2 convention.
Changed Alt-SVC “v” parameter.  X+hex, c+ 4 char token; multiple v= options instead of v=value,value,value; Mike thinks that’s a bit ugly, but it’s a point for HTTPBIS to consider.  Martin: let’s just use a number.

Mike: if we go that way, use the x representation, but drop the leading x.

Martin also suggestions that instead of using v=, we should use quic= (can’t use q= because of q value).

Victor: why not use base64 instead of hex?

Martin: doesn’t save much, and nothing else uses base64.  Optimize for the final version.

Mike has a draft in httpbis that allowed for variable length settings using an extended-settings frame.  Feedback was not to bifurcate settings in h2, but take up in next rev.  This is taking that up.  Currently in the doc, optimized for boolean values.

Martin: the encoding for booleans is a bit odd.

Switching to QPACK, which is a re-ordering resilient hpack.  Creates explicit index, explicit deletes to manage table size. Consequences is that you can have the same key/value pair in the index more than once.

Ian: how do you know, if you re-use indices, that you have the right state of the world.  You cannot re-use and index unless you have an appropriate ACK from the decoder that it has seen all the uses.

Igor:  you said that you can insert the same key value multiple times, do you update the use count?  Yes.   Ack of insert is not required, because the presence of the index value takes that role.

Lucas: isn’t that a bit of a layer violation?  It’s an app-layer ACK, not a transport ack.  Question: what’s the heuristic for when I can count on compression (user-agent string example)?  What is a reasonable strategy, here?  How many of a 20-request flight would have inserts and how many have references?

Buck notes in jabber theat ~1% of flows have head of line blocking on headers.  So insert twice is a useful spitball, but priorities could inform this.   On delete reordering, do we have any limits on the number of uses?  No, probably needs bounding.

Martin suggests a variant of immutable where something that is used more than N times can’t be deleted.  65k uses, but the other possible strategy is that when you use something more than 65k times, you create a new one.

The fatal flaw:  packet loss + no retransmission = references that never arrive (also true for HPACK).  General problem also exists of maintaining shared state in these conditions.

Victor:  if you cancel a stream, you can send the deletes on the a separate stream.

Buck: we may be over-engineering on a header stream, as they generally won’t be reset.  Like stream 3, it would not be reset.

Jana: you reset the body, but not the header streams.

Buck:  but the general case is that you want the paired streams to share fate.

Jana:  this works outside of the 0RTT case.

Buck:  If you have the code that says every time you create a pair of streams you must act on them in concert, this works (e.g. refuse both).

_Going to lunch at 12:05 JST; back from lunch 13:12 JST - Brian Trammell scribing now_

Mark: It’s safe to say there’s general support for QPACK, we’d like to work on it a bit and see some proposals. Do we want to adopt now, or sit on it for a while?

There was discussion about the actual performance impact of QPACK versus HPACK, and the complexity involved. Patrick noted that HPACK on stream 3 shouldn’t have HoL problems that it would on H2/TCP.

Jana: We’re planning to run an experiment to determine how much of this problem is already solved. Current HPACK over a single stream has HoL delays.

Buck: 1% of connections experience HoL, Median delay 150ms, tail is bad, seconds. Strictly a tail effect, but it’s a bad tail. For indexed entries, have a histogram of time of use… less than 10% happen less than 40ms apart. 20% more than one RTT apart. HoL not an issue for those.

Mike: discussing different request patterns, when everything is on a primary origin, frequent headers on that first req. get reused later Vs CDN, where you’ll have more headers in flight at once.

Patrick: Would like to understand performance data a bit better… is everything blocking on HoL, or can some streams make progress? How does the blocking effect perceived latency?

Buck: Anything depending on blocked stream is blocked. Other streams can make progress.

Dragana: How is this measured? All connections, any client, network dependent?

Buck: Measured in session layer of QUIC, percentage of all connections. Can drill down, but high level stat is across connections.

Craig: 1% of all connections might be 15% of a geography or type of network.

Buck: One drilldown I did, I looked at data for India, didn’t look too different.

Ian: Can we reframe data in terms of requests instead of connections?

Jana: Users?

Buck: Between 40% and 60% of users experienced some HoL.

Patrick: I like QPACK, but lots of things can go wrong, it’s a uncoordinated state synchronization problem.

Buck: Most implementations will need H2/TCP and HQ, code can be shared.

Mike: Compressor for Buck’s can be used for H2 as well, but is different from the current HPACK compressor

Ian: I’d like to see Buck’s description written up.

Jana: Don’t have to rush into this, HPACK/QPACK is split out. I think QPACK would be a new document.

Mike: Yep, it’s a separate doc unless it’s just framing around HPACK.

Mark: please open an issue on this. (#228 opened)

## HTTP Issues

### Issue #95 / #202 - CONNECT

Do we want CONNECT (largely from H2) or not?

ekr: We’re carrying a lot around from ‘94, does this need to be carried here?

Martin: When you make the new version of the protocol and don’t do things the old version did, you leave some part of the userbase behind. We didn’t leave this use case behind when we did H2, why would we do it now?

ekr: It was invented for HTTP proxies, to blow and opaque hole through them. We don’t know how to implement this securely, how do you validate the end-entity certificate?

Jana: One use case for a QUIC proxy, one connection to QUIC proxy which multiplexes many TCP connection out to the world. This particular way of using a QUIC proxy is useful. We have a datasaver proxy that does this, only for HTTP at the moment. Really helpful in markets with poor connectivity.

ekr: Are the CONNECT semantics the semantics we want to have here?

Lars: Perhaps mark this feature at risk, see if anyone complains?

Lars: An alternative design would be to app-multiplex over QUIC.

Mark: What harm is there in leaving it in? Maybe we can move on and find an concrete reason to kill it later. Close EKR’s #202, follow up on #95.

### Issue #165 - Resetting Streams

Mike: Proposal: reset only affects sender’s side, REQUEST_RESET requests receiver to reset.

Jana: If you use the NO_ERROR code for reset stream, retransmission still occurs.

Mike: If NO_ERROR on stream reset is special, we need text for that. One nice thing about having REQUEST_RST as a frame is that it maps nicely to an overlying socket action: close for reading, i’m not listening. Mostly thinking of this in terms of reducing special cases.

Mirja: Definitely good to have this be explicit.

Igor: You might not know the (future) byte offset at the point you want to send a stream reset - no error. The resource you’re providing might be coming from somewhere else.

Martin T: Request reset is basically “I’ve already stopped listening”.

Mirja: Should the sender then actually reset after a request?

Mike: yes.

Mark: Is this generally useful, or should we move it to H2?

Ian: Generally useful.

Mike: Allows us to remove app_close states in stream state diagram

Martin: Can we recycle this frame type for partial reliability?

Brian, Mirja, Ted, Ian: No!!!

Ted: PR is no-retransmit, not no-transmit.

Mike: General support for a separate frame type, there’s a PR to review. Martin T and Jana to discuss.

_15m break_


## Transport Issues (resumed)


### [Issue 175](https://github.com/quicwg/base-drafts/issues/175)

This would make streams actually unidirectional, which would simplify the state machine.  Idle-->open-->closed would be the only states in the state machine.  You would then have to do other things to associate stream numbers to HTTP streams (e.g. push streams).

Jana:  what is the problem we’re trying to solve here?  Simplification.  Of?  Everything!

If you do this, there is now a stream correlation problem.  In particular, if you have an increasing stream identifier, the response has to be in-order resulting in requesters skipping ever other stream.  You could still have two streams in request and two streams in response (header/body; header/body presumably).  We’re back to “it’s a tuple, friends” as now the same stream number is used by each participant, but it is now (client, number) for the initiator  (server, number) for the response.

Igor: what happens when the client wants to use 7 and the server wants to send a push and 7 is next?

Martin:  the server is still obligated to use even numbers.

Mike:  I already think of H2 this way, so I don’t think the current system is not that complicated.

Martin:  but it is hard to write down some times.  Other formulation is streams are bidirectional, but each side can be in idle--open--close states.

Marten:  using two streams per get request is only because of connection level flow control.

Mike:  more compelling is the property that  we don’t want to reset header streams, but need some stream we can reset

Jim: two questions.  A useful thing to have would be an example that demonstrates that this is a simplification.  I would also generally prefer standardizing things that we are already know how to do.

Jana:  I generally agree with the points Jim made and would really like to see a use case for simplification.

Lucas one of the main differences that this would allow would allow you to reset in a single direction; previously we were discussing a use case for that.  Discussion of a WebRTC approach that would generate a very large number of streams (one stream per video frame) in one direction, but not necessarily in the other.

Ted asked a question about whether there was a use case in HTTP, or the use cases were in other protocols.

Kazuho noted that this doesn’t really simplify things for H2, due to reordering, having the two state machines move independently means they might get out of sync, and H2 needs to remember that the opposite direction isn’t closed yet.

Martin: net number of states in the system is the same.  Current “half-closed” == one closed, one open.

Ted: One way to recast this point, you’re not creating unidirectional streams if you require them to be paired

Martin: The pairing requirement would be part of the H2 mapping, other apps might not need it.

Mike: One way to recast this: the sender on a stream is the only one who can fin/rst the stream, is the only one that knows the last byte offset.

Lucas: You need a bit to note whether a reset stream is in response to a request or not.

Martin T: There’s an error code for that.

Marten S: There are differences in RTX requirements for these two different frame types.

Mirja: If you don’t have reservations, this change is actually tiny.

Jana: What are we changing? Documentation?

Martin T: yes, and generality

Ted: At the moment we’re moving some of this machinery in order to have the abstraction be unidirectional, and HTTP takes care of making sure these are paired. Any bidirectional application will have to import similar machinery. Are there unidirectional applications that don’t have to do this, then it might be worth it. Otherwise it seems like you’re moving complexity into HTTP it didn’t have for previous transports

Lucas: With unidirectional streams you can build any asymmetric configuration of bidirectionality. E.g. one stream in one direction, two in the other like stdin, stdout, stderr. Silly to model with 2 or 3 bidirectional streams.

Mirja: I’d phrase it the other way around. We already imported this machinery from HTTP.

Ted: Multicast.

Ian: I have two applications. Message-based apps; i.e. QUIC for VPNs, MOSH.

Lars: Can we table this, go have dinner, come back tomorrow.

Jana: My fear here is we don’t have experience with this. I don’t know about the corner cases. I’m worried about this complexity. What’s the motivation to move from the design that works?

Mirja: Can we get a hum?

Ted: At the moment HTTP has a fallback. We presume that’ll be around for a while. If you have a version of the protocol that works with the fallback that needs to be remodeled to work with a unidirectional model of QUIC with this change, that hinders deployment…

Martin: We’re already there.

Mike: This doesn’t make HTTP more complex, it turns into a set of stream assignment rules.

Lars: Let’s close the discussion. Martin and Jana should go talk about this, Martin has enough to understand how much work to put into this, maybe not yet a PR.

### Issue 66: Remove STOP_WAITING

Note discussion happened in #63. Now, STOP_WAITING says no longer send ACKs for packets less than X. If one is willing to track ACKs of ACKs, you know what your peer knows about your acknowledgment state; you only have to store one number to keep this.

Ian: One of the benefits here is that requiring STOP_WAITING causes you to have to invent protection against malicious or poorly implemented peers, it makes sense to get rid of it.

Martin: this also cleans up spurious retransmission detection.

Mirja: Do you ever send STOP_WAITING for something other than the left edge?

Ian: Nope. I’ll write the PR.  Will solve the same time as #63 ack transmission.

### Issues 104 and 114 on Priority and Retransmission Priority

Lucas: Nothing changes on the wire. It’s an implementation optimization question.

Mirja: Is this an interface question?

Jana: If the application expresses priorities, then the implementation should do something with it. This might be an API question.

Lucas: Decisions need to be made about relative priority between retransmission and application priority levels. The situation changes a bit when the transport is low on flow control headroom. Not clear that this needs to be in the document though, probably just implementation detail.

Mark: One of the things we haven’t talked about much is what does it give applications to hang on to. From an HTTP perspective, this is not an optimization.

Lars: If QUIC doesn’t have priorities for streams, you can leave it up to the transport. If it does, then you need to say something about relative priority of transmission and retransmission, and we don’t have an API at all.

Jana: It seems hard to figure out how priority changes with retransmission. How we do this in QUIC now is that retransmissions win: lowest-prio RTX is higher than highest-prio first TX.

Lucas: This has a bad corner case with early loss on a background stream.

Brian: Why not make a recommendation of RTX wins, but leave it up to the application?

Igor: There is a lot of academic work here.

Mirja: If you can easily do it wrong, then write it in the spec.

Martin: Implementation considerations: flow control needs to be considered, RTX can help you out here. We don’t have to spec it out, but point out not to screw it up badly.

Ian: Even in the flow control corner, you eventually fix the problem, even if suboptimal.

Jim: Consider fallback to TCP: also has RTX prio as Jana said. May not be optimal.

Kazuho: easy for existing H2 apps to…

Decision: add advisory text, mark editor-ready.

### Issue 115 Connection migration

We need text that explains that this is possible, and the implications of doing it -- privacy impacts of using the same ID on many paths, routing considerations, consent to sent, how much congestion control state can be migrated, and state rebinding along the path.

Need to clarify whether this applies to client migration as well as server migration?

Lucas: I’d like to keep it symmetric, for WebRTC reasons.

ekr: ICE has to figure out a new path.

Lars: Multipath is symmetric, but doesn’t handle simultaneous migration. That’s a reasonable choice.

Jana: MP is the general case. Migration says you can only use one path at once. Multipath allows simultaneous, but the state is much more difficult to maintain. Pretty much everyone who says they want multipath actually wants migration.

Ted: You have up here reasons for migration that are client-initiated, and some that are not. There’s a very different set of abstractions when you have changes of what may occur without the knowledge of the client. On linkability: if you know you’re going to make a change, you can agree (secretly) beforehand between the peers what the connection identifier is going to be. But if you don’t know you’re going to make a change, you can’t do that.

Mirja: We have to handle both cases.

Igor: Maybe I can change connection ID for no reason, in the general case.

Eric: This is a 2x2 matrix: whether or not you know about the change, and whether or not you still have access to the old connectivity.

Ted: One thing we could say here: we’re willing to do connection migration when initiated by sender.

Lars: One thing we’ve used before: you can agree on a function to generate next connection ID…

Eric: Can you establish a new connection and provide proof that you were the old peer?

ekr: In the unknown path change case, the first packet with the old connection ID causes linkability.

Ian: You need the Connection ID to rebind on UDP, since the timeouts are sometimes ridiculously low.

Jana: We ping on open streams to keep them open. Otherwise, on closed streams the client sends the first packet anyway and the rebinding happens automatically. You want to keep congestion control state, path state, without caching and reopening zero RTT. It comes down to a tradeoff between NAT rebinding and privacy.

Lars: Are there privacy-preserving ways to do this?

Martin: We can rotate connection IDs on a timer that expires over the expected rebinding time.

Ian: If we care at all about debuggability, rotating connection IDs could make this heinously difficult to impossible.

Lucas: Can the client make a choice here? I want mobility, so I include the connection ID?

ekr: There’s been some work on doing better than that. It’d be worth thinking about it a bit more.

Jana: It’s not just about the linkability of connection ID, it’s about the increase in linkability, over the benefit of connection ID.

Ted: We’re talking about what state we want sides to be able to reuse. If the client wants to rely on server state, most of that in H2 is application level as opposed to transport level state. Simply doing 0RTT that state is lost. We might make progress about what state is maintained across connection migration events, that might help us work out where the optimization curve is…

Martin: My understanding is all of the state.

Jana: All the stream buffers are transport state.

Igor: Application state is much, much larger.

[?] / Brian: Linkability isn’t just about connection ID. Packet number as well. Lots of information in the header, lots of old literature about how to track packets across NATs etc. Making connection ID “safe” doesn’t fix the problem.

Jana: If we’re talking about linkability, we’re talking about packet emission. Even if the change doesn’t happen at the server.

Lucas: Let’s add new-connection-ID, it makes privacy and resumption work properly in the case where the sender knows about the pending change.

Igor: You still don’t know in this case, because maybe your route changes after writing the packet down to the kernel but before it makes it into the interface’s output queue.

Lars: Let’s put this in the parking lot and discuss it in Chicago.
