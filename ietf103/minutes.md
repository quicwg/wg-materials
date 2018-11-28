# QUIC Working Group Minutes - IETF103 Bangkok

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

  - [Tuesday, 6 November, 2018](#tuesday-6-november-2018)
    - [INTEROP REPORT - LARS](#interop-report---lars)
    - [EDITOR'S UPDATE - Martin Thomson](#editors-update---martin-thomson)
    - [MIRJA PRESENTS OPERATIONS DRAFTS](#mirja-presents-operations-drafts)
      - [pmtu discovery](#pmtu-discovery)
      - [connection id generation](#connection-id-generation)
      - [application handling](#application-handling)
      - [rejected 0rtt](#rejected-0rtt)
    - [VERSION NEGOTIATION presented by Martin Thomson](#version-negotiation-presented-by-martin-thomson)
    - [HTTP ISSUES PRESENTED BY MIKE BISHOP](#http-issues-presented-by-mike-bishop)
      - [settings interlocking slide](#settings-interlocking-slide)
      - [length prefixed frames considered irksome](#length-prefixed-frames-considered-irksome)
      - [initial priority](#initial-priority)
      - [naming http/quic](#naming-httpquic)
    - [INITIAL INJECTION ATTACK from Marten Seemann](#initial-injection-attack-from-marten-seemann)
  - [Wednesday, 7 November 2018](#wednesday-7-november-2018)
    - [Spin Bit](#spin-bit)
      - [Overview](#overview)
      - [Discussion](#discussion)
      - [Hums](#hums)
        - [1. Confirm: decision will be limited to the single-bit variant](#1-confirm-decision-will-be-limited-to-the-single-bit-variant)
        - [2. Confirm: the spin bit is fit for purpose](#2-confirm-the-spin-bit-is-fit-for-purpose)
        - [3. It must be possible not to spin](#3-it-must-be-possible-not-to-spin)
        - [4. Confirm: the privacy/security/ossification aspects of spin are well-understood](#4-confirm-the-privacysecurityossification-aspects-of-spin-are-well-understood)
        - [5. Intent to implement and deploy](#5-intent-to-implement-and-deploy)
        - [6. To include the spin bit in the specification, as laid out here. Some decisions can still be made.](#6-to-include-the-spin-bit-in-the-specification-as-laid-out-here-some-decisions-can-still-be-made)
        - [Hum: No negotiation for spin bit support?](#hum-no-negotiation-for-spin-bit-support)
    - [Planning](#planning)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Tuesday, 6 November, 2018

*13:50-15:50 Tuesday Afternoon session I, Thai Chitlada 1 - in other time zones*


### INTEROP REPORT - LARS

unlikely to meet the nov deadline

2 tables full of implementors; around 10 implementations

getting back to basic interoperation after stream 0 changes

very few stacks dealing with key updates or migration - concerning wrt timeline

prg hopes for -17 interop.. or maybe interim in tokyo

hq is also not real well exercised

christian: concerned about lack of migration implementation. at which point do we cut features?

mnot: we are moving beyond interop talk

ekr: things that are hard to test do not get tested even if implemented. e.g. recovery. we need a test harness w automation

jana: the matrix does not contain the full feature set of quic. not ready to discuss what to cut

lars: +1 to ekr's comment. perhaps something like packetdrill

ekr: wants to prioritize harness and seeks people of similar pov

jana: what about the suite that showed up in LHR.

lars: that was more of a conformance test.. quic-tracker (?)

### EDITOR'S UPDATE - Martin Thomson


colin: wrt first octet discussions and avtcore.

mt: we have slides on that later

ekr: would like 4 weeks before freeze

mt: fair. point still stands that you have been warned about oncoming freeze

mnot: wg has expressed that we need a period of stability to let impls catch up

mt: outright bugs will continue to get fixed. but soon a stable protocol will need to set in. suggests a speculative issue for improvements will be more aggressively closed - this does not exclude bugs. discussing on list before opening issues will become better. editorial issues are always welcome with PR

mt: we lack experience in deployment, and we need that before rfc. therefore get that soon. might mean there are some aesthetic things that suck

(Long Header Slide 4)

ekr: probably need 1 more bit for type

david s: extensibility argues for more type bits.

ekr: 8bit pn is plausible

lenox: is this part of this version?

mt: this is not invariant (other than 1st bit) wrt next versions

colin: this avoid collisions with stun and (mumble) - please coordinate with avtcore. can we get stun demux as an invariant

mt: new requirement!

jana: is that so we don't need to continually re-argue?

colin: easier to have an invariant

jana: invariants are things that we are choosing to keep fixed as a minimal set.. stun could be one of those

colin: likely to be extremely important. basically just adding 1 additional bit of invariant

ekr: opposes. most quic don't have to be demuxed w stun. endpoints need to be able to demux, but middleboxes are more concerned about invariants

colin: expects p2p will need infra to allow this to move through

### MIRJA PRESENTS OPERATIONS DRAFTS


ekr: don't talk about it

jana: people who are going to do this understand it

ekr: this isn't something we have taken on

jana: we are not in the business of telling apps what they should not do.

ekr: if document has force it should not do things that are not advisable and this is not advisable

jana: import to say why not what

martin: people are already doing this.. quic/ws reference

spencer as AD: partial reliability is explicitly out of scope. we should talk

ian: its fine to say nothing given spencer's comment. however this totally works fine!

mirja: ekr please add your arguments to the github issue

lars: quic v2 will likely contain partial reliability. ops shouldn't presuppose this

mirja: just documenting current practice

jana: not clear what partial reliability is without a definition.. hard to do given its not in charter scope. stay out of the way

tommy: don't mention the PR hack. precedent to include the whole list of whacky stuff that's possible? otoh error cases are important

mirja: should we give more guidance on interface on cancelling stream?

tommy: talking about strategies is useful. agrees to do a pull request

harald: disappointed in wg discussion. the choice is whether or not we want to provide a forum for discussion of this topic or not (and yield influence if not)

lars: nobody is trying to shut down the partial reliability discussion - we're talking about this document

harald: we have minimal chance of influence and it seems like we are pushing it away

lars: disagrees. more documents and versions are coming

harald: there's a lot of junk in rfc series such as ipv5 we should worry about the discussion more than polluting the rfc series

spencer as AD: do people have incentive for partial reliability in some other way?

ted: charter presumes PR is an extension. is the document defining applicability of core quic or that of extensions + core? considerations around extensions could be dealt with in a new doc by limiting scope of this doc to core quic and create a new one for extensions

mirja: we can be more explicit about versions.

#### pmtu discovery

mnot: thumbs up

mt: take the text if available

gory: ??

#### connection id generation

jana: martin duke knows

#### application handling

- martin thomson: should be redundant so we don't need them here. application protocol should specify behaviors
- mirjia: beyond http, we need rules for app protocols without mappings
- lars: we need to be more active on operations drafts

#### rejected 0rtt

christian: you are worried about making general discussion about specific applications mappings. interop happens at application layer

mirja: general classes of application can benefit from advice

ekr: this one is application specific (0rtt)

subodh: +1 to ekr.

mirja: can we tell people something useful independent of application

subodh: now thinks general advice would be useful

martin: not enough background - need more look from WG on document (+1 from mnot)

### VERSION NEGOTIATION presented by Martin Thomson

martin duke: new initial is supposed to have same dcid. so in general case this will be routed to same server and we wont have this problem

martin thomson: new version can be flipped during the statless rtt - so it can still happen

kazuho: dcid might change because it is not an invariant


### HTTP ISSUES PRESENTED BY MIKE BISHOP

#### settings interlocking slide

mt: weird to depend on 0rtt settings.

mike: server always goes first

mt: weird. prefer not to have that one. ok having defaults for alleviating hol blocking as long as defaults are simple e.g. no header table use. however hedaer block size is not conducive to that. so in big picture hol blocking is tolerable

mike: not using qpack dynamic table at all is rather a drawback to request size
jana: what mt said. also what is the use case for negotiation?

kazuho: use case is that endpoint can wait for peer's signal to decide whether or not create qpack decoder stream. full negotiation just moves blocking part around - prefers negotiation

subodh: worried about offer/select semantics .. and also current state of waiting for settings frame. prefers defaults mode. h2 has a defaults mode as client can speak wout server

alan and dmitri: qpack default size to 0 in impls

eric kinnear: not sure this is a meaningful hol improvement
mt: i hear that defaults are ok - but not sure how to impl it. how do i do a header block size default eg? 0 is only safe default but not useful

eric kinnear: yuck wrt different rules from different settings (from off mic).

subodh: 0 means don't compress, not dont send

mt: no. it means no headers

kazuho: h2 .. in tls13 server speaks first, tls12 client speaks first. but in quic we have consistency

jana: outside of qpack, is there another feature that needs offer/select

mike: not at this time. perhaps mutually exclusive extension (different flavors of priority e.g.)

mt: we can deal with that some other way!

mnot: too early to hum. lets see more fleshed out proposals on list

#### length prefixed frames considered irksome

ian: in favor. framing in framing makes it hard to make large content serving work. 0 is currently invalid - so its not overloading a current valid

ekr: mildly in favor

mike: existing alignment is to allow push promise

jana: more in favor. imagine a world without push and then you don't need this.

dmitri: to ian still need to support peers that frame data

kazuho: server timings as trailer is a good use case

#### initial priority

mt: accept it and move on

mike: I will close the issue based on feedback

#### naming http/quic

ekr: this is really a fork

mnot: h2 did not deprecate h1

mnot: h2 did not obsolete h1 either

mike b: you should use h2 unless you cant

ted: is there confusion between tokens and names?

patrick: h3 is meant to be a successor to h2 because its better. also h* all have same semantics which is important signal

kazuho: logging will not like anything other than http/* and h2 already said no minor version numbers

spencer: update charter before ad transition

mnot: naming of http needs to stay in http community

mt: this is a fork? mnot: semantics vs wire is what is important

HUMS ON SUPPORTING RENAMING to H3

support hum strongly in favor with non zero do not support. perhaps 70:30

support hum for letting httpbis wg decide: ~100% support

### INITIAL INJECTION ATTACK from Marten Seemann

martin d: pr 1819 was meant to allow receivers to drop initial packets. not sure how to bring back the dead PR

marten s: We still need the ACK in 1819. This proposal will require some changes to loss recovery.

lars: out of time!

kazuho: we have this discussion on and off since may - opposed to changing this now because it is an optimization

marten s: its an attack surface issue


## Wednesday, 7 November 2018

*9:00-11:00 Wednesday Morning session I, Thai Chitlada 1 - in other time zones*


### Spin Bit

#### Overview

Recap of spin bit: it uses one bit in the short packet header. Client sends bit, server reflects, and the client then flips the bit once it sees the edge of the bit reflected.

Similar to work done in IPPM as alt-mark, except that was two synchronized boxes, while this is end-to-end.

Why?
- Interdomain troubleshooting
- Quality monitoring
- Bufferbloat detection
- Internet measurement

Microsoft, picoquic say they will implement

Concerns are:
    - Geolocation, which was analyzed by design team
    - Selective spinning, if all clients spin, then ones who don't look odd
    - Semantics could change between versions

Concerns about robustness, and usefulness. In good conditions, it works very well! Paper shows good results. Susceptible to high reordering.

As an observer, how do you filter out non-participating endpoints?

- Paper proposes "valid edge counter" to use two additional bits (but this is out of scope for QUIC now)

- Non-explicit edge validation (heuristics and reverse path validation)

Hackathon implemented heuristic at IETF 102.

Reverse path validation handles cases well with 10% reordering and depth of 5ms

Overestimation is not necessarily a problem actually causes earlier action, which may be good. We can filter out underestimation.

#### Discussion

Considering doing some hums first prior to discussion to check for consensus.

Potential of IPR disclosure, but none has been made, so discussion is assuming not.

HUM TOPICS
- Confirm: decision will be limited to the single-bit variant
- Confirm: the spin bit is fit for purpose
- Confirm: the privacy/security aspects of spin are well-understood and acceptable
- Confirm: intent to implement and deploy
- Consensus: include the spin bit in the specification
- Consensus: requirement level / negotiation mechanism for the spin bit (if previous consensus achieved)

Christian: does this include the recent PR to make the use of spin a percentage?

Bob: The last point (requirement level) is not well phrased as a question

Ted: For understanding of privacy/security, we must know that it must be possible to not spin

DKG: While there was a reference to ossification earlier, that's not on the hum list. I'm not convinced we know what the ossification risks are.

Subodh: To add to the ossification concern, what's the differential treatment concern?

Richard Barnes: Seems odd to have "acceptable" in the hum confirmation.

(ACCEPTABLE IS REMOVED)

Spencer: As individual; should it worry me if we're asking about sufficient analysis, since not having found concerns yet doesn't mean there aren't any.

Mark: It must be possible not to spin.

ekr: If we miss consensus on any item, do we stop and talk, and if we don't, we're done?

Lars: Yes, if it's inconclusive, we figure it out

Christian: The arguments for several spin bits (VEC and Orange) can do things like detect loss, but the decision indicates that these are out of scope now.

Lars: Yes.

#### Hums

##### 1. Confirm: decision will be limited to the single-bit variant

**Yes: Strong hum**

**No: Nothing**

Martin: this next question includes whether enough people do it

Bob: It's fit for the purpose for those who want it

Igor: To clarify, it's not everything all operators need, just RTT

##### 2. Confirm: the spin bit is fit for purpose

**Yes: Strong hum (jabber agrees)**

**No: Nothing**

Christian: Two parts about not spinning--I can tweak a bit in my implementation to not spin. But it should also be possible to disable without ill effect of singling someone out.

Lars: Clients, or also servers?

Christian: Definitely includes servers. Both.

Marten Seemann: For p2p applications there's no real distinction between client and server. It must be possible for both sides to opt-out unilaterally.

Sanjay: There was discussion about how to specify that you must spin..

Lars: This eliminates the possibility to "must spin".

Jana: As far as opting out without consequence, there's the question of how to negotiate this.

Mark: Let's talk about that later

Marten Seemann: It seems like you could still have preferential treatment

Martin Thomson: The specific design for opt out is the last item. That's not this question.

##### 3. It must be possible not to spin

**Yes: Strong hum**

**No: Nothing**

Ted: Clarifying that everyone should know that this is not in invariants

ekr: These are all three separate items (privacy/security/ossification). I don't think we understand ossification.

Mirja: There has been more privacy/security/ossification analysis than for any other bit in QUIC. Is this understanding what has been discussed, or if there are unknowns.

Lars: I want to confirm that people have the information they need.

Kazuho: I want to point out that for ossification, we have done plenty of analysis for zeroing or randomizing. We haven't discussed using another signal.

Cullen: I don't think we understand these in any protocols! Would the chairs change the question to "do you have enough info today to decide the other questions".

Marten Seemann: There's been an analysis of geolocation, but not for VPN or NATs. You can get the RTT from the VPN endpoint and the server.

Lars: That's just for TCP proxies.

ekr: We previously hummed that you must be able to opt out. I'm not convinced we know how to design a mechanism.

Mark: is that about having enough information?

Ted: Responding to the concern that Marten raised about VPN: it is the case that if you are *very* far away, you can detect that there is a VPN gateway present. You can't tell where it is, though. It is possible to determine a tunnel is present, but nothing more. If this is a case of concern, make the default to opt out over a tunnel. I am convinced we can mitigate this successfully.

Marcus: On the topic of preferential treatment, the incentive of the network is to use the bit to improve your experiment. If you don't want this at all, a network can just block all QUIC, but they don't have any reason to do that.

Jana: Rephrasing was useful, because we can't always get to the end of all issues. There might be more issues, but we can still make a decision on this for now.

Bob: To Jana's point, these are all dogfights, and various entities will get ahead, and go back and forth. It's enough to say we have enough at this time.

Toma: Even when the RTT is shown to a third party, we can figure out how far, but not where. I haven't seen the analysis of what would happen if a possible attacker could do BGP hijacking and used RTT to limit the possible sources, and enumerates the sources.

Kazuho: By confirming the third issue, we confirmed that the spin bit is optional. That means that this question is "can we propose it as an optional element".

Christian: About BGP hijacking: the spin bit is a tradeoff between privacy risk and network management. Network management can detect BGP hijacking. If we refuse to expose things, it's not necessarily true that everything will be better. This isn't black and white.

##### 4. Confirm: the privacy/security/ossification aspects of spin are well-understood

**Yes: Strong hum**

**No: Weak hum**

Mark: Will more time help any of the negative hums?

Martin Duke: I'm afraid we lost the plot. We remove the negotiation part?

Mark: We're not there yet. That's not the decision we're making now. We're making sure we know what has happened so far.

ekr: As someone who hummed no, I don't presently understand if the proposed design meets the ossification criteria. That's the only reason I hummed against.

Al Morton: We haven't put a green check or red X on this (4). We've emptied the line for the negative. We need to make the call.

Nick Sullivan: To ekr, is ossification equal to discrimination?

DKG: I think discrimination is the ossification concern. I agree that the chairs took the right feel of the room though.

Jana: Can we move on to the last question without closing this?

Gorry: I would like to just move on and decide

Tommy: I think the traffic discrimination can be solved; there may be trailing ossification aspects, but they are more about how we can reuse the bit later.

Lars: We want to know if people will have sufficient traffic.

Tommy: Apple plans to do a majority of spinning on clients

Gabriel: Microsoft does still intend to use it (client and server)

Florin: Broadcom will be exploring using (middleboxes)

Ian Swett: Chrome will not do this, and Google servers are a "may"

Martin Duke: F5 is a middlebox and server and would support in both

Dmitri Tikhonov: LiteSpeed Technologies will implement in client and server

Dan Druta: Will use and deploy as a middlebox

Subodh: Facebook as client and server will most likely not, but reserve the right to enable it

ekr: Firefox does not intend to set the spin bit

Jana: Fastly doesn't intend to do it now, but no promises

Marten Seemann: quic-go won't implement it

##### 5. Intent to implement and deploy

No hum, but there are at least some clients and servers that would do so. It is a non-trivial amount of traffic.

Design:
- SHOULD/MAY spin/echo
- If spin, MUST opt out (some traffic)

Martin Thomson: This is essentially what Brian articulated. I'd like to defer the negotiated versus discretionary discussion

Mark: I wanted that too; some people seemed to gate their decision

Martin: I'd like to litigate that after the fact

Christian: Yes, we have a spec in the spin bit draft. The mechanism to not spin is to provide an anonymity set, the observer cannot detect that the client is trying to protect a particular path. We don't know how to build a foolproof anonymity set.

Christian: The threat of differentiated traffic is a concern about operators harming their own networks. The other concern is about spies watching you and identifying sensitive traffic.

Bob: To state the obvious, you're already exposing your five-tuple. But an operator would never go to that level of discrimination.

Sanjay: Penalizing for not being able measure RTT would be shooting yourself in the foot.

ekr: Is this a hum for the general design space, right?

Mark: yes, with room to improve.

Mirja: You can always block QUIC traffic as a whole. So if we're so concerned about differential treatment we should stop working on quic as a whole.

##### 6. To include the spin bit in the specification, as laid out here. Some decisions can still be made.

**Yes: Strong hum (4-5 hums for inclusion, no against)**

**No: Medium-Strong hum (less)**

Mark: Seems like 65% in favor. I don't think we can walk away from the discussion.

Lars: Seems like rough consensus to include the spin bit.

Lars: We have a proposal from Brian. That's the starting point. Kazuho has some different design stuff, so look at that discussion.

Martin: I want to conclude the negotiation idea. I think it's a bad idea to negotiate.

Mark: Ten minutes for this.

Kazuho: I think that version negotiation gives a better signal to the observers. They can use the the VN to know that it's spinning. It also provides a way to evolve from the endpoint and middleboxes.

That said, it's only one bit. I'm not strongly opposed.

Ted: Thank you! I strongly believe that making this discretionary is far better for anonymity. The discretionary use is more likely if there is a version explicitly.

Martin: I'm with Ted. You need to lose the signal upon migration to avoid linkability. Gives much more options.

ekr: I concur with Martin and Ted. Negotiation is a bad idea. Extra complexity.

Marcus: As a consumer, I wouldn't trust the version. I can use a signal to ignore spin, but that's it.

David: Agreed, I don't like negotiating.

Mike Bishop: +1

##### Hum: No negotiation for spin bit support?

**Yes: Strong hum (several hums on jabber too)**

**No: Nothing**

Mirja: Are we ready to merge?

Lars: Yeah, go for it. Ask Martin and Jana.

Christian: I'll probably give another PR about when to opt out.


### Planning

We have an interim in January in Tokyo. Go to quicwg.org.

Registration ends on December 18. Please register early. Akamai location.

Charter/Milestones has us shipping QUIC RFCs in November. That seems unlikely ;)

The goal is to freeze -17 to let implementers interop and build their full solutions and find inaccuracies.

We push back the milestones to July 2019, Montreal.

We want deployment experience in this time before then.

We can have other discussions about what to do next for QUIC. Interest in these areas:

- Multipath

- Partial reliability

These efforts should merge their work, rather than having to hash it out in the WG.

Ian: To clarify on the last point, the hope is to deploy -17 at global scale. That's the intent, right?

Lars: Yes, that's the intent. We can -18 if we need to make it better.

Martin Duke: To clarify, if we "freeze" -17, what's the status of open issues? Are the rest punted to v2?

Mark: We have the v2 and Parked labels. We can look at Parked, and consider them.

Martin Thomson: I've gone through all parked and v2 issues, and my view is that we can have very short discussions on all of those. My expectation is that parked with either be closed or merged as minor, or punted.

David Schinazi: I agree with the goal to get experience on -17, but would it still be reasonable to test the extension mechanism before we ship? Can we get some experience with one extension first before we go to RFC?

Martin Duke: If we talk about next steps, I'd like to consider adopting load balancing.

Jana: I expect some churn in the recovery draft, just to let people now. We should continue to engage there.

ekr: Following up on Ian, one thing that didn't go as well for TLS 1.3, we had a bunch of small draft versions, and it got annoying to interop. It may be better to have larger checkpoints.

Mike Bishop: With subsequent small drafts, if there's no wire image change, just editorial, we could have a "version number to use" and stick on an old one for editorial only changes. We can skip versions.

Martin Thomson: Let's not discuss now what the interop goals are, take that to the list.

There was a QUIC human rights review done outside the WG. It was on the agenda to get feedback, and that is being done in the human rights group.


