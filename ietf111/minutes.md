# QUIC at IETF 111

[Agenda](https://github.com/quicwg/wg-materials/blob/main/ietf111/agenda.md)
Scribes: Robin Marx, Watson Ladd
Chairs: 🪑🪑🪑 (Lucas Pardue, Matt Joras, Lars Eggert)

Note: especially near the end, notes don't cover _all_ points made by all speakers. Watch videos for full content. 

## Administrivia - 5 min total

* Blue sheets
  * Meetecho does the bluesheets
* NOTE WELL
* Agenda bashing

**Lars**: 2 things. 1) I hope to not be chair of QUIC anymore as soon as this meeting ends :) 2) we don't have interop report today, but 1 thing: we need sponsored hosting for the QUIC interop runner tools (or more disk space/github credits etc.)


## Hackathon / Interop Report

None

## WG Items

### 10 min - Open issues, updates to [manageability](https://datatracker.ietf.org/doc/draft-ietf-quic-manageability/) and [applicability](https://datatracker.ietf.org/doc/draft-ietf-quic-applicability/). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf111/ops-drafts.pdf)- *Mirja Kühlewind*

**Mirja**: Docs are basically ready to go. We had 2 WGLC's and did bunch of updates after each. Will talk through last ones now and 1 new thing.

**Mirja**: Applicability: 3 PRs which actually changed content. 1) h3 ALPN token to clarify what we're doing now. 2) more guidance on use of DSCP. Not really content change but clarification. 3) ACK frequency guidance now included 

**Mirja**: Manageability: clarification on PMTUD + SMI parsing

**Mirja**: New PR #392 on uses of source ports (see also discussion on list). Questions: Is this specific to QUIC and should we add it? Should we add something to manageability to also avoid these ports? 

**Mark Notthingham (mnot)**: We should do this

**Martin Thomson (MT)**: What is likely to happen is that this port will be selected and they won't work. Not because of any high principled position, but just because some people have to block these ports due to nature of services. Will happen. Documenting them might help, but never provide guarantees. Not sure we need to add to manageability as well though.

**Lars Eggert**: (as individual) agree with Mark and Martin. Lots of UDP in the past but even more QUIC in the future. Documenting this seems fine. If we want to work on broader document later is fine too. Could say: IETF might update this guidance in the future. 

**mnot**: Is strictly speaking general guidance, but directly applicable to QUIC. Whether or not something happens elsewhere isn't clear yet. Raised in tsvarea. Some folks seem amenable, one is not, don't know what will happen. Fine with MT's suggestion to broaden scope a bit. 

**Mirja**: do you plan to work on a broader document? 

**mnot**: really rather not :) but if need be...

**Jana Iyengar**: Put this in update to RFC 8085 maybe. If that's in there, maybe not having to do this in QUIC. Should go in 8085 anyway

**Roberto Peon**: We should do it in the context of this wg because QUIC will def run into these problems. If scope is broader: wonderful. 

**Mirja**: Issue was raised on mailing list about privacy concerns where server might link client via connections. Could have been discussed in transport doc, but isn't in there. Could add to applicability. No PR yet, if you want this: add it. **crickets**

**MT**: Think this is pretty clear, don't need to repeat it

**Christian Huitema**: would be good to at least have a notice of that. Discussion in transport doc is very brief. Comments from Stephane Bortzmeyer should be document a bit more explicit than just in transport.

**Mirja**: This is mainly about TLS, but we indeed don't mention this specific issue with migration. Could indeed add to applicability. Unless Christian wants to do so, I'll open PR and close loop in a few days.

