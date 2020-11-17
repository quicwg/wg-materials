# QUIC January 2019 Interim Meeting Minutes

* Chairs: Mark Nottingham, Lars Eggert
* Location: Tokyo, Japan

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Wednesday](#wednesday)
  - [Interop Summary (5 minutes) Lars Eggert](#interop-summary-5-minutes-lars-eggert)
  - [Process change discussion.](#process-change-discussion)
  - [Crypto-Related Issues](#crypto-related-issues)
    - [First issue: #2308](#first-issue-2308)
    - [Second issue: #2214](#second-issue-2214)
    - [Flow control for post-handshake CRYPTO messages #1834](#flow-control-for-post-handshake-crypto-messages-1834)
    - [Third Issue: #2170](#third-issue-2170)
    - [Fourth Issue: #2329](#fourth-issue-2329)
    - [Fifth Issue: #1874](#fifth-issue-1874)
  - [Version Negotiation-related Issues](#version-negotiation-related-issues)
    - [Sixth Issue #1773](#sixth-issue-1773)
    - [Seventh Issue: #1810](#seventh-issue-1810)
  - [Connection ID/Migration](#connection-idmigration)
    - [Discuss Requirement that connection IDs not be correlatable.](#discuss-requirement-that-connection-ids-not-be-correlatable)
    - [Define a safe algorithm for changing CID in response to a change in CID](#define-a-safe-algorithm-for-changing-cid-in-response-to-a-change-in-cid)
    - [Don't change CID on peer CID change](#dont-change-cid-on-peer-cid-change)
    - [Why are we bothering to number CIDs?](#why-are-we-bothering-to-number-cids)
    - [Can Initial/0-RTT CIDs safely be used for routing?](#can-initial0-rtt-cids-safely-be-used-for-routing)
    - [Be more conservative about migration?](#be-more-conservative-about-migration)
    - [Issue 2101 Should retiring all CIDs be an error?](#issue-2101-should-retiring-all-cids-be-an-error)
    - [Issue 2372 PATH_* frame should not be ACK-eliciting](#issue-2372-path_-frame-should-not-be-ack-eliciting)
    - [Issue 1994 endpoints don t know how many connections IDs the peer is willing to store](#issue-1994-endpoints-don-t-know-how-many-connections-ids-the-peer-is-willing-to-store)
    - [Issue 203 connection migration should be indistinguishable from a new connection](#issue-203-connection-migration-should-be-indistinguishable-from-a-new-connection)
    - [Issue 2319 Introduce and error code for loss recovery-related errors](#issue-2319-introduce-and-error-code-for-loss-recovery-related-errors)
    - [Issue 1989](#issue-1989)
    - [Issue 1990 encoding of connection_close reason phrases.](#issue-1990-encoding-of-connection_close-reason-phrases)
    - [Issue 2151: where can you send CONNECTION_CLOSE](#issue-2151-where-can-you-send-connection_close)
    - [Issue 2347](#issue-2347)
    - [Issue 2118 allow PMTU probing of a path suspected of not supporting …..](#issue-2118-allow-pmtu-probing-of-a-path-suspected-of-not-supporting-)
    - [Issue 1638 Dead path timeout](#issue-1638-dead-path-timeout)
    - [Issue 2342 spoofed connection migration as a DoS vector](#issue-2342-spoofed-connection-migration-as-a-dos-vector)
    - [Issue 2348 specify IPv6 flow label for QUIC](#issue-2348-specify-ipv6-flow-label-for-quic)
    - [Issue 1243 ICMP and ICMPv6 PMTUD with asymmetric connections-ids](#issue-1243-icmp-and-icmpv6-pmtud-with-asymmetric-connections-ids)
    - [Issue 279 Public troubleshooting Flags.](#issue-279-public-troubleshooting-flags)
    - [Issue 632 On-Path calculation of loss and congestion](#issue-632-on-path-calculation-of-loss-and-congestion)
    - [Issue 602 End-To-Path close signal](#issue-602-end-to-path-close-signal)
- [Thursday](#thursday)
  - [Misc Issues](#misc-issues)
    - [Issue 2299](#issue-2299)
    - [Issue 2049](#issue-2049)
    - [Issue 2344](#issue-2344)
    - [Issue 2360](#issue-2360)
    - [Issue 219](#issue-219)
    - [Issue 969](#issue-969)
    - [Issue 1482](#issue-1482)
    - [Issue 1993](#issue-1993)
  - [Path Issues](#path-issues)
    - [Issue: #279](#issue-279)
  - [Handshake-Related Issues](#handshake-related-issues)
    - [First Issue: #1951](#first-issue-1951)
    - [Issue: #2267](#issue-2267)
    - [Issue: #2309](#issue-2309)
    - [Issue: #2180](#issue-2180)
    - [Issue: #655](#issue-655)
    - [Issue: 2397](#issue-2397)
  - [HTTP/QPACK Issues](#httpqpack-issues)
    - [Varint the Things](#varint-the-things)
    - [Issue 2275: Varint h3 unidirectional stream types](#issue-2275-varint-h3-unidirectional-stream-types)
    - [Issue 2253: Consider making h3 frame types varint](#issue-2253-consider-making-h3-frame-types-varint)
    - [Issue 2233: Why are setting identifiers not varints?](#issue-2233-why-are-setting-identifiers-not-varints)
  - [Push Issues](#push-issues)
    - [Issue 718: Retain use of SETTINGS_ENABLE_PUSH](#issue-718-retain-use-of-settings_enable_push)
    - [Issue 2232: Should receipt of multiple promises really be an error?](#issue-2232-should-receipt-of-multiple-promises-really-be-an-error)
  - [Extensibility Issues](#extensibility-issues)
    - [Issue 2291: Allow extra data after self-terminating h3 frames](#issue-2291-allow-extra-data-after-self-terminating-h3-frames)
    - [Issue 2229: Can I send non-data frames on CONNECT streams?](#issue-2229-can-i-send-non-data-frames-on-connect-streams)
    - [Issue 2224: Why do control streams need to be typed?](#issue-2224-why-do-control-streams-need-to-be-typed)
  - [HTTP Messaging Issues](#http-messaging-issues)
    - [Issue 2396: HTTP/3 frame encodings are unnecessarily difficult to serialize and parse](#issue-2396-http3-frame-encodings-are-unnecessarily-difficult-to-serialize-and-parse)
    - [Issue 2395: HTTP/3 uses LTV unlike TLS or QUIC transport](#issue-2395-http3-uses-ltv-unlike-tls-or-quic-transport)
    - [Issue 2230: What indicates the end of a message?](#issue-2230-what-indicates-the-end-of-a-message)
    - [Issue 2228: How do I generate an RST?](#issue-2228-how-do-i-generate-an-rst)
    - [Issue 1885:DATA frame encoding is inefficient for long dynamically generated bodies](#issue-1885data-frame-encoding-is-inefficient-for-long-dynamically-generated-bodies)
  - [Relationship to HTTP/TCP Issues](#relationship-to-httptcp-issues)
    - [Issue 2223: When can you coalesce connections](#issue-2223-when-can-you-coalesce-connections)
    - [Issue 371: ALTSVC Frame](#issue-371-altsvc-frame)
    - [Issue 2384: What scheme should be used for HTTP/3?](#issue-2384-what-scheme-should-be-used-for-http3)
    - [Issue 253: HTTP/QUIC without Alt-Svc?](#issue-253-httpquic-without-alt-svc)
  - [HTTP Closing Issues](#http-closing-issues)
    - [Issue 2226: Why do I have to explicitly cancel after GOAWAY?](#issue-2226-why-do-i-have-to-explicitly-cancel-after-goaway)
  - [Planning](#planning)
  - [QPACK Dynamic Table Issues](#qpack-dynamic-table-issues)
    - [Issue 2276: Disallow changes of table size after 0-RTT](#issue-2276-disallow-changes-of-table-size-after-0-rtt)
    - [Issue 2258: Initial maximum table size needs clarification](#issue-2258-initial-maximum-table-size-needs-clarification)
    - [Issue 2363: The initial table capacity is zero](#issue-2363-the-initial-table-capacity-is-zero)
    - [Issue 2100: Avoid creating QPACK codec streams when unnecessary](#issue-2100-avoid-creating-qpack-codec-streams-when-unnecessary)
    - [Issue 1420: encoder stream can deadlock](#issue-1420-encoder-stream-can-deadlock)
  - [QPACK Wrapping Issues](#qpack-wrapping-issues)
    - [Issue 2112: Largest Reference algorithm can produce invalid values](#issue-2112-largest-reference-algorithm-can-produce-invalid-values)
    - [Issue 2371: Assign QPACK error codes?](#issue-2371-assign-qpack-error-codes)
  - [QUICvis - Robin Marx](#quicvis---robin-marx)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Wednesday

Morning Scribe: Ted Hardie
Afternoon Scribe: Alex Gouaillard

### Interop Summary (5 minutes) Lars Eggert

This sheet is the greenest we’ve had since -04, but still slightly concerned that there are some basic stuff that is not yet done.  Not a lot of H3 out there, though it is gaining traction.  Picoquic is now testing NAT rebinding.  If we can focus on test coverage, rather than making further changes to the draft, things are looking “pretty” good.  Martin Duke adjusted the algorithm for the level of “greenness”, so it is now directly proportional to the completion.

Interop planned again for the Prague hackathon.

After this interop is over, we will move to draft -18, -19 might make draft deadline, but not early enough to make an interop target for Prague.  There was also a small off-line QPACK interop, which seemed to go well.

Patrick has a build of Firefox that can show iQUIC, would be nice to be able to show something like that rather than terminal.  By Prague it should be working (Ian Swett speaking for Chrome).

Christian notes that there was some performance testing results shown yesterday; it might be useful for Prague to have some focus on that.  Lars agreed and said that doing it during the interim as well.

Martin Duke asked if we should define a set of tests--just put them on a wiki page, and we can add those to the sheet as well, though it gets a bit busy.

Any other issues for the interop?  Hearing none, moved back to logistics.

Site logistics were reviewed.  Note that the vending machine includes soup!

Reviewing the agenda for the rest of the meeting.  Note that the QUIC issues list approach this time should be driven from the issues list and include all issues.

### Process change discussion.

Core change: declare consensus on the TLS and Transport drafts, modulo the open issues.  That is accompanied by raising the bar for a new issue.  Change the process so each draft from -19 represent consensus.  Invariants has already past this process, essentially; we’ve already raised the bar for that.

Ekr commented that there are currently so many open issues that it is difficult to determine which have consensus, which are contested, etc.  Looking for a better way to manage that.

Mark responded that we are aiming to have a very small set of open design issues, and that they are more clearly described.   Difficult for those reviewing the documents to have a map in their heads of what is still truly open. Will try to note when specific issues are particularly gnarly and need to flag those to the implementers.  (Continued on slide 7, Chair slides).

The onus will shift to those raising a new issue to insure that it is self-describing, atomic, and a meaningful technical issues (no bike shed issues at this point:  style and editorial issues should be very minimal).  The chairs will label issues as “design” if the working group needs to gain consensus on it.

MT notes that he has done a lot triage, and he would like to have a way to manage some aspects of this.  Conclusion that editors can establish that something is editorial; the chairs will identify those not editorial as design.  Those that don’t meet the bar for right now may be parked as v2.

Ekr says the eventual bar that is needed is working group attention vs. has consensus.

Mark notes that for cases where the working group doesn’t even need to pay attention (previously considered, not well described), this is prejudiced toward closing those.

Clarification:  technical defects are clearly in.  The other category, for technical improvements, is more nuanced; there needs to be some interest shown.  Mark notes that the aim here is to give the implementer community some stability.   Marten asks whether when we open a design issue are we trying to go for minimal changes or are all design spaces on the table?  Mark, don’t want to bind our hands to much, so no options are off the table, but still prejudiced to stability where possible.

David asks how this all gets determined--the answer is the usual IETF process (wg consensus, as judged by chairs).  The upshot is that the editors will generally not close design-level issues; they can close editorial ones.  Aiming for a process similar to the end stage of TLS, but not quite there yet.

Mark notes that this isn’t magical, and no one is getting a new powers here; we’re here to get everyone in the same head space, that would allow us to move forward a bit better.

Ekr asks if we need a separate conversation, maybe at the end of the meeting, on how we get feedback from deployments.   Some of those will be simple (adjustment of defaults, changing ambiguous language), but others will be harder to get described and to triage.  Maybe we can have that conversation during our final planning phase for this meeting?

Mark confirms that this approach makes sense to everyone (close or park issues as described above).

Jana asks if the existing “design issues” get this process.  Basic approach is yes, but to grind through them as quickly as possible during this meeting or after.

Next question:  do we have consensus to declare that the  -18 drafts of Transport and TLS, modulo their open design issues, are ready to be in this “raising the bar” phase.

Ekr: if we can agree that there are some issues that are on the agenda to discuss whether they should have been closed or merged, then I’m in favor.

MT notes that those are explicitly on the agenda.

David asks for clarification on what “interim consensus means”

Mark and others explain that this is partly that they accurately reflect the current state of the working group’s understanding and partly that we are now saying that the editorial job has shifted to reflecting wg consensus rather than speculatively updating.

The group then discussed briefly changes that might have occurred without appearing in the change logs, and agreed issues could be raised on that.

We are just getting a sense of the room now, and we will delay the confirmation on the list in order to give time for re-reading -18.  Given that, is this a good step forward?  People say that this is needed in order to make progress.

We cannot sustain the rate of changes in our document and expect to get anything shipped in 2019 or maybe ever.  We are currently on issue 2384; that’s a lot of discussion.  The spreadsheet is a pulsing animation of green fading to white and returning; we really need to progress toward steady green.

The group then turned to discuss what other drafts might be ready or when specific drafts (e.g. recovery) were likely to be ready. By Prague we may be able to get some of the higher layer ones stable, but the current ones that need stability are TLS and Transport.  Target date for call on the list is mid-February.

Christian asked if we should have an online Interop event to validate the -18 consensus.  Will be discussed during the planning session at the end.

Jana and Christian make the point that showing interop would be the strongest indication of consensus.

Martin Duke and Roberto note that getting that done in 2 weeks is unlikely.  Agree that for the mid-February call, only review is required to declare consensus.

Best way forward on drafts where we have not yet declared consensus is to have the WG members exercise appropriate discretion in opening new issues.

The chairs set the stage for the need for the speed in reflecting this (8.5 minutes per issue if we want to do them all!).  Hold on to your opinions if you can, unless you have a real need to weigh in.  State preferences quickly and get to the point.  Hypothetical, devil’s advocate discussions should be very limited.  For each, maybe we should gauge the interest in the issue as quickly as possible at the start.  At the end, there will be someone assigned to drive those kept open to conclusions.

The chairs remind folks of how to manage the mics for remote participation.

Keep in the back of your mind that we may need decisions on some things where there is no reason to pick one over the other--grab the coin and move on, may be the way to.

Agenda bash: quick discussion of what to do about individual drafts?  How do they relate to our timeline?  So far we haven’t been very strict about discussing them in QUIC meetings; basically, we need to establish if any of them are needed for version 1.  The load balancer draft is an example, it may not need to hit the RFC editor queue at the same time but it needs to be fairly quickly after (this conversation will be deferred to the planning discussion on day 2).


### Crypto-Related Issues

#### First issue: #2308

https://github.com/quicwg/base-drafts/issues/2308

Marten filed this as “handling of coalesced packets with decryption errors creates a DoS opportunity.”

WG wants to address this.

Ekr is AEADing a lot slower than doing 70-80 AEADs.

If it is, we are now trading off this new facility off the old path.
Relative to the client’s ability to do public key operations, this is not an interesting attack from a client perspective.  The worst case scenario is an on-path attacker who knows the connection ID.

MT suggest we should shift this from MUST to SHOULD, to allow this to be at discretion?  That might break Kazuho’s currently path mtu approach.  Possible approach is to limit this to just limit coalescence in some way (e.g. to a set number of packets, or by encryption level).  Roberto notes that servers are going to do whatever it needs to do when it is under a DDoS attack; we can close this with this understanding.  Ekr agrees.

Marten wonders why his particular solution is not acceptable?  Why not limit to a single decryption level?  Ekr reviews the proposal and agrees that this is acceptable. Mike agreed that if this is a problem we are going to fix, Marten’s fix is okay.

Martin Seemann will have the token to fix this with a PR.

#### Second issue: #2214
https://github.com/quicwg/base-drafts/issues/2214

Next issue, also from Marten #2214.

MT reviews the synchronization problem.  The fix is to limit the number key updates to one per round trip, but there is disagreement on what mechanism will enforce this.

There are two proposals--Kazuho take a bit to indicate “accept a key update”, otherwise a frame that acknowledges a key update.   Reflecting a key update to the peer is a flavor of one.  A third possibility is using the ACK update.

Christian says there is no reason to make the key update as fast as possible.  Ian agrees with Christian.  MT what’s the proposal concretely.

Victor suggests ask for permission to rotate keys in a frame (DTLS 1.3 style).

Jana asks for a review of Christian’s proposal, and Christian goes through it, stressing that it is a conservative approach.

Roberto:  it seems that we are agreeing that a key update shorter than one per round trip is out of scope?  General agreement.

Kazuho reviews the case of a device coming off and on a network, which would typical cause a key update.

Ekr notes that he agrees with Christian’s general approach (“don’t be stupid”), but it does need some spec language, so you can define what happens when it does occur after testing.

Who cares?  A quick design team: Martin, Ian, Marten, Kazuho, Ekr and Victor.  Include Christian to the best of their ability.

#### Flow control for post-handshake CRYPTO messages #1834

https://github.com/quicwg/base-drafts/issues/1834

Raised by Victor, asking for a way to bound the buffer.

Ekr asks why the server can’t just through those packets away?  Because you have to throw away whole packets, which may have other data.

EKR agrees with Marten that this can happen, but because it happens before the CFIN.  (Note that this is not related to the EPOCH boundary, despite the current write-up).

Robert asks what the proposal is.

Subodh asks why this is different from previous discussion on initial data.

MT notes that there is a time bound there, and that the limitation is that abuse results in a handshake failure.  Also, here there is no limit created by TLS.

Subodh notes that the session tickets will process them immediately, and

Marten re-reviews what happens when the first byte is missing and why that creates buffering.

Kazuho suggested we just pick a buffer bound and stick in the spec, and ekr agrees (e.g. 50kb of buffer).   Note that the state machine for acknowledgement generally doesn’t affect anything else, and this would be a departure from that.

Ian, three options: nothing in the spec, there will be random closures; we can state a limit and the closure will not be round; go with flow control.

Nick suggests closing the CRYPTO stream if there is abuse of this.

Ekr says this is like you are doing TLS on a different connection.

MT also likes that suggestion, and it is only used for session tickets.  Recipient keeps a fixed buffer of some size, after the buffer over-flows, it just discards; that means eventually the mis-behaving the client will drop the TLS connection.  This is consonant with the fact that TLS requires in TLS acknowledgement for things that require post-handshake authorization.

Discussion of whether the transport acknowledgements of the post-drop packets is confusing

Is the the same as being permissive of broken implementations.  If so that seems bad.  Fixed sized buffer would be better then.  Fixed sized buffer problem is what is the sender’s view of the buffer- there is none.  What stops the sender from sending a ton.

MT - still likes the idea of tweaking say you must accept at least this must.  If buffers are overrun then drop packets and kill connection.

Subodh - can we just ACK the overflowing buffer.  Ian do not want to implement that.

Kazuho - If the buffer overflows then the client must terminate connection - can we make it a should.

MT - I would allow all: ignore and kill.  Duke - this is just about NSTs so can we just have one in flight.

Ekr - no that would collide the stream and ack processing.  Duke - If I can just refuse data from TLS if stuff in flight ...

Chairs: so where are we at?

MT: I am writing up this proposal and I’ll take to the token to drive this to conclusion.

Short break, followed by quick introductions.  Everyone marvels at the vending machines!



#### Third Issue: #2170

https://github.com/quicwg/base-drafts/issues/2170

Goes through the issue, showing the protocol expansion; base question do we match TLS approach or just use quic quicv2, etc.  Matter of taste.  Martin and ekr will work it out between.

#### Fourth Issue: #2329

https://github.com/quicwg/base-drafts/issues/2329

Actions to take when Reserved Bits are not Zero.  Issue is that 3 out of 4 garbage packets result in the connection being torn down.  If we are sticking with the current approach, needs a clarification; if we change, need text.

MT prefers option 1, and that’s why it is in the draft.  We have a responsibility to do something about timing side channels. (e.g. CBC padding exploit when they were permitted to be any value).  2 bits is not a lot of leverage, but formally option 1 is the right choice.

Roberto , David.  Implementations may do something other than this, but the correct guideline in the spec is useful; 1 is the right choice in the spec, but implementations might vary.

Ekr reviews the current state of header protection for this and notes that this means the CBC padding exploit may not be salient here.  Because of header protection, you know that these are the bits the sender intended, they just are wrong.  That means “Must Be Zero, but ignore” leaves this in a reasonable state, even if it is technically a protocol violation.

MT the philosophy I was applying, was “if someone deviates from the spec, kill the connection.”

David strongly prefer MBZ, must ignore.  If you receive some protocol violations kill this connection makes sense, but for  this it is a no-op.

Roberto  if you have specified something you should mean it, and you should kill it to promote interoperability.

Marten was that there was fear it could be used to signal to a middlebox without negotiations.

Ekr disagrees that this a reasonable concern.

Jana agrees with Roberto, though possibly with a less visceral response.
Wants to shutdown the extensibility argument.

Mark:  this seems to be converging on leaving as is?  (ekr asks whether we are defining what the protocol violation result should be?

MT responds when detected, departure from the spec is a protocol violation and shuts down the connection)  A brief digression into nihilism about RC 2119 results.

Consensus for option one, but refreshing the issue to assign an editorial PR task to Martin Duke.

#### Fifth Issue: #1874

https://github.com/quicwg/base-drafts/issues/1874

Formal analysis of the protocol would be nice.  It would be, but this is a not assignment for the WG, but something like a wiki page of what needs to be verified.  So wg members will facilitate, but nothing will gate on it.

### Version Negotiation-related Issues

#### Sixth Issue #1773

https://github.com/quicwg/base-drafts/issues/1773

Desire a version negotiation method that limits additional round trips.  Current method requires burning a roundtrip to get to version n+1.

David and ekr have discussed and one option is to remove version negotiation, making the VN packet in the invariants a stub.  VN method can be used without downgrade protection, but the real method is coming in v2.  Discussion of what the greasing story would be here; it’s similar, but the client always reconnects on v1.

Marten reminds folks that we gave 32 bits to VN, so we could have a lot of experimentation, and that if we are not allowing VN until v2, we should claw them back.

Jana asks what we should do with experiments, which was partially answered.  Roberto notes that we should have the attitude that v2 will be quick.  He also wants to be sure that the middleboxes cannot drop version 2, to force them to stick v1.

MT believes that middleboxes will be able to do it.  So, to make v2 have version negotiation, you’d have to use a transport parameter to add it back to v1.

Eric asks if we are really doing something that has a lower cost in RTTs; it’s worth doing something now.  The one RTT cost is bad enough to avoid it.

Ted asks whether the re-introduction of VN in a transport parameter will again cost an RTT (answer “maybe”  it could, or if the V2 VN version negotiation is based on EKRs, then it might not).

Marten says basically if we have a 0RTT VN design we should do it now, is it clear that this available?

Ekr goes through the theory behind his period, which flips the design to be limited to a compatible version negotiation, rather than a big enough change to be incompatible.  If you need an incompatible change, you need a new port or a new scheme, etc. Remember that the server can offer supported versions in its transport parameters.

Roberto:  returns to the question of experiments, and reminds folks that burning an extra RTT allows you to force experiments even if you control only one endpoint.

Kazuho doesn’t like adding RTT to experiments.  Also concerned about the ability to change the initial packet.

Ekr reviews the options is:  nothing, kick the can down the road, do it now.  Christian has a lot sympathy for what Martin is saying; you have to pay a penalty to negotiate update.  We have to deal with up and down and sideways.

Subodh, there are other ways to discover v2 is usable. Ted notes that incompatible change may still be needed, and that the fallback (new port, new scheme) is a very high pain to pay.  It may be useful to have the discussion of whether incompatible change is important to us, because they may tell us whether to kick the can down the road.

MT notes that there are some possibilities in the PR that forces a RTT when there is an incompatible changes.  Note that this has to be a v1 extension at any point that this gets reintroduced.  Convergence appears to be for kicking the can down a short road, with a rapid v2, but Marten notes that we have had that theory for a bunch of other changes (see multipath etc.), and that getting them all in could be useful.

Martin Duke asks if we can keep the current Transport draft and then have a new document on the side?

Martin notes that the other server upgrade discussion in BKK came to a different conclusion for that upgrade question.  Jana notes this applies to other protocols than HTTP.

Roberto none of this negotiation matters until we have v1.

Proposal is that David’s PR is the basis.  A small design team on the other approach is ekr, David, Ted, Marten Kazuho, MT,

#### Seventh Issue: #1810

https://github.com/quicwg/base-drafts/issues/1810

Is this OBE?  Yes, MT will record.

### Connection ID/Migration

#### Discuss Requirement that connection IDs not be correlatable.

https://github.com/quicwg/base-drafts/issues/2084

Half editorial;half other.  This rules out a number of designs for connection IDs, e.g. consistent hashing for first packet (so that you get them in the same bucket every time).  That may be fine, but is it what we want?

MT whether it would be sufficient to list a couple of options and describe their properties?  This isn’t observable, so it is very hard to penalize bad connection ID generation.

Roberto; we’re all in agreement that MUST NOT is not observable and so might need to be downgrade--not agreed.

Ian if the connection ID is no more correlatable than the destination IP, then there is no issue here--MT, but anything we do must be strictly worse than this.

Ekr notes doesn’t know what we are trying to achieve.

Christian suggests we describe the attack in the security section, and give a forward pointer to that description, so that implementers know what the risks are.

Jana agrees with Christian.

Assigned to editors to describe the attack.  That may include removing the RFC 2119 language.

#### Define a safe algorithm for changing CID in response to a change in CID

https://github.com/quicwg/base-drafts/issues/1795

Duplicate, moving to the next one to discuss.

#### Don't change CID on peer CID change

https://github.com/quicwg/base-drafts/issues/2145

Is there a way to force the peer to change their connection ID?

MT notes that the current one is change the port. Essentially, this is change per path, and a port change is considered a path change.  Since the real reason for this is avoiding linkability, we shouldn’t use it just because we have a mechanism.

Eric and Kazuho discuss whether there is a big loss in losing the ability to run multiple connections on a single 5-tuple using different connection IDs and rotate both CIDs at the same time.

Eric agrees that this could be valuable, but probably something we can lose, Kazuho points out you can change ports and force such a change.  This means that the connection ID doesn’t change on the other side change, but do change on the path change.

MT has a PR that does just this.  We can then move on to the other question.

#### Why are we bothering to number CIDs?

https://github.com/quicwg/base-drafts/issues/2159

Would prefer timers.  No one is with ekr on this, so this is dropped.

#### Can Initial/0-RTT CIDs safely be used for routing?

https://github.com/quicwg/base-drafts/issues/2026

Trying to avoid having someone be able to attack a single server.  Note that there are some designs that don’t allow this to be targeted, but they are sticky, and Ian notes that’s Google’s design.  This was shifted to editorial.

#### Be more conservative about migration?

https://github.com/quicwg/base-drafts/issues/2143

In this case the attacker causes data to go to the wrong address; the current defense is to probe both paths when you see migration, and not migrating if the old path responds.

Eric--this is explicitly an on path attacker, and this is the case in which path validation will eventually fail.  During the time it takes to prove that the attacker isn’t the real endpoint (the path validation timeout), the wrong path is used.

Roberto notes that multipath TCP had a similar issue, which allowed an attacker to force the use of a path that had a more capable of adversary.  There are two options to fix this; signal intent or don’t send packets until you get confirmation on the new path.  Spamming both paths during this period might be a mitigation here.

But ekr wants to see a strong description of the security properties required.  NAT can be a attacker in this scenario.  Probing both paths may be required here because of the NAT rebinding.  1 RTO not 3 RTO because of the probing.

David thinks it more important that we work through NATs than coming something that improves against this attack but does not enable NAT traversal.  Close, no action, but EKR will write a description of the principles for the on-path attacker defense we intend.

Roberto points out that what we have now isn’t as good as TCP, but TCP also doesn’t survive NAT rebinding, so this may be a base-level tradeoff.

Martin believes that the section 9 should shift from SHOULD to MUST.

Robert describes why the current mechanism is worse.  One way to bring in the new mechanism would be to insist on probes but exempt something like port (since the common NAT case will be thus covered).

Christian notes that on-path attackers who can affect the route (e.g. routers, not observers) are already capable of taking over anything.

(Lunch break)
new scribe - Dr Alex G. (CoSMo)

eric@apple - strict(er) proposal: do not consider port and address separately. If any change, you MUST re-validate.

Kazuho - We might want endpoint to send several path_challenge.

Jana: we should not differentiate IP and port: …


Martin D: fine with that
Even if we were to send data before validation finishes, we would still wait for validation to happen.
Christian: the IP address is not protected by either encryption or authentication. Because of that, we resort to heuristics. I think that what we have today is good. We could do something about ipv6 (since it s then less likely to have a NAT and then it would have some interesting properties).

Eric: requiring validation before going to the new path remove the heuristic about believing people can […] you or not. It’s now deterministic in that regard. Agreed, there are still some heuristic left.

Martin (moz): what’s the cost then?

Christian: the connection slows down. I do not believe you can have an attack whithout effect. In the case of a NAt rebinding we also slow down anyway.

…….: MUST might be too strong

Martin: could you structure it as a MUST … UNLESS?
Port number only change?

…@fastly: how much a problem is it?

ted@goog: ipv6: tcp bindings and udp bindings in NAt are different, and ipv6 changes are a strong signal. However, I’m not sure i understand what we want to optimize. We want to protect ourselves to a reasonable degree, but that “reasonable” seems to be all over the place. Especially NAT rebinding happen very often, while the attacks require such a sophistication that their frequencies should be very low in contrast.

Ekr: there is a cost / benefit analysis to be made. Is there a reason not to be super conservative now, and then relax later? We run that for a while, and once we have data, we can discuss relaxing the rules.

eric@apple: being stricter makes sense.

Roberto: to remind everybody about attacks: timing attack, amplification attack. IoT means attacks from behind your NAT are very possible. Let’s not assume unless we do know.

Kazuho: discussion about which path should be used in transition. Right now you should not send before a certain window (two packets). We have the path_validation with a SHOULD, i’m advocating making it a MUST.

Ted: answering ekr with respect to cost. The cost is one RTT over and over again for all those not rebinding. I acknowledge the problems of IoT. I m still not convinced that IoT is greatly improving the risk of behind-NAT attacks. Advocating “MUST validate”.

Ian: discussion about the two packets, and the risk of one to be dropped.
Martin (@moz): research question: do we have numbers? We have time, we can keep the issue open, time to get more data, to be more confident in our decision then.

…: Reformulating the question: Which path should be use, in which circumstances, in response to an apparent path change.
Keep sending on the old path
Validate the new path
If you detect it s a network rebinding, send two packets on the new path
Remove distinction between Ip and port change

Roberto: Second R&D question: if it is an attack packet, how bad are they,

eric@apple: we need data. There is definitely additional complexity, I’d like to have a feeling of the frequency of it happening.

Ekr: we could also provide hints and guide for people who want to deal with it by pointing them at the possible risks and mitigation vectors.

AI: martin (@moz) to follow-up

#### Issue 2101 Should retiring all CIDs be an error?

dmitri:I m not sure what to do in that case?

Ekr: this is an easily detectable error.

roberto(?): you re likely to want to close it.

Ian: is there a reason why we cannot make it a connection error?

Martin: you can deal with all, but the question is: do we mandate it?

Mark: is it really worth face to face time discussion?

Ekr: yeah, it s an edge case.

Mark: can we deal with it simply?

Martin (@moz): i can take the PR if someone goes ahead and write a PR that states that one should not do it.

Ian: MUST not do it, may generate error. (retry on the next path)

Dmitri: yes, it s good, as long as a decision is made, and we have a reference.

Mark: done.

#### Issue 2372 PATH_* frame should not be ACK-eliciting

Rui: at least two implementations assume that PATH_RESPONSE is the acknowledgement

Martin duke: do you need a separate timer then?

All: we already do.

Ekr: by default, things are ack’ed. Let’s define the criteria for not ack’ing and check that those messages meet the criteria.

Rui:

Ian:  Making them ack-eliciting has certain impacts on the congestion controller.  We perhaps don’t want those impacts, and some of them are hard to reason about.

*scribe lost*

Ekr: when you’re asking path validation, you send the challenge on the old path but might get

Christian: you don’t want to repeat the path_challenge on the main path because you lost it.

Roberto: you need to make sure everything is accounted for as far as it comes to congestion control. If it takes ACK’ing to get the congestion control right, so be it.

Jana: there is an assumption that the path_response comes on the same (old) path as the path_challenge. ACK can cause confusion…

Ekr: if the path frames are bundled with other frames, then there will be acks regardless. Either one path is valid, or both are.
If i understand Jana’s point correctly,

Roberto: is it good enough the way it is?

Ian: close with no action, re-open if new data.

Mark: ACK

Mike: the draft is not clear, and we should state one way or the other.

Martin @moz: i disagree, the draft is real clear on those cases.

Jana: i feel that there will be issues, and it will need to be addressed.

Igor: i’m confused about the old path, since in case of migration, when you have a new path, you don’t have an old path.

All: agreed.

Mark: I think it’s closed, and we reserve the right to reopen with new info.

???: we need implementation experience.

#### Issue 1994 endpoints don t know how many connections IDs the peer is willing to store

Marten: problem: there might be some implementation which keep connection ID for the entire lifetime of the connection. We could exhaust the connection ID space. It would be nice to manage a maximum number of IDs. a PR is ready.

Mark: call for the room.  A few strongly for, more mildly for, some mildly opposed, no one strongly opposed

Martin @moz: it is a fixed number.

Christian: there are other resources that could become eligible for such magic number e.g. token. I’d be in favor or keeping the spec as-is.

Ian: it’s not flow control. I believe it’s trivial. I’m in favor of it , because it’s trivial, and the number proposed for the max is way above what i need which is 2.

Ekr: i’m slightly against. I find the semantics are not clear.

K : if it’s not an error to go beyond the max (i.e. if the number is advisory), then i don’t see any reason against.

Eric, ian, …

Ekr: I think that it not being an error is a problem. You can be stuck at the limit.

Roberto: is it good enough the way it is? Do we have to figure this out today?

Mark: we don’t seem to be in agreement.

Roberto: can we break the tie.

All: doesn’t look like it.

Roberto: then let’s not speak about it.

Compromise on merging the new TP, but only as a hint.  No error for violating.

#### Issue 203 connection migration should be indistinguishable from a new connection

This is old and nearly impossible.  Close; we can choose this as a design goal when we eventually do multi-path.



#### Issue 2319 Introduce and error code for loss recovery-related errors

Christian: having an error for this should be in the main spec, and not in the loss recovery. Then it makes a lot of sense, it’s a protocol violation.

Mark: is it an issue people have strong feelings about? Is it going to be onerous or dangerous for us?

Ekr: typically the reason for having a separate new error code, it’s because the client will act on it.

Roberto: i would love to hear from implementor especially, whether or not it would be too hard, or easy to do, and everybody will understand the protocol violation meaning the connection will go bye-bye.

Martin: The error code is in CONNECTION_CLOSE -- the connection is going bye-bye anyway.

K: it seems straightforward. In practice we could use either the error code or the packet in this case, my preference would go for not adding a new error code.

Marten: we had already a discussion about error codes. We removed several. We said we would later re-introduce new error codes.

david@goog: do we care?

Christian: i kind of care because I don’t want to give more information in that specific case. The ACK’ing could be feeding an attack.

Mark: would you be more comfortable with not being required to generate it?
Several people shaking their head “no”.

Martin @ moz: there is only one behavior possible in that case: connection goes bye-bye, so adding more info through an error code is not going to help the application. It does not bring value.

Roberto: we have errors code to help people fix problems, or help answer directly. Identify three buckets: happen often enough that we need an error, some cases that might or might not benefit from an error message. And the standard.

Mark call for the room. Decide then to close it. Martin (@moz) to wrap this.

#### Issue 1989

K: I like this issue. It’s useful for other issues.
Is frame type really useful?

Ian: i agree with marten, it’s kind of useless and annoying.

Mark: are we going to be able to make real progress here, or are we wasting precious f2f time.

Ekr: is anybody really standing up to keep this field?

Mark: can we close this issue with no action.

Consensus to close with no action.

#### Issue 1990 encoding of connection_close reason phrases.

Lars: for the protocol there is nothing to:

Mark: textual (not blob), utf-8, not language tagged.

Consensus. Issue to be closed.

#### Issue 2151: where can you send CONNECTION_CLOSE

Martin T.: Looking for agreement on principal:
* Send the highest level of encryption available?
* Send the highest level of encryption your peer can read?

Martin D: 1786 discussion lead to that.

K: Sometimes you are not aware of the highest level available, either locally or from your peers. E.g. if you’re dropping the handshake keys, but you don’t know the server has 1-RTT keys yet.

david@goog: propose the highest when you know, and treat the rest separately. I believe they are separate issues.

Roberto: we don’t want random elements to react.

Jana: we want the right peer to be able to read it though.

Roberto: how large is a connection frame? Is the size unique? If it was unique in size, and always the same size, one attacker could infer the packet type.

Martin D: this is a rehash of an issue we already closed so ………

Ekr: I’m happy to rewrite.

Martin D: i write this is editorial in nature and assigned to ekr.


#### Issue 2347

K: currently the server must not send any packets during the closing period.  In the closing period after an idle timeout, you can’t tell the client the connection has closed (Stateless Reset) if a packet arrives at the wrong moment.

Martin: when you reset, there is a window of time during which you are not supposed to answer to any packets. In the case described in this issue, i believe a stateless reset is better in that case.

Roberto: we all agree that the server not being able to answer is kind of silly.

Ekr: in favor of taking the PR.

Christian: yes, the PR seems to do exactly what you just spoke about.

Mark: is that good enough for everyone.

Consensus. No objection.

#### Issue 2118 allow PMTU probing of a path suspected of not supporting …..

Igor: instead of ceasing all packets if the PMTU reported is below 1280, we propose to keep the ability to probe. PR proposed in #2108.

Already fixed.

#### Issue 1638 Dead path timeout

When (after how long) do we decide a path is dead?

Martin T.: the idea is sound, but we do kind of meed more concrete proposal. When does the timer start? …. Be specific.

Jana: TCP standard has a mechanism for that. We should just reuse this. We just then need to choose multiples of (consecutive) RTOs.

Christian: when moving from wifi to 3G the delays can be very different.

Jana: I was just separating the concept of dead path and the concept of dead connection.

Christian: it looks like this is an implementation detail, not a standard feature.

Jana: this is definitely a local implementation issue, but this is one that all implementation will have, so we could have advisory rules in the standard.

Roberto: it does not seems to be part of the protocol per say, since it does not interoperate. We should pu tit in another spec, e.g. “best practice” ?

Mark: can we write down what we just say, and keep it for later.

Ian: I’d like to see something about that in “transport”

Mark: everybody ok with that?

Martin: I have a little bit of text.

Mark: I think we can move on then.

#### Issue 2342 spoofed connection migration as a DoS vector

Igor: describe a simple man-on-the-side attack.

Mike: if migration, disable packet from …. Address.

Igor: that’s one way.

Ian: is it significantly worse than taking a packet send it to another server to generate a stateless reset, and then send it back to you?

Martin:there is text in the spec to treat that case.

Ekr: mike suggestion seems to be the right one.

Igor: disable migration for another reason, but ok with net rebinding.

Roberto: are we sure we can distinguish between what we are trying to distinguish?

Igor: boils don’t to : do something, but don’t close the connection.

Kazuho: migration is disabled, …

Ian: is it going to the same point? Client should not make migration.

Martin D: i m confused about the difference between net rebinding and migration.

Ekr: trying to understand what we are trying to achieve.

Jana: ..

Martin T: we require everybody who does migration to go through the full machinery of path validation. If you have disable_migration ON, you still need to do path validation, or at least attempt to.

Martin D: in what condition should I set disable_migration?
E.g.: when you have an UDP-only load balancer.

Kazuho: i suggest changing the name to discourage_migration.

igor : what about a 0-rtt client?

Kazuho: disable_migration is confusing. Disable_explicit_migration might be better?

Roberto: what’s the point here if the client is still doing NAT rebinding.

eric@apple: reason for sending disable_migration were: my infra can’t, or I don’t want to. It looks
]s

Mark: this issue i straightforward, but there is a problem about semantics.

Martin T: the text is not bad. We should all read it again.

Roberto: you cannot drop all the packets, you need to do a path change.

Ian:

Ekr:

Mike: we could move to a totally different ip address, it s almost guarantee to be a different server, don t try. If it s the same ip and port, no problem.

Martin D: you can get a stateless reset.

All: no you can’t

Mike: if there is a rebing that happen to get back to the good server, what should be the server behavior?

K: small set of server. E.g. …. 1 server.

Eric@apple: server should give a good faith effort. “You should not do it, but if you do and it work, so be it”.

Roberto: I cannot think of a strategy that I would implement and be a good strategy. I could induce long answer time, longer than usual. Is there another trusted domain I could use?

Jana: you should get a stateless reset.

Mike: explains how to abuse that.

Martin: that’s why we require validating the routing.

David@goog: if the server gets the packet from somewhere, it must try its best to make it work.

Roberto: i’m at the point where i do not believe we will be able to reach a consensus here and now. We should take it to the list.

Mark: we have a proposal to delete a sentence today, and bring the bigger question on the list.

Consensus on that decision.

#### Issue 2348 specify IPv6 flow label for QUIC

Christian: should we push for conformance with RFC 6437. I.E. adding the requirement that if we are doing IPv6 adding a label for that connection.

david@goog: I’m ok with SHOULD, i m opposed to MUST.

Roberto: are we trying to avoid compatibility?

Martin T: read the issue.

Mark: it seems that we have enough people to support it. At least for a SHOULD.

#### Issue 1243 ICMP and ICMPv6 PMTUD with asymmetric connections-ids

Igor: we need a way to do MTU probing so that the ICMPv6 we get back is good. The method that K proposed works.

Mike: the proposed method is not written anywhere in the document.

Igor: I can write the PR.

MArtin T: done!

#### Issue 279 Public troubleshooting Flags.

Martin D: flag for V2

#### Issue 632 On-Path calculation of loss and congestion

Martin D: i suggest to push it to V2, as it’s clearly not happening in V1.

Lars:  That will be a different issue; close.

#### Issue 602 End-To-Path close signal

Martin D.: some discussions about CONNECTION_CLOSE being an endpoint only feature.

Mike: we said this morning that it was a non-goal.

Martin T: agreed, but if we speak about closing the path it’s different.

Roberto: we did not want the path be able to observe that we are closing the path to avoid OSSification.

Mark: martin, do you really want an unspoofable thing.

Martin D: i won’t die on the sword for that in the scope of V1. The incentive is to encourage boxes vendors not to time out NAT bindings so quickly.

Roberto: there are better things to do than this.

Mark: who would ready to make a proposal?

Jana: I’m ready to detail the goals.

Mark: ok.


## Thursday

Morning Scribe: Eric Kinnear


### Misc Issues

#### Issue 2299

https://github.com/quicwg/base-drafts/issues/2299

Marten: Can we just close this with no action?

Mark: Is everyone happy closing this with no further action?

Ekr: This reopens whether or not you should enforce minimum encoding. If nobody cares about enforcing minimum encoding then we can just close

Marten: In spec?

Martin T: Only for frame types right now

Ekr: I’m okay with requiring that people minimally encode. I don’t want to require checking minimum encoding.

Mark: Status quo seems acceptable?

Several people: Yes


#### Issue 2049

https://github.com/quicwg/base-drafts/issues/2049

David: Can’t you put a bit of padding at the start?

Marten: We have a requirement for protection that it’s at least 4 bytes

MT: If you have a short packet number and a short packet there is a case where a DATA frame that goes to the end of the packet can produce a packet that is too short by one byte.

David: So just use one byte of padding

Marten: That’s the case that I ran into, I added a padding byte

Ekr: We could always require one byte all the time.

Christian: If I’m including a stream frame, either it fills packet or it doesn't, if it doesn’t I encode the length

Mark: Do we need to change the spec?

Marten: Maybe editorially?

MT: Make people aware of this very small edge case?

Mark: Can go editorial or you can send PR

Marten: I’m happy with it going editorial

Marten might send PR, otherwise up to editors to close or change

#### Issue 2344

https://github.com/quicwg/base-drafts/issues/2344

MT: We had a PR that does just this, Marten said why not flow control and all these other things. RESET_STREAM is the only that increases the risk, the rest of them we’re fine apart from this.

Kazuho: My argument was about enforcing the stream limit *missed rest*

MT: Argument here is mostly around denial of service, not sure I understand/agree, seemed like part of the risk of taking 0-RTT
Kazuho: You cannot allow all frames for 0-RTT: CRYPTO, ACK, and STREAM frames have different rules. Why allow other frames that are never used in 0-RTT.

Marten: Which frames?

Kazuho: NEW_CONNECTION_ID, for one

Ekr: The way we got here was what’s safe, it may be the case that other things are safe. It’s not entirely clear they’re safe, many of them aren’t useful. We’ve already got rules about other epochs, why would it be simpler to allow
more in 0-RTT.

MT: Reset and stop sending would operate like normal and that makes things simpler

Roberto: Two things. (1) What is the minimum set of stuff in 0-RTT for it to be useful? I think we should do that and only that. (2) If it doesn’t make protocol worse, can we just not do it?

Kazuho: We should allow max stream count, max data, things that flow control. We don’t need to allow other frames like NEW_CONNECTION_ID, etc. there will be frames that don’t need to be sent and it’s a waste of time to analyze security properties of sending them.

Ian: If 0-RTT is sent by the client, and client just sent TPs for flow control windows and such, why do we need flow control messages?
Reset stream makes sense, but rest of them?

Jana: You might want to send initial small values and increase for specific streams.

MT: That’s what Firefox does now

Marten: There are frames that could be useful if you think about it, we used to think about flow control, it makes sense if you’re expecting a large download. New connection id you might want to supply so the server can switch immediately after the handshake.

Kazuho: By time handshake is complete, client should be sending 1-RTT.

Mike: Server will have been sending 1-RTT packets, only after handshake completes on the client can it send 1-RTT packets.

Kazuho: Client can send 1-RTT with client finished, handshake completes when ack of client finished is received.

MT: Let’s discuss handshake part later

MT: My original issue here was about the other frames, I couldn’t see a reason not to do some other frames

Kazuho: Path challenge?

MT: If we can make a decision on path challenge ones, we can draw the line at the stream related ones.

Ekr: Are we going to be able to resolve this today? Could we just keep list or have someone go sort it out?

MT: Path challenge Jana?

Jana: Path that you’re doing handshake on, you’re doing validation there

Mike: That’s an argument for why it’s not useful, not why it’s dangerous

Christian: Flow control is about sending new data, but we want to limit for security reason, I have concerns about allowing people to send more data until we’ve confirmed connection

Jana: We can’t do the analysis in the room for every frame, let’s draw a line in the sand at thing that we know we need. We can always move it as we find new needs, like Firefox’s use of flow control frames. If people need more, let’s do one by one

Mark: Lots of people nodding at that

Mike: Yes you want to limit impact of 0-RTT until client is legit, but no QUIC frames affect anything outside the connection

MT: That’s the analysis that I did

Mike: We don’t have any frames that do that except for data, we should probably specify the same requirement as TLS, but I don’t see why any frame would be harmful. We need to decide if our standard is minimum we need or minimum that is safe

Ekr: Do we agree no CRYPTO?

Mike: Sure

MT: No use for it

Jana: Proposal: Minimum set that we know we need and know are safe, include those now. As implementations progress if there are others, do the analysis separately per frame in the future.

Mark: Applying that principle to that issue, we have a minimal set and this is the issue for reset stream and flow control

MT: Based on that we have several in question: CONNECTION_CLOSE, NEW_CONNECTION_ID, PATH_CHALLENGE, PATH_RESPONSE

Marten: And PING

MT: Those are the five frame types that are out of scope and forbidden
Kazuho: And extensions

MT: If we do this, extensions need to solve this problem for their extension

Mike: Proposal: Prohibit CRYPTO and include others as needed.

Jana: Oh sure

Ian: We’re pretty close to a default allow and prohibit list

Roberto: Allowing server to optionally accept something and having some servers do different behaviors is not great. Let’s do minimal set that we accept and everything else reject. If we want something more do it in v2.

Mark: v1 and HTTP, we’re currently focused on minimal set, let’s make sure we keep that in mind here

Kazuho: 0-RTT packets can be sent at a much higher rate because you can just copy those packets, server cluster cannot reject all the copies because they don’t have a single hashmap for checking if ticket has been reused. For example, if we allow NEW_CONNECTION_ID in 0-RTT packets, a server implementer is required to handle connection IDs arriving at a much higher rate rather than 1-RTT packets where we know the client is legit.

Jana: Clarification, suggesting to *not* allow those?

Kazuho: Yes

MT: I’ve written down proposal

Mark: I’ve heard some pushback on proposal

Christian: I’d like to pushback and mention that this is a different animal, I’d like us to consider effect on replay attacks

Mark: I think that’s the direction we’re going in. Martin, please restate proposal.

Proposal:

MT: Limit to stuff we know we need. Leaves only the five mentioned above (CONNECTION_CLOSE, NEW_CONNECTION_ID, PATH_CHALLENGE, PATH_RESPONSE, PING) out for the moment, do analysis for each one when we know we need it.
Allow STREAM, RESET_STREAM, STOP_SENDING, MAX_DATA, MAX_STREAM_DATA, MAX_STREAM_ID, DATA_BLOCKED, STREAM_DATA_BLOCKED, STREAM_ID_BLOCKED, PADDING.
ACK, CRYPTO, NEW_TOKEN not allowed.

Ian: These are things that are useful, not things we need.

MT: Sure

Mark: What about reset stream

MT: Reset stream is allowed

Jana: People are thinking about this in two ways

Ekr: Seems like we have a set of frames that are permitted and rest forbidden. Is this adding new things that are permitted?

MT: Yes, typing in now.

Marten: The list is really small, there’s obviously no security impact of PING, I already made the case for NEW_CONNECTION_ID, CONNECTION_CLOSE can be useful. Path challenge/response are the only ones left

Ekr: Not obvious to me that PING doesn’t have security considerations

Mark: Let’s rename issue to match larger scope

MT: Will do

Jana: Does allow mean everything else prohibited

MT: Yes everything else prohibited

Ian: Objection. Seems weird to allow half and not other ones. But also don’t  want to keep talking about it.

Ekr: Yeah this seems like no principles at all

MT: PR went with principle of just allow everything

Ekr: Need to go one way or the other (permissive and prove, or restrictive and prove other way)

Christian: Not comfortable with adding unnecessary things like MAX_STREAM_DATA, etc. in 0-RTT

Martin D: All of 0-RTT is not necessary

*multiple talking*

Roberto: For QUIC to succeed, has to be enough better than TCP to be worth the cost. 0-RTT is a huge benefit, getting streams in first packet are absolutely necessary, we might be having slightly different definitions of necessary here. Are we all in agreement that 0-RTT stuff is necessary here?

Mark: I see a whole lot of nodding heads

Ian: I was going to say I would rather prefer that we prohibit ACK, CRYPTO, NEW_TOKEN and leave everything else. Or just don’t do anything and just move on. I think the middle ground is really weird.

MT: I did some analysis and think the new ones in this PR are safe. I know Kazuho disagrees and I disagree with that, but I think we’re going to have to table this.

Martin D: Meaningfully latency reducing is the necessary bar here. I agree with what we’re doing with this set.

Rui: I think PADDING should be allowed as well

MT: It already is, I need to add it to this list

Ekr: What would be awkward if we didn’t take the new ones?

MT: Firefox current behavior opens up flow control immediately.

Ekr: Need to walk me through that.

Jana: I was going to suggest that we can do that, it’s not lack of principle, just a different principle. Seems like people aren’t sure how they all feel about these frames.

Kazuho: I wanted to make point that if you allow more streams then rules about how to handle stream frames are different since FC limits are different. I don’t buy that allowing more frames gives you more consistency.

Martin D: I want to withdraw comment that CONNECTION_CLOSE in initial is not useful, there is a need for it

Eric: Can we split this into principle acceptance separate from taking the new frames?

MT: Can we do this later once people can think about it?

*Coming back to this later*

#### Issue 2360

https://github.com/quicwg/base-drafts/issues/2360

MT: Related to discussion about what can go in 0-RTT. When someone is sending 0-RTT they shouldn’t be reading 1-RTT. If you’re reading 1-RTT you should have sent the rest of the handshake. This suggests that you prohibit increasing flow control, makes it a protocol violation to use those flow control increases.

Ian: How to enforce?

MT: Server can say this is a packet that exceeds what was in TPs

Ian: I can’t implement that

MT: You don’t have to, just require client not to do

Ian: Works for me

Kazuho: Unless we take this we’re relaxing requirements from TLS 1.3

Ian: Could we just say once you send a 1-RTT packet, then no larger can be sent in 0-RTT

Ekr: This is somewhat different, if you’re given a flow control window of 50 bytes for 0-RTT, but 1000 for 1-RTT, you could use that credit in 0-RTT. Say don’t do that, server can enforce or not as it pleases.

Marten: I don’t see how this is equivalent to max early data in TLS

MT: M.e.d. Comes from previous connection

Marten: For performance reasons you may want to set high limits, for security send a smaller value.

Ekr: Client can only get here if already consumed entire server flow including finish, so no reason not to send in 1-RTT.

Jana: If we don’t require server to enforce it, then we’re weakening requirement on client

MT: Ian’s point is good here, it’s difficult for server to enforce, I don’t think we can put that burden on server
Ian: It’s harder because you now need two flow controllers, one for 1-RTT, one for 0-RTT

Jana: You don’t need a new flow controller, just keep count of how much for 0-RTT

MT: Special processing for stream frames in 0-RTT

Ekr: No way to increase 0-RTT flow control window, doesn’t strike me as that hard to enforce

Kazuho: Can apply this check, I don’t think we need to enforce, but need to allow servers to enforce it

Ekr: We do require servers to enforce flow control violations. Why require that? Should that push us towards requiring this?

MT: Just an additional check, I would assume we would have special handling for data in 0-RTT and check against a counter/limit

Alan: I’m going to make you send me illegal stuff to see if I error

Ekr: We do that all the time

Alan: How often server changes flow control limit is probably once a year, probably very rare

Jana: Sure sure

Ekr: Maybe the argument here is that you have to remember this, maybe that’s more annoying. For ordinary flow control you have server state and you know exactly what’s allowed

Mike: You already have to save TPs

MT: If you’re doing something like increasing limit from 5k to 10k, you don’t necessarily have to remember that

Ekr: Why save TPs?

Mike: They’re only allowed to increase and client must comply with that during the first flight

Ekr: This one is different, max early data is a separate TP that only applies in first flight, and there’s no opportunity to change it

MT: This isn’t quite that, we just use the standard flow control limits

Alan: Is this just MAY vs. MUST?

MT: Yeah, if it’s trivial MUST otherwise MAY
We had a discuss already around application of TPs to new session ticket, had ability to put TPs attached to new session ticket, allows setting limit for the next connection 0-RTT. Decision was not to have the extra degree of flexibility.

Ekr: You could just define a new TP if you really needed that

MT: If you wanted to do 1-RTT thing you could send MAX_DATA after connection was established

Ekr: The only piece of flow control in TLS is max early data and otherwise you’re limited by TCP so this can’t happen there

Marten: So then we’re still weakening security of QUIC

Jana: Does TLS require that the server enforce this limit?

Ekr: Looking it up, I know we enforce it. TLS says SHOULD enforce

MT: I can use a SHOULD

Ekr: We all agree client can’t go above, I’m not going to press for MUST enforce, SHOULD seems good, MAY would be okay
As far as separate TPs, how many people are going to actually use this, if nobody then doesn’t matter, if everyone then we should have another TP. Let’s check implementation experience

Mike: I don’t see why you couldn’t just include window update in first 1-RTT

Ekr: You could, if everyone’s doing that we could just separate them

Mark: Do we have agreement

Yes, we’re good to let implementation experience raise an issue if we need two, for now require that client doesn’t do it and server SHOULD enforce.

#### Issue 219

https://github.com/quicwg/base-drafts/issues/219

Ian: Channeling Victor:
This is a regression vs. h2, there you can increase default initial flow control window for streams. There are ways to do this, but I’ve not been able to convince anyone to implement it. Willing to slap -v2 label and move on, but be aware this is a regression vs. h2.

Alan: Isn’t there a way to do this?

MT: There’s an opportunity cost there

Ekr: Allowing client to send updated TPs would be good because they aren’t encrypted, if they’re willing to burn an RT then that could be more valuable

New frame type could be -v2 or extension

Mark: Go to -v2?

Ekr: Or extension

Mark: But off our list for now

Ekr: Yes

#### Issue 969

https://github.com/quicwg/base-drafts/issues/969

Nick: I didn’t realize this was even still open. Issue is that you process ACKs from smallest to greatest to invalidate the oldest packets first, this requires sorting, then processing.

On the flip side, it makes it more difficult to write the frame than what we
have now to read the frame, so I’m fine with closing it.
Lars: I’ve been processing ACKs in the other direction
Nick: For RACK and FACK that invalidates older packets in response to newer packets. I take the smallest ACK, invalidate everything before that, go to the next one, you don’t want to get it backwards.

Roberto: If I’m understanding, this is implementation efficiency as opposed to protocol win.

Nick: Yes

Roberto: I propose -v2 where we think more about perf on implementations

Martin D: I found current model to be more efficient

Ian: There are some tradeoffs, hard to figure it out

Mark: Okay, any objection to close

*Silence*

Close it

#### Issue 1482

https://github.com/quicwg/base-drafts/issues/1482

Mike: We have this extension mechanism, we’ve tossed around ideas for extensions. We should actually build one. Adopt one, deploy it a bit, see how it goes

Subodh: Don’t move blocked to an extension, it’s very important to do in the real spec

MT: Nobody’s proposing that now, though it was the original suggestion in the issue

Mark: I think we should assume our design is the design we want

David: Datagram extension

MT: We’ve discussed two candidates yesterday. Little risk that it’s a problem. Issue has done its job

Jana: We do not want to move BLOCKED to an extension.

Mark: Can we close? Any objection?

Mike: Can we adopt any before RFC?

Mark: To revisit that issue later

#### Issue 1993

https://github.com/quicwg/base-drafts/issues/1993

MT: Came out of discussion with WebRTC folks about potential use of API and how QUIC interacts with server
They proposed a TP in their specification, without discussing with anyone else
Client says to server “I’m a browser, the thing on the other end is web content treat accordingly” Server acks and treats according
There are some nasty hacks that use fact that someone is on the same network for auth, but browsers don’t always do that

Mark: Why is this the right layer for that

MT: Look at WebRTC land, I don’t think we need to do this

Ian: You mentioned transport param. Can we close and say “write an extension proposal”

Mark: Any other input that doesn’t mirror that?

*nobody*

Go for that


### Path Issues

#### Issue: #279

https://github.com/quicwg/base-drafts/issues/279

No objection to pushing to -v2, doing that

### Handshake-Related Issues

#### First Issue: #1951

https://github.com/quicwg/base-drafts/issues/1951

Also related, 2267.

Ekr: This is where we failed in our principles, on path attack at beginning of connection. This is about how long window for attacks survives. Second is around key transitions and expiry of old keys. Previously had timers, this replaces with a somewhat goofy signal. Elsewhere we still have timers. Two problems: (1) Don’t need to fix this at all, we’ve got lots of problems at beginning of handshake, extending a little isn’t super serious (2) If we must do something about this, we should do something else and not this

Nick had a suggestion about a general retire key bit, we should do a single mechanism like that if we’re going to do anything

Suggestion: Revert this PR

Ian: Reverting is not practical, this fixes several actual textual issues.
Those issues are not purely editorial.

Marten: Only reason we use timers is for reordering resilience. Nothing bad happens other than reordered packets are not decrypt-able and get retransmitted, so those are purely optimization. Handshake keys on the other hand, we rely on encryption level, and we need to use those keys because we can’t retransmit with other keys.

David: I agree

Kazuho: If the attack doesn’t go away, I don’t see a reason to pay the cost of this mechanism

Ekr: This creates a weird interlock

Marten: I think timers are bad too, though. There’s nothing bad about seeing that next encryption level was used and inferring that we know packets were received

Ekr: We have a mechanism for determining when things are delivered and that’s ACKs

David: If we don’t discard keys at all, there are attacks for injection later from Initial, etc. We want to stop accepting Initial packets. However, if we stop accepting too soon we can get into weird situations. Proposal I like is to have an explicit signal: the moment you can agree you stop receiving you use that signal and stop then *missed some more detail*

Christian: It’s really about when do you want to stop accepting, need to coordinate that between the two sides.

MT: Can we keep it on this issue?

Ekr: I think this is about the keys, not quite the same issue. If we have an approach of saying “I’m done with this key”, it solves lots of the problems here.

MT: I’m actually okay with that

Ekr: That would then be ACKed and you’d have all the right properties, new one is sent with the new key not the old key

David: Two general’s problem. Let me explain: You can never be fully sure of the state of your peer. https://en.wikipedia.org/wiki/Two_Generals%27_Problem

Ian: I was originally in favor of the change in the PR. Reasons: (1) most implementations will remove from send queue all initial data once they could anyway as an optimization (2) I don’t like timers that expire on 3MSL, prefer having a real signal that is exercised all the time instead of something that doesn’t occur on all connections.
Fine with a different explicit signal that isn’t handshake packet.

MT: Explicit signal could work just fine, man-on-the-side could no longer send you a spurious Initial packet later one, which is the whole point. Would also kill off other handshake-y problems. Going to need to write up and discuss a PR for a concrete proposal, want to roll forward rather than back something out.

Ekr: This also kills 2267

Mark: Yes

Ekr: Also solves key-update

MT: Potentially solves key-update.  It’s beautiful.

Martin D: Is there any objection to solving initial with timer?

Subodh, David don’t like it

Subodh: Yesterday we discussed flow control handshake messages, is it such a big deal for you to keep handshake keys?

Ian: You’re talking about 2267? No

MT: This is the case with 2267 where if you didn’t throw away the keys, you wouldn’t have that problem.

Ian: But TLS says discard after 3PTO and throw away keys

Marten: Proposal is to have explicit signal, one way, per encryption level

David: Signal says I have received everything I’ve expected to get at the previous level, once you’ve sent that and received it from the peer, then you throw away the keys

Marten: You can discard directional keys earlier, but okay

David: Sure

Subodh: This adds more complexity though, explicit signal adds more conditions to check vs. implicit signal which is easier to check and the whole thing is only useful for Initial->Handshake transition anyways

David: I think there’s value in later transitions, good to discard them and save state. Also condition from Marten where CFIN gets retransmitted indefinitely, nice to have one solution that does all of them.

Jana: Behavior hasn’t changed, you’re just more explicit about knowing that the peer did that

Subodh: Yes, but you have to check and now deal with it if they violate that. It’s not free, there could be more dragons in that closet

Jana: Seems like it’s less cost

Ekr: We’re waiting for MT to make a PR now

MT: I’m going to do this as a mega-PR that kills: Key update, 1-RTT transition, Handshake transition, all subtly different, will be big but the core of it will be relatively straightforward. We want a signal that says “I have read and write keys for this epoch” and I am prepared to use those keys. Once you’ve both sent and received one of those, you can remove everything from before that.

David: I would slightly tweak, you need to be done with the previous one, including CFIN.

*Jana and David discuss read key*

Christian: You can do stuff with implicit, there are some things you can’t do, there are some attacks where you need to send ACKs but could be sending for spoofed packets and then the peer could kill your connection. Secondly, let’s be done with it.

Subodh: I think that’s only relevant for 1951 with spoofed ACKs with Initial->Handshake transition. I think implicit can still work with Initial->Handshake, doesn’t work as well for Handshake->1-RTT, can just keep Handshake keys, but if people prefer to drop them that’s a different thing

Ekr: I agree there’s not a huge amount of value in dropping the Handshake keys. But I prefer the more general solution, and if it solves more problems then that’s great too.

Marten: How does this relate to the key update problem we had before with frequent key updates, do we still need the bits in the header?

MT: No we don’t, this would be the frame that people were arguing for to solve that as well. So this rate controls the key updates and we’re all set with that problem.

Mark: How long to write the PR Martin?

MT: I have most of it there already, so shouldn’t be a huge amount of time.
I’ll do two phases, technical pieces correct, reason about it, then organize and clean it up: this will touch recovery, transport, and TLS.

Mark: Mostly concerned about how we judge consensus.

MT: I want to do this on new process. 2 weeks.

Mark: Make PR, proposal, get consensus on list.

That closes 1951, 2267, key update elsewhere.

MT: Noted in 1951 that conclusion in 2267 will be placeholder for this.

Mark: Everyone okay with that.

*No objection*

#### Issue: #2267

https://github.com/quicwg/base-drafts/issues/2267

See above discussion.

#### Issue: #2309

https://github.com/quicwg/base-drafts/issues/2309

Christian: Migration before handshake is completed is very messy. We had some implementations try doing migration right after connection is setup, but then you get a repeat of handshake packets, but then you see some of them being sent on the new address.
High level solution is to not initiate migration until you’ve completed the handshake.
Wanted a PR to do just that, but we don’t have a way to refer to what constitutes “completed the handshake”. Want a way to say it’s done, but if we have

Jana: Principle sounds good. Let’s do it and add the definition.

David: gQUIC makes a new connection.

Ian: I think that’s what Eric was saying as well.

Mike: I will concur, we just need a better definition; previous issue will add one.

Christian: It’s not sufficient to have the keys that you need, you need to be sure that the peer whas all the keys that they need.

Mike: Client can’t really know the handshake is finished.

David: MT, in your PR, can you define handshake finished as when you’ve discarded Handshake keys.

MT: Defining handshake finished that way is wrong, but cannot migrate until Handshake keys have been discarded is okay.

Mark: Note that we’ve agreed we want to do this, how it gets incorporated depends on the PR for 2267.


#### Issue: #2180
https://github.com/quicwg/base-drafts/issues/2180

Ekr: In the case of Retry, you can do two things: make a whole new connection with crypto state, CIDs, etc. Other one is to replay previous initial packet.

MT: We’re not very clear on that point

Ekr: It would be one thing to say nothing, but we encourage people to make a new packet, if we want people to do that, we should require it. Argument against: It may cost a lot to do that, especially with post-quantum. Some level of variance as to what you could take from previous one (key shares). We should decide if we think this is a whole new connection, or is it a continuation of the previous connection.

Ian: I believe it’s a continuation of the current connection, but I know that’s not documented.

Jana: I think it is, it’s the original CID, if it’s not the same one, then semantically it makes no sense. Must be the same connection.

Mike: You’re regenerating client hello whether it has same key-share or not.

Martin D: Client TPs don’t have that, so not

Mike: Ah, I’m remembering a different iteration

Subodh: We cache CI, since 0-RTT data needs to be dealt with, do we replay it or not, do we tell application to retry 0-RTT data themselves, what do we do with that?

Ekr: Wasn’t there some stuff about how to fix the 0-RTT data?

MT: If you get a retry you can send 0-RTT. If you don’t change key then you have to keep increasing packet numbers, there is text there already for that

Ekr: We think you can use 0-RTT in Retry

MT: Yes we’ve already decided that

Martin D: If we do in fact have language encouraging people to write a new client hello, we should strike that, I don’t see any negative impacts if the client wants to do that, but we can leave it up to the implementation.

MT: Reason for that text is the 0-RTT stuff.

Christian: Kazuho and I have been working on a secure way to do the handshake which would remove the possibility of having an attack during the handshake. A key part of that is verifying that the client hello is exactly the same in the client initial and in the retry. As in a hash of the crypto data matches the previous one.

Ekr: Christian, as I understand it, you would like to prohibit changing the client hello. *Yes* Modulo 0-RTT sequence number issue, there is no actual reason to change the initial packet at all, we know how to make the 0-RTT packet safe with the sequence numbers continuing to increase. That makes more sense with layering design of QUIC. Architecturally I don’t see any reason to change it, so it’s better to say that you can’t change the client hello. There’s at least one reason you would say that: There might be situations in which you want to get a head start on processing the data while you wait for the retry.

Subodh: One of the reasons that you might want to change it -> VN downgrade protection might require regenerating to include new TPs.

Ekr: VN is different. That always conceptually required regenerating it.

Subodh: We have this special cause where one way you do it this way, VN, you do it the other way. It would be nice to have consistency there. Regeneration of client hello would allow you to do that in one way.

Ian: I support Christian and Ekr saying you MUST NOT change it. Tells you nothing new about it. Why would you regenerate something based on absolutely no new information.

Jana: VN and Retry are semantically completely different, I think it’s appropriate to keep it that way.

Marten: I’m okay with implementations wanting to reuse their client hello. In my implementation it would cause a lot of trouble to reuse it, so I don’t want a MUST NOT.

Ekr: Why?

Marten: It would be easier to start a new TLS connection. You can either tell TLS to close and start a new one.

Ekr: I just assumed you hold onto the data from your Initial packet, since you need to do that in order to retransmit it anyways.

Kazuho: I prefer MUST use same client hello. TLS 0-RTT has this requirement that says when a packet arrives later than expected, then it should reject 0-RTT, want to make sure implementations won’t reject if it comes back 1-RTT later.

Ekr: Yeah we need to find a way to fix that, the issue is that we have a time difference between the packet was sent and received, but now you’re going to have built in a bunch more time difference.

Kazuho: Argument that TCP also has retransmissions

MT: Yeah that seems like the right argument. If you treat this like loss, that just kind of works, and doesn’t impose anything new on implementations

Martin D: What if I want to edit client hello to allow 0-RTT

Marten: There’s nothing stopping much later Retry

Nick: Should be time limited to prevent attacks.

Ian: There’s a time limit on retry token and you can’t wait forever

Roberto: Sounds like we’re arguing that we should change protocol to make implementation easier. Can we do that in -v2.

Ekr: The proposed MUST is about making protocol thing easier.

Proposal: Resolve this by saying you must reuse same client hello every time. Argument for: One version is better than two. Reason for this version, makes Christian and Kazuho’s proposed protection for initial handshake easier. Argument against: Makes Marten’s implementation harder.

Marten: Why are we doing this to support an extension that we aren’t actually doing yet / which would be unenforceable.

Ian: It’s much easier to only have one path, less prone to failures in the real world that are hard to debug, let’s just do it one way.

Marten: Unenforceable MUST

Christian, Nick: Put hash in retry token, totally enforceable

Hum: Support for Ekr’s proposal

*Loud hum*

Against

*One*

Marten: Already articulated my reasons against.

Mark: Go ahead and close the issue with text. Marten okay?

Marten: I guess I have to live with that, thanks for asking.


#### Issue: #655

https://github.com/quicwg/base-drafts/issues/655

Victor: I’m surprised the issue is still open. Happy for it to be -v2.

MT: This is super clever and super unnecessary.

Mark: Okay, it’s -v2.


#### Issue: 2397

https://github.com/quicwg/base-drafts/issues/2397

Lars: Comments on issue says it can be closed with no action.

Mike: Missing text people assume should be there. We don’t have text that says discard if packet doesn’t match connection’s version.

Conclusion: Short PR just to make that text clear.



*Afternoon Scribe: Sean Turner*


### HTTP/QPACK Issues

Ian: We’re not raising the bar on the HTTP3 Issues.  So we can go through them faster.  We just don’t want to royally screw anything up.

#### Varint the Things

Mike: There’s a group of issue related to varint.  Maybe we just do it all for ‘em?

Ekr: I guess I not think leave it alone is the right argument.  What’s the right argument: consistency and no extra expansion point.  Seems like it’s a pretty dominant position

Roberto: Do not see any strong opinion either way.  Pick one pick it keep it. Move on.

DavidS: As we’ve talking about the transport draft, we’ve been saying if it ain’t broke don’t fix it.  But, I am for making them all varints.

Kazuho: preference goes to single byte because http3 requires error code be sent - we can’t continue to send error.

Subodh: variant adds significant implementation complexity. Harder than QUIC, where it goes in one packet.  There are different design constraints.

MT: It applies to stream types anyway.  0 length will open.  Doesn’t agree with Kazuho.  More important for consistency.  But, get all of the same rules of extensibility as elsewhere.  Opposed to minimal length encoding for any of these.

Ian: MT said most of it and I want to agree with MT that Subodh’s argument is compelling.

Mike: The issue there is that anytime you want to parse something that starts with a varint - you have to read one byte to figure out long it is.  For frame types and one other thing, it’s usually 4 bytes.  For unidirectional stream this can’t be assumed.  It’s workable.

Roberto: So … either HTTP3 is layer on QUIC or not.  If we are peering into that then it really isn’t making sense.  If we’re going to do a layer violation we need a really good reason.  varint forces us to acknowledge the abstraction.

Alan: I want to make the other case.  I prefer stream types on 1 byte.

MT: That’s the one we have arguments for varint.

Kazuho: Depends on API.  If it’s in the kernel there’s one set of calls and if it’s in user space you have another.

mnot: Who wants to die on the sword.

Hum: Should we go all in on varints?  In decisive

Hum: Can we live with either? Never did it

Eric: varints are used elsewhere because they’re great.  If it holds here too aren’t we good?

Subodh: The HTTP3 API is going to expose different things.

Alan: The stream type in particular are not under a length prefix.

Mike: We’re going to talk about frame types in just a sec.

Ian: Is there a reason to not do settings.

ekr: What are the principles? varints are extensible, but harder to parse.

Roberto: When reordering happens you end up with the same buffering problem.  Reordering happens so we have to deal with it.

Victor: varints are much easier to write IANA policies for.

Kazuho: Regarding API: are always different.?

Christian: Stream types - encoded as ASCII Charters surprised me.

Mike: They’re octets. We picked those for values, but I really do not care?

#### Issue 2275: Varint h3 unidirectional stream types

https://github.com/quicwg/base-drafts/issues/2275

Frame types

Mike: Currently a length prefix so under the same logic it would be fine.

MT: It’s not under length.

Roberto: 0=1

Hum: Unidirectional to varint? Ambiguous.

Ian: I do not think that we’re going to run out of space.

David: the point of unidirectional stream type is you can just send ‘em

MT: requires minimum length

Victor: I’d like a bigger space?

Hum: Varint these.  Yes.

Alan/Subodh: I am grumpy (and want it minuted)


#### Issue 2253: Consider making h3 frame types varint

https://github.com/quicwg/base-drafts/issues/2253

See earlier discussion.  And then we landed back here.

Mnot: sounds like we are okay doing this.

Subodh: with or without min

MT: without.  We made exceptions for QUIC frames

Generate PR!!

MT: MALFORMED Frame needs to also change.

Mnot: Is this controversial?

Mike: The issue is that the bottom byte is the frame type.

Kazuho: Use reason phrase!

Ian: Use low byte.

MT: 0-254 is fine 255 is something new.

Kazuho: Can’t we just remove it? Why do we want do this?

Ian: I do not think that we should be using reason phase in production

mnot: Let Mike write it up?

MT: Does anybody care

Ian/Alan: don’t remove it.

#### Issue 2233: Why are setting identifiers not varints?

https://github.com/quicwg/base-drafts/issues/2233

Hum: should be settings to varint? Yes!

Moving on to LTV.  Will come back.


### Push Issues

#### Issue 718: Retain use of SETTINGS_ENABLE_PUSH
https://github.com/quicwg/base-drafts/issues/718

Mike: Explains issue.

MT: Special race case related to settings.

Mnot: Close with no action?

ALan: would like to see setting returned.

Mike: I want to bring the setting back.

Hum: Settings for push? Yes hum won.

#### Issue 2232: Should receipt of multiple promises really be an error?

https://github.com/quicwg/base-drafts/issues/2232

MT: the problem is that if you get multiple push promises you get multiple header sets which then might not match…

Mnot: closed with no action?

### Extensibility Issues

#### Issue 2291: Allow extra data after self-terminating h3 frames

https://github.com/quicwg/base-drafts/issues/2291

David: explains issue

Mnot: I would personally say no.  We have other escape valves.

Roberto: What is a proxy supposed to when it sees on of these.  Ambiguity will cause us much pain.  We need to be able to route it.

Jana: I would prefer we explicitly design and use extensibilities.  We do not need another way.

Ekr: TLS1.0 had this design and it didn’t work.

Alan: Move to close discussion.

Mnot: anybody support this?

David: I agree with the statements with one caveat: it would work if we had a way to extend it.

Mnot: Any need to clarify the error handling

David: no need.

Roberto: it is not clear that adminig this is safe from a security perspective.

CLOSED!

#### Issue 2229: Can I send non-data frames on CONNECT streams?

https://github.com/quicwg/base-drafts/issues/2229

Ekr: Please provide clue

MT: We need to say.  Connect is special.

Mike: A connect stream is still an HTTP transaction so it’s just like normal.

MT: what we are looking for is do handshake do new DATA XX - this is a special snow flake.


Ekr: What about error frames?

Nope.

Ian: Can you prioritize connect?

MT: File an issue

Mike to draft some text.

#### Issue 2224: Why do control streams need to be typed?

https://github.com/quicwg/base-drafts/issues/2224

Ekr: Explains issue.

Ian: there were a lot of people that Ryan Hamilton agreed, but we talked through this and you’re in the rough.

Ian: Anything that could be said to change your minds.

Mnot: Closed.

### HTTP Messaging Issues

#### Issue 2396: HTTP/3 frame encodings are unnecessarily difficult to serialize and parse

https://github.com/quicwg/base-drafts/issues/2396


MT/Ian: explains issue

Mike: Knowing you have a complete frame is a generalization of the issue we discussed earlier.

MT: I like the Length for that.  The cost of working out the length can be varints not minimal length.  I think this is unnecessary especially considering you might not have everything.

Ian: we are at a different layer that in QUIC so it’s okay that we have different logic.

Victor: It’s easy to parse in transport because you got all the frame.

Ian: I am okay with closing this, but just wanted to raise the issue.

Ekr: I do not think having a lookup table is all that hard.

MT: you don’t need a lookup table because you got all the data.

Ekr: I agree that it undesirable to byte by byte parse the frame to figure out the length.  There are also cases 1) goes to end of stream, 2) fixed length frames.

MT: For fixed length frames we’d like to not have the length.

Roberto: Knowing how to frame something, having optimal frame, knowing how to parse. Sometimes the first two get mixed.  It’s a little confusing as to what we’re trying to solve.

Ekr; Seems if have extensions you can negotiate this.  Let’s kick this down the road.  We can’t skip 2395.

Mike: Some frames contain a single varint. You’re reading a varint to tell you how long the next varint will be.

Dmitri: I think we need to agree on the principle.  I think we’ve been talking about keeping flexibility.

Ekr: my proposal 1st time we have an extension that needs it update this spec.

David: This only works if we have a lot of type space.

Mnot: this sounds like a separate issue.

Jana: If we’re going to talk about TV to happen in extension frames.  We should apply it to the frames we have.

Ekr: The only frame we might need that for is DATA.

Mnot: Any interest in TV for anything other than DATA?

Mnot: not we’re talking about TV for our existing frames?

Roberto: If you are 256 it’s all going to be varint.

Kazuho: Against TV for anything other than DATA.  Makes decoding difficult.  (argument ensues about how difficult)

Jana: I completely agree that we should keep the length.

Mnot: whiplash - closing with no action but we’re going to get to data frames.


#### Issue 2395: HTTP/3 uses LTV unlike TLS or QUIC transport

https://github.com/quicwg/base-drafts/issues/2395

Ian: explains issue

David: One other niceness is that right now we have LTV that are known fixed length.  It feels silly to fall over and die on that.

MT: Happy with LTV.  no desire to use TV.

Ekr; The argument was about some cases where the remainder of the data?

David: Another issue …

Ian: Changing to TLV allows us to not lie about the length.

Alan: Not in extensions.

MT: Suggest we make the switch the TLV?  Can’t remember why we ended up with LTV..

Mnot: any reservations.

Alan: Makes we want not want varint more.

MT: Then LTV!

Mnot: any reservations?  No response from the room.

#### Issue 2230: What indicates the end of a message?

https://github.com/quicwg/base-drafts/issues/2230

Mike: I think this is editorial/terminology.  I do not think we need to change this.

Ekr: Having two things is worse than having one.

Ian: Nobody uses trailers.

Roberto: There’s no such thing as an empty headers block.  When we do wish to consider different reps, e.g., as message, and more overhead will be required.

MT: is there an incongruity?


Ekr: Overhead would be two octets.

Roberto: might be longer if we start to do partial reliability …. Then you need to describe what the data is.

Kazuho: considering the fact we sometimes omit the body we don’t have a consistent way to fix this.

Ekr: Not going to the mat on this.

Mt: More than half requests have zero length bodies.

Ekr: happy to close, but address last sentence.

Mike: Need to fork that the server not send PUSH_PROMISE after the second headers.

Mike to clarify.


#### Issue 2228: How do I generate an RST?

https://github.com/quicwg/base-drafts/issues/2228

Ekr: This has to do with connect.  Explains issue.

David: Can we make this a SHOULD?

MT: MUST RESET if possible close otherwise.

Mike to craft text.


#### Issue 1885:DATA frame encoding is inefficient for long dynamically generated bodies

https://github.com/quicwg/base-drafts/issues/1885

Mnot: Bringing back HTTP1 nightmares.

Ian: The main reason is about making easier to fast zero copy implementations.  Most compelling argument against - they aren’t going to use the crappy thing we have now enough.

Mnot: Yeah I see that, but is a nice optimization.  We should do this in another Frame type.

Ian: this should be a different frame type.

Roberto: I feel strongly about this one!  Seems like it’s easy to mess up and do so subtly.  It only helps those that know the path, but it doesn’t bring benefit everywhere.  Difficult to argue that its benefits will outweigh its cost.  We’ve seen this go wrong.

Mnot: Why wouldn’t this allow trailers.

Roberto: Proxy get to use frame type before or after it parses all the headers …

Mike: In terms of protocol consistency we should nothing or make it a property of frames in general.  Can also be done as an extension - existing draft.

David: It doesn’t need to be unidirectional.

MT: there might be dragons here.  Prefer to have there’s a new XX frame.

Ian: Understand Roberto’s arguments, but don’t agree on many points.  Adding necessary framing makes it harder to implement.

MartinD: Memory consumption for connection is a pain.  Needs solution to give the content later.

Victor: 1) Nested multiplexing framing code is super U-G-L-Y 2) Last frame is easier to optimize.

Dmitri: If it’s cache you know the length.

Ian: Not always true.

Roberto: zero copy isn’t going to happen anyway because we’re doing crypto.

Lars: If you offload then you can do zero copy.

Roberto: If you got hardware you can fix this.  We need to solve this because there is a cost.  On Mike’s point, I think we should hold off to discuss it until v2.  What you are proposing will result in huge framing changes.

Mike: There are options that do not require big changes.

Ekr: No extension. If it’s a good idea do it here, if not then do not ever.

Mnot: Is an optimization.

Ian: yes.

Ian: we are talking about a TV.

Roberto: You can punt this to the QUIC layer.  This should be solved at QUIC not here.

David: We have a notion that HTTP layer is causing a problem.

Kazuho: This issue would be better solved at stream layer.  Make it series of messages.

Jana: Is the suggestion we do a new stream type that is a stream of messages.

MT: I think Kazuho’s PR is hard enough to make me against it.

Victor: My intuition that there are edge cases where the are proxies so I’d go with an extension.

MT: Let’s get some experience with this.

David: If we were to come with an extension would the WG be open to giving us an IANA number under 64?  Never mind, withdrawn.

ekr : this needs to be a negotiated extension!


### Relationship to HTTP/TCP Issues

#### Issue 2223: When can you coalesce connections

https://github.com/quicwg/base-drafts/issues/2223

MT: This is hard!

Mnot: Let’s not do this now.

#### Issue 371: ALTSVC Frame

https://github.com/quicwg/base-drafts/issues/371

Mike: Explains issue

MT: Mike has a draft for this.

Mnot: We need a little more aging of H3.

Mnot: Can this ship right after or with?

Mike: This will go to Httpbis.

#### Issue 2384: What scheme should be used for HTTP/3?

https://github.com/quicwg/base-drafts/issues/2384

Mike: HTTPS URIs are defined to be TCP-only.  We need a way to refer to HTTP/3 endpoints.  Alt-Svc is one way, but requires talking over TCP first.  Options include redefining meaning of “https,” putting Alt-Svc in DNS, or minting a URI scheme that refers to a different transport protocol.  Issue proposes new URI scheme.

Mnot: A new scheme is not a decision the WG can make alone.  We need to coordinate this with the HTTPbis WG and W3C Tag.

Ekr: 1st principles: if you have an HTTPS site and QUIC and they are not the same origin it is going to be a disaster.  How do you tell the client that QUIC is available? Can we do this with a self-contained URI to convey this info.

Mnot: Should this WG do this?

Ekr: No

Mt: Nobody should do this.

Eric: Not all of them make me sick.  But, it needs to be backward compatible.

MT: We should not do this.  I like revising HTTPs to say QUIC could be there.  A new scheme would be a huge PITA for security.

Victor: I would like to do happy-eyes with custom ports.

Roberto: URI is not well suited for that.  Should probably do this in HTTP area of scpoe.

Mnot: Closing this issue out.

Mike: One thing I found is that the spec says the scheme tells you what transport is. Doesn’t limit it to only one transport, though.

CLOSED

#### Issue 253: HTTP/QUIC without Alt-Svc?

https://github.com/quicwg/base-drafts/issues/253

Mike: Same issue as above, more generally.  If not a new scheme, what will we do?

Ekr: Say I am handed an hTTPS URI and I happy eye ball it?  Can I do that?

Mike: You have contacted an endpoint that has no guaranteed relationship with the origin.

Ekr: Yeah that sounds broken.  Fix URI to deal with this.

Subodh: …

Roberto: This part is right we can do this with some mechanism.  History is that TLS cert and happy-eye balls has worked.

Mnot: Hum do we need to make sure this can work with happy eyeballs.

YES - but this is HTTPbis’s problem.  Refer to them (issue opened) and put what they tell us in the doc.


### HTTP Closing Issues

#### Issue 2226: Why do I have to explicitly cancel after GOAWAY?

https://github.com/quicwg/base-drafts/issues/2226

Ekr: Explains issue.

Mnot: remove 1st sentence of 1st para in PR

Mike: Nothing tells the QUIC stack that the stream should be closed.

MT: change the wording to make it not mandatory to give advice instead.

Subodh: This is kind of weird wording.  Needs to say what server does.

Ian: If we do not require that the server do is there a risk that the client …

Kazuho: I prefer keeping this a SHOULD.

Roberto: There is a potential race that this might resolve.

Alan: I prefer requiring it.

Roberto: I agree.

Ekr: add what cancel is about.

Mike to draft some text.

### Planning

Chairs will discuss process minutiae.  The issues we’ve discussed now will have seperate WG consensus calls.  Need really good control when entering Issues/PRs.  Editors need to follow new rule.  If you got questions use mail/slack because Issues have a cost.

Meeting in Prague.  Two sessions.  Agenda is work in progress.  Probably won’t have a -19 before Prague.  Will talk more about HTTP and recovery there.  If you see an Issue generate PR - speeds the process up.

Need one more interim.  Mid-May.  It will be in Europe.  Maybe week on May 20th (not set in stone); should know by Prague.

Interop for Prague has been requested.  -18 will be the next interop draft.

Lars will send out a doodle poll for virtual interop.

Next up “RTC” and Multipath.  There have been side meetings to discuss these issues.


### QPACK Dynamic Table Issues

#### Issue 2276: Disallow changes of table size after 0-RTT

https://github.com/quicwg/base-drafts/issues/2276

MT: We resolved this.

Victor: Is possible to prohibit behavior in 0-RTT that is allowed in 1-RTT.

MT: No. This is different.

Mike: The default is the same transport parameters.  I know I’m the rough.

Roberto: Sounds good.  Is there value in being more restrictive.  I.e., put it in transport parameters.

MT: No.

Alan: to submit PR as document in issue.

#### Issue 2258: Initial maximum table size needs clarification

https://github.com/quicwg/base-drafts/issues/2258

Ian: it’s a one line change.  It’s another PR and we’re good with it.

#### Issue 2363: The initial table capacity is zero

https://github.com/quicwg/base-drafts/issues/2363

Skipping

#### Issue 2100: Avoid creating QPACK codec streams when unnecessary

https://github.com/quicwg/base-drafts/issues/2100

Alan: Explain issues.

Dmitri: …

Kazuho: Please just make a decision.

MT: THis is an optimization

Mike: Also not required to create the streams.

Adopt Kazuho’s PR.


#### Issue 1420: encoder stream can deadlock

https://github.com/quicwg/base-drafts/issues/1420

MT: This is editorial and I will get to it.  Skipping.

### QPACK Wrapping Issues

#### Issue 2112: Largest Reference algorithm can produce invalid values

https://github.com/quicwg/base-drafts/issues/2112

Mnot: is this editorial?

Mnot: Merge it!

#### Issue 2371: Assign QPACK error codes?
https://github.com/quicwg/base-drafts/issues/2371

Mnot: it’s clerical.

Alan: They are TBD in the doc, but registry is in HTTP doc.

Kazuho: use 02xx

Alan: Sold


### QUICvis - Robin Marx

Working on Web-based tools along with JS implementation.

MT: I would like to see somebody work on standardizing this format.

Mnot: We should have done this for H2.

Jana: Thanks for doing all the work!  We might only need to agree on much more than JSON format.

Roberto: Kudos and open.

Ekr: CBOR all the things (kidding).

Jana: This particular tool uses both sites but in production we can’t expect both.

Lars: Should you do a draft.

Robin: I am coming to Prague.

Ian: Can we just put this on GH or wiki?

MT: We can add YANG later!

Lars: Put it on the tools repo.

Lars: If you’re interested in Epic talk to me!



