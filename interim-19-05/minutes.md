
# QUIC May 2019 Interim Meeting Minutes

* Chairs: Mark Nottingham, Lars Eggert
* Location: London, UK
* Scribes:
	- Wednesday morning: Cory Benfield
	- Wednesday afternoon: Mike Bishop
	- Thursday morning: Martin Duke
	- Thursday afternoon: Eric Kinnear

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Administrivia](#administrivia)
- [Interop](#interop)
- [Transport and TLS](#transport-and-tls)
  - [#2736: More Connection ID Space](#2736-more-connection-id-space)
  - [#2534: ECN text disables ECN too aggressively](#2534-ecn-text-disables-ecn-too-aggressively)
  - [#2581: Bring back AEAD_AES_128_CCM_8 now that we pad the plaintext](#2581-bring-back-aead_aes_128_ccm_8-now-that-we-pad-the-plaintext)
  - [#2656: Discarding connection state at server on unvalidated client](#2656-discarding-connection-state-at-server-on-unvalidated-client)
  - [#2541: Clients cannot abandon Initial packets while server can still send initial close](#2541-clients-cannot-abandon-initial-packets-while-server-can-still-send-initial-close)
  - [#2673: Output of the discard keys design team](#2673-output-of-the-discard-keys-design-team)
  - [#2550: Apply GREASE to transport parameters](#2550-apply-grease-to-transport-parameters)
  - [#2602: Idle timeout needs more description and a recommendation](#2602-idle-timeout-needs-more-description-and-a-recommendation)
  - [#2552: Saving a round-trip time in the initial handshakes with retry](#2552-saving-a-round-trip-time-in-the-initial-handshakes-with-retry)
  - [#2546: ACK of ACK are useful](#2546-ack-of-ack-are-useful)
  - [#2441: Peers that only terminate a single connection on an IP/port cannot migrate with 0-byte CIDs](#2441-peers-that-only-terminate-a-single-connection-on-an-ipport-cannot-migrate-with-0-byte-cids)
  - [#2496: QUIC Version Ossification](#2496-quic-version-ossification)
  - [#2084: Discuss requirement that connection IDs not be correlatable](#2084-discuss-requirement-that-connection-ids-not-be-correlatable)
  - [#2170: Embed QUIC version in expansion](#2170-embed-quic-version-in-expansion)
  - [#2143: Be more conservative about migration](#2143-be-more-conservative-about-migration)
  - [#2180: Is Retry a new connection or what?](#2180-is-retry-a-new-connection-or-what)
  - [#2473:  CID Length Changes](#2473--cid-length-changes)
  - [#2387](#2387)
  - [#2389:  Be clearer about the purpose of disable_migration](#2389--be-clearer-about-the-purpose-of-disable_migration)
  - [#2309:  Migration before handshake completed](#2309--migration-before-handshake-completed)
  - [#2308:  Handling of coalesced packets with decryption errors creates DoS opportunity](#2308--handling-of-coalesced-packets-with-decryption-errors-creates-dos-opportunity)
  - [#2580:  Is path validation a SHOULD or a MUST?](#2580--is-path-validation-a-should-or-a-must)
  - [#2192: Optimistic ACK in early handshake](#2192-optimistic-ack-in-early-handshake)
  - [#2394: Spoofed Retry token attack on IP Authentication](#2394-spoofed-retry-token-attack-on-ip-authentication)
  - [#2205:  Largest acked MUST NOT decrease](#2205--largest-acked-must-not-decrease)
  - [#2471:  Stateless Reset Lacks Normative Text](#2471--stateless-reset-lacks-normative-text)
  - [#2743: Better articulate principles for ciphersuites](#2743-better-articulate-principles-for-ciphersuites)
  - [#2656: Discarding connection state at server on unvalidated client](#2656-discarding-connection-state-at-server-on-unvalidated-client-1)
  - [#2541: Clients cannot abandon Initial packets while server can still send Initial close](#2541-clients-cannot-abandon-initial-packets-while-server-can-still-send-initial-close)
  - [#2496](#2496)
  - [#2741: Revisit Initial keys discard](#2741-revisit-initial-keys-discard)
  - [#2725: We lost the text recommending replacement of used CIDs](#2725-we-lost-the-text-recommending-replacement-of-used-cids)
  - [#2645: Retire one’s own CID](#2645-retire-ones-own-cid)
  - [#2724: PATH_RESPONSE not retransmitted](#2724-path_response-not-retransmitted)
  - [#2689:  Checking Duplicate TPs is onerous](#2689--checking-duplicate-tps-is-onerous)
  - [#2684:  Mixture of transport and congestion control functions](#2684--mixture-of-transport-and-congestion-control-functions)
  - [#2732:  Reuse of SRTs](#2732--reuse-of-srts)
  - [#2685:  CC state after a change of path](#2685--cc-state-after-a-change-of-path)
  - [#2720:  Privacy of spin with multiple connections on same 5-tuple](#2720--privacy-of-spin-with-multiple-connections-on-same-5-tuple)
- [Viktor - WebTransport](#viktor---webtransport)
- [Planning](#planning)
- [Recovery Issues](#recovery-issues)
  - [#2728: x1](#2728-x1)
  - [#2650: simplify recovery if Handshake Timer was unified with PTO.](#2650-simplify-recovery-if-handshake-timer-was-unified-with-pto)
  - [#2648: crypto time value should include rttvar](#2648-crypto-time-value-should-include-rttvar)
  - [#2638: max-ack-delay unknown for new connections.](#2638-max-ack-delay-unknown-for-new-connections)
  - [#2630: define “under-utilization” of cwnd](#2630-define-under-utilization-of-cwnd)
  - [#2596: should platform delays be in ack-delay?](#2596-should-platform-delays-be-in-ack-delay)
  - [#2593: persistent congestion when app-limited](#2593-persistent-congestion-when-app-limited)
  - [#2556 kPersistentCongestionThreshold 2 or 3?](#2556-kpersistentcongestionthreshold-2-or-3)
  - [#2555: idle period for congestion control](#2555-idle-period-for-congestion-control)
  - [#2534: ECN verification too strict](#2534-ecn-verification-too-strict)
  - [#1860 (Editorial): ack-only feedback loop in recovery instead of transport](#1860-editorial-ack-only-feedback-loop-in-recovery-instead-of-transport)
- [Resolve Asymmetric Idle Timeout Definitions](#resolve-asymmetric-idle-timeout-definitions)
- [QPACK](#qpack)
- [HTTP/3](#http3)
  - [#2718: Truncated Stream Handling is Aggressive](#2718-truncated-stream-handling-is-aggressive)
  - [#2711: Relax prohibition on server-initiated bidirectional streams](#2711-relax-prohibition-on-server-initiated-bidirectional-streams)
  - [#2699: Specify handling of QUIC SERVER_BUSY connection failures](#2699-specify-handling-of-quic-server_busy-connection-failures)
  - [#2551, 2662: Replace MALFORMED_FRAME with specific error codes](#2551-2662-replace-malformed_frame-with-specific-error-codes)
  - [#2516: Semantics of MAX_HEADER_LIST_SIZE](#2516-semantics-of-max_header_list_size)
  - [#2498: Behavior on out-of-range settings](#2498-behavior-on-out-of-range-settings)
  - [#2412: Can MAX_PUSH_ID go backward?](#2412-can-max_push_id-go-backward)
  - [#2410: Import rules on “malformed requests” from RFC7540](#2410-import-rules-on-malformed-requests-from-rfc7540)
  - [#2697: SHOULD use PRIORITY](#2697-should-use-priority)
  - [#2502/2690: Priority inversion from reordering](#25022690-priority-inversion-from-reordering)
  - [#2678: Use unidirectional streams for everything!](#2678-use-unidirectional-streams-for-everything)
  - [#2526: PUSH_ID frame](#2526-push_id-frame)
  - [#2632: Symmetric GOAWAY](#2632-symmetric-goaway)
  - [#2488: Embed address validation token in Alt-Svc](#2488-embed-address-validation-token-in-alt-svc)
  - [#2439: http:// URIs over HTTP/3](#2439-http-uris-over-http3)
  - [#2223: Coalescing rules](#2223-coalescing-rules)
  - [#253: HTTP/3 without Alt-Svc](#253-http3-without-alt-svc)
- [QUIC Firewalls](#quic-firewalls)
- [HTTP/3 Priorities](#http3-priorities)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->



## Administrivia

Don’t register for in-person unless you are really going to attend.  Finding meeting rooms for 50 ppl is challenging.

## Interop

Good participation of ~17 implementations, but many still working on basic issues.
Reminder that physical presence in Montreal not required for interop: may use Slack for virtual interop.

## Transport and TLS

Triaging issues at https://github.com/quicwg/base-drafts/projects/5.

How to contribute? https://github.com/quicwg/base-drafts/blob/838b1c203de4cc1aed278a873a23c49eed6145fe/workflow.png

Concerns about long-standing editorial issues that are unclosed. Clarifies that editorial issues are at the discretion of the editors and that editors can do whatever they see fit, including asking the filer to provide a PR.

Guideline: changes to normative text are design issues, even if they are only intended to clarify existing text.

### #2736: More Connection ID Space

https://github.com/quicwg/base-drafts/issues/2736

Core question: are we willing to reopen the invariants to allow more connection ID space? Discussion suggests general willingness to widen CID space at this point. No pushback in the room: rough agreement on proposed wire form (https://github.com/quicwg/base-drafts/issues/2736#issuecomment-494722498).

Discussion regarding limiting the max CID size: proposals to have invariants limit to 255/256 and potentially limit to lower size in QUICv1. Proposed lower values include somewhere around two symmetric cipher blocks plus some slack (e.g. 2 bytes). Also proposed to limit to no larger than one cache line.

Hum for limited vs unlimited. Hum in favour of limited (zero hums for “practically unlimited” which corresponds to 255/256).

Consensus in the room: don’t GREASE the first bit.

How do we respond to connection IDs that are larger than the limit? Simplest proposal: drop the packet.

Proposal is for Martin Duke to prepare a PR adjusting the text to allow widening the CID space. 

Later:  PR #2749 has been filed for this.  We will not use varints to encode the length of the CID.  Much discussion about greasing the part of the range we aren’t using while being able to reclaim them in the future, but likely will not.  If they ossify, we cope; if they don’t, we use them.

### #2534: ECN text disables ECN too aggressively
https://github.com/quicwg/base-drafts/issues/2534

Agreed needs addressing as a design issue. Not a transport issue, it’s a recovery issue. Agreed Jana will write a PR.

### #2581: Bring back AEAD_AES_128_CCM_8 now that we pad the plaintext
https://github.com/quicwg/base-drafts/issues/2581

AES-CCM-8 is present in TLSv1.3 primarily for IoT implementations (GCM is poor fit). However, CCM8 is not a generally good cipher, so unlikely to want to build a webserver with it. Ekr requested clarification about what the intended use-case is here.

One option is including CCM_8 in transport and banning it in HTTP/3. Bit awkward that it wasn’t previously banned in HTTP over TLS1.3, but workable.

Text has an error that must be remedied asserting TLS 1.3 only has 16-byte tags in the AEAD, which is just untrue.

Question: must QUIC stacks reject offering CCM_8, or just ignore it? If the answer is “ignore”, adding CCM_8 later is a very simply RFC. Only reason offered to add CCM_8 now is consistency.

This specification ought to be written in such a way that new cipher suites being added to TLS should just naturally work with QUIC, absent any extra reason it shouldn’t work. There appears to be a requirement to add text for any new algorithm to explain how it works with header protection. Ekr volunteers to add text to attempt to future-proof for new algorithms.

Noted that IANA does not mark the CCM_8 cipher suites as recommended.  In fact, there is a note to explain that the CCM_8 suites are not for general use.

Martin Thomson is drafting functional requirements for cipher suites. New PR opened to track this proposal with wording: https://github.com/quicwg/base-drafts/pull/2743.

Outcome: the CCM_8 issue will likely be closed with “no action” once the related work is completed. The current text must change, see #2743. Martin is writing text.

### #2656: Discarding connection state at server on unvalidated client
https://github.com/quicwg/base-drafts/issues/2656

Core issue is that unvalidated connections should have shorter timeout than the standard idle timeout.

Left to the handshake editors to amend.

### #2541: Clients cannot abandon Initial packets while server can still send initial close
https://github.com/quicwg/base-drafts/issues/2541

See also #2741: https://github.com/quicwg/base-drafts/issues/2741.

Endpoints must either send close in initial and handshake, or delay discard of initial.

Deferring until we evaluate #2741.

### #2673: Output of the discard keys design team

A design team was formed in Prague to look into discarding old keys. Outcome is https://github.com/quicwg/base-drafts/pull/2673. Moving to consensus call on the list.

### #2550: Apply GREASE to transport parameters
https://github.com/quicwg/base-drafts/issues/2550

Author to write a PR.

### #2602: Idle timeout needs more description and a recommendation
https://github.com/quicwg/base-drafts/issues/2602

Expected behaviour is that an endpoint uses the minimum value of the idle timeout provided by each peer.

Disagreement in the room on the above. Argument is that the idle timeout is a promise to close at time X: alternative understanding is that it is a promise not to close *before* X time.

Counter argument: keeping the connection alive longer than the lower timeout may incur a 1-RTT cost to get a stateless reset. Implementations concerned about performance may choose to never incur this risk and use the min.

The min approach is particularly dangerous if the peers disagree: if the first peer sets a timeout to 5 seconds and a second peer sets it to 10 seconds, the second peer really should avoid dropping the connection earlier than 10 seconds as the first peer may be relying on the connection still being up. This argues for clarifying the text.

Of course, the connection can be dropped before the idle timeout anyway for many reasons. Perhaps the document should be amended to clarify that the idle timeout can only possibly be a guideline and connections can go away at many times.

Similar issue to TCP user timeout (RFC 5482).

The server may choose to advertise the min of its max and the client set value, to avoid ambiguity. The client cannot use this algorithm as it is forced to speak first.

Hum in the room: who believes Martin Thomson’s pitch (keep idle timeout asymmetric), who would like to explore min of the two values.

Martin Thomson will provide a PR that clarifies the current text (https://github.com/quicwg/base-drafts/pull/2745). A second PR will be provided by Ian Swett to explore alternatives.

### #2552: Saving a round-trip time in the initial handshakes with retry
https://github.com/quicwg/base-drafts/issues/2552

Consensus in the room was to close, as this can be implemented as an extension. Will be taken to the list.

### #2546: ACK of ACK are useful
https://github.com/quicwg/base-drafts/issues/2546

Question is whether the MUST NOT should be changed to a SHOULD NOT: otherwise the issue is editorial. Alternative is to use ACK+PING which requires no normative text change.

There may not be a problem here due to ACKs of flow control frames.

Ian Swett proposes that allowing the sender to choose when it wants feedback on ACKs (by ACK+PING) is useful. On poor connections, ACKing ACKs can lead to connections that never go away. ACK+PING also allows the peer that holds the state that needs clearing to control when that state gets cleared.

Martin Thomson notes that well-behaved peers that send data should be sending ACKs in at least some of the packets.

Agreement in the room to close. Ian Swett to write editorial text to cover how implementations should behave in this case.

### #2441: Peers that only terminate a single connection on an IP/port cannot migrate with 0-byte CIDs
https://github.com/quicwg/base-drafts/issues/2441

Agreed in Prague this would be deferred / closed.  Requires consensus call, no discussion needed.

### #2496: QUIC Version Ossification
https://github.com/quicwg/base-drafts/issues/2496
There is a proposed PR: #2573 (https://github.com/quicwg/base-drafts/pull/2573).

This mechanism is optional to allow servers that cannot commit to preserving keys to not have to do so. There are concerns about whether optional proposals can actually prevent ossification.

Proposal in the room that this issue be an extension via an I-D. Given that this issue is relating to preventing version ossification, v1 may ossify before we have that extension. It is mentioned that middleboxes that want to ossify on v1 may do so regardless of this extension by dropping packets altogether and allowing fallback.

Ossification may occur before the RFC is finalised as middleboxes don’t pay attention to RFCs they pay attention to wire traffic. Middleboxes may ossify regardless of this proposal by applying more sophisticated heuristics. It may be better to simply mint a v2 early to ensure that there are always multiple version numbers. Note that this proposal requires both a client and a server to actually do this in order to be effective.

There was a hum about whether this has to be solved by when v1 ships. Hum indicated that this discussion should be continued.

Alternative proposal from Kazuho is to allow ossification of this field as it only freezes the initial packet format. Essentially this would follow the TLS model: add a new version field that you actually do GREASE.

Ekr intends to float a different proposal than the one in the PR.

Both proposals are being discussed without certainty as to whether they will end up in the transport specification or whether they will end up as extensions.

Discussion also covered whether it should be possible to fingerprint QUIC packets by means of the version number field. There was pushback against using the version number as a mechanism for fingerprinting QUIC: the room notes that it’ll be used for that purpose anyway.

Jana’s research: there are 6 firewall vendors that offer QUIC identification and disabling at this time. This is already happening.

### #2084: Discuss requirement that connection IDs not be correlatable
https://github.com/quicwg/base-drafts/issues/2084

### #2170: Embed QUIC version in expansion
https://github.com/quicwg/base-drafts/issues/2170

Assigned to ekr.

### #2143: Be more conservative about migration
https://github.com/quicwg/base-drafts/issues/2143

Eric Kinnear does not believe that anything needs to change here, though it may require summarising the current state.

Ekr would like to have a list of assertions of the security properties of QUIC.

Christian:  The only way to be more conservative here is to disable support for NAT rebinding.

Eric Kinnear to finalize.

### #2180: Is Retry a new connection or what?
https://github.com/quicwg/base-drafts/issues/2180

Christian:  There are a dozen implementations that got it right -- let’s close this.
Jana:  Doesn’t mean it’s clear.
No one is willing to propose changed text.
Change to editorial to verify that the change he promised to make has already happened - require client not to change ClientHello following Retry.  Does server have to enforce this?
No, but it MAY.

### #2473:  CID Length Changes
https://github.com/quicwg/base-drafts/issues/2473

Agreed to close in Prague.  Moving on.

### #2387

Already assigned; no discussion.

#2342:  Spoofed connection migration as a DoS vector
https://github.com/quicwg/base-drafts/issues/2342
Servers that prohibit migration could open themselves up to a DoS if the attacker makes it look like the client has done a migration that it was told not to do.  Server can’t treat a happened-to-work migration as a protocol violation.  In Tokyo, agreed that server can do validation and allow the migration if it makes it, but TP is a signal to client that it probably won’t work.  Means we need to remove the error code for an invalid migration and the text requiring it be sent.

Rehash of Tokyo; just needs a PR.  Erik’s PR doesn’t quite cover this; will update to close this issue as well or create a new PR.

### #2389:  Be clearer about the purpose of disable_migration
https://github.com/quicwg/base-drafts/issues/2389
Erik will fix this in the resolution to #2342.

### #2309:  Migration before handshake completed
https://github.com/quicwg/base-drafts/issues/2309

Depends on handshake/key design team PR.  Leave it.

### #2308:  Handling of coalesced packets with decryption errors creates DoS opportunity
https://github.com/quicwg/base-drafts/issues/2308

Agreed in Tokyo that each packet type can be present only once in a datagram.  Sender cannot coalesce multiple packets of the same type.  Receiver MAY discard second and further packet of the same type. Maarten was going to write a PR and hasn’t yet.

Ekr questions whether this attack has real performance impact, and what the principles and threat model are which motivating this defense.  No one could articulate a precise threat model, and there was some movement toward not doing this.  Jana observed that there’s a recovery problem if we allow this, regardless of DoS concerns -- many packets at the same encryption level magnifies perceived reordering in the recovery logic.  This justifies the prohibition, but perhaps only as a SHOULD.

MT has already written the SHOULD NOT sentence; receiver MAY ignore all but the first of a given type in a datagram.  Ekr is concerned there might be a deadlock there.  MT will work it out in #2747.

### #2580:  Is path validation a SHOULD or a MUST?
https://github.com/quicwg/base-drafts/issues/2580

Will be closed by #2637; needs a consensus call.

### #2192: Optimistic ACK in early handshake
https://github.com/quicwg/base-drafts/issues/2192

We discuss this in the Security Considerations already.  Let’s just close this as already addressed.

### #2394: Spoofed Retry token attack on IP Authentication
https://github.com/quicwg/base-drafts/issues/2394

Don’t need to address this; Retry token is one of many things you need to do, not something by itself.  Purpose isn’t to avoid amplification attacks, but to help servers mitigate DoS.  Ekr will respond to issue; propose to close with no action.

### #2205:  Largest acked MUST NOT decrease
https://github.com/quicwg/base-drafts/issues/2205

Text added since then has mostly covered this; title is no longer accurate.  Jana will prepare a PR restating what’s already there, but Mark would prefer to take it through a consensus call anyway.

Ian notes that retransmitted ACKs can mess with RTT estimates.  This is worth recommending against in the recovery doc.  Ian will open a separate issue for this.

### #2471:  Stateless Reset Lacks Normative Text
https://github.com/quicwg/base-drafts/issues/2471

Consensus call is pending, but Martin Duke objects to the proposed resolution.  Stateless Reset is never required, so SHOULD or MAY send it; SHOULD look for it on incoming packets.  Will remove the proposal-ready tag; Martins will confer and MT will update the PR.

### #2743: Better articulate principles for ciphersuites
https://github.com/quicwg/base-drafts/pull/2743

Issuing consensus call.

### #2656: Discarding connection state at server on unvalidated client
https://github.com/quicwg/base-drafts/issues/2656

Assigned to Jana.

### #2541: Clients cannot abandon Initial packets while server can still send Initial close
https://github.com/quicwg/base-drafts/issues/2541

Leave as-is.

### #2496
https://github.com/quicwg/base-drafts/issues/2496

Kazuho, Christian, and Ekr will sort it out.
Triage

### #2741: Revisit Initial keys discard
https://github.com/quicwg/base-drafts/issues/2741

Triage approved.  David is willing to take this back to the Design Team for discussion.

### #2725: We lost the text recommending replacement of used CIDs 
https://github.com/quicwg/base-drafts/issues/2725

Declared editorial.

### #2645: Retire one’s own CID
https://github.com/quicwg/base-drafts/issues/2645

Triage approved; there’s obviously ample discussion already.

CID design team agreed that CIDs are irrevocable once issued.  However, there are cases where you can’t honor an old CID any more.  How does the issuer force the consumer to move off of it?

Various specific proposals, but high-level question is whether we need this in the core protocol.  Nick argues that endpoints can encode information in the CID, and if it changes (e.g. RSS rebalancing) the old CIDs become “wrong,” or the handshake CID has to be selected before the value is known.  Much discussion about design and repeated pull-backs to whether we want to do this.

Ian says he would “probably” use this if it exists; would others?  Jana points out that there are other potential uses.  Kazuho thinks the mechanism is attractive.  Lars suspects anyone interested in high performance will eventually be interested.  Some discussion about whether this is client-only or server-only, but desire to keep it symmetric.

We could force re-establishment of the connection.  Does QUIC need a mechanism to do this gracefully?  Discussion about which is more appropriate.  Could this be an extension and certain application protocols require it?  For Nick’s scenario, no -- this is a generic issue across all application protocols.  

Nick will consider a more concrete proposal and bring it back to the list.

### #2724: PATH_RESPONSE not retransmitted
https://github.com/quicwg/base-drafts/issues/2724

There’s already a PR for this -- it’s converting prose to a MUST.

### #2689:  Checking Duplicate TPs is onerous
https://github.com/quicwg/base-drafts/issues/2689

PR for this is ready -- issue consensus call.

### #2684:  Mixture of transport and congestion control functions
https://github.com/quicwg/base-drafts/issues/2684

There’s a lot in the recovery draft that’s typically considered transport and vice versa.  Try to separate them out more.  Ian agrees, after reading.  Mark this editorial and Gorry will work offline with the editors.

### #2732:  Reuse of SRTs
https://github.com/quicwg/base-drafts/issues/2732

Already has a PR.  Not illegal, but if you do this you have to remember all the CIDs, even if they’ve been retired.  Sending for consensus call.  One outstanding comment; Mark will ask for follow-up.

### #2685:  CC state after a change of path
https://github.com/quicwg/base-drafts/issues/2685

“Reasonably sure” is too loose; Jana will propose a more concrete definition, and Gorry will poke holes in it.

### #2720:  Privacy of spin with multiple connections on same 5-tuple
https://github.com/quicwg/base-drafts/issues/2720

This is a lower-case “should try” that no one will ever implement, according to Ekr.  Editorial by unanimous acclamation.
Future-Looking
Want to seriously drive down design issues by Montreal.  Aiming for a period of “no design changes” soon for deployment experience and stability, and the chance to release editorial-only drafts so people can verify that only the presentation has changed.

We’re not going to make our July 2019 milestones, obviously.  Should we move?  Perhaps just leave them alone until we have a more realistic estimate.

## Viktor - WebTransport
Slides:  https://github.com/quicwg/wg-materials/blob/master/interim-19-05/webtransport-20190522.pdf

Transport-independent API that exposes streams and datagrams (like WebSockets) without caring what the underlying transport actually is (WS, H2, WS/H2, H3, raw QUIC, strange alien technology…).
Some additional features people are hoping to see here (priorities, scatter/gather, etc.) that Viktor intends to incorporate.  Much interest from various directions.  David points out similarity to Masque and possible synergy there.  Discussion about discovery, or lack thereof.



## Planning

Lars: Time for draft-21? It would need to be within the next month. Is there enough stuff in the editor’s draft and about to land to make it worthwhile?

Mark: few enough design issues in -transport that we could conceivably be done for Montreal.

Christian: We should test the change to the invariants sooner rather than later.

ekr: Version Ossification is a potential invariants change as well.

Roberto: things are already in production!

ekr: The drafts say not to put it into production.

DavidS: Willing to make changes, as long as people respect our constraints

Lars: proposal - focus on discard keys, version ossification, and connection ID length as a gate for the next draft.

Ian: We may not reach consensus on version ossification by then.

Mark: beyond Montreal, drafts should be stable for a while

Lars: I will propose a virtual interop date.

Mark: We could hold an interim about extensions

Lars: probably don’t need an interim on base drafts.

Mirja: extensions may need a wider audience.

Mark: what we really need is another interop -- maybe 2.5 days

Lars: might dedicate a session to extensions.
Roberto: when do we start up v2? If we don’t do it explicitly, stop.

Lars: we need a recharter -- more than v1 and multipath on the table; real-time stuff, v2, etc.

Martin S: Ship v2 just to add version negotiation.

Ekr and DavidS: We could just make it an extension, but we could start greasing version numbers.

ekr: issues may accrue; let’s not assume we’re done. Not sure multimedia is a great subject.

Roberto: That’s because we’re trying to not to slow down v1. We’re holding back.

David S: talk about DATAGRAM extension

Mark: BOF in Montreal?

Martin D: QUIC-LB.

Mark: Nice thing about that one is that it doesn’t need outsiders

Jana; would be nice for media streaming and DATAGRAM to be in parallel, rather than series.

Mirja: We should put out a call for subjects. Not everything might be in the QUIC WG.

Mark: We’ll figure out how exactly how to organize this offline.

Lars: next interim/interop: North America, September.

Mark: if it’s only interop, is that OK (show of hands is ~80% OK with it). If there are travel to US issues, let us know.

Martin D: How big does an interop room need to be?

Mark: interop only could probably need to fit only 35 people.

## Recovery Issues

### #2728: x1
Christian: we should exit slow start earlier sometimes
Lars: we’re not chartered to design congestion control - makes sense, but off-topic

Ian: Cubic references 2 RFCs. We can add those references editorially.

Christian: yes, let’s have a pointer for naive implementers.

Jana: This is not the only problem with Reno. Opens the floodgates to a million new references.

Christian: close with no action.

### #2650: simplify recovery if Handshake Timer was unified with PTO.
Ian: Timers are awfully similar now, with a few edge cases. I tried to write a PR, and failed. I’ll try again but would like confirmation that I’m on the right track. Main substantive difference is that handshake timer would include RTTVAR.

Jana: We’ve implemented this and it seems fine.

### #2648: crypto time value should include rttvar
Jana: subsumed by the same PR as #2650

### #2638: max-ack-delay unknown for new connections.
Jana/Mike B: PR is there, needs to go to consensus call.

### #2630: define “under-utilization” of cwnd
Ian: There’s a PR for this.

Jana: If inflight is less than cwnd, what should you do?

Christian: This is a change from Reno.

Gorry: This problem has been around forever. It’s tricky to get this right. We have to say something.

Ian: There’s a pointer to an RFC in the existing text.

Lars: we would need to translate into QUIC terms.

Jana: Let’s define under-utilization in clear terms, then provide pointers to some possible mitigations.

Ian: We either have that now, or had it until recently. We can’t say pacing means we’re not cwnd-limited. We just need to pound out some text. Ian, Gorry, and Jana will do it.

### #2596: should platform delays be in ack-delay?
MT: we have a resolution for this. the reported ack-delay is intentionally added, not the various inherent costs of getting things on the wire.

### #2593: persistent congestion when app-limited
Ian: I think this is fixed. I’ll follow up with Subodh.

### #2556 kPersistentCongestionThreshold 2 or 3?
Jana: best discussed in Montreal. How many PTOs before we do an RTO-equivalent?

### #2555: idle period for congestion control
Ian: Will fix it in one PR with other stuff. Everyone recommends slow start after idle and no one implements it. Instead, have a short burst and then pacing. Microsoft neither slow starts nor rate paces, and objects to codifying that.

Christian: isn’t this congestion control research?

Roberto: nobody does what the spec says. So it’s not research.

Jana: There is no standard solution to this problem. Let’s list a minimum set of things to be compliant and point people to other solutions.

ekr: why push a document people won’t comply with?

Gorry: IETF specs apply to the general internet. We don’t need to say much here.

Christian: congestion control is not an interoperability issue.

Jana (to ekr): It’s Reno, so we’re already there. help naive implementers do something not stupid.

Martin D: how about just say “SHOULD NOT send large bursts after idle”, and leave it at that.

Jana: how do you define burst?

Martin T: Let’s be up front about it.

Gorry: we have a notion of a burst and pacing.

Martin T: bursting is sending at line rate.

Mark: Nothing we will say here will change behavior.

Martin T: Let’s just state our disagreement on behavior.

Mirja: RFCs should state behavior we know to be safe.

Martin T: Let’s be explicit about that principle.

Jana: Let’s articulate some higher-level principles that we must adhere to, and then provide Reno as an example. WE have enough info to move forward.

### #2534: ECN verification too strict

Martin D: talked about this yesterday; Jana has a PR now. (#2752)

Martin T: No advice for how to determine if path supports ECN. Many comments/proposals in my review. We should test a path for a while, then give up.

Jana: I didn’t want to be too strict about what to do, endpoints will need to figure this out for themselves. I think general advice is useful. 
At the beginning, does the assumption about ECN capability on the path hold throughout? 

Martin T: You test it once, mark it as capable if test passes, if it ever fails, disable. A reasonable tweak would be to allow retesting later. 

Gorry: It would be reasonable to “MAY retest if reason to do so”

Mirja: The general assumption would be that it should would. If not locally exposed then that’s a real problem, but anything else would not be a real problem. We should not optimize for a case that’s not a real problem. 

Martin T: If you get bleaching because the other side can’t read the markings or because the path is actively scrubbing them, then you’d keep sending them on one side and I don’t think that’s a problem. 

Mirja: Should not be sending it if it’s not working on the path. 

Jana: We do detect bleaching. That’s the test to see if you can get it echoed back. 

Mirja: If you only implement that part, you’re probably good. 

Gorry: We could add some text that says “if your path supports ECN then the test just passes right away”. 

Jana: Will take that as an editorial suggestion. Everyone is okay with describing a test for what to do? I think we need that, unless someone strongly disagrees. I can write it in such a way that someone who doesn’t care for doing testing they can simply bypass that section. 

Martin T: I’m making a new issue to track writing down an algorithm and then we can negotiate the bleaching case. 

Jana: The bleaching case is already there, we can move it around. How does new issue relate to this PR? 

Martin D: Original problem was outdated reference to RTO, but that has been satisfied now, so the original issue is good and if MT wants to open a new one to change the text that’s good too. Let’s close the old issue.

Conclusion: Close the old issue, MT opening new issue to track moving text around (and writing down algorithm for test if not already there).

### #1860 (Editorial): ack-only feedback loop in recovery instead of transport

Ian; we should just move it all to recovery.

ekr: It should all be in transport; as recovery is quasi-optional.

Jana: loss recovery isn’t optional.

Mike: this feels like the kind of thing you have to do to interoperate, thus in -transport.

Ian: putting critical stuff only in transport hasn’t really worked out.

ekr: as an implementer, -transport is the right place to have this material.

Mirja: Minimum requirements to transport, fancier stuff to recovery. e.g. “one ack per RTT” in transport, “every other packet” in recovery.

Ian: does anyone object to all ack-sending text to transport?

Jana: we have to have something about it in recovery to set sender expectations. do we want to have lots of overlap?

christian: relationship between recovery and transport is same as transport and invariants.

MT: send all of recovery section 4 to transport.

Martin D: there is less flexibility in ack sending because we don’t know the sender’s exact loss recovery and congestion control.

Gorry: you have to read both documents anyway.

Mark: recovery in the old process. Should probably move it over soon. Are you comfortable moving it over?

Ian/Jana: in Montreal, once we land stuff in flight.

David S: Discard/keys is relevant to acks, so this change works better.

Mirja: Don’t move all of Section 4, but I’m not sure what.

Jana: almost all, not all.

## Resolve Asymmetric Idle Timeout Definitions
Roberto: I would like to resolve asymmetric idle timeouts. 2 conflicting definitions. Difference between “sending more packets is counterproductive” and “state probably still exists on the remote host”

ekr: what’s the practical difference?
Roberto: I might want to send in the second case.

Ian: what is expected to happen if it sends?

Roberto: it’s a crapshoot, maybe there have been packet losses? First order is to define what it means.

Ian: We should not send after the idle timeout. (ekr concurs)

MT: question is what you do after your own timeout?

ekr: A reaper could mean that I exceed my timeout.

Kazuho: in the general case, the client cannot adjust its idle timeout based on the server’s number. Thus, we should use min.

ekr: it’s pointless to send data after the peer’s timeout. But are you obligated to send a close?

Roberto: I should not send any packet after the peer timeout (a new incoming packet should reset the timer).

Christian: these are optimizations. the contract is that I’ll still be there during the idle timeout.

MT: we’re spinning our wheels

Jana: we don’t need to police behavior in the space between the two idle timeouts. If I happen to set a receive, lucky us.

Roberto: Extraneous CLOSEs are bad for radio networks.

ian: It’s painful to match the TPs on the serverside. What use case is this supporting?

ekr: current doc says “I will hang around that long, and will send a CLOSE before that”

Christian: There is the silent close issue, but also how often we are sending keepalives.

MT: If our timeout is smaller, but we have something to say. Should we send it?

Mirja: large timeout probably not an issue if we advertise it; send a close.

Lars: there is a slippery slope to negotiating. If I said an hour, I should be around for an hour.

Jana; what a waste.

Udip: I don’t think servers are going to wait once its timer expired.

Kazuho: Lars’s model creates an HTTP race condition.

Roberto: the races are irresolvable.

ekr: what are the expectations after the peer’s timeout?

martin d: let’s please pick one and discuss it.

lars: OK, can we take the min of the timeouts and use it as my idle timeout? this is the first thing to resolve

Alan: Just take the min. silent close is better than forcing a CONN_CLOSE.

Lars: reason not to do min is to minimize PINGs

Martin D: Is anyone actually opposed to min?

Mark: Everyone too hungry to discuss. Go to lunch.



## QPACK

#2100: Avoid creating QPACK codec streams when unnecessary
https://github.com/quicwg/base-drafts/issues/2100 

Alan: Summary from Tokyo: Don’t have to create them but can’t prevent the peer from creating them.
Says SHOULD give at least 3 unidirectional stream credits, but probably ought to be a MUST.

Mike: We have a should on putting that in the TPs, but can also send MAX_STREAMS, which would also be perfectly functional. 
Can’t use QPACK table until you’ve opened the streams and can send

MT: I think that’s reasonable. Anyone who wastes the opportunity to create that stream is writing their own death warrant. 

Kazuho: Can I reset the stream if I see it being opened and don’t want it

Mike: In Tokyo, said you can allow it to be open, but they may never send anything

Alan: Draft says you can’t reset it 
Can we mandate that you MUST give 3 streams one way or another, or do we leave it alone

MT: If you didn’t get credit, suffer. Recommendation to provide enough credit is a good thing. 

Alan: That conflicts with Tokyo

Mike: If you’ve set the table to 0, can you require that the peer not open the stream in the first place. We said no you can’t do that, the peer can open the stream no matter what. 

MT: That’s separate from the question of if you’re hitting the stream limit and can’t create the stream. 

Alan: If you don’t have enough credit, then there’s not really any purpose in saying you must allow them to create it, since they can’t

Roberto: There is a purpose, there are other cases where it’s easy to do and just because there’s a bad case doesn’t make it useless

Kazuho: I want to see a situation where you can still use QPACK even if blocked on the stream. 

MT: Difference between not being able to send bytes on the stream because blocked vs. not being able to open the stream isn’t very big, you need to be able to handle it anyways

Alan: If you have to cope with it not working, then we don’t need text saying you must allow them to do it

Mike: But we do need to say that it’s not an error if they open the stream

Alan: What is the minimum amount of uni-stream credit that an implementation must offer

Kazuho: 0

Mike: At least 1

MT: Anyone for 2?

MT: I don’t think there’s a great answer to that question

Alan: I think there should be a MUST minimum number. 

MT: I’m okay with saying 3 as a MUST, even if people can burn them and waste them, at that point it’s their fault. 

Mike: We have SHOULD right now

MT: Must would be a fine change

Christian: The argument for 0 is that you can always send max streams after that

Roberto: I won’t argue if we want to do 3, but it’s a feel-good thing and doesn’t provide any actual guarantee. People that do stupid things are going to find that this doesn’t work so well. There’s no way that you can guarantee anything. 

Alan: I agree, but I think 3 is going to work for a lot of people.

Ekr: If there’s no QPACK stream, I can still be fine without doing QPACK. 
Is this a way for someone to say I don’t like QPACK and you shouldn’t do QPACK

Alan: You do that via settings

Roberto: If we make this a MUST, how do we observe and deal with it? 

Alan: You get the TP, max uni streams is less than 3 then you close the connection, they’re not conforming

Conclusion: You MUST give 3 as max uni streams. If they use those streams for other things then you do not have to keep granting them more credit until you get QPACK. Alan to put into issue.

## HTTP/3

### #2718: Truncated Stream Handling is Aggressive
https://github.com/quicwg/base-drafts/issues/2718 

Mike: Conversation about different forms of error handling. Argument is that current requirement is too aggressive. But I think it’s reasonable to argue that it must come to a stop in a frame. Proposal: Close with no action

Lucas: I agree

MT: So do I

Conclusion: Close with no action

### #2711: Relax prohibition on server-initiated bidirectional streams
https://github.com/quicwg/base-drafts/issues/2711 

MT: There was some confusion. I don’t think HTTP needs to say anything about what TPs say. They say that bidirectional streams from server have no meaning in this protocol and must be negotiated by extension.

Mike: Sounds good

Eric: I agree

Roberto: This means that getting a server initiated bidirectional stream doesn’t mean HTTP/3 at all? 

MT: I’d rather not do that, doing stuff without any good semantics and no signal for what they mean we’re in some scary places. If you get one and haven’t negotiated a use for them, it’s a connection error. 

David: QuicTransport is going to define how to negotiate this, but without that negotiation it should be an error

Ekr: I concur with that

Conclusion: 
“I don’t think HTTP needs to say anything about what TPs say. They say that bidirectional streams from server have no meaning in this protocol and must be negotiated by extension.”  (And unless there’s an extension negotiated, blow up if a server-initiated bidirectional stream is opened.)


### #2699: Specify handling of QUIC SERVER_BUSY connection failures
https://github.com/quicwg/base-drafts/issues/2699 

Mike: I don’t know that we need anything for server busy

Mark: This feels like a duplication of status codes for HTTP. We don’t require any behavior, the client chooses what to do. 

MT: I don’t think we need to say anything concrete, but I do wonder if we need anything from the alt-svc perspective

Mike: Doesn’t it already say that? 

MT: I didn’t think it was anything specific, will check

Mark: This is effectively an HTTP term, hop by hop behavior, we’re going to have to specify the behavior here

Martin D: In the real world where do people configure the thresholds for the server being busy. Isn’t that in the HTTP/3 server?

Mark: On the server side, yeah, then the configuration for how to handle it is on the client side. 

Martin D: We should get rid of transport level error and make it application error if people want to use this mechanism. 

_Concerned noises_

Roberto: I’m not sure if I agree with that. At the HTTP/3 layer, you can always be redirected to another end-to-end host with alt-svc. Because of reverse proxies you think it’s different, but it’s not. 

Mark: I do question why this semantic is in the transport

Kazuho: I want to send this before the handshake completes when my server is busy, but I can only send connection close and not application close

MT: Kazuho is right, nothing has happened at the application layer, the server is making that decision just by looking at those beginning packets

MT: I don’t think we need any text here. RFC 7838 section 2 says for alt-svc “if it fails or is unresponsive, client can fall back to using origin or another alternative”, so we’re already covered in this case. 
Mike: Should we specify what an intermediary returns downstream

MT: Doesn’t matter, it should do what it already would have done

Roberto: When DoS is happening, server’s gonna do what server’s gonna do. TCP RST, 5xx, etc.

Mark: Nothing has changed in HTTP/3 for that, we’re just adding one more state to that table.


### #2551, 2662: Replace MALFORMED_FRAME with specific error codes
https://github.com/quicwg/base-drafts/issues/2551 

Mike: A problem now that we have varint frame types

Ekr: We just stop communicating the frame type at all

Mike: Anything that wanted to define that a frame type was unacceptable would need to define a new error

MT: What limits does limit exceeded cover?

Mike: 
Pushed over stream ID
Prioritized stream you wouldn’t be allowed to create
2 or 3 others

Lucas: I don’t like the current design, this is better

Kazuho: I prefer not to have different error codes for each frame indicating that it’s invalid. I think we might just go with invalid frame error and bad frame size error.

Mike: That’s really a question of how detailed do we want the errors to be. Falling into bucket of bad frame size is reasonable. Do we want errors specific to each frame type where the frame type can be misused in some way. 

Kazuho: While I agree with the sentiment, we could just make a table for that instead of basically making that via error codes. 
I don’t disagree with an error code for the ones that we need to care about, but it might help to have a catch-all for invalid frame. 

Mike: In addition or instead of some of these? 

Kazuho: These are fine, but I don’t think we need cancel push, that’s a generic error

Martin T: Good point. Cancel push probably doesn’t need to be separated from other classes. What general things do we want to signal about errors? Maybe a class for prioritization, a bunch of things around push (invalid ids, duplicate push, etc.), and then a specific “you’ve got a bad frame dude” error code. That’s almost what’s here. But having groupings for areas that you can look at when trying to find the problem can be helpful. 

Ekr: These all have a string right? 
Several people: Not RST_STREAM, but all these yes, ending connecting

Ekr: These are all protocol violations of one side or another. I could live with this particular set, but I think having one for “I can’t even parse the stupid thing you sent me” which could be good. For TLS we tried to make distinctions and much of that became unclear about when to send one vs. the other but didn’t really help debugging. 
I think the ones that are most interesting are duplicate push limit exceeded, could be good to track down hard bugs in your implementation, but others are just like decode errors (bad frame size). We should use this just for ones that are non-obvious errors that come up after some time. 

Lucas: Good observations. Some of the errors are bad use of frames, logically disagreeing fields in a frame. Others are you sent this frame at the wrong time. But those are all in the same PR. The important thing is that bad frame size was in HTTP/2, but we replaced that with malformed frame as a general catch-all for “that one’s screwed up”. 

Alan: One editorial observation is that we have “bad”, “invalid”, and “malformed” we should pick one. The way our software is segmented is to return error codes when bad things happen, it may be difficult to get strings through all of that. Software is software and we can fix it. But I have slight preference. 

Conclusion: Lucas is going to take feedback on the PR. Will send email to list with all of the error codes and divide into sections and explain rationale for that segmentation. Give some principles for why they fit.

### #2516: Semantics of MAX_HEADER_LIST_SIZE
https://github.com/quicwg/base-drafts/issues/2516

Mike: We have some lack of clarity on how this comes in from HTTP/2. This is advisory on the peer’s part, so there’s not really anything that they need to do with it. What they can do: Fail immediately instead of sending a message that’s too big without sending it over the network first. Language is unclear and we don’t have agreement on how it’s supposed to work. Let’s get agreement before we write text. 

Cory: In HTTP/2, has anyone written an implementation that checks outgoing header list size against this setting? 

Alan: Yes, we do, sever sets limits and sometimes that’s exceeded and the best way to find who’s doing this so they can fix it is to detect it right away on the server side. It’s very nice to know exactly right when they’ve set it vs. trying to track it down later. 

Alan: I do send the request for other reasons, but ideally I wouldn’t.

Ian: For GQUIC we have a magic limit. We don’t communicate it, we just brutally kill the connection on you. We don’t have any way to advertise it. It would be better to have a limit so that people know where they stand. 

Cory: Without the SETTINGS frame then I have no way to know when I screwed up. 

Kazuho: We don’t advertise it, but we have an internal setting for it. 

Mike: That’s all consistent with the text currently. This is how you advertise it if you do. 

Ian: We should give a reason why SHOULD NOT

Mike: Anecdotally, even clients that have this setting will consume any size of response

Kazuho: An interesting thing about imposing this limit is that you also have a limit for compressed and uncompressed sizes. 

Lucas: Annoying is that default value is unlimited, and there’s no requirement that you ever get a SETTINGS frame. Question the value of this since it’s going to be super inconsistent.

Cory: The value is that all the implementations have this already. It’s better to discover this because there’s an advisory way to tell the other side than to have the connection die on you.

Conclusion: Say that you SHOULD NOT send message if it’s over the limit. Say why, which is that the peer might close the connection and that causes all other outstanding requests to fail.

### #2498: Behavior on out-of-range settings
https://github.com/quicwg/base-drafts/issues/2498 

QPACK and HTTP/3 interaction. QPACK defines max size for settings, HTTP/3 doesn’t have a way to say “settings out of range”. We need to define the concept and maybe an error code, even though none of them are used by HTTP/3. 

MT: You have a SETTINGS error, for you screwed something up in SETTINGS. One error to cover them all is probably enough. It’s pretty easy to eyeball when it’s going wrong.
Mentioning that implementations can restrict value space. 

Mike: Okay

### #2412: Can MAX_PUSH_ID go backward?
https://github.com/quicwg/base-drafts/issues/2412 

Flow control going down is an error, QUIC says it’s not an error ignore. QUIC can be reordered, HTTP/3 has ordering so if they come out of order then you’ve screwed up. My inclination is to keep this an error. 

MT: There’s absolutely no reason to reduce it in value, on an ordered stream. 
Christian: HTTP ERROR U R IDIOT

Mike: Okay

Conclusion: Keep it an error.

### #2410: Import rules on “malformed requests” from RFC7540
https://github.com/quicwg/base-drafts/issues/2410 

Mike: Do we want to just restate the list of ways that requests can be malformed from HTTP/2 and do it in HTTP/3

Ian: Seems like the right thing to do

Martin T: Let’s not do this piecemeal, let’s have a clear definition of a valid message, any deviation from that is a stream level error (which may turn into a connection error) of the appropriate type.

Mark: You don’t want someone reading this to think they need to buffer the entire message to determine if malformed. 

Mike: HTTP/2 has a bunch of things to say “if it does this, kill this”

Martin T: Most you can cite 7540 but there are subtle differences. Things like interleaving of headers with data frames, which we don’t in QUIC and don’t ever want to do again. 

Mark: Do our own instead of by reference

Martin T: Unless only a few exceptions, but yes

Alan: If you get data before headers that’s not in 7540. 

Martin T: You can’t open a stream with data frame so that’s not possible in 7540. That’s new in QUIC, in HTTP/2 you had to use headers frame, so we have some new problems now. 

Mike: HTTP/2 doesn’t consider it malformed if header blocks after trailers, just says no semantics. 

Conclusion: Just restate them, but carefully.

### #2697: SHOULD use PRIORITY
https://github.com/quicwg/base-drafts/issues/2697 

Mike: Do we need to say you SHOULD send priority frame, do we want to require?

Kazuho: I think we should make it very clear that when you are going to have bad performance unless you send priority frames if you’re a web browser

Martin T: There’s a distinction between the value of prioritizing responses to requests (this being very important) and the value of signalling the client’s idea of what priority of things should be. I think we can leave it much the same as in HTTP/2, let’s have the discussion later. Delivery is important and we don’t know if the signalling is important. We have browsers that don’t do any prioritization and leave it all up to the server, and so we have some servers that do nothing with it. 

Mark: We’re chartered to map HTTP/2 onto QUIC, not to second guess HTTP WG or to fix things we don’t like for HTTP/2

Roberto: This is unenforceable if we say MUST for this in the text

Conclusion: Leave it alone (for now)

### #2502/2690: Priority inversion from reordering
https://github.com/quicwg/base-drafts/issues/2502 

Mike: Streams can arrive before you know priority. As we currently have it it becomes a child of the root, so one of the most important things on the tree, and then you find out it wasn’t super important. The proposal here is to make a holding pen that is lower priority than everything else and if it shows up early it gets to be lowest instead of highest priority. 

Kazuho: This is very conservative, but guarantees that it’s no worse than HTTP/2, so very good properties to have. 

Martin T: Addresses in minimum possible way, quite nice, degrades to HTTP/2 in the presence of packet loss and reordering. And if you’ve got nothing else going on then everything just goes through and you’re fine. 

Ian: I find this appalling and a total bummer. And where we’re at this is a reasonable fix and better than the status quo. My first impulse is that this is very concerning, but yeah what are we going to do. 

Mike: On a separate issue that this was filed recently, if you don’t have bad effects from having an unprioritized stream show up, we can back out a bunch of our deviations from HTTP/2 and put priorities on control stream (bring back exclusive prioritization). 

MT: Priorities on request stream is abomination and this allows us to get rid of that

Mark: Lots of nodding heads

Alan: The tree is now a DAG, everything points at this child?

Mike: This becomes a placeholder that depends on the root with 0/1 weight and if you don’t know the priority of something it’s a child of that placeholder. 

Alan: Just trying to think about how we do this in our code, but we can make it work.

Ian: I wanted to add that I would like this to happen in short sequence with restoration of exclusive prioritization and take it off of the request stream. 

Mike: Yup

Christian: Is there support for never ending streams.

Martin T: 2^62-1 octets on it

Christian: How does that fit in the priority tree

Mike: If you have a never ending stream and you always have data to send on that stream, anything that is a child will never get bandwidth 

Christian: So if I have WebEx or a movie playing, and I’m browsing on the side, then children of the video are screwed? 

Martin T: You choose where to put them, so don’t put them as children there. If you want it higher/lower than the movie you can do either. 

Christian: If I put it in the tree, then it means finish that branch before moving to the next branch. 

Martin T: 7540 explains that the parent gets done before the children, and children all get done at the same time with some weighting between them. 

Christian: So round robin on the children. 

Martin T: Effectively, yes. But don’t need a tree with lots of children at the same time, so just make a deep chain of children. 

Conclusion: Enthusiastically go for it and change the associated things quickly too. “Make a holding pen that is lower priority than everything else and if it shows up early it gets to be lowest instead of highest priority.” 

### #2678: Use unidirectional streams for everything!
https://github.com/quicwg/base-drafts/issues/2678 

Mike: No technical reason to avoid this, but maybe timing reason to not do this. 

Ian: If we did something like this, I’d like some requirements that try to restrict the number of open streams since those cost memory. Technically there’s head of line blocking, but the benefit here seems marginal. 

Martin T: Wanted to make sure this was discussed, if there’s ever a chance that these would block, then needs own stream, but we looked at each one and none of them should block. 

Mark: Schedule is important but if it’s the right thing to do, then we should do it. But it’s not clear that this is the right thing to do. 

Martin T: There’s no strong reason to do this, and there’s some economy in putting all the common, small things together. 

Conclusion: Close with no action. 


### #2526: PUSH_ID frame
https://github.com/quicwg/base-drafts/issues/2526 

Mike: Settings and priority are frames that can only be first frame, we can make PUSH_ID frame.

Lucas: Opened and okay to close with no action.

Conclusion: Okay to close with no action.

### #2632: Symmetric GOAWAY
https://github.com/quicwg/base-drafts/issues/2632

Mike: Don’t know which of extension-defined things have been processed when you got a GOAWAY. 
Should we expand goaway to cover unidirectional streams and/or allow clients to send them or do we want extensions to define their own way to shutdown. 

Alan: I’m pretty sure HTTP/2 allows clients to send GOAWAY. Did we have a good reason to remove that? 
People who want to do bidirectional extensions will now need to do it again which is annoying. 

Kazuho: I think my weak preference goes to moving GOAWAY to transport. For HTTP/2 with an HTTP/2 level error you could indicate the stream ID that was processed. That’s lost in QUIC. 

Ian: Martin T made a great argument about why it should be the design that it is today. I think that argument holds, but either I think we keep the same or make both directions and move to transport. 

Martin T: We’d have to understand all the extensions in order to know the right way to shut them down. We have this right now because our atomic unit is requests and everything we know about requests. We draw a line in the sand and say “we’re going to complete these and throw everything after that away”. Unidirectional streams and not directly covered, but are covered transitively, since push associated with request can be done still, but the request is the unit for the line in the sand. 

(See Martin’s comment on 2632, the long one)

For exchanges where you’ve got multiple streams and messages, etc. we don’t know what that’s going to look like and so we shouldn’t be trying to define this for that because we don’t know the unit of work that they’re going to stop processing. 
HTTP/3 can say how it shuts down, but we can’t say it for others. 

Jana: I want to push back on making this a transport signal, there’s a nice line that you can draw for HTTP where things after a particular request can go on a new connection, but you can’t draw that line for others like WebRTC.
I like the idea of doing this as bidirectional so a client can say goaway to a pushy server. 

Roberto: If QUIC streams are akin to TCP connections (and let’s face it they are in some ways). Refusing streams and refusing TCP connections are the same. Providing a new signal that you’re not going to accept new streams in any context is valid and reasonable. HTTP can choose to interpret it in the context of requests, but that doesn’t mean that others need to do it. 

Kazuho: You could change it to a blob and then define the semantics of the blob in the HTTP protocol but have it go via the transport. 

Jana: How does that translate from application to transport. 

Kazuho: Application defines content of the blob, but everyone has a blob. I don’t know that it’s super important for us.

Mark: Is anyone willing to write up a proposal of how to do this in transport? _No_

Christian: It’s trivial, special-case a CONNECTION_CLOSE error code, and… _starts to explain and then cut off_

Alan: I’m advocating that we support this because it helps bidirectional, you should also be able to say “I’m going away, no more pushes”. Saying I’m not going to accept any more pushes, that’s a valid HTTP/3 use case for a client sending a GOAWAY.

Lucas: The thing about GOAWAY is it’s two things, you want to tell the other side to stop making new things and you want to also tell it what was done and what is safe to retry elsewhere. Maybe we need both or one? We could break it into two things. But maybe you need the atomic GOAWAY behavior. I might be interested in writing the PR at the application level to see how it could work. 

Martin T: The reason the client doesn’t need to send the GOAWAY is that it’s the one doing the creating. 

Others: But what about pushes. 

Mark: We need to port HTTP/2 not reinvent

Alan: HTTP/2 had this

Martin T: We’ve used the stream ID to refer to requests in HTTP/3 for a lot of reasons, but we have to remember that it’s the request that is important here. If the client wants the server to stop sending pushes it can stop giving access to pushes and it can reset the ones that it couldn’t stop. 

Jana: You can only stop after an RTT

Alan: Seems like a lot of work when you could just send a GOAWAY and we already have that in HTTP/2

Roberto: I would propose that we table any discussion about moving this to the transport, although I am interested, I think that’s a much larger discussion. If we decide we want something there maybe we have it in both. Let’s move forward. 
GOAWAY says what you haven’t processed, not what you have

Cory: Client goaway can indeed be simulated, but that asymmetry is profoundly annoying, it’s so much easier to have it be the same on both sides, it works the same way, when you’re trying to implement a stack

Kazuho: I disagree, the stream ID is important because idempotent requests and need to know about that. Push responses are expected to be cacheable.

Martin T: I don’t think there’s agreement about what it means to send a GOAWAY from a client, even in HTTP/2. My understanding is that a push is part of answering a request and if the client says GOAWAY then that’s fine. We need to get clarity about what it means in HTTP/2. I think we’ll come back to the same place if we start digging. 

Mark: If I’m an HTTP/2 server and I get a GOAWAY from a client and my forward connection is HTTP/3, what do I do? Nothing? Could be good to have a mapping.

Mike: Anything being pushed is that it’s dependent on the stream where it was promised. The client either knows all the streams and can cancel the pushes or the server knows and won’t deliver. 

Alan: If the server has the original request before it has the push data. 

Mike: If it doesn’t, it doesn’t matter if it starts using the empty pipe. 

Mark: Can we move forward by parking this and asking HTTP WG what it means to send from client. 

Conclusion: HTTP/2 semantics must be defined by HTTP WG. We define how to carry that semantic.

### #2488: Embed address validation token in Alt-Svc
https://github.com/quicwg/base-drafts/issues/2488

Mike: You could save a roundtrip by putting token in there as well as VN. 
If this were a separate Alt-Svc extension then you might need to list as one with- and one without in case the client doesn’t support it. 

Martin T: Extension.

Mark: Thumbs and nodding in the room. 

Conclusion: Close with no action, ask issue author to write extension.

### #2439: http:// URIs over HTTP/3
https://github.com/quicwg/base-drafts/issues/2439

Mike: We don’t define in HTTP/3 whether you need to ask the server before sending it http:// or do we say this is a new protocol let’s get it right this time. 

Ekr: This is back to 2014 when we had this argument about HTTP/2

Mark: We’re building a new protocol, but the software behind that protocol may not understand the requirements 

Kazuho: The same

Ekr: Sadly, same

Martin T: We should not say anything about just doing https://

Mark: But words need to be written

Conclusion: Keep the requirement from 8164, don’t change anything


### #2223: Coalescing rules
https://github.com/quicwg/base-drafts/issues/2223

Mike: I think that this is pending text in httpbis about how to decide what to use for a given URL. Right now if you have Alt-Svc then use it. That doesn’t mirror HTTP/2’s look at the cert policy. 

Conclusion: Wait for HTTP WG to write text that’s standard across all HTTP versions. Mike to link to the issue in http-core.


### #253: HTTP/3 without Alt-Svc
https://github.com/quicwg/base-drafts/issues/253

Mike: Want some text somewhere we can reference that says this.

Conclusion: Wait for HTTP WG to write some text we can reference.


## QUIC Firewalls

Jana

Went digging to find out what the world currently does. A bunch of people identify and block QUIC, some deeper, some just by UDP 443. 

Lars: Proposal to rename QUIC to Firepower Threat

Jana: If you know people at these places, please talk to them, help to educate them, try to find out what they’re doing and what’s likely to ossify. 

Ian: People offer a bunch of different stuff, like things to say “this is bad for my employees, make them stop”. Some of them are pretty adverse to reading IETF specs. The applicability or management doc might be shorter and easier for them. A lot of people are saying “how do I get SNI out of this packet?”.

Ekr: A bunch of them are forcing back to TLS since they don’t know how to deal with QUIC yet
Ian: Also zero-rating is happening a bit

Ekr: I think the best thing would be to give a set of rules about how to do it, give them the non-ossifying way to identify it. 
I don’t love having that property, but I think it’s better to avoid a war there. 
Kazuho: You talked about middleboxes that have a way of detecting protocols and blocking them. That’s known. Are there any that detect version numbers of other protocols? 

Ian: There’s one fairly popular antivirus that works with GQUIC 46 but all other versions are blocked. Version 46 is the one that starts using the QUIC bit. Theory is they read the spec and decided to look at that and drop everything else. 10% of Windows traffic gets blocked. 

Martin D: The invariants seems like the right draft. 
David: Would it make sense to have a Wiki page that’s easier for people to read.

Eric: It would be better to give a real way to block that doesn’t ossify rather than let them figure it out. 

Jana: Would it be worth doing a wiki page? Second question: It would be good to put in manageability as well? We should be aware of what’s happening and keep our eyes open. 

Mark: If we create a resource that gives information, we have the ability to mold their perceptions, especially if that comes up high in search results. 

Martin T: Has anyone actually read the applicability and manageability since there’s a good way to 

Sean: About a year and a half ago, I talked to some folks and it makes me think that there are products because people asked for them. If there’s any way we could note down specifics about how QUIC isn’t part of the “UDP cesspool”, we should write those up to combat the FUD.

Kazuho: People are likely to assume semantics about invariants especially the version field, if we’re going to add some anti-ossification measures there it’s painful. 

Ekr: We have gotten some benefit from people being able to identify QUIC, papers and metrics about QUIC levels, etc. It’s valuable to help people find what’s in the packets. We can also explain how it’s not a great idea to be blocking some things. Talked to Cisco firewall people, the people that are easiest are Cisco and Symmentac. 

Mike: I wanted to respond to Sean’s comment about FUD where QUIC looks like attack traffic. QUIC does look like attack traffic. Internally, we will filter out traffic that looks like stuff the endpoint doesn’t want to receive. In some cases, people want to identify QUIC to let QUIC through but still block attack traffic. 

Lars: People have infrastructure implemented to get visibility into TLS over TCP, when they don’t have that for QUIC blocking QUIC can force a fallback. The argument can be made that if we think QUIC is more secure then this is kind of not great. 
There’s a desire to lose that visibility from TLS over TCP so it’s not just QUIC’s fault. But a lot of this goes back to the larger encryption argument that’s been going on for a long time. 

Rui: As a WG we pretty much have the tools and specifications for detecting QUIC. The alternative for people is to block it if they don’t understand what it is, but most of us will fall back to TCP most of the time. I don’t know what else we can do about what QUIC is and how we can deal with it. 

Martin D: I want to clarify the outreach need. There are two things: is it good to block QUIC? Harder to convince people since that’s up to their end customers. The purpose of outreach for these vendors is to get them to do it intelligently, not whether or not they choose to do it. 

Jana: Thank you for the discussion, that’s super helpful because it leads me to the last thing: If you know people at these places please send me information and I’m happy to work on building this list and reach out to them. If you have contacts send them along or if you know of more products. 

Gorry: This room seems to contain a flavor of that discussion, which isn’t what I see when I talk to enterprises that want to secure their networks. The people who deal with enterprise security and securing their networks have a different perspective. Maybe we need to talk to their end customers, not just the people making the boxes that people buy. 


## HTTP/3 Priorities
Ian Swett

Mark: HTTP WG is the one who defines this, we’re just mapping onto QUIC. However, we are aware of some of the pain here, this is hopefully the start of a conversation that will interest people here, and will probably go to HTTP WG.

Ian: This is me channelling what I’ve heard from people unhappy with the status quo. 
Chrome had HTTP/2 priorities, didn’t see any difference, now disables them by default. 

_Walk through HTTP/2, HTTP/3 status quo, in slides_

PR #2700: 
Removes streams depending on streams, adds 1 byte exclusive priority to replace that functionality
When you have a giant list, you just flatten it, this is very similar to Patrick Meenan’s proposal + HTTP/3 placeholders. It’s also a variant of Osama Mazahir’s 2014 proposal 

_links in slides to earlier proposals_

Appears that the two short term issues here are going to be solved already, but I do think it’s worth going into the larger conversation here. 

What are we trying to get out of priority? Faster page load time? 
Fair sharing in CDN to origin? Is anyone using that? 
Do we need to preserve HTTP/2? Something else?


Cory: HTTP/2 priority is optional, frame parsing is mandatory, but many servers just ignore it. 

Ian: Default round robin is a problem and gets worse via HTTP/3. We have a short term solution. 

Roberto: We could solve this by mandating at least “n” placeholders. 
Ian: Yeah, we need to decide if we’re going to solve, but that’s in the issue.

Ian: How do we get something that we think will get wide adoption?
Could be valuable if you do it right. This could have as much impact as all of QUIC if done right, so we should really try to make it happen. Best practices could go in the HTTP/3 doc. Priorities as an extension could make HTTP/3 slower than HTTP/2 and that would be a bummer. How do we get the buy-in that we need? 

Patrick Meenan’s numbers show only 25% of major CDNs have full HTTP/2 compliance. 

Kazuho: I don’t think HTTP/3 will be slower, since if you have it off for HTTP/2 then you don’t need it for HTTP/3 to get comparable performance. 

_continue with slides: Allow server side input_

Server push really benefits from initial priority.

Roberto: Trying to expose IDs to JS is probably bad. Child of relationships are probably more manageable. 

Kazuho: Are we expecting push to be supported in HTTP/3 browsers?

Ian: Chrome will implement but we don’t know if it will be enabled, we are proceeding with implementation. 

Ian: It would be nice to have priorities in the transport. There are a lot of non-HTTP/3 applications that could benefit from priorities, but what we have now is probably too complicated. 

Jana: We did discuss this exact thing a while ago. We decided to not do priorities in transport, we didn’t want to bake in one understanding to the transport, every application will have it’s own interpretation of priorities and that is still true. 

Roberto: When you don’t have priorities at transport, you get a bad sharing problem on transports, so you’ll need to have some kind of sharing system. 

Christian: You can have two definitions of priorities at the transport. One is local API for what the user of the API wants to have be the order that things should be treated. Or you have something that’s how it’s treated on the wire. I don’t think we need the latter. 

Kazuho: Stream level prioritization among multiple connections could be a reason to need this. 

Christian: That has such a big attack surface we probably wouldn’t want to do it. 

Victor: Seconding Roberto, whenever you have a transport you get a writeable event and you have to decide what to write and that means that you’ve got a priority scheme whether you wanted it or not. 

Ekr: HTTP/2 priorities are for the client to communicate with the server. If you just want to control that locally, then you don’t need it. I don’t see any reason that WebRTC would need to communicate that over the wire. 

Ian: They would like a semi-standard framework to plug their scheme in unilaterally, not that they need to do it over the wire. 

Victor: When you decide priorities you also should be prioritizing retransmissions. 

Kazuho: Thanks for the presentation Ian. I have mixed feelings here, for many deployments people don’t do this on HTTP/2. I do think that making it easier might be good. However, having a different scheme means that it HTTP/2 won’t get improvements. But this is going away from porting the semantics of HTTP/2 to HTTP/3. 
If we are going to have something different, it needs to be really really simple so we can agree immediately. 
Or ship HTTP/3 as is and then define this as an extension for both HTTP/2 and HTTP/3. 

Victor: What’s HTTP/2 semantics?

Mark: We need to talk to HTTP WG. The process we’re doing right now is also how we got to HTTP/2 priorities, so we need to see what will get this to be different.

_See list of important questions at the end of the slides_

Ian: Who would be willing to work on this? 

_A few hands wave around_

Ian: What data would be useful? 

Kazuho: We could get some implementations to run and test

Mark: +1 for running code

Roberto: If the APIs aren’t there, it won’t be used in any of the ways that you think are exercising the surface. 

David: To Mark’s point about running code, we don’t really have running code in the spec either. I know there are charter questions, we could say that this moves to another draft and that makes it easier for people to deploy multiple priority schemes at the same time. 

Eric: At the same time, having something not deployed isn’t fixed by splitting to multiple things. 

Ian: Connection tests via Chrome Incognito to Alexa top 10. 

