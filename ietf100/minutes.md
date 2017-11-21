# QUIC WG Meeting Minutes - IETF 100 Singapore

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Tuesday, 14 November 2017](#tuesday-14-november-2017)
  - [Hackathon / Interop Report](#hackathon--interop-report)
  - [QUIC Invariants](#quic-invariants)
  - [Working Group Status and Scope](#working-group-status-and-scope)
  - [Spin-Bit Evaluation Design Team Report](#spin-bit-evaluation-design-team-report)
- [Wednesday, 15 November 2017](#wednesday-15-november-2017)
  - [Editors' Update](#editors-update)
  - [Loss Recovery](#loss-recovery)
  - [Connection Migration](#connection-migration)
  - [Third Implementation Draft](#third-implementation-draft)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Tuesday, 14 November 2017

_13:30-15:30    Afternoon session I, Padang_


### Hackathon / Interop Report

ekr: lots of green here. handshake works. first gap: would be useful to have clear standards for what success is, how many channels, what is close. into melbourne, would be good to have relatively detailed  second gap: lack of clear continuous integration / continuous testing. have talked with lars about doing some CI for melbourne. talk to me if you'd like to help.

### QUIC Invariants

Martin Thomson [presentation](https://datatracker.ietf.org/meeting/100/materials/slides-100-quic-sessa-invariants/)

ekr: Clarifying question: major version not draft version.

mt: yep, point is to agree on principles. note that we don't get to change our minds about this particular concept. hope that people will do experiments at reasonable scale before pub of RFCs to test that these things...

BT: This is the right definition.  Noting there's a lot of stuff hiding behind routing of QUIC packets independent of version.

IS: Excellent!  There' also a little behind A.  Stuff is going to ossify on the handshake. Short form packets might be changeable. Long form packets not so much.

MT: There are some ways to protect against ossification.

Emile: Multipath?

MT: Interesting. Haven't talked much about it the wire image looks like. it's part of (b). if that means we have to talk about multipath....?  Maybe we can differ?

Emile: Routing will be independent of version?

MT: That's the hope

Emile: Multipath changes routing.

Phillip Tiesel: There might be ways to do this with the current wire image -- there are MP drafts whose authors know how to do this.

MB (now at Akamai): even though it might not be part of b stateless reset is there.

MT: stateless reset is fun.  Need to do some work on this.

BJ: This is the right level of abstraction.

Roni Even: Will this cause more limitation on what you can do in future versions?

MT: Absolutely. We have to gt this almost right.

RE: ?

MT: Version field loc necessary for nego. We can move other things around though.

RE: How are we going to work with things that version independent?

MT: As long as VN works across versions. Once you have a version do what you want.

RE: The question is do we require that if we support N then I have to do N+!?

MT: Nope.

Lars: Martin means DC/load balancer routing. You mean in the network

RE: ah okay!

BT: I think that Lars' qualification is a modification? routing of quic packets is where the go?  Saying they only care about boundaries is bad way to think about.

MT: we need to make the sure the intended destination there may be version dependent behavior beyond the routing... but yes.

CP: What you just said I absolutely agree with. Lars' clarification does not clarify

MT: Let's call it an example.

JL: This all outside of the encryption.

MT: Yep

JL:  None of this is crypto anyway. Encrypted means not invariant.

MT: The invariants we have are smaller than the things that are not encrypted. Can we move on?

Igor: Routing should be done by IP and UDP headers only?

MT: It should be possible for someone to mark a packet with invariant bits.  ConnectionID is definitely part!

Jana: Brief response. If you use CID for V1, you can continue using them in 4,5,6. Independent from can or must use IP.

Gabriel Montenegro:  ConnectionIDs are neither A nor B.  Is another invariant what we'll let the middleboxes see.

MT: Yes

ekr: routing in DC, routing by third parties. For DC, CID can move around. For NAT, not the case. Maybe inconvenient to look up version in DC. But not impossible. Thing reqd for cooperating people, and things for non-cooperating people. A is probable cooperating-only. B covers both coop and non-coop

MT: not sure we examined it from this perspective.

ekr: Version negotiation is a practical matter, once we agree on that, no change. That's basic principle/invariant.

*moving to slide #3*

BS: Include MTU?

MT: that is not guaranteed.

BT: Sematics between codepoints 1-5 are going to be invariants.

MT: We have not made that commitment?

BT: It will be made for you.  It seems impractical.

IS: WE're going to be stuck with 1-5.  Is it worth trying to fix that?

ekr: we make them all zero and stuff them in...so it's not a big deal.

BT: We put breakpoints in where we want them or they will be put in for us, and we'll have to find out where they are later.

Jana: The point of this discussion is what won't change.  Other things might ossify.  There might be more things we'll agree to not change in the future.

RE: Just the location - not the semantics, etc.

MT: Yep, we commit to no semantics, semantics can change.

mnot: constrain to what our intent is, not what's in crypto or what might ossify...

*Moving to slide #4*

CP: Would like to talk about formulation of the problem. How do we mux quic an RTP is not right. Problem I'm raising is how to we run QUIC P2P, which means we need to demux STUN. RTP would be nice. STUN is more important. That's a different problem.

MT: Okay that's fair and a better way to approach it. It would be disruptive to put STUN in QUIC.

*Moving to slide #5*

*Moving to slide #6*

BA: question wa about option 2... option one sucks.

*Moving to slide #7*

CP: That's one option. Another option is to pick some subset, and say for example we only care to not collide with STUN

Roni: We have 8 bits in first byte. Not clear than one byte is enough, maybe we should extend to two first bytes?

MT: interesting suggestion, giving away a porton of this space

Spencer (not as AD): what's confidence that this set of protocols is complete wrt what you want to mux with quic

MT: This is really a happy accident. Some of the later ones were engineered to fit (TURN, RTCP). Not a good architectural basis to say let's fit into narrow spaces of this octet

BA: Aside from problems with QUIC header, it also allocates everything to QUIC

MT: Yeah, tiny slices, makes rest of space unusable.

*moving to slide #8 (SHIM)*

*moving to slide #9 (avoid conflict, swap short and long*)

IS: Option 4 is fine, let's do this.

Lars: (relaying unknown) Turn channels only happen after STUN nego.

*Moving to slide #11 -- do this in a new version with more invariants*

IS: I think we can do 4 and then do 5 later.

MT: Option one remains the safety net.

Jana: agree on invariants, on mux: do not have an exhaustive list of conflicts. other protocols, RTMFP. Others we will conflict with one by one, we don't want to ask is this really use, instead, more scaleable is to look at stuff like STUN and say do we need this in version one. if we want to demux with stun, or rtp, then we define something, probably a shim, we define it later. we can't coexist with everything else

MT: we have people looking at this set of protocols as used with quic (WebRTC), "sort it out for yourselves" would do them a disservice.

CP: re: shim, that only works if it's either always there or it's greased.

MT: Does the P2P use case see similar sorts of... actually, you may be right, since P2P QUIC will look a lot like client/server QUIC.

CP: Option 4, picking a subset probably makes sense, not entirely convinced about temporal demux. Key point, think about what we need to lock down for our use cases. Will never avoid all. Essential thing is to enable P2P use of QUIC. We will want to do that. I do not want to re-invent STUN, so we need to avoid STUN.

MT: simple solution. invoke the connection ID bit.

Magnus: TURN channels are there... (offline) have not made up my mind. but STUN is the most important to avoid here.

Martin Duke: clarifying on option 5... we always commit to longform bit and connid bit in short form?

MT: Yes

MD: You can work around that with enough flex for Option 5?

MT: Can make it easier

BA: Possible to move the version field up?

MT: no. unless we believe necessary to move it now.

BA: In some protocols version fiel comes first to allow all other things to change version, but already committed to other parts of short and long hdr struct..

MT: We've chosen differently, have put routing things right up front.

BA: If able to move version field or conn ID could guarantee that a given octet has a given value for a shim, and version has space.

MT: If we were going to go with a SHIM we'd have to do some major surgery.
Roni Even: Major concern with having just one packet type byte. Moving to uint16 allows us to do more with first bits of packet for mux etc. Okay muxing just with STUN though.

MT: Will produce a standalone document with respect to QUIC invariants...  fd

Mark: Invariants are the base for discussions about versioning as well as about middlebox interactions...

Spencer as AD: thanks Martin for doing this work. If you document invar in its own document, then you can open other docs for revision without touching them.

ekr: good idea to deal with this in own document, still need to discuss principles and exact invariants.

Mark: will have something meatier to discuss by next interim.

### Working Group Status and Scope

CP: By only focusing on a client-server protocol we run the risk of breaking P2P forever. Back to Invariants: without stun mux in V1, may not work.

Lars: Q is whether demux with stun is part of that for V1. if we do it, it's V1, because it's invariant.

mnot: we're not fully fleshing out every option in v1.

CP: I agree, but we are running a risk.

Ted Hardie: Also not happy with "HTTP-only for V1" for many of Colin's reasons. like second formulation much better, V1 + invariants. delivery in current timeframe is HTTP + a QUIC v1 obeying those invariants. does not mean is only for use of HTTP. someone can still use V1 for non-HTTP, as long as other apps get to talk about what invariants they need. Worried that "HTTP only" could be used as a stick to beat down issues, better to phrase in terms of invariants.

Lars: Moving the milestone is a big deal. Hope that by focusing for next six months, we can ship something people can run. Don't stop looking at MP or PR, want quic v1 to be easy to add other things in future.

mnot: important to keep in mind that invariants are purposely limited.

Romi Even: I think that issue is not invariants.  Not quantification of HTTP over QUIC.

Lars: multipath is nice to have it's not required.

RE: I'm not saying required I'm saying realistic.  We need a document that says that. I have manageability issues, not necessarily HTTP scoped

IS: Interesting point about mptcp.  We could easily ship H1.1 over quic . We probably need to decide the boundary. Modulo all Patrick feedback, I like this. Exact timeframe, if we don't have something implementable by London we are in bad shape. Will take nonzero time to finish implementing, four weeks to ramp up to large deployment... need five or six months to fix all bugs. London should be hard and fast goal. If we can't make it, cut.

Lukas: when will we see revised milestones?

Lars: after we have this discussion.

Patrick: Original problem may be one-time-only. Charter was written with implicit conflicts. Everything in the document doesn't have consensus, we have aggressive timelines, but as things go on we have more and more consensus. We aren't going in circles, but this is just a problem with how we started. HTTP hat: header compression is required.

Jana: I think this is very useful to have this direction.  I've heard a number of implementers say how they can't pause and wait.  They need to get going and keep going.  There is also some speed needed because there is ossification happening now! (yikes). We need to pick the invariants sooner rather than later.  It will help us implement and deploy faster.  In reality we need to do it soon!

Lars: Need to get the invariants done they are very important.

Praveen: Agree with direction.  HTTP over QUIC is very general.  Could do an API that limits functionality.  Need to work backwars from say Dec'18.  Lock it down before then and see we can get them incorporated.

Lars: If it's dec2018 we need them locked down in Melbourne.

BT: Agrees with IS.  If we're not cleaning up in Melbourne we're in a bad, bad place.  And he agrees with Jana.  The shape of them is correct, but not sure how to write the contract about the externalities.

ekr: descoping is good.  Add more manpower and descoping speeds things up.  But, what really makes shit get done is working hard by those saying make it go quicker.

mnot: do we need to revisit the decision about interims if we want to keep an aggressive schedule

ekr: I don't think more meetings helps. What will help is many summits of major people who cannot come to consensus. e.g. not useful to have Melbourne watch me and MT fight.

mnot: hackathon makes it go faster.

MB: more interims, please dear god no. however we can do hackathons virtually.

mnot: one day a month of interop?

Lars: formal joint time on slack would be useful.

mnot: lars and I will chat with spencer

### Spin-Bit Evaluation Design Team Report

Ted Hardie: [presentation](https://datatracker.ietf.org/meeting/100/materials/slides-100-quic-sessa-spin-bit-evaluation-design-team-report/)

TH: asks that all questions come at the end.

ST (a scribe): claps

BT: on #8: implemented spin bit it does what is ays on the tin when you have full traffic in at least one direction.  You get really good data.  WRT: ascii art this is a relatively well known thing based.  Slide #6: yes he thinks it worth it.  With sparse traffic it is extremely well known that some RTT samples are bad. Easy to reject. Suggesting that this leads to traffic analysis is a bit much (aka BS).

MK: This is a general purpose tool and there will be scenarios when it is useful.  Afraid that if we do this in the next version that we will be unable to put in the next version.  It's easier to put the bit and pull it out later.

TH: Putting it in

RE: Glad to hear disagreement about this, very similar to TCP, we know about the sparse data problem. Instead of ack, you get spin bit, otherwise same thing. It works. We use it. Important that it is implemented as a mandatory feature in V1.

IS: Are there different approaches people like better

Ted: We can up-level if we get consensus... loss...

DKG: Discussion presented here does not mention that people may be forced by networks to emulate standard expected pattern. Certain traffic flows wil be expected. Networks measuring on basis of spin bit, then networks will force

Ted: Not consensus in design team that this was a potential source of ossification. Discussed, no consensus

Martin Seemann:We have been discussing this since the beginning. In Tokyo, Paris, Prague. Question: what do we gain? I ask for numbers.

Ted: please review links in preso

Markus: Lots of things where we show this is very useful. Among people who want to use this, there is consensus that this mechanism is sufficient.

Gorry: Looked just at spin bit. You did not see security threat?

Ted: Examined security threat, spin bit is not one.

Gorry: You could look at other mechanisms as well

Thomas: Is this valuable? I think it is. It's a weak signal. I'd like to have more for measurement, better signal than nothing. Limitation: endpoints can fake information. Network cannot rely on signal, since it is not tied to state machine.

Ted: The way this measurement works with TCP, you are taking information from endpoint state machine. You cannot falsify the data without breaking the state machine. Lo

??? telefonica: regarding additional processing is needed... we see this as a very useful tool, we would like to see this in version 1.

Al Morton: re DKG, I don't believe that having insufficient traffic would be a forcing function for ossification.

Jana: I was hoping we'd have a very clear understanding of what all this would be used for or what it would enable.

Ted: Things on slide 7 are the things that the operational community said they would use this for.

Jana: Network can measure handshake RTT now.

Ted: DT pointed this out in rejecting spin as new info.

Jana: Concern remains: if there is not strong demonstrated need, we shouldn't add it

Markus: looking at the links you will see demonstrations of usefulness, inter-domain troubleshooting on different links/paths. Two or three docs there describe that. If V1 is HTTP only, many of these corner cases might not apply... sparse traffic is less of a problem for h2

Ted: This is probably invariant

Roni Even: Not part of the state machine and therefore falsifiable... okay, but many measurement methods not tied to state machine are currently in use. This is an SP problem because SPs are the ones who pick up the call when an end user has performance issues. This makes inter-domain troubleshooting important. Need to figure out where the problem is. This is mostly a video thing.

Dan Druta: Disappointed. Back to square zero. In Prague we discussed threats, here we see there is no threat. We need this, and it's in the charter that we make QUIC manageable.

mnot: Charter says we will consider

Emile: We also have to troubleshoot loss... in order to troubleshoot, we can use the fallback to TCP. Is fallback to TCP invariant? Then we block QUIC to get troubleshooting.

Colin: Sensitive to operator concerns here. Since you put the protocol state machine behind crypto, everything outside crypto might be fake. That makes this difficult...

Gorry: There are other methods to get fine-grained RTT at different places on the path? What were those?

Ted: Look at original reference from Christian, IPPM work on OWAMP, alternate marking. This is an engineering tradeoff, you can do this without the spin bit, but it is much more

Lars: Can we postpone this?MK thinks we need it.

TH: agrees with MK.  Points out that the running spin bit happens after you have crypto connection so it's outside of the variants.  Possible to still have it greased ...we can differ it as long as we know we not deferring it.


## Wednesday, 15 November 2017

*9:30-12:00 Morning session I, Collyer*

*note takers: Brian Trammell and Ted Hardie*


### Editors' Update

[Review of Recent changes](https://datatracker.ietf.org/meeting/100/materials/slides-100-quic-sessa-editors-change-summary/) (Martin Thomson):


slide 2: Martin reviewed changes from -06 to -07.

slide 3 (closing): Martin described changes in termination modes.  There are currently 3 modes with two states prior to termination, which share a timer. Draining does not permit send; closing does permit resending the closing frame.

slide 4:  Martin described the timeout within the closing state in the state machine.

slide 5:  Martin described the case where a closing frame is lost.

slide 6:  Stateless reset:  so simple.  There is no state.

slide 7: unidirectional and bidirectional

Martin reviews the unidirectional and bidirectional stream_id initiation and mechanics.
Use two bits of the stream ID to indicate origin and uni/bi-directionality .  This will require a new state machine description.

Roni Even: Can you explain the diff unidir/bidir with respect to closing?

MT: Primary difference here is that both sides of bidir stream are opened on open. Blocking is also tied together. In steady state, exactly the same. Close the same way. Saw some frowns.

Ian: Martin's inflight PR clarifies this nicely. Wait for -08.

*slide 8: integers*

Some updates to types associated with numbers, so that there is now just one format.  2 bits for size, remainder big endian.

This is in the HTTP mapping as well. No more continuations in HTTP header blocks (audience: amen!)

*slide 9: miscellany*

pong frame for address validation post-handshake; packet type rename. Will fix packet number and ConnID thing, lost of little stuff.

Mike Bishop: have talked about push ID

MT: Did that, didn't upload changes, sorry. Moving to a model where requests have IDs on HTTP layer. Push after push promise includes that iD. Suggestion, provide ID explicitly at HTTP layer, in order to not expose stream ID

Ted: Format of ID?

MT: It's a number.

Ted: Can make it trivial to use mech for something like DNS, uses QNAME, and we can map QNAME to a number, a mapping for protocols using a string would be nice.

MT: Not generic, HTTP specific.

Ted: A different protocol can use a diff format for something similar?

MT: Yep. DNS can QNAME or whatever.


### Loss Recovery

Ian Swett [presentation](https://datatracker.ietf.org/meeting/100/materials/slides-100-quic-sessb-quic-recovery-and-congestion-control/)

*slide 2 goals/ non-goals*

Minimize time to repair, and ensure forward progress.

Non-goal: tell implementations what to send.

*slide 3 principles*

Focus on when to declare packets lost, not what to send.

Don't mark packets lost until an ack for a later packet is received.

F-RTO by waiting for RTO verification (No UNDO)

*slide 4 differences from TCP*

Ian goes through the points on the slide, expounding on the final point:  QUIC ends recovery when the first packet number after recovery is acknowledged.

ekr:  this seems subtle, a diagram might help

ian: yeah

ekr: brian trammell's student is apparently writing this for me so maybe I'm done

BT: Hahaha

*slide 5,6,7,8,9 fack*

Declare packets lost when a packet sent 3 or more later is acked.
(there is also a time based loss detection, see slide 12)

*slide 10,11 early retransmit*

Early retransmit based on an RTT timer (1/8 RTT timer, as in TCP in  linux kernel).

*slide 12: timer loss detection*

This is a bit more different from TCP.
Timeout packets count towards bytes in flight, and timeout events do not cause packets to be declared los or change cc.

*Slide 13: time based loss detection: Handshake*

Note: expected RTT may be based on past connections to the same host or connections to other hosts.

*Slide 14: Tail loss probe.*

Ted Hardie: For RT frames do you include PING and PONG frames? Not in themselves rtxable...

Ian: Yes, interesting point. PING used to be rtxable though. Short answer yes

*Slide 15: RTO*

Gorry: You send a lot more after RTO expiry than TCP would in the first round, correct?

Ian: My understanding is that Linux sends two

Praveen: You're only supposed to send one

Jana: TCP is supposed to send one. The cost of RTX after timeout is very high. The first packet is very fragile, can need to wait 2RTO. Sending to protects you from this. TCP should consider this, too.

Praveen, OK, when we deviate

Ian: the contents of these slides are taken in part from what Linux has as defaults, which may be more aggressive.

Jana: Some of the constants are aggressive because useful...

*Slide 16 magic numbers*

Jana: Some are not what TCP on Linux does. In QUIC our TLP is more aggressive, bt still safe because fundamental mech still the same.

Praveen:  the only concern would be if the safety property was not retained.  A conservative implementation may choose to use lower constants.

Jana: We should discuss. A big part of this is the constants. High order point: should be clear that safety properties ate not getting violated.

Praveen: Q on TLP (14)/(16) ack delay?

Ian: 25ms, smaller than some stacks. Makes some CC situations work better with delayed ack eg. with BBR

Praveen: In TCP we can assume other side does 50ms. This might be a useful transport parameter to negotiate

Ian: Issue 912. Does anyone object to communicating max ack delay as trans param

Gorry: Open issue in TCPM.

Jana: Matter of process. With constants and mechanisms, this is a standalone doc, will be its own standalone process. Will not live with same musts and shoulds forever, from TCP. Constants different. Some mechanisms subtly different. Different target, latency. Constants come from current specs as well as practice.

Lars: Echo praveen's suggestion, document differences to TCP. Explain why. Otherwise same Qs over and over

Jana: you mean diffs from TCP constants in RFC stream?

Lars: Also expired drafts. Two sets of things ppl familiar with: RFCs, linux. Can pick either. If you pick another, must say why.

*(Chairs confirm that the document references to TCP constants are informative)*

Praveen:  That seems fair, but instead of saying Linux, then say standard implementations or typical implementations.  That may be more fair.

Lars: Only ones we get constants from are the open source stacks

Praveen: RFC deviations are straightforward. Otherwise taking value from Linux is OK.

Ian: happy to have your help with that Praveen.  What we have now is pretty terse.

Jana: Don't just look at constants. Look at mechanisms too, they are subtly different

Lars: Text like that is lacking.

Lars: that would be an excellent point to make in the document.

Praveen: Max ack delay is missing in TCP. Other Q, 200ms handshake timeout. Caching the handshake RTT is a good idea e.g. for satellite.

Ian: the current situation is to cache the value for a previous connection to a server, but it turns out that this is not sufficient for stations behind very long delay links.  Using information from other servers helps ensure you do the right thing quickly.

Michael Sharf: Please document any deviations from TCP. At the end of the day if that's what speeds things up we need to know. Please also bring to TCPM.

Ian: RACK implemented many of these principles

Gorry: Worried that this could be more aggressive (in a bad way). Need some way to understand how this competes in queues in a strange environment

Lars: Hope next year we have implementations you can run bulk data through. We can show results in ICCRG.

Gorry, Ian: yay!

Gorry: I like that, thank you.

Ekr: Why expose max ack delay as a TP? Might consider other approaches. Worried about codifying this assumption about receiver in the protocol, maybe the receiver doesn't have a timer? How do you express more

Ian: In this case, communicate maximum timeout. Not whole alg. Way too complex. Just the max. TCP now says 1 sec timeouts, but that's crazy so nobody does it. Idea is to expose envelope when it's less crazy.

Ekr: Important to write carefully.

Ian: Agree.

Brad Jordan:  I'd like to shift gears a little.  All of the acks will be in the encrypted tunnel, yes?  How do we enable the operators to foster success in their networks?

Chairs:  This is the wrong document for that discussion.

Jana: I would like to respond to Gorry.  It is the case that the constants are a source of benefit here and that definitely should be discussed with TCP, but there are also seriously different from TCP.  Retransmitted data does not re-use sequence numbers in QUIC and that has consequences in how the algorithms function.

Lars: Excellent for document

Jana: Briefly. In most recent we put in a bunch of text

(Never got approved)

MT: point about advertising values. if you do this as a client, you advertise them to the network, since TPs are not encrypted.

Lars: Thinking in TLS about encrypting this?

MT: Yeah, some ways to do that. They have latency costs. We could build another mech later. But that mech is maybe not useful. Think about consequences of throwing a bunch of stuff in there. ote that ack delay is observable on net anyway so not a problem. But when we add stuff to TPs we need to be careful

IAN: We should consider this on a case by case basis.

Mirja: Note also that you may want to adapt ack delay due to network conditions within a flow.

MT: We can't do that now, we can do that later when we get encryption.  If you want to do this in a data center it would be in response to observing a really low RTT.

Sebastian: Can we go below this in really low RTT situation?

IAN: We do expect microsecond accuracy, that's what we had when we timestamps.

Praveen: If we nego a TP with a max that's strictly better...

ekr: Only need to worry about diff between us and ms... {missing}

*slide 17: implementation tips*

Ian: Stuff we messed up. Do not do them.

Praveen: First slide says we don't recommend what to send. Might be useful to make a suggestion?

Ian: Transport draft has wishy-washy text about RTX before new data to reduce flow control blocking. No normative language though. However TLP can use new data because likely to be spurious.

MT: Ian covered much of what I was going to say. The question will be informed by priorties, for instance.

Jana: Add that also discussion about possibility of partial reliability...

Lars: Stuff you always say at the mic should go in the draft)


### Connection Migration

Jana: I'm going to discuss connection migration as it is in the draft and where we want to go with this, using new mechanisms that are more resilient and more useful.  This is a higher-level discussion, looking for feedback from the community on direction.  This is an initial sense of direction.

*Slide 2: Current draft behavior*

(peer here is client movement in a client-server case)

Latch + ping/pong to verify.  Assumes only one address is available at any time.
Works well for nat rebinding, make after break.  Does not allow for proactive migration, and a spoof causes validation.

*Slide 3: Using multiple addresses*

Migration in one of these cases is to shift to a preferred network (e.g. from cell to wifi).  But the preference is subject to a usability test (Can I reach this server).  A different version of this is the parking lot problem, when WiFi does not drop sufficiently aggressively.

*Slide 4: principle 1: probing and latching should be separate*

Ted: In a lot of cases with cell+wifi, when you have a wifi interface you have no data channel on the cellular interface. How would you craft a probe to create a data channel? You may need to reach down into the OS stack to make this happen

Jana: yep. assume client has right privs. has to be willing to pull up server net when it needs to probe. Do you think this is a protocol spec or impl issue?

Ted: Definitely impl, but need to be cautious that existence of radio does not imply path that is probable. Probing by itself will not necessarily bring it up. If you want MBB you need the OS to let you do that.

Jana: Might warrant text

Tommy Pauly: Would work fine. A benefit of QUIC doing this in userspace is you get more freedom to play with knobs (bring up intf, etc). You may often have a path in a available/not-ready state. Should capture that state here

Spencer (fuzzy hat): how stable do you think preference order is? Natural law? Anything we need to say about how to express those prefs?

Jana: Implementation specific.

Praveen: Yep seems so. When traditional interfaces are available, then you probe. Maybe you don't require QUIC to be able to kick an intf for probing.

Jana: Should we proactively probe and keep paths around, or only reactive. Deliberately not getting into that.

Eric Kline:   Instead of talking about interfaces, talk about addresses.  This should also work with IPv6 privacy addresses

Tommy Pauly: Document should be agnostic to system policy, describe mechs. Both in terms of what preferences as well as the aggressiveness of switch. MPTCP has higher level APIs... both should be possible. This relates to work going on in TAPS. Should be compatible with that.

*Slide 5: Using Multiple addresses*

Principle 2:  Interface use is a local decision.  When possible support peer's ability to choose.

Jana: there are a lot of policy questions here that the client can control, and it's not always the case that only the sender or only the receiver has a better idea of which path is better.

*Slide 6: Migration with multiple addresses (straw-man)*

MT: To Tommy's point earlier, note this is one of many approaches you can take for this. This is an example policy. What's in the draft now is another policy, it's abrupt and breaks things. Note that his particular design does not optimize for throughput as you won't have the same CWND. Also possible to keep two connections up simultaneously

ekr: What's your threat model for this design.

Jana: Um. Two things. You don't want the server to start sending to arbitrary (spoofed) IP address.

ekr: not following step 4 (server receives packet over wifi) claim, don't latch until you get the probe ack. Transmission of data over wifi is implicit rtt

MT: I can explain. Probe has ret route check.

Jana: Server also needs to validate that client is legit.

ekr: what do you believe an attacker can do with this. If I have momentary access to a network, can I divert you to another one? If I can get one packet out... Let's talk about the threat model not about the design.

Jana: Missed saying server also needs to validate client.

Ted: Martin wanted to point out that MAB model is one potential policy. One of the things the first example is designed to do is nat rebinding. Are we going to try to make mechanisms for of nat rebind resp the same as this. most elegant is to say yes they are... but maybe hard.

Jörg Ott: you have aggressive schedule for rtx. when switching interface, may experience different RTTs. should reconsider tx schedule...?

Jana: Yes, will interact with loss recovery in interesting ways

Praveen: regarding threat model... can source addresses be sent in encrypted payload. Is value in probe beyond addresses

Jana: Yep NAT.

Tommy: Agree with that point. We're looking at threat model etc, another thing to look at for encrypted mobile UDP protocol. MobIKE can do this, has explicit support for this. Check their security considerations.

Jana: Good point thanks

Xavier Marjou:  I am thinking about other applications on the same device.  Do you see QUIC as activating new interfaces, and how does that impact other traffic leaving the device.

Jans: Sounds implementation specific. That is not something  we can address in this document.

Martin Thomson:  I got up to push you to the next slide.

Jana: I'm not done with this slide

MT: I'll wait here until you are done.

Jana:  Describes how the probe mechanism interacts with the parking long problem.  Basically, re-uses SCTPs failover model.

Chairs: Moving to next slide despite HOL being used as a forcing function.

From Jabber: Is this in scope for version.

Jana:  I believe that it is in scope, but don't want to say that

Chairs:  We must survive a NAT rebinding.

Rick Taylor:  I think we're disappearing quite deep into the weeds here.  QUIC needs to understand that bearers come and go, how that happens is out of scope.

Brian: We're really creeping into designing a multipath transport protocol here (yay!) but we shouldn't do that by backing into it.

Jana:  It's not a line of code; it's much more complicated.

Lars:  The things you need for multipath you also need for this; having two different ways of doing this would be bad.

Jana: multipath requires twinning everything.  This does not, even though failover would be a special case of multipath if we had those mechanics in place.  This doesn't require all that (see Multipath versus failover in MPTCP)

Jana: sender has to maintain multiple congestion control state, window state, etc.
Failover is incredibly useful, and I would argue for having it in v1

Yoshifumi Nishida: What's the difference between this and what SCTP is doing for address management?

Jana: SCTP model is you failover...

Yoshifumi: What happens if other side is behind a firewall

Jana: your probe packet may not get through in that case Note that This is not applicable to the handshake

Yoshifumi: Please clarify in draft

Martin Thomson: Whoever it was that caused us to uplevel, thanks.  I am inclined not to do this, even though I think Jana's design is fundamentally correct and works pretty well.  That kind of thing is in the current draft, but only kind of.  Maybe that is enough for now.

Jana:  No support for make before break?

MT:  You can do it without changing the design we have.  It's not good (given latching issues).  But it can be done.

Lars: Your point: what's the minimal thing we can do for v1 that lets us do something not terrible

Jana: I think what we have right now is not suboptimal. If you try to implement it, it is incomplete. Latching point I grant. But you need to probe the alt path. Need to deal with consequences. Don't want to reset CC twice. Probe packet is part of seq space. When you work out the details, you get here.

MT: If we don't commit to make before break we don't have to do that.

Jana: But you don't get migration

mnot: Charter is a little fuzzy. We should resolve that. Need to find out how that affects invariants.

MT: That was why I was suggesting shelving.  I totally agree with Jana that it is not good enough.

Daniel Migault: I think this is really different from failover.  This is something that we have already done elsewhere, and I support doing it.

Tommy Pauly: Martin, I disagree, full multipath is a lot more. That's not in multipath. We need to make sure this is not conflicting with multipath, I think it is not. If we can do kludgy handover, I will make sure it's disabled. It'll need to get revised and updated. This is well understood in other protocols. If we put anything in, let's do this. Existing model is there  but only argument for it is inertia. What is beneficial other than not wanting to take new text.

Mark: Discussion should be about why this needs to be in v1

Jana: i don't think this changes invariants.

Mark: Can we do it in v2?

Jana: yep

MT: If we're going to spend time fending off requests for the feature then we need to just do the feature.

Mirja: I think this is an important use case that will make the later multipath design much easier.  This is the right direction to go. We might also want to consider adding a probe-request frame.

Bryan Ford: To add to migration vs multipath, concerned that mechanism and policy stuff is getting lumped together. Mechanism for migration and multipath should be practically the same. Migration is a type of multipath policy with only one at a time. A migration type policy can be done more easily than full blown multipath. Most important is from the start be able to distinguish policy/mechanism split. Mechanism should be in v1.

Jana: Disagree. Connection migration is simply a policy is a view you can take when you already have multipath. I don't want to go there. How can we make connection migration a special case of single path. Can we add exceptions for probing packets

Bryan: You get most of the complexity.

Jana: we are we trying to establish what we can leave out to get this (e.g. no having multiple congestion controllers, etc).  That is something that we can do and minimize the implementation complexity (though it comes at the cost of some specification complexity)

Andrei Popov: Observing that UDP based transport is likely to work on a subset of interfaces. Should migration work across transport protocols.

Lars: NOOOOOOOO not part of charter

Ian Swett: current section was designed to potentially accomodate... I think we can take on some work to make minor mods to current text to make this possible and implementable. Support doing that now. This is super useful.

MT: Not opposed to doing something better here. Would like to see a more fully worked proposal. The slides are not enough. Concerned about use of conn IDs and packet number gaps in this context. If you flip between them you get gaps every time. Not sure that works. You really want a dedicated packet number space per path. Loss recovery impact, path delay impact. All of this we need to understand in more detail.

Lars: butterworth is booked 12:30 - 13:30 to work on this, seats 12.  We need more time on this.

MT: I want to see a design first, form a design team on this.

Lars:  If you want to serve on the design team, send an email to Jana.

Lars:  We'll figure out after we've talked whether it is a v1 or v2 issue.

Mark: keep scope in mind and don't try to design full multipath

Lars: We need something for v1, but we need to know what subset.

Jana:  I want to push back against that, because I don't want this to be a special case of multipath.  That's too complex.

Lars: Need nat rebinding and some migration for V1

### Third Implementation Draft

Mark: Full day interop in Melbourne, this is the target for this draft. Assumption is we're done with second impl. Is this true? Implementers?

ekr: Not done with 2nd impl draft. Not useful benchmark though. Two things might be next: Much more filled out test matrix for 2nd impl draft without new features. Or more features with crappy testing. I would say we should fill out the test matrix, but any experience at all with stuff we have not done would be useful too. So let's pick out a small set of new things based on -08. From things that did not make the cut for 2nd impl: 0rtt definitely, sad we have not yet done congestion control. So either loss recovery or congestion control or both. Demonstrating you can move large data over internet is useful. There's a lot left.

Ian: 0rtt def on list. We don't need all of LR, but we can tack fast rtx on rto. Basic AIMD CC would be helpful. That plus 0rtt is fine.

Lars: We have eight weeks minus holidays. -08 certainly. Add proper LR. Something beyond flow control would be nice. If there is strong interest in 0rtt, let's add it. Hesitant to do more. Implementations need to settle a little longer.

Mark: Will we start at the interim with 3rd target, but continue in London

Praveen: 0rtt, LR, CC seem good. LR + CC is not much about interop. Strict test cases would be useful. Number of test cases will explode. Having defect software would be useful. But need strict cases otherwise too open ended.

Mark: We will be on university wireless in Melbourne. Can provide wired switch.

ekr: I hacked up an interop harness, 2 impl on the same machine, easy to add delay and loss to that. Would say you can successfully deliver x packets of y size under certain network characteristics. Want a separate linux box that can do this.

Lars: Repeatability is good. Random loss is nice and easy to do, might want to specify which packets are lost. Also possible to do random loss with specified seed.

Praveen: Would be very useful to drop specified packets eg. handshake

MT: Def want 0rtt + resumption. Won't get header compression now... want to be ready to do that as quickly as possible. PMTUD + key updates can be pushed off. TLS shows nobody does this. Otherwise, move up 0rtt, resumption, basic CID changes, Migration.

Lars: By Melbourne?

MT: Why not?

Lars: Because it's soon

Ian: It's tomorrow.

Lars: Let's have priorities.

MT: Ordering then is -08, loss recovery, resumption, 0rtt, then migration. We need it. Don't take it off the table. Add 2nd impl things on the list too. HRR and stateless retry adjacent to 0rtt.

Lars: Want to ask non-editor to put together 3rd impl spec...

Ian: Agree with MT. Keep http/.9 option available, don't force to H2, it's a fair amount of extra work. I'd almost like to do the mapping at the end. Suggest we move to tls -22. Annoying our BoringSSL team.

ekr: all the stacks that were here do it anyway. 21.7 was the target on Saturday

Jana: Agree with Martin, also with Ian on H2. One minor point about LR, useful to have non-random losses. We want to test specific cases.

Martin Duke: Confer with basic consensus. Have code to drop specific packets.

Lars: Stuckee for third draft wiki page?

ekr: me

Mark: Can you also drive contributions for test cases?

Mark: Roadmap forward for HTTP header compression. We have three proposals. Chairs will work with proposers to converge.

Mike Bishop:  In Seattle, you asked me and Buck to form a design team, but I have had no time to do that; apologies.  Hoping to get that started this week.  There are more things that are common than you might initially consider.

MT:  We should reconsider some of the features, e.g. delete which would radically simplify the proposals.

Mark: Mike work with Buck and make a proposal to the list in the next couple of weeks.

MT: and please include Dmitri









