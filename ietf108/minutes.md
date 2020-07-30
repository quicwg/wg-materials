# QUIC at IETF 108

Note Takers: Brian Trammell, Robin Marx, Chris Wood(?), Eric Kinnear

Wednesday, July 29, 2020

11:00-12:40 Wednesday Session I

## Administrivia
Blue sheets
Scribe selection
NOTE WELL
Agenda bashing

## Issue Discussion

*Ends latest at 12:10 UTC*

[Drafts that require discussion](https://github.com/quicwg/base-drafts/issues?q=is%3Aissue+is%3Aopen+label%3Adesign+-label%3Acall-issued+-label%3Aproposal-ready)

(Issue link template)
https://github.com/quicwg/base-drafts/issues/3765

### Migration

[Issue 3765](https://github.com/quicwg/base-drafts/issues/3765) ([slides](https://github.com/quicwg/wg-materials/blob/master/ietf108/migration-3765.pdf))

- Igor Lubashev: prefer the first one, do something technical to indicate nonmigration. There's a reason for the parameter in the first place. For servers that might identify the contract kind, same case for them as any server that disables from the start. Seems like no-one is opposed to the ???? solution in the PR, just needs to be nice and clean.

- Eric Kinnear: we first discussed this as something people might like to put into an extension. OK to close the rest of the gap and put it in SPA. Previous discussion, consensus was extension though. Answer you get back for an address is anyway only going to be good for one interface. No problem in just not accepting packets from other sources that are outside of your contractual domain. Nice if you have address changes within that domain (e.g., embedded cache in an ISP), that will continue to work fine. If you say no to active migration, you might mistakenly think you're (missing?) these packets and freak out. 

- Kazuho Oku: I can't agree with what Eric said. No technical need to make change. Makes some sense to have same feature set for original address and SPA. The current PR recommends endpoint (client) to use same source address, concerned about that as it changes assumptions about how client can be implemented, it can't let the OS choose source address anymore. Having bit/flag in transport parameter is fine.

- David Schinazi: *tired noises* If I understand this issue correctly, minor change, happens after handshake enough so it can happen in an extension, so prefer to have it there.

- Christian Huitema: Worried about testing issues, the more options we open, the more test cases we need, the more bugs. Fixed client address is problematic, there might be a CGNAT, source may change (without your knowledge). Uneasy with doing this now after WGLC and prefer leaving as an extension.

- Mike Bishop: keeping same source address discourages network attachment migration at same time as SPA. We can wordsmith that. What we had said was, not aware of concrete scenarios requiring this, can add later with extension. Now we have scenarios. How much later are we?

- Igor Lubashev: it could complicate a few implementations to require the exact same source address. Would be reasonable not the include the capital ??? and it's ok to let the OS choose the address as long as you don't deliberately change and migrate later. For practical purposes, you'll migrate soon after handshake and sticking with same network attachment you have during handshake. More pragmatic to say: migrate once and don't migrate again. 

- Ian Swett: Discovered two things about this feature, that I didn't anticipate. 1: if a server really wants to not wait for a timeout, they are incentivised to mint stateless reset oracle (despite the doc saying not to do that). 2: incentive to not give out CIDs, which is the easy solution as a server. I don't know that we like that, but no strong opinion from deployment perspective.

- Jana Iyengar: What Eric said is relevant. At a high level, we are rehashing a discussion that happened on the issue. same circles. the problem is basically solvable as in the PR. Question is what do we want to do at this late stage in the game? Alignment in design here: migration should be attached to addresses, not endpoints. With Mike's change, moves it back to per-address. Where it should be. Some trepidation from implementors but not strong pushback. Suggest to take this solution, not a lot of people have implemented/tested SPA yet, and move forward, and stop rehashing.

(will cut the queue after Christian and Eric *or not*)

- Christian Huitema: I have implemented 28 and 29. And tested. Others have as well. Client-side problem: two possibly contradictory TPs. One says migrate is allowed or not, one says please migrate to this address. What does don't migrate + migrate to this server address mean? Please only migrate to this transport address? Ambiguity in the spec that Mike's working around in this PR. *tired noises*

- Eric Kinnear: Agree strongly with Christian. We're wiggling around the fundamental distinction. If we scope to specify per-address, not per-endpoint (which is good and we should do this either way), say we covered this one thing, and will cover the other gaps in extensions. Filling that gap by saying "you can't migrate anymore after first migration" might make us all happy.

- Jana Iyengar: Eric suggests we allow for one migration per additional address. Confirm?

- Eric Kinnear: Yep, that's what I'm saying. Further restrictions and lots of logic in a future extension. 

- Jana Iyengar: What happens if you don't specifically allow for this migration, packets come to server, server may or may not get there if they come from a different source IP, worst case is connectivity loss.

- Eric Kinnear: You could also just not accept the packets. 

- Jana Iyengar: this narrows it down a little more.

- Eric Kinnear: this is an explicit way to express that (and only that).

- David Schinazi: following discussion here *tired noises* this conversation sounds like a brainstorm. Are we still in front of a whiteboard trying to figure this out? No production deployments of this yet. Recommend that we stop and take this engineering effort into an extension we can bring back to the WG is ready.

***HUM TIME***

1. we need to address this migration issue before shipping: piano (medium)

2. it's ok to leave this as-is and consider an extension after shipping: fortissimo (loudest)

- Mark Nottingham: if people who hummed for 1 could get into queue to provide additional details? 

- Igor Lubashev: conceptually, we are leaving a hole, though it's not hard to fill. Looking at the design, did introduce parameter for some reason earlier. There is however a common case on the Internet that would in the same way benefit from a new TP. To deliver a coherent v1 of QUIC, especially since it doesn't take much effort, doing something now would be the better alternative. Don't want to create incentive for people to do their own thing. 

- Mark Nottingham: Igor, would you strongly object against closing without change?

- Igor Lubashev: would be disappointed, but as said, it can be worked around (though workaround is weird since it entails reducing CID issuance, which we like for privacy reasons)

 - Mark Nottingham: other option would be to create a design team, but that's maybe not ideal at this late stage.

- Igor Lubashev: we don't need a DT, we have a proposal, no technical objections to it. this is about change the text now or don't touch it. 

- Mark Nottingham: will cut the queue now, unless someone's mind has been changed since the hum

- Jana Iyengar: no strong technical disagreement, just no appetite to think though the potential issues here. lack of clarity is a good reason not to do something at this stage. We want to experiment with these things. We'll learn through deployment, we'll find more gaps. We have to accept that.

Mark: go ahead Lars
Lars: go ahead Mark
(maybe we need a WG to increase the speed of light)

- Lars Eggert: putting a note on the issue to close with no action. this was the last issue the editors had that they wanted to discuss today. There are more issues floating around, a whole lot of editorial, some in triage. we see more new issues, which is not what we need at this point, so please think hard if an issue is justified, if that doesn't work, we should maybe have a very late stage process that's more formal. it's too late to have discussions on fundamentals. Anyone else want to talk about base drafts?

- Martin Thomson: relaying EKR, let's talk about 3965. I'd like to talk about it and say don't do it, no action.


### Version-specific Transport Parameters

[Issue 3965](https://github.com/quicwg/base-drafts/issues/3965)

- Martin Thomson: I don't see why we need to solve this now.

- Ekr: propose to close without action, want to do that now.

- Nick Banks: Fine closing after existing discussion, or alternately editorial warning text to say don't back yourselves into a corner. 

- Mark Nottingham: Changed from design to editorial. Other issues?


## Hackathon / Interop Report

- Lars Eggert: I am in Europe and most interop was in US, but [interop matrix](https://docs.google.com/spreadsheets/d/1D0tW89vOoaScs3IY9RGC0UesWGAwE6xyLk0l4JtvTVg/edit#gid=2020321510) looks pretty full and good. Have some white, but those are new stacks that haven't participated actively yet. Some issues: ECN doesn't seem to be supported well yet, even though it's an easy addition to just report the received counts (willing to send PRs myself or put your interns on it). Pretty sure we will continue having interop events for next draft, but automated testing is also in full swing now ([QUIC interop runner project](https://interop.seemann.io). So create a docker image for your server and client to hook it into this, and then you get daily new results running against everyone else. Highly recommended.


## QUIC-LB: Generating Routable QUIC Connection IDs

*5+10 min - Discussion of the [QUIC-LB](https://tools.ietf.org/html/draft-ietf-quic-load-balancers) draft - **Martin Duke***


[slides](https://github.com/quicwg/wg-materials/blob/master/ietf108/quic-lb.pdf)

### Discussion on Issue 12

- ekr: AIUI this second issue is only with ECH, otherwise with SNI you know who the customer is. 

- Martin Duke: An attacker observing SNI, minor compromise, could be more of an issue with ECH. 

- ekr: is there any way to solve this with public key crypto?

- Martin Duke: *cryptosystem-designing silence* with a massive change to the design maybe. better way would be trial decryption, if it has a rich enough SID space.

- ekr: LBs don't have enough memory to cache answers, if using PK. encrypt conection ID once, then cache the data, does that work?

- Martin Duke: we resist keeping state.

- ekr: will go think about this.

- Ian Swett: yes, you can definitely cache it but it mitigates one of the wins of using crypto in this case. not really sure that the third config rotation buys you enough extra space, but that's just intuition.

### Discussion on Issues 8/16

- Eric Kinnear: *the same QUIC pun we've heard 1000 times* Rather than saying here's a potential compromise, we could only allow options that don't include huge compromises. Then again, there's a reason these compromises exist. 

- Martin Duke: personally don't have strong opinions about this issue one way or the other. What I see in Jabber is resistance to obfuscation, and some comfort idea with plaintext. Some disagreement on threat model -- one possible threat model is attacker can focus traffic on a server, some aggreement as to whether this is a problem, do I really care if you take out one of my hundred servers? Does anyone want to speak up for the obfuscated CID algo?

**crickets**

- Martin Duke : hearing little enthusiasm for obfuscation, which is great, because that was terrible code to write. Btw: now have an [open source implementation](https://github.com/f5networks/quic-lb) for that as well. 

## Manageability/Applicability of the QUIC Transport Protocol

*5+5 min - Discussion of the [Applicability](https://tools.ietf.org/html/draft-ietf-quic-applicability) and [Manageability](https://tools.ietf.org/html/draft-ietf-quic-manageability) drafts - Mirja Kühlewind & **Brian Trammell*** 

[slides](https://github.com/quicwg/wg-materials/blob/master/ietf108/ops-drafts.pdf)

*Brian is apparently too weak to present and take notes at the same time, so I'm taking over*

- Martin Thomson: creating interdependencies between drafts by citing LB draft. I'm comfortable with that, but want to make sure everyone else is as well. These 2 drafts are closer to being ready than the LB one.

- Brian Trammell: this is supposed to be an informative ref, not normative. Intention is to NOT block this draft on LB status. If it's normative now, we should fix it. 

- Martin Thomson: probably make this clear when we get this out the door so it doesn't get held up in a queue. 

### Issue 75

- Ekr: do we want to document the wire image as of the time of publication of the base drafts? Especially wrt SNI

- Brian Trammell: Could set 1 line of text saying: SNI is here now, but ref why that's going away soon

- Ekr: that would be fine too. 

- Brian Trammell: add that as note to issue #75 (TODO)

- David Schinazi: spent a lot of time discussing SNI in QUIC with middlebox vendors. Many of them currently parse SNI from TLS and want to for QUIC too. Huge headache for multiple reasons. First: vendors have proted code from TLS parser to QUIC parsers but haven't thought through implications. E.g., in TLS, five tuple will stay the same and if migration, new connection with new SNI parsing. In QUIC, even if you parse SNI, if you detect black hole, Chrome will spuriously migrate client port to check if that helps. Can no longer link SNI to those new packets. What is the point of parsing SNI then? Second: had one format earlier for gQUIC, which then changed. On some networks, were forced to stay on old format... so this effectively has already ossified QUIC. Are communicating this to middleware vendors, but am really concerned to include text that specifies how to extract SNI from IETF QUIC: will cause ossification. If we do have text: have extra paragraph to explain why it's a bad idea (even though people won't read it)

- Brian Trammell: share sense of nihilism. Are you volunteering to do a pass on these documents to make sure we're appropriately non-recommendative? Especially for invariants.

- David Schninazi: I can commit to that if someone adds me as a reviewer to the PR (TODO)


- Brian Trammell: Please, people of QUIC, read these docs, as we're in WGLC and time is short. 

## Greasing the QUIC Bit draft

[draft](https://datatracker.ietf.org/doc/draft-thomson-quic-bit-grease/), [slides](https://github.com/quicwg/wg-materials/blob/master/ietf108/quic-bit-grease.pdf)

- Ekr: do we still need this bit to distinguish from gQUIC? 

- Martin Thomson: deliberately unstated, believe that Google uses this, don't have to ship the server part.

- David Schinazi: We still support Q043 (first version of invariants) and Q046 (second version), now we're at the third/current version. We won't need this after we deprecate 43/46. Not a blocker, still a good idea. Can't support on server until deprecation but can implement in client.

- Ekr: can we remove the invariant? Does this bit need any consideration at all?

- Martin Thomson: need to point out: this is NOT an invariant. Explicitly want to protect the fact that it -is- version specific? 

- Ekr: With the H3 case, as soon as Google changes we can randomize it all the time. In the RT case, depending on what's deployed it either needs to be permanently one, or it's always randomizable. 

- Martin Thomson: so point with real time case is that you can negotiate this to be fixed when multiplexing with something else, so don't need to worry about that

- Ekr: if gQUIC is going away, we should require it to be randomized at all times for H3.

- Ian Swett: Timeframe for getting rid of gQUIC: ASAP but >1y. You could shift default posture from never-randomize to always-randomize with a way to turn it off. Needs to be in the base draft, though, due to the multiplexing issue. Would not want to decide we're ditching mux at this late stage.

- Ekr: we're only chartered for H3, cannot do RTP as well, though agree that's going to be a problem in practice.

- Lars: let's take it to the list. Moving to the next one.


## 3GPP Access Traffic Steering Switching and Splitting (ATSSS) - Overview for IETF Participants - Spencer Dawkins

[draft](https://datatracker.ietf.org/doc/draft-bonaventure-quic-atss-overview), [slides](https://github.com/quicwg/wg-materials/blob/master/ietf108/atsss-overview-00-v3.pdf)

- Jana Iyengar: there's a race condition: is 3GPP actually doing work on things here in QUIC to make this work?

- Spencer Dawkins: no, absolutely not. I skipped over the bottom of slide 2, which said that the participants on the draft want to do work in the IETF and 3GPP agrees with that. "Race conditions" are mainly between 3GPP deadlines and IETF momentum. This is not new, but now we're coupled more closely with 3GPP than we've been for other recent 3GPP dependencies on IETF work. 

- David Schinazi: I've seen discussion about 3GPP MPQUIC, impression is that outsiders are thinking: yes, 3GPP is doing MPQUIC, it's happening! But they clearly are not... this work needs to be done in the IETF. We should really clear up that confusion, because right now it's a mess

- Spencer Dawkins: I understand the confusion, part of this is race condition between how quickly we are moving in the IETF and how quickly people outside the IETF seem to need what we're specifying.

## QUIC Version Aliasing draft - Martin Duke

[draft](https://datatracker.ietf.org/doc/draft-duke-quic-version-aliasing), [slides](https://github.com/quicwg/wg-materials/blob/master/ietf108/version-aliasing.pdf)

*the ghost of christmas audio problems strikes again*

*and again* (Martin should stop googling "recursion")

## Planning

- Lars: We could certainly do a WG interim, timezones might be a challenge; we haven't done them because they can be cumbersome. Would prefer to work desync on GitHub and push the issues there, unless we get blocked. So plan to meet at 109. Plan to do another WGLC on -30 or -31 if necessary. Pick up an editorial issue and send a PR if you want to make things go faster. Once we're closer to IETF LC the next discussion is how to recharter / slice and dice future work. Extension work on the horizon would need a home. Minor revisions to base draft. We'll have that discussion in the 109 timeframe. 

- Mark: Next WGLC will be shorter, to confirm that first WGLC comments were properly addressed. 

- Lucas Pardue: *clearly doesn't understand timezones and joins 2 minutes after meeting concludes* doing conensus call after the meeting, local internet issues, watch the list.


