# IETF QUIC WG Interim Meeting Minutes - January 2018

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Tuesday Morning](#tuesday-morning)
  - [Summary of the Interop](#summary-of-the-interop)
  - [Status update from the Editors](#status-update-from-the-editors)
  - [Invariants](#invariants)
  - [HTTP Header Compression](#http-header-compression)
- [Tuesday Afternoon](#tuesday-afternoon)
  - [Deadlocking](#deadlocking)
  - [Multiplexing with other UDP (Jana)](#multiplexing-with-other-udp-jana)
  - [Greasing](#greasing)
- [Wednesday Morning](#wednesday-morning)
  - [ECN](#ecn)
  - [Connection ID](#connection-id)
- [Wednesday Afternoon](#wednesday-afternoon)
  - [Larger Connection IDs](#larger-connection-ids)
  - [Connection Migration](#connection-migration)
- [Thursday Morning](#thursday-morning)
  - [Connection ID](#connection-id-1)
  - [Header Compression](#header-compression)
  - [Loss recovery draft ](#loss-recovery-draft)
- [Thursday Afternoon](#thursday-afternoon)
  - [Abstractions](#abstractions)
  - [Extensions](#extensions)
  - [3rd Implementation Draft](#3rd-implementation-draft)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Tuesday Morning

*Scribe: Ian*

### Summary of the Interop

EKR: Some people made more progress than before and got resumption working.  Found a lot of items weren’t in the release notes and some of the changes were unclear and hard to find.

Patrick McManus: If we make some progress on QPACK/QCRAM then we might want to add

Christian: Want the spec to stabilize more before expanding the scope of the interop, which we’ve heard.

Christian on the topic of December Interop: Seems like a lot of the issues were problems with TLS interop or the handshake encryption, and that made testing QUIC interop more challenging.

Lars: Ideally we’re at the point where TLS has stabilized, so problems with TLS stacks should decrease over time and stabilize.

Ekr:  (Still implementation bugs.)

Lars: Plan to do another interop between now and London.  The next interim will likely be somewhere in Europe, and we may want to spend 2 days on interop and 2 days on interim instead of 1 and 3.

Lars: If we’re serious about Nov ship date, the window for large changes is closing.  After 09, it would be good to do an editorial update instead of spending time on changes.

Ekr: Sympathetic to the idea of not making major changes, but we’re just starting to get real development experience.

Christian: One thing about the next draft that is large is connection migration.  If we are going to do it, it should be soon.

Jana: Some changes are feature requests and bug fixes, so at some point we’ll have to focus on bug fixes.

Ian & Jana on whether we’ll have good data on IETF QUIC by November: Jana said we’d evolve towards IETF QUIC and Ian said at some point there would likely be a large jump.

Ranjeeth: What if we target HTTP 1.1 instead of H2

EKR: That would have some advantages, much more straightforward.

Ted: What if there is a performance regression vs H2, that might be hard to communicate externally.

Ian: I’m concerned that supporting HTTP 1.1 over QUIC transport will delay the transition away from Google QUIC, which is probably not in anyone’s interest.

Patrick McManus: Maybe we should talk about this on Thursday.

### Status update from the Editors

MT: Header compression ‘hopefully’ will make 09 but maybe not.  Also greasing is coming down the pipe, but probably won’t make 09.

### Invariants

MT: Maybe ask for WG last call in London.

EKR: Instructions about what won’t change and instructions to the network about what they can assume.  We can assume that any changes that conform to the invariants should be deployable and those that change the in

MT: We should be more confident in changing things in QUIC as long as the changes do confirm to the invariants.

Brian Trammell: I think we should better understand the line between this document and the manageability document. In particular, the invariants document is short and sweet, and describes things we will commit to not changing. Well, the colored parts won’t change; we might commit to future invariants on the grey parts. But assumptions that will be made on our behalf; does that go in manageability?

Ted Hardie: I’m not sure what you need about assumptions made on our behalf.

Brian: Things like the packet number which middleboxes may assume have certain semantics may become very difficult to change, even if they’re not part of the declared invariants.

Christian: If it’s not greased, it’s not going to be usable in the future.

MT: Call for adoption and call for earlier adoption than the other docs.

Spencer: MIC: I'm still hoping that the invariants doc will be really short, re: relationship with manageability doc, because you don't really want to open it to make changes to text and then get proposals to make more changes since the doc is open, anyway.

MartinDuke: Is the bar for GQUIC an RFC?

Ian: I have a fairly clear idea for what our plans are and am happy to go into them either in person or for the entire WG if there’s interest.

Roberto: Should specify that these hold across v4 and v6.

### HTTP Header Compression

*Mike presenting*

Slide comparing performance of static HPACK, QMIN, QPACK and QCRAM compression efficiency

MartinDuke: Why is QMIN worse than static HPACK at the very beginning(first request)?

Dmitri: This config is setup to be very aggressive about inserting cookies into the table, so it ends up sending both a literal and dictionary insert for initial requests.

Buck: Both QPACK and QCRAM provide much less head of line blocking and latency under loss compared to HPACK.

EKR: Are there any experiments planned to provide more useful data about how to choose between these?

Jana: Loss reduces congestion window, so the simulator is not truly representative, but how complex do you really want to make the simulator.

EKR: We’re going to make decisions based on data and aesthetics, what more data do we need?

Roberto: The only way we get realistic data is to implement and deploy all of them.  But we need to short-circuit the process.

MNot: If we get to parity, then we’re doing well.

Mike: Right now, we’re chasing parity with H2 (for compression efficiency), not trying to exceed it.  The goal is to achieve this with better HOLB properties than HPACK.

Second to last slide:

Jana: Proposals are representing design points, but we don’t need to adopt a specific one if we want.  Call it QCRAM+PACK.

Mike: Or call it QPACK-05?  QCRAM style accounting with things sent on the control stream.  Do we want an optional feature to say “no blocking” on the decoder side?

EKR: Worst issue is deadlock.  That seems like a dealbreaker.

Ian: That’s why Ian and I were thinking of QCRAM with all mutations on the ‘header’ stream.

Buck: I think either QCRAM and QPACK could move to an entirely non-blocking approach via configuration.   And no config is going to be ideal for every circumstance.

MNot: Skeptical that applications are going to be able to use this knob effectively.

MT: Want at least the ability to do no-blocking and some-blocking in return for header compression.

Alan: Could mitigate this with transport params(or settings) that allows you to seed the dictionary.

Ian: Could use extra space in CHLO or subsequent packets to populate the table via headers

Roberto: This speculative use of requests to ‘prime’ the header compression table could end up being abusive, since that’s how applications might end up accomplishing the priming.

Jana: Agree on the first step from HPACK.

Mike: I think it’d be easier to take QCRAM and always send dictionary operations on the control/headers stream.

Buck: If streams shutdown due to an abort, it’s important the header compression context ends up being kept in sync.  If there was an HTTP level abort frame, then you can cancel it at the app layer, and then the other side can stop writing new data and defer the RST until the headers have been acknowledged.  All implementations end up with application level header acknowledgement, so the big change here is a wait.

Christian: Is concerned that Buck’s proposal requires redefining the transport level reset.

Buck: There’s no transport level reset in my version.

Alan: If we’re trying to get a conservative solution, In GQUIC, every header block goes on one stream.  In ‘this’, all table modifying stuff goes on a control stream and everything else goes on the stream itself.

Buck: In analyzing the QCRAM simulations, I think having all updates on the control stream may be a bit of overkill.  You get a lot of simplicity out of putting everything on the stream.

Jana: Echoes Alan’s point of picking something simpler.

MartinDuke: We should aim for something with similar performance to HPACK in the no loss case and aim for better performance than GQUIC in the lossy case.  Ian seconds that direction.

Buck: Push promise was what put headers back into the stream itself.

Subodh: Why are we discussing compression efficiency and not latency?

Buck: We do have some loss in the simulator, and we do see marked improvement with QPACK and QCRAM.  10x reduction in HoL blocking events by using them instead of HPACK.  Corollary: 9 out of 10 are not ‘vulnerable’ to HoL blocking and only reference data already inserted into the table, so HPACK is pretty pessimal.

PatrickMcManus: How much benefit is this?  1% reduction in header latency is even less in overall.

Subodh: 10x improvement is enough for me.  There’s no point to get better than QCRAM or QPACK.

Jana: Given that we’re trying to get done, the first 10x seems good for now.

Direction Forward: Mike to write up a PR to tweak QCRAM to not send dictionary inserts on the same stream as the HTTP request and hopefully fix up any resulting issues.  He’ll send to Buck and assuming it’s workable, we’ll discuss again on Thursday morning and hopefully call for adoption of this updated version.

## Tuesday Afternoon

*Scribe: Martin Duke*

### Deadlocking

Martin T: A stream has a dependency on a different stream, but there’s no flow control credit (a priority inversion).

Simple solution: don’t accept data unless the prerequisite is accepted. Application would withhold flow control on dependent streams, which transport would enforce.

Jana: priorities would help here.

MT: only if it’s a strict priority. Legacy H2 isn’t absolute enough.

Proxies issues: intermediaries that don’t know the app that can create problems. Can be solved by not having stream dependencies that we’re forcing the transport to resolve. Or eat memory cost at receiver. 3) timeout / cancel / retry at app layer; 4) something in between?

That would be that you terminate the connection, you own the problem. Declare ALPN, you support the protocol.

Amendment to that: Flow control is end-to-end, intermediary flow control only advertises what it’s received.

Things are more complicated with one-to-many proxy relationships.

Problem is deadlocks are low-probability, so you don’t detect until after deployment.

Roberto: one-to-many case is irresolvable. Thing to do is to focus on how to detect and resolve. If QUIC has value deadlock will happen sometimes.

MT: Please write that down if you know how.

Roberto: freeing up conn level flow control, then allocating memory to another stream would allow progress, but there’s no way to signal that over the channel.

Subodh: flow control is end-to-end but depends on RTT, etc. which is not end-to-end. Need a way to say “only make progress on this stream”.

Christian: get rid of either stream FC or conn FC.

Roberto: It was miserable with that in HTTP2 because you’re either overcommitting or starving streams for no reason.

Christian: must keep non-blocking streams quite tight.

MT: That doesn’t happen in practice.

Roberto: For full utilization, every stream must be BDP.

MT: I will keep writing down what we know, and Roberto can figure out deadlock detection and response.

Jana: What document?

MT: 2 paragraphs in the transport docs.

MD: SHOULDs or MUSTs?

MT: Doesn’t matter. Just cautions.

Alan: Are we going to encode dependencies on wire?

MT: Not at all.Priority info might not arrive in time.

Martin D: Even if I understand HTTP/2 at the proxy, how do I inherently understand all the dependencies?

Roberto: You don’t

### Multiplexing with other UDP (Jana)

QUIC might multiplex w/ STUN, ZRTP, DTLS, TURN, SRTP (0-3, 16-79 , 128-191 taken in first byte)
Long Header is 128-255, but collision with SRTP is OK given the use cases.

Ekr: SRTP thing might be true depending on your demux.
Ian: might want RTP over QUIC

Jana; replace SCTP with QUIC, plus replace media transport with QUIC

Ted: if dumuxing SRTP over QUIC, could do by port if it weren’t on 443. Use cleartext RTP headers to figure it out. Is the point making demux cheap?

Ronnie: Wanna use just the first byte. If we’re in short headers we’re OK.

Jana: is SRTP collision OK?

Ekr: what is the objective?

Jana: Not to run all on one channel. One port where all this stuff is running.

MT: People only care about STUN

Ekr: must separate easy to mux, hard to mux, near impossible to mux (with trial decryption). What are the objectives.

Roberto: Do I need to know about this is the QUIC spec?

Ekr: wire image is partially dictated by requirements of peer-to-peer QUIC.

Christian: Why only on this first byte:? There is a magic number in the STUN header.

Ekr: it must be possible to distinguish for all these cases. If for every packet, must be efficient. If occasional, doable but not super-easy.

Roberto: we’re doing port allocation. That’s bad.

MT: in this use case, we’re always omitting conn id, so we only use 64+ for short headers (just a TURN channel, but we don’t care)

Ekr: so we cannot use conn id in this context.

Ian: version # is kinda a magic cookie in long headers.

Jana: Greasing might apply. Less if we’re multiplexing. Carve-outs are not invariant.

Jana: The purpose is to figure out if anyone has problems with the current codepoints.

Ekr: RFC 7290 defines all the byte ranges.

Lars: should we grab some of the unused SRTP codepoints.

Martin S: would like to see conn id move

Lars: who cares if codepoints are contiguous?

Ekr: what are we trying to do here? Only STUN really collides.

MT: if P2P doesn’t use conn ids, which might be a safe assumption if they keep doing crazy stuff, then we can only consider TURN and SRTP for the first octet. There is somewhat hairy thing where you have to do some parsing beyond the first octet.

Ekr: as long as stuff isn’t misidentified as QUIC, we’re good to go.

MT: I think we’re close to that. The stakeholders I’ve talked to can live with this. We have to write down that conclusion and how demux should work.

Ian: conn_id flip is a total bummer for GQUIC migration.

Marten S. solvable problem if long header types are distinguishable

Igor in jabber: i agree with Ian.

Ekr: code point to add dumux byte.

Praveen: yes, demux byte. Add a p2p bit.

Ted: people keep adding to a tool. When port isn’t helping, we need this.

MT: Want to keep same greasing for P2P and usual case.

Martin D. Can we do a transport parameter saying “don’t grease the stun bits”?

MT: What about long packets?

Ted: if we don’t grease it all, then middleboxes will ossify the ungreased part. We don’t have write-ups of these use cases.

Martin D.: tension between leaving codepoints for other protocols and greasing.

Ian: Long headers are pretty good. Short headers: want to use each codepoint, but applications can define profiles that hold certain codepoints.

ekr/ted: client/server + P2P are common. If latter never uses 16-19 bec ZRTP, then ossifying/classifying

Martin D: Are we trying to help the demuxers or take the byte? Has to be on or the other.

Roberto: This demux won’t work anyway

MT: Do it just for this set of protocols, not worry about future protocols. Sometimes must process beyond 1st byte, but that’s OK.

Roberto: say we’re not being nice. The spec might be ignored. An implementation might ignore it if it’s multiplexing.

Ian: Better off just do what we want, put stuff in invariants to make stuff flexible, then punt to v2.

Ted: we can make this work. As long as invariants don’t block future versions that do what we need, we’re fine.

Lars: I feel like we’re reaching consensus.

Martin D: Let’s punt to QUICv2, unless someone shows the invariants aren’t sufficient.

Jana: do we want to go to the old codepoints?

Roni: The document already exists to explain what to do.

Jana: we’ll take it offline.

Martin T. Current codepoints make the stakeholders happy, so we’re good.

**Lars: The current spec will not change? Yes, modulo greasing.**

MT: Can we close Issue #426? I will close it with note of consensus in the room.

Ian/Jana: remaining issue is flipping C bit vs. DTLS conflicts. Will discuss later.

Christian: I like not touching anything until we have a really good reason.

### Greasing

Martin T: This is how we preserve all the non-invariant things vs. ossification.  Casual observers will see randomness, not fixed codepoints. New codepoints for each connection: simpler than encryption or per-packet variation. This is defending against Murphy, not Machiavelli.

issue #1043 Packet secrets get a random number, added to true value, to fill in fields. Packet #s start at zero.

Christian: We can’t obfuscate the size of the packet number. Short headers: we can’t get the length without a type. Long header: we might ossify on monotonically increasing PNs. 1043 has a small bug.

Jana: We need clear requirements.

Victor: three different things. changing key derivation, packet number, packet type. 1 is good, 2 has concerns, 3 might be unnecessary. Split it up.

Mark: Issues, not PRs.

Victor: not sure pkt type greasing is not useful.

Martin T. I’m happy to scale back this approach to packet #s for connection migration. To solve many problems. Might use other techniques for other fields.

Inject conn id into key/iv generation, not expansion for client/server secrets. Would generate “pnadd” at same time as key/iv. Conn ID also injected into all key generation, not just handshake.

Ekr: I might want to clean this up.

Jana: Which is used for the AAD?

Martin T: mutated PN is the AAD, expanded PN is the IV.

Changing conn IDs is a signal for a key update - but let’s not open that can of worms right now.

Ekr: omit_conn_id won’t support key updates.

Martin T: Collateral: no more PN randomization, smaller ACK frames. If we grease type it blows up multiplexing. Does not solve problems with invariant stuff, monotonically increasing PNs, pkt timing.

Jana: I like this for PNs. solves issue with PN gaps for migration.

MT: I wanna hold off the type greasing until Google guys catch up with invariants, etc.

Kazuho: Can we use  a block cipher instead? (ekr supports) MT likes it too.

(Various discussions of alternative designs to obfuscate packet numbers)

Martin D.: how is this blocking against ossification?

MT: If 4-byte field is not monotonically increasing, it might be misidentified as “not-quic”

Ekr/Mark: any objections?

Martin D: Service providers might object to trouble with measuring loss and reordering. Fixing linkability can be done in other ways.

Marcus: I can live with this if we get the spin bit.

Ted: You can do measurement in IPv6 headers. Breaking linkability very important.

**Martin T will do a whole new PR.**


## Wednesday Morning

*Scribe: EKR*

### ECN

Lars: Ingmar + Group was tasked to come up for a proposal for ECN with QUIC. Question is, should we do ECN for v1.

Ingmar presents slides….

Swett: If ECT blackholes are rare, then it’s probably fine to set it on retransmissions. As long as the handshake fails, we can fall back anyway.

Hardie: Would you fail back to not using ECT?

Swett: Fail back to TCP most likely.

Huitema: With migration, in the acknowledgement you need to indicate which path you received ECN on.

Lars: Team needs to take into account impact on multipath.

EKR/Jana: ECT might cause apparent migration failures. Maybe don’t set ECT on retransmissions.

Huitema: *Missed this point, sorry*

Even: Same behavior for ECT(0) and ECT(1)?

Swett: A lot of people don’t deploy ECN on servers

Trammell/Duke: It’s actually quite common

Trammell: One question is if you can set the ECN bits from user space.

Lars: I would like to make some progress because it affects the ACK frame?

Igor: Is there a defense against ECN rewriting?

EKR: Why can’t we just add this later?

Lars: The idea would be to at least put the probing here so that we pave the way for later use of ECN.

Swett: What about data centers?

EKR: Well, that only works if you refuse to work when paths are ECN not clear.

Huitema: We shouldn’t set the ECN bits if we don’t plan to respond to ECN. That’s the contract.

Iyengar: I don’t think that that’s actually the contract?

Duke: Are we encouraging routers to drop this?

*Discussion of mismatched objectives*

Eggert: The way we got here is that the idea was to get it into v1 it had to be small, so we just did the negotiation.

Kinnear: I see value in having the negotiation so that we can at least figure out whether it’s safe to have ECN at all with QUIC.

Bishop: You need most of this, including the feedback frame format, to do any probing even if the congestion controller doesn’t support it.

Duke: Is it really that big a deal to do this? Marginal work seems small

Swett: Agree, it’s not a lot of additional work.

J. Iyengar: This would need a lot of redesign to work with connection migration.

Trammell: This is also an issue with rerouting in TCP.

J. Iyengar: there are ambiguities about what the ACKs mean during migration. Do they apply to probe packets?

Kinnear: Can it fix with just having the probe packets be special?

EKR: Is this going to be a big research problem? If not, fine to include, but if so, maybe we should defer.

Huitema: *Missed this*

Eggert: Not worth breaking off a piece. Can we get resolution in London so we can try to implement thereafter.

Iyengar: I think we may have a solution for the migration stuff. Also worth potentially breaking off the ECN frame. Need to look more.

Eggert: Complexities with breaking off ECN frame. Let’s try to resolve in London.

J. Iyengar: Hard to get bits out of kernel

Eggert: Actually, you can.

J. Iyengar: What about Windows.

Swett: Praveen, what about datacenter use of ECN

Praveen: ECN would allow for better congestion control in constrained environments,

J. Iyengar: Can you read and write ECN in Windows < 10

Praveen: Read in Windows 10, but you probably can’t send (it is on our backlog). Probably can’t read in Windows < 10.

EKR: Is it still useful if you can read but not write?

Swett: Well, you could write on the server (where we control the kernel), and then read it on the client, even if it’s Windows.

EKR: Then it needs to be symmetric.

Praveen: Don’t base the design on what’s currently available: we are interested in QUIC and so will probably make the writing possible.

Eggert: Resolution, we have gotten feedback. People are joining ingmar’s team. Hopefully resolve in London.



### Connection ID

*Ian presents*

Bunch of discussion of several variants of issuing a new connection ID in the TLS handshake, somehow, so that the client can convert properly.

Huitema: NEW_CONNECTION_ID is pretty complicated to use for this purpose.

EKR: What about we instead put the (client ID, server ID) pair in all long header packets.

S. Iyengar: What about putting this is in a special crypto frame?

Huitema: Please no.

J. Iyengar: Do we need to have two connections on the same 5-tuple?

EKR: I do think we need to resolve this, because it drives the design.

Hardie: Is this an invariant?

Banks: We are worried about #2 because of port exhaustion, so you might have multiple simultaneous connections.

J. Iyengar: It’s multiple handshakes, so can’t you just be careful?

Banks: We have this problem with TCP.

EKR: How do you solve it in TCP?

J. Iyengar: I don’t think this works in TCP

Banks: Would need to look it up.

Duke: Is this second conn-id an invariant?

EKR: Not sure.

Swett: I want to go back to option 3.

EKR: That one is gross

[Long discussion about this that was hard to transcribe]

Pinner: Putting this in the TLS handshake removes complexity.

[More discussion]

Praveen: What are we trying to solve? N-tuple sharing?

EKR: Two things you might solve (a) n-tuple sharing and (b) stateless retry

Praveen: I don’t care about n-tuple sharing

Proposed resolution: Just have the server use the new connection ID in the stateless retry and we’re done. MT prepared PR#1066 to this end.


## Wednesday Afternoon

*Scribe: Mike B*

Martin has a PR for the Connection ID change.  General approach is agreed, modulo wordsmithing.

### Larger Connection IDs

To support connection migration, you either get new IDs from the load balancer or share state with the load balancer to create them yourself.

(Load balancer as oracle)

Alan:  Does load balancer oracle presuppose that the LB is stateful?

Ian:  Not necessarily, but probably.

(Shared algorithm)

(Keep some bits unchanged across changes)

Kazuho:  More bytes to identify server means easier to exhaust remaining bytes; probably need to use sequence numbers and even more linkable.

(AES for Connection ID)

Roberto:  Is content smuggling seriously the bear we’re worried about here?

Jana:  It’s a concern, but not my concern.

Martin:  The larger something gets, the more possibility to put a side-channel or a supercookie.

Igor:  Even 8 bytes is enough for someone malicious to make some use.

Ekr:  We don’t actually decide how the server picks connection IDs.  We can come up with a set of practices we want to make sure remain possible.  If we think this is bad for some other reason, that’s fine.  If we just want to make some approach impossible, that’s not cool.

Ian:  Load balancers will be built for QUIC, and they’re going to figure out some way to do this.

Roberto:  If the server determines this, anything we say about how is purely advisory anyway.

Praveen:  Shared state is non-trivial when the load balancers and end servers aren’t managed by the same entity.  That’s a general issue.  This is a best practice; the client can’t confirm the IDs are unlinkable.

Victor:  +1, and this isn’t the only area where we make recommendations and leave it to implementers to sort out.

Jana:  External oracle seems difficult.  If you do something with encryption, it requires a shared key.  But does 16 bytes make it actually easier / better?  Why not 17 or more?

Martin Duke:  Primary reason for 16 bytes is to use normal encryption algorithms.

Martin Thomson:  Also so you can fit more stuff.

(Slide:  What size do we want?  8/16/variable?)

Ekr:  What do we want to allow people to do?  DTLS says receiver dictates connection ID.  Server has to have some way to parse ID back out.  To the extent that we’re paying only the data size price, why would you do 16 rather than variable?  If someone can do smaller, let them save on overhead.

Ian:  Prefer #2 or #4.

Martin:  Could allow version-specific extensions of Connection ID, but only the first 8 bytes are invariant.

Roberto:  This gets really messy, you have to be able to parse it before you’ve done version negotiation.

Jana:  Less thrilled about variable.  That’s asking for processing errors.

Ekr:  Also, differentiate between client’s initial connection ID and the server’s ability to specify.  The server won’t pick an ID the server would reject; we can lock down the client’s ability to choose the initial ID.  If we’re going to allow variable-length, the client needs to be able to send whatever the server proposes it.

Praveen:  What about a client-supplied and server-supplied segment of the ID?

Ekr, Jana, others:  That’s basically Leif’s suggestion, and it’s very linkable.

Subodh:  We already have variable-length -- 0 and 8.  Why is it a concern to make it 0/4/8/16?

Lars:  Remain unconvinced by the longer connection IDs.  If the back-end is privately controlled, you can do whatever fancy stuff you want.

Christian:  Not enthusiastic about 16 because you can sneak stuff into it.  But if we can’t stick with 8, make it variable.  Describing how the server and the load balancer coordinate is outside our scope.

Jana:  No, but we should think about the implications of likely designs.  If you’re going to go variable-length with a fixed set of choices, that’s fine -- just please no length byte.

Roberto:  If you want to be unlinkable, you need routing data, salt, and sequence number.  That’s hard to fit in only 8 bytes.

Mark:  The “fancy stuff” that has been done for TCP is a nightmare.  We can do better here.

Victor:  Outlined the scheme in my e-mail because I believe this is something plausible and it doesn’t fit in 8 bytes.

Ekr:  +1 -- every time we try to do something with Connection ID, it’s not big enough.  Don’t necessarily need MAC, if we can make weaker security guarantees.  Do we agree whether we need more than 8?  If we do, we can bikeshed the details of how big later.

Praveen:  Need to talk about deployment issues of this, even if we don’t specify an exact scheme.  Prefer not to put larger CIDs in invariants.

Kazuho:  If you want 8 bytes, you would use DES, which is slow.  If we use 16 bytes, you can use AES.

Roberto:  Load balancers serve an important role.  We need to enable the load balancer to do the best job it can -- let’s make sure it has enough bits.

Ted:  Making this an invariant size is problematic -- we won’t know the needs of the system before we ship.

Leif:  If we don’t move from 8 bytes, it will be worse than TCP, not just as bad.  We need a way to get the right things to the right machines consistently.

Lars:  8 isn’t enough for that?

Ian:  Not if you also need unlinkability.

MT:  We’ve tried really hard to save bytes other places.  This seems to move in way the wrong direction if we just make it 16 bytes.  Let’s do variable, if some people need it that big.  Not everyone will need that.

Christian:  Communicating with the load balancer is complex, but solvable.  They need communication or a shared key; we should be explicit about that.

Ekr:  +1 to Martin, but again:  Can we agree that we need to permit larger connection IDs?  That would shrink our argument space.

Lars:  16 bytes seems an insane amount of overhead.  I’m willing to believe in the creativity of middleboxes if we don’t give them the easy option.

Jana:  It’s true that this seems profligate, but remember that server-to-client typically doesn’t use a CID at all, and the client-to-server direction is typically not bandwidth-limited.

Lars:  But they’re still paying for the data expense!

Patrick:  If variable gives you the possibility to go lower than 8 bytes, that seems worthwhile for the net cost.

Subodh:  Load balancers aren’t going to optimize for unlinkability, they’re going to optimize for their management.  If we try to force their creativity, not all of them will actually do anything creative.

Ian:  Victor’s proposal is totally valid for some use-cases at Google, but not all use-cases.  We have others that are fine with 8 bytes, and some that could maybe get away with 4.  I don’t want to go to 16 bytes all the time.

Martin Zeeman:  For P2P, 4 (or even 0) is sufficient.

Praveen:  Other scenarios where client-to-server do carry lots of traffic; don’t assume that.

Mark (as chair):  Let’s get a sense of the room.  Option 4 seems to have a lot of support…?  Drain queue, then discuss.

Roberto:  PRISM.  If you’re going to use short Connection IDs because you think you’re safe in your data center, you’re wrong.  If you permit short Connection IDs, you incent people to do the wrong thing and make it linkable.  Game theory says servers can do a better job by doing the minimum, because the server isn’t going to care about the client’s linkability.

Victor:  +1 to Ian’s point, we don’t always need 16.  I’m not sure 4 bytes will actually be worthwhile, but variable-length has few disadvantages (other than what Roberto said).

Igor:  Not confident that companies will abuse the opportunity to use shorter CIDs.  Like variable; some cases don’t need long CIDs, but 16 bytes is best for user’s privacy.

Christian:  Was thinking variable, but sensitive to privacy argument.  Also complexity ensues if CIDs aren’t a consistent length.

Ekr:  DTLS lets server specify length, and both sides just know what it is.  Doesn’t need to be embedded in the packet.

Martin Duke:  This is not a technical problem -- there’s a lot of politics embedded here.

Chairs:  Need to conclude this in London if not sooner.

Martin Thomson:  This is a threat to the invariants.  Need guidance ASAP.

Anyone can’t live with anything in 1/3/4?  (Silence)

Hum for 8 bytes invariant:  A few

Hum for 16 bytes invariant:  Comparable to #1

Hum for variable:  Decidedly strongest, including online

Jana:  There are details on how to do that.

Ekr: But not in this meeting.

Lars:  Do we have consensus on minimum/maximum?

Martin Duke:  I echo Christian’s concern about the code complexity.

Ekr:  Design points that are relevant:  Min/max and whether the wire format states the size

Subodh:  Is it server-chosen variable-length?  Client-chosen?  Does it vary across the life of the connection?

Martin Thomson:  If you don’t have many connections, linkability gets to be easy anyway.  In those instances, having a minimum doesn’t make sense.  Prefer not to encode the length on the wire -- if you need it, encode the length in the CID.

Ted:  Disagree with using a single length in the handshake.  Once the server proposes something, it needs to match the length the client proposed.  Also, v1 doesn’t need to go crazy -- we just need to enable HTTP.  So long as the invariants aren’t affected, we can rev this.

Mike:  Do like packet number; both sides know the super-long CID, but don’t have to put the full CID in every packet.  If you only need the last byte, or four bytes, or eight bytes to disambiguate then you don’t put the full thing in your packet.

Christian:  We have client-chosen IDs that are used briefly, then server-chosen after that.  Don’t make client-chosen variable, but let the server specify the length that it needs.

Victor:  Make CID two bits instead of one, then allow 0/8/16-KeyPhase1/16-KeyPhase2.

Jana:  Hard to use fixed-size during the handshake, because ??? load balancers ???.  Also, prefer self-descriptive packets so load balancers don’t have to remember the size of a connection ID per connection before they’ve found the connection ID.

Ekr:  I think it’s clear we don’t have consensus -- let’s move on and let people work offline.

Mark:  Will you lead that design team?

Ekr:  Wasn’t volunteering, but… sure.

Roberto:  If we do variable-length, have to either grease it or use it.  Someone has to exercise different code points.  If we choose to revoke invariants for v2, which of these is easiest to live with?

Martin Zeeman:  If we have variable-length, I would like 0/4/8/16.  There’s value in a four-byte option.

Who wants to be in the group?  Ekr, MT, Ian, Jana, Roberto, and (nominated on his behalf) Brian Trammell.

### Connection Migration

Discussed in Singapore, asked for more specific proposal, so here it is.

Ekr:  What’s the “limit”?  (Slide 4)

Jana:  Probably the IW

Ekr:  This still presents an attack risk.

Martin Duke:  What’s the handover timeline?  If it’s long, we could be super-conservative in this case.

Jana:  That depends on the scenario.  If you’ve lost the previous path, you might not have much time.

(slide 5)

Subodh:  Is PATH_CHALLENGE the only thing in the packet?

Christian:  PING w/ data and PONG don’t need to be removed for this.

Mike:  But those were added for this purpose, so it makes sense to replace them.

Jana:  Can separate that out, if desired.

???: How does this map to New Connection IDs?

Jana:  Can’t enforce that the client uses them, but it can.

Nick:  Can the max packet size change?  That’s currently in transport params.

Jana:  Keeping it the same is preferable.

Mike Bishop:  We need to use both Connection IDs for a while if you’re probing one path and continuing to send data on the other.

Martin Thomson:  Yes, and you can do that without risking linkability if you encrypt the packet numbers.

Christian:  Have to use packet number encryption here.  Like it.  Bye, off to enjoy Maui!

Ekr:  Can you draw this?

Jana:  Yes.

(Drawing and clarification ensues; can someone put a photo here in the final version?)

Jana:  What are you confused about?

Ekr:  Everything.  Not clear how the slides map to the drawing.  This feels like redesigning ICE in a suboptimal way.

Jana:  Goal is that mutual validation happens on the side.

Roberto:  Are we talking about changing 5-tuples or Connection IDs?

Jana:  Migration of 5-tuples, which might use a new Connection ID as well.

Martin Zeeman:  Is there a reason the server would want to delay its path challenge?

Jana:  Probably not, but there are cases in which only the server wants to validate.

Roni:  Is simultaneous migration of both peers supported?

Martin Thomson:  Not the intent, but that’s possible in this design (I suppose).

???:  Is it possible to probe without committing?

Jana:  Yes, that’s the point.

Rui?:  What if you want to switch, but don’t have anything to send?

Eric:  You have to send some frame other than CHALLENGE, RESPONSE, or PADDING.  Use a PING, if nothing else.

Ekr:  You’ve described this as one side driving and the other side responding, but there’s a race condition where each side thinks it’s driving.

Eric:  If your old path dies, you might just switch and hope, without probing.  At some point, the client will switch; that triggers the server to probe.  The client can choose to probe first, and that’s fine too.

Subodh:  What’s the rationale for path validation when Wi-Fi is going away?  And if you wanted to switch, can’t you just start sending data?

Jana:  For the second, not a requirement; enables the client to probe without switching, but client can just switch if it wants / needs to.

Subodh:  But if I want to use a different path, wouldn’t I just start using it?

Eric:  You can, but you also have the option to find out about your options and make an informed choice.  You can also get all the proof of address ownership out of the way before I switch to avoid the limited congestion control.

Rui:  One of the purposes of PING is to maintain a NAT binding.  What if I want to keep a NAT binding open on a path I’m not using?  PING would switch over.

Jana/Eric:  You can keep doing PATH_CHALLENGE over and over, if you want to keep the binding open.

Roberto:  Are you sure this isn’t very close to full multipath?

Jana:  Yes, based on implementation experience.  There’s a lot to be done beyond this for true multipath support.

Martin Zeeman:  This should work in a P2P environment, provided you don’t have simultaneous NAT rebindings?

Ekr:  Probably, but you’d use ICE then, which handles this and more.

???:  After I switch, I’ll receive data on the old path; where do I ACK that?

Jana:  New path.

Igor:  Can you get a RESPONSE from a different IP than where you sent the CHALLENGE?  And what if a client wants to probe from all of many IPs -- is that an attack vector?

Jana:  Yes, you can do that, but you’ll trigger another CHALLENGE because it’s a server migration at that point.  And you can probe as many paths as you want, but the server will only commit to one.  If the server forgets that it validated one, it will just validate again.  Client can only actively use one address at a time.

(final slide)

Roberto:  If we ACK packets from the old path over the new path, we’re effectively lying and putting bad data into the new congestion controller.

Jana:  That’s true -- it will recover.

Martin Zeeman:  What if you’re congestion-limited from sending?  Can you still send PATH_CHALLENGE?

Jana:  Should obey the congestion controller -- the paths might have a shared bottleneck.

Ian:  Put some language about not triggering loss recovery from lost CHALLENGEs.  Also, better to rate-limit CHALLENGEs than congestion control.  The alternative is a new connection on the new path, so provided we’re less aggressive than a handshake, this is fine.

Martin Z.:  There’s already an exception for ACKs.

Jana:  Like the idea of using the handshake timer.

Roberto:  Multipath question again:  There’s the protocol piece and there’s the implementation piece.  This seems like 90% of the protocol side, and you’re just omitting the implementation piece.

Jana:  Is congestion control implementation or protocol?

Martin Thomson:  Interesting listening to people in the room start to design ICE from first principles.  ICE is 90 pages, and covers lots of stuff.  We asked you to generate a PR, and thanks.  But this is actually really big (I know you disagree), and trying to absorb this might slip our schedule.  This is complex, as evidenced by different people asking the same questions during the same discussion 20-30 minutes apart.  I’m suggesting we not do this in v1.

Jana:  I understand what ICE is after, and people who understand ICE or multipath will look at this and say it’s a special case of what they know.  But this is simpler and tries to answer only one piece of it.  We can take simpler answers for this scenario, and I have running code to prove it.  It might be hard to specify, but in terms of specification, it’s not nearly the size of ICE or multipath.

MT:  Still disagree.  There’s significantly more here than I’ve seen documented, even if it’s less than ICE, which I’ll admit.

Jana:  I think this lets endpoints build a not-amazingly-performant but sufficient migration solution.  It’s possible.

Mark:  v1 is focused only on HTTP; the only scenario which is covered by that milestone is NAT traversal (rebinding?).  Web browsers today can’t do this over TCP; we can clearly live without this.

Eric:  No, they do this with application-level semantics.

Mark:  But having it done by the transport is new.  H2/TCP just falls over in these cases, and keeping parity for v1 is okay.  The WG has decided its scope -- if we’re going to expand the scope in this direction, that needs explicit WG consensus to change.  I think it’s okay, provided we have guardrails to keep ourselves on schedule.

Jana:  The use cases are important -- I’ll argue that this is needed in a modern mobile world.

Ekr:  The argument is that the current spec doesn’t sufficiently handle NAT rebinding.

Jana:  The current draft doesn’t do probing separately from committing.

Ekr:  Okay, the functional answer is that it lets you make an informed choice rather than blindly leaping to a new connection.  So we’re already better than TCP, and we’re talking about getting better still.  I find myself currently unable to evaluate whether this is technically correct.  One possibility is that it’s generally fine and just needs refinement; the second is that it needs a pile of new work.  If it needs a pile of new work, I’m concerned about the time it would take.

Mark:  Can this be an extension?

Ted:  Maybe.

Roni:  This seems partial.  It works for servers, but you’ll need ICE for P2P.  We can extend this later, but we should understand that it’s not a full solution.

Tommy:  With H2 over MPTCP in hand-over mode, we already do this.  Lack of that capability in QUIC could block migrating our services to QUIC.

Eric:  This looks complicated because we took several use-cases and then tried to generalize into primitives from that.  The actual primitives are really simple.

Martin Thomson:  All the machinery is in place; I suspect we want to take on the substantive changes to the frames regardless.  Then we don’t have to worry about extensions.  Which is good, because we currently have no way to extend the protocol.  We should talk about that separately.  I still have all the reservations about the full solution that I had before.

Ian:  I won’t say that we have to do this, but if we don’t we’re in a weird situation where large portions of the WG want to do this and spin off a custom version.  That’s suboptimal.  Also, I’ve seen the code to do this -- there’s complexity, but most of that is due to our infrastructure and not the mechanism itself.  I think it’s sufficient for the use cases we’re targeting.  Text just needs to be improved (quite a bit).

Ted:  Agree with Martin that if we try to go all the way to ICE, the schedule would blow out.  How do we make sure that this useful step moves a step and not falling down a greased staircase into happy places full of clowns?  Keep the H2-like use cases in mind and strictly limit scope.

Martin Duke:  How much is this lifting out existing mechanisms from MPTCP and how much do we need to test and gather data?

Martin Thomson, Jana:  More like ICE than MPTCP.

Ian:  Also, we implemented this because the existing mechanism fails in odd ways.

Jana:  This has been implemented and deployed.  We have an existence proof and data.  GQUIC will maintain this, regardless of what the IETF does.

Hum:  Strong hum for “need to do this”; almost none for “bad idea”; strong hum for “don’t know yet.”

Mike:  Please read new QCRAM draft before tomorrow, so we can discuss adoption.




## Thursday Morning

*Scribe: Ted Hardie*

Thanks to Jonathan, our local host from RMIT; the venue has been fantastic.

Mark reviews Note Well.

Discussion of schedule for the day.

### Connection ID

Ekr reviews the summary he sent to the list on Connection ID (see email entitled “Read-out on offline connection ID discussion”).  Discussion of wasting bytes on the long header, with general view that it was sent rarely enough that this was not an issue.  Discussion of whether or not the length was an invariant or the encoding was an invariant.

Marteen is concerned about ossification, that there is a chance that the first player to go to IETF QUIC will end up setting up the expectation in middlebox.

Jana asks if we can grease this; Roberto describes a simple 0-padding implementation.

Marteen remains concerned that there is not enough incentive to make this happen.  It seems that there is a commitment from several implementers and deployers.  Jana says that you still can control the rate at which you grease, so that it is not significant to the deployment of the largest players.  Concerns about whether or not low rates will be effective; there are mechanisms to focus the tests so that it is obvious to peers (e.g. per AS focus).

Jana: the incentives are there from our side.

Folks still need a bit more detail; ekr will write a PR or email to describe in more detail.

Question about the details of the load balancing servers interaction with the servers; seems like default size or default minimums would solve this problem, even if they were published by the service.

Roni is concerned that this requires specific dependencies on action from the middle, and that this is contrary to the QUIC design goals.

Ekr and Roberto note that there are distinctions between the cooperating middleboxes and non-cooperating middleboxes.  This knowledge gets shared with cooperating servers, and that’s the intended state.  Greasing will help make sure that the non-cooperating middleboxes either fail earlier or do not set up incorrect assumptions.

Roni--you are expecting that they will do nothing; they will do something.

Roberto--we believe that we can prevent this ossification because large players will vary, either for greasing or as a standard practice.  There remains a risk of ossification to a small number of values, but this remains a problem.  Ted notes that if we always include the largest possible value as a one of the sizes used in greasing, then we can fall back to the largest available size.

Roni remains concerned that the firewall will attempt to use a heuristic analysis to determine what is well formed; they will act on that.

Roberto and Jana remind him that the purpose of the greasing is to provide data to that heuristic analysis of what the bounds should be; for those that do not follow that greasing in heuristic analysis will fall back to TCP.

Lars notes that the chairs would like to call consensus before London; don’t know how we are going to do it.  We could do a webex; the self-organizing design team will work through this.

Jana suggests a formal design would be useful.  It is clear that 8-byte fixed is not what people want.

Ekr will get the interested folk: Subodh, Kazuho, Ian, Brian, Marteen, to produce a proposal or set of proposals ASAP or by February 15.

Roni thinks it would be good to send to the mailing list a note about the creation of this design team.

Mark and Lars will take care of that.

### Header Compression

Mike reviews the draft, starting with Section 3.1.

Allowed instructions on the control streams manage inserts into the table.

Roberto describes how this could be extended, but does not argue that it should be updated at this stage.  This is comparable to HPACK’s performance in the lossless case and better than HPACK in the lossy case.

MT argues that this is the right target and that we would need a very strong case for making changes past this.

Christian is plus one; question to the room on adoption of QCRAM.

Dmitri notes that the design team had different proposals that were better than this, and did not have a single stream and so did not have this problem.  We should take stock now and understand that this has a structural problem; if you understand the structural problem and vote yes, okay, but I will vote no.

Clarifying question:  are you arguing for multiple control streams?

Dmitri: that is the obvious design alternative.  This is the kind of change that might well meet this bar of higher avoidance of HOL blocking.

Christian:  the better is the enemy of good.

Jana: we’ve been through this; we need something to allow us to move forward, and we can swap in new things are they are proved to be better.

Mike: Dmitri, I want to confirm that we see this as a starting point and we do see incremental improvements as coming.  We need to pick one and test what we can import into it.

Dmitri:  I’m not arguing for a Chimera, and I recognize that we can go forward from here.

Patrick argues that we have been discussing this for a long time and it is a blocker.  We need it to move forward.  Overwhelming preference for adopting the document now.

Mike:  this is the right time, and this is good enough (it’s in the ballpark and we can get to home base later).

### [Loss recovery draft ](https://github.com/quicwg/wg-materials/blob/master/interim-18-01/recovery.pdf)

Pacing is recommended, but without a specific approach.  Introduced MAX ACK delay, partially derived from proposal for TCP from Yuchung.  Witnessing MIN RTT is a little bit harder during ACK coalescing, but with a large enough sample set, there will occasionally be a quick turnaround ACK.

Christian believes that this is gambling.  Not clear that he objects to it on those grounds.

Martin Duke confirms that there may be RTT measurements that are lower than the MIN, but the current theory is that these are discarded.

Several folks expressed concerns about the max ack delay described on slide 3 (this is a reported value, not a direct measurement, so less subject to outlier situations where something is stuck in a buffer)

Question from Lars about whether adding this to v1 is required; it certainly seems to be an improvement, but the charter focuses us on delivering a standard congestion controller.  Can we limit ourselves to that for v1?  Ian, sure, but we need some reason to motivate the inclusion of Max Ack Delay, so that we can move forward with it; it could even say that it does nothing in v1.

Ian suggests that we complete the slides and then discuss further.

Discussion on whether or not we need a transport param for Max Ack Delay (pro’s and cons on slide 5).

Jana notes that it may not be knowable in User Space what the Max Ack Delay will be.

Ian: it’s an initial state, not the observation.

Patrick; so this is seeding Max Ack Delay?

Ian: yes, though you could also seed it with the default (25 millisecond delay).

Roberto:  I’m thinking about it being in the clear on the public internet--is it likely to be used on the public Internet?

Ian:  it should be generally available, since it may not be obvious in cloud situations whether you are traversing the public Internet.

Christian:  I’m concerned that this because something that adds to the fingerprinting capability, and that having a bunch of these parameters has privacy implications that we have not explored.  Subodh asks about the source of some of these constants--Ian replies that many come from the tail loss probe drafts.

Jana notes that knowing what MAX ACK DELAY is can help you to limit the number of packets sent for ACKs, but I agree with Christian that this explicit metric may not be necessary, given the additional data on timing availability in QUIC ACK packets.

Ian:  there are two requests to the working group, but I am not asking to make the decision today.  The last slide will describe the data I intend to gather.

Roberto:  there are two ways to express this:  as a factor of something else and as an absolute.  The latter is brittle.  Also a question on whether communicating this in crypto, whether the delay would be a problem.  If we had an Update Transport Params, we could throw it in there, in the protected part of the stream.  (There are issues there with other types of transport params, so introducing that type of update frame would have to have limits on what params could be included).

Praveen and Jana discussed some timing aspects of when the TLP would be fired off; for any learning mechanism, you have to encounter it once to get the data.

Ian:  I think saying that we have to have a TLP for every congestion control context, rather than having an early default, seems to be expensive.

Praveen: one another option is that the very first TLP would be very conservative, then subsequently snap to the current estimate.

Martin Duke:  I’m concerned that trusting a single TLP might be problematic.  Also, don’t personally plan to implement this, but wonder if this needs to be a transport param?

Patrick:  yeah, you could have this update be in a different frame.

Ian reiterates that he was hoping for feedback, no need to have a decision today.

Switching now to discussion of MinRTO (Issue #1017).  MT notes that we seem to be sending more packets to lower latency.

Twiddling thumbs at 2 it’s crazy but at microseconds it’s CRAZY!.  If we can do something about this we should.  On the other hand I’d like to see some safeguards around when we don’t know what the max is.

Christian(wearing the IETF “nerds in paradise shirt”): One of the differences it’s easy to measure in QUIC the spurious ACKs.

martinduke: How do you know it’s ack delay or RTT?

huitema: Even if you do not know you can make some conservative decision.  You can measure the n+1 but the time between that one and the next one was so and so that will give you an idea of the re-ordering.  Rather than getting all excited about max-delay, we should look at spurious RTO detection.

mD: what’s that impact on the spec?  20ms is crazy - can’t we change that?

ekinnear: Even if we are explicitly communicating it you might not be able to trust it.  Need to build in good detection.  I.e., let’s explicitly indicate it - even though we know it’s not perfectly accurate.

Jana: what do we need in v1?  Would love to nuke minRTO, but is afraid it will push us back.  Have the max dah and doh and worry about removing it later.  Leave the stuff needed to do the experiments.

Preveen: for safety we should avoid causing them in the first place.  As far as eliminating MinTO we need to be conservative.   Need to document some acking strategy.

Sub: sender wants to limit when the timer gets set.  Wants to help protect against DoS.

Q:Is this normative? A: Not sure about the feeling. (but don’t loose that lovin’ feelin’):
https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwiLy8z17vHYAhVBN5QKHSZ7AiEQyCkILTAA&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DuOnYY9Mw2Fg&usg=AOvVaw0oV2aK8I4BjC_6j6LDx6kt

Ian: Think we’ve set it up in such a way as to not abuse them.  Check my math.

MartinDuke: Be included to have a mechanism to be as good as cutting edge TCP.

Roberto: Agreed with MartinDuke.  If we attempted to provide this normative, then we’d need some hammer to enforce it.

MT: Let’s be reflective of reality.  Premature to put it in quick

Christian: Sometimes we need to repeat packets so it’s never a hard and fast rule to not resent.

Praveen: Christian, quite true.  I think what is important here is that normative behavior guides us here; we might want to provide knobs here that allows us to vary or experiment.  I think safety properties are things we ought to care about.  We should be careful about deviating from TCP, since it will be sharing networks with TCP for a long time.

PatrickM: What I have learned from TCP is that constants suck (consistently), and that we have the option here of a much better feedback loop, and we should take advantage of that.

Jana:  QUIC has a bunch of signalling that we do not have in TCP.  There is a proposal to include the RTO in TCP and we can consider it for QUIC as well.  I’m arguing for including these constants in v1 only to make sure that we have a baseline that we can experiment against.  This is a sender-side only change, so we can adjust as we get more data.

Ian: last slide is Plan:  Gather Data (Slide 7)

Martin: are you going to do this in both data center and open Internet?  Ian: just open Internet.

Subodh: if you can write this up, we would like to run these tests as well.

Jana:  Going back to what we want for v1--we don’t have to block on any of these for v1, except for 2.  We need a mechanism to carry the data for MAX ACK DELAY (without that, can’t run the experiment).

Ian: should I spend cycles on coming up with a way to carry that without it being in the clear?  Feedback on that desired.

Praveen: MinRTO is already being used for TCP, despite it not being in the RFCs.  Other experiments: ER vs. non-ER.  One TLP vs. two TLP would also be useful to gather data on.

IAN: zero, one, or two could be tested.

Ian:  I’m done, should I come up with a way to communicate MAX ACK DELAY outside the clear?

PM: Yes.  Martin Duke: what’s the tradeoff here?

Ian: If this is not v1, then I won’t work on it.  Fine as an extension, if we have extensions, and we need something to test extensions with.

Ian: Update Transport Params is my preference, but I have other uses for that.

Break for lunch, then talk about abstractions and next steps.

## Thursday Afternoon

*Scribe: Sean Turner*

### Abstractions

Slide 3 (connections)

Christian: You introduce connection control but you didn’t mention paths - Yes.

Lars: Is 1st bullet how an implementation can identify a packet? Or is it how a server identifies them?

Jana: Echo this point separation between entity that has keys and not.

Streams

Ordered but not not necessarily in-order; to make a distinction: I have five packets worth of data.  These are each one byte per stream - receive 2-5 but not 1.  May interpret those without having received 1.

Ekr: agrees but it makes a little confusing because we offer reliability for the entire stream.  Explains difference with RTP.

Jeff: There’s actually in QUIC that requires an endpoint to retransmit on a stream.  The protocol doesn’t require to retransmit everything.

MT: It’s delivered in order.

Ekr: it does talk about retransmission.

Jana: The spirit of where the draft was to expect this to be in order byte streams.  Does this need to be a requirement?

Jana: In response to Jeff, we expected that they would. (?)

Ted: It might actually help to say sequential.  Properties of QUIC streams not HTTP over QUIC streams.  Right now it’s there, but it’s not there for the current application.

Roberto: Might be true for google, but would like to maybe make it true later.

Mike: Your example triggered some confusion with retransmission and …  Agrees it’s an API choice.  I think the 1st byte gets retransmitted unless you say you’re not going to.

Ekr: Spec prohibits both of these.  I.e., spec requires in-order delivery and filling in holes.

Jana: It’s easy to specify not doing in-order byte stream - it’s one sentence but it’s hard to implement.

Roberto: It’s possible that it’s not that hard.

Jana: We need to think about other considerations in addition to the specification writing - without explicit signalling of delivery model being used - it makes it tricker for an application to use.  Application can’t assume a particular behavior.

Roberto: If there’s two APIs, it’ll pick one - if there’s only one you get one.

Jana: Being explicit in specification forces designers to to be explicit.

MartinDuke: So what’s the point here.

Mnot: THis is the in-formal design team response - no decision.

MartinDuke: How does this differ from partial reliability

Roberto: They are not the same but they are complimentary.

MartinDuke: Partial reliability is in not in v1.

Roberto: If we just strike in-order delivery then that’s all we really need.

Jeff: All I can tell from a spec was that it was in-order.  A better conception is do I provide file or stream access.

Ian: Was going to say that he agrees with abstraction; however, in the quic transport doc I don’t want to get in partial reliability.  It would be huge time sink.

Eric: I like Ian’s idea of requiring what must be there.  Interesting to explore, but let’s not preclude them.

Roni: Does this mean interleaved.

Roberto: No guarantee that you’ll get it the way it was sent.

Alan: Agrees that we’d like to be able to make use of data before it all gets there.

Igor: Partial reliability mostly about knowing what not to re-send.

Christian: Introduces a new abstraction.

MartinDuke: API must allow you be sent to the same proxy.

Roberto: Need protocol mechanism to support this.

MikeB: What do you mean HTTP is not reliable.

MT: If you get a response to a request then something has happened.

Grouping: A request from a sender that all streams in the group terminate at the same L7 location?

Roberto: Thinks this goes in the QUIC Layer.

MikeB: Disagrees.  If it’s an L7 concept maybe it should stay there.

Roberto: Let’s talk about compression: another stream would allow ….

Alan: to clarify - is there another mapping at the H3 layer?

MartinD: in the H2 of TCP case is there any grouping? No but it was in SPDY4.

Roberto: Some protocols are doing things sub-optimally.

Roni: Any time syncing.

Roberto: no.

LEIF: Is this a client directed thing.

Roberto: It can’t it is merely a request.

MartinD: If you’re getting less compression efficiency then this is the client’s problem.

Ian: Interesting and it feels like an interesting feature request.

Mike: What Ian said.  But, I get ¾ of what you’re after and it could be reframed would be to say you can multiple connections which share the same congestion control.

Christian: +1 (and others)

MT: needs more work

Roberto: this is definitely a V2 feature…

Mnot: Have discussions - have breakouts -

Jana: This is a useful conversation.

Roberto: We’ll take grouping out of the abstractions draft!

Eric: Have a similar use case - similar to push promise.

MT: In-order delivery there is a PR.

Mnot: What’s the next step?

Roberto: Having a wider discussion that does not stop slow or stop 1 would be nice to be done very quickly after v1.

Lars: This is important in that it explains something about QUIC.  Some of this should go in the
Applicability statement.

Jana: I think it’s nice to think about this but none of it is necessary for v1.

Roberto: THere’s a PR in for the on v1 change.

### Extensions

Extensions are a pressure release value.  Only differs from HTTP2 idea because it’s bigger!

If you need the extension to be reliable - you gotta make it so.

Ekr: only allocated 00-17?  We have 240 spaces free? What’s the point about ignoring vs reliability?  Code point space is too big.

Ian: Interesting to have, but a little grumpy about providing it without having a mechanism to negotiate it.  Don’t want to add it until we have a negotiation mechanism.

Mnot: do we need something.

Ekr: dissents - most everybody says you need this.

Jana: Negotiation can be handled.

Jana: Space can used for experimentation so we need to have some way to note what numbers they’re using.

Lars: I would like this so we can get rid of all the block frames.  You can put all of the block frame info ….

Ekr: Huh

Patrick: Flashback!

Victor: Have an idea for a extension that is similar but somewhat different …. It’s more negotiation-oriented.

Roberto: can we just have something!

Mnot: when do we need it?

MT: We need it …

Mnot: could we adopt this and admit it’s not perfect.

Christian: Already provided feedback but basically it’s okay except for the assignment mechanism.

Ted: Look at the IAB RFC to do an extension!  Treating the extension differently than the base protocol could be dangerous.

Mnot: we’re not designing it today, so it’s on the front burner.

HUM: Who thinks we should include it now (after some discussion on this)

Rough consensus (to be confirmed on list): include it.

### 3rd Implementation Draft

Don’t change milestones …

r/draft-08 and TLS 1.3 -22/draft-09 and TLS 1.3 -23

Should add HTTP “non-sense”?

This of these features as table stakes and advanced.

ship -09 by Monday

Add HTTP2 as advanced as those might do it later.

Do virtual interop day in Feb and do the 4th interop in person.

Week of Feb 26th for virtual

Patrick edit Wiki!

1st week of June for Interim:

Locations: XXX

Weeks: one of the 1st two weeks of June