**MT (in chat)**: We have enough text on this in TLS, not needed here (lots of +1's on this)


### 10 min - Open issues, updates to [DATAGRAM](https://datatracker.ietf.org/doc/draft-ietf-quic-datagram/). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf111/datagram.pdf) - *Tommy Pauly*

**Tommy Pauly**: _reads from the slides mainly_

**Tommy Pauly**: Issue 35: believe we don't need this in this draft, but want to get opinions. Answer the question: what should implementation do if it receives datagrams and doesn't know what it means. Imo: similar to receiving stream data where you don't know the application layer protocol... this is why we have H3 datagrams. 

**Lucas Pardue**: (as individual): say in applicability that any mechanism in QUIC that's designed to carry app data might have this kind of problem. Don't mention specific extensions/mechanisms. 

**Mirja**: We have section about datagrams in applicability, maybe add this there.

**Tommy**: so let's move it over to there then

**Jana**: IF compare datagrams with STREAM frames. Different semantics, but offer particular service to application. Don't describe app that uses STREAMS, so don't need to describe apps using datagrams either. If app doesn't know what to do, shouldn't be sending. It's for app to handle, not for transport to specify. Don't think there's anything we need to do here. 

**MT**: Please don't do anything. But please: ship datagram!

**Kazuho**: Assuming we add something somewhere, nto sure applicability is sufficient. We should have ref to [unclear] to say what implementers SHOULD do. Delegating responsibility to applications using datagram frames is correct. Then, requirements for those should be in datagrams document.

**Roberto**: Interesting thing about dgrams are that they are almost entirely semantics-free. Only 2 problems: routing to the right place and doing business logic. Talking about former makes sense, latter is futile. Enough to say 'this is what you SHOULD do' but nothing more. 

**Tommy**: General sense: nothing particular to say here. Probably close issue, confirm it on github. 


### 10 min - Open issues, updates to [version negotiation](https://datatracker.ietf.org/doc/draft-ietf-quic-version-negotiation/). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf111/version-negotiation.pdf) - *David Schinazi*

**David Schinazi**: _Doesn't promise not to abuse control_

**David**: Today: main changes in last update. Simplified proposal courtesy of MT's input.

**David**: Be able to do VN without using an RTT is important. 

**David**: Two diffeerent kinds of VN. 1) incompatible: works between any 2 QUIC versions. incurs 1 RTT overhead 2) Compatible: requires 2 versions to be compatible. Server replies immediately with compatible version. 

**David**: what is "compatible"? Version A can be converted to B. Not necessarily bijective, not necessary to have 100% compatibility (e.g., ignore new frame type)

**David**: Handshake Version Information: invariant between versions. Exchanged in handshake with integrity protection --> use transport parameters. Prevents on-path downgrade attack. Simple format: chosen version + other versions (client = compatible versions, server = supported versions). 

**David**: A SLIDE IN THE SLIDES

**David**: What does server support mean? Conceptually simple, but can lead to connections failing. E.g., remove a version between time you sent a VN reply and client reconnects. Solved with 3-step algorithm: separates versions in 3 sets: 1) Accepted versions 2) Offered versions 3) Fully deployed versions (mainly downgrade prevention). Note: Google deployment doesn't really care about these failures, won't deploy this. Is a SHOULD in the spec.

**David**: Downgrade protection is easy. 

**David**: 1 issue #43: order client versions by preference. What do people think?

**Roberto**: server's gonna do what server's gonna do. Even if you require it, can't enforce. Not needed.

**Jana**: Agree with Roberto. But this is info from client to server, so server can do what it does slightly better perhaps. Could be useful if not much cost. Worth to put it in there.

**EKR**: concur with Jana. No effort, so we have to do it.

**MT**: Then have to repeat the selected version, no (because not always most preferred version)? That gets awkward? So do nothing, let server do what it's gonna do. 

**David**: Chairs, let's do a HUM? 

**Jana**: Clarification question. Not sure I understood MT's comment?

**David**: e.g., QUIC v2 comes out and is compatible with v1. But when v2 comes out, clients supports 1 and 2, and prefers 2. But few servers that support 2 and more that support 1. So reasonable for client to use 1 first even though it prefers 2, to improve compat with as many servers as possible. As such, need to encode in client's compatible version list where the preferred one is exactly (so need to offer 1, then repeat in list after 2, to make clear 2 is preferred). Without ordering, you cna just say: I chose one, but compatible with 2. 

**Matt Joras**: Let's do show of hands instead of hum

**Poll results**: 39 participants: 30 prefer ordering, 9 prefer not ordering (only about 25% of particants, 154 total in the room)

**David**: so propose to keep ordering in the draft as it is today. 

**Lucas**: let's do that. Keep it in issue, take it to the list for consensus. 


### 10 min - Open issues, updates to [QUIC-LB](https://datatracker.ietf.org/doc/draft-ietf-quic-load-balancers). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf111/quic-lb.pdf) - *Martin Duke*

**Martin Duke (MD)**: Kind of stuck in some ways. Main issue is lack of implementations... mainly servers. Partly because address migration is low on people's priority list and without that the LB part doesn't matter. 

**MD**: New use cases come up though that fit this framework. 

**MD**: 3 possible paths forward. 1) let MD grind through and get it done 2) wait for implementations 3) split retry service from LB service

**MD**: Example new use case: Stateless Reset offload. If a server goes down and loses state and receives unknown packets, can send reset. Offloader that knows server is down can send this on its behalf. Personally don't really like this use case, but open for feedback.

