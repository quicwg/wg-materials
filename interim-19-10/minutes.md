
# QUIC May 2019 Interim Meeting Minutes

* Chairs: Mark Nottingham, Lars Eggert
* Location: Cupertino, US

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
- [Wednesday Morning](#wednesday-morning)
  - [Agenda bash and arrangements](#agenda-bash-and-arrangements)
  - [Interop Summary](#interop-summary)
  - [Transport and TLS Issues](#transport-and-tls-issues)
    - [Issue 3014: Are we changing Retry?](#issue-3014-are-we-changing-retry)
    - [Issue 2928: Multi-packet CH](#issue-2928-multi-packet-ch)
    - [Issue 2863: Handshake deadlock issue](#issue-2863-handshake-deadlock-issue)
    - [Issue 3067:  PTO gets extended before handshake completion](#issue-3067--pto-gets-extended-before-handshake-completion)
    - [Back to 2863](#back-to-2863)
- [Wednesday Afternoon](#wednesday-afternoon)
  - [Transport and TLS (continued)](#transport-and-tls-continued)
    - [Issue 2602: Idle timeout](#issue-2602-idle-timeout)
    - [Issue 2496: Version Ossification](#issue-2496-version-ossification)
    - [Issue 3091: Require sending ACKs for ack-eliciting](#issue-3091-require-sending-acks-for-ack-eliciting)
    - [Issue 3053: Padding requirements are incorrect](#issue-3053-padding-requirements-are-incorrect)
    - [Issue 2152: Stateless reset being checked after MAC failure](#issue-2152-stateless-reset-being-checked-after-mac-failure)
    - [Issue 3085: Stateless reset should be datagram-based](#issue-3085-stateless-reset-should-be-datagram-based)
    - [Issue 3020: Transport parameter registry changes](#issue-3020-transport-parameter-registry-changes)
    - [Issue 2741: Initial key discard](#issue-2741-initial-key-discard)
    - [Issue 2792: Timing side-channel on key updates](#issue-2792-timing-side-channel-on-key-updates)
    - [Issue 2143: Be conservative about migration](#issue-2143-be-conservative-about-migration)
    - [Issue 2387: Security considerations](#issue-2387-security-considerations)
    - [Issue 3027: Codes for frame encoding errors](#issue-3027-codes-for-frame-encoding-errors)
    - [Issue 3054: Label for key updates](#issue-3054-label-for-key-updates)
    - [Issue 3046](#issue-3046)
  - [Triage](#triage)
    - [Issue 2909: Path migration assumptions](#issue-2909-path-migration-assumptions)
    - [Issue 3100: ACK+PADDING in response to ACK should be illegal](#issue-3100-ackpadding-in-response-to-ack-should-be-illegal)
    - [Issue 3062: Disconnect version number from draft number](#issue-3062-disconnect-version-number-from-draft-number)
    - [Issue 2755: ECN algorithm](#issue-2755-ecn-algorithm)
    - [Issue 2823: Do initial secrets change after retry packets?](#issue-2823-do-initial-secrets-change-after-retry-packets)
    - [Issue 3097: Is CONNECTION_CLOSE really ack eliciting?](#issue-3097-is-connection_close-really-ack-eliciting)
    - [Issue 3095: Backoff of connection close needs to be a MUST](#issue-3095-backoff-of-connection-close-needs-to-be-a-must)
  - [Recovery](#recovery)
    - [Issue 3094: Bursty sends on cwind increase](#issue-3094-bursty-sends-on-cwind-increase)
    - [Issue 3078: Lost server Initial takes too long to retransmit](#issue-3078-lost-server-initial-takes-too-long-to-retransmit)
    - [Issue 2555: Define idle period for CC](#issue-2555-define-idle-period-for-cc)
- [Thursday Morning](#thursday-morning)
  - [Future Planning](#future-planning)
    - [Next Meetings](#next-meetings)
    - [Interims](#interims)
  - [QUIC-LB](#quic-lb)
- [Thursday Afternoon](#thursday-afternoon)
  - [HTTP and QPACK Issues](#http-and-qpack-issues)
    - [Next issue: GOAWAY, see above.](#next-issue-goaway-see-above)
    - [Next issue:  How we deal with SETTINGS](#next-issue--how-we-deal-with-settings)
    - [2797  concurrent requests and initial_max_bidi are not the same?](#2797--concurrent-requests-and-initial_max_bidi-are-not-the-same)
    - [2817. Guidance around how to translate error codes?  If so, should it be normative?](#2817-guidance-around-how-to-translate-error-codes--if-so-should-it-be-normative)
    - [2911 Not have a unified space?](#2911-not-have-a-unified-space)
    - [2963 Doe we need to explicitly state that if the server does not abort reading, the client MUST continue sending the request body even if it sees a response begin?  What about if the response is complete?](#2963-doe-we-need-to-explicitly-state-that-if-the-server-does-not-abort-reading-the-client-must-continue-sending-the-request-body-even-if-it-sees-a-response-begin--what-about-if-the-response-is-complete)
    - [3061 Missing QUIC Version Hints](#3061-missing-quic-version-hints)
    - [QPACK:  Boolean blocked streams setting #3073.](#qpack--boolean-blocked-streams-setting-3073)
  - [HTTP Priorities](#http-priorities)
  - [Key discards](#key-discards)
  - [Jana:  Interop runner.](#jana--interop-runner)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Wednesday Morning

### Agenda bash and arrangements

No objections; agenda posted on GitHub

Need an Apple employee to get back in if you leave the building; restrooms and coffee accessible without leaving the secure area.  Please wear stickers, no photos.

### Interop Summary

Spreadsheet at https://docs.google.com/spreadsheets/d/1D0tW89vOoaScs3IY9RGC0UesWGAwE6xyLk0l4JtvTVg/edit#gid=1510984897

Lots of green, but some things are still not implemented widely (key update, 0-RTT).

Lars:  Interop in Singapore; will there be a new draft before then?  Probably, but minimal changes from -23.  Do we interop on -23 or use -24 with very little lead-up?  Conclusion:  Submit -24 at the cutoff, interop on -24 in Singapore, but no virtual interop beforehand.  Budget time accordingly.

Martin D.:  Can we sunset HTTP/0.9?  I don’t want to fix those bugs.

Ekr:  Want to keep it; easier to troubleshoot.  (+1 from Jana)

Lars:  Clients don’t need to implement; helpful for servers.

Christian:  Minimal HTTP/3 implementation is not horrible, but not small.  Use my code if you need it.  Testing the transport independently is valuable.

Roberto:  Are we suggesting using HTTP/0.9 on the Internet long-term?

Group:  No.

Alan:  Facebook supports HTTP/1.1 over QUIC.

Kazuho:  When we get to v2, might want something other than HTTP that’s simple to use.

Roberto:  Lots of things deferred to v2 are needed for non-HTTP protocols.

### Transport and TLS Issues

Goal:  Come out of meeting with decisions and directions for all open issues.

Ekr:  Let’s defer 2496: Version Number Ossification to a discussion among interested participants.

#### Issue 3014: Are we changing Retry?

Retry packets aren’t protected, but any corruption causes the client to present a broken token and poisons the connection attempt.  Trying to protect them imposes high cost on a DDoS path, exactly where we don’t want it.

Ekr:  Not sympathetic to trying to avoid crypto work; a sender can make you do as much work as they want.  The idea this needs to be essentially free is unconvincing.

Lars:  Redundancy?

David: CRC is cheaper and better understood than any redundancy options.

Tommy:  Let’s just rely on UDP checksums.

Jana:  Optional GMAC you can disable when under load.

Martins:  Which is when you’d send this packet.  Pointless.

Nick:  DoS protection boxes currently keep short-term state instead of doing crypto.

Roberto:  Does this happen often enough that we have to fix it?  What is the user cost vs. the dev/CPU cost?

Jana:  Most v1 deployments will have a TCP backup; the client will probably fail back to TCP instead of reattempting without the corrupted token.

David:  Not clear that UDP checksum will be consistently reliable over the Internet.

Ian:  Worst part, there’s no way to fail quickly so client can immediately retry.  No second Retry packet, no CONNECTION_CLOSE, etc.

Kazuho:  Might be difficult to distinguish corrupt token from too-old NEW_TOKEN token

Christian:  This is another face of early packets not being really encrypted.  Protected handshake draft fixes this, but that’s clearly v2.  Either you protect these packets, or you don’t.  If you don’t, this is where we are.

Why does the bit-flip from server-to-client matter, but not from client-to-server?  Because client will retransmit with the correct token.  Corruption S2C causes the retransmissions to always contain the corrupt token.

Ekr:  Let’s not change the handshake logic.  Cheap checksum is our best path here.

MT:  CRC32 of the packet?

Nick:  Not opposed to a checksum, just don’t want to have encryption.

Kazuho:  I’d prefer GMAC, but mandatory CRC32 is better than optional GMAC.

Ekr, David:  AES-GCM with no key would be comparably cheap, and algorithms we’re already requiring.  Might be better.

David:  The Retry packet currently carries the ODCID.  If we stick that into the AAD, we get the same protection properties without having to send the bytes.

Agreed:  Plaintext packet with a mandatory AES-GCM with zero key and zero nonce functioning as a checksum.  (Entire packet is AAD, no plaintext or ciphertext.)  Author of PR may consider David’s suggestion.  Conveniently, David will author the PR.

#### Issue 2928: Multi-packet CH

Requirement that ClientHello must fit in one packet is a vestige of using HelloRetryRequest for address validation instead of Retry packet.  There are scenarios (post-quantum, resumption with client certs) that lead to ginormous ClientHellos.  Can we consider removing this rule?

David:  Some people are afraid of having to keep the state.  In the current code, I can do this anyway by sending a ClientHello with no keyshares and force a HelloRetryRequest.  This just saves a round trip.

Ekr:  How does this impact amplification?  Can you use this to help servers with big ServerHellos?

(various):  Already can, in several ways.

Martin D.:  We’re changing basic assumptions here; be careful about follow-on breakage.

Kazuho:  HRR already creates those corner-cases.  If you don’t handle it, you’re already broken.  (And to go by interop, several clients were and had to fix it.)

Agreed:  Remove the requirement.

Christian:  Make sure we test this in interop.

Nick:  Can we guarantee that ALPN will be in the first packet, so we can avoid committing state?  We make decisions about whether to commit state based on that.

Ekr:  Not an unreasonable implementation to drop packets that don’t have your desired information and wait for them to be retransmitted.

Christian:  How do I identify the “first” Initial packet?

(various):  CRYPTO frame with offset of zero.  If you depend on the contents of the ClientHello, however, you’re in uncharted waters.


#### Issue 2863: Handshake deadlock issue

We want someone to formally prove that there aren’t handshake deadlocks in whatever we settle on.  How do we make that happen?

Lars:  Talk to academics; I have contacts.

MT:  Conclusion from yesterday was to require that both endpoints send something ack-eliciting in 1-RTT.  That solves the specific issue, but we don’t know that there aren’t others lurking.

MD:  Relies on Ian’s PR; let’s discuss that first, because if we don’t take that then we’re back to the drawing board.

#### Issue 3067:  PTO gets extended before handshake completion

During the handshake, the PTO gets extended any time ack-eliciting data is sent, but packet loss can rely on PTO expiring to recover.  An app at Google hit this.  Solution is to have separate PTO timers per packet number space (i.e. 0-RTT data can’t prevent PTO for Initial).

MT:  Naive implementation of this can send up to six probe packets per PTO interval, which is sub-optimal.  Cap to one probe packet per PTO.

Ian:  Yes, if you’re not coalescing.  We can add text.

If you do this and don’t drop keys until we’ve sent/received something ack-eliciting in 1-RTT, we aren’t aware that deadlocks are still possible.

Agreed:  Ian will update PR 3066.

#### Back to 2863

Handshake deadlocks can occur if one side never sends 1-RTT data after the handshake completes from one side.

Possible solutions:
* Keep handshake keys for LONG periods
* Start a PTO timer in 1-RTT even with no outstanding data
* Require sending an ack-eliciting frame after the handshake is complete (thus arming PTO)
* Handshake “confirmed” once an ACK-eliciting packet is received from the peer

Christian:  3/4 depend on the behavior of the peer.  Prefer not to rely on peer behavior.  Reasonable client might never send 1-RTT data.  Request in 0-RTT, response in 0.5-RTT; ACKs aren’t ACK-eliciting, so the client never needs to send anything.

Ekr:  This is a perfectly reasonable use pattern, and we don’t want to require useless packets.

MD:  You either have to send extra packets or maintain a little extra state.  It’s a beauty contest.

Christian:  Under 4, the server can unilaterally fix the issue by sending a PATH_CHALLENGE.

MS:  Diagram in issue why 4 doesn’t work.  (Discussion)  Concludes that 1/4 vary in the dropped-packet case, but are the same if no packets are lost.

Agreed:  We’re doing 4 unless MS brings new analysis; MD has a PR.

Please read 3099 and 2602; will decide after lunch.

## Wednesday Afternoon

### Transport and TLS (continued)

#### Issue 2602: Idle timeout

Both peers declare an idle timeout value. Does the connection die at the minimum of those two values? What happens when that time is reached? What should do when that time is reached?

Each side can do it unilaterally, and should explicitly close before if it is before its advertised timeout. 

Or peers that expect the other side to have closed should not keep sending after that time.

Ekr: What are we trying to accomplish with this at all?

Alan: Silent closing is cheaper than waking up the radio again

Roberto: Reduce the L2s throughout the network, as well as the RTTs. You’re otherwise wasting the RTT.

Ekr: I agree with both those statements, and so the purpose of the mechanism should be to tell the other side to not bother after that time.

Lars: In London, we agreed to have a PR to do the min, which Ian made. (The PR was made just today)

MT: I can live with that based on the current formulation

Alan: Excited that he convinced MT of something =)

MT: Min makes a lot of sense if there is a high probability that the peer won’t be there at all to respond. It then makes more sense to make a new connection.

Roberto: The min implies a race that’s hard to resolve, so I don’t like it. Prefer it to be asymmetric.

Jana: The point of the min is to reconcile cases in which the idle timeouts are vastly different

Roberto: But what if I’m the one who advertised the smaller time, and I’m still around, can’t I use the longer time.

Jana: You are committing for being around for at least as long as you advertise.

Roberto: The server pays a very small cost for being around, but a cellular client has a higher price to pay.

Alan: If the client wants to be around longer, it should have a longer idle timeout

Roberto: Then you need more slots in the cellular bandwidth

Alan: So if client says 1 minute, and server says 5, the server cannot send anything to the client after 1 minute

Ryan: So the server just accumulates data for 4 minutes?

Kazuho: I prefer min from a concern about the API telling the server that it can’t actually send for four minutes, which is hard to do

Jana: I assume most people will do it as a min

Roberto: Kazuho’s point is super important; it’s too hard to expose

Jana: Have some feedback on the PR, but we can go back on forth on that.

Martin: We do need to fix the PR.

Mirja: As a note on the API, exposing if something can be sent isn’t technically needed if the API layer (like HTTP/3) could choose to reuse an old connection, or else start a new connection.

Alan: That wouldn’t work for servers though

Mike: If keepalives are delegated to the application, the application needs to know what cadence to use for keepalives. Depends on the implementation.

Ryan: We can change it to declaring a max idle timeout on each side, and then the actual idle timeout is based on interpreting those transport parameters.

Jana: Got it, that makes sense

#### Issue 2496: Version Ossification

Lunch discussion. 

MT: Go ahead with proposal to provide extra incentive by coupling to the use of tokens, or session ticket; if you send a new token frame it carries the information. Creates an incentive to use the scheme rather than ignore it.

Work with Martin’s PR (2573) (ekr will massage the PR), and then take additional input from Kazuho (which will be written up as a separate issue)

Ekr: Will need a long discussion about what relevant threats are considered and addressed.

MD: It is optional for the server and client, right?

MT: That’s where we are now, but Kazuho has some ideas to tweak that

Ekr: This mechanism will be far more effective the more servers add support for this. Having this in alt-svc increases the likelihood.

See the project board.

#### Issue 3091: Require sending ACKs for ack-eliciting

Seems like it may be quasi-editorial; there isn’t a normative statement, and the proposal is that this should become a MUST.

Agreement from MT and ekr.

#### Issue 3053: Padding requirements are incorrect

Kazuho: Only initials specify that they need to padded; but this doesn’t technically include 0-RTT.

Mike: Ends up just being editorial, just remove the word “only”.

#### Issue 2152: Stateless reset being checked after MAC failure
#### Issue 3085: Stateless reset should be datagram-based

This is asking about the order of operations; we don’t need specify the current order of checking. MT has modified the text to say the checks are independent. If it fails decryption, you do need to check for stateless reset.

You should check datagrams for resets, not packets technically. If you receive a valid packet in the datagram, you can stop looking for stateless resets.

Would like to merge the PR. PR should be ready. Comments should go into consensus call.

####Issue 2944: Layout of PreferredAddress

Trying to put all the fixed length fields first. Many think it’s a minor improvement, but not major.

David says he could change the order if they change the format of the transport parameters anyhow. Will ask to close on consensus, but may take opportunistically if we take #3020.

#### Issue 3020: Transport parameter registry changes

Two related issues:

David wants to innovate in the transport space. The main joint for changing is transport parameters. This space is 16 bit and the experimental region is only eight bits, which can lead to collision in experiments. 

TLS presentation language is confusing and unnecessary, since we have our own format for everything else.

PR makes the length a varint and restates TPs in QUIC packet style.

Lars: Could also make it 32 bits.

Matt: With common code between TLS and QUIC, would be harder to parse this as varint for us.

Roberto: a new version is a way out. Make the space smaller!

Kazuho: This proposal has two changes: the flexibility of the parameter IDs, and the length. Our TLS implementation exposes a way to parse the struct. It’s easier to parse the length as fixed 16 bits, but ID can be varint.

Victor: The reserved experimental space never works (see “x-” headers). Why would people migrate? I have an objection to the issue in that regard.

Mike: I agree with the statement, but I’m not sure what to do with it. Should the experiment region be small? Or none at all?

Victor: I was asking for none at all.

MS: I’m in favor of this change; the TLS presentation language is hard to parse, and many people had to ask how to implement it. Getting rid of this last bit of TLS presentation would help. Also the transport parameters are in the clear, so moving to a QUIC-specific format would allow us to reduce fingerprinting by changing the ordering.

Ekr: Starting with philosophy first here, there seems to be a desire for a larger space from David; and smaller from Roberto. Then, if we want to make it bigger, how would we do that? If you use varints, there’s a benefit to having low values that are standardized.

Mnot: I agree that there’s a benefit to expressing the philosophy behind this. If we make this larger, then it will seem like a more global space.

Ekr: People often do pairwise experimentation by sending an extension everywhere.

Tommy: We don’t love that transport parameters aren’t encrypted; let’s not necessarily make this space bigger to incentivize more options prior to a QUICv2 in which we have better encryption here.

Jana: The people who will run out of space will be the ones that don’t have a large deployment

Lars: It would be good to encourage that people choose high numbers, and not just choose the next integer a la TCP.

Mirja: But TCP uses RFC required, not spec required

MT: We are currently using the same advice as TLS

Ekr: This fixed the need for RFCs, but didn’t make experiments super easy

Roberto: Are experiments long-lived or short-lived? If you only do them at small scale, it doesn’t matter

MT: I don’t like the carve-out for experimentation. Have a spec required for permanent registration. For small experiments, just get a very easy allocation.

Mnot: I like that

MT: I’d like to propose that model for all of the registries we have in QUIC. Will file an issue for provisional registrations.

Victor: The implication of private use is that you can use it for short-term experiments.

Mirja: You only need one (or a few) numbers for that

Jana: The issue we’re discussing is predicated on the idea that the range is too small. But this PR allows for almost 2^16 specified numbers. Even 256 transport parameters is too many. Do the opposite carve-out. (i.e. 256 reserved for standards, everything else is for extensions)

Roberto: To expand, I *do* like innovation. I think that one way or another, you want to compute a unique integer for you unique experiment. One way to say this that the QUIC version mod 256 + the transport parameters number becomes the namespace for the experimental transport parameter region.

Ekr: I think we’re talking now about just changing the registry allocation balance, not changing the wire encoding.

Eric K: If we need more, we can use versions to increment the space. Invert the allocation between specified and experimental, and don’t change the wire.

David: We can’t easily use the version number here; if we want to pairwise experiments with both YouTube and Facebook, we can’t use both experiment spaces. I want the freedom to mix and match. Flipping the space does help, and is better than what we have today. But the encoding is still an interesting conversation.

Victor: Regarding provisional registration, how do we actually revoke them?

MT: The general policy is that they are kept until they get reclaimed when an experiment is over.

Mirja: If you try to reclaim it, you find out if it is used or not anyhow

MT: The point is to know what space is reserved for the short-lived items.

Victor: I’m okay with the current encoding

Mirja: Even if you don’t change the on-the-wire format, we don’t need to use the TLS presentation language in the document. If everyone will move to v2, I’d prefer to make the parameter space smaller.

Mnot: I don’t see anyone really caring about changing the size of the space, it’s more about registry policy.

MT: I’d like to see a PR for changing how the space is described in non-TLS-presentation format.

Jana: So the proposal is just draw a diagram to not use TLS presentation format; and then separately flipping the allocation of the spec required and experimental space.

Using 3020 to track changing the space allocation. Separate PR for editorial change.

#### Issue 2741: Initial key discard

Ekr agreeing to close with no action if we fix 2863.

#### Issue 2792: Timing side-channel on key updates

There’s a PR from MT. The PR suggests one way to close the timing attack. It’s a “SHOULD but we know you won’t do it”... if you follow the advice, it would be good, but people may not do this. It’s not that interesting of an attack to solve.

PR needs more eyeballs. Do a consensus call on it.

Ekr: I did have one outstanding comment

MT: We’re just adding QUIC KU to the end of the TLS 1.3 label used for key updates.

#### Issue 2143: Be conservative about migration

Eric K has PR out for this issue (2925). Added text for threat model. The one thing we haven’t addressed is if we agree with the technical conclusions that were made. We should check with the room. There are TBDs that are ekr’s problem once this is done.

Ekr: I think it is okay based on the look I took. Reflects what we’re trying to achieve.

Eric: The intention is to leave the TBDs in.

Needs Gorry to review.

#### Issue 2387: Security considerations

Ekr will do after 2143 is closed

#### Issue 3027: Codes for frame encoding errors

Adding principles for how to send a frame encoding error. If the frame decoder detects an error in parsing a max stream frame, it could give either error (frame encoding or bad max stream).

Can we call this editorial?

Mike: Can it be implementation choice?

MT: That’s the PR from MS

Mnot: No pushback, just call consensus


#### Issue 3054: Label for key updates

Referenced in 2792 minutes. We are just using what TLS does, “TLS 1.3 QUIC BLAH”. Everyone seems okay with this.

PR in 3050


#### Issue 3046

Kazuho will work on the PR

### Triage

#### Issue 2909: Path migration assumptions

Jana: We’ve addressed some of these already; mostly editorial.

MT: If Jana finds anything that’s not editorial, we should open a new issue for that.

Eric: When the comment was written, there were a few things on the list to change. Can sit with jana to work on this.

EDITORIAL

#### Issue 3100: ACK+PADDING in response to ACK should be illegal

Should be editorial, just say what we meant

#### Issue 3062: Disconnect version number from draft number

David: Reason the issue exists is to talk about it here; discussed back in January. Want to avoid the issue in which different drafts have different numbers, but the same wireformat. That seems like a silly issue.

Mnot: Same thing in H2. Only certain drafts got marked for implementation. We can address this just by changing our process for documentation.

David: That’s fine for me

#### Issue 2755: ECN algorithm

Lots of text for specific cases, but not fully specified for the edge cases. Should have an exemplar algorithm for the state machine. Will move if find needed changes.

#### Issue 2823: Do initial secrets change after retry packets?

In practice, everyone does. But not changing them is better.

This should be a DESIGN issue that is discussed.

Kazuho: My concern is that the client would no longer be doing a key operation, which makes the client do less work on retry.

MT: I don’t think that’s how we want to ensure that the client does work. A few SHA256 operations isn’t much.

Kazuho: The other possible issue is if the token is corrupted

Ian: I am leaning towards doing option (2), can make a PR for that

MT: I don’t think we can do (2), it breaks the security guarantees for key derivation

MT: Want to take Ian’s existing PR

MS: Why are we changing anything at all here?

Ian: When we wrote this, we didn’t realize it had the side effect of not allowing connection close.

MS: Proposed action would be to make this clearer/editorial, but not make a wire-format action.

Will do consensus call here (option 3, no change to implementation, but add editorial)

#### Issue 3097: Is CONNECTION_CLOSE really ack eliciting?

Jana: I don’t think it’s technically editorial, but we may have meant it

MT: I don’t think we thought about it

Design + proposal ready

#### Issue 3095: Backoff of connection close needs to be a MUST

If there is no backoff, there could be an attack that causes closes to bounce between two servers that receive error packets, and they are directed at one another.

DESIGN issue

Finished triage!

We have 10 issues that need PRs, please work on those

32 editorial issues beyond that.

### Recovery

#### Issue 3094: Bursty sends on cwind increase

MT: Can bursts of acks cause a cascading problem?

Victor: Doesn’t pacing solve this?

Jana: Not everyone will necessarily pace. Many TCP implementations don’t have any pacing, but have other mechanisms to control the burst size. You can’t eliminate them, but you can help.

Vidhi: For TCP, we can do ABC, etc. Suggestion is to max the burst to 1-MSS per RTT when in slow start, etc.

Ian: How can you increase the congestion window by more than 1 MSS anyhow?

Vidhi: An ACK could contain more than one congestion window

Ian: With the exception of PTO you can’t have more than the MSS outstanding

Jana: You can’t increase by more than once cwnd, but that can happen with a single ACK. The window can double in a single ack during slow start.

Jana: I agree with Ian that during congestion avoidance this can’t grow too much.

Ian: Is there anything about this that’s worse than TCP?

Christian: What we have is something that’s been tested on TCP for many years.

Jana: No, Reno is fine. It is old, but holds up well. Linux does more for burst avoidance, but we don’t go into that (because we say please pace). It may make sense to have a few safeties for people who don’t do pacing.

Roberto: Failing to do pacing harms the application by not using the link effectively

Jana: My proposal is to limit the number of packets acked per ack

Ryan: Can’t we just say to always use pacing?

Mirja: It’s as simple as saying don’t send more than 3 packets at a time anyhow, which pacing complies with, but works generically too.

Victor: I don’t think this is solvable without pacing. The only input you have is the ack clock. You can start by only sending three packets, which underutilizes the connection.

Mirja: To Ryan’s point, I assume you ack more often than every 100 packets, but if you are not sending loosely, you’ll catch up

Jana: I don’t think we should get into a discussion of pacing being required or not. I am in favor of pacing as the simplest solution. But TCP has these protections. We should have protections too.

Vidhi: Either we don’t increase the window for non-pacing implementations, or we don’t send.

Roberto: I haven’t found that burst is defined in a single way.

MD/Lars: We’re supposed to do what TCP does

Lars: Sounds like this may be something that TCP does that we’re missing

David: It feels like we’re in a CC rabbit hole… it might be nice to table this until Jana has a proposal written as the editor.

Eric: We have to think about this eventually. In terms of concrete things, this isn’t an issue if you don’t do pacing. We can add text to say what to do if you don’t do pacing, and then we’d be done.

Christian:  We’re chartered to use TCP standards, and this is Experimental.  We can’t require it.  Recommend mitigating if you don’t pace, and point to the TCP ABC RFC as one possible mitigation.

Jana: offering to Vidhi to work on this, but happy to work on it myself.

#### Issue 3078: Lost server Initial takes too long to retransmit

Wanting to avoid 1 second delay in case of a particular loss. A few different directions to go with this. Either something more complicated, or document optimizations implementations can do. 

Ekr: People are sad about how hard it is to set this timer in DTLS

Ian: Multi-packets actually can make this particular case better. (Different from DTLS)

Mike: Should we start looking at empty ack again?

MD: Is this only in handshake packets? (yes)

David: How do you know that the server initial got lost?

Ekr: You get handshake packets that you can’t decrypt as the client, and you’re stuck on the retransmit timer

David: If you think you’re in this case, can you just retransmit the client initial?

Nick: That was my suggestion

MD: That’s better than an empty ACK

This is covered by 3080 mainly, Ian will update


#### Issue 2555: Define idle period for CC

Roberto: Should define things as a MIN(10, current congestion window).

MT: It says you either pace or *reduce* your window to 10. Which is correct.

Ian: Not sure what else needs to be added to resolve the issue.

Lars: Will punt back to Praveen to see if it’s now closed based on 2675.


Lars: Is the recovery draft ready to move into the late stage processing?

Ian: I think that would be fine

MT: After the next draft, no reason not to.

Eric: I had said we shouldn’t before, now think we should.

## Thursday Morning

Scribe: Sean Turner

### Future Planning

There is a plan for all the remaining TLS and Transport issues. 

Recovery draft in late stage processing.

HTTP discussion will happen today.

Issues deluge will pass.

Completely conceivable that we go go to WGLC.

1 Month WGLC - Delay of like 6 months.

Lars: Shouldn’t delay v2 charter discussions.

Roberto: Should do other bindings here.

Tommy: When we move something to WGLC people will start people implementing.

Christian: One of the reasons to WGLC, is that other WGs will be base their work on QUIC.

David: When can we work on QUIC-related work.  Don’t want to wait until QUIC RFC is published.

Mirja: Early next year would open the flood gates.

Lars: The earlier you go the more risks there are.

Sean: Need to consider researchers too.

ekr: We are behind where were with TLS.  18months out.  It looks like most of the extensions people are talking about are based on stable QUIC concepts.  It would be reasonably safe to begin that work.  We shouldn’t run head long at the RFC because we should be shooting for better not faster.

Mirja: not all of the QUIC extensions might go in the QUIC WG.

Roberto: The pressure here is that we deploying things that would prefer be QUIC.  By not talking about it in the venue we’re harming v2.

Jana: So… I support the idea of not waiting until the RFC # is applied.  WGLC seems to be a good time when new work should show up.  It’s better to have the work start in the IETF because it will result in less friction and protocols get developed.  Can we divy up the suggested changes into editorial and technical.

Victor: The last real change to the protocol was 2 years ago. 

Mnot: WGLC sooner rather than later is what is wanted.  Not planning on shipping it directly to IETF after that.  After the WGLC, we could start work on extensions, etc.

Lars: We could do one sooner that would basically end adding new design issues.

Mirja: Editorial issues can crush you.

ekr: WGLC is not quite where we are because the doc is not done.

Kazu: In draft -24 we expected that a pre-WGLC state?  Does that -24 is blocked to make changes.

Mike: Should we have WG consensus to open a new design issue.

Roberto: There’s a different v2 that is different and it fixes v1.

Lars: Having v1.1 doing bug fixes.

David: The failure mode is that for some reason it does not work quite as well as TLS.  Users complain and go to the CDN to untick http3.

ekr: our process requires some level of support for something to be a design issue.

#### Next Meetings

MT: we should start having the extension requests

Ekr: Good for the participants to know the rules they are operating under.

Mnot: give time for LB and other extensions in singapore.

Ekr: it’s not premature to adopt datagram or Load Balancers.

Mnot: we need to make sure our charter is good to go.

#### Interims

1st week of Feb …. Asia Pacific or Europe.  Will know more in a week or two.


### QUIC-LB

Martin Duke

Slides

Shooting for WG adoption in Singapore so please read!

ekr: the transport doc has somer requirements about CID

MT: cleartext option seems like a no

ekr: are you suggesting weakening requirement

MD: would have to look if we adopted the cleartext option.  A server mapping is no strictly linkable.

Mike Bishop: Text is about why you might not want to be linkable.  It’s not normative.

Kazuho: My personal view is that sending the server ID in the cleartext does not violate the transport draft.

Ted: Are LB and server a compound service? Then that might be correct.  May need to explicit about which deployment model gives what properties.

MD: The trust model here is a bit different because it’s on your silica.

Jana: It’s useful to think about different trust models.

Christian: What concerns me is that there are three options: no communications between LB and servers, some synchronization of keys and then you need to share key IDs, [garbled-garbled].  And, I think we should just stick to those three models.

MT: There’s not really a probably with having more than one option documented.  We just need to make sure they are good options.

MD: Draft has become kind of a catching ground.  Might need two drafts.

Roberto: There is a different linkability model for client-MB and MB-server.

Subodh: One could come up with a solution that provides more power to client but then it can DoS you.

Mirja: How do you see the relationship to management draft?  Just reference it.

Mirja: Should it be in STDs track?

MD: L4 would advertise support for these protocols.  Hence this should be STDs.

MT: Why make a new protocol?

MD: Not married to new protocol, but liked in looking QUIC-like.  Would make it through.

Kazuo: Instead of protocol can’t we just say this is an URI and then use HTTP.

Lars: Provide feedback about what should go.

Mike Bishop: This isn’t for the Internet, but for the datacenter.  Do we have precedent to do this?

Lars: Yes, lots of management protocols in the IETF that aren’t meant for the open Internet.

Jana: Already the mechanism between the middle box and servers may need to be reused.

Roberto: What I do not see in the draft is tunneling. I.e. QUIC over QUIC.

MT: That was explicitly ruled out of scope.

MD: There’s no MTI on regular QUIC implementations.


## Thursday Afternoon

Scribe: Ted Hardie

### HTTP and QPACK Issues

See the http issues list and qpack issues list.

GOAWAY slide deck: https://github.com/quicwg/wg-materials/blob/master/interim-19-10/H3%20Goaway.pdf

Alan:  Two sub-issues: do clients need to send a GOAWAY; if so, what goes into it?  In particular, what do you do with indefinite/infinite resources?  Do they need an explicit signal? Slide 2 is an example from Facebook.  On this slide, if the uplink is H3, it no longer works as it did in H2.  It can be done less gracefully (close the connection) or with less clarity (taking push credit away).  

MT:  The credit for pushes might end up holding this up.

Roberto:  The single push might be indefinite (example of iFrames in specific video encoding; it would be useful to terminate graceful).

Alan:  We removed this from H2 and we should put it back (Humm now) (Laughter at preemptive close).

MT:  I was originally unconvinced because you had coupled them together.  I didn’t like that entanglement.  But I can see the use case for having a clear signal for “clean everything up”.  

MB: I am a little skeptical because the infinite series of push things isn’t a function of HTTP itself, but in terms of wire capabilities, having explicit signals is better.  I can see the need for a capability.  

Roberto:  I am saying that even if you eliminate the proxy from this example, this is pretty annoying.  The client can’t know when to cut this off.

Roy:  Is this GOAWAY all streams?  Are we assuming that there is only one client per origin connection (No, it is per connection no matter how you model the clients).

Section 2:  What belongs in a client-initiated GOAWAY?  Logically  a server’s GOAWAY revokes stream “request” credits (equivalent to a stream close on all of the stream IDs relevant to the GOAWAY).  Now discussion of what could be in that ID--Nothing, Unidirection Stream ID, Psh ID, Bidirectional and Unidirectional Stream ID.

MT: Unidirectional streams are not exclusively used for push, so you don’t know how many you’re going to get is, say 10.

MB:  This in the other direction to indicate what it can safely retry.  The server doesn’t have to care what it has pushed successfully in the client case.

Jana: Doesn’t cover BiDi and Push ID.

Alan walks through the options.

Slide 4: Nothing

(still a semantic change from H2)

Slide 5:  Server initiated Unidirectional Stream ID

Any new unidirectional streams would be rejected.

MT: You don’t get any certainty about what the streams were used for (pushes or something else).

Slide 6: Push ID (new PUSH_PROMISE or push stream with a higher ID would be cancelled)

Symmetric parsing, close to H2 semantics.  Cons:  extensions defining new unidirectional stream types must define new GOAWAY.

MT:  You had a proposal that had symmetry here, right?

Alan: Yes, we had a draft proposing a fully symmetric relationship (Servers can request from clients), and that was one of the original drivers.

Kaz:  You’d need a separate signalling mechanism for graceful shutdown of the extension.

Push already has a load of frames, why not make this a frame like “no more pushes”.  

Alan: there could be two distinguished types of action: “drain this” and “stop pushing”.  Maybe getting them disentangled would help.

Jana: what about the server side?

Alan:  this would not change the server side.

Nick and Ryan discuss the semantics of whether this continues to mean “drain” or “stop pushing”.  

MT: Pushes may get dropped and there is potential waste, but no other issue.  How much weight you put on the “stop sending” side versus the correctness e.g. can I try again?

Alan:  Option 3:  the advantage here is that it is close to H2, so it is easy to reason about.

MD:  As someone building a proxy, the fewer semantic changes in a translation between h2 and h3, the better.

MB:  The most compelling piece here is that in H2 is that the server gets the message that you must stop pushing now.  Prefers 1, could take 3.

Alan: but option 4!  If we were putting GOAWAY in the transport now, this is how it would work.  It provides some functionality that might be leveraged by extensions.  Not entirely clear, as there might be variability there, but it gives you something to work off.    Semantics include some states we don’t have states that make sense in H3.

Roy:  How about using special terms like Stream 0 to mean stop pushing?

Kaz, Alan:  the H2 draft uses max for that.

MT:  I prefer 1, but I could live with 3.  

Alan: 2 and 4 seem to be out.  The difference is how parallel this is to H2:  Fight!

Ryan: I would receive the stop pushing after 

Lucas: It’s not that easy to do the mapping between HTTP/2 and HTTP/3, because the stream IDs still need to be managed on both sides.

Subodh:  walks through sending MAX_ID first, then going to a specific stream ID, and concludes that option 1.

MT: Next question is whether this needs a new frame type or can re-use the existing frame type.

Kaz:  What happens to requests in flight?

MT: Graceful drain, so it finishes what is in flight or, if it is an infinite stream, it ends at a graceful moment.  

Mnot:  I would be more comfortable if there was an explicit relationship of the intended semantics that could be surfaced to the application

MT: We have a relevant error code here, at the transport layer.

MNOT:  We should have a signal that this is an infinite resource

MB: HTTP layer rather /2 or /3.

MB:  The server here must not send new push streams, but you can’t enforce them.  If you don’t send a push ID, then it is up to the server to decide what graceful looks like.  If you include a number, then the semantics are a bit more clear.  The server can stop sending bytes on pushes higher than the provided stream ID.  The server’s connection gets a bit more efficient.  

MT: Gives an example based on video stream segments (each a second long).  

Roberto: gives a GOAWAY Max example semantic.  

Ted: Question on how that works between GOAWAY Max and infinite resources, when the client doesn’t know it is an infinite resource.

Ryan:  That’s true, but not distinguishing between GOAWAY Max and other conditions, because you have that same problem with GET-based resources.

Alan:  I hear Option 3, with a PR.

MT: After the conversation, I’m not happy with that.  I want to continue the conversation on whether this really closes pushing.  I’m not comfortable we’ve resolved that.

Alan:  I will write an explicit PR on what the push Id means in that context, and we can then argue on the PR.  

MT: Okay, that works.  I would like to understand what the pushID means here and how different it is from the other context.  

MB:  Updated the issue to reflect the progress made.   

MB: Change to H3 Slides

https://github.com/quicwg/wg-materials/blob/master/interim-19-10/HTTP-issues.pdf

MB: Old and Moldy issues: #253 and #2223, punted to http-core/#237.  What we need to state somewhere is how I take and HTTP URI and how that gets mapped to a TCP and UDP endpoint. 

Mnot:  currently spread across many specs.

Roy: this is assigned to me already for -core

Mb:  I will point to your text when it is done.  We agreed that you should be able to use https URI and go straight to QUIC.  

Roy: What we are doing in core is removing the things that would stop you from doing it, we’re not telling you how to decide to try it.  ALT-SVC being one way to get there.  Other methods may be available.

MB:  Do we keep the DNS check?

Mnot: that’s a can of worms.

Ekr:  HTTP2 doesn’t have an ALT-SVC issue, but it does have rules about what you can send down an origin once you have a TLS connection.  

MT: The core documents only define what is possible, not necessarily how to do it in all other ways.

Mnot: we need to have some list of what you might do.

Ekr:  Why would it not be fine, given the URI, to attempt QUIC?  You’d have the same properties as HTTP/2.  There is an authority vs. origin issue here (whether or not ports change the origin).  

Roy has the token to update the documents such that a client seeing an HTTPS URI can test both the TCP and UDP ports (either decorating the authority or the default ports) to see whether the HTTPS authority can be mapped to a QUIC connection.

MT:  We might have done this wrong in H2, since we didn’t have core; we’ll have a bit less here than what h2 said, since we’ll be able to rely on core.

#### Next issue: GOAWAY, see above.

#### Next issue:  How we deal with SETTINGS

This is a very weird frame, with a lot of special rules.  Maybe this shouldn’t be a frame, but should be some other type of blob.  One proposal is the header to the control stream.  This is functionally equivalent to what we have now; there are some errors that drop away (what happens when you re-send the frame, which is not permitted).  The other  is moving settings to transport parameters.  

Kaz:  I have a question about one of the pro’s “removes race conditions around coalesced packets”.  Is there a reason to store the token separately from the other two, or it is good practice to store it in the same place?

MT:  I believe that we agreed yesterday that we should store them in the same place.  We store anything critical to the context together, since the loss of any of it kills you.  We want to narrow down things to origin/local storage.

Kaz:  these are used once and thrown away.  So storing them together means that there isn’t a race condition.

MB:  The code problem is that if you receive the session ticket before the token, can you store it before you get the other?  This clarifies that race conditions.

Nick:  Still can get some issues when settings are still awaiting--you need all three in that store to take the optimization.

MT: All three are optimizations.  If the client chooses to remember settings, it doesn’t have to use the defaults while it was waiting on Server to send settings.  It’s great, but just an optimization, as are the other two.  That’s why the race condition is not that significant.

Ryan: Implication doesn’t have a true MUST here, because it can always restore by getting new settings.

Alan: Will this be aped by other protocols here?

MT:  Other protocols may not have the same privacy properties, so it may not be as safe.

Ted: Strongly agree with MT, it may be very different in other protocols.

David:  The advantage of this is that you get these settings for things like QPACK very early, and then you can avoid having to wait for settings.

Ryan:  We might treat this like 0-RTT, which is sharp enough that each protocol has to work out whether it can do that after an analysis.

MT:  I am concerned that other people will simply excuse their choice based on whatever the logic is here, even if it doesn’t match their actual set of privacy risks.

(nodding).

Ekr:   The issue in doing this server-to-client is much less privacy concerning, but then you have asymmetry.

(discussion of the disadvantages of asymmetry).

Alan asks about putting this in 0.5RTT data.  Nick notes that this would work for some cases, but it will not in 100%.

MD:  Why is this not a TLS Extension?

Ekr:  Same thing, different spelling; we need to get this semantically correct, then worry about whether it is in which TLS message.

Alan: If you want HoL blocking why not just do that at the application layer?

Ekr:  Yes, you can that; this is just a default.

MB: The chrome data is that settings is not arriving early.

MT:  People are not doing 0.5 RTT data yet.  It will get better.

David:  This can still fail; we still have ways this can fail.  Moving this makes it not fail.

Roberto:  There is more than one way for things to fail, and one can be a difficult plumbing--this is dropping 2 layers down.

Ted: ranted for a bit about privacy properties.

Kaz: The ideal solution is an encrypted extension in TLS, which eliminates the privacy issue but still means that this is prior to the application layer.

Ekr:  This sounds workable. Like a type-B extension like in dkg’s proposal.  This means that this would be a head of line blocker.   

David: That’s big door, and I think it is QUIC v2 work.

MD:  Agreed.

So the question is what we do now, if anything.

Nick: In some future TLS work, an encrypted extension would be ideal, either just client to server or bi-directional.  In the mean time, we can put server to client right now.  MT’s objection there is really just that server to client is not worth doing.  Roberto: server to client we can get that done without disadvantaging any later protocol.  Client to server, we seem much less capable of getting that right.   

Lucas:  If we didn’t use TPs, do we default back to a frame, or can we consider control stream?  

MB:  That’s also a valid design.  It’s a slight improvement with a slight increasing complexity.  It eliminates a class of errors.

Kaz: I doubt the improvement for the client in the 0-RTT cases.

David:  that depends on the implementation.

Action items:  future request to TLS that we would like to have this feature. (Ekr:  this was in TLS 1.3 until very late, we took it out because we didn’t have a driver for  it.  It can go back in fairly simply).

Closed with a QUICv2 tag.

On to HTTP/2 comparison.  

#### 2797  concurrent requests and initial_max_bidi are not the same?

PR available.

#### 2817. Guidance around how to translate error codes?  If so, should it be normative?  

Guidance seems desired, but normative language does not seem to be required.  

#### 2911 Not have a unified space?  

Keep unified space.

#### 2963 Doe we need to explicitly state that if the server does not abort reading, the client MUST continue sending the request body even if it sees a response begin?  What about if the response is complete?  

Mnot: will be clarified in core, and either point to that or rely on that?

Mike to raise an issue in core if there isn’t already one; this issue to track pointing at that.

#### 3061 Missing QUIC Version Hints

Ryan:  we do this now by advertising a tuple.

Mnot:  My preference is that HTTP3 is a binding to a specific QUIC version (not changed is the binding to QUIC does not change).  

MD:  This issue is kind of premature, as we’re going to see this blow up.

Ryan: But these are all expressed within the ALPN token.

Lucas: A question came up in #3063,  and I’d be happy to get rid of it, but I’d like to know who would be sad.

Ryan:  We used to use it, but we don’t need it now that we use ALPN.

Ekr:  This could result in silly states, if they negotiate things and then use a lower QUIC version (H3/Q2 negotiated but run over Q1--not defined)

Roberto:  They could leave the field blank and talk shit to each other as well

(laughter).

Discussion of how to order negotiation and what the document should says.

MB: points out issue 12 dealt with this, and we’re overturning that.

Ekr:  I’m starting to get a little concerned about this>

Mnot: Let’s get a real PR on this and go from there.

(Discussion of what “H3” means in this context, and how bad it is)

David lays out a couple of ways to go forward, and everyone agrees to punt it down the road.

He will write a PR deleting a section.

#### QPACK:  Boolean blocked streams setting #3073.  

Alan:  The decoder says you may risk HoL block on N streams.  Bence has suggested that this be changed back from a number to a boolean (May block on all or may not block).  

Alan: proposal that we keep this as it is and close the issue.

Ryan:  How can you be happy having this number of streams and not stream ids and headers?

MB: This caps the h3 processing in favor of quic processing.

Alan: the complexity of the current method is not back.

Victor: This is effectively flow control for block streams?  How do you deal with the peers not be in synch about which are blocked?

MT: The instruction is a risk tolerance; you say “up to 100”, but there is a chance that none block.  At the dedocer side of things, if you haven’t gotten all the necessary insertions, you put it in the queue; if you go over the queue size, you generate an error.  

Ian:  looking at the code for this, it is fairly complex.

Alan:  If the encoder is conservator, it gets less complex.

### HTTP Priorities

Ian

https://github.com/quicwg/wg-materials/blob/master/interim-19-10/HTTP%20Priorities%20Update.pdf

Some data from Chrome/Google.  Compared SPDY/H2 priorities, Round Robin, FIFO, LIFO.  See experimental results on slide 2. (LIFO is by stream ID)

What we believe we know:  N priorities + 1 bit works well both in simulation and practice.  

Christian:  Do you have any insight into the relationship with head of queue buffering?  Parallel send vs. priorities

MT: Basically no, we have no data.

MB:  If you have only one thing in flight in time, there is no advantage to QUIC’s ability to not fate-share between streams.

Jana:  Want to draw a parallel to OS scheduling.  If the server has knowledge of what the resources its sending out, can it use “shortest job first”?  

Ryan, the difference between this an OS scheduling is that the client can have knowledge of which one is most important; not commonly the case in OS.  

Roberto--there are many different schemes we could come up with; this is good enough and not hard.  Can we agree to this, and explore the others later?

(Some thumbs-up).

Areas of consensus 

Ian: we do need a negotiation mechanism, whether it is the existing draft or not, we need something. Focus on web page and VOD streaming, as the live streaming case may turning out to be different.

Roberto:  the reason we might want to consider is that we are explicitly not addressing Live streaming.

Emerging consensus: Header, based on draft-kazuho-httpbis-priority

Priority  = urgency = 3, progressive=?1 is an example syntax.

Lucas:  this is an exact duplicate representation frame of the original header 

Ian: copy paste error on my part.

Mnot: Roy and I were talking and we came to the conclusion that trailers come after the body; they could be interleaved.  

Much wretching and signs of distress. 

Open issue: how to indicate support?  Draft-lassey-priority-setting

Lucas:  the design from Montreal has evolved to bitmask negotiation on highest compatible scheme.  

MT: highest mutually supported did not work out well with other protocols.

End-to-end vs. Hop-by-hop?  Header means what the original requester saw as the priority.  

Ian:  does “background” priority indicate less aggressive congestion control.  Useful, but is it cross-layer?

Roberto:  being able to use a header allows us to re-use a known api.

Victor: could you have both “background” and non-background on a single connection?  If so, how do you deal with switching congestion controllers in a single connection?

Jana:  This is a very hard problem.  If all of them are a background, this works as long as no non-background resources come along later.

Mnot: we’re running over time, so let’s treat this as an update and hold questions.

No normative language should come from this--purely a note that these priorities should be considered in the selection of things like congestion controller.

Lucas:  Is the prioritization all about the response bodies?

Mnot: Good question.

Ian:  Seems like it is response or it doesn’t matter.

Lucas:  There are prioritizations of things like posted bodies?

Mnot: probably need two headers, as these are different.

Can we ship something in time for HTTP/3?

Ryan: we should have some mechanism to help servers send the right things to clients.  If it is simple enough, then we can do it in time.  Things look simple enough here to adopt this and get it done in time.

(Discussion of wrangling required)

Ian will write a draft for Singapore and present it in HTTP and QUIC.  The draft will need extensions for both H2 and H3; the negotiation pieces for H3 needs to be done for QUIC.

### Key discards 

MT: No one has gotten a solution that has resulted in happiness.  My suggestion is:  you keep the keys forever.  If someone can find a solution that allows us to discard them before the connection closes, we can consider that.  

Kazuho: the simplest way to confirm that handshake is confirmed then doing a key update.

MT: I’d like to see that proved.

Jana: I propose we resolve the issue with “keep the keys forever”.  We remove the section.

Victor: discard them after 3 minutes.

Ekr:  That was my initial suggestion

(shouted down)

David:  If we say forever, it won’t be honored; people will drop them, and they will pick the wrong times.

MT: We warn them of the deadlock.

Subodh: We have a lot of implementation pitfalls in TLS.  We may need that for QUIC, for all things like this.

Roberto: my least favorite cost is the one where I pay for something and get nothing.  Deadlocks and long time outs are really painful. 

Ryan:  I am super sensitive to the concern that we would like to drop the keys if we can’t.  But the days of discussion have left me that this is not doable until someone can prove otherwise. We can get along without this mechanism, and we should tell people why we came to that conclusion.

Christian: We did this to confirm both key rotation and migration.  We have to be a bit more specific than just remove the text if we are going to handle this well.

Kaz: my personal feeling is that key update works, but it only works if the client stops sending handshaking packets. 

Ekr:  I’m generally in favor of this, although I’m also in favor of 3 minutes and 1 second.  We’ve burned a lot of time and brains on this, and this puts the onus on folks who believe they have a solution.

Roberto: This is not verifiable by the client, so it’s only a suggestion; folks may be doing something other than this suggestion, and there is nothing we can do.

Nick:  I think explicit signal is the only way around this, and we don’t have that.

Eric:  I agree with Christian that we need to retain text to tell people when they can go on to other things; we shouldn’t lose sight of that.

Subodh:  What about 0-RTT keys?

All: not the same issue of deadlock.  

Mnot:  We have a plan, the next step is PR.

### Jana:  Interop runner.  

Marten:  Dockerized implementations that run test cases against each other and reports the output.  After the tests run, we take a pcap and check that the right thing happened (e.g. retry).

https://github.com/marten-seemann/quic-interop-runner

Adding tests now.  We will be adding performance tests, for example, in loss conditions (to see handhsake packet drops are recoverable, etc.).  Cloudflare and Facebook working on adding dockers now. If you have ideas for new test cases, please send us a PR.

License file will be added.

For every test, it saves the log files, you can see what went wrong in the log file.  


