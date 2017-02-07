# Minutes: QUIC Working Group 24-01-17

Chairs:  Lars Eggert, Mark Nottingham
Scribes: Ted Hardie, Patrick McManus

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

  - [Administrivia](#administrivia)
  - [Transport Introduction](#transport-introduction)
  - [Transport Issues](#transport-issues)
    - [Issue 74: Application-defined error codes CC](#issue-74-application-defined-error-codes-cc)
    - [Issue 104: Priority in QUIC Transport ND](#issue-104-priority-in-quic-transport-nd)
    - [Issue 51](#issue-51)
    - [Issue 45](#issue-45)
    - [Issue 45 and TLS as part of version resumed](#issue-45-and-tls-as-part-of-version-resumed)
    - [Issue 146 stream frame boundaries](#issue-146-stream-frame-boundaries)
    - [Issue 174 - stream reservation](#issue-174---stream-reservation)
    - [Issue 183 abstraction of TLS](#issue-183-abstraction-of-tls)
    - [Issue 135  Dos using version negotiation packets](#issue-135--dos-using-version-negotiation-packets)
    - [Issue 112 - greasing version negotiation](#issue-112---greasing-version-negotiation)
    - [Issue 124 alt-svc quic version hint](#issue-124-alt-svc-quic-version-hint)
    - [Issue 50 updating transport parameters](#issue-50-updating-transport-parameters)
    - [Issue 181 remove settings and settings ack](#issue-181-remove-settings-and-settings-ack)
    - [Issue 122 define transport parameters](#issue-122-define-transport-parameters)
    - [Issue 126 separate transport params for 0rtt](#issue-126-separate-transport-params-for-0rtt)
    - [Issue 117 - what is scup?](#issue-117---what-is-scup)
    - [Issue 35 - starting packet number](#issue-35---starting-packet-number)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Administrivia

9:30 - Start (doors open at 9:00)
Welcome, Introductions
Scribes, Blue Sheets, NOTE WELL

9:29  Side conversations on cipher suite negotiation and ALPN negotiation.
9:30 Mark notes that we’ll start in 5 minutes to allow folks to make their way in (abou 5 folks still not present)
9:31 White Blue sheets begin circulating.
9:35: Mark goes through logistics.  Lunch at 12:00.  Drinks/Coffee available.
9:37 Note Well
9:40 Introductions

Discussing the Agenda, chairs note that Transport/Loss issues will return on Thursday, so that some discussion today may be deferred to Friday when a deeper dive is required.  Parking lot issues will be assigned by chairs.

Jana asks if there is a need for a short discussion of “survey” on loss/recovery to ground discussion.  Lars asks if there is interest in the room, and ekr clarifies if this is QUIC- specific loss/recovery.  Question on the amount of time required?  30-90 minutes?  Ian asserts that he could do it an hour, and several folks indicate that half hour would likely be too short.  Lars suggest that it go at the end of the day, so folks can consider what is needed.    Ian wonders if this might be better done at the Chicago meeting, since slides for this would be non-trivial; Jana says that it might be an informal discussion today, since this a meeting that allows for that.

Lars notes that upcoming meeting will be 2x2.5 hours, with alternate room set up.  We’ll see if that’s possible, but it might go back to normal if no larger rooms can handle that set up.

(Slight delay: DHCP server is out of address, so Jana has no network, so getting the presentation is not working)

Back to logistics:  no arranged dinner, given both size of group (50) and lack of local knowledge.


## Transport Introduction

9:56  Jana goes through draft-ietf-quic-transport-01

- Changes from -00
- Network byte order adopted
- Reworked description of packet and frame layout
- Replaced DIVERSIFICATION_NONCE flag with KEY_PHASE
- Defined versioning
- Divided error code space

Slide on Replacing DIVERSIFICATION_NONCE

1 bit in Flags field of packet header

Required for QUIC crypto, no longer needed.

KEY_PHASE allows receiver to know which key to use for decrypting.

Only 1 bit, which allows only two keys, but this is not enough during handshake; further discussion in TLS draft, but it may move.

Question:  why is this in the packet header?

The handshake is TLS, but QUIC is the encapsulating transport.  After TLS negotiates keys, the keys are exported to QUIC.

ekr notes that this is the same as the EPOCH flag in TLS.

Jana suggests that there may be slightly more to explore on the relationship between QUIC and TLS.

ekr notes that without an in-order delivery guarantee, there is a chance that the packet train will have some packets encrypted with one and other packets with two.  This allows you to disambiguate without in-order delivery and without trying multiple decryption methods.

Question:  is there still space in the public header for making this 2 bit?

Brian:  there is a chance for flag bit recovery.

Jana: we don’t want to freeze the format so that we’re out of flag bits, so we need flexibility.

Brian:  this is something that can change, but we should note that negotiation bits are the hardest bits to change as versions progress.

Jana says that we will probably need to discuss how many bits are needed, especially in light of Martin’s comments on 0-RTT and ekr’s concerns.

Versioning

- QUIC versions are 32-bit value
- Versions with most significant 16 bits of the version are cleared for use in IETF consensus docs.
- 0x00000000 is reserved to represent an invalid version.
- First RFC form is version 0x00000001
- IETF drafts are created by adding the draft number to 0xff000000.
- draft-ietf-quic-transport-01 is version 0xff000001.
- Experimental versions of QUIC to be coordinated on github wiki

Concern expressed with this scheme that we are changing the way feature exploration can work; in TCP other forms of extensibility are possible without rigid versions.

Jana and Martin note that there are other extensibility methods contemplated, and so we may see extensibility via those other methods as well.

Martin:  there is another discussion of transport parameters, and that is the right place to do this type of negotiation.

Jana agrees.

Question: is this form of versioning also where you would negotiate crypto?

Chairs: it’s a bit early for that discussion, so let’s defer it.

For transport parameters, is this like TCP option negotiation?

Brian: yes, but be aware that TCP options don’t actually work as fluidly as you may imagine, clusters of parameters work better, especially with middleboxes.

Error codes:
- 32 bits long, with first two bits indicating the source of the error code
- 0x0000-0x3FFF: App-specific error codes. Defined by app protocol.
- 0x4000-0x7FFF: Reserved for host-local error codes. MUST NOT be sent to a peer, but MAY be used in API return codes and logs.
- 0x8000-0xAFFF: QUIC transport error codes.
- 0xB000-0xFFFF: Cryptographic error codes. Defined by crypto handshake protocol.
- Error codes from -00 renumbered.
- quic-transport-01 now has only transport error codes.

The original Google QUIC did not have this split; so this split is new and will be reflected in error codes in particular drafts.

Mike Bishop:  I had not understood connection close errors and reset stream to have different error codes.

Jana and Ian note that the error codes in 00 were connection close error codes, and the question of whether there is a different set of reset stream is open.

Ekr:  the experience of this kind of split is that it gets very difficult to assign the semantics to a particular code; in TLS, that separation didn’t work.

Mnot:  at the end of the day they are going to be in a registry, right?

Mike: given a QUIC connection that has different applications using QUIC, unless we want everyone to be playing in the same registry for “why I killed my connection”, there is no point in overlapping space for app-specific codes.  HTTP will be resetting streams for reasons unknown to the QUIC layer.

Ekr agrees that mixing transport and application, then yes splitting the space makes sense, but the host-local, cryptographic, etc. split doesn’t make sense.  Question on actual size and typo:  it says 32 bits and looks 16 bit, plus the error code ranges don’t work.

Brian agrees with ekr that the sizes here are probably too large.  Two segmentation strategies: code path creator and receiver code path.  If you select the second approach, the size goes way down and the receiver code path gets much simpler.  Having different versions for things like out-of-memory error etc. makes no sense.  Segmentation is good, but the code size is too large and the split inside the individual buckets is too fine grained.


Jana asks if we could have an action item to go through the error codes and simplify.

Martin Thomson takes an action item to create an issue for this.

Lars suggests that we come back on Thursday after side discussions.

Martin suggests that we will settle on a few dozen.

On loss recovery draft:  most of the work was in trying to make it more self-contained, so that you didn’t have to chase 14 external references.  Instead, the pseudo-code should be sufficiently complete to create a new implementation.  Note that congestion control is still a pile of to-dos.  Especially if you are familiar with TCP loss recovery, please read and make sure it works.

Ian:  this is moving toward pseudo-code to make it more useful.  If this is the wrong direction, please say so as soon as possible.

Brian: self-containedness is good, but with this audience, but there needs to be some introductory material (so self-contained but not just pseudo-code).

Lars: if someone can read your text and get the same pseudo-code, then it is good.  It is an aspiration, though, and we may not get there.

Jana says that the pseudo-code is illustrative of the algorithm, rather than a drop-in for creating the code.

Lars notes that they don’t have to be standalone, they can refer back and forth to each other.  Marten is somewhat concerned that we will standardize loss recovery.  In TCP, there is a lot of scope for innovation at one end.  If we move away from stop waiting, that may get harder.

Ian suggests that stop waiting and loss recovery are not as intertwined as you think maybe two slides on that would help?  Ian also notes that there is something that we consider a reasonable baseline doesn’t mean that we are trying to ruling out innovation.  We want that innovation to consider, but it has to start from QUIC’s primitives and terminology rather than just starting from TCP.

Lars:  TCPM is trying to consolidate the different documents.

(Mike shows off his toddler).

Jana says that there is a real question about what will be normative in this draft.  What we do we want to describe as normative, given that there is no requirement to use a particular loss requirement in TCP.

Mirja suggests that maybe loss detection is crucial to protocol functioning, but loss recovery may not be as central.

Ekr are we are all trying to achieve the same thing:  we are trying to get to a point where slavishly following the docs we gets me a reasonable implementation.

Jana adds without closing out further updates and innovation. Mirja says that loss detection requires protocol mechanisms and those have to be defined and what you do with that is up to you.

Spencer says that what you have in the spec should be plausible on how you detect loss and what you do if you want to recover, but we want to have later documents that extend that.

Patrick says that he would encourage as much normative text as possible.  Some of the variance is exploration but some as well is just folks deciding which bits of the optional text to implement.  Avoiding that is useful.

Mirja says that the transport document alone should have enough to produce a conforming implementation.

Lars and ekr say that enforcing that this go forward without a split is not a high priority.

Ian says that keeping the split lets things like BBR to go forward without updating the basic transport draft.

Mark as chair says that this is primarily an editorial decision, and the editors can take advice, but will make the decision.

## Transport Issues


[Issues list](https://github.com/quicwg/wg-materials/blob/master/interim-17-01/transport-issues.md)

### Issue 74: Application-defined error codes CC

Number 74: the editors believe that we have consensus to carve out space for application-specific error codes.  PR has been incorporated into the draft.

Martin:  has anyone suggested that these be split by method completely, a la HPACK?

Mike no, you get some  issues with that, as we saw with HPACK.  Martin:  this is a fine design.

Lucas:  just a confirmation that the same error codes could be used with different meaning in different protocols.  Would we want them to be non-overlapping.  Pick non-overlapping as a goal, but this is not a guarantee?  That seems to have a good support.  This will be tagged as interim-consensus/closed pending objections.

### Issue 104: Priority in QUIC Transport ND

104:  HTTP/2 Priority implementations tend to withhold data from the buffers so that high-priority streams can be inserted.  It would be nice to avoid this in QUIC.  This would not show up on the wire, but would be useful.

Jana notes that there are two different questions:  does QUIC need to expose stream priority on the wire and does it need to understand application priority.

Ian asks if this requires a defined API between application and QUIC transport, so that an application knows what facilities the transport provides.

Marten notes that there is no reason someone who has an existing HTTP/2 browser couldn’t simply use the same QUIC priority and do all of it at the layer above.

Mirja:  what about retransmissions?  Jana: at the moment, they are prioritized above all other packets, which may not be correct in all cases.

Jana:  even with stream prioritization, an application has/may have a different view of retransmission than of new packet data.  Ian note that there are two different ways of defining this:  QUIC can own all the buffers, and the application has to be asked about what to send next in all kinds.  The other view is that all the buffers list in application space, and it has to manage filling the buffers.  Which upcall API you use is different, but it looks the same on the why.  A third method is that the applications shoot data at the API with priority indicating so that they can fire-and-forget.

Jana: all of this is specifying what kind of API we want to have.  We may want a functional API.

Lars: what happens when you get two streams of equal priority.  Is it random, do they get equal resources etc?  This has not worked well, other than background class.

Patrick notes that the HTTP/2 system has very complex methods.  Martin:  is the application really should we have stream priority in QUIC? Yes.

Lucas asks it is sensible to have the receiver indicate priority schemes?  Ian notes that there are HTTP/2 use cases for changing use cases.

Lars/Jana an all encompassing priority at the quic layer, if we make that choice, would anyone be unhappy?

Ian doesn’t want on-the-wire priority.  It doesn’t impact the protocol much, but does change the docs and APIs.

Patrick:  it does impact retransmission.

Igor: is all of this something that needs to go into the document?  If we don’t put it on the wire, it really doesn’t matter.

Mirja:  two different simple schemes like strict/round robin would help people, if there were a simple API for that.

Jim Roskind:  there are questions here whether retransmissions should be starved for certain kinds of transmission, so partial reliability is not the only case here.

Marten:  is this implementation specific?

Igor: may be application specific.

Marten:  if there is a simple, small set that may be useful.

Jana:  can we punt this as an API discussion to later?

Question: what’s the difference between this and loss recovery--that’s similar, but there is prior art in TCP, where there is no prior art here.

Jana: we still may want to prioritize stream 1 because it is the crypto API.

Praveen:  we may want a separate document on APIs.

Marten:  we need something, because I could otherwise end up sending all stream frames and no acks.

Martin Thomson: we are dead on stream 1 after negotiation is complete.  Session tickets is another.

Mark: we are at diminishing returns in this, summarized into the issue, but the issue is left open.

### Issue 51

Seeking consensus on version number scheme as documented and described?

Brian: we need to have a discussion on version number packet layer encoding, but as a logical system it is fine.

Friendly amendment from ekr to go ahead and reserve the Google QUIC versions;

Martin says that those are in the wiki.

Discussion about whether this needs to be in the draft as well.  Reservation seems to be uncontroversial.

### Issue 45

Seeking consensus on how to confirm that two QUIC peers opening a handshake know which handshake protocol to expect.  The version number will be used as a proxy for this, so that the transport layout implies this.

Roy:  this is very large space, why not reserve a few bits just for this?

Ekr  I think reserving bits actually makes this worse.

Jana:  doesn’t the UDP port imply a handshake protocol.

Ekr:  I think it would be useful if the version alone specified the handshake.

Jana: if you are getting something on 443, you should not expect anything magical there.  There is ancillary information.

Ekr:  why would you want the behavior you are espousing?  If 449 were kerberos with shmls, rather than TLS, how is it being signalled with the port valuable?

Martin:  how much do you want the server to know before it processes the packet?  Does it know that it is QUIC or QUIC+Cryptographic handshake.

Ekr:  the port number never gets validated by the cryptographic security layer; an attacker could change the port number and get a different cryptographic behavior.

Jana; how is this different from TCP?

Mike Bishop:  technically ALPN allows you to negotiate more than one app protocol.

(Someone else):  SSH over QUIC might use TLS or the other SSH handshake protocol, which would be a use case for having multiple cryptographic handshakes over a single port.

Mark:  one of things we did in HTTP/2, we had a discussion early on how we felt about ALPN.  We agreed there that ALPN strings were cheap, and that allowed us to move forward on many things.  We don’t need to make the same decision here, but if we have a large version space, we could make them cheap.  Not quite as cheap as ALPN, but cheap.

_Lunch break starts; will at end 13:00 JST._

### Issue 45 and TLS as part of version resumed

Jana does not see why we need to tie TLS to version - port is sufficient and existing model.

MikeB points out that using versions is the way goog will have to mux between google-quic and ietf-quic.

Mirja points out that is the only way to evolve.

Jana wants one wire format to be able to point to multiple handshakes.

Ted points out that number of handshake changes are going to be fewer than other parts of the protocol that will rev.

Ted and Jana agree that we can standardize stream 1 as a handshake protocol, but Jana doesn’t want it to be required to be TLS.

Jana points to SSH as an example; port 22 is sufficient there.

EKR says you’re definitely going to need a new rfc for that (version number is the easy part).

MartinD says the point is to not reopen the transport doc, even though a replacement for the TLS doc of course is needed.

Do we want to make the crypto handshake negotiable?

Mark asks: should the version of the crypto handshake being used be tied to the version of quic? Hum?

Martin says its really the reverse (quic version implies crypto handshake)

Hum for support quic version identifying particular handshake and Against:  for marginally stronger but no clear consensus. Move it to the parking lot or revisit as things come up - non conclusive.

### Issue 146 stream frame boundaries

Mikeb: application does not get semantics on boundaries - issue is about error handling..

Mt: can you reframe by coalescing and splitting in a different way - which results in retransmissions getting partial data you already have. Ian: Existing google-quic implementations will fail on this.

Lars: why would we do something different that tcp?

Jana: spec is inconsistent - mostly by defining this error code.

martinD what is the use case for this?

Jana: overlapping data that is inconsistent.

Ian: debugging for multiple sessions with same connection id(?) on unencrypted handshake packets

Lars: MAY does not accomplish anything.

Ekr: spec should require a consistent data stream, though reframing and coalescing in any way is ok.

MartinD says strike the error code.

Resolved in favor of option 2

### Issue 174 - stream reservation

Mt: quic state machine is different than h2 but it picks up the stream reservation concept. Moving that to the application layer would simplify quic state machine. Applications would need identifiers independent of stream ID. mnot thinks this is ok from http layer.

Jana: streams are not necessarily created in order from pov of receiver.

Mt: what value does reservation have for transport stack?

MikeB: API is going to need concept of gimme a stream even though I don’t have data to go out.

Ted: unclear how much this simplifies state machine, but could clarify API to see what is in send state vs reserved state.. And that lets you use the same identifier space.

Mt: says that doesn’t let you police the creation order and receiver needs to be prepared for anything and that has state management implications (i.e. ddos problems).

Ted suggests heuristics about windowing of stream ids - resetting streams you haven’t seen arrive yet.

MartinS says what happens when 1 peer sends a frame for stream id 2^30 does that force peer to reset all lower numbered streams (modulo window).

AlanF says you wouldn’t reset anything without headers, but what is the generic app independent approach.

IanS says current implementation as receiver reserves up to the highest stream you have received anything for that. Everything underneath that needs to be closed (recvs rsts) or open. A reserved stream is essentially open.

Hooman - is there a non h2 push application? Mt: can application talk about streams in a different order than the transport deals with them? Artur: if client does something reasonable - CONNECTION_CLOSE

Mt: my suggestion says move it to h2 layer.. Downside is need new identifier space.

Ted points out that quic transport can’t help smoother this stuff before the application when in need for resets.

Consensus this path is worth pursuing let’s see the PR - need h2 mapping draft changes to deal with reset case

### Issue 183 abstraction of TLS

Same as handshake discussion - lets come back to this on thursday. Ian thinks its orthogonal. Still coming back to it on thursday :)

### Issue 135  Dos using version negotiation packets

Mt: reject from a server could be the request from a client. You can end up with 2 servers talking to each other.

MartenS - no way to distinguish between version negotiation and a request from a client you can’t parse.

Mt: client can pad, server doesnt have to. martinD says you don’t consider a non-padded packet as client request - early fail.

MartenS says this will need to be a persistent quality for all new versions.

Ekr thinks the packets should identify which party (c/s) they are from.

MartenS also suggests abusing reset flag; mt is tempted.

Ekr says cost should only be on handshake packet.

Goal is to identify directionality, including making version negotiation packet bigger as that’s a corner case. (first offered version is a reserved magic number).

Briant says 136 is related and might help resolve.

Ekr goes back to chelo needs to be large/padded for anti-reflection reasons and its OK to use that send explicit directionality info there. No need to be that clever about where to stuff this information. Consensus to say version bit means we have 8 bytes of version + magic instead of 4 bytes of version (in one direction). (or something similar) This is fixed forever as part of public version interpretation info.

### Issue 112 - greasing version negotiation

Clarification discussion about technique and reserving code points. No real concerns offered.

### Issue 124 alt-svc quic version hint

Mike b - if client ends up with stale/bogus hint for a non optimal version does that work as a downgrade.

Ted: is this persistent?

Mirja: higher versions are not necessarily better unlike in crypto.. Just different.

Ekr: client would need to have supported versions in client hello.

MikeB likes sending it in client as that would allow either one of them to force an upgrade..

Eric concerned that they don’t mutually agree on which is better. Ted thinks decision should be in the hands of just 1 peer to avoid endless tussle.

Jana talks about ideal and experimental versions going out in parallel.

Ted points out client has enough information because server sends the full list of its capabilities - so it can make a decision. This can be flipped if client includes its supported version list in hello.

Discussion focuses on which peer gets to make the decision. Argument made that the client hello has a lot more space to burn. This perfect information makes unauthenticated hints acceptable.

Ted seeks to get us to agree that one of the parties should play that role having perfect information during version negotiation not considering alt-svc. (nodding of consensus and strong hum). Means alt-svc does not need to be authenticated

_BREAK 1510. RESUME 1535_

### Issue 50 updating transport parameters

Ekr: do we need a settings frame for quic transport? Mt: is it okay to do some of these more than once (connection flow control?)

Consensus that we are ok with these being fixed for now.

### Issue 181 remove settings and settings ack

Mt: there are just size of header table and ?? left, can they be moved to transport parameters and remove settings/ack from h2 mapping. MikeB - has implications for extensions. Otherwise we need per stream markers to indicate sequence point for settings ack.

Ted: how large is the optimization? Jana: problem is quic specific - related to the ordering.

Mt adds other problem: client settings are in clear-text.  Not okay.  Suggests making SETTINGS only at start of connection, constraining server from using a stream other than stream 3 until it has seen the client’s SETTINGS. Maybe.

If header table size is the only mutable element, maybe build something just for qpack within qpack.

### Issue 122 define transport parameters

Jana: gives blob some semantics for tls interface. Consensus to factor out and merge that part; other pieces are still under discussion.

### Issue 126 separate transport params for 0rtt

Mt: when a client does 0rtt what terms does it use. Defaults, leftovers from last time, negotiated params specifically for case of 0rtt. PR says leftovers for max streams and flow control.. Otherwise defaults. Some things don’t have defaults - so leftovers are impt.

Jana - risk is server will have to refuse more streams, but life will go on.

Ted - other option is to create defaults for 0rtt

Ian - out of band key exchange could also out of band transport params.

martinD - loose MAY cache language..

Lars - rather have MUST to do 0RTT

MartenS - in 0RTT would the client learn a changed value? Mt: yes, because you do full handshake exchange, just async to client sending..

Mt: notes you enforce this by binding the cached value into the ticket.

Mnot: clarify MUST is on client, server does not have to enforce

Ted: do we need machinery for setting defaults as opposed to here’s what you might have right now.

Tldr -   client SHOULD cache, if not cache use defaults.

### Issue 117 - what is scup?

Consensus - goog proprietary. Kill it.

### Issue 35 - starting packet number

MartinD - avoid packet number wrapping as long as there is a 0 bit at the front.

mikeB - points out this is in conflict with identifying initial packet on LB. but now that version flag serves that purpose

Jana - what is the initial ack block range (how does the receiver know this is the first packet)
No resolution



