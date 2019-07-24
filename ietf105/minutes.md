Version 5949 Saved July 23, 2019
Authors: Sean Turner, Tommy Pauly, Brian Trammell, Craig Taylor + 1 unnamed author ( )

Tuesday, 23 July, 2019
10:00-12:00 Morning session I, Place du Canada
==============================================
 
NOTE: The acoustics in Place du Canada are suboptimal. 
Please review these notes and replace [text in brackets] (unintelligible or partially intelligible speech) with what you remember saying, if possible.
 
New Wiki for related work: https://github.com/quicwg/base-drafts/wiki/Related-Activities
Please add your side projects here to share with the working group in a central location.
 
Hackathon / Interop Report
==========================
 
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
 
 
 
Issue Discussion
================
 
Project board at https://github.com/quicwg/base-drafts/projects/5 -- looking at design issues today. Issues were assigned during London interim, a lot of these are still open. Today we will discuss newer issues and assign people to address them. For issues with owners, questions: have you made progress? do we need a new owner? 
 
Lars Eggert: If this keeps up we will start closing these with no action. We will do new stuff when we have issues under control. They are not currently under control.
 
Mark Nottingham: We can't keep doing this for another year or two.
 
https://github.com/quicwg/base-drafts/issues/2792 (Marten Seeman assigned to Sean Turner)
-----------------------------------------------------------------------------------------
 
Martin Thomson: I have thought about this a alittle. It is hard. Not sure it's worth addressing beyond a little text. Want a little time to think about it
 
ekr: not sure I understand the issue. 
 
Martin: Problem limited to you learn when a key update happens
 
ekr: countermeasure is precompute next key.
 
Martin: as said, don't think it's worth doing much here.
 
ekr: [unintelligible]
 
Ian: +1 to Martin. Can write something in security considerations if we understand it better.
 
Mark Nottingham: keep it open? Martin, can we close?
 
Martin: Security Considerations text, if that. If Sean or Marten have ideas, good. Don't want to block on this.
 
Mark Nottingham: More than text?
 
Jana Iyengar: mark as something other than design?
 
Lars: send a PR or we close? 
 
Mark: Will this come up again at WGLC, if not close issue.
 
Marten: This is a timing side channel, we need to resolve it
 
ekr: can you explain it please? what information does the attacker learn?
 
Marten: same as [packet number]?
 
Martin: In the case of a key phase bitflip, the next step takes nonconstant time.
 
ekr: The attacker learns what?
 
Martin: That the keyphase bit changed -> value of keyphase. Let's deal with it offline.
 
Lars: Deassigning Sean, assigning to Marten Seemann.
 
Mark: Outcome is security considerations text, not a protocol change?
 
Marten: Think so.
 
https://github.com/quicwg/base-drafts/issues/2670 (Nick Banks issue, Martin Thomsom presenting)
-----------------------------------------------------------------------------------------------
 
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
 
Martin: [pedantry]
 
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
 
https://github.com/quicwg/base-drafts/issues/2844
-------------------------------------------------
 
David: Problem is CCIDs don't do what they're supposed to. Server can decided to decide to use 0-len connection ID even when it can't multiples, but then nat rebindings and migration are impossible. Propose to say (in 2851) that you can use 0-len when you can multiplex without CID. 
 
Martin: I think David's solution is correct. Using information you control to get packets to you is good. Source-address based routing is bad.
 
Mark: Problems with this proposal?
 
Igor: What about two machines that know they're not NATted just not using CIDs?
 
David: are there multiple clients talking to same client on same port? that breaks migration. I think that adds a bunch of complexity for a rare use case.
 
ekr: Substantial deviation from our earlier decision that one could build a server that had same connection semantics as TCP. [unintelligible]
 
Martin: to use source address they need to know that sll clients are not natted
 
Ian: [missing]
 
Tommy: maybe one solution, specify that server can have zero length if migration explicitly disabled
 
Eric Kinnear: disable migration will become disable active migration
 
