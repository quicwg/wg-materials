# QUIC Working Group Minutes - IETF105 Montreal

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Tuesday, 23 July, 2019](#tuesday-23-july-2019)
  - [Hackathon / Interop Report](#hackathon--interop-report)
  - [Issue Discussion](#issue-discussion)
    - [https://github.com/quicwg/base-drafts/issues/2792 (Marten Seeman assigned to Sean Turner)](#httpsgithubcomquicwgbase-draftsissues2792-marten-seeman-assigned-to-sean-turner)
    - [https://github.com/quicwg/base-drafts/issues/2670 (Nick Banks issue, Martin Thomsom presenting)](#httpsgithubcomquicwgbase-draftsissues2670-nick-banks-issue-martin-thomsom-presenting)
    - [https://github.com/quicwg/base-drafts/issues/2844](#httpsgithubcomquicwgbase-draftsissues2844)
    - [https://github.com/quicwg/base-drafts/issues/2863](#httpsgithubcomquicwgbase-draftsissues2863)
    - [https://github.com/quicwg/base-drafts/issues/2763](#httpsgithubcomquicwgbase-draftsissues2763)
    - [https://github.com/quicwg/base-drafts/issues/2834](#httpsgithubcomquicwgbase-draftsissues2834)
    - [https://github.com/quicwg/base-drafts/issues/2770](#httpsgithubcomquicwgbase-draftsissues2770)
    - [https://github.com/quicwg/base-drafts/issues/2785](#httpsgithubcomquicwgbase-draftsissues2785)
    - [https://github.com/quicwg/base-drafts/issues/2741](#httpsgithubcomquicwgbase-draftsissues2741)
    - [https://github.com/quicwg/base-drafts/issues/2534](#httpsgithubcomquicwgbase-draftsissues2534)
    - [https://github.com/quicwg/base-drafts/issues/2656](#httpsgithubcomquicwgbase-draftsissues2656)
    - [https://github.com/quicwg/base-drafts/issues/2496](#httpsgithubcomquicwgbase-draftsissues2496)
    - [https://github.com/quicwg/base-drafts/issues/2084](#httpsgithubcomquicwgbase-draftsissues2084)
    - [https://github.com/quicwg/base-drafts/issues/2170](#httpsgithubcomquicwgbase-draftsissues2170)
    - [https://github.com/quicwg/base-drafts/issues/2143](#httpsgithubcomquicwgbase-draftsissues2143)
    - [https://github.com/quicwg/base-drafts/issues/2388](#httpsgithubcomquicwgbase-draftsissues2388)
    - [https://github.com/quicwg/base-drafts/issues/2387](#httpsgithubcomquicwgbase-draftsissues2387)
    - [https://github.com/quicwg/base-drafts/issues/2205](#httpsgithubcomquicwgbase-draftsissues2205)
    - [https://github.com/quicwg/base-drafts/issues/2342](#httpsgithubcomquicwgbase-draftsissues2342)
    - [https://github.com/quicwg/base-drafts/issues/2389](#httpsgithubcomquicwgbase-draftsissues2389)
    - [https://github.com/quicwg/base-drafts/issues/2602](#httpsgithubcomquicwgbase-draftsissues2602)
  - [AOB Tuesday](#aob-tuesday)
- [Wednesday, 24 July, 2019](#wednesday-24-july-2019)
  - [Issue Discussion](#issue-discussion-1)
    - [#2844 Client Connection IDs are Broken](#2844-client-connection-ids-are-broken)
    - [#2863 Unrecoverable loss patterns lead to deadlock](#2863-unrecoverable-loss-patterns-lead-to-deadlock)
    - [#2496 QUIC Version Ossification](#2496-quic-version-ossification)
  - [H3 Priorities](#h3-priorities)
  - [Recovery and HTTP Issues](#recovery-and-http-issues)
    - [#2789 Use a higher speed RTT for new paths](#2789-use-a-higher-speed-rtt-for-new-paths)
    - [#2630 Define under-utiliation of cwnd](#2630-define-under-utiliation-of-cwnd)
    - [#2555 Define idle period for congestion period](#2555-define-idle-period-for-congestion-period)
    - [#2534 ECT text disables ECN too aggressively](#2534-ect-text-disables-ecn-too-aggressively)
    - [#2923 Min_RTT management](#2923-min_rtt-management)
    - [#2632 H# GOAWAY should be symmetric and cover bidi and uni streams](#2632-h-goaway-should-be-symmetric-and-cover-bidi-and-uni-streams)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->



## Tuesday, 23 July, 2019

 
New Wiki for related work: https://github.com/quicwg/base-drafts/wiki/Related-Activities

Please add your side projects here to share with the working group in a central location.
 
### Hackathon / Interop Report
 
Lars Eggert: 19 implementations participated in interop Saturday-Sunday during the hackathon. There are a few blank columns and rows in the Interop spreadsheet because -22 dropped close to the interop.

Still lacking implementation of some very basic features; e.g. key update, migration. Not where we thought we were. 
 
Lars Eggert: Jana and Marten have created an ns3 environment for repeatable recovery testing. Robin Marx added visualization of logs. 

Allows for better congestion control testing, and initial tests show expected patterns.
 
Emile Stephan: Lot of work on spin bit during the hackathon. Measuring packet loss, etc.
 
Mark Nottingham: Physical interops versus virtual interops: which is more effective?
 
Lars Eggert: In NA timezones the virtual interops work quite well, less useful otherwise. Do we want to reduce frequency of the physical ones, since they are costly? Given results, not sure we should.
 
Eric Kinnear: virtual interops are great, intermediate deadlines clock the work. Face to face time is also very useful. We finished issues we wouldn't have otherwise found. 
 
David Schinazi: +1 lots of value in both. Magic deadlines are forcing functions. In-person meetings, London first time that the interop was more useful than issues, spending more time on interop would be good. 
 
Lar Eggerts: Interops are also easier to host.
 
Kazuho Oku: Keep in-person interops, difficult for people in Asia to attend virtuals.
 
Eric Kinnear: Useful to discover issues and spend evening fixing. Less than two days not good.
 
Lucas Pardue: Two days in physical interop also useful as representatives are often channeling remote teams sometimes in other timezones, can come back with fixes next day.
 
Mark Nottingham: Looking for space for an interop/interim in September/October, looking at week of 7 October. If you have suitable space, please do come to us. Hopefully one of our current potential sites will work out.
 
 
 
### Issue Discussion
 
Project board at https://github.com/quicwg/base-drafts/projects/5 -- looking at design issues today. Issues were assigned during London interim, a lot of these are still open. Today we will discuss newer issues and assign people to address them. For issues with owners, questions: have you made progress? do we need a new owner? 
 
Lars Eggert: If this keeps up we will start closing these with no action. We will do new stuff when we have issues under control. They are not currently under control.
 
Mark Nottingham: We can't keep doing this for another year or two.
 
#### https://github.com/quicwg/base-drafts/issues/2792 (Marten Seeman assigned to Sean Turner)
 
Martin Thomson: I have thought about this a alittle. It is hard. Not sure it's worth addressing beyond a little text. Want a little time to think about it
 
ekr: not sure I understand the issue. 
 
Martin: Problem limited to you learn when a key update happens
 
ekr: countermeasure is precompute next key.
 
Martin: as said, don't think it's worth doing much here.
 
ekr: *unintelligible*
 
Ian: +1 to Martin. Can write something in security considerations if we understand it better.
 
Mark Nottingham: keep it open? Martin, can we close?
 
Martin: Security Considerations text, if that. If Sean or Marten have ideas, good. Don't want to block on this.
 
Mark Nottingham: More than text?
 
Jana Iyengar: mark as something other than design?
 
Lars: send a PR or we close? 
 
Mark: Will this come up again at WGLC, if not close issue.
 
Marten: This is a timing side channel, we need to resolve it
 
ekr: can you explain it please? what information does the attacker learn?
 
Marten: same as *packet number*?
 
Martin: In the case of a key phase bitflip, the next step takes nonconstant time.
 
ekr: The attacker learns what?
 
Martin: That the keyphase bit changed -> value of keyphase. Let's deal with it offline.
 
Lars: Deassigning Sean, assigning to Marten Seemann.
 
Mark: Outcome is security considerations text, not a protocol change?
 
Marten: Think so.
 
#### https://github.com/quicwg/base-drafts/issues/2670 (Nick Banks issue, Martin Thomsom presenting)
 
Slides at: https://datatracker.ietf.org/meeting/105/materials/slides-105-quic-acknowledgment-delay-scaling-00.pdf
 
Options are:
    A. Don't scale at all
    B. Shift
    C. Multiply
    
Roberto: Multiplying is the most error prone
 
Martin Thomson: No strongly Asking for a hum for least favorite. 
 
Ted: Use another alternate decision process: pick someone and make them decide. 
 
Martin: My reading is A is much less preferred. 
 
Ted: This is predicated that anyone can handle any of them. 
 
Christian: Option A will increase overhead. Don't know how much. But we have been driven by reducing overhead. If A is much worse, then binary decision between B and C.
 
Gorry: I do care about overhead, has anyone measured it?
 
Andrew McGregor: we are communicating useless precision in A.
 
Mark: hum A versus B/C. Who prefers A, no scaling? *extremely weak hum*
 
Mark: hum for B/C, some form of scaling? *strong hum*
 
Martin: *pedantry*
 
Mark: Pedantry noted
 
Mark: Hum for option B, exponential *hum*
 
Mark: Hum for option C, multiplicative *hum*
 
Brian: Coin flip?
 
Ian: One of these is already in the document and all the implementations.
 
Martin Duke: Reducing churn is good. My preference for B is to not move stuff.
 
Mark: Close with no action?
 
Jana: Milliseconds to microseconds is *1000, not <<10. 
 
Kazuho: agree with Jana, OTOH, either of these reduces to A with scaling 1. 
 
Christian: If the point is ms->us conversion, you can deduce multiplication from shift. 
 
Marten: why use a shift? to save bytes. this is a value you send once.
 
Lars: you also have to store it and apply the value to the one in the ack frame.
 
David Schinazi: transport is late stage, my understanding is that something with no WG consensus we close with no action. why are we still here?
 
Mark: That's for opening issues. Seems like some people still have strong feelings. 
 
Lars: Rerun hum.
 
Roberto: Any result is better than still talking about it. If you choose 0 with option C, you have problems. For B it just works.
 
ekr: C', C except value is multiplier-1.
 
Mark: exponential, please hum now *big hum*
 
Mark: multiplicative, please hum now *small hum*
 
Mark: Clear hum for B, exponential.
 
#### https://github.com/quicwg/base-drafts/issues/2844
 
David: Problem is CCIDs don't do what they're supposed to. Server can decided to decide to use 0-len connection ID even when it can't multiples, but then nat rebindings and migration are impossible. Propose to say (in 2851) that you can use 0-len when you can multiplex without CID. 
 
Martin: I think David's solution is correct. Using information you control to get packets to you is good. Source-address based routing is bad.
 
Mark: Problems with this proposal?
 
Igor: What about two machines that know they're not NATted just not using CIDs?
 
David: are there multiple clients talking to same client on same port? that breaks migration. I think that adds a bunch of complexity for a rare use case.
 
ekr: Substantial deviation from our earlier decision that one could build a server that had same connection semantics as TCP. *unintelligible*
 
Martin: to use source address they need to know that sll clients are not natted
 
Ian: *missing*
 
Tommy: maybe one solution, specify that server can have zero length if migration explicitly disabled
 
Eric Kinnear: disable migration will become disable active migration
 
ekr: tcp has semantics.... *but this room doesn't have acoustics*
 
Brian Trammell: Would support a slight change to this PR that says if you want TCP semantics (5-tuple routing), great, you will get TCP guarantees. Need a warning. 
 
Roberto: The application stacks will always need timeouts and reconnects, so the case of NAT rebinding will break connections with 0-length CIDs, and that's OK. This seems more editorial.
 
David: The reason we have client CIDs is for multiplexing on local source port. That's the only use case. That doesn't work in the current spec because I don't know if the server is using these TCP-like semantics.
 
Martin: ekr's point is really good and mostly convincing. If you want TCP semantics, you get TCP guarantees. This is an unilateral decision in a two-party protocol.
 
Mark: Can this decision be made by the application mapped onto QUIC?
 
Martin: You can have server-server scenarios where this makes sense. As a browser not sure I want the server making that decision on my behalf.
 
Roberto: prefer to close with no actions
 
Igor: *missing*
 
Kazuho: +1 to David. Really hard to have one implementation that does both client and server
 
Tommy: Another way to do this is to take this PR and put it in the applicability draft
 
David: It is a property of the server to use either QUIC CID or TCP semantics. Do we want the server to want to make that decision? You can't negotiate this, so the server needs to be unilateral here.
 
Andrew: What about s/MUST NOT/SHOULD NOT/ -- achieves the same thing as current wording, warns about consequences.
 
Martin: Good improvement, doesn't fix unilateralness. 
 
David: MUST allows us to remove a bunch of text further down. 
 
ekr: inherent restriction of TCP: can't have two connections with same 5-tuple. Should we require all QUIC servers to support CID semantics? 
 
Martin: change that andrew proposes perhaps sufficient. It's not applications so much as deployments, deployments can make this decision themselves.
 
David: Moving this to a SHOULD NOT and adding "here's what will break if you do" text, would be acceptable.
 
Kazuho: MUST UNLESS?
 
ekr: *missing*
 
Lars: can we come back to this tomorrow?
 
David: will update PR.
 
 
#### https://github.com/quicwg/base-drafts/issues/2863

Ian: Punting until tomorrow, discussion ongoing
 
 
#### https://github.com/quicwg/base-drafts/issues/2763

PR already merged for this, proposal to remove one paragraph. will do this using the normal process.
 
#### https://github.com/quicwg/base-drafts/issues/2834

Long Header Packets and Routing Conn IDs
 
Nick Banks: Kazuho came up with a solution with the long header source, we don't need to keep this open anymore. Happy to close with no action.
 
#### https://github.com/quicwg/base-drafts/issues/2770

Ian: Come back to this tomorrow, please read the PR (#2869)
 
#### https://github.com/quicwg/base-drafts/issues/2785

David: Current spec sets stateless reset token per connection ID.
One of the interops saw an implementation using all zeros for all of their
stateless reset tokens. Reusing tokens is bad and loses security properties.
Rather than having a caveat, just say they MUST be different.
 
Martin: It's not necessarily losing them, it's about additional steps you need
to take. If you have two CIDs with the same token, you need to always remember both.
 
David: Question to the group is if we want to simplify things.
 
Kazuho: I think we should disallow reuse since this is more complex for the receiver
to maintain use counters on reset tokens.
 
Martin: We will be then adding a requirement for uniqueness (probabilistically), and allow
generating a protocol violation (not require) if a duplicate is detected.
 
Mike: How about requiring a violation if they're outstanding at the same time?
 
Martin: Almost with you, but I don't think so; there are edge cases.
 
Martin: Will write text
 
#### https://github.com/quicwg/base-drafts/issues/2741

ekr: Punt to tomorrow
 
#### https://github.com/quicwg/base-drafts/issues/2534

Jana: PR written, has comments, it's on me to fix this week.
 
#### https://github.com/quicwg/base-drafts/issues/2656

Jana: This one should be marked editorial, clarification needs to be added. A sentence or so. 
 
Mark: Anyone who isn't OK with marking editorial, please raise it now.
 
Martin: Need to look, will wait for PR.
 
#### https://github.com/quicwg/base-drafts/issues/2496

Version Ossificaton. Punt to tomorrow? yep.
 
 
#### https://github.com/quicwg/base-drafts/issues/2084

ekr: I will write text. Now.
 
#### https://github.com/quicwg/base-drafts/issues/2170

ekr: Close please
 
 
#### https://github.com/quicwg/base-drafts/issues/2143

Eric Kinnear: Sent a PR (2925) for this, lots of discussion.
We should have a threat model for what attackers can and can't do. This just lists what can happen, but is not new information.
 
On-path attackers can mess you up completely (that's expected). Specifically for migration, if you're on path for both paths, you can prevent migration. But you cannot prevent migration to another path.
 
Off-path can race packets, and can potentially beat your path to the server. In the worst possible (very rare/hard) case, the off-path attacker can become limited-on-path.
 
ekr: We may want to clarify the terminology to be more standard
 
Off-path cannot cause migration to fail or cause a connection to close.
 
Mark: Let people have a chance to read through it, try to get consensus.
 
#### https://github.com/quicwg/base-drafts/issues/2388

Martin: there is a PR for this (2880), feedback please. There was a request to do this for HTTP, which has both connection and stream scoping, so it'll have more text.
 
Mark: PR is two weeks old. Proposal ready?
 
Martin: Yep.
 
#### https://github.com/quicwg/base-drafts/issues/2387

ekr/Eric: The PR (2925) mostly covers this, but needs to be filled in by ekr.
 
ekr: Will finish this up.
 
#### https://github.com/quicwg/base-drafts/issues/2205

Ian: close with no action?
 
Martin: is this not the ECN problem?
 
Ian: conclusion was no design change, document ECN issue?
 
Martin: IIRC there is an encouragement to increase value for e.g. devices that ack single packets
 
Martin: what was useful was airing this and seeing Gorry nod.
 
Mark: will we have a proposal?
 
Jana: yes
 
#### https://github.com/quicwg/base-drafts/issues/2342

Spoofed connection migration
 
Eric: PR ready to go.
 
Igor: will add some more clarification, editorial.
 
Eric: questions raised about whether or not we should have a TP here. if it exists, we need editorial text about it.
 
Mark: Ready to go in terms of consensus.
 
#### https://github.com/quicwg/base-drafts/issues/2389

disable_migration
 
Eric: Same PR.
 
 
#### https://github.com/quicwg/base-drafts/issues/2602

Ian: will write a PR by tomorrow.
 
Mark: We're done with the design/late-stage list, yay us. Tomorrow we'll discuss getting recovery/HTTP into late-stage process. We'll come up with a runlist for tomorrow, 
 
### AOB Tuesday

Brian: Regarding applicability and manageability, we have a handful of issues, and we'll be soliciting help on writing text for these issues. Please volunteer!
 
Eric: We should give the quic-lb draft some airtime here, as well
 
Martin D: Reminder that that draft has not been adopted; I think it's important that it's an adopted document.
 
Mark: Interim and/or Singapore
 
Lars: Might need a tiny recharter.
 
Roberto: Worried that we'll start discussing WebRTC before other v2 features; getting v2 chartered first is a really good idea.
 
## Wednesday, 24 July, 2019


### Issue Discussion


#### #2844 Client Connection IDs are Broken

David Schinazi: Addressed comments in the PR. Asking for review. 

Ekr: Will review

#### #2863 Unrecoverable loss patterns lead to deadlock

Ekr: Gotten less clear in the past day. David may need to open up the DT.

David Schinazi: Negative progress.  Will discuss with the DT participants and figure out way forward. Unarchived Slack channel and will arrange meeting with to discuss next steps.

MT: Cluster of issues around this one. We'll bucket them here. Can't do anything in the meeting now. Should have an update by the interim.

Jana (meta): want to make sure we get to the recovey issues.

Mark: ACK

#### #2496 QUIC Version Ossification

Martin Duke: Not convinced that "have server provide an alternative VN" is viable.

Ekr: Attackers can strip out versions they don't like and we land at an equilibrium, or fall back to TCP.

Martin: Any model will require support from some critical mass of clients and servers to encourage folks to not ossify.

Roberto: *missed*

Gorry: Networks want to know when new versions exist so they can be let through. Not convinced this threat model is the one we need to deal with.

Ekr: Threat model is legitimate. Should be treating middleboxes as dumb pipes and prevent them from looking at data. Idea is to avoid arms race.

Gorry: This might be an issue. Don't agree with the threat model.

Ekr: Google has seen this with gQUIC.

Gorry: Yes, but don't know of this is true of IETF QUIC. Might not be the same case.

MT: Many things assume that symmetric crypto is free and public key crypto is prohibitively expensive. Retries requiring public key crypto are a non starter.

MT: Another option (relating to migration looking like connection establishment) might be viable.

Mirja: Whatever we do is just increasing the work for someone to break it and for servers (receivers). This is worse if there are middleboxes with few QUIC connections yet servers with many QUIC connections. Might not be worth the performance cost given uncertainty of threat model and risks. It's more important we have a way out for now.

Ekr: Not sure we're increasing the cost for server of client. One or two more symmetric crypto operations is not that bad. 

Ben Schwartz: Split mode ESNI forwarder is a middlebox that needs to knwo the version number. Split mode is probably incompatible with in-band VN. 

David Benjamin: Also consider whether or not the middleboxes can be updated. In TLS 1.3, middleboxes ossified and couldn't be updated. The idea with trial decryption and rapid updates made it so that some middleboxes never caught up, and for those that did can be persuaded to be fixed.

Ekr: ACK -- agreed that there's some class of middleboxes that can't be updated. 

Roberto: Protecting against lazy implementers. We're missing protecting against lazy endpoint implementers. Important to think about second aspect, which is that hard working implementers will do the Right Thing. We should consider whether or not detection of them is important.

Brian: Two operations one can do without the keys: (1) detect QUIC and drop (want QUIC vs non-QUIC to not be the flag to drop in v1), and (2) middleboxes might detect different versions and force downgrade. 

MT: Don't disagree. We have evidence that people build "if TLS then drop packet" products. The first issue (suppressing is this QUIC v1) is important. Can't suppress QUIC vs non-QUIC.

Subodh: Not convinced that masking the VN is sufficient to stop motivated attackers from detecting QUIC v1 vs v2. Attacker could do trial decryption to make a determiniation. More substantial changes are needed if we want complete indistinguishability. Protecting against lazy implementers (with obfuscation) is good.

Ekr: Agree that masking is not enough. Need encryption under unknown keys. Ability to parse CH is version dependent. This helps enforce protocol correctness.

Jonathan: Detecting QUIC vs non-QUIC to be able to let QUIC but not other UDP through may be needed.

Ben: Middleboxes *will* attempt to detect and distinguish VNs. Need to parse SNI out of CH for censorship. These are common. These systems will be doing version-dependent processing, and will likely not fail open if they don't like the VN.

Brian: Strongest desire is to distinguish QUIC from garbage to let QUIC through. Best way forward is to have a single clear breakpoint inside the initial. 

Gorry: Want QUIC v2, v3, etc to appear. 

Jana: Some firewalls do offer QUIC detection as a feature. That’s likely to increase. And SNI-based censoring will continue. Lazy implementers is a real problem that we should address. (There’s a lot precedent for folks getting protocol details wrong in shipping products.) We should not lose solving the first problem while working for the second one. 

Lars: Thee hums: do nothing, protect against lazy implementers, and protect against eager implementers.

David Schinazi: Recently deployed Google QUIC 46, respecting IETF invariants. Many introspection features exist (sniffing SNI for video broke since they changed packet format) and are used in practice. Afraid of lazy implementers. Protecting against eager implementers is hard since, if the client can detect it, then so can the middleboxes to some degree. Opinion: do a little bit for now, and don’t get too smart. 

Mirja: Don’t want to get to the point where people won’t support QUIC if they’re unable to perform current or deemed essential services.

Ben: Some discussion of a QUIC bit. Would like the inverse, that there’s a space of packets that have an inverse wire image of QUIC that won’t collide and would like to multiplex other protocols alongside. 

Lars: We currently have that. You want to maintain current behavior.

Ben: Exposing the VN can occur in the last packet.

Mirja: Purpose of ESNI is to force people to block everything if they want to block anything. Agree that some things are more expensive and that some eager implementer mitigations are only incrementally expensive. Currently undecided between the options.

Kazhuo: Connection greasing is a good way to prevent middleboxes from decrypting the CI to determine version. Consensus call: are we going to decide these as optional or mandatory features?

Lars: Assumed they’d be mandatory.

Ekr: Some are optional and some are not. The version with removing the VN and do trial decryption is not optional, whereas connection greasing is. 

Ian: Assumed they’d all be optional. Are any options going to be what Christian suggested to submit new versions rapidly update. 

Ekr: Is that “do nothing”?

Ian: Not really, since we’re actively doing something (submitting new versions).

Lars: Can’t agree on shipping frequency. 

Jana: Can make optional vs non-optional earlier on. 

Ben: Lazy implementers might take off-the-shelf library and shove packets into it to determine what version it is. Seems to be less engineering work.

Mirja: Answer to the hum depends on the solution.

Roberto: Lazy versus hard working is the same as those that have not read and read the spec, respectively.

Hums:
 - Nothing: little
 - Something for lazy: strong consensus
 - Something for eager: little

MT: This is a decision that will bind our actions in this WG before we ship the protocol. Does not preclude future work. 

Lars: The hum was to determine what we’re doing for QUIC v1. Does not preclude future work.

Martin Duke: Optional things don’t need to block v1. 

Mirja: There is an option to do nothing and protect against lazy implementers by sending two versions at once. 

Lars: Not clear if that’s a viable long term solution.

Mirja: Keep deploying versions quickly and dynamically.

Lars: WG can’t agree on this sort of solution.

Kazuho: Have not spent much time on discussing hard working implementers.

Lars: Hum indicated that we’ll spend time on option (2).

Ekr: Matched my understanding. Do we need a Design Team or something else?

MT: Martin Duke suggested that if we remove this from blocking V1 we might have some time. H3 will take the longest to finalize. We’ll have plenty of time to sort this out.

Lars: Closed by the interim?

Ekr: Suggest bringing proposal to the interim. 

Lars: Lots of people are interested. Talk to Ekr, who will lead the team.

MT: Version downgrade is not really detectable. Should be coupled to the VN work that’s ongoing. 

Ekr: There’s no version negotiation currently. Would like to change those semantics. 

David Schinazi: The reason to remove version downgrade prevention was due to ratholing. The rationale was to take it out and implement it as an extension.

Roberto: Trying to avoid ratholing. For the design team: is downgrade detection part of the scope? 

Ekr: No, since there’s not any version negotiation currently. 

### H3 Priorities

Ian (summarizing side meeting): Fairly broad interest in removing H2-style priorities from H3 spec. Interest in trying to ship something in time for H3. Unclear if it should be blocking or not, and whether or not it should be conveyed in a frame or header. Broad support for a setting that indicates if priorities are used and which scheme.

MT: Not broad support for that. Broad support for signalling that one’s not doing the H2 scheme.

Ian: We need broader consensus on the idea that we will not do H2-style priorities. 

Mark: Needs cross discussion with httpbis group. Might need to take this to the AD for a charter change. 

Roberto: H2 priorities have failed. 

MT: Agreed. If this goes on the critical path it’s unlikely that we’ll ship an RFC next year.

Roberto: Both outcomes of removing priorities (everything’s fine, and some things break) are fine.

Jana: Are we talking about creating a new priority scheme in this group or in httpbis?

Mark: We’re discussing H3 with no priority scheme, or one that’s compatible. 

Jana: Supportive of shipping with no priorities, knowing that some implementations will do it but not based on a specification. 

Mark: Priority scheme means client-to-server priority hinting mechanism.

David Schinazi: What we have in the spec currently is complicated. Preference is to not have hints in the core spec. There will likely be experimentation with priorities as extensions, and they can all land later.

Kazhuo: *missed*

Roberto: These schemes were always optional. Either outcome should not block H3. 

Lucas: Agree with Roberto. Disagree about placeholders. Hard to create hints without a placeholder. (??)

Hum:
 - Keep H2 priorities in H3: (1 in Jabber)
 - Remove H2 priorities from H3: (lots) // please rephrase this question as needed
 - Don’t know what to do yet: (nothing)


### Recovery and HTTP Issues

#### #2789 Use a higher speed RTT for new paths

MT: Didn’t understand Gorry’s text. 

Gorry: If the principle is to do what TCP does in this environment, then text needs to be improved. 

Ian: Some text has improved since Gorry filed the issue. Will work with Jana to prepare a PR.

Jana: *missed*

Gorry: *missed*

Lars: This is only editorial.

#### #2630 Define under-utiliation of cwnd

Gorry: Complicated to get the text. The intent was easy.

Ian: There’s a PR for this issue. Need more people to review the PR.

Praveen: (Comment from audio will go into the Github issue.)

Jana: We have algorithms for capping cwnd. 

Gorry: Will work with Jana to update soon.

#2556 Should kPersistentCongestionThreshold be 2 or 3?

MT: If TCP had principles we could use to make a decision here, then we should use it. But we don’t have that.

Ian: We picked a constant that was most similar to the number of TLPs we send before declaring congestion. 

Jana: Spec says two TLPs then an RTO. 

Lars: Close with no action and re-open if an issue is found with validation.

MT: Not sure we’ll have enough information to pick a constant with confidence. Maybe we should just acknowledge that.

Lars: Which value is more conservative.

MT: 2 is more conservative. 

Lars: In the absence of data, let’s just do 2. 

Jana: In the absence of data, we can also do 3. It doesn’t matter to me. We need an illustration as to what the value means and what happens if it’s changed. People may set these constants to whatever they want anyway.

Gorry: This is new ground in the IETF. 

Lars: Close with no action.

#### #2555 Define idle period for congestion period

Ian: Need to discuss with Praveen.

Jana: On general issue of idle period, we chose not to not walking into that territory and defer discussion of that to a separate RFC. 

#### #2534 ECT text disables ECN too aggressively

Jana: Will update.

#### #2923 Min_RTT management

Lars: LEDBAT has similar concept of Min_RTT, and we refresh it over the lifetime of a connection. Does anyone know what it does.

Jana: Not sure LEDBAT does anything.

MT: Would suggest something less than something naive, wherein you cut and start over every 10 minutes. Probably want to do something in terms of number of samples rather than time. 

Roberto: Provided code does not require a variable with Min_RTT, great.

Andrew: *missed*

MT: There are many ways to bike shed this issue. We should make some suggestions and not do anything more complicated than that. Resetting on idle won’t work for a number of usage patterns, since definitions of idle vary. 

Ian: How many people have read recovery document. (Lots of hands are raised.)

Jana: Maybe they read it and don’t care.

Eric: We did what was in the recovery draft.

#### #2632 H# GOAWAY should be symmetric and cover bidi and uni streams

Mike Bishop: GOAWAY in H2 refers to streams and makes things stop in both directions. Should do the same thing here. 

MT: Want to argue the converse, since this depends on conception of PUSH. If you shut down PUSH, you need to let requests continue.

Mark: Does anyone else care about the outcome? (No hands.) Is this issue a blocker?

Mike: If PRIORITY is removed, we can close over half the issues.

MT: Will commit to discussing with Alan. People who understand the problem need chat.

Roberto: Does GOAWAY make most sense at H3 or a layer beneath. Will we resolve it in V1? Not sure.

MT: Against moving GOAWAY down in any version.

Mark: Take discussion to the list.
 
