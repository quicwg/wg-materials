# QUIC Working Group Minutes - IETF104 Prague

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Tuesday](#tuesday)
  - [Interim Meeting Planning](#interim-meeting-planning)
  - [Hackathon / Interop Report](#hackathon--interop-report)
  - [Editors' Updates](#editors-updates)
    - [Discarding Old Keys - Martin Thomson](#discarding-old-keys---martin-thomson)
    - [Recovery Draft from ian](#recovery-draft-from-ian)
- [Wednesday](#wednesday)
  - [Early Report from Key Update Design Team](#early-report-from-key-update-design-team)
  - [Transport Issues](#transport-issues)
    - [2528, Are Transport Parameters Mandatory?](#2528-are-transport-parameters-mandatory)
    - [2496, QUIC Ossification](#2496-quic-ossification)
    - [2473, Connection ID Length changes](#2473-connection-id-length-changes)
    - [2471, Stateless Reset Lacks Normative Text](#2471-stateless-reset-lacks-normative-text)
    - [2464, Remember Fewer Transport Parameters for 0-RTT](#2464-remember-fewer-transport-parameters-for-0-rtt)
    - [2458, Client MUST use 1-RTT packets if it reads 1-RTT packets](#2458-client-must-use-1-rtt-packets-if-it-reads-1-rtt-packets)
    - [2441, Peer that terminate a single connection on an IP/port cannot migrate with empty CIDs](#2441-peer-that-terminate-a-single-connection-on-an-ipport-cannot-migrate-with-empty-cids)
    - [2436](#2436)
    - [2403](#2403)
    - [2400: VN packets may be dropped more often when QUIC bit is 1.](#2400-vn-packets-may-be-dropped-more-often-when-quic-bit-is-1)
    - [2389](#2389)
    - [2388](#2388)
    - [2387](#2387)
    - [2360: 0-RTT flow control limits can't be increased](#2360-0-rtt-flow-control-limits-cant-be-increased)
  - [Future plans](#future-plans)
  - [QUIC Connection Migration](#quic-connection-migration)
  - [QUIC Offload](#quic-offload)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Tuesday

### Interim Meeting Planning

Next interim planned for May 20th in London, United Kingdom.

### Hackathon / Interop Report

5 min - Discussion of what QUIC implementers did and learned at the hackathon - Lars
[quic interop sheet: https://docs.google.com/spreadsheets/d/1D0tW89vOoaScs3IY9RGC0UesWGAwE6xyLk0l4JtvTVg/]

lars notes that connection migration is trailing in testing, but overall pretty thorough. target was -18

more h3 this time around, but still no browser integration

ietf network contains a box that reorders by size - excellent test network for re-ordering

chirstian notes confusion between ordering of transport params and needs more testing

jana notes that some progress on tooling is going on - hopes to get some interop participation

jana notes that chromium participated with browser integration

david: that's the chromium implementation of quic, but not the whole browser

erik kinnear: have loaded quic/h3 over safari all the way through the stack

*applause*


### Editors' Updates

#### Discarding Old Keys - Martin Thomson

note: slides updated yesterday, already out of date

There's really 3 intertwined issues: 2237 2492 2504

keys ready uses a frame.. alternative is a bit in first octet

keys ready is implicit about which keys it is talking about

when you recv keys ready the older keys (from older epoch) are no longer relevant. key update can proceed

ekr: what do you do if you recv keys ready and you have outstanding unacked data

mt: you can drop the data from the initial packet

ekr: you can cease transmitting any state prior to the keys ready frame?

mt and jana: yes, recovery state as well

david s wrote an alternative - retire_keys. send when no more data will be sent under a set of keys. also implicit.

ekr - send this after all data has been acked in that epoch?

david s - yes. it turns out it can be hard to know when ack has happened. but I think it can be done earlier

david s - alternative is to key off tls state machine transition (handshake complete signal)
ian - once you are done sending at a encryption level you can send this. once you have sent and received it you can move on (drop old keys)

ekr - done sending means I know the other side received it.

all - yes

mt - retire_keys is encrypted with the new key

ekr - its not clear that old data needs to be acknowledged before sending retire_keys as new keys can be used.

david s - send it when you won't send anything else at that layer - so as soon as you have keys for a new epoch (not unacked stream data - which can be sent under new epoch)

ekr: many tests I have to make in the code for each of those conditions

david: concept is clean, implementation not necessarily

ian: clarification, does the ACK really need to drive this. not looking for ack, just saying done sending with this key

mt: if you drive just off retired_keys, you can get simultaneous update. M->N->O can skip N, same keyphase bit, cannot be distinguished. peer sees gibberish, not the key update. this is the essence of the bug

marten s: is this equivalent to just looking for an ack in an advanced epoch?

mt: max_key_updates is a different approach. flow control for key_updates; proposed by kazuho

mt: if you allow more than 1, then you are committing to trial decryption

christian: i know when I can stop sending any given epoch, but I don't know when I should stop acking. In this diagram (slide 12), client may repeat end of client handshake because it did not see an ack...

victor vasiliev: when do i want max_key_update to have any value other than 0 or 1?

mt: it's cumulative, like flow control.

mt: use a bit proposal a lot like keys_ready but the signal is in every packet and doesn't need retransmission rules

mt: make_key_updates is the only one that allows an implicit transition on the handshake. that ensures that close cannot be handled by handshake keys after new keys are made

david s: the initial keys are the ones that need to be dropped quickly because they don't have same security of a full exchange. timing of read vs write may be diff.

mt: risk of DoS comes from retaining willingness to receive Initial packets, attacker may inject CONNECTION_CLOSE at lower protection than keys you have

ekr: disagrees with david. this is a minor and redundant dos exposure. if discarding earlier is inconvenient it is not worth it. 

david s - clarifies a server drops read keys but not write keys (early). and once the hs is complete it all gets tossed away.

ekr: that will cause retrans where you can't read the ack

mark: not cutting queues, but we want to talk about recovery. do we need to do this small-group discussion here? ten minute warning

marten: unified explicit signal for dropping keys seemed good in tokyo. looking at proposals here, initial and handshake look special, and we need special handling for them anyway. might as well accept that. build special case for this. unified explicit signal for all other updates, but implicit for initial. (12) Server knows when it send server hello, can drop initial keys *missing* so no injection attack in server dir

mt: primary wrinkle is server DoS mitigation

marten: for mitigation we only need to count bytes

christian: what marten said. initial is special. if I have HS keys I don't need initial on client side. server side is wise, need to keep until client has handshake key too.

ian: yep, need to separate signals. david + marten's ideas are interesting, optimisations a server could perform, not necessary

ekr: threat model plz. in order to inject, you need client [], theory is attacker has client initial, can't transmit its own initial in other dir? particularly this second not true. attacker on path can't control -- some attackers can always put packet in front, some never, some sometimes. please articulate the attack that the proposal actually defends against because these scenarios aren't unique to what is being protected

jana: conversation from what to do with initial should be separate from handshake keys. initial has a different threat model. 

mt: let's shelve initial. anyone arguing for keeping these together?

ekr: i am

kazuho: clients having a pair of keys..?

ekr: I have seen lots of specific attacks without an overlaying theory of what attackers are and are not allowed to do. I don't want to analyse them case by case as we are doing with this. So lets not separate the questions

mt: we are dealing with two things here. one is a bug. one per RTT explicit fixes the bug. let's do that and come back to argue initial attacks to heart's content. 

ekr: best answer to bug may not be the general answer.

mt: make progress!

ted: am i a usual suspect or a diminishing return? if we do split this off, relatively easy to look at what we are optimising for in each case. note that reassociation is cheap. if we are optimising for not dropping packets on the floor, then we have to come up with a mechanism to prevent simultan

mt: discouraged on progress - felt this was mostly closed as a concept.

mnot: supportive of editors making progress

jana: small design teams have worked in the past. do it now.

mnot: do we have <=8 people that would be willing to do this? (as was decided in tokyo)

lars: we've hit the bug in interop - this matters

brian t: I've noticed that there is rough consensus around splitting these. DT should start from that

chairs: david s has been named focal point for this. TALK TO DAVID AT THE END OF THIS SESSION - and will make a slack channel for the DT (#discardkeys)



#### Recovery Draft from ian

[link slides] material that is the same as the slides given from mic will not be transcribed

ian: retransmittable is now referred to as ack-eliciting

mt: retransmittable had nothing to do with whether you were actually going to retransmit something

gorry: i don't get what you want to call it. "ack-eliciting"?

jana: let's try this with a few ACKcents [this pun needs to be memorialized] because it's hard to say.

eric k: what if we want to retransmit a packet but not elicit an ack

ian: it used to be confusing because retransmit is not something the recovery draft does

ekr: to be clear - this is a packet that will cause the other side to send an ack within max ack delay

ian: yep


praveen: clarify persistent congestion timeout please

ian: essentially 3 pto which includes kPersistentCongestionTimeout [is that right?'

**re 2023 - pace packets or reset cc after idle**

praveen: tcp defines idle as a period; quic defines it as state of nothing to send. not many stacks are doing ss after idle

ian: linux stacks are doing pacing after idle. can you file a bug regarding idle def

jana: tcp's definition doesn't consider pacing.what we want to prevent is sending a burst after idle

praveen: agree - good change. idle period needs to be defined crisply

jana: maybe more liberally?

praveen: will open issue to discuss

jörg ott?: can we apply existing idle tcp definition here?

ian: maybe. core goal is to avoid adding large burssts to the network

mirja: there is a TCP window validation after idle, cwnd decreases. Will recovery do this? 

Ian: we do an informational ref, but no recommendation

mirja: either you pace, or you decrease. There should be middle ground. 

Lars: Please figure out details and file an issue

jana: newcwd was done in tcpm and its referenced in the quic draft. the same considerations apply

mirja: bare minumum, reset window

gorry: pacing is the big thing to make a huge difference

jana: if you want something more liberal that default conservative behavior, see newcwv.

**gen q&a about recovery**

praveen: one more change not mentiond here, not grow cwnd on [unint.], this is a deviation from TCP. in draft-19 right now. i will file an issue

lars: we have the new process applied to transport and TLS. recovery and http are not there yet. is recovery ready for this process in -19?

praveen: more interop testing might help. don't know all the issues yet. also need to test TCP and QUIC on the same link. 

lars: describes old process as editors making normative-heft decisions and seeking consensus afterwards; new-process is the reverse

ian: would like one more version under old process (between now and london interim)

eric k: we haven't been steered wrong yet by the editors.. no urgency to go to new process

lars: recovery has been a more stable document issue wise

mnot: places a lot of responsibility on editors shoulders and that is kinda unfair.. as chair would like 1 process in place for chair convenience

jana: the workload is easiest on this document. some agility is useful and we are not ready for late-process yet

lars: process only makes a different to design issues. editorial things are unchanged. most work here is editorial

jana: disagree. lots of design issues

mnot: move on

ekr: target london for raising old-process issue list

mnot: reasonable

brian t: caution against new process because testing is not really covering the edges of recovery envelope yet. including sharing tcp links

martin duke: interop test at high volume would be good (christian's original idea)

gorry: editors are doing great - but we need to do full collapse testing before freezing

lars: not about freezing editorial changes

chairs: revisit in london

lars: a throughput stress test would be useful to be documented as part of interop.

**issue 2184 - kinitialrtt of 100msec is too aggressive**

ian: choices are 200, 300, 1000.. picking too conservative is encouraging implementations to find more info

praveen: emphasize "may choose to use additional information" and encourage cached values

gorry: dont optimize for the 99%

ian: we are talking about 1 spurious retransmit

emile: does this apply to 0rtt?

ian: in practice it does not apply to 0rtt as that should be cached with 0rtt info

lars: we don't say you shoudl retransmit with that 0rtt

michael tuxen: tcpm says ???

ian: clarifies length of 0rtt credentials is ~several days

gorry: for sat users its every connection all the time

lars: heard mild pref for 1 sec, point out 300ms from Linux, and that caching can be beneficial.

jana: tcpm rto-reconsidere says in the absence of knowledge about path the RTO must be 1000 (or is that what the quic draft says?) 0-rtt is not absence of knowledge about path

ekr: will chrome use 1 sec

ian: yep - but it will encourage us to cache

tommy pauly: good approach. wrt 0rtt we do need to make some recs in the absence of network info (e.g. wifi->cellular)

ingamar j (via jabber): lte can be >100 often, but when radio is alive < 40

emile: name it initial1rtt. (to differentiate from 0rtt)

praveen: necessary to cache per path, and invalidate when networks change

lars: too-short initial value catches a lot of bugs, so maybe we keep it

**1978 - sender controlled ack ratio**

ian: any objection to closing 1978, and saying we do this as an extension

bob: a number of networks do ack-thinning, wanted to make sure these networks do ack-thinning, to discourage them from trying to work out which the 

lars: can we punt to v2?

bob: yes, then we can see whether this happens

jana: we should make sure people know that the shortest packets in quic are not necessarily acks. 

brian/lars: can you file an issue on manageability?

jana: yep

**issue 2185 - TLP 1 or 2 packets when triggered?**

ian: is the current text ok - SHOULD send 1 or MAY send 2.

lars: text currently should 1 may 2

praveen: persistent congestion definition depends on this, since it's defined as 3xPTO

ian: yep, 

praveen: text is fine.

all: close it

**issue 2393 - are max ack delay + ?? added before exponential calculation**

praveen: keeping *???* is consistent with what TCP is doing. posted comment yesterday, one possible change, can take this offline.

jana: agree, point of EBO is we waited this long, didn't hear anything, so wait twice as long, collapse the whole thing down anything. 

ian: will close with no action


===========================

## Wednesday


###  Early Report from Key Update Design Team

[slides](https://datatracker.ietf.org/meeting/104/materials/slides-104-quic-discarding-quic-old-1-rtt-keys-design-team-proposal-00)

David Schinazi: Formed a team yesterday to talk about how to discard keys. Key phase bit in short headers. Key update is just flipping the bit. Problem is that the sides can flip too many times and get out of sync.

Design principles:
    - Avoid trial decryption
    - Explicit signals for new epochs
    - Didn't want new ack or retransmission logic; that may change
    - Don't ask for permission to key update
    - Want to update keys symmetrically (both sides at the same time)
    - Implementations should not need to keep too many keys around

Proposal is to take up a reserved bit for the "KEYS_READY bit" to signal when you've ready for a key update (you've received on the previous epoch)

This allows for simple negotiation and no way to get out of sync.

There is one open issue—if an endpoint does a key update every RTT, and the other side doesn't want to keep all the keys around, we need to either:
    - Wait before sending key ready
    - Wait before starting a new key update
    - Ignore it

Ian: we have enough data on packet reordering to say that this is not a problem; zero reordering in 90% of connections, very little in others. Corner case. 

David: Congestion controller will treat them as lost anyway

Kazuho: Whether you have packet reordering depends on the protocol now, and could change in the future.

Mark: continue work, and we'll take it from there

David: informally e.g. on slack 

Mark: The issues here are using the late-stage process, in which we have the WG come to consensus before merging issues. Only going through design issues now, not editorial ones.

### Transport Issues

#### [2528, Are Transport Parameters Mandatory?](https://github.com/quicwg/base-drafts/issues/2528)

Martin Thomson: I think we're done with this one. Consensus seems to be emerging that they are mandatory. Problematic if client doesn't send them. You can open any streams, etc. Becomes ridiculous. Proposal is add one line to require both client and server to send transport parameters, and send an error if you don't get any transport parameters.

Mike Bishop: This means you need the TLS extension for transport parameters, but no given parameter is required to be included. (Room agrees)

Ekr will make a PR

Ekr: Note that it only really requires client to send

Martin: But we want symmetry

#### [2496, QUIC Ossification](https://github.com/quicwg/base-drafts/issues/2496)

Martin Duke: We need to timebox this issue, not near consensus. We have put a lot of effort into blocking ossification, but it's still easy to drop any new versions. This happened to TLS with 1.2 going to 1.3. We've had discussion on the list about obfuscation methods, etc. If we're going to fake out the version, let's not waste bytes.

Martin Thomson: This is a research question, but I don't think we need to fix this in the document now. All we have is a published spec. No matter what we do, it will be possible to have someone identify the versions and behave badly. We could smuggle something in that they don't understand, but they could drop that too. I don't think we can win this game. The version system is crude but not a burden.

Mark: I've thought of this issue as version ossification, correct? (Room agrees) When we finish short discussion, we should get the temp of the room on how to progress.

Brian Trammell: This is interesting research. We could have had an alternate design with many versions being deployed. That doesn't seem likely at this point in the process. I think this discussion needs to be captured in a document, but not necessarily a core doc. We should capture thoughts, but we should punt this issue.

Lars: Could fit into applicability. If people start blocking, we could have countermeasures, but we don't want to.

Jana: To Martin's comment, congestion control is research, but we still do it! My general thoughts are that we don't understand the problem fully, but if we can do something minor to help ossification (simple obfuscation) that may be worth it. The bar for what some vendor boxes will look at (not docs) is fairly low. Sending one number as a version is pretty risky. We still don't know what will happen when Google revs its versions.

Lars: We won't stop people from researching, and if we get a proposal in time for v1, great. But we don't need to solve this *now*.

Mark: One thing we can do is make this a shipping blocker.

Mike: If you have one version, they can ossify. If you have a predictable set, that can be ossified. We can't encrypt. If we use a salt, that can ossify. I'm inclined to say that maybe they need to do a bit of work to ossify, but we just ship and not worry too much. The best way to fight this is to deploy draft versions.

Philipp Tiesel: Proposing using version aliases, that the server sends as synonyms for the version with a timeout, so that the clients end up sending a bunch of different version numbers.

Ekr: I don't agree with Jana, but I like the model he describes. There are people who read the spec, and people who don't. If the threat model is people who don't know the spec, we can obfuscate, but we can't protect easily against people who do read the spec. My sense is that with TLS, people did read the specs (not well).

Mark: So designing something to get people to read the spec won't help much?

Ekr: Right, it will help minimally, but not much. I think this should not block QUIC's deployment. If people want to make proposals, start with the threat model.

Lars: No one spoke for this being a blocker. Some people said we should close the issue with no changes. The other one is  to have a simple obfuscation.

Lars: Let's close and move text into applicability. Applicability issue is [ops-drafts#62](https://github.com/quicwg/ops-drafts/issues/62)

Jana: I agree. I think we need the ecosystem to use multiple versions, but that doesn't need to be in this draft.

Marten Seemann: I like the proposal that was made by Philipp; I'd rather keep this open and design more.

Ekr: I want to table this and not revisit this until we have new information. Come back with a new proposal and a new issue, that's fundamentally new rather than just a change.

Martin Thomson: We don't know what a good solution is, and we can proceed with research on the side. We should carry on with the core protocol.

David: To ekr's point, we can't make the version a v2 feature, since it's an invariant. So if we're asking for proposals, we're asking for new issues later? (essentially yes)

Ian: Google will probably use a draft version (or many) that look like IETF-QUIC in parallel, and by the time those go away, we'll have a QUIC v2 document. This is a good incentive for v2.

Lars: And other implementations can also negotiate private "clones" of v1.

Mark: Who intends to come up with a proposal?

8 hands go up for interest in making a proposal.

Lars: If you put your hand up, talk to Marten and discuss. Not a design team.

Hums:
    
    - [stronger] Close with no action, punt to applicability statement
    - [some, but weak] Leave open and block v1
    
Lars: (rough, but not very rough; medium sandpaper) Consensus for first option? Take to list.

#### [2473, Connection ID Length changes](https://github.com/quicwg/base-drafts/issues/2473)

Martin Duke: The spec forbids going from zero to non-zero connection ID. This seems like it would be useful for migration.

Proposal is that you can provide new connection IDs with non-zero length, and switch to that upon migration.

Ian: For peer-to-peer, we may need to switch from five-tuple connections to using CIDs

Kazuho: I don't understand the value of this; don't feel strongly.

Martin Thomson: This forces whoever does this to do trial decryption. If you go from 0 to non-0, you may still have a collision with a CID and encrypted data.

Mike: Yes, that's possible. But you can recognize connection IDs up front. Going from non-0 to 0 makes for more connection IDs.

David: If you run over IPv4, you may be requiring a CID, while not needing it for IPv6. You could use these out-of-band
understandings to know what to expect. Doesn't require trial decryption.

Christian: Confused by the problem. I don't see a problem with receiving connection IDs from the peer, because the peer decides what it knows how to accept (including empty). Have synchronization issues if you need to change your mind.

My vote is to not do anything.

Martin Duke: Where this issue ended up, the question is about mixing specifically 0-length IDs.

Martin Thomson: There is maybe valid cases in what David describes, but you don't control the situation—the peer does. So the sender could always choose a different set of CIDs. Using any CID on any path is valid in the protocol. Note also you can't do stateless resets with 0-length IDs. Do I have multiple stateless resets with multiple empty CIDs?

Mark: Does anyone actually want to change this?

Mirja: Do we need a transport parameter to support the zero-length?

David: We could have an extension for server preferred address? That could make this okay.

Martin Thomson: That's discussed in this very long issue. I'd be in favor of setting a 0-length CID associated with a preferred address. That should be its own thing.

David: i'm OK with that, and can do the new issue.

Ian & Mark: Should probably close this then.

Jana: How many people will use this? (David raises hands, then shrugs) I understand the theoretical flexibility, but we should figure out if it is needed.

Lars: I think we'll close this one, and then can determine if the subset in a new issue will be used.

Hum!
 - Should we loosen things in the server preferred address? Weak hums
 - Should we loosen more broadly? Weak hums
 - Should we leave this as is? Broader hum, that's more strong.
  
Rough consensus is to leave as is. If people want a new issue, please bring it (along with rationale to the group)
  
#### [2471, Stateless Reset Lacks Normative Text](https://github.com/quicwg/base-drafts/issues/2471)

Martin Duke: No guidance about how to handle stateless resets.

Mike: Fundamentally, the reset is an optimization. Should only be a SHOULD not a MUST.

Jana: On the receiver, it's a MAY (but in your best interest).

Ekr: I think it's optional for the server, but not the client. What's the argument for not requiring on the client side?

Martin Thomson: That's fine. If you receive one of these, you really have a MUST for handling this. It doesn't make sense to ignore the reset.

Mark: Can you write a proposal?

Martin Thomson: Yes, and I'll also ask Martin Duke.

#### [2464, Remember Fewer Transport Parameters for 0-RTT](https://github.com/quicwg/base-drafts/issues/2464)

Martin Duke: A lot of transport parameters don't make sense to remember in 0-RTT. We should go through and figure out what makes sense.

We have a PR that we think we have agreement on.

Lars: We just need a consensus call then.

#### [2458, Client MUST use 1-RTT packets if it reads 1-RTT packets](https://github.com/quicwg/base-drafts/issues/2458)

Martin Thomson: When discussing what can go in 0-RTT packets, we noted that we should not be able to reply to a 1-RTT with a 0-RTT. If you
can read 1-RTT, send on 1-RTT as well.

Mike: The discussion here is a bit scattered. There's a PR from Martin that is valid; Mike has one describe how the server can detect this.

Need to combine 2461 and 2466.

Martin Thomson: There is a split in the PRs between describing and requiring. Would rather not rely on enforcement rules here.

Ekr: I think it's fine for things to be enforcable. What I don't want to do here is to have a lot of hoops for the other side
to enforce correct behavior. We don't need a software way to detect misbehavior in this way.

Kazuho: Preference is to use a MUST NOT to limit amount of 0-RTT data.

#### [2441, Peer that terminate a single connection on an IP/port cannot migrate with empty CIDs](https://github.com/quicwg/base-drafts/issues/2441)

Ian: Current text says you cannot do that, but I'd like to do this for WebRTC.

Ekr: I agree WebRTC should be able to achieve this, but I thought it would be with ICE. When we bind QUIC to peer-to-peer, the IPs will be largely irrelevant. They exist only at the ICE level.

Martin Thomson: WebRTC gets path validation already, so it doesn't need the other machinery in QUIC.

Mike: We talked about trial decryption. CID is what allows you to ignore the junk from the network that you don't recognize. If you're using ICE, you're not migrating from QUIC's perspective. I think the current text is fine.

Ian: I think this is still useful, but can be in v2.

Ted Hardie: I think that the suggestion that we do this in v2 is good; just because one peer-to-peer case uses ICE doesn't mean
that we should forget it.

Mark: Okay, we're closing this one and flagging for v2.

#### 2436

already merged PR, just confirm consensus

#### 2403

same as 2436

#### 2400: VN packets may be dropped more often when QUIC bit is 1. 

Ian: Proposing we just set this flag to 1 to make it like the rest of the packets.

Martin Thomson: I think Ian is right about setting to 1.

Mike: QUIC bit is part of version 1, and VN is invariants. This causes the invariants to change, or is it just an encouragement?

Ekr: Since VN already means you're blocked, detecting VN being blocked compared to other packets is fairly impossible.

Jana: Agreed, we need to be clear on what the threat model really is. We can leave unspecified in VN.

Brian: Must also agree with Ekr and Jana. We can have a question when we close invariants about if we want to put this in invariants now or later.

Martin Thomson: Lots of settings in which this bit is not useful. If we allow endpoints to signal that they want to set this bit to 0 occasionally, that might now. We could grease it in an extension. Therefore we may ignore the ossification for now.

Jonathan Lennox: For doing demux with other protocols, it seems like you'll probably need to indeed set the QUIC bit.

Martin Thomson: Proposal—when generating a VN packet, clients SHOULD set the bit to 1 to match. But invariants still says you ignore the bit.

Room is happy with that. People nod their heads.

#### 2389

editors need to do more work after Tokyo

Jana: I don't think this is design, sound like editorial.

Martin: I think we don't have consensus on how Jana interprets this one

#### 2388

editors need to do more work after Tokyo

#### 2387

same

#### 2360: 0-RTT flow control limits can't be increased

Mike: Sounds like a dup of 2458


### Future plans

Chairs: Planning future meetings. We'll have the interim in London if the city still is running at that point (wa-wa-wa).

2 days of interop, 2 days of slogging through issues.

When will the next draft be published?

Martin Thomson: Probably before London, not many changes. Questions is what people want to interop with.

Lars: Sound like getting a -20 in April to interop in London

Jana: To note for recovery, just always use the latest

Ekr: +1 for using -20 for interop, and getting that draft ASAP would be great!

Lars: Looking ahead to Montreal, we can start looking at future stuff. The main two candidates there are unreliable and multipath.

We also have another EPIQ conference in August. Call for papers open, etc.

### QUIC Connection Migration

Cherie Shi, Google

Sharing deployment experience of migration. Goal is to move connection requests between interfaces.
Classic case is parking lot problem, when you lose Wi-Fi and move into cellular.

Demo shows that the connection migration implementation is far faster to adapt to these scenarios.

You need some signals: connections being disconnected/connected/made default

Pre-emptive signals of network changes

Path degrading detection dynamically

At the app level, 2% of requests see an opportunity for migration with network changes.

At connection level, 7% of connections close due to network changes. 0.72% have pre-emptive signals.

Stage 1 of testing was triggering on platform notifications and write errors.

Very reliable, confidence level of 99%. Helped failure rates for search by 0.7%. So about 
half of the opportunities were acted upon.

The gap was due to handshakes not being complete or not having other radios up.

Some connections can detect path degradation prior to migration.

So, there are two approaches: racing of handshakes, and migration on degradation.

With the improved algorithm, got up to 1.5% - 1.9% improvement (out of 2%)

Principles:
    1. Do not fail the request if it can succeed
    2. Respect the platform's choice of default network
    
Ekr: To look at the data, why do we see improvement at the 50th percentile, since migration isn't that common?

Cherie: Due to retries at the application level

Eric: This looks great! Would love to see more data shared, etc.

Tommy: You mention that if the other network isn't available, the migration can fail. Do you use timers to trigger or wait for networks?

Cherie: Yes, using timers. Think about 10 seconds.

Tommy: Such algorithms would be great to document for implementation guidance.

Igor: Is this unicast or anycast?

Ian: This is mainly unicast.

### QUIC Offload

Manasi

Experimenting with Chromium doing hardware offload

Encryption offload and transmit segment offload

Done offloading of parts, but to do full offload of stream frames (more like TCP offload),
you need very detailed information.

Request to add a length to ACK frame to help offload. There's a lot more, but that's the most
important point.

Martin: Good to identify STREAM and ACK as the important ones to offload. There is a length of sorts in ACKs, but we can move it. We should be confident that this is necessary first.

Jana: Thanks to Manasi for doing this work and waiting to get us to pay attention! It's less about needing this, and more about the usefulness.