**MD**: not much enthousiasm. Feel this will remain stuck for a while. Can people indicate if they plan to do migration soon maybe?

**Christian**: if server ID is encoded in connid: some possibility that resumption goes back to same server in the pool. If that's true, you can make a lot of assumptions. E.g., not having to encode the tickets using STEK. Wonder if there is interest in adding something like that.

**MD**: most straightforward: re-use CIDs from previous connection when you re-connect. 

**Christian**: It's easy, but can server assume enough clients will do it so they can go to a STEK-less deployment? 

**MD**: Don't have strong feelings about one or the other. Good example of yet another use case that keeps expanding this while we're not getting closer to completion. 

**Roberto**: solving session definition problem? IDs we use to define connection session. Then this can continue trhough some state changes. Sadly, don't see a lot of interest in folks here in solving that problme right now. Mainly because problem is larger than what we're doing now, and we're not discussing that problem.

### 20 min - Open issues, updates to qlog. [Main schema](https://datatracker.ietf.org/doc/html/draft-ietf-quic-qlog-main-schema), [QUIC event schema](https://datatracker.ietf.org/doc/html/draft-ietf-quic-qlog-quic-events), [HTTP/3 and QPACK event schema](https://quicwg.github.io/qlog/#go.draft-ietf-quic-qlog-h3-events.html). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf111/qlog.pdf) - *Robin Marx*

**Robin Marx(RM)** The philosophical update. Adopted, 3 docs. Main schema (protocol agnostic), two docs one for quic, other for http3/qpack

**RM** Distant future additional docs with new schema to keep it all working. Event schema main thing
**RM** Metadata, list of events. Timestamp, event type, structured data based on event. Most of the protocol docs look like they define events you should log and what they should look like. From schema many serializations into presentation. On left simple JSON default

**RM** Secondary format: newline delimited JSON. Work around issue of needed final deliminator in streaming implementation.

**RM** What do we standardize and why? Add, keep, change. Serialization format
**RM** JSON picked for flexibility and well supported in most environments. Easy to make tools. Don't need tools, text works
**RM** Obvious downsides: performance, NDJSON not supported anywehre, alternatives: CBOR, Pcaps, Protobufs, flattbufs, etc.
**RM** bikeshed for many years! So let's not
**RM** What is the problem we're trying to solve? Interoperable logging for reusable tools or issue no one can log efficiently? Clear that I think its the first and not the second. Most of you know how to do it efficiently. Unfair statement. Chosing one doesn't preclude the other. Can make tools on optimized format. More optimized, more difficult to make reuseable tooling. Other arguments against complexity. Some very scalable implementations show JSON can happen at large scale. Not optimal but workable. Some do intermediate binary to qlog. QLOG as lingua franca for converters.

**RM** Think people will continue doing it. JSON can be compressed. Concrete proposal: ok, stick with JSON. Going to have something custom for streaming. 
**RM** What events? Three categories. One close to wire image; what goes in and out. Other category for internal state changes like congestion. Third category: custom, implementation defined events. Can even display events they don't know. Would think its enough. But found some nuaunces. Packets ACKed event. Same as logging ACKed frame? NO! Duplicate ACKs. Only newly acked ones in Packets Acked event. And then frames processed event. Log frame without headers as they come in. Separte header payload processing or aggregate frames into single event.
**RM** Ties into into point of Mark Nottingham. Looks more like surfacing implementation details rather than semantics and events of protocol. Very recently weirder proposal where same exact frame logged? Can't I template and log only changed. Personally not a biggest fan. understand where question comes from. All of these useful, but can't support them all. Tools and implementors complicated. What events are being used for visualizing. need guideline to limit event definitions.
**RM** Proposal, log what's in and out, only deviate for events like congestion control. Can deviated when it makes sense, e.g. packets ACK, qpack log only wire image, not whats going in. Would like higher level. Would get rid of things like frames_processed. Could have some implementations have trouble and need converter. But people were doing it already.
**RM** JSON, custom streaming. Reduce even number
**RM** two main issuues, many more open. feedback welcome. But these two things will make a lot easier to solve.
**Lucas (with hat)** Newly adopted, implemented widely, quite a few issues to burn through. Rough consensus sooner, easer to move. RFC 7464 as streaming JSON. Worth looking up.
**RM** 
**Jana Iyegar** Always thought interop between producers and consuumers which are tools, pcap-NG of quic. Where produced directly or not, not a problem. Go through the format. Like the principles, lots of sense. Close to wire. Other things useful, but how many care. Have to balance. To me QLOG intermeiary. direct production not an issue, can use a converter.
**Paul Hoffman** A lurker, care only about QLOG. Agree philosophy matters. Gets mixed up: logging or debugging. Many choices mostly for debugging, can expend space or lose thing. Needs to determine this, as logging is more space efficent, even sampled. Gazillions a moment. Once answered some will fall out. Names like this, except this way: ok for debugging, not for logging format. Keeping as JSON great. Expect binary format that's smaller. CBOR would work. Doesn't have to be main format. As tooling comes up obvious platform. Get it. Can't compress on fly. Both can be helped. Willing to participate. Would like to know which.
**RM** Would like that obviously more debugging, not logging. Sampled seems to hold up with current. Not clear if comment was abot JSON or verbosity.
**Watson** Main interest debugging. Comparing important. Size doesn't matter. 
**Waton Ladd**: keeping close to wire format is most important than size and speed. 
**Matt Joras** Schema and serialization separate. Then down the line can change. On serialization, careful about premature compression. Compression algorithms good, file formats bad. "compression" in quic. Streaming and files different. The people who spend their lives doing that are good at it. we just log straight JSON from quic. Works! Could be faster and smaller, but we just compress it and good enough. Standard interchange format for JSON where we should go. Most agile way for tools.
**JI** Human readable important. I think its good, don't need other formats
**Lucas** Getting consensus will take on list. JSON doesn't stop other things