ekr: tcp has semantics.... [but this room doesn't have acoustics]
 
Brian Trammell: Would support a slight change to this PR that says if you want TCP semantics (5-tuple routing), great, you will get TCP guarantees. Need a warning. 
 
Roberto: The application stacks will always need timeouts and reconnects, so the case of NAT rebinding will break connections with 0-length CIDs, and that's OK. This seems more editorial.
 
David: The reason we have client CIDs is for multiplexing on local source port. That's the only use case. That doesn't work in the current spec because I don't know if the server is using these TCP-like semantics.
 
Martin: ekr's point is really good and mostly convincing. If you want TCP semantics, you get TCP guarantees. This is an unilateral decision in a two-party protocol.
 
Mark: Can this decision be made by the application mapped onto QUIC?
 
Martin: You can have server-server scenarios where this makes sense. As a browser not sure I want the server making that decision on my behalf.
 
Roberto: prefer to close with no actions
 
Igor: [missing]
 
Kazuho: +1 to David. Really hard to have one implementation that does both client and server
 
Tommy: Another way to do this is to take this PR and put it in the applicability draft
 
David: It is a property of the server to use either QUIC CID or TCP semantics. Do we want the server to want to make that decision? You can't negotiate this, so the server needs to be unilateral here.
 
Andrew: What about s/MUST NOT/SHOULD NOT/ -- achieves the same thing as current wording, warns about consequences.
 
Martin: Good improvement, doesn't fix unilateralness. 
 
David: MUST allows us to remove a bunch of text further down. 
 
ekr: inherent restriction of TCP: can't have two connections with same 5-tuple. Should we reqiure all QUIC servers to support CID semantics? 
 
Martin: change that andrew proposes perhaps sufficient. It's not applications so much as deployments, deployments can make this decision themselves.
 
David: Moving this to a SHOULD NOT and adding "here's what will break if you do" text, would be acceptable.
 
Kazuho: MUST UNLESS?
 
ekr: [missing]
 
Lars: can we come back to this tomorrow?
 
David: will update PR.
 
 
https://github.com/quicwg/base-drafts/issues/2863
=================================================
Ian: Punting until tomorrow, discussion ongoing
 
 
https://github.com/quicwg/base-drafts/issues/2763
=================================================
PR already merged for this, proposal to remove one paragraph. will do this using the normal process.
 
https://github.com/quicwg/base-drafts/issues/2834
=================================================
Long Header Packets and Routing Conn IDs
 
Nick Banks: Kazuho came up with a solution with the long header source, we don't need to keep this open anymore. Happy to close with no action.
 
https://github.com/quicwg/base-drafts/issues/2770
=================================================
Ian: Come back to this tomorrow, please read the PR (#2869)
 
https://github.com/quicwg/base-drafts/issues/2785
=================================================
David: Current spec sets stateless reset token per connection ID.
One of the interops saw an implementation using all zeros for all of their
stateless reset tokens. Reusing tokens is bad and loses security properties.
Rather than having a caveat, just say they MUST be different.
 
Martin: It's not necessarily losing them, it's about additional steps you need
to take. If you have two CIDs with the same token, you need to always remember both.
 
David: Question to the group is if we want to simplify things.
 
Kazuho: I think we should disallow reuse since this is more complex for the receiver
to maintain use counters on reset tokens.
 
Martin: We will be then adding a requirement for uniqueness (probabalisticly), and allow
generating a protocol violation (not require) if a duplicate is detected.
 
Mike: How about requiring a violation if they're outstanding at the same time?
 
Martin: Almost with you, but I don't think so; there are edge cases.
 
Martin: Will write text
 
https://github.com/quicwg/base-drafts/issues/2741
=================================================
ekr: Punt to tomorrow
 
https://github.com/quicwg/base-drafts/issues/2534
=================================================
Jana: PR written, has comments, it's on me to fix this week.
 
https://github.com/quicwg/base-drafts/issues/2656
=================================================
Jana: This one should be marked editorial, clarification needs to be added. A sentence or so. 
 
Mark: Anyone who isn't OK with marking editorial, please raise it now.
 
Martin: Need to look, will wait for PR.
 
https://github.com/quicwg/base-drafts/issues/2496
=================================================
Version Ossificaton. Punt to tomorrow? yep.
 
 
https://github.com/quicwg/base-drafts/issues/2084
=================================================
ekr: I will write text. Now.
 
https://github.com/quicwg/base-drafts/issues/2170
=================================================
ekr: Close please
 
 
https://github.com/quicwg/base-drafts/issues/2143
=================================================
Eric Kinnear: Sent a PR (2925) for this, lots of discussion.
We should have a threat model for what attackers can and can't do. This just lists what can happen, but is not new information.
 
On-path attackers can mess you up completely (that's expected). Specifically for migration, if you're on path for both paths, you can prevent migration. But you cannot prevent migration to another path.
 
Off-path can race packets, and can potentially beat your path to the server. In the worst possible (very rare/hard) case, the off-path attacker can become limited-on-path.
 
ekr: We may want to clarify the terminology to be more standard
 
Off-path cannot cause migration to fail or cause a connection to close.
 
Mark: Let people have a chance to read through it, try to get consensus.
 
https://github.com/quicwg/base-drafts/issues/2388
=================================================
Martin: there is a PR for this (2880), feedback please. There was a request to do this for HTTP, which has both connection and stream scoping, so it'll have more text.
 
Mark: PR is two weeks old. Proposal ready?
 
Martin: Yep.
 
https://github.com/quicwg/base-drafts/issues/2387
=================================================
ekr/Eric: The PR (2925) mostly covers this, but needs to be filled in by ekr.
 
ekr: Will finish this up.
 
https://github.com/quicwg/base-drafts/issues/2205
=================================================
Ian: close with no action?
 
Martin: is this not the ECN problem?
 
Ian: conclusion was no design change, document ECN issue?
 
Martin: IIRC there is an encouragement to increase value for e.g. devices that ack single packets
 
Martin: what was useful was airing this and seeing Gorry nod.
 
Mark: will we have a proposal?
 
Jana: yes
 
https://github.com/quicwg/base-drafts/issues/2342
=================================================
Spoofed connection migration
 
Eric: PR ready to go.
 
Igor: will add some more clarification, editorial.
 
Eric: questions raised about whether or not we should have a TP here. if it exists, we need editorial text about it.
 
Mark: Ready to go in terms of consensus.
 
https://github.com/quicwg/base-drafts/issues/2389
=================================================
disable_migration
 
Eric: Same PR.
 
 
https://github.com/quicwg/base-drafts/issues/2602
=================================================
Ian: will write a PR by tomorrow.
 
Mark: We're done with the design/late-stage list, yay us. Tomorrow we'll discuss getting recovery/HTTP into late-stage process. We'll come up with a runlist for tomorrow, 
 
AOB Tuesday
-----------
Brian: Regarding applicability and manageability, we have a handful of issues, and we'll be soliciting help on writing text for these issues. Please volunteer!
 
Eric: We should give the quic-lb draft some airtime here, as well
 
Martin D: Reminder that that draft has not been adopted; I think it's important that it's an adopted document.
 
Mark: Interim and/or Singapore
 
Lars: Might need a tiny recharter.
 
Roberto: Worried that we'll start discussing WebRTC before other v2 features; getting v2 chartered first is a really good idea.
 
Wednesday, 24 July, 2019
10:00-12:00 Morning session I, Place du Canada
==============================================
 
Issue Discussion
================
 
 
Future meetings, implementation drafts, and getting to Last Call
================================================================