# QUIC Interim Meeting Minutes: June 2018

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Morning 2018-06-06](#morning-2018-06-06)
  - [Topic I: Interop Report (Kazuho Oku)](#topic-i-interop-report-kazuho-oku)
  - [Topic II: Editors Report (Martin Thomson)](#topic-ii-editors-report-martin-thomson)
  - [Topic III: Stream 0 Design Team (Ian Swett)](#topic-iii-stream-0-design-team-ian-swett)
    - [Flow Control for Handshake](#flow-control-for-handshake)
    - [Empty ACK](#empty-ack)
    - [HANDSHAKE_DONE](#handshake_done)
    - [Packet # Encryption/Spaces](#packet--encryptionspaces)
  - [Handshake Examples (EKR)](#handshake-examples-ekr)
- [Afternoon 2018-06-06](#afternoon-2018-06-06)
  - [Topic IV: HTTP (MikeB)](#topic-iv-http-mikeb)
  - [Topic V: QPACK (Alan)](#topic-v-qpack-alan)
    - [904/1355 New Static Table](#9041355-new-static-table)
    - [1343 Static Table Negotiation](#1343-static-table-negotiation)
    - [1371 Tracking header blocks for resent stream](#1371-tracking-header-blocks-for-resent-stream)
    - [Interop](#interop)
- [Morning 2018-06-07](#morning-2018-06-07)
  - [Topic VI: ECN Proposal (Magnus)](#topic-vi-ecn-proposal-magnus)
    - [ECN Ack Frame](#ecn-ack-frame)
    - [Capability Check Verification](#capability-check-verification)
    - [Continuous Verification](#continuous-verification)
    - [Congestion Experienced](#congestion-experienced)
    - [Connection Migration](#connection-migration)
    - [Issue: ACK Frequency and Recovery Period](#issue-ack-frequency-and-recovery-period)
    - [QUIC ACK Frequency Considerations](#quic-ack-frequency-considerations)
    - [Receiver Tracking of Recovery Period](#receiver-tracking-of-recovery-period)
    - [Blackhole Mitigation](#blackhole-mitigation)
    - [Conclusion](#conclusion)
  - [Topic VII: mvfst (Subodh)](#topic-vii-mvfst-subodh)
  - [Topic VIII: WG Planning](#topic-viii-wg-planning)
  - [Topic IX: Load Balancer (MartinD)](#topic-ix-load-balancer-martind)
  - [Balance of Time: Issues (MartinT)](#balance-of-time-issues-martint)
    - [1342 implicit open page 6](#1342-implicit-open-page-6)
    - [58 frame type extensibility (page 8)](#58-frame-type-extensibility-page-8)
    - [1016 - initial_max_stream_data](#1016---initial_max_stream_data)
    - [1296 negotiating packet number protection (slide 12+)](#1296-negotiating-packet-number-protection-slide-12)
    - [Long Headers and ICMP](#long-headers-and-icmp)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Morning 2018-06-06

*Scribe: Eric Rescorla*

### Topic I: Interop Report (Kazuho Oku)

Interop on 3 versions

* draft-11: ATS is now improved, otherwise same as before
* draft-12: 4 implementations. Problems with PN encryption. Should have provided test vector
* draft-11 + Stream0 DT: Minq and Quicly reached interop with both 0-RTT and 1-RTT, but no Retry

### Topic II: Editors Report (Martin Thomson)

See [Martin Thomson’s slide preso](https://github.com/quicwg/wg-materials/blob/master/interim-18-06/editors.pdf)


### Topic III: Stream 0 Design Team (Ian Swett)

[Presentation](https://docs.google.com/presentation/d/176bVI27bRJrfahf8RR89hbZ_owMs54ipxXALNUUsV1c/edit?usp=sharing)

Assorted notes that may not be in slides:

Early versions of this in PicoTLS, Minq, BoringSSL. NSS, OpenSSL will be in nightly soonish. OpenSSL is probably the furthest behind.

Huitema: Need to tell people not to get clever and merge the ACK structures.

EKR: The current slides actually miss the destination connection ID in the Retry token to avoid DoS attacks. Will fix slides.

Some questions we don’t seem to have too much clarity on:

Why multiple retries? Cascading retries?

Should you be able to change CID on multiple retries?

Hardie: do the tokens have to be self-contained?

EKR: No, but they have to be unforgeable.

Jana: I just noticed you can only change CID on the first retry? Is that a good idea

EKR: Not necessarily, but we wouldn’t be able to use the same anti-injection mechanism.

Recording: Open issue. how many retries should be allowed.

No strong consensus in DT on one Initial type versus >1

*BIO BREAK*

Mark Nottingham: DT output has no special status

There was a request for detail of the handshake. EKR volunteered to do a presentation about this. Tomorrow?

Ted: Who is going to analyze this? EKR took action item to liaise with academics

Gabriel: We (Microsoft) are in favor of this, though it will be a big change. Let’s try to minimize big changes going forward.

Consensus call: Does anyone object to going forward.

No objections.

**Consensus: We will go in this direction modulo the open issue Martin raised + the separable issues.**

Now move on to the separable issues and pick up PN spaces later.

#### Flow Control for Handshake

*Long discussion*

**Consensus: Do nothing in QUIC but punt to TLS WG and let them handle it.**

#### Empty ACK

Kazuho: Can’t we just send a coalesced packet in the lower space.

Proposal: Punt this to v2 and Ian will explain how to use coalesced packets. Then we can take a look at whether the proposal works.

#### HANDSHAKE_DONE

Conclusion: You should not discard keys earlier than 3RTO after the handshake is complete unless you have a signal that the other side has the keys. Martin Duke to write examples of signals.


#### Packet # Encryption/Spaces

*Long discussion*

**Consensus: Continue with separate packet number spaces; there are some reservations from MT and Christian? It is legal to use a single sending counter if you want.**


### Handshake Examples (EKR)

[Presentation](https://github.com/quicwg/wg-materials/blob/master/interim-18-06/quic-flow.pdf)

## Afternoon 2018-06-06

*Scribe: Sean Turner*

### Topic IV: HTTP (MikeB)

[Presentation](https://github.com/quicwg/wg-materials/blob/master/interim-18-06/HTTP.pdf)

Principle: HTTP/QUIC is like HTTP/2 except when it is not :)

Dropped flags from HTTP/2 because it’s in the transport layer.

mnot: What about HTTP/2 Extension frames?

Lucas: ALTSVC and ORIGIN frames don't define any flags. 

mnot: [CACHE_DIGEST](https://tools.ietf.org/html/draft-ietf-httpbis-cache-digest-04#section-2) does, something for the authors to watch out for.

1 byte per frame saving if we go with the proposal.

Conclusion: Define flags inside priority, not in every frame type.

Principle: Application layer shouldn’t need to “grab” a particular stream by ID.
Can’t combine control streams because either side can initiate.

Dmitri: It’s not actually simpler; you’re in limbo until you read the 1st byte.

MT: It made my code simpler.

Robert: 1) Order and in-order are subtle different.  This would require that something be interpreted as in-order. 2) It’s difficult how to drop into the middle of a session and debug.

McManus: It’s a nice extension point.

Conclusion: There’s some nervousness, but we will continue discussing the type byte proposal on list.  Comments are welcome.

Principle: See 1st principle.

Priority doesn’t work well with QUIC.

4th option (not shown on penultimate slide): restricted form of HTTP/2 priority to only allow dependency on placeholders.  Doesn’t work well for video, others.

Conclusion: This needs to be done in consultation with httpbis, at the least.  Present to them in Montreal.

### Topic V: QPACK (Alan)

[Presentation](https://github.com/quicwg/wg-materials/blob/master/interim-18-06/qpack%20update%2006.18.pdf)

Clarification Questions:

Decoder can limit Encoder’s use of acknowledged header: yes

Why is there a length on the instructions: Some HPACK decoders have issues if instructions are partially received.

Can we get in a deadlock position with flow control: potentially?


#### 904/1355 New Static Table

1st flight is what it is used for request headers but not much beyond that.

HPACK was 61

How many fit into first byte 16 or 62ish

Highly browser specific!

Where is diminishing returns come into play?

**AI: mnot suggests Hooman get some #s.**

#### 1343 Static Table Negotiation

Nobody has asked for an alternative table.

Transport Parameters - put the ….

Conclusion: QUICv2 for more than one!

#### 1371 Tracking header blocks for resent stream 

Conclusion: Option 2 doesn’t fully work.  Discuss over beer.

#### Interop

Call Alan if you’re interested in Interop!

## Morning 2018-06-07

*Scribe: Brian Trammell*

### Topic VI: ECN Proposal (Magnus)

[Presentation](https://github.com/quicwg/wg-materials/blob/master/interim-18-06/ECN%20for%20QUIC%20-%20interim-18-06.pdf)

See PR #1372: https://github.com/quicwg/base-drafts/pull/1372 

#### ECN Ack Frame

Lars: Do we need an ACK-ECN frame, or can we put ECN in ACK frame? Zeroes back are also info, and are efficient (varint, three bytes). In majority of cases, ECN works.

Brian: Two issues here. Path impairments are rare. Stack impairments less rare but will become more rare. Two frames feels mainly like it’s easy to write, not a great reason.

Jana: Even if peer doesn’t want ECN, would still have to send extra bytes.

MikeB: no difference between new frame and flags in frame itself

Ian: new frame type might be easier to implement

Lars: If you make ECN look optional in the spec, then people will treat it this way.

Roberto: A bit sad to me that we are solving ECN for quic. Debugging issues are linked. Allowing additional debugging information would be nice. ECN doesn’t belong in the application protocol. Belongs in a layer that the network knows about and reacts to. 

Lars: Aggregating ECN marks and what you do with them is certainly transport.

Roberto: Yo it’s good that we’re solving ECN, we should handle debug too.

Brian: QUICv2.

Brian: Can we solve Lars’ layer 9 problem by renaming: put ECN in the ACK frame and having a smaller ACK frame (short ack = SHACK or small ack = SMACK.

Jana: ACK-ICN (implicit)) for cases where ECN didn’t work?

Martin: Maybe have a flag that says the ACK frame contains an ECN counter update.

Lars: No separate frame type 

Martin: ACK block count goes back from varint to one byte, high bit means ECN counters are present.

MikeB: this complicates reliable delivery a bit...

Jana: You don’t want ECN changed, you want ECN information present.

Christian: We spent some time to prevent optimistic ACKs, does ECN reintroduce this?

Jana: Fundamental issue with ECN: endpoint can mark to get better treatment and ignore. Let’s not litigate ECN here, but that’s a reason a peer might decide not to participate.

#### Capability Check Verification

Lars: Is there any benefit to turning it off when not capable?

Magnus: yes, otherwise you’re not playing fairly.  Network will prefer the ECN traffic, but not actually get the payoff of a ECN-behaving client.

#### Continuous Verification

Magnus: packet duplication makes this hard, you can get slop in the counters, list discussion on this ongoing.

#### Congestion Experienced

Magnus: Classical ECN behavior, but we can do experiments. Text points to 8311.

#### Connection Migration

Magnus: new paths start with capability check, if already working then continue in continuous verification.

Brian: Is there a linkability problem here?

Magnus: No, always ECT on path probing. 

Christian: Is it possible to set CE in order to ensure it makes it to the end of the path?

Magnus: Hard. Stack might allow ECT but not CE.

Magnus: Probe not yet fully spec’d out, blackhole mitigation is impossible. As currently laid out, mark probes too.

Brian: The bit of information that leaks here is that the endpoint doesn’t support userspace ECT, which is not much.

#### Issue: ACK Frequency and Recovery Period

Ian: Any time a packet is newly missing, an ACK is sent immediately. It might make sense to treat a CE counter increase the same, this fixes the ACK frequency. Let’s split off the details of ACK frequency optimizations for this mechanism from this PR. 

Magnus: This is a very simple rule…

Jana: Spec says this

Magnus: PR doesn’t yet.

Ian: Treating CE marks as much as possible like newly missing packets is a good idea.

Jana: With a loss, you want to send a few immediate acks, with CE one should be enough.

Magnus (AI): will update this PR to say this

Kazuho: Issue here: as you transmit more packets, cumulative counters get bigger, more overhead, higher ack frequency means this hurts us more. Alternate design (bitmaps against inflight map) would work better...

Jana: Hard to compress. ACK loss.

Kazuho: Can only carry bitmap for newly acked packets

Jana: need some more redundancy to account for ack loss, but this seems better than current scheme.

Magnus: Being explicit about which was marked doesn’t give you much from a CC standpoint. Cumulative counters get bigger, yes, other encodings might fix that (such as truncating and reporting low bits). I want to get to a baseline, then talk about the details.

#### QUIC ACK Frequency Considerations

Magnus: this NOT ECN, came up during design process...

Kazuho: why RTT/4?

Magnus: maintains recovery period for ECN is the starting point. 

Kazuho: Could be 2 or 8?

Ian: GQUIC changed to always using RTT/4, totally independent of Magnus’ work, did not check RTT/2, RTT/8. In practice fairly similar, /4 had identical app performance, fewer ACKs. Coupled with ack per ten, but this works well because we use BBR. We chose minRTT, not sRTT, so would need to rerun experiments. Did not recommend lower bound, need to do that. Would set it based on expected timer granularity. In userspace on most systems 1-2ms is expected.

Christian: Using minRTT instead of sRTT is better, because it does not have the feedback loop. 

Patrick: We also used RTT/4, but move to ACKing every packet on out of order.

Jana: Reno and Cubic have bandwidth limits related to ACK frequency, must compensate for that. Whatever we do here, we should have recommendations on how many packets can be 

Magnus: 

ekr: Document should describe an algorithm that will work well, not necessarily optimal, okay if quasi-normative, but I would be very sad if as an implementor I had to figure out RTT/4 myself.

Subodh: We also choose 4, with a floor and a ceiling on RTT freq.

Martin + Brian: Let’s just write down minRTT/4

Subodh + Patrick: we’re SRTT/4

#### Receiver Tracking of Recovery Period

Magnus: this is not a good idea.

Issue: Packet Duplication
Magnus: Duplication causes ECN counters to increment higher than packet count. Packet replay without racing could drive congestion window down.

Jana: This could be a legitimate mark as well

Brian: Pick an arbitrary deduplication approach and move on?

Magnus: you need basic duplication suppression at the receiver side. This is a hole in the QUIC spec. 

Martin: The protocol just continues to work with dups now.

Ian: We do reject dups, turns out to be easy. Packet number outside ACK block is just ignored. Window of out-of-orderness you are willing to accept should be in line here.

Martin: Very simple deduplication approach, just keep track of next expected packet, have an arbitrary length bit vector for earlier packets. Ian’s is based on plan-to-ACK.

ekr: IKE and DTLS have to do this as well. You could just point to those. I don’t want the spec to dictate an algorithm, but we could point to examples.

Martin: takes AI to fix this. Need to be careful about stateless resets...

Roberto: For the mic: I think this is a case where the correct behavior isn't actually obvious. Seems like we should warn implementers that duplication can happen. Look out for it.

#### Blackhole Mitigation

How many packets to send with ECT on handshake before falling back to non ECT?

Martin: One is a good number.

Roberto: If we want people to implement this stuff, don’t add complexity for exceedingly marginal benefit. why not just say that if the path doesn’t support ECN it doesn’t support QUIC?

Kazuho: Assuming we do path migration, this is a MUST.

#### Conclusion

Unanimity that we should add ECN, just working on the details.

Roberto: If we believe ECN has positive benefit, then it is reasonable to tie the use of QUIC to the non-blackholing of ECN on the path. This is simple, and advances the proper thing.

ekr: what is the standards content of this? 

Roberto: I’m speaking specifically about blackholing. If it is blackholed, then you don’t get QUIC.

Jana: As a QUIC stack you still need to be able to set the bits in IP header, and read them.

Lars: Your stack might blackhole you

Roberto: Normal fallback to TCP on ECN blackhole. We will not attempt to recover.

ekr: Is this something implementors do, or something the standard requires?

Brian: Let’s call the fallback a MAY.

### Topic VII: mvfst (Subodh)

[Presentation](https://github.com/quicwg/wg-materials/blob/master/interim-18-06/mvfst.pdf)

Issue: setting the right idle timeout is hard, and idle timeout is underspecified. Ping interval can be longer than idle timeout. 

Suggestion: ping idle-timeout/2 to keep the connection alive, but this is an issue on mobile (don’t want to waste battery). Whether to keep alive is an application prerogative. 

Jana: Misalignment. Transport should be responsible for idle timeouts and NAT rebinding, but application needs to be involved now. 

MikeB: Refcount. Take a ref when the application is waiting for the server and the transport should ping stuff. Release the ref. Refcount zero: let the connection idle TO.

Action: Subodh to file an issue.

Jana: Tooling will be important. Need to do better than TCPdump and Wireshark

Lars: Plug for EPIQ (Lars, put a link here please): workshop on QUIC research. Tooling in scope.

### Topic VIII: WG Planning

Mark: Hopefully by Montreal we can start announcing that we’re getting close to done, and that any remaining implementers should come to the table. 

Mark: We’re planning an interim at NetApp in New York City the week of 17 September 2018. Two days of interop and two days of meeting. It looks like we’re not going to be done by Bangkok, so we’re starting to plan an interim the third or fourth week of January 2019 in Asia or Europe, people with facilities please talk to us. 

Mark: Target for next interop at Montreal hackathon? Will we be able to 

MartinD: How many stacks do PNE?

Lars: 3 or 4, exposed some other bug.

Jana: Drafts can come out in the next couple of weeks, but no Stream 0

MikeB: Do we want to do two separate interops? e.g. HTTP -12, or -13 over Transport -11, then Transport -12 or -13. Or do we want -13 with PR [missing], then -14 with Stream0?

ekr: I think we can have stream0 implementations before Montreal. We have six weeks. Not interested in interoping -12.

Lars: Let’s add some sort of migration for the remote interop between Montreal and New York.

Mark: Who’s driving the details of the next interop? ekr.

Lars: Someone needs to be the hackathon person for Montreal, I won’t be there: ekr.

When do the Stream 0 changes come in?

ekr: will drop a PR next Wednesday

ST: deadline for IETF is 2 July

Patrick: start implementing to a branch if we can’t submit a draft.

Lars: Also between Montreal and New York we should test ECN

Brian: Need standard test equipment/firewall/vm to mark CE

Ian: would also like to work on HTTP -13/-14 on transpo -11 in Montreal. If I know now that others will do that I can get people on airplanes.

Gabriel: can also do that, need to prioritize the app now too.

(on QPACK vs HQ)

MartinD: QPACK has fewer dependencies on the transport than HB

MikeB: so, QPACK in Montreal and HQ for New York.

### Topic IX: Load Balancer (MartinD)

[Presentation](https://github.com/quicwg/wg-materials/blob/master/interim-18-06/quic-load-balancers.pdf)

Seeking feedback on whether group is interested in problem statement and high level technical feedback on design proposed

Design choice: this could be dtls based - udp 443 is the key thing

Fundamentally the proposal is how a set of balanced servers communicate with LB wrt connection ids that can be routed back to those servers (i.e. a side control channel). Focus on diversely owned servers and lb

Subodh, igor, and martin d discussed algorithms for assigning cids

Discussion of whether this should be upleveled to something like REST or another management protocol suite that shall not be named.

Mike b: you may want a model where lb informs the servers of their assigned cids

Discussion of  whether the logical consumers of this are represented in the quicwg rather than hosting operators, etc..

### Balance of Time: Issues (MartinT)

[Presentation](https://github.com/quicwg/wg-materials/blob/master/interim-18-06/misc-issues.pdf)

Stateless reset oracles (page 2 + 3): 

Mt highlights man on the side copying the reset

Ian: sending to a different IP/cluster also does not work

Mt: this has interactions with group arrangements that mix anycast and unicast addresss (preferred address - Christian too)

Subodh, jana, kazuho all have suggestions on scope of keys. Text needed

Proof of receipt “simple fix” text will be coordinated by MT.

#### 1342 implicit open page 6

Do we or don’t we have implicit opens (currently?) -

General feeling is these aren’t very different - but we need to be clear

Marten suggests that protocols that come from tcp (such as spdy) require ordering and thus no implicit open

Kazuho prefers yes implicit open - more clear about state of stream that hasn’t appeared on wire

Subodh - senders (recommend) that streams are opened in order. Lets be consistent. Rst stream implicitly opens (and then resets) streams.

Jana suggests modeling implicit stream as an explicit stream with len 0, marten counters with concerns about reordering on receiver

Ekr: fewer funky behaviors the better - unidirectional streams serve the use case for implicit (he’s a no)

Gabriel / Nick: likes implicit and symmetry on both sides in face of loss

Mnot: can you not live with any of the options: 1 hum

Who prefers implicit open: lots, who prefers explicit open: a little

Strong preference declared by chairs for implicit open

#### 58 frame type extensibility (page 8)

Mnot asks who has strong opinions on outcome; ~8 hands raised

Kazuho wants only one way to extend quic functionality

Mt: right now transport params are the only mechanism. The question is adding frame types

Ekr: pushes back on all extensions should have access to a one octet encoding. 2 octets easily fit in a first come first served registry. Options 4 and 5 means frame types are asymmetric between peers

Subodh: does everything need to be negotiated? Mt says the frames don’t have standard length delims, so yes.. Option 1 might address but ruled out in MEL
Brian - can we bind extensions to quic version? 
Mt: in MEL we said we wanted a more fine grained mechanism

Mnot as individual - accuses the wg of overdesigning.

Viktor: regrets his own PR on the topic. We should copy tls extension mechanism as its proven to work well. EKR: we could do so literally as we’re using TLS

Martin d: notes extensions from client in the clear, and there is finite INITIAL space.. MT says plenty pre-post-quantum, already out post-post-quantum

Ian: also concerned about unilateral negotiation and redundancy

Mnot: idea here is give MT as editor feedback and him make a choice (which we will then debate again?)

Mt: leaning towards varint and registry(?)

Jana: this is a standard model - negotiate extension (top level feature) and N frame types fall out from that. Lots of yepping from the peanut gallery working group

Momentum builds..

Note that transport params that declare you support a feature have optional values for configuring the feature.

#### 1016 - initial_max_stream_data

Jana likes flexibility and likes default of 0.

Kazuho - patrick - jana - we should do it

Nobody voices unhappiness with that direction

#### 1296 negotiating packet number protection (slide 12+)

Kazuho: this exposes linkability of path migration - should we disable migration if pne was disabled?

Ian: thinks this most be bilateral; but prefers transport param over new version #. Also says pne is separable

Jana: doesn’t like tp. Separate version seems reasonable even with different vendors as long as you stay in the DC environment

Roberto: benefit if you do want linkabiity for debugging, its also a bet against quic being successful wrt hardware acceleration. Use a different version

Brian: seems to be vn is about package of base behavior and also a wire image. This is a wire image feature therefore this is VN not TP

Ekr: we’re already extensible so that someone else can do this later via ‘specification required’

Igor: seems like a viable option that the wg should tackle - big audience

Kazuho: don’t delay quicwg docs, make it a separate draft

Gabriel: separate draft is possible. There seems to be more than one entity interested. PNE is premature; without studying crypto offload. 

Mt: sounds like people would be open to reading a draft

Jana: not having pne means that packet 0 we still need to encrypt the long header

Brian: are we just trying to be hands off something we do like

Lars: there are actually a lot of details for a wg to work through

Ekr: I don’t want to figure out the security properties of quic with this axis

Mike b: tell proponents we’d be happy to review the document but unclear if we would be willing to adopt

Mnot - we need a list consensus call this is a prediscussion for the list - leaning towards a separate document not necessarily in the wg

#### Long Headers and ICMP

IGOR PROPOSES ALLOWING LONG HEADERS WHENEVER TO HELP ICMP

Kazuho: just prepend the short packet with a longheader corrupt sentinel

Subodh: unreachable is interesting as well as pmtud

Roberto: this isn’t congestion controlled - so use sparingly

Igor to send pr regarding pmtu and this approach