### 20 min  Open issues, updates to [ack frequency](https://github.com/quicwg/ack-frequency). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf111/ack-frequency.pdf)- *Ian Swett*

**MT**: don't think I can implement #22 (1-RTT only) without major changes in codebase. We do have default value for max_ack_delay in case it's absent, would prevent it from being major problems. Don't see roblem with having people send it in 0-RTT. Have to remember, but not big problem.

**Ian**: persistence is not a big problem. Concern was that misconfiguration risk across different locations is higher. 

**Jana**: MT, could you explian more about why making it 1-RTT only would be problem? 

**MT**: a lot of frames that can only be sent in 1-RTT, agreed (e.g., no ACK in 0-RTT, doesn't make sense). But none explicitly _forbid_ 0-RTT sending. So our implementation simply divide by PN space, not making diff between 0-RTT and 1-RTT. Very difficult to plumb this in now. 

**Jana**: We couldn't really find a clear answer for this tbh. Anything the wg wants to go for is probably fine. You could hit a different server farm if you use 0-RTT and minRTT might be different then. 

**Ian**: note that there are some other gotcha's not on the slide, so would appreciate another few people looking into this on the issue. Will follow up on the list.

**Gorry Fairhurst**: Are we specifiying when to act on it in 0-RTT or simply to exchange it and then act on it when the 0-RTT completes (and all params,etc have been exchanged)?

**Ian**: [unclear]. Taking action on it can be a problem. Race condition potentially whether you apply Transport parameters or ACK frequency frame first. 

**Jana**: So when you receive ACK frequency frame later because of packet drop? 

**Ian**: Or TPs are applied later because you put 0-RTT in local buffer and apply TP later due to handshake offload etc. so you get ACK freq frame processed before TPs. 

**Jana**: Should then take this back to the issue and hash it out there. 

**Kazuho**: #34: having new frame for this is good idea. Doesn't need to be 1-byte. Only use this frame in tail which typically always have more than 1 byte available.  

**Ian**: true, but e.g., in PTO you wouldn't have the byte available. 

**Magnus Westerlund**: Is reordering strictly re-ordering? Skipping ACK, actual packet lost, reordering all covered by this? Do you actually want to differentiate things when ACKing? e.g., reordering is ok to skip, but not ACK skipping? Is there even a way of capturing the difference here?

**Ian**: intent was to align with RFC 9000 to exchange what "in order" means. I'm not sure I understand all the use case for this ignore_order flag, so if others could clarify, that would be helpful.

**Christian**: We don't so much send ACKs after packets than after flights of packets. Many implementations that just drain receive queue, and only then send an ACK. How do you reconcile that with idea that you should stop what you're doing and send an ACK?

**Ian**: great question about how this is defined. Intention: this byte elicits an immediate ACK as in "ASAP", not "undo other optimizations". If that's not the correct behaviour, people should speak up. 

**Christian**: But if you don't specify that, spec because fuzzy, is it still useful?

**Jana**: think we can be reasonable without being overly specific. Think it's a reasonable thing we can describe. Can we get higher order direction out of this? 

**Matt**: seems like most people are in favor of option 2, 1-byte frame (or semi-PING frame, see jabber). Doing option 1 (header bit) is probably not realistic. 

**Jana**: will go ahead with option 2. If strong disagreement, please comment on issue.


### 10 min - Open issues, updates to [Greasing the QUIC bit](https://datatracker.ietf.org/doc/html/draft-ietf-quic-bit-grease). - *Martin Thomson*

_no slides_

**MT**: nothing to say. People have implemented this. Haven't needed to touch this since put the codepoints in the doc. Ready to go for WGLC imo. 

**Lucas**: agree it's ready for WGLC


## Other (aka "As Time Permits")


* QUIC versions, ALPN, version++. [slides](https://github.com/quicwg/wg-materials/blob/main/ietf111/quic-version-stuff.pdf) - *Martin Duke*

**MD**: do we want to have v2 to exercise VN mechanism? 

**MD**: should new version numbers be incremental or random? 

**MD**: most interesting thing is ALPN here. How do we keep track of which QUIC versions can support which applications? 4 alternatives; (1) Couple ALPN to underlying QUIC version? Is clean, can use alt-svc. However, if many different QUIC version, you get broad matrix that's difficult to track, and applications that provide the ALPN have to know about QUIC versions.

**MD**: Other proposals; (2) New versions can use the same ALPN but have to formally "update" the application draf -- might fill up the first page of application drafts.  (3) Extend an IANA registry (either ALPN or QUIC Versions) to keep track of which ALPNs or versions are supported. (4) Just put text in each new version or application draft covering compatibility with known applications or versions: this has the least bureaucracy, but hard to do the forensics on what supports what.

**MD**: I would prefer (3) or (4)

**Mike Bishop**: Previously did decide to tie ALPN to specific QUIC versions. If we want to change that, really don't like enumerating things that are allowed to used QUIC in the QUIC registry (so not option 3B). [missed a point here]. Or option 4 can also be workable. Main point: does QUIC provide features that the application needs? Maybe time to byte the bullet and explore how to write that formally. 

**MD**: have tried to find the consensus on tying ALPN to QUIC version, but couldn't find... not sure that's entirely true. 

**Mike**: [quotes part from H3 draft]. 

**MD**: If QUIC v2 exists and has current language ("yes you can use h3 with this as well"), then that's consistent with existing text. 

**MT**: in favor of proposal 4

**Christian**: QUIC v2 that says that it works for "pretty much all apps that use v1". If we don't do that in the spec, if we have to get approval of each application group before v2 can be deployed, we have a massive ossification problem. So we must not be in that position. 

**David Schinazi**: if we don't do anything, as a client, there are multiple mechanisms to tell me what ALPNs server supports (alt-svc, DNS HTTPS rr). However, need to send a flight to server to discover which QUIC versions we support. Sounds like it might add an RTT if QUIC versions aren't tied to ALPN...

**MD**: definitely incurs more VN if ALPN isn't tightly coupled to QUIC versions

**David**: currently only have handful of QUIC versions and handful of apps, but still would like to fix this: 1 RTT is too much to be wasting.

**MD**: so should QUIC v2 draft define new ALPN for h3?

**David**: that, or define QUIC versions in alt-svc (had that before), but indeed: defining new ALPN is best here

**MD**: ok. Any enthousiasm to try and adopt this placeholder v2 to experiment? _crickets_ ... ok, hearing none

**Lucas**: wouldn't take lack of response too hard now. Let's try it a bit later down the line. Out of time now. 

* Updates to [0-RTT-BDP](https://github.com/NicoKos/QUIC_HIGH_BDP/tree/master/ietf-document/draft-0rtt-bdp). [slides](https://github.com/NicoKos/wg-materials/blob/main/ietf111/0rtt-bdp.pdf). - *Nicolas Kuhn*

Out of time

* Multi-path QUIC extension and experiments. [slides](https://github.com/quicwg/wg-materials/blob/main/ietf111/multipath-experiments.pdf)  - *Yanmei Liu/Yunfei Ma*

Out of time


## Planning & Wrap up

**Lucas**: Lars is now no longer a chair... he looks happy not sad though?

**Zaheduzzaman Sarker**: Lars is given more time now to do his IETF chair work. We all appreciate all the work you did here and thank you for your time. If we need you in the future, we will bring you back!

**Lars**: No you won't! This was the most fun I've had with IETF standardization, so thanks everyone! 



