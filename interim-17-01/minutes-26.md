# Minutes: QUIC Working Group 26-01-17

Chairs: Mark Nottingham, Lars Eggert
Scribes: Ted Hardie, Brian Trammell, Ian Swett, Patrick McManus

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
    - [Next Steps - getting to interop, implementation plans, editor plans, meeting planning](#next-steps---getting-to-interop-implementation-plans-editor-plans-meeting-planning)
  - [Transport / Loss issue discussion (cont'd)](#transport--loss-issue-discussion-contd)
    - [Server-proposed connection ID #119](#server-proposed-connection-id-119)
    - [Path MTU #64 / PR #106: PMTUD](#path-mtu-64--pr-106-pmtud)
    - [Minimum Packet Size #64 / Minimum MTU #139](#minimum-packet-size-64--minimum-mtu-139)
    - [Padding Handshake Packets #164](#padding-handshake-packets-164)
    - [Issue 145](#issue-145)
    - [Issue 204: Headers streams do not contribute to connection level flow control](#issue-204-headers-streams-do-not-contribute-to-connection-level-flow-control)
    - [Issue 35 - starting packet number](#issue-35---starting-packet-number)
    - [Issue 118 - source address token encoding](#issue-118---source-address-token-encoding)
    - [Issue 136 - First client packet size](#issue-136---first-client-packet-size)
    - [Issue 148](#issue-148)
    - [Issue 56](#issue-56)
    - [Issue 62 - Finding Frame lengths](#issue-62---finding-frame-lengths)
    - [Issue 70](#issue-70)
    - [time format #109](#time-format-109)
    - [Interframe padding #158](#interframe-padding-158)
    - [Issue 144](#issue-144)
    - [Issue 169 response to loss handshake packets](#issue-169-response-to-loss-handshake-packets)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

##Administrivia

9:30 - Start (doors open at 9:00)
Scribes, Blue Sheets, NOTE WELL

### Next Steps - getting to interop, implementation plans, editor plans, meeting planning

Mark: Notes that we’ve made pretty good progress in the last few days.  What are the next steps, it seems like it’s a bit premature for interop.  What does it look like as well?  HTTP over QUIC, PING over QUIC, etc.  Interims seem to work well, and having another before Prague seems like a good idea, likely in Europe.  First full week in June?

Lars: We could have a half-day before an IETF, but not everyone could come.

EKR: Hackathon would conflict, which could be a problem, but at some point, it’d be a good time to work on interop.

Lars: After Europe, likely to do North America.  Get an 02 draft out before Chicago.  MT agrees.

Lars + Mark: Implementations page exists(link).  Please add a link and detailed description to the page if you have an implementation or are starting to work on one.

Lucas: QuicGo noted they don’t have time to implement the drafts as they stand, but will once others start to implement as well.

Mark: Notes that in H2, a draft was nominated for implementers.

Ian: Suggests that Google will implement a draft, hopefully mid-year timeframe, and in the meantime, will inch towards the IETF version when consensus is reached on items.

Lars: QUIC logo is being designed, sponsored by ISOC.  Mark notes this will not be a consensus call item on the logo.

Mark: Contributing section(link) goes over the lifecycle of issues and what “Closed” means.

## Transport / Loss issue discussion (cont'd)

### Server-proposed connection ID #119

As a matter of principle, it’s better to have the connection ID picked by the server, since it can be used in routing etc by the load balancing infrastructure. Right now that infrastructure is stuck with whatever the client picks.

Second, you don’t need the connection ID on initial handshake of an initial (non 0-rtt) state. Connection ID can be useful for 0-rtt since 0-rtt state might be on a particular instance.

Three options:
* Keep as is, let server suffer
* Give server option of proposing new connection ID
* Have server always propose connection ID (i.e., never allow client to pick)

Brian: Solve this at the same time as the connection ID migration; i.e. a frame for new-connection-ID on the control stream?

How do we solve the initial problem?  Why do we need the client ID at all?

Jim: Connection ID was intended to be proposed by the client, and then the server may replace it.  (option 2)

Jana and ? propose that option 3 seems better than option 2.

MT and Ian and Jana note that you can (but don’t need to) bind STK to a connection ID.

Subodh notes that you may want to use a STK multiple times with different connection IDs.

Lucas: We can just change the semantics to have the client not send an ID in its first packet, and the server reply with one.

Brian thinks this defeats client selection of connection ids for non-linkability.  Ian and Jana and others note that this is mostly orthogonal: the server can propose multiple connection IDs.

Kazuho: What happens in the case of a NAT rebind?   Ian thinks this isn’t a concern during the short period of time there isn’t a connection id, particularly because the inchoate case is only one packet, so NAT rebind is a non-issue.

Igor: Connection ID contains information to allow connection to reach the correct backend server.

Jana notes you could omit the connection ID on every 0RTT request.  THis doesn’t work if the source address has changed since the last connection since STK verification will fail. Would be nice to enable rebinding with a new source address.

ekr: need a mechanism to send a few proposed connection IDs. this is a correctness issue unlike session tickets in tls.

Igor: For 99% of cases you only need 1 connection id, multiple seems like overkill.

Ekr: Adds complexity and could cause connection failures, Jana notes that more likely it’s just cost a round trip.  If you’re ok with not using a connection ID as well, then you can just include STK and no connection ID.

MT: This is only useful if you need to store resumption information for 0RTT information.  Ian notes that it could also be used to prevent DDos style attacks potentially.

Jim: These are interesting problems that Google had to overcome. We weren’t sharing cryptographic states across the server complex. The trick was how do we route the next 0RTT request to the same server. Connection ID was a possible hint to come back toward the same server.

Subodh: If you’re in Namibia and your 0RTT key is in the US...

Ian: There’s another use case: you can prevent overuse of an STK by balancing on connection ID.  If a connection ID/IP is relatively stable, all 0RTT requests for a given STK would hit the same server, and it would reduce the possibility of overuse of a single STK.  If the connection ID didn’t match the one in the STK, you could force a 1RTT handshake.

ekr: no reason an STK can’t be used for an arbitrary number of connections, it’s only proof you have the address.

Subodh: with low connection idle time limit, you might want a new connection ID to conserve server state

Ekr: If you have a STK and get a handshake failure, then you could fall back and not use the STK. We have lots of client identifiers that all have subtly different semantics now. Not clear we want to do this, or to define just one and use it for multiple things.

?: If we believe connection IDs are long lived, this doesn’t matter too much.  But if we’re going to resume frequently, this seems more useful.

Jana: Client has to decide whether to send a connection ID.

Ted: We’re dancing around an issue to avoid yesterday’s rathole: using connection IDs to work around ECMP problems on rebinding, as a routing token. If you don’t need that for your connection, then you can use a different connection ID every time. You can also have a batch of connection IDs that are equivalent, and you can change them periodically or base interface change. If we’re modeling them that way, as a destination routing token, then it’s very clearly the server and we should have server-proposed connection ID. And the rats in yesterday’s model get less numerous. #119: answer is yes, go for it. Consequences in particular deployment are

Brian: Totally convinced by Ted.  But….  the server can make you trackable by only giving you one(ie: supercookie).  Now that would be visible by the path.

Ted: Agrees that is a potential problem if the path knows how connection ids are generated, but that creates a ton of other issues, so we’ve lost.

ekr: not buying it; ekr/ted/igor: in that case there’s enough collaboration that you’re trackable anyway.

Igor: what you do want is to keep the path from swapping connection IDs on you

Martin Duke: okay so then we need to AEAD that (revisit that issue)  Load balancer needs to deal with no connection ID anyway.  When are we omitting connection ID today?  Ian notes only from the server to client, not client to server, at least today.

Proposal in github.

### Path MTU #64 / PR #106: PMTUD

Retained text about default size captures what Google’s doing now, using loss as an MTU signal for PLPMTUD.

Lars: The max default size is in direct conflict with RFC 5405 bis, which says 576. I expect the IESG will go about this.

Jana: That’s the default.

Lars: Recommendation in 5405bis is don’t send UDP > 576 if you don’t know anything about the path. Second recommendation is don’t use ICMP-based PMTUD since it’s not reliable. Should not recommend to only use ICMP. Option one: reference 5405bis. If we really want to say the default packet size is > 576 there will be arguments. Ideally everyone implemente PLPMTUD.

Jana: We always have the fallback case if PMTUD fails: TCP

ekr: initial packet size is 1kB to reduce amplification factor.

Martin D: Lower constraint on minimum packet size: ClientHello size.

(Ian’s notes when he didn’t realize he was offline)

Lars: You can make an argument for QUIC that (1) TCP fallback and (2) 1280 v6 MTU and (3) it’s 2017 mean we can have a larger default.

Martin Duke: Added the option to do do ICMP based Path MTU, as well as packet PLPMTUD.  Indicates that if you’re not doing PMTU, use a fixed size of 1350 bytes for v6 and 1370 as v4.

Lars: Issue 1 is that 1350 is much larger than the IETF typically agrees to, and issue 2 is that we should not recommend we use ICMP based, because it has been found too unreliable.

Jana: The alternate is we recommend a small packet size, and and everyone actually uses a much larger packet size.  (See RFC6919.)

EKR: Initial packet is there to limit amplification attack, and if we make it 550, we increase our potential amplification attack quite a bit.

Lars: Could make the argument for QUIC that assuming a IPv6 sized minimum is reasonable, given QUIC has a fallback.  RFC5405 has many SHOULDs, and at some point we need to document how we do or do not comply with 5405.

Martin Thomson: level of authentication you need is “sender for ICMP is on path”

Lars: ICMP is at best additional information. We can ignore it and say just use PLPMTUD.

Martin: At least include the suggestion that the sender should make sure the packet wasn’t received before making an MTU decision.

Note that ICMP-based detection is also difficult since the interface to ICMP information is narrow (you might just get write errors).

Martin: will suggest provisional MTU reduction. And ignoring ICMP on that path.  Ekr suggests “path” may be too specific?

Lars: Packetization path MTU may not really be that practical, because it’s been a while since it was written, and it’s never really been exercised.

Craig Taylor: Heard ECMP mentioned for load balancing.  Are people aware that ICMP will balance differently from normal traffic, which can create a sort of blackhole.

Spencer: Why not MUST PLPMTUD?

Martin Thomson: Constrained devices. Might decide 1280 is good.

### Minimum Packet Size #64 / Minimum MTU #139

Martin Duke can write language. Fallback to TCP if you can’t send 1280.

### Padding Handshake Packets #164

Martin Duke: Favors “at least one” packet in each direction must be padded to the max packet size.

Lucas: What if an implementation doesn’t want to pad to the full packet size. 1280?

Ian: Suggested we add text that the initial packet is the max size until other path MTU discovery is performed.

Lars: Two ways to phrase. #1 1280. #2 cache PMTU information. Restart at 1280 or at old value.

Marten: Two issues. Avoiding amplification, PMTUD.

Lars: Yes, but you want to avoid early loss.

EKR: Given 1280 is close to 1500, seems obvious to do the handshake with 1280, and then use a padded PING packet to perform cheap Packetization PMTUD.

Brian: MUST at least 1280, SHOULD exactly 1280. Lars: Cautionary statement.

Ted: Unless you know what the PMTU is.

Martin: And you give the network more to play with inside its amplification attack avoidance envelope.

Marten: note that MUST 1280 makes it easy to identify the first packet of a connection.

EKR: Notes that one might be on a network where the MTU is larger(ie: a datacenter), so there are valid use cases where a larger value makes sense.  Server might wish to limit its packet size between what it received and 1280.

###RST_STREAM and flow control #162/#163

MT: RST_STREAM indicates the last offset of a stream that’s sent, even if it hasn’t yet been delivered.  If that value exceeds flow control, then you’re required to emit a flow control violation.

MT: Maybe #163 is editorial.  Mike notes the correct description is there, but in a different spot than MT was expecting.  (10.1.2)

### Issue 145

... filed by Marten should probably now be editorial.  Changed.

### Issue 204: Headers streams do not contribute to connection level flow control

Marten: This is complex, it’d be nice to simplify this.

Jana: These don’t count because we don’t want other streams to block on sending of headers -- but when you have N header streams this kind of defeats the purpose.

Lars: it also bakes HTTP stuff into the transport.

Lucas: There’s an example here… Imagine a browser uploading than the server can process, then you become connection flow control blocked though there is download flow control window available.

Lars: Client can avoid by not using the whole flow control window.

Lucas: Then we need to add language to the spec that you shouldn’t clog yourself.

Mike: Can you send blocked on a stream that hasn’t been opened yet?

Marten: It’s just a debugging frame

Martin: But then the server knows.

Ian: This is working as intended. Not sure we need to spec it, also not common in practice.

Lucas: Logical problem, if server never increments flow control window… should require peers to consider the window blocked before 100%, otherwise deadlock is possible.

Ian: There is no advice for sending window update frames. A policy on that would allow a peer to make a more informed choice about flow control window utilization

Lars: This is also a problem with TCP.

Jana: This sends us down a rathole, because we don’t know how much data there is to send.

Mike: There is language in the spec with lower case should about sending flow control updates frequently enough.

Lars: It would be nice to remove the special case.

MT: If we drop the special exemption, and use priority, then if we don’t get blocked, everything works well.  Be more prescriptive: when connection level flow control is 2BDP from the end, send window updates with every ack, or some other more frequent basis.

Jana: Receiver doesn’t know sender’s BDP. We’ve implemented, and we can talk about autotuning, but we shouldn’t go down that path in this document.

MT: If you burn your entire flow control window sending useless stuff, you’ve dug your own hole.
Lars: There needs to be a separation here. You can’t tie up memory at the QUIC layer because you don’t want to at the HTTP layer.

MT: H2 already has this problems: headers don’t contribute to FC window. We can call them “not consuming memory” because the entire set of headers has to arrive in order and at the same time (TCP handles this) and the header set can be decompressed and handed off to the next layer immediately.

Mike Bishop: one of the differences between QPACK and Buck’s model is you can partially process headers.

MT: if you’re partially processing something, you’re actually expanding the memory commitment, due to decompression.  You probably can’t hand it off until you’ve got the full set.

Ian: Isn’t this provably intractable? 1k flow control and a request that requires 2k to process.

Jana: Flow control usually doesn’t apply to a protocol’s own control frames. The problem is we’re mixing the layers.  HTTP/2 didn’t flow control headers, but headers aren’t QUIC’s control frames, they’re application data.

_lunch break - continued discussion on #204_

Ian: There may be other solutions, and I re-arrived at a variant of Buck’s proposed solution: single stream for compression dictionary. Wording in document is not prescriptive re window update frames. Always send a window update when it’s 1/3 full. Jana: there are two variables (when and how much).  Ian: how much is obvious, what you are suggesting is auto-turning.  We don’t want to get into that.  Ian:  I agree, but I think we need to change the basic tuning to ⅓: you get 2 rtts.

Lucas: Bigger issue…

Jana: This may be an HTTP problem. Then let’s take it out of QUIC.

Martin Duke: Whatever counts for FC should count for CC.

Lucas: There’s a DoS. Say you have 100 streams. Simple implementation: 100 HTTP parsers. Limit 10M per. With one headers stream, 10M limit, ok With 100 headers streams, 1G limit. not ok. Easy solution: introduce an aggregate limit, doesn’t work due to deadlock potential. One solution: limit the number of concurrent running HTTP parsers using a pool. Don’t read data when there’s no parser on it, use flow control blocking. Issue there: amount of HoL blocking that we’re reducing from a single header stream probably not worth it. Jana: we’re a little in the weeds. basic question: we’re talking about how to make HTTP work on a QUIC that has all of its streams subject to flow control.

ekr: table stream one, is it exempt?

ian: reasonable. not sure it’s necessary

jana: we *know* it’s special. it’s the control stream. it just happens that all of our control is crypto.

Lars: it would be nice to be able to keep the specialness of stream 1 to its contents, rather than FC

Mirja: how much gets sent after the handshake - is it worth special case.

Jana: this is about connection level not stream level

Ted: +1 to Mirja

Jana: much of quic signaling happens outside of stream 1

Ekr: would want exception if hol block would happen in competition with other stream. Sense is that doesn’t happen.

Igor: whole point of FC thing is to protect recvr buffer.. And if stream 1 does not get buffered then its not impt

Many: it can!

Ian: example where it can be deadlocked - enough 0rtt requests in conjunction with chelo then you can prevent (resend?)

MT, if you send too fast you can’t finish the handshake,

Mt: debunks somehow (help too fast).

Ekr: server should be acking data

MT: when you have to CHLO again the 0rtt data never happened...

Ekr: its harmless to exclude stream 1 (other than complexity) and nervous it opens up a problem

Jana: easier to exempt stream 1 - agree

martinD: … more reasons

Mt: should stream 1 count towards stream limit?

Many: just make it clear

Ekr, jana: discussion about where the enforcement happens arguments both for exemption and not.

Mnot: editorial discretion

Mike Bishop: crazy idea: if stream 1 is special and doesn’t count for stream limit and connection-level flow control, why not stream 0? you never need to refer to it in a reset or a window update.

Mt: concerns about 0rtt scenario from above as applied to stream 0

Jana: should stream [0,1] have stream-level flow control.

Martin Duke: client hello is limited to 1280.

Marten: it’s a stream, I can send you gigabytes…

Igor: or open stream 0 and skip the first gig by offset.

Mnot: lets move on

### Issue 35 - starting packet number

Mt and Jana: randomize agreed?

Ian: suggested range not settled

Jana: at least 16 bits

Mnot and lars: editors propose something

Brian - tied into representation in packet layout

Martin D - always still monotonically increasing?

Many - yes

Martin D - concerns about AEAD - satisfied its not a problem

#52 source address validation

Review of PR 120

120 refers to TLS for STK.

Ian: Both STK and resumption ticket can be used for the validation, correct?

MT: they’re completely the same thing.

Jana: no reason to separate them. This is a transport issue, just as tcp does for tfo. Tls1.3 assumes transport is doing src addr validation. Concern would be ??

Mt: my concern is we don’t know how to it otherwise

VV: not ready to discuss because we haven’t solved the issue of deciding whether we abstract tls or not and stateless retries. Tied into STK.

Mt: can deal this based on an abstract property - not a blocker

Jana: i would like quic to be able to do 0rtt src addr validation.

MK: wouldn’t every crypto stream do it for you?

SI: cookie is bound to hashed state.. Putting ip etc in there seems weird.

Mt: not that complicated, it can all get bundled into the blob and tell TLS to store and retrieve opaquely.

SI: how do you disambiguate between (help?)

MT: hello retry request in just one of those cases

Ekr: one case is for a lot of load - forces back into multi rtt. The other is willing to do crypto and send cert but you will terminate and expect peer to come back

Mt: whoa. New info.

VV: reiterate postpone

Mt: this is just a connection you terminate immediately.

Ted: pov of transport what I need is a cookie to hand back to client that will be returned later. Quic abstraction can be about those mechanics and tls mechanics are separable

Ted/martinD: asking if we can agree on the fact that tls is agnostic to how it is done

Ekr: you could imagine ip address certificates also being used (crazy pants) - challenge/response is not the only paradigm

Jana: if the stk were in the transport you would need to indicate to tls that it did not work

Ekr: hello retry request is designed for when client is in dgram mode and has not sent you a chlo you can process. There are multiple reasons for HRR

VV: explicitly write down the guarantees we want to provide with source address validation. We understand this but do not spell it out

Jana: why would validation live in transport

Mt: it knows about addressing

martinD: how does this address ekr’s problem? Transport has to block on hrr until this validation is done?

Mt: yep. That’s the cost of the abstraction

MD: back to the opaque blob without a specific format.

Mt: transport may ask for unconditional stateless reject.

Ian: can you end up with a small window if validation fails? To control amplification but complete the crypto

Ekr, mt, jana: application layer blocked.. 0rtt from unrecognized address, you could proceed but at slow rate

Vv: dont want to do that if you’re stateless

Mt: syn flood problem is worse than other protocols due to cpu

Many: agreement on mechanism - editor to change interface section in tls doc regarding implications of validation and advice on what might be included. Clarify abstraction.

_Marked editor ready_

BT: connection id and ‘leg’ can be indicators as well.

Mt: yes, this is mostly for first rtt

### Issue 118 - source address token encoding

marked editor ready

### Issue 136 - First client packet size

We did this.. ~1280. Editor ready

##Management and Applicability Draft

MK: this is for a milestone in charter. Give guidance to someone that wants to use quic as an application. Mgmt from the pov of the network what the network can see

Lars: what if a stack has no tcp fallback

Bt: don’t do that

MK and BT: you have to have a fallback, unless the draft talks about when you don’t need it

Ted: fallback might not be tcp for something like dns

Lars: if you’re ok with not having a fallback, draft should say that’s ok just beware that’s the case

Bt: zero-rtt will surprise app developers other than h2 and dns. not-Exposing stream ids also a bit surprising for legacy tcp folk. In this phase this is a dumping ground for discussing things that have an impact that we don’t want to normatively include in the protocol document.

Authors: does the group think this approach meets the needs of the charter?

Mnot: encourages wg to adopt and edit as necessary

Lars: wider audience of chicago would be good

Bt: dont want a CFA at interim

Lars: please update before chi

Emil: is there room for troubleshooting considerations in the document? (166)

Authors: yes

Ted: can this be split into applicability vs manageability as 2 documents?

Authors: we started doing that, but it might not matter. Could refactor though.

Ted: encourages refactor. Points out iesg would be prime target

Authors: actively seek co-authors that have relevant experience on both sides

Lars: sounds good

Ekr: seems like roughly right direction. What is the common understanding of the purpose of charter item? Is it to say that we are aware people want a different level of information disclosure? We should document that but not argue about it.

Emil: does this reflect what is on the network today, or the protocol draft? (ietf vs google quic). Right now a lot of traffic is on tcp today, some is on google-quic. And we cant troubleshoot google-quic effectively

Jana: lets do that outside this room

Ian: google is moving in the ietf direction and they will share many properties

Emil: proposing design team

Lars: no design team.

Ekr: google-quic has a bunch of management properties that are harder than tcp - ietf quic expected to share that (to whatever extent it is true). And that discussion is a match for this document.

BT: yes - document evolves along with protocol draft realities.

Jana: expects more management discussion than applicability

Ian: privacy and manageability are traded off

Lars: need to have that discussion as we go along with examples of new/equivalent ways of helping operators operate. CHI will be a better venue with more operators

Ekr: there are several distinct attitudes towards this tradeoff. Dkg at one end, mumble at the other. Need a structure for having this discussion.

BT: from plus bof, very difficult for us to reason about the devices on the path when those devices are not bounded. Sandvine draft is starting to catalog that in a I-D where we need more detail than just nats and not considering backdoors

Jana: i wanted a middlebox map of the internet. Hardest thing was to characterize beyond types - configuration options turned out to be the most interesting (and most elaborate). Firewalls and ids in particular.

Bt: yes. It might even be impossible?

Jana: yes

Ian: are there any things in the doc we should discuss now

Bt: debuggability is interesting wrt info to do passive rtt measurement.

Chairs: concrete proposals are the best thing we can do here - encourage them.

BT: have recvd a list of operator requirements that can largely be done with exposed packet numbers and knowing something about resend behavior and application running on top of it

_BREAK!_

###Issue 40 - [Variable Length Fields](https://github.com/quicwg/base-drafts/issues/40)

Jana:  In favor of reduction, but we should not be afraid of this; we can simplify this.

Ian, but we need to find a balance, since fixed length fields will consume small percentages of total Internet traffic over time.

Brian is suggesting that we shift to a single or a small number of variable-length integer encoding.

Ian: we have had zero bugs about that particular issue.  Lots of other dragons (QPACK, flow control etc.) that produced bugs, but this did not, so maybe we shouldn’t be that scared of it.

Mirja: hardware offloading would be easier with fixed-offset encoding.

Ian:  note that the Brian/ekr encoding is probably very hardware-unfriendly.

Lars:  two distinct issues:  1) are we in favor of variable length encoding and then 2) if so, what do we want to support.  We need to simplify for the easy cases.

Lucas:  we already have this problem with stream offset.

Martin:  we also have this issue with stream IDs.

Lucas, I’m not sure that is the same.

Ekr:  there are a number of things that are difficult about the current system.  There are a lot of different lengths for individual items and a very large universe of potential interactions.  0,2,3,4,5,7,8 for stream offset, for example.

Jana: we could take a shot at simplifying this and see what comes out.

Ekr:  another issue is the distance between the control flags and what they control.  There are some unfortunate splits in the current system. You need a path to look at the common header before looking at the later section about what they control.

Jana:  there are a few packet types, and those map to what parsing you need.

Ekr:  the implementation type may have different damage from this; BSD styles wouldn’t have that much trouble, but a subroutine/parses mechanism wouldn’t be that easier.

Jana:  some of these are part of things that we don’t have yet (like hardware offload), so let’s be careful about presuming that those would exist or how they would be built.

Lars: There clearly are hardware offload in TCP, and we can presume they would arrive.

MT: I think that we can reduce this to two problems: how packets are constructed before we have a connection and how packets are constructed once we have a connection.

Lars:  a principle could be that the packets are self-describing for this.

 MartinD:  common encoding would also be useful, so that if you have a 2 bit integer it is always represented the same way.

 Lucas:  I disagree a bit with this.  Different parts of the protocol would have different conventions (like packet numbers).

MT: your point is well-made, and that there are different constraints in different parts of the protocol (you wouldn’t have a 6-byte packet number).  Reducing the options is basically a good idea.

Clarifying question:  are we trying to unify these with the using protocol (like HTTP stream identifiers).  Not the scope of this discussion, which is transport-y bits of QUIC.  Can be considered.

Marten:  there is no complexity in having different representation; we might collapse into a single representation, but it shouldn’t be a guiding principle.

Lucas: can we make a list first, we might not have that many to consider and coalesce. Jana: that would be a good exercise.

Lucas:  can we do this editorially?  Can the editors just reduce this and we look at it again at the next meeting?

Jana: the editors can propose something and based on some of these principles.

Jana: I am surprised no one brought up timestamps (several: we were being nice to you).

Ekr:  This isn’t variable length, but there are two bits in the public header that are never used (version, public_reset).  We might be better off with either having a placeholder fingerprint or an {unusual bit} followed by a type.

Martin: why don’t we separate out handshake/special from normal packets and treat them independently.

Ekr: that would simplify the handling for it.

Brian: now you have one bit, and you could steal that from

Ekr: or you could have a special packet pattern, like a 64 bit string.  You can scrub for it.

Lucas: that feels like over-engineering.

Martin: we are already spending bits on packet number, key, connection id bit, etc.

Ekr: we have plenty of spare bits, yes, but that it is not really the issue.
Divergence into signalling whether connection-id is present in all packets or not.

Martin: that’s a micro-optimization.  If you have a special packet split, then you can avoid the optimizations for very unusual packet types.  Version number is present on special packets.
Jana: we need text.

Ekr:  I will take the action item to write this up; if doesn’t make sense we can throw it.

MartinD:  I would like to push back on whether or not we need a lot of flow state here.

Brian/Ian: I think we should write something up, as there are a lot of ways to proceed here.

Jana: I would like to consider Ekr’s proposal *and* the simplification PR so we can compare them.

### [Issue 148](https://github.com/quicwg/base-drafts/issues/148)

... is closely related; it is a dupe of the thing the Ekr just opened. (It’s getting late; ekr opened it as a TLS issue]) Instead ekr will copy into it.

### [Issue 56](https://github.com/quicwg/base-drafts/issues/56 )

We need an escape valve for extended flags, is that a version number or something else that extends public flags?  Given that extended flags are after version, version seems to be enough.

MartinD: we could have N flag bytes.

Ian: we are going to get middlebox fixing on this, at some point, so we need to get this defined sooner rather than later.

MartinD:  in accordance with my preference to keep these together, I’d rather have these be sequential, but I can see it as possible to have them buried back there.  Signal bit would enable the Google implementation to pick that.

Mirja: if you don’t have the version on every packet, the middleboxes will have trouble believing in multiple version and may ossify early.

Jana: the existing flag byte already atrophied

Jana tells a war story of middlebox that was classifying by using just the flags byte.  Allowed the signalling to complete, but then the data traffic was dropped.

MartinD: I didn’t hear a ton of pushback on declaring the extra byte bit now and move it to the front.  (Acclaim)

Lucas suggests we use it randomly to avoid atrophy.

Ekr: is the rule that it is set to 1 for all but the last flags byte?

Ian: that makes the quic header unparseable.

(Descent into possibility of abuse, using this for backchannel public data).

MT: what do we want to put into the public header?  Ian: nothing.

EKR: we need everything required to set up the cryptographic context.

Brian: moving to special packets prior to cryptographic context may reduce what you need.

Ekr: routing information and crypto bootstrap is required, and nothing else.

Jana: we haven’t demonstrated we don’t need more flags, just that ways exist without them

MT: want to see a strawman for an extra byte in the common (non-special packet) header before we add this.

Ted: going the special packets route runs us almost into the signaling/data protocol architecture, which is a slightly different model from the one we started out with. one of the risks is people who don’t care about the data start caring a lot about the signaling. that’ll ossify. we may want to do something for active defense against ossifcation. greasing helps

MT: we already have this problem. grease the hell out of it.

Lars: what do we put in the box?

MartinD: we have a dueling proposal thing going on at the moment.

Ian/Ekr Not sure it is dueling, as we will likely do both.  We do need to see a proposal for special packets.

ian: I think we’ll see two proposals for special packets

ekr: I have two proposals for special packets.
There are at least three types (special, key phase, normal).

### [Issue 62 - Finding Frame lengths](https://github.com/quicwg/base-drafts/issues/62)

Ian:  I think we have all agreed that fixing this is reasonable.  Moving all the elements that are required for working out frame length computation to the front.

Agreed, editor ready; there is a different issue (#168) that is a subset and can be closed.

MartinD:  calculate length by IP packet length or the UDP header length field.  What is passed to crypto is the UDP length field bytes.  This does not work with UDP trailers, but folks are okay with that.

### [Issue 70](https://github.com/quicwg/base-drafts/issues/70)

Lucas: there are a few frames that don’t make sense more than once in a packet.

Mirja: i thought you could have per-stream and per-connection information

ekr: either it’s a bucket of things that are typed and conceptually similar or it’s two buckets

MT: you can save some space by doing this

Jana: here’s what it’ll look like. packet header, public part and private part. pieces are varlen and can be turned on/off with flags.

ekr: maybe if there’s enough stuff that’s common in every packet, then frame encoding is bad. that’s the intuition behind the common header. you could also have just a private header frame.

Jana: difference is the private header appears in the top of the packet

Marten: two things: ack frames, and window updates. so we save a byte.

ekr: if you want to encipher the packet number with ECB, you could add this to that block. *cringes*

Jana: A reason not to do this. Upgrade to new stream frame type, with 0rtt connection, you don’t know if the other side supports the frame.

ekr: frame lengths are frame specific

Jana: if you’re reading a frame and you can’t parse the frame, lengths help. in SCTP we moved from SACK to NRSACK, this might be useful for something like that.

ekr: do you have to consent to me sending you new frame types?

Lucas: if we want to introduce a new frame that’s connection-wide, we’d have to put it in the extensible

Igor: private header with fixed structure… ?

resolution: to be opened if new information.

#108 max stream number

jana: use case, many small streams. streaming audio, etc.

ekr: if we’re designing for many small streams to send a video frame or a voice packet, you shouldn’t send a pile of stream closes in the other direction. we should open an issue for that.

MT: maybe the application knows on both sides it can close. this AT_CLOSE state in the doc, that isn’t described anywhere. have a PR to remove it.

Jana [surprised] are you saying the document is incomplete?

ekr: write up the sending patterns so we can understand the design constraints

Lucas: why do this?

Ted: Let’s use audio as an example. Codecs break into short chunks, say 20ms. Each of those 20ms things, if it drops, i don’t care. You could design something where you have one stream per frame, frames sent independently.

Lucas: Why do you want to do that without in-order reliability...why are you using QUIC then?

Jana: Nice property, if streams are cheap, you get message orientation. 2^64 makes streams cheap.

Brian +1

Jörg note that with 2^32 you get 2^26s of 20ms audio frames

Ted: I think the motivation for this is a different application, make sure we’re not shutting them off. I agree with ekr, this tiny question is much smaller piece of the whole pie of the “does this protocol fit this use case”. we can’t tackle that whole thing. So we can use 32 bits, and just rev the version. versions are cheap.

ekr: persuaded by ted. make sure we document that streams should be cheap.

Kaoru: any requirement coming from key update? does number of streams influence that?

ekr, mt: no

### time format #109

there’s code for uf16 in the issue. proposal is scaled integer. Marten notes that some things are delayed more than 65ms on host. we’re wasting bits with a linear format, don’t need microseconds to express “slow”. an exponential format makes sense here.

Ian: scaled integers are reasonable. no strong opinion.

Lars: for TCP, we have microseconds now because scaled ints don’t work in datacenters. we might have a similar problem.

Jana: Marten may be right, but 65ms is useful.

Marten: 2 sec RTT on mobile?

Lucas: Ack delay, doesn’t depend on RTT.

Jana: you can scale to 10ms units, then you get 655ms.

Ian: If we’re going to fix this for all time, then I’d rather use u16.

Lars: if we want the current format then we need to write it up.

Jana: The floating point format seems like it’s a haven for bugs.

Ian: Can Lucas verify that Mikkel’s code is good?

Lars: Does anyone have a problem with this

MT: YES! I have two pages of text for sixteen bits in the code.

Brian: This is the most complex bit of machinery in QUIC other than crypto

Ian: Negotiation would be worse

Resolution: Let’s document and revisit if we see lots of bugs or get pushback.

### Interframe padding #158

ekr: i’m antsy about the number of frame types we have.

lars: we discussed an experimental frame type. ff -> frame has a length. other way to define this

ian: what about a one byte padding frame?
you have to touch all the bytes after it.

jana: can also just say padding frame is zero but then you have to scan one byte at a time to the end of the packet.

ekr: could also say a codepoint means rest of the frame is garbage
resolution: zero byte in packet context -> padding.

_ekr moves to adjourn_

###  Issue 144

... was marked as editorial

### Issue 169 response to loss handshake packets

Lars: notes 2 and 3 in issue are not operable

Ian: I can add more text

SI: can’t ack the version negotiation either

Ian: is that its own issue?

SI: I can open its own issue - you can merge

Lars: 17 issues cleared, 21 new opened during the meeting. Congratulated ourselves on making progress.

Mnot: next interim likely june 6,7,8 needs to be confirmed Paris @mozilla
