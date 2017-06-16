
# QUIC Interim Meeting

* Chairs: Mark Nottingham, Lars Eggert
* Agenda: https://github.com/quicwg/wg-materials/blob/master/interim-17-06/agenda.md
* Issues List: https://github.com/quicwg/base-drafts/issues


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [7 June 2017](#7-june-2017)
  - [Agenda review.](#agenda-review)
  - [Review of First Implementation Draft](#review-of-first-implementation-draft)
  - [Slides:  Server chosen Connection ID.](#slides--server-chosen-connection-id)
  - [Issue #58 Frame Type Extensions](#issue-58-frame-type-extensions)
  - [Issue #588 Pull Request (CSID/SCID)](#issue-588-pull-request-csidscid)
  - [Issue 568: Consider making Cleartext integrity version independent](#issue-568-consider-making-cleartext-integrity-version-independent)
  - [Issue 383: maximum packet size](#issue-383-maximum-packet-size)
  - [Issue #426 Hdr format/multiplexing](#issue-426-hdr-formatmultiplexing)
  - [Issue #311: grease the packet type octet](#issue-311-grease-the-packet-type-octet)
- [7 June 2017](#7-june-2017-1)
  - [Issue #215: Design Public Reset (aka Stateless Reset)](#issue-215-design-public-reset-aka-stateless-reset)
  - [Issue #353 Replace Connection Close with Public Reset](#issue-353-replace-connection-close-with-public-reset)
  - [Prune transport error codes #467](#prune-transport-error-codes-467)
  - [Packet Number Echo PR#269](#packet-number-echo-pr269)
- [8 June 2017](#8-june-2017)
  - [1-bit Path Information](#1-bit-path-information)
  - [Unidirectional Streams](#unidirectional-streams)
  - [Encrypted MetaData](#encrypted-metadata)
  - [Discussion of hackathon mechanics and funding.](#discussion-of-hackathon-mechanics-and-funding)
  - [Hpack](#hpack)
  - [Ack Spoofing.](#ack-spoofing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## 7 June 2017

Ekr gives a summary of local logistics.

Blue sheets are circulated.

Working on audio; will need attention to scribing for remote folks.

Brian Trammell volunteers to take minutes for one shift on day two; other volunteers needed.

### Agenda review.

After introductions, we will review the First implementation draft plan.  The real goal for the meeting is to walk out with a firm idea of what has to be done to get implementation drafts out.  That lets us get implementers a set of common specs to work up for the implementation testing, which starts the feedback loop for implementation/draft development.  A question is what pace folks want to set for interop testing and the follow-on steps.  Mark’s initial impression is that it is a small number of months.

Ekr: notes that an interoperable implementation requires us to make decisions that we’re not quite prepared to make.  We can finesse that with place holders, but we need to signal that those are placeholders.

Mark notes that we are using the issues to signal that; if the issue is still open, it hasn’t actually been made.

Ekr:  notes that he would be more comfortable if the draft listed those explicitly (e.g. by an open issues list in the draft or via explicit pointers in the draft).

Mark:  conscious that we are asking a lot of the editors, but it would be very useful if there are markers in the text to the issues.

Jana: that’s reasonable, but the problem is that the issues are larger than the text.  We can call out that the text is not final.

Christian:  is it enough to mark text as provisional if it is intended for interop draft but not the final decision?  Patrick and others say yes.

Martin Thomson:  that’s all people are asking for--clarity on when the drafts’ decision is not final.

Mark: going up a level, the editors have been incredibly busy; I’m hoping that once we have an implementation draft, that we can shift focus and some of the editorial work can take place on a different pace.

Confirmation of the Note Well (contains a pointer to 8179, which is new version of the IPR RFC).

Magnus: Are expected to speak our names during the meeting?  Mark said that we have not been doing that.

A round of introductions takes place.

### Review of First Implementation Draft

Stress that the first implementation draft will not have everything in it; it will list only what it requires to get us bootstrapped.

Martin Thomson:  The basics is to get the handshake of the protocol right, a complete list can be found here.  We’re not doing anything of the details of loss recovery or congestion control, this is just basic version negotiation, TLS 1.3 handshake etc.  Does not include transport primary negotiation.  You do not have to do with the stream state machine, or flow control.  It also leaves out the full HTTP overlay, the 0-RTT state machine, the streams other than those carrying TLS.

Mike:  Would you like to see something like exchange of PING before close?
Ian:  That’s what we had said “what are you going to do, send a ping and a pong?”  “Sure”.

Brian:  What’s the dumbest possible application to put on this? Echo, chargen?  That actually makes the problem with the first implementation draft much harder, because you now need to have congestion control etc.

Christian:  maybe a single packet echo would be a valuable test implementation.
Martin: that’s essentially the same discussion we had privately; at the point at which the handshake is done, adding something else in opens a bunch of additional work, and there is already a lot to do.

Mark: how many have read the wiki page in advance of this meeting? (almost all hands in the room are raised)

Partick: Wants to see some of the crypto up first.

Martin T: There are two pieces of API here that are new here.  Maybe three, if you consider 0-RTT.  The ability to install transport parameters in the handshake and the other is stateless reject.  Both of these things are completely new code; OpenSSL has some code for this, but it is new for them as well, associated with TLS 1.3.

If anything moves, suggestion would be that transport exchange of parameters to move into the next one.

Ekr:  perhaps this implies that version negotiation should also move into the next one, and assume the same version.  Since there is only version at the moment, that makes the logical chunk a little different.  (Note that this means we are not testing greasing until the next implementation draft).

Ekr notes that the pace set in TLS 1.3 was fairly tiring, and that going to a large number is probably going to create some problems.

Mark notes that it was 3-4 a year in HTTP, with editorial drafts in between.

Brian asks if we want to link implementation drafts to IETF hackathons, since there are 3 a year; that may be a win. Could be worth trying.

Mark notes that this may depend on what implementations arise.

Mark asks whether folks are fine with this plan.

Ekr notes that he had proposed a change, to remove version negotiation along with stateless reject.

Martin says that the version negotiation is trivial.  Jana agrees that this is simpler.

Martin Duke and Mike West note that it is below TLS.

Jana walks through the logic in repacking a Client Hello with a version change.

Martin Duke asks if this isn’t a pretty artificial test.

Patrick points out that we have the greasing tests, and that these would make this a valid test.

Martin:  the top piece here is the code that hits the TLS stack.  If we want to push that into the next version, then we have resumption as something that would be done at the same time.

Patrick, I guess I would like to know when the second implementation draft is coming to know what I want in.  If it is 4 months further out, then the second implementation tests are 7 months out.  That’s quite slow for some of this functionality.

Ekr responds that he is concerned that people will subset these features for testing.

Jana notes that folks can always implement aspects that are not marked for the first tests.

Mark notes that we don’t know how many resources are going to be thrown at this; the room is then polled for how many implementations we are going to expect.

8-10 implementations seem likely, based on responses in the room.

Would it be more helpful to have a granular listing of elements for testing?

Christian and Brian note that test vectors would be useful. Ekr then says that a generic test harness would be nice to have, as that is the more painful part of this.

Brian:  a wiki page of that and the test vectors would be very useful, as we don’t have to publish that.   It has been published in the HTTP case, but it is easy to make that decision later.

Mark: we’ll return to these subjects at the end of this meeting.  We have two meetings for Prague, and we have the hackathon as well. We’re also talking about another interim in the style of this meeting sometime in October.

Jana asks the format for interop.  We can do that at the hackathon, or we could have one day of a three day interim be the interop testing.

Mark: any other discussion?  Did we come to a conclusion about ekr’s proposal.

Martin Thomson: I’d like to get a sense of whether folks can do Hello Retry Request and the stateless reject; if someone is not going to implement that, it would be useful to know (keeping in mind Patrick’s concerns here).

Martin Duke: I’m counting on someone else to provide me the TLS 1.3.

Martin Thomson: if you are not sure, maybe stick your hand up for this.

Patrick:  But we can’t keep kicking it down the road.

Christian: 1.3 is not completely finished, and it is a large set of options.  Should we explicitly profile it.

Ekr: there are implicit profile elements here, as there are some things (e.g. key update) which do not make sense for QUIC.

Martin:  I think we should focus on what we are going to do right now (handshake).

Christian: what about someone is going to implement only the TLS pieces for QUIC?

Ekr and Martin speak (couldn’t hear).

Martin said:  I think we really have to focus on the initial key exchange.

Ekr: The MTI is already set, so we don’t need that.

Jana: everybody who is going to implement has that set.

Subodh asks whether we are spending time on whether we are nailing down the exchange of data, or are we nailing down the state machine right now?

Martin:  I am kind of tentatively hearing that there is no objection to x25519 being included; ekr, I’m not violently opposed to it, but there is an MTI and we should stick to it.

Subodh: this is really a question of what people want to start off with.

Ekr:  it seems odd to have the default setting to be something other than the MTI.

Ian asks whether there are anything people don’t like it in the room?  Why would we make the choice of not using the MTI?

Ekr: because Boring offers it.  Why don’t we assume that it is a matter of a knob and move on?  Mike: it might not be.

Ekr: you’d think so, but.   (Webex work goes on, to enable the logitech speakers and allow Victor to speak).

Victor:  I would prefer x25519, as it  is significantly smaller.  It would fit into one packet, so it would be easier to get right.

Ekr:  that actually seems like an argument in the other direction, as it may make it harder for us to detect overflow (where a p-256 selection might identify it earlier).  Mike: I would agreed.

Christian: what do we want to achieve?  If we want to test the viability of the handshake, we should test the QUIC part of the code, rather than the TLS part of the code.

EKR:  that’s not the point I was making. I am worried that if we choose the smallest curve, we might miss that we have used up all the headroom in the rest of the packet, and might discover it only much later.  I think the anchor point should be the MTI.

EKR: I think we are doing what we discussed earlier: putting a lot of time on something that it is a placeholder.  Mark: agree, don’t want to rathole.

Ian: there seems to be a small number of people who care about this; perhaps they could go off and work this out?  Agreement.

Mark:  any other comments on this?  None.  Okay, that’s the goal for the group now.

Lars: note that we may have some interop days that may be distinct from the interim days, as we have done that in the past.

Mark:  That takes us to the issues on the -03 drafts.  Review check: again, lots of hands.

Mark:  No issues raised against the milestone.

Ekr:  The test I’m trying to apply is “could I implement” this, no matter how stupid I think it is?  Yes.

Mark:  Did folks have a chance to look through these and are folks happy with the way in which they were handled?  Seeing nodding heads, but not many nodding heads.

Jana: Have some slides on one set of changes. (A USB stick exchange ensues).

(Mark gives feedback to edge and chrome on full screen slides, and Mike notes upcoming improvements.)

### Slides:  Server chosen Connection ID.

Previous Design changes:  Server chosen connection in 02 was Client chooses CCID, the Server has the same one until it is about to complete the handshake.  There was an issue pointed out that redirecting incoming connection cannot be done in this design, the initial server is stuck serving the client.

New design provides this capability.  The client chooses a CCID for client initial or 0-RTT.  There is a new server chosen connection ID in cleartext (SCID). The Client cleartext and 1-rtt packets have this SCID (simple cases).  With retry, the Packet Number is echoed for verification when an SCID1 has been chosen but retry required.  (Martin:  this is the most complicated).

Ekr: what is this doing for me?  Jana: this enables a server to redirect you when a client initial has been received (it’s “use this connection ID instead”, which will get tracked to the right server).

Ekr: what is the use case?  Jana: it wants to redirect you to a different server in the same farm.  Christian: if you want to do that, you receive this on an anycast address, you could do a full redirection to a specific address?

Martin: this is a different use case.

Christian:  in what we have, the new server ID arrives after the cryptographic state is established; in this case, we do not.  That’s how we get man-on-the-side injection.

Discussion of whether the server connection ID is too complicated; a client generated connection id on 0-RTT and initial exchange, but a server client ID as a separate ID on client exchange two. (May not have captured that well).  Jo Kulik:  does the client have to use the SCID1?

Jana: there is no way to be sure that the client does so.

Martin: there is nothing in the version case that allows  you to tell that the client followed the advice; in the stateless retry case, the server can send a cookie that allows this to be checked.

Mike: it might be clearer to phrase this as there are two places in the handshake that allow the server to change the connection ID:  it likely won’t use both of them.

Igor Lubachev:  I don’t think this is a redirect per se; this is a way of making sure that it reaches a different server within an anycast domain.

Jana: there is one slight nuance here: the server can generate a SCID1 such that the client initial will reach a desired server.  The hashing infrastructure still treats this a client chosen one, it simply results in the hashing algorithm getting it to the right place.

Igor:  I would much rather see this be explicit (client and server chosen IDs being distinguishable). Jana: the point of `````````server chosen is diluted when you can’t actually prove that it is server chosen.

Ian: there’s a use case where you have a sparse set of available hashes.  You could have a server structure for some of them but otherwise continues to use ECMP.

Jana:  either the load balancer has to look at the packet and see the structure or you must have a way for the server to know what the hash algorithm is, so that it can generate a hash that produces the right result.

Jana:  The client initial carries a client generated ID.  It indicates a new try.  A stateless retry is always an initial, since it will go to a new server.

Ekr:  I feel like we need to uplevel.  Christian raised an existential point.  The reason we wanted the server to give you a connection ID was because you wanted a way to make sure that you could get back to the same server.  This is now enabling a redirect, is that something that we want to enable?

Christian answers: no. I want to minimize the amount of logic that goes into cleartext, as that will be abused.

Christian:  you can build protection for the server from the client with this, but you can’t do the reverse. You cannot protect the client from the server with this, because echoing the packet number is very weak.

Ekr: we can protect the client from an off-path attacker with this, but the method won’t protect you from someone on-path.  We can’t fix the second with this method.  This looks more like policy-based redirect rather than a load balancing method.

Brian:  I would change the statement of this issue:  the server would like to redirect this within 1-RTT.  There are any numbers of mechanisms available if you are willing to complete the handshake and if that server is separately addressable.

Jana asks how we want to solve this problem; Christian-- I don’t want to do this without completing the security handshake. It’s a really bad idea.

Christian:  An on path attacker can redirect you to a server with a lower version, using this.  Jana, Martin:  not really.  As long as the server is selecting the initial, you’ll see the version set that is acceptable.

Ekr:  the security issue is that this is a non-trivial piece of additional mechanics; is this worth it?

Subodh: why is this non-trivial mechanism not matched with functionality?  This is a new piece of functionality, which would help us shift services to new nodes, and that would be useful. Igor, if you upgrade half a server farm, this sort of mechanism would be very useful.

Christian:  the concern is that there is a history of attack on hash tables, making sure that everything hashes the same.  An attacker can then target a single server.

Igor:  that’s no different from where you are, where a single IP address exposure can get you the same thing.

Subodh:  having the client switch to the server chosen connection ID as soon as possible may actually be better for that attack profile.

Mark:  to go up a second.  We are having lunch at 12:15.  We need to go very quickly today and tomorrow; Thursday we’ll have a more traditional Parisian lunch.

Subodh:  I had one question on the mechanism.  We have two places now where the client or server can choose the connection ID.  Could we have a distinguishable ID for retry?  So that it is unambiguous that this is a retry?

Jana: there is no way to verify that; Subodh, yes, we can specify it, but not check it.

Igor:  there is a big difference between an attack that can happen and normal operations.  This is very useful and cheap in normal operations.

Jana: on a hello-retry initial, the connection id sent by the server must be indicated in the cookie, so it can be checked.

Jo: I have two questions.  I think it would be useful to have a state machine here, as it may be that there is a simple state machine, despite the apparent complexity.  What is the use case for not including a cookie?

Martin Thomson:  we don’t say anything about what goes into the cookie. We could have a set of suggestions.

Jana: does this makes sense to people?

Ekr: I’d like to see this written down.  Martin Duke: I’m trying to follow this and confirm that the flaw in -02 is serious enough to warrant this.

Ian: you can solve this problem if you want to do some heroics.  Complete the handshake with a ticket, then send a go away, which directs somewhere else.  That doesn’t work for version negotiation or cryptographic negotiation.

Ekr:  the motivation for doing something in QUIC, rather than elsewhere, is that it has to be cheaper, faster, or only effective at this level.

Ian: Subodh’s argument was that this helps mitigate DDOS, and that would be an argument for this.

Subodh points out that server stateless reject actually helps with dos mitigation, by avoiding the pinning to a server when not required.

Ekr is concerned that the use case around version and cryptographic negotiation is going to be very small.  There is a strong motivation for these to converge as soon as possible.

Martin: address validation is the other motivation.  This is a load shifting mechanism, when a machine is already under some load.

Martin: I think you’ll find that having this is actually of some use.

Subodh: this isn’t unsolvable without this, but this would make this lighter weight.

Ekr: do you want to do address validation for crypto or anti-amplification?

Ian: anti-amplification.  We don’t do this at Google today, but it would be easy to simply not send data until the handshake completes.

Jo:  this is enables you to move the traffic to where you want.

Mark: is this something we need to get into the first implementation draft?

Martin Duke:  I think everybody is fine with what is in draft 02, maybe this doesn’t need to change now.  That may depend on whether this is a common case or not.  If somebody sends a source address token, and it isn’t valid, how different is that case?  (Different) That means that this use case will only be version negotiation or TLS mismatch that causes an HRR.

Jana: no, that’s not the use case for this.  This doesn’t save an RTT, it saves server resources.

Subodh:  I would like client cleartext packets to have logic that bind as soon as possible to the server

Mark: A separate RFC would be great for hardware implementers

Christian: Need a spec that tells servers when to engage in version negotiation.

Mark: Too hard to find in the draft. Also too awkward to reference QUIC v1 in future versions of QUIC. But let’s not rathole on an editorial issue.

Jana: We can always add another integrity check.

Ted: FNV-1a will always have the magic number function; but may lose the integrity check function. [ Not yet determined -- Martin Duke ]

Jana: We should have a discussion of what is invariant.

Ekr: Why not just drop bad versions for now?

Jana: Just table this, handle Issue #58, then everything else is in version negotiation.

Brian: Don’t do any version negotiation, because we will learn from implementation.

Ian: Do we need #58 (frame type extensions) for interop #1? Ready for -03 draft?

Jana. Need to do an -04 draft just for #588.

###  Issue #58 Frame Type Extensions

Ted: Martin D’s Type/length thing is easy enough for this.

Lars: Should we punt for the first implementation?
Brian: All these issues ares “what is an invariant?” None relevant to first implementation.

Jana: I’m cool with that. Modulo #588.

Ekr: So are we cool with implementation #1 to drop all bogus packets (which would normally be public reset)

Mark: We agree that the draft (modulo #588) is fine?

Martin D: 1st implementation draft says nothing about public reset.

Martin T: I’ll add it to thing we’re not doing.

### Issue #588 Pull Request (CSID/SCID)

Martin T presented the pull request (#589)

(discussion of nits)

Ekr: does the first flight of 0RTT packets have mixed CIDs?

MartinT: No, but acks will be with the SCID and 0RTT data will be CCID.

Mark: Consensus in room; will have to take to list. And we are now done with first implementation draft.

Igor: After VN packet, do clients get a new connection id?

Ian/Jana: due to downgrade attack issues, client should keep its chosen connection id across the VNP receipt.

Ian: should also say 5-tuple doesn’t change during handshake.

Igor: If some servers are v1 and some are v1/v2, this can cause handshakes to fail.

Igor: Wants to allow version negotiation to propose conn id.

Jana: Version negotiation not quite stateless. Must record version negotiation history.

Martin T: Way to fix, not pleasant.

Jana: 1) Hope the 5-tuple sticks
2) Ship a cookie in the VNP.

Lars: There will always be versions that are common.

Igor: A set serves 1, another serves 2. Client bounces between mutually incompatible versions and the handshake fails.

Lars: You shouldn’t prefer a higher version till everyone speaks it.

Igor: Have to keep state in load balancer to see that CCIDs end up in the same server.

Ted: Yes, that’s the deal. Can this force a downgrade?

Ekr: A new SCID in version negotiation can force a downgrade.

[Some debate on whether this is the case]
selected ID.

Mark: would it be useful to task a small group of people to go off in the next couple of days?

Martin Duke:  I think once we are clear on the existential issue, this will get easier.  I don’t think this will save any RTTs, so the number of cases it will be used is small.

EKR:  It would help me to have a ladder diagram, so that I can see when this is going to get used, and that would help drive a decision.

Martin Duke and Subodh discuss the timing aspects.  EKR:  I don’t have any problem with pushing the server selected connection ID into  the second packet; Subodh: that’s all I want.

Mark:  I would like to see a new issue or to update the existing issue with this new proposal.

Jana: Summarizing, neither stateless retry or version negotiation carry SCID, they carry client chosen ID.  We drop SCID1/2 and end up with only SCID.  The state machine is simpler.

Ian: that actually eliminates something that worried me, which was a pathological state in which the server just cycled among connection IDs.

Issue 577 relates to this, but a new issue will get written to capture today’s discussion.  We’ll then get a milestone for it, and it will go into the first implementation draft.

Now looking at additional issues to be considered before the first implementation drafts (04, which will be first implementation draft).  The new issue Jana is writing up will get added to this list, and the list will be the main focus.

Break, back at 13:00 (local)

### Issue 568: Consider making Cleartext integrity version independent

Patrick: what happens if non-QUIC packets arrive on the port?

Martin T: Version-invariant header format is in the draft, but we haven’t said anything about version negotiation

Ekr: do we validate packets with unrecognized versions? Part of this issue - if we change the hash, there are issues.

Patrick: We ought to have something that is not treated as QUIC

Ekr: Should we ever change version negotiation?

Mark: does this matter for 1st implementation?

Martin T: would be nice to lock down version negotiation. This is important with multiple versions.

Ekr: point is, we have to get authentication nailed down or there are issues. We’ll drop packets with different versions.

Martin D: Security implications of not authenticating packet?
Ekr: Not really, just a checksum to verify no errors.

Brian: We need to find a way to make sure early versions can agree on a version. Only need stub version negotiation (just drop packets if no version match).

Mirja: should there be an error message?

Brian: Hadn’t thought it out.

Ian: Just send a version negotiation packet.

Mike: There is a set of perpetual invariants. The current list is incomplete. Should they be separate RFCs? (Mark agrees)

Jana: Adequate to have 5-tuple + CID fixed. Data centers with version discrepancies can adjust.

Ian: I assumed that 5-tuple was stable during handshakes.

Ted: if we have experimental frame types, it keeps the number of versions manageable.

Christian: I would like that. I don’t like version numbers for extensions.

Mark: All issues but #588 are moved out of the Implementation #1 issue list.

Jana: If we have 5-tuple + CCID, worst case (with low probability) is handshake fails.

Ted: Servers should be careful not to advertise versions in transport parameters if some in the data center are not upgraded.

Jana: Adequate to have stable 5-tuple + CCID?

Room: Yes

Martin T: Will add text about 5-tuple.

Martin D: Connection will fail if NAT rebinding during handshake

Ian: That’s a feature; potential attack.

Jabber: Would like to load balance during the handshake (i.e. add SCID in version negotiation)

Christian: Messing with this stuff during handshake is insecure.
Mark: We’re ready for implementation now.

Ekr: what happens if you send VNP with the version you offered?

Jana: I think you drop it. We should discuss weird packets.

Ekr: Error codes should be usable during handshake, where errors tend to happen.

Mike: Add to public reset?

Ted: We drop garbage anyway.

Patrick: Is that fine?

Ekr: For implementation #1, what should we happen for drops? Should send something before closing packets.

Consensus: Ekr will propose wiki text for debugging of connection errors; will result in a packet that is not a public reset purely for this troubleshooting.

[Break]

Open issues are organized in a series of buckets
https://github.com/quicwg/base-drafts/projects/2


### Issue 383: maximum packet size

Add a message saying “the packet is too large”. Why not just do a PMTU drop?

Magnus: IP fragmentation will make the packet large.

Christian: Similar to endianness. Also, IPv6 large packet issues.

Martin T: This is for cases where acceptable size < MTU.

Ekr: why not just drop packets too big?

Martin T: can’t do < 1280.

Ekr: min max must be >= 1280.

Martin S: Security issue if client can force you to cache packets. Should set a limit.

Ian: Google just drops it on the floor, but signalling is better.

Martin D: How is this different from MSS option in TCP?

Magnus: TCP’s paradigms may not be relevant here.

Lars: different questions: do you signal? What if peer violates the signal?

Subodh: We signal other server constraints like receive window, why not this?

Christian: I can force you to use more packets as a DoS.

Martin T: Making the floor 1280 will solve that problem.

Lars: Need data

Martin S: Don’t want to allocate 64K for every pkt received.

Lars: don’t have to unless you support fragmentation.

Ekr: why not just drop packets?

Ian: probing up over a limit is pointless.

Ekr: we could extend it easily

Martin D: Packet drops are a bad signal
PMTUD involves probing up; good to have a ceiling
Load balancers find it useful to control PMTU to servers on a per-connection basis.

Martin T: Not clear it’s easy to extend QUIC later.

Martin D: There are several people who think this is useful, and no strong objections.

Ekr: As long as the minimum maximum is 1252. (1280 - IPv4 - UDP hdr)

Consensus that Martin T should update the PR. -- and it’s done.

### Issue #426 Hdr format/multiplexing

Can’t distinguish the magic number from STUN/TURN etc  with ICE

Ekr: Do we want to do the work to make it demultiplexable?

Jana: could just have QUIC process first -- authentication should resolve these issues

Ekr: we should add a framing layer in these port sharing cases.

Jana: protected packets are safe
Packets with fnv-1a: use 192..255 for long header types.

Martin T: Not sure if this is needed; if needed, we can add a framing layer later that would be negotiated in the WebRTC signaling channel (STP?).

Jorg: But middleboxes don’t have access to the signaling channel!

Christian: Reserve some a number meaning it is not a QUIC octet; it’s framing.

Ekr: if we think this is a problem, we should just do it.

Martin D: Does this mean that v1 of QUIC will not support multiplexing on 443?

Jana: No, there’s a framing protocol that people will have to do. Some other RFC.

Ian: We’re going to be mixing RTC with QUIC soon, we’ll find if it’s a problem.

Consensus: Until we get more information, QUIC v1 is assumed to not support multiplexing. Ian’s project may provide more information

### Issue #311: grease the packet type octet

Use all first-byte codepoints so middleboxes can’t ossify.

Martin T: must identify first packets easily. Will be hard to grease long headers without much thinking.

Ekr: code points must be contiguous blocks.

Ian: server could specify code points in did not want to use to allow multiplexing.

Ekr: could just xor with last byte of packet

Martin D: Easy for middleboxes to still ossify

Ekr: not easy enough

Martin T; migration headaches from Google QUIC and identifying which is which

Ian: hence the verboten code points

Martin T: Jana and Ian will figure out if this breaks Google-QUIC migration.

Ian: are the blocked code points just a one-off, or needed in the protocol?

Mirja: if middleboxes can easily identify QUIC, that’ll prevent ossification.

Jana: changing bytes will force them to read the RFC.

Christian: just have a static map. Do we want a keyed permutation?

Ekr: problematic to get the connection ID, which determines the key.

Martin D: The greasing should be deterministic, to avoid a covert channel.

Martin T: We’ve given up on blocking covert channels.

Ekr: encryption occurs before masking.

Conclusion: this is a good thing. Ian and Jana have to look at migration difficulty. If no major issues, Martin T will write a PR.

Christian: insists that unkeyed greasing is useless.

Ekr: simple key (once a year?) given to load balancer.

Brian: load balancers need to read connection id before getting the whole packet.

Lars: this is less true than before

Martin T: if long header, the connection id is definitely there. For short headers, this is a problem. Load balancers can demand that conn id is always there.

## 7 June 2017

### Issue #215: Design Public Reset (aka Stateless Reset)

Martin: This is actually called stateless reset. What’s the purpose? What signals do we want? Who should consume them?  Bigger question: What is the role of a middlebox in QUIC?

Taxonomy of signals: end-to-end (basically everything); mostly-implicit signaling end-to-path; path-to-end signals (PMTU, ECN). Important: There is only one connection, but multiple paths.

Lars: Yeah, but more complicated. Upstream and downstream might be different. ECMP might split packets across multiple IP paths.

Assumptions of stateless reset: End-to-end signal. An endpoint loses state, and wants to tell the peer that it has done so. Used only by server. Terminates connection.

Ian: Should this always terminate the connection?

Lars: Need to differentiate between connection and the path it’s currently using.

Christian: What about server migration? I think we should [unintelligible].

ekr: I think server migration is a fundamentally different thing. You can do things in your network that are bad, that’s your fault. Note, many designs we’ve discussed are one-shot. Server migration is a corner case.

Ian: If a connection ID was being emitted for proxy reasons, and five-tuple routing stopped working, a new connection ID can get back to the right machine.

Magnus: We expect the server to have no state?

Martin T: Server is configured, but per-connection state is gone.

Lars: It can’t decrypt it

Magnus: And it can’t prove it had state

Martin D: Why not when client uses state?

Martin T: In the case where the handshake fails and we want a signal, that’s not public reset, that’s something else, some cleartext signal. When client loses state, don’t need

Mike Bishop: Client loses state, OS might not be able to route to app, then NAT will close port.

Martin D: With a Linux client in this state, you get resets.

Ted: We have people looking at using this in WebRTC. What a server is and what a client is in a P2P relationship is determinable, but it’s more symmetric. No harm in letting client do this. When multiplexing, if QUIC not expected, how do we deal with that? Seems related to public reset, and

Brian notes that there may be a distinction between initiator/responder versus the application-layer construct of client-server; there are patterns where the initiator is the “server” at the higher layer.  This is really for “responders”, not server.

Jana: Some context: Public resets are visible now not because of state loss at server but [unintelligible]. This is not loss of state, it’s just messed up. It happens in server farms, load balancers. If you want this on the client, what causes that to happen on the client. Client restart is not exciting, you get ICMP port unreachable. What is the reason a client loses state?

Christian: We will get scenarios where the asymmetry between client and server is not appropriate. A solution should therefore be symmetric.

ekr: as Mike said, the only scenarios that matter are server in a server farm needs to say shut up.

Igor: This facility allows much more certainty than ICMP port unreachable. What do you do with multiplexing… I think that’s a question for multiplex RFC

Ted: What happens if you’re multiplexing and you get QUIC you don’t have state for, but I do want a QUIC connection. There are two different stateless resets here, actually: one is stop and go away, and one is stop and resynchronize. Example: I have an open socket, and I get packets on the data channel.

ekr: Why is this not done by the WebRTC signaling channel? Side that sends stateless reset also sends negotiation needed.

Ted: Okay, for WebRTC, true. Do we want go away and come back to be in the transport? Or is that tin the application?

Martin: We agree.

Christian: I think what you’re saying is that application semantics are [unint]. Meaning of reset: if you keep doing that, I can’t do anything with it.

Lars: By replying with a quic packet, you’re stating you want to speak QUIC on that port.

Martin: We concluded that this is when an endpoint loses state, the server/client distinction goes away. Making this symmetric is relatively simple and worth it.

Martin: If path elements can recognize resets (which it is has an incentive to do), then it may do so to drop its own state. This might open a vector for DoS: spoofing PR-like packets might drop state. We might want to keep middleboxes from doing this (analogous to RST).

Lars: The stateless reset is for a connection, not a path.

ekr: A sensible middlebox will see this signal and tear down state, unless middleboxes span two paths. Martin’s about to argue we should make this

Lars: I’m still confused. If we have multipath, and a second connection ends up at a connection…

Jana: Question, does a SR tear down *all* state or…

Brian: Does it tear down state on a 5-tuple + CID? Depends on how multipath is designed.

Martin: Three options: (A) Prove: PR20, expose verifier and allow path elements to validate. (B) Grease: Send lots of fake stateless resets to keep inference for working. (C) Hide the stateless reset, make it indistinguishable.

Mirja: You can also do a three-way reset: a reset ends with a synchronization of the reset state.

Martin: How to not leak SR: slide 11. This requires a connection ID on every packet.

Ted: The key must be quite widely distributed across a s

Martin: this is an existence proof?

ekr: The relevant point is the previous slide: is it desirable to hide the stateless reset?

Igor: B or C would have to be invariant for all versions, since version information is not available to the endpoint sending the reset.

Mirja: More important is non-spoofability. All designs fulfill this. Don’t think we need to hide.

Ian: Now that I see the solution for C, I very much like it.

Jana: If SR is visible, you’re eno

Brian T: I like the mechanism as a mechanism; stateless reset as a side-effect of reaching this state...we should have the option not to share this with the path.  Greasing the type means that you have  three possible positions for connection ID, but you don’t necessarily know how to recover connection ID; it becomes less useful to grease the packet type.

Mirja: I like the design, but it doesn’t cover all the cases we have. What happens if the packet ends up at a server --- And endpoint that does not understand a packet to be a reset may send its own reset...

Jana: A very simple design. A server has a constant… In the interest of not ratholing on solution, we can look at other solutions with other properties

Christian: Yes there is a lot of signal here.. exchanging a secret to grease, exchanging a secret to SR -- you don’t want this widely shared. But once you get it, you can use it to do all sort of things, e.g. encrypting the packet number.

ekr: Just sent a long writeup of how to encrypt connID and packet number, but I agree if we don’t do that then we don’t have to grease the type. Nonforgeable, verifiable signals by on- and off-path elements are possible -- middleboxes could respond to this by acting on stateless resets. We could design C’, which requires the middlebox to attempt hash verification on every packet… I don’t know that we can design something that is cheap that doesn’t have the problem that [stateless reset]

Jo: You need some agreement on the secret to make C-type solutions work. Every server in a server farm needs the the same secret; how complex are the solutions here, including the overhead to get that agreement?

Ted: It doesn’t have to be servers that have this agreement. If you’re going to have something like a shared secret, you can leak it forward to a device in the network, e.g. a load balancer. That makes this a more tractable solution, but Jo is right that we’re trading off complexities in the mechanisms for sharing the secret with trusted devices in path there, against something where middleboxes not in that trust circle can’t do anything. Is there a scenario where we want something like A, so we can push the stateless rejector further toward the network boundary.

Mirja: If we want a design like this one then we really want to hide the signal. But if you want to expose, then what we want is a cancel-reset signal. Combine with greasing to force middleboxes to wait for the whole signal.

Brian: ...I’ve lost state.  In this discussion of state-on-path and the middleboxes want to see the end-of-connection signal, there is an unanswered question about how expensive the state is.  If we assume that this state is essentially free, i.e., that you could not care about maintaining state because recreating it is cheap.  This opens up the discussion for later.

ekr: Jo asked about design invariants… designs have commonality on server side, requires server to calculate something it can use to reset every connection. All use symmetric crypto on connection state out of a one-way function. Designs that don’t need conn-id are much more complex. We converged on general design because it has the best-tradeoffs in this complexity space.

Jana: Restating solution here. Revealing information is the general solution here; how the server generates that is a separate question.

ekr: If you want a signature, you actually have to sign packets, so you can’t pregen values.

Jana: I don’t think we know whether we as a group agree that we want o

Igor: Can C be symmetric?

Everyone: yes.

Igor: If SR is indistinguishable from any random packet then you can force ping-ponging of SRs.

Martin (Jabber): easy to fix, see below.

Igor: A middlebox with a broken treatment of ICMP Port Unreach will allow attack already. If the middle box treats ICMP Port Unreach well, it can treat a plain SR in the same way. No additional problem to solve.

Subodh: Clarification: do we expect client to retry infinitely, or should there be guidance on when to shut up. What keeps someone from sending multiple invalid PRs?

Martin: The general philosophy here is that if you throw packets away for too long, then you have a broken link.

Brian: On the question of whether we should hide this, I think that the answer is yes.  The costs for ossification are such that we should avoid them.  With the narrower scope, this is the best conclusion to that problem.

Martin D: Expose non-SR connection shutdown to the path?

Brian: Let’s talk later.

Jo: Agree with Brian. Let’s see what we can do for

HUM Do you think C, hiding SR, is the area we should explore? Strong hum in the room.

HUM Should SR be exposed? Quiet, plus gorry (until we understand more, not sure yet)

Mirja: The reason for not hiding is that we might be another signal, and if we need the exposed signal anyway, it’s not clear that the complexity here will end up being worth it.

Igor: We already have a problem, middleboxes need to handle ICMP well anyway, and they don’t.

Coffee: DRINK ME

### Issue #353 Replace Connection Close with Public Reset

Martin D: This is a middlebox issue. We want to have a generalized end-to-path signal for close. Now SR doesn’t expose anything, which gives you a way to be private. Close signal exposure

Martin T: Close and reframe the question in terms of what signals we want to send to the path.

ACTION Martin D: Okay, will file new issue.

Martin Thomson: Ending Connections slides

Martin T: A connection ends when either endpoint decides to stop. Ideally both endpoints agree at more or less the same time that a connection is done.

Lars: TCP of course does half close

Martin T: Yeah, we have that for streams.

Jana: One of the distinctions we have… FINWAIT states map to connection closing state in QUIC, that happens at the connection level.

Martin T: We can decide to hide the signals, or we can allow them to leak. Explicit signals could use separate mechanisms.

Ted: We can’t cover this completely without a multipath design. But if you want to gracefully shutdown a path, that’s separate.

Buck: Does it make sense to think about how to stay alive?

Martin T: Total loss of connectivity is tricky.

Jana: Someone pointed out that we don’t specify max number of RTX timeouts.

Lars: It’s up to the implementation to decide when it wants to give up.

Jana: We can give guidance.

[loss of signal]

Jörg: As with SR, would we want signaling to connectivity loss to be symmetric?

Martin T: Fatal errors are bound up in CONNECTION_CLOSE; emerging proposal is to restrict CONNECTION_CLOSE to be errors only. The Reason string is good for debugging here. Questions here: what happens if it’s lost? These are solvable problems, just write up what GUIC does.

Martin T: Graceful Shutdown. HTTP/2 doesn’t work with QUIC here, so we should dive in. Proposal: application tells transport to shutdown (at  and transport goes straight into TIME_WAIT like state. No explicit end-to-end FIN signal at the transport layer, application is expected to coordinate this on its own.

Christian: This is like DNS. If DNS over TCP connection not used for some time, then you tear it down.

Martin T: Yeah, if you’re idle for some given timeout, by agreement, the connection is gone.

Christian: In DNS, the time is never fixed. The case you want to avoid is where one side brings state down and the other side doesn’t.

Martin: Yes, in TCP you do this with FIN. So we could create a signal here.

Christian: In current practice, this is more like GC than timeout.

Buck: What if you’re more concerned with network packets than with server state?

Jana: Don’t want to wake the radio to send a fin.

Lars: One question I have about this assumption… it seems to limit apps to those with app-layer negotiation. We might want to invent that.

Mike Bishop: Do we want a stream for session management?

Igor: It seems like this model allows you both options. You can have an explicit FIN-like signal, or you can have a model that and endpoint discovers that you’re done i.e. with PING fail.

Jana: The concern is that not all apps want to do their own signaling.

Brian: In a non-coordinated application and then if both walk away, then the connection disappears and no packets are sent.  In that case, you could also have a signal to drop earlier or rely on stateless reset if you walked away.  This matches what happens in middleboxes.  Maybe you could use 0-RTT to repair a connection if it needs rapid repair.

Christian: I see Brian’s point -- the client doesn’t know whether the server shut down, but it suspects that is might. But it might immediately start a new connection. Server will want to get rid of the state for the old connection,

Brian: you would need a way to use 0-RTT to latch onto an existing connection, where if the connection exists, you could connect to that state if it exists, or do 0-RTT otherwise.  Needs more thought.

Jana: Want to echo something Brian said earlier: it’s important in 0rtt world and UDP nat rebinding to rethink what a connection is and what it needs to be. TCP keeps a connection alive for a long time. You might not be able to do that. There is a cost: PING frames to keepalive. Better off closing connection and 0rtt. Not the world we have lived in, need to think about it that way.

Martin: The biggest concern is that we reach a state that both sides agree. Idle timeout relates to uncertainty about this. There is a parameter: I will wait this long, if you haven’t heard from me, connection down.

Lars: TCP has this, user timeout, option, not widely used. 0rtt is very powerful and new, and you should use this. This might be input for the applicability statement

Subodh: All these shutdown mechanisms are questions of a different API. Protocol machinery is different.

Jana: That’s different from semantics.

Martin T: And close gracefully means different things for different apps.

Subodh: Server sends conn close, client goes away, server rtx, client stateless reset. You again have a not quite graceful close, wake up until then… Propose an explicit close message; I want to do this explicitly

Jana: Argument is that applications usually wait a while and close,

Subodh: There are cases where I want to gracefully shed state immediately.

Jana: So send a message to the other side in the application. Applications haven’t been

Buck: With the right coordination this could be done opportunistically… We might have a chance to be battery- and state-friendly here, this could be driven by the

Brian: Applicability statement says that you need to be careful with 0-RTT; you need to avoid non-idempotent things.  Some of the architectures for load shedding require an explicit shutdown and others don’t.  That’s an implementation-level detail.  There should be an optional close-now thing.  That has implications for how we might expose a shutdown to the path.  If you have an architecture that shuts down the entire path, you might want an explicit signal to the path.

Martin D: 0rtt is not idempotent and not forward-secure. If you haven’t shutdown and your peer has, there is a 1rtt latency penalty there. Going into finwait, would you cleanup state?

Jana: Called this in email the Drain state. If it has sent everything then it waits to receive

Martin D: Will it wait for streams to close?

Martin T: No.

Jana: Defined precisely from last packet sent the first time (regardless of rtx)

ekr: You don’t get PFS with 0rtt, I don’t think 0rtt is a great replacement for the connection to be alive. We have a connection ID, whose whole point is to keep an a connection alive so you don’t have to do this. I do understand the impulse to not stuff stuff into quic, but most apps assume that signaling closing the transport is a service the transport layer provides.

Jana: 0rtt is a useful mechanism, assuming that apps can use it sensibly

Brian T: Yeah, but not as a replacement for state maintenance.

Jana: On timers: any app that wants to keep an connection up, needs to keep the connection up via PING frames. There’s a cost to that. You need to think about it more in QUIC.

Christian: How to do long term state for DNS? implicit close can work, but caveats: state machine must be well-defined, want to avoid states where [unintelligible]. Fine to say server closes if idle for 20sec. Client needs to know it. Needs explicit end-to-end signal. If server has to breach contract, must send a signal.

Jana: Could be an error close.

Martin T: This was the point I was going to make. We spent a lot of time ratholing on 0rtt, but we want to fix this otherwise, by avoiding the state where there is a disagreement. Subodh said I need to gracefully, immediately shut things down. Bit of an oxymoron, but very useful. Fits within this model perfectly well. It’s still an error CONNECTION_CLOSE.

Mike Bishop: Going back to 0rtt transparent recovery -- a smart app can do that. QUIC shouldn’t be transparently creating a new connection.

Jana: Agree. Reneg on a contract shouldn’t be a common case...

Ted: Are we optimizing the right thing here? Pushing this complexity into applications works if there are only a small number of applications. If there are many applications… There’s an another way to do this, if you can have a way to implicitly close by closing streams.

Matt: Flashbacks to SCTP. We wrote a ton of text in 4960 about closing connections that might be useful input here.
Wednesday Afternoon session
Scribe: Sean Turner

Recap: number of people who were happy with the general model, but there was a few want a need for an “abort” connection command.  But, there is already something like that with some minor modifications.  Subodh also wanted to support some gotta drop this stuff.  For applications that have some indeterminate length period they would rely on the abort case.  Applications are responsible for graceful shutdown: remove all state I have on this connection that it succeeds to be best of its ability.

Ted: wants to go back to that this is generally a good pattern.  A common pattern for applications that don’t have stream 3 is helpful.

Jana: Could do something more generally signal.

Ted: To open GH Issue for “common pattern” signal.

Mike B: Because of ordering the changes in on different streams the sender might not have closed all of its streams.  Receiver may see that open streams close to zero.

Martin: There’s also idle time to consider.

Lars: There was a bug in TCP because the sender idle time.

Jana: Need two timers: idle and drain.

Ian:Can we use the maximum stream number as a way to reach this common end state?

Martin: that might work.  It’s effectively a forced-idle.

Jana: gQUIC: send ping frames when they are open.  Do you want to do idle times

Lars: In TCP the semantics are I am willing to keep the connection around as long as there is traffic over a given time.  WHy not allow the same thing for QUIC.

Jana: In TCP, there’s no way for the server to indicate that the connection is done with closing the stream.  If there’s no streams there’s no reason to shut down the connection.

Buck: If we close connections with long-lived streams, then applications will generate their own PING frames to keep from idling.

ekr: Why do we need to dig into this at all?  The behavior seems like an API issue.  The question is not how you signal the connection stack.  It’s really how you signal your peer that you’re done with this or please don’t turn on the connection.

Jana: agreed - where does the timer start.

Subodh: Should we say that the application should use connection close unless there is a good reason to?  Connection close looks like the way to exchange errors?

Jana: Not inclined because he might do the exact opposite.

Jana/Martin: Maybe we can figure out when the timers start later.

Igor: 1) transport to notify local makes sense 2) What is exactly we’re trying to call transport.

Ekr: What do ping frames add to connections that are implicitly open?  Why is this useful?

Jana: need these for silent close.

Ekr: thinks that we can’t solve this.

Jana: Can’t solve this 100% of the time.  It’s FIN wait state in TCP.

Christian: ekr’s concern is totally solvable:  You use different timers on client and server.  The client knows it might take ~3 retransmits to get a packet through, and it knows the RTT.  So if the server says a 20 second timeout, the client considers anything past 17 seconds as “too late” and opens a new connection.  The client has to start its keep-alive before that cutoff.  However, we need to clearly spec which things reset the timer so everyone agrees.

Ted: Referred to RFC 7828 and 7766, which are DNS level mechanisms for managing TCP timeout mechanisms and values.  Might be useful for the editors to review, since it mirrors a bit of their application-manages-close-by-idle-timeout.  If we made stateless reject symmetric then we’ve got goodness.Though it may create a new pattern of where the successor initiator/responder no longer map to the original mapping between application role (e.g. client/server) on the predecessor transport.

Jana: Hesitant to go down this path.  It’s not entirely solvable, but that’s life.

Mirja: Earlier we said they negotiate - we’d use the minimum of the two values. Thinks we need a renegotiation?

Jana: wants to punt on the negotiation mechanism.

Patrick: are we discussing mandatory, optional?  Thinks is recommended but not required.

Martin: Current spec says timeout is mandatory to use.  WE could decide default is 300 years and then it’s really forever.

Jana: Wants some sensible values.

Martin: Want people to set value, but not say what that is.  The thing that would change is the go_away frame would move from transport to http.  Thinks it’s either broken or not very good.

Subodh: Wants more clarity on the responsibility of the transport state.

Jana: Can work on articulating this and sending it to the list.

For Action: Move go_away to http spec, flesh out timeouts, flesh out how the abort connection close works and what the peers are supposed to do, retransmission, acks, and timers.

### Prune transport error codes #467

If you have an error - send some kind of alert.

Martin: Principle do I need to send this to the other side? DO they need to act differently?

Brian: Error codes on both sides: Two error codes if sender and receiver do something different based on them, one if the receiver can only ever do the same thing. Note from Martin T: the debugging case is covered by the Reason Phrase.

Mike:  Pointing back to HTTP workshop, many error codes defined but the only one that gets used is protocol error.  Have been using the alternate direction in HTTP/QUIC, defining error codes per frame type.

Ian:  Would like to continue that direction, so I at least know what area of my code to look in.

Jana: Wants as a receiver of an error code to go fix it.  As a system going to set up alarms.  If I break PING, it will be a negligible increase in my rate of PROTOCOL_ERROR, but might be very noticeable in my rate of MALFORMED_PING.


ekr: in TLS we have protocol errors and they get used.  Don’t need them for self errors, just use “internal error,” but want to call out errors in peer’s behavior.

Subodh: Wants more context, e.g., for the invalid_stream_id.

Jana: The level of granularity is where Jana and Martin disagree.  Jana wants to indicate the peers errors.

Martin: Need a catch all; if you don’t have a catch all, then you’ll discover something later you didn’t think of.

Brian: This is kind of analogous to a parser throwing a parse error without a line #.  Are these more specific errors codes just for testing?

Jana:  No, it’s all about alarms.

Brian: As long as you can identify the frame, you’re good right?

Mirja: Reflect part of frame with the error?

Ian: Add packet # as an optional field?

Jana: We have one frame error or per frame type error code?

Ekr: It’s valuable to be able to determine what was busted?  Do we need machine readable code?

Mike:Reason code i not just that it’s optional it’s free form.

Martin T: We recommended UTF-8.

Igor: Arguing for a string is better than pre-canned error codes.  The alarms are for the apps and the string give you the ability to create more.


Marten: Why are we trying to cut out ten bits out of it to make one.  Using the string doesn’t make any sense.

Lars: The string is going to be a red herring for internationalization weenies (i.e., Apps ADs).

Jana: Granularity of errors is good they use it.  Why not use it?

Igor: would it be better to use HTTP style of error codes?

Ekr: THe resource being consumed here is developer and standardization time.
Jana: completely agrees - because there were too many of ‘em.

Lucas C: The error string less usable might want to include dynamic information in there.

Martin T: We do see decode errors during test.  THere’s a bunch of error types.

Ian: This does come to play.

Jana: Yes part of this is that it’s a new protocol.  Because we’re going to have experimental we’re still going to need so many.

Subodh: these errors should be useful and should be exchanged.

Roy: If it’s optional should we just allow people to use it.

Ekr: every single error in NSS that parse TLS. gives the same error.  More errors means way more programming errors.  More errors are good but want to avoid implementation complexity.

Martin D: There is a trade-off space here: one hand complexity the other is not knowing where the error.

HUM on: In addition to a generic frame error, we’d have a more specific you fucked up this frame error.

Hum results: clearly more support for the compromise.

Dissenting opinion (Jana): Not convinced that we need more generic error if we have the more specific.

Ted:  More general errors have to exist, because not everything will fit neatly into a bucket.  If the more general errors exist anyway, it’s effectively an implementation detail whether someone sends you the specific or general.  Just deal with it.

Consensus: go with the compromise

### Packet Number Echo PR#269

Packet # echo is seeable by network boxes, but not ACKs because they are encrypted.  Need this for RTT measurement and AQM.

Jana: We shouldn’t rathole on the design; there is a PR.

Brian: This function consists of at the packetization layer - echo the latest or highest.

Ekr: If we encrypted the packet #s what would the impact be. Answer, not very useful.  Could you echo the authentication tag - yes, that would give you most of the data you needed because it’s unique to the packet.

Ted: About context: we don’t have to see it as control and we don’t need to echo it.  If it’s a unilateral agreement between the two end points that want to share it with the network, you can pick anything that’s known to both as the echo fragment.  If you choose to make this as a bilateral, the info need not have any bearing on the state information shared by the endpoints.

Markus: Use the more better AQM in mobile networks.  Use TCP proxies for this now.  Reduce buffer bloat and well behaved flows over the radio.  There is AQM in radio base stations and they’re kind of out of date and it’s costly to replace them.  Now experimenting centralizing AQM to see RTT progression over different flows.  The nice benefits is that we can be up to date and we start to see really good performance.  But in order to do this we have to estimate RTT and we can’t do that now.  We’d like an explicit way to get this as opposed to relying on information leakage.

Marten: From this helps with Cubic, but QUIC is going to use BBR

Markus: If everybody used BBR maybe, but we can’t expect that everybody is going to use it.  NewReno is what is currently specified.

Lars:  We’re chartered to use standardized congestion control algorithms, which at the moment means New Reno.  If BBR is done by the time we ship, we can use it.  If we think we have to use it, we can even wait for it.

Christian: 1st point: it’s really good to take care of the this in the network. 2nd thing I heard Rtt measurement whether you want RTT or packet #s.

Markus:  It’s RTT measurement not packet #s.

Lars: Could you use ECN marks downstream to figure out if you’re building queue buildup.



Magnus: Radio networks has rapid fluctuations in throughput in some situations. We also want ECN for QUIC, especially as way of signalling from the AQM to the QUIC congestion controller to react on buildup, preferable L4S like (See draft-johansson-quic-ecn). However, the RTT measurements Markus talks about are a way to implement the AQM so that it can mark also for older base stations. We are still uncertain of how well BBR works over wireless links.

Brian: There are several other applications: Straight up passive measurement - operator monitoring and regulatory monitoring.  Why is this on packet echo # - it’s easy implementable and closest to what’s done now.

Lars (chairs prerogative): These are not part of the charter - regulatory measurement is not in the charter.

Lars (again): If there’s a fraction of TCP traffic in both scenarios does it still work?

Markus: For AQM yes

Brian: For measurement, the paths need to be comparable. Of course, there’s a very easy way for force passively-measurable traffic to be generated: just block QUIC, take your measurements, then stop blocking QUIC. We want to find a way not to use that sledgehammer.

Jana: Points 1) There is differential treatment but that’s near the customer, 2) measuring across two points you can still get measurements.  Doesn’t really think that QUIC will completely replace TCP.  Can we solve it differently for QUIC.

EKR: What’s good for the end points?  What is it costing us to do this?  If we can’t encrypt then I care a bunch.  If we can keep it encrypted care less.  If we need to make sure that both sides agree to this - i.e., to Ted’s point that it be bilateral agreement.  And, making it an opt-in.

Jana: The middlebox needs to know too.  Make this a trilateral agreement.

Ian: There is evidence BBR performs better without TCP termination, so it seems possible it may make AQM less necessary, but still a good thing.  I believe it will be standardized, it’ll likely be a while, but I expect before QUIC is standardized.  Ted first brought up a good point that there are three options: 1) Do nothing 2) Make this optional.  3) Make this so required it MUST be on every ack and the transport won’t work without it(which I think would preclude encrypting packet number)   How often are operators and others using passive monitoring today?

Brian: 8 separate vendors shipping IPFIX measurement boxes do passive measurement. Mostly customers care about downstream latency, upstream latency and loss

Christian: *Privacy*  Q: What is the precision? A: Couple of measurements/RTT.

Markus: We aim for is a couple of measurements per RTT.  Not getting the information is not catastrophic.  We look for RTT and how it changes over time.

Emile: Review the TCP header info to make measurement and per segment measurement.  Used for troubleshooting, volume, etc.  Thinks the 1st version of QUIC should carry data to help.

Martin D:  1) Service providers think they offered this to customers.  Bilateral agreement falls afoul of this. 2) As we’re moving away from packet #, why not just put an RTT measurement in this field.

Mirja:We have diff mechanism to get the same thing. TCP was just the easiest.  Why don’t do something for just measurement?  Keep it separated from the internals of the protocol.  The reason why we use packet echo is because it’s already there and provides some additional information.

Brian: we could converge on bi/tri-lateral opt-in packet type in the short header that is sent sometimes that is a QUIC-RTT header.  Gives us a way to not use the internal protocol bits, and can run while the protocol runs.  Making it optional lets us determine whether there is actual value for the endpoints: If it works they’ll keep it and if not ditch it.

Jana: Responding to MartinD: if you’re going to put something like RTT explicitly that the middle box wants it.  It might be just noise.  Responding to Brian: likes the idea of a tri-lateral agreement but don’t know how to do it - may be bi-lateral that exposes it.  Can block QUIC if the agreement is not there.

Igor: It looks like we have the case where somebody on the path wants to do the measurements but the endpoints won’t know that this needs to happen or how often.  What about an ability to have the middlebox to set a bit requesting it be done.

EKR: It would be superior for it bilaterally agreement, but there’s a concern that middleboxes will be used to hold traffic up.

Dan: Responding to Martin D: not done all the time, but done only when traffic is abnormal.  Having it default on would be a LOT of data.  Having some special packet would be useful.  Igor is also right that we don’t want to be flooded with the data if we don’t need to do the measurements.

Christian: Point out that there are other designs: measurements today are based on IP - and we could do the same thing with two QUIC header packets.  What are the properties - doesn’t expose packet #, x.

Sanjay: Can only hold traffic because of DDoS, etc. can’t drop traffic because of regulatory concerns.  Need to know at what point you are compliant with your SLAs.

Jana: In response to Sanjay: UDP and TCP traffic is throttled.  Operators will have some knob and can use it stomp on your traffic if you don’t give them insight.

Jo:  use a separate set of frames than overloading existing fields.  What happens if it’s not implemented and it’s not used?

Ian: It might get fixed when operators ask for it from servers.  It has worked in the past.  Can turn it on for some small %.

EKR: The scenario there is a signal that says when you don’t do this is different than you packages get mysteriously lost.  Concerned, that unless there’s someway to force users to opt-in before network access will result in hostage taking.

Brian: Don’t want to enable the hostage taking.  This is more restrictive.  End points should have control.  What’s the conops for this?  Don’t need to run it all the time, and only on small % of traffic.

Ted:With a bilateral agreement, note that the hostage knob has to be pressed by both the end user and the system they are talking to.  The hold the operator has on the system to which the client is talking may be much smaller.   This is another good reason for wanting bilateral agreement. What knobs are needed to control sender-side sampling? In browserland we have 1% experiments, but maybe that’s not the best model.


Jana: What are we taking out of this?  Completely sympathetic to ekr’s concern.  Making it bilateral ios nice, but we know it’ll be used.  You have to incentive the endpoints if it is to be used.  If we are in agreement that we need to design it, then it ought to be bilateral.

Mirja: Operators might need operators to know there’s a problem right now.  End points have some of the information now and they can make a determination about when to give up this info.

Dan: What’s important to know about when something gets dropped you have to keep Enterprise networks in mind. These agreements need to be frictionless.

Lars: would prefer to minimize the information exposed, maybe just one bit that could be always used.

END OF QUEUE

Action Item - Brian to propose design and document use cases it covers, focusing on passive RTT measurement. Design considerations should include fingerprint resistance, lack of hostage negotiation.

May use red/blue packet idea (we’ll coin the packet tuple “Neo”)





## 8 June 2017

Mark:  Based on feedback from previous days, we need to time-box the discussions.  The conversations have been good, but to make progress we need to actually close.  Discusses queued presentations.

Martin:  These are the topics that will have large downstream effects on many issues; if anyone can think of others, please speak now.

Ian?:  Extension frames?

Martin:  Yes, but maybe not now.

Christian:  Soon.  This implementation draft or the next.

Mark:  This should take us until lunch.

Ted:  HPACK/QPACK/QCRAM?

Martin:  Probably a useful discussion after lunch.

Lars:  We got a request from Ericsson for ECN.  We’re going to discuss that in Prague; not blocking first implementation draft and need more transport people in the room.  We should get to this soon, though.  Also relevant to the middlebox discussion.

Ian:  On ECN, anything we could do to encourage exposure of ECN via OS APIs would be helpful.

Jana:  Does encrypted metadata cover the handshake?

Ekr:  No, mostly packet number.  We can talk about handshakes separately.

### 1-bit Path Information

Lars:  At dinner, there was strong interest in exploring Christian’s idea from yesterday.  Seems to be minimal enough to give middleboxes RTT and flight size.  Has the advantage that this doesn’t impact the QUIC state machine, so it doesn’t permit interfering with QUIC or inferring internal state.  Could even be implemented in the NIC, perhaps.  It’s so minimal, we might be able to mandate implementation.  Useful for middlebox vendors, since they can rely on it.

Ted:  MUST implement, or MUST employ?

Lars:  Implement.

Ekr:  Is a conformant implementation required to flip the bits?

Lars:  Yes, but if you don’t, it still works.  Only downside to not doing it is depriving the network of information.  Seems like the sweet spot; exposes good information and doesn’t appear to create any vulnerabilities.

Patrick:  Easy for endpoints to tell you’re not doing this; not always for network.

Mike:  Until you have improbably RTTs.

Brian:  Everyone who’s interested needs to go read draft-ippm-????, which specifies almost exactly this.

Christian:  Probably a previous version of this.  If you want to add a reference, that’s fine.

Brian:  This is basically a report from an experiment Telecom Italia did; they found it useful.  Also specifies packet loss and one-way delay measurement.  Might want to look at complexity on send side versus additional information.

Christian:  If I remember correctly, it’s handled by additional options.

Brian:  Yes, because they didn’t control the transport protocol.  We do.  This does have the quality that you can make it bilateral; node that doesn’t want to participate sets to zero.  Mechanism to turn on/off?

Ekr:  Require initial packet set to 1 for participating, 0 if not.  Simple enough.

Brian:  Take detailed discussion onto the PR.

Patrick:  This does explicitly expose what data (which window) is in which round trip.  When a protocol has a request-response pattern, it becomes easier to tell which packets are in which window.

Christian:  Yes, and if you’re a super-potent adversary, a little machine learning will get you that anyway.

Patrick:  So are we saying middleboxes should do that?

Christian:  They’re not all ominpotent.

Lars:  Look at the PR.  This looks like a good way to handle the issue in line with our charter.

### Unidirectional Streams

Martin:  Assume people know basics of unidirectional already.  Premise is currently two coupled state machines.  Some steps to break that already; this is the next layer of break.  Removes implicit coupling between outbound and inbound data.  If you’ve read Bryan Ford’s SST paper, models stream-based transport as streams-are-messages.  Lots of protocols model as one-to-one inbound and outbound messages, but not generally true.  H2 is one-to-many due to server push.

Request: a link to Bryan Ford’s paper, mentioned by Martin, should go here and here it is: http://www.brynosaurus.com/pub/net/sst.pdf

Ian:  I didn’t get that from the SST paper.

Martin:  Lots of people read it and go back to the old way of thinking promptly.

Jana:  You can use short-lived streams for that.

Martin:  Yes, but…???  (Can someone fill this in?)

Christian:  Even Stream 0?

Martin:  Yes, and I’ll go into more detail.  Lots of issues because of the existing coupling; they just go away if the sides are independent.  Part is predicated on assumption that DISINTEREST proposal gets accepted.  Currently require that if one direction gets RST, other side has to RST as well.  Mike’s proposal breaks that, so you can terminate one direction and still send data in the opposite direction.  Useful in H2, server not interested in body of request but can still respond.

Other niggles, like needing to send empty frames with FIN for one-way streams (e.g. push).  Alan also pointed out that when you send GET request, if the empty frame to open the body stream gets delayed, server can’t respond.  Can hack around this (swap streams) but it’s a kludge.

Current model is good for one-to-one protocol models, which seems general, but it’s not actually.  Server push doesn’t have this model.  The approach people are looking at for RTP certainly isn’t one-to-one.

Ekr:  N-to-1 meeting.  Not a 1-to-1 mapping in any sane way.

Martin:  Not without major surgery.  CoAP is one-to-many.  Websockets.  Basically everything is multi-way.

Jo:  Anything pub-sub is that way.

Jana:  What do you mean by “unidirectionality has an effect on protocols…”?

Martin:  There’s no longer a necessary coupling between outbound stream X and inbound stream X.  You need to explicitly couple the related streams, because the stream ID is no longer sufficient.

Buck:  Can’t the application close the one-sided streams?

Martin:  We already decided to remove that.

(#515)  In TLS 1.3 1-RTT, the server can speak first, but in HTTP/QUIC there’s nothing it can usefully send except SETTINGS.  However, Stream 3 is client-initiated, so the server can’t send until the client does.  Server spends a whole RTT with no ability to say anything.  Could move to stream 2, but in 0-RTT client can’t speak first.  We could switch based on TLS mode, but that’s painful.  Server could assume client will speak by the time it receives its packet, but different implementation issues could cause that to break badly.

Jana:  Why can’t you always use stream 2?

Martin:  Because the client can’t speak there.

Mike:  Could use 2 and 3 respectively.

Martin:  Then you’re unidirectional already.

Push operates in two stages -- promise on response stream, headers/body on other streams.  Can be from Link headers, can be from parsing/generating body of response.  Promise needs to happen before actual link reaches the client to avoid the race condition.  Otherwise, there are terrible inefficiencies.  Problem is that the order you discover is different from the order you want to deliver.  Script before images.  You can run out of space because you have to consume the streams in the PUSH_PROMISE.

Buck:  In H2 that was decoupled -- you can promise a stream that you’re not allowed to send.  Why can’t we do that here?

Martin:  In QUIC, usage has to be completely sequential.  That doesn’t work.

Buck:  You can’t control wire order; things can appear in any order.

Martin:  Has to be a contiguous block; if you’re allowed up to 100, you can’t use 170.

Buck:  We’ve simplified ourselves into this problem.  H2’s reserved state dealt with this.

Martin:  But that creates unbounded state commitment.  We fixed that bug.

Buck:  Not unbounded.

Jana:  Could address bug in other ways.

Martin:  This is another way.  Ideally, you could fulfill the promises in any order.  Even if we had a reserved state, you couldn’t progress until the client gives you credit.

Buck:  Can still use priorities.

Martin:  No, because of the window.

Buck:  (groan)  Now we have a window, where before there was a count of streams.

Martin:  Diagram of current state machine, not including DISINTEREST.  But current state of DISINTEREST PR doesn’t actually affect state machine.  Basically rip state machine in two.

Ian:  Need to FIN/RST each direction?

Martin:  Already true.

Ted:  This doesn’t reflect the need for an explicit correlator.  The main thing useful about this is the ability for a stream to be correlated with 0, 1, or N other streams.

Martin:  True -- we’ll get there.  Note that RST of idle stream is no longer possible.  That’s no longer needed.

Subodh:  Shouldn’t it transition to open, then closed?  Reordering can make the RST arrive first.

Martin:  Yes, but you won’t send that.  That’s an artifact of receiving things out of order.

Ekr:  If I get a RST_STREAM for stream 6, I need to open 1-6, then close 6?  Why are we opening streams implicitly?

Martin:  Technically don’t need that now.

Subodh, Ian:  Really useful, though.  Much easier to track state.

Martin:  Discussion on list that this shouldn’t be receive STREAM, it should be any frame that mentions a stream.

Impact on HTTP.  Slightly different from Mike’s version to address different problems.  If you’re responding, you say what stream you’re responding to.  Push streams identify the stream and promise ID they’re fulfilling.  Header streams identify whether to expect bodies; body streams would need to identify where the headers were.  (Unless we take #557.)

Ted:  That means PUSH_PROMISE doesn’t include the stream ID?

Martin:  Don’t need to; and it supports responding in any order.

Buck:  One of the things we liked about double streams in HTTP was that bodies wouldn’t need framing for the body.  But you need framing for interleaved PUSH_PROMISE with the body.  This leads to a nice simplification, but some protocols would want multiple duplex channels.  Might want to be able to split body across several streams.

Mike:  Might be possible in my model; we’ll talk about that if QUIC changes.

Martin:  Let’s talk about what we have now, add new stuff later.

Kazuho:  Can we still let the transport correlate the two sides of streams?

Martin:  Not easily; requires deeper understanding in transport.  Final thing you need here is that you can’t RST a push because the stream doesn’t exist yet.  Requires new frame at HTTP layer.

Buck:  Today PUSH_PROMISE tells you what stream it will appear on.  Can’t you cancel that?

Martin:  Mike’s version still does that; mine uses an identifier for an unknown stream.

Ted:  That concerns me a little bit.

Martin:  Advantages here.  No empty streams required.  No odd/even streams.

Buck:  How do you decide who owns which streams?

Martin:  Independent numbering spaces -- you own your stream 5, I own my stream 5, they’re not the same stream.  You can have twice as many messages, because you don’t have the even/odd split.  Saves a lot in HTTP where many messages don’t have bodies.  Wouldn’t need to burn streams.  Other advantages (see slides)

Maybe-negative stuff:  Pushed streams and response streams are now in the same pool -- more flexibility for server, but client has to manage appropriately.  Extra correlators at start of each stream; slightly more framing, but probably outweighed by savings on empty streams.  Probably comes out in the wash.

Different Martin:  Is that correlation in the application or in QUIC?

Martin:  Application.  Note that client can make more requests than server is allowed to answer if they get it wrong.  Clients can back themselves into this corner.

Buck:  Note that gQUIC doesn’t have quite that problem; we’ve made this push problem for ourselves.

Martin:  But we’ve made those changes for good reasons, so we need to deal with it.

(goes through before/after examples)

Realized that we could solve the PUSH_PROMISE with bodies issue with this too, but ran away screaming.

Jana:  What is your goal here?

Martin:  Plant the seed, see if there’s enough interest to write up a PR.

Christian:  This would make the DNS-over-QUIC mapping slightly simpler.  Currently have two ways to correlate response to query; need to have extra check to make sure they’re aligned.  If there’s just one correlator, it’s simpler.  Second, we have a couple security considerations about misuse of stream numbers; how does this impact those?

Martin:  Doesn’t change them meaningfully.  Makes control of number of streams more direct, but you had control over that anyway.  They’re effectively the same.

Christian:  Two maximum stream IDs now?

Mike:  Same two we already have.

Martin:  No longer implicit permission to send responses.

Ted:  Doesn’t seem like it goes far enough if you’re going to go here.  If it’s many-to-one, the syntax doesn’t actually work here.  Look at RTP -- many flows over QUIC, with a RTCP-equivalent flow in the reverse direction.  Need to say this RTCP references streams 1,5,9,17, etc.

Martin:  That’s totally possible.

Ted:  But now you’re requiring the application layer to manage the stream IDs as well as their identifiers.

Martin:  Not necessarily -- if you already have a correlator in your protocol, just use that and don’t worry about stream IDs.  HTTP is unique in that it has historically relied on TCP or H2 streams to implicitly correlate.  RTCP already has that, DNS already has that, don’t need to build anything new.

Ted:  Would like to see a one-to-many example.

Martin:  This is one-to-many, because of push promise.

Ted:  Having to manage that in the application layer is where the complexity will come from.

Martin:  Yes.

Buck:  A lot of applications depend on TCP being bidirectional bytestreams.  We’re punting problems to higher layers; we might need to define an upper layer that provides bidirectionality.

Martin:  Every protocol I’ve looked at isn’t strictly bidirectional.

Buck:  Sure, every protocol can work if you tweak it.

Martin:  Of course.  There’s enough in QUIC that you’ll need to create a fresh mapping anyway.

Buck:  I like that this open up new capabilities.  I also think we should think about how priorities work with this.

Martin:  I don’t think it changes priorities at all.

Buck:  I think it does.  Example:  GRPC is a bidirectional message stream over HTTP.  People would like to have different priority between these messages, which this opens the door for.

Martin:  That wouldn’t be HTTP any more.

Buck:  This isn’t HTTP anymore.

Jana:  The focus on users of unidirectional streams suggests this simplification.  But other applications use bidi streams because they’re used to TCP.  They’re useful, and we shouldn’t automatically throw them out.  Could we consider a mix of unidirectional and bidirectional streams?  Yes, it’s more complex, but if complexity scares you, you shouldn’t be here.  I don’t think there’s support for saying every application needs to go unidirectional.

EKR:  Why RTP/QUIC mapping is the way it is (one-to-many)?  The stream is a bundling mechanism, not a semantic mechanism.  Kind of sad that HTTP/QUIC is inheriting the idea from H2 that the stream is the message.  Main thing you’re getting is “end-of-message” marker.  This helps break that mindset we have from both TCP and H2 that streams are a first-class concept for the application rather than a convenience.  Seems like any bidirectional-based mapping is easy to emulate here.

Ian:  For many applications, this is an improvement.  But this is a departure from what we’ve had for so long, and this may be imposing a lot of work on the application mappings.  I would feel better if someone tried to code this up and prove they could do something useful.  Not volunteering, but I’d feel better if there were at least one implementation.

Christian:  We already have bidirectional data on stream 0.  Even if I build a simple stream-per-message API, I still have to build bidirectional support for stream 0 and the crypto.

Martin:  Yes, but that’s pretty simple.  One stream in each direction.

Christian:  But you can’t do the stream-per-message abstraction there.

Martin:  I don’t see TLS as independent messages; the order matters, so you want them on the same stream.  Ian wants to see someone do this; I do too.  “Have to pass the bill to see what’s in it?”

Ekr:  Minimum is a PR plus some code.

Martin:  The code shouldn’t be hard.  I understand the reservations people have, but I think it’s worth the effort to explore.

Jana:  This is fantastic.  There is simplification here, and HTTP isn’t quite bidirectional.  Most interesting applications have that weird “not quite” situation.  What’s the best basic unit to start working?  Is there a compromise here?

Martin:  Looking for a superset?

Jana:  Yes, that’s my biggest concern.  Can whip this up in a few days, but I’m wary of standardizing this without having actually used it for real workloads.

Martin:  If that’s your best argument, we’re doing pretty well.

Jana:  Standardization is something you do when a bunch of applications have built something and you understand the corners.  We don’t understand this yet.  As to stream zero, all the streams are a bundle of bytes.  You can’t say messages versus bytestreams.

Jo:  I’m in favor of this.  I’ve had to think about how IoT protocols would map on QUIC, and currently how they map onto TCP/UDP is awkward.  This would go a long way to helping.  But what do we mean by “code” as our standard?

Martin:  I understood Ian to mean a proof-of-concept that there’s no weird corner cases.

Ian:  Take an existing codebase, give this a new version number, and make sure it interoperates.

Martin:  Might be able to poke at QUIC-Go, but I don’t think we’re there yet.

Jana:  Kind of premature.

Mark:  Martin, do you need anything else?  What’s your timeline?  Prague?

Martin:  Might not have the implementation by Prague, but a PR should be feasible.  Enough people now interested that I’ll have help; come talk to me.  And Mike already has some text, but it looks different from what I have here.

Mike:  These are in the “unidirectional” and “unidirectional2” branches, but no PR from them yet.  Unidirectional keeps stream ID correlation in HTTP and breaks them apart at the QUIC layer; Unidirectional2 changes the HTTP mapping to leverage the changes.

(Coffee break)

### Encrypted MetaData
(slides: https://docs.google.com/presentation/d/1Tm37PG7V4agIB_VvW73QYDmIy4UCY9lf1BDgkz4SPME/edit)

Ekr: Encrypt all the things because we don’t know where the leaks are.  Not asking for action today, but we should try to minimize leaks where we can.

Ian:  Some leaks are useful for debugging.

Martin Duke:  Can’t you see a new 5-tuple without a handshake and infer a migration?

Ekr:  Maybe, depending how much is going on.  Main source of leakage is the handshake; we’ve done work to make the TLS 1.3 handshake better.  If we had DPrive and SNI encryption, we’d be a lot better.  But most of QUIC’s leakage is the TLS handshake, so QUIC can just ride along with our progress.  That leaves correlation between packets: Connection ID (explicit correlation) and the packet number (implicit correlation).

Major design options:  Status quo.  Omit Connection ID, encrypt packet number.  Encrypt both.

Christian:  What about changing Connection ID on migration?

Martin:  Already have that.

Ekr:  Yes, but it’s not fantastic.

Christian:  So for Connection ID, we’re really talking about migration / path change the client isn’t aware of.

Ekr:  Yes.  (2) still provides some value, and it’s probably better than the current packet number skipping approach on migration.  Don’t want to get into weeds with crypto, just proof that it’s possible.  AES-ECB, AERO, etc.  Different options with different trade-offs.

Martin Duke:  How about the use of PN as the IV?

Ekr:  Use the decrypted one.  Or the enciphered version, either works.  But the decrypted one decouples them.

Subodh:  What does this do for PN compression?

Ekr:  Always the big one.  But Aero is better and would help with that.

Ian:  We could pre-define our window.

Ekr:  Or in-line encode it.

(Crypto discussion)

Ekr:  These are the weeds I didn’t want to get into.  What considerations should we have in deciding whether to do this?

Christian:  If we decide our requirements, we can ask for the crypto algorithm we need for the sizes that are relevant.

Ekr:  Rathole warning:  Next slide is an attractive nuisance.  It’s a lot of overhead, but it could actually be simpler.

Ian:  Byte-wise, the overhead is more.

Martin:  Not as bad as ECB.

Ekr:  Yes, it is.  Server gives you a pile of tokens which are opaque to the client, and the client just uses them on successive packets.  Just need a strawman way to construct the tokens.  Effectively burns 32 octets of overhead in each direction, since server has to issue and client has to use, offset by no longer having packet number or connection ID in packets.  That’s how we get the 20 bytes net overhead; fancier crypto might bring that down.

Martin Duke:  Server does this as well?

Ekr:  Think you need to do this bidirectionally, but if you’re omitting the connection ID anyway, you can use (2) in the server-to-client direction.  These are mostly proof of plausibility -- please don’t pick on the proposal, but this demonstrates we could find a way to do it if there’s a will.  What to discuss is: what is the bar to meet before a technique like this would be adopted?

Ted:  Middleboxes would have no access to the connection ID, which means NAT rebinding would happen as often as it does now.

Ekr:  Correct.

Brian: Unsurprisingly, I’m not sure I buy “encrypt all the things” as a first principle. Prefer allowing endpoints to make privacy/performance tradeoff. I mean, I like encryption, but I’m afraid that it’s far too optimistic about the limitations of analysis resistance given the existence of non-header and other essential metadata. But that doesn’t actually matter, because the correlation leak is very real and I don’t see a workable way to close it without either rearchitecting every access network or removing PN/CID from cleartext. OTOH the encrypt everything seems heavyweight, but not insanely so. Other notes on trade offs: encrypting CID makes it useless for ECMP, if we care about that. This conflicts with symmetry as a principle. On debugging: a common (out of band) debug interface might be a way to address that, but that seems complex.

Jana:  Important to know what the complexity is; it can be debilitating on the server.  Value in having these things is that they’re used.  Options don’t always get used, so don’t build five options and maybe-support-or-not.

Ekr:  Yes, just looking for level of interest.

Jana:  If this makes NAT rebinding not work, that makes QUIC not useful.  That’s a basic bar.

Martin Duke:  Why do you say QUIC wouldn’t be useful in the face of NAT rebinding?

Ekr:  So why can you remove Connection ID now?

Ian, Jana:  We only turn it off server-to-client in practice, even though the protocol allows it symmetrically.  NAT rebinding is important, and we leave it on client-to-server because of that.

Martin, Ekr:  Then why is turning it off supported at all?

Roy: Ditto what Brian said, except I don’t think it is worth exploring what to encrypt as a base without some notion of an attack that this would actually prevent.  Traffic analysis can defeat this already.

Ian:  (3) is terrifying from a code perspective.  Doing flow control on packet numbers is guaranteed to get it wrong.  Less concerned about (2), that’s an existing code point, but it’s overhead.

Igor:  Removing CID would reduce reliability due to load balancers misrouting packets.  Encrypting CID will make it difficult to rotate shared keys, since load balancers cannot easily verify whether the new or old key has been used.

Victor: is protecting connection in the event of migration without explicit signal even possible?  That would require connection look the same no matter where you split it, which is infeasible because of congestion control and other considerations.

Mike:  Does this break the one-bit RTT measurement protocol?

Ekr, Martin:  No, use the 5-tuple.

Ian:  Unless there are multiple QUIC connections between the same hosts -- then it gets really messed up.

Sanjay:  (???? Missed this, sorry.) impacts to load balancing, troubleshooting and connection migration has when both ConID and Packet ID are encrypted? [Sanjay]

Martin:  What are the constraints?  We’re optimizing for saving bytes in some places and dumping bytes in elsewhere for other things.  Right considerations are:  Key management is tricky.  To a lesser extent, computational cost, but this is low enough.  Most modern CPUs can handle this without noticing.  Primary concerns here should be operational -- can I deploy a load balancer feasibly?

Mark:  Ekr, do you have what you need?

Ekr:  I think so.  Take-away:  People are fairly enthusiastic, but not universally.  Concerns about what this does to load balancers.  Willing to put more effort into this -- no one has said “death before this.”

Brian:  Expected to be at that point, but sounds like we’re converging on a separation of measurability and the protocol aspects.  That satisfies me.

(Break for lunch until 2 PM.)

(Returning from Lunch)

Mark: We still have one party missing, including Jana and Mike.  They enter, to wild applause.

Mark:  We have a scribe again.  We left at a pretty good place before for lunch.  We seem to be dwindling a bit, but we’ll move on.  Other topics:  hpack/qpack (30minutes); verifying migration and ACKs (30min), revisit the first implementation draft (and potentially touch on the second implementation draft). We are scheduled to end at 5:00, but we have touched on everything that is blocking the first implementation draft.

Jana: I would like to put aside some time to see if there are high order concerns.  We may not consume.  Are there issues that cause people concern.

Martin:  I’ve been trying to get to those, but maybe unsuccessfully.

Jana:  Yes, but we should have some open time.  I also have two more issues:  go around the room and ask about implementations, to see if there are changes in folks’ thoughts after the meeting. The second is about process for involvement and engagement.  I would like to see what we can do to make the working group go better.

Mark.  That’s good.  That also reminds me that I had a discussion with Martin as going to lunch; if you are interested in working on the unidirectional streams question, please jump in on that discussion.  Not as a separate list, but together.  Martin:  I’ll put that into a PR, and we can comment on that as a group.  That will make sure what we have in Prague gets us to a concrete discussion.

Jana:  that will be really valuable.

Mark:  let’s have this discussion right now.  As a chair, I see the editors as very active, but it would be good if others were more active.  Maybe via pull requests and engagement on them.

Jana: it does take a bit of time, as we have mailing lists, issues, and PRs and there are discussions on all of them.  That makes tracking discussion hard.  Most people are tracking the email list; some are tracking issues; even fewer PRs.  We may want to be explicit.

Mark:  the IETF process requires that the mailing be a valid place to have a discussion.  We should all be on the same page.

Lars:  there was a point earlier that involved discussions shouldn’t be on PRs, they should be on issues.

Ekr:  that’s not what’s happening.

Mark: yes, but we should be clear.  When people raise architecture issues, they should be pushed out to issues.

Jana: currently tracked with “design”

Mark/Martin: yes, but we could have a third and push the “architecture” onto the mailing list.  “Design” means needs-consensus, i.e. not purely editorial.

Brian: the time I have for this is very bursty.  The time I have to get up to speed is short.  It is much easier to work from issues, since there are core areas I care about.  I can look at those and see that the right people are there etc., but it adds significant re-synchronization time.

Mark: if architecture questions were separated out, we might get less duplication

(several): yes

Jana: it took me a while to digest the work style, even if in the contributing.md.  That may be entirely my fault.

Mark:  I’m happy to ride shotgun on the PRs and say “take it to the list, off the PR.”.  Can we take some action items to boil down some of the architectural issues?

Jana: yes, but time consuming.

Mark: yes, but if there is the will to do that, it will pay back benefits.

Brian: there are benefits to that in identifying holes in the architecture.

(bike shedding on the “architecture” tag color--needs discussion).

Patrick: I’m normally a fan of github issues, but it does not do threaded replies well.  With “architecture” issues that might be particularly painful.

Discussion of threading and quoting pain and whether folks like gmail or github or hate both.

Patrick:  it may also get some of the IAB not active in the group to focus on the right things.

Jana:  I prefer email threads over issues.

Mark: I’m hoping moving these out will pull some heat from other issues.

Ekr:  It would be helpful for me to know what status PRs have, so I know when to focus on them.

Mark:  Should point to the issue it resolves.

Ekr:  That’s not the point.  These are provisional, and it would be useful to know how soon things will land,  so I can prioritize.  Those that will land soon need to be higher in my queue. Maybe have a date target?

Mark:  can’t really do that.

Ekr:  Maybe just label with “review promptly” to indicate that it will be landed soon.

Martin:  they are sent to the mailing list.

Mark: landed doesn’t mean improved here, which may be different.

Mike: some PRs are editors intentions, while others are suggestions for contributors.  They are different classes.

Ekr:  I just assume that anything from an editor will get merged in some state.  “Merge imminent” tag.

Mark:  will an email to the list do it, because that is close to what we now.

Jana:  but the linkage is to issue, and closing the issue is what triggers the landing.

Mark: I’m with you, we don’t want folks to look at the PR first, but at the issues.  But an explicit “ready for merging in the issue” would be good.

Ekr: fantastic.  This just makes it easier than backing things out would be, since that requires a new issue, etc.  Not trying to get rid of editors latitude, just trying to make the reviewers life a little easier and the work more focus.

Martin:  I’m willing to put work into this, since it will help keep things from rotting while they are outstanding.

Ekr: sometimes we also have a “help wanted” tag, that will attract attention from those who might contribute PRs.

Jana:  the one thing we have not done successfully is do these on the issues, there are spread comments between issues and PRs.

Mark: is everyone willing to try the tags?  (yes).

Mark: do we want to go to higher order questions?  (Pushback) It goes further back into the agenda.

Martin Duke: architecture vs. design?  Design is something that needs consensus, but architecture is a higher level set of issues (like the jeopardy/game show categories).

Ekr: higher order question--have we punted on loss detection and recovery until later?

Jana/Ian:  I think we have.

Martin Duke:  I think we want to decide whether the second draft will iterate on the transport or move to mapping draft?

Mark:  the 2nd draft will probably be loss recovery, plus whatever we learned from the first implementations.

Jana: plus streams.

Mark: agree.

Martin: there’s going to be a lot of churn in the transport, if we are going down this road.

Mark: please minute “sigh”.

<sigh>

Lars: depending on what cadency we want, 2nd could be bug fixes only.

Ekr: my sense is that we are going to find a ton of things that are so incoherent that you can’t implement them.  We may want to spin an editors copies or -0Nfixup drafts.

Patrick: maybe we should talk about the next milestone draft, rather than next implementation draft.

Mark.  We haven’t been talking about HTTP for example.

Patrick:  I’d like an abstraction for the milestones, so the next milestone might be “data exchanged”.

Mark: you’re losing me.

Patrick: take it offline.

Ekr:  because there may be an arbitrary number of drafts from implementation draft one; so the next milestone should be identified by “2nd milestone” rather than draft number.

Martin Duke: we need to identify what goes in implementation 2.

(Discussion of taxonomy of bugs, features, and implementation).

Mark:  this sounds like roadmap.

Martin Duke:  yes, but as a practical matter, we need to know how we are spending our time for the rest of today, Prague, and on.

Mark:  Let’s make this more concrete. (Makes a milestone, and starts description.)

Jana: We need to know what we are doing with streams going forward, as there is going to be a lot of work around that fundamental construct and the related data structure.  We need to nail that down.

Mark: depends on our cadence.  If we do a bugfix only draft, that might not pull in the new streams work.

Ekr: now I am super confused. Maybe this is a problem of naming.   Patrick is talking about milestones, which map to features.   All drafts that map to a feature set related to that milestone are still the same “implementation draft”.

Lars:  So, our current theory is that naming something an implementation draft is a marker of where to work.  This is proposing an implementation phase, which has a set of drafts in it. Martin:  this is just acknowledging reality.  The point that ekr raised is -04 plus all things that make it work.  Those might be -05, -06, -07.  But new things (streams, recovery) are in a different phase.

Jana:  Let’s talk about that, which is what we want to talk about.  What goes into implementation phase 2?

Mike:  Sending ACKs.

Martin: I’m optimistic about recovery, because it is a single block of pseudo code.

Ian:  there are three options for recovery: everything; timer based only, which is what you need for the handshake;  implement a simple re-ordering based one.

Jana:  Straight up fast retransmit, we’d have to figure out how to separate that out, since the draft currently puts that into one.

Ian: the other things is congestion control, do we care about that for this draft?

Martin: that’s nicely separable.

Ian: maybe punt for the next phase.

MartinT: Let’s not deep dive.

MartinD: We’re trying to asses the amount of work.

Lars: adding congestion control is small, if you are already doing this, because you have parsed everything.

MartinT: flow control?

Martin Duke: that’s a big lift.

MartinT: just mean adding the frames etc., not implement the full controller.

Mark: Does anyone think we will ship the second draft before Prague?

MartinD:  I just want to know what we are trying to talk about for the next 24 hours of meeting time.

MartinT: given the axle-wrapping, we should do a smaller group to identify.

Mark: volunteers: Martin Duke, Ian Swett, Jana, Brian Trammell, Patrick McManus volunteer to draft the second implementation phase.  The theme is “recovery”.  List proposal due in 2 weeks or so, will inform list discussion and Prague/after meeting discussion.

Pace discussion:  still looking at 3 implementation phases per year.

Mark: retake the poll we had on Monday:  still 10, but some are 60% chance of doing it.  10 will attempt, how many will succeed?  Tune in soon!

Mark: do we want to tackle the high order questions?  Timebox discussion of that for 20 minutes.

Lars: echo what we said earlier.  We need to scale out. To rope other people in, or an editor loss will be a big blow.  We need more people to do active things.

Mark: can we identify things that are larger issues about the protocol space.

Jana:  questions about QUIC itself or about the issues they need resolved for their implementations.    Raise them now.

Mark: more of these will surface as we have implementations. Virtuous cycle starts (of concerns?).

One issue is that there are so many issues and you can make all kinds of assumptions, and that needs to get pulled down.  That will solve itself with more timing.

Jana:  people aren’t going to implement just the first implementation draft, but once you go on you immediately hit the stream stuff, etc.

Lars: I would not like the editors to be the ones who are organizing interops; I would like to see another group doing that.  That’s going to be very critical.

Mark: describes h2 experience, which was just “implementors in the room” style, not more structured.  Hackathon is a natural match at the IETFs.  Do it before interims.  Plan for 20 people.

Lucas: It is easier to come to an interim than a full IETF, because those are more expensive and a bigger time commitment. Maybe support remote participation at the interims which are interop-focused.

### Discussion of hackathon mechanics and funding.

Patrick: positive testing tends to happen via email channels.  The interop events are for debugging things that don’t work.

Lars: Experimental room format for Prague?

Mirja and Ekr:  we don’t have that as an option for the next IETF.

Hour and change to go:  hpack clust/verifying migration.  Any other big issues?

We know of DNS and WebRTC being tried over QUIC, are there others?  Suggestions for very quick echo/chargen?  (IPfs is brought forward as something that folks are working on ).  Subodh notes that when they tried that they ran into limitations of echo.  Brian puts out a proposal to define a test suite with a baseline protocol that tests network loads.

Kazuo:  tcp over QUIC?  (initial laughter, but Lucas says that they actually have that running)

Christian: two efforts around DNS now, some of which are feature focused and some are designed to increase ubiquitous availability of DNS.

### Hpack

Mike: Allen has done his simulations of hpack and qcram.  (Reminder: hpack requires in-order delivery, which is not guaranteed unless you are on a single stream.  That creates HOL on that stream. There is also a concern about killing streams,because HPACK can die if you do that).  Buck’s draft takes the existing hpack language, augments the frame and lets you reference a packet only after you know that it is has been received and processed.  That loses you some compression efficiency, but never blocks.  Mike’s departs from hpack by having a single stream for header tables.  It doesn’t have as bad of HOL blocking but you might have a situation when you receive an instruction but can’t process it until you receive the references).

Allen implemented both. Accidentally did hpack draft one in implementation, then simulated both.  Qcram has no HOL unless you have evictions from the table; that can occur if you overflow the table.

Buck describes an issue with the way qcram in its current form interacts with the 2 stream model (push promise streams); there will be a change in the next version to deal with that.

Martin: once you have fate sharing, you can’t cancel any of the streams which are establishing connection level state.

Mike: exactly.

Buck; assuming that we are moving back to one stream, then I’d take it back toward the mechanism in qpack.

Mike: this might be the most important question--whether we go back to a single stream from dual stream.

Martin:  there are cases where this is less than ideal in ordering push promises.

Buck:  there are cases where having the ordering of push promises fulfilled would be a big improvement

Martin: it shouldn’t be the end of the world if they aren’t; you may lose efficiency in that case while it waits for fulfillment.

(Discussion of overhead of data frame headers being included).

Kazuo:  I still prefer to see state changes being on a single stream because it simplifies retransmission.

Mike:  I think in any of these proposals, we will have a single control stream.  The question is whether we have a single stream for all the data.

Jana:  I’m trying to work in my head how this will impact flow control.

Mike: headers were not flow controlled in h2.  We wanted that and split them out, but then we removed the flow control for headers, so we could coalesce.

Jana:  I’m wondering if there is a weird blocking case around flow control.

Mike; you could give header streams very large overhead and higher priority.

Mike: this also raises the question of whether we’ll actually support interleaved push promise.

Alan: this already pretty hard to get right without complex synchronization.

Subodh:  you can make headers have priority for retransmission as well.

Alan describes their push priority theories, with several push promises which still might be interrupted by a chunk of other data.

Mike: servicing push promise as soon as possible would not be a bad alogrithm.

Martin: if the browser isn’t ready, could be a performance hit.

Mike:  We’ve seen perf hit from sending push bodies too early; hard to see why it would hurt to send the promise earlier.

Ian: Buck, you have done some of the work in moving to two streams.  How much work was that.

Buck:  Wasn’t that bad.  On the hpack level though, the http mapping needs the reset reslience if they are using the existing hapack.

Ted:  when will we have an answer to Mike’s question about 1 stream or two.

Mike: don’t know.  We have some desire to stay with two, but it means we don’t have an answer for ordering push promises.

Buck:  that might mean we have to make the ordering a should.

Discussion of how this interacts with the clients requests and send priorities.  They are guidance.

Ted causes a rathole around the DNS use of a similar mechanism.

Alan: is there general agreement that too soon is better than later?

Jana: half and half, as there remain concerns about too earlier.

Mike:  if you do two streams and interleaving, then you still need framing.  If you want to be deliver on a SHOULD for ordering.

Martin:  you can try now, but you can’t guarantee without fate sharing.

Subodh:  if we are re-introducing framing, we should go back to one stream.

Jana: yea, let’s not do two streams and have framing again.  Remind me how this interacts with QPACK?

Mike:  there’s one blessed stream that if you kill it you’ve lost all state, because it is the place where you’re collecting all of the stream.  Qcram was changed to behave like this as well.

Qcram design has an assumption of very tight integration between packetizer and header compressor, Alan notes that this was one of their issues, because they didn’t see an api that made that easy.

Buck: If we move read-write separation into http mapping, we can do both for a while and make a decision based on implementation experience.

Mike: Two versus one?

Buck: yes.

Jana: It sounds like we need to do one stream to

Martin: Ther’s a perfromance cost

Mike: Only way to do without adding new components to the transport.  Don’t really want to do that.

Jana:  I hate push.

(general agreement)

Martin:  If your transport can handle this, it’s flexible enough for other things too.

### Ack Spoofing.

There is a chance when someone introduces random gaps that you may get a problem that you will get spurious acks of things that were never sent.  That’s a particular problem in the case of connection migration.

Proposal is to have a verification/probe frame that replaces this entire mechanism. Jana: that is useful for migration, but don’t see how this helps otherwise. Ian: if you are checking that the peer is honest, then you can do this.  Jana: but what about the regular use of ACKs for the congestion window--if someone is ACKing optimistically or ahead of the packet set sent, you may blow out the congestion window.

Martin: but there are rebinding cases where you are relatively sure you have not changed path, despite needing to probe and validate.  In those cases (port only change, e.g.), then you might return to the old congestion controller with the new signals.

Jana critiques the language, and Ted apologies for the language.

Jana and Martin agree that when you have a new path you need new state, but that you can re-use new state when it is not a path change (only a port change or move within IPv6 privacy addresses).    What we are trying to work through is how to distinguish between clamping during verification and requiring new state.

Ekr points out that Ian’s method actually helps both detect unexpected mobility events where you believe the the endpoint is just opportunistically acking but is not receiving the data (force youtube video to be delivered to starbucks after I leave) and where you are getting at least some of the data (but are blowing out your own congestion window for some reason).  This latter is less interesting attack.

Martin Duke: could you give them an updated source address token?

Martin: yes, but it is an order of magnitude more hassle; you just want them to demonstrate that they received a packet (ping received and demonstration of ping received).

(Ping must reliable for this to work). You may still need an unacknowledged keepalive for other uses.  Jana: with that would we not have to have packet gaps any more?’

Martin Duke: assuming that we are encrypting packet numbers, yes. Otherwise, still need it for client-initiated mobility, to avoid linkage.

Scribing ends at 59 pages.






