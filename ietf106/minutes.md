# QUIC Working Group Minutes - IETF106 Singapore

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Tuesday 19 November](#tuesday-19-november)
  - [Hackathon / Interop Report](#hackathon--interop-report)
  - [Issue Discussion](#issue-discussion)
    - [2792 Timing side-channel on key updates](#2792-timing-side-channel-on-key-updates)
    - [3111 Version ossification](#3111-version-ossification)
    - [3212 Remove requirement for handshake to complete before KeyUpdate](#3212-remove-requirement-for-handshake-to-complete-before-keyupdate)
    - [3020 Transport parameters are too constraining](#3020-transport-parameters-are-too-constraining)
    - [3159 Do not accept 1RTT before handshake completion](#3159-do-not-accept-1rtt-before-handshake-completion)
    - [2863 QUIC Discard Handshake Keys](#2863-quic-discard-handshake-keys)
    - [3197 Active connection ID limit defaults to 0](#3197-active-connection-id-limit-defaults-to-0)
    - [2602](#2602)
    - [2143 more conservative about migration](#2143-more-conservative-about-migration)
  - [Triage Issues](#triage-issues)
    - [3189 Add loss bits to unencrypted header](#3189-add-loss-bits-to-unencrypted-header)
  - [QUICv2 For HTTP/3?](#quicv2-for-http3)
- [Wednesday November 20, 2019](#wednesday-november-20-2019)
  - [Planning](#planning)
  - [Issues](#issues)
    - [David Schinazi:  #3014 (Corrupt retry packets)](#david-schinazi--3014-corrupt-retry-packets)
    - [3094](#3094)
    - [Refs in Recovery](#refs-in-recovery)
    - [3265](#3265)
  - [Datagrams](#datagrams)
  - [Version Negotiation](#version-negotiation)
  - [QUIC Load Balancers](#quic-load-balancers)
  - [Interop Runner](#interop-runner)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Tuesday 19 November

Scribes: Brian Trammell and Tommy Pauly


### Hackathon / Interop Report

Martin Duke: 7 clients, 11 servers. Worse than usual, attendance not great and -24 dropped recently enough that 3-4 teams not ready to go. Pretty successful. Basic protocol functionality in good shape. Some implementations doing mobility stuff, some implementations doing push, we'd like to see more.

David: Some implementations doing datagram interop

Jana: There was also testing of the docker testing infrastructure for QUIC implementations.


### Issue Discussion

#### [2792](https://github.com/quicwg/base-drafts/issues/2792) Timing side-channel on key updates

ekr: Discussed in Montreal. If you receive a phase 0 packet and phase 1 packet. If valid, update keys. If invalid, []. Keyphase bits are not AEAD, attacker can flip bit and force processing / failed integrity check. Could probe keyphase since key update takes more time. Therefore keys should be computed in advance. However, spec also says no more than two keys retained. 

mt: draft currently says SHOULD, ekr argues MAY. Don't care. There can be the timing side channel, but that's often OK.

mt: Any objections? (nope) Will create a PR.


#### [3111](https://github.com/quicwg/base-drafts/issues/3111) Version ossification

ekr: defer? we thought this would be simple in Montreal. we have discussed. it appears more complicated. maybe requirements creep. we will have a relatively long period of draft/release overlap so the corresponding risk of ossification seems less high in deployment. Let's use an extension once we're actually deploying. Not in v1.

mike bishop: part of why we need the negotiation discussion tomorrow. we need some idea of how to detect fallback. need to adjust scope to pull all into v1 or push it out. ekr's proposal is reasonable.

Kazuho: this works only for large providers that own two sides. we can punt this.

david schinazi: +1 ekr. if this becomes an extension, that's ok. goal is to prevent downgrade middlebox. establishable with large providers only, chance we deploy is high. can defer.

Ian Swett: Pulling this in without VN would be a disaster. Punt.

Jana: Also agree with ekr. Put this aside in the interest of moving forward. Put it on the sidecar.

Marten: Just deploying versions of QUIC might not be enough to prevent ossification. Extension is also valid.
    
Martin Duke: Put in the sidecar with QUICLB and Prio

Mark: we'll talk about extensions tomorrow


#### [3212](https://github.com/quicwg/base-drafts/issues/3212) Remove requirement for handshake to complete before KeyUpdate

Martin: Document currently prohibits key updates until connection confirmed, but there can be updates as soon as 1RTT available.

Kazuho: There is another key proceeding 1RTT, clientside 0RTT, confirmartion gives us time to retire 0.5 key.

ekr: channels something isaid, not what this issues says. this says text in spec is redundant. Point 2 implies handshake confirmed, but that is an extra test that is redundant. we should hold off on evaluating this. other point, we could have laxer key update rules. point of this rule is to reduce ambiguity with only one keyphase bit. as soon as you have 1RTT keys to send, you can send the next phase becauase the other side can't be confused. we can relax that rule if we want.

Christian: revisit this after the handshake done issue. editorial change OK.


#### [3020](https://github.com/quicwg/base-drafts/issues/3020) Transport parameters are too constraining

David: main extensibility joint is 16-bit transport params space in IANA registry. almost all of this is spec required. experimenters may want a codepoint without writing a spec but it's 256 codepoints, there could be collisions. correct fix is to tweak the registry. PR 3109 fixes this. 

Martin T: Provisional registrations can go anywhere, expert review for the entire space, some advice on reclaiming codepoints. won't go into detail. let's discuss this on the list. 

ekr: provisional registrations are essentially free? (yes)


#### [3159](https://github.com/quicwg/base-drafts/issues/3159) Do not accept 1RTT before handshake completion

Martin T: this goes to core of design philosophy. we have tried to maintain impossibility of stuff we don't want people to be able to do. however TLS allows server to send 1RTT packets before it should be able to. implementations would get 1rtt secrets and start accepting packets. how can we prevent this? if we want to change TLS, that would be disruptive. would rather in PR [3224]() just make the normative language stronger.

ekr: this is a misfeature of tls, we have had some discussions about fixing it. ok with merging now.

Martin D: I have a different proposal here, lots of QUIC, fewer TLS, you can't just pull TLS off the shelf. right place to specify this is in the interface between TLS and QUIC, that's the narrower part of the waist in a full-stack implementation (PR [3174]()) but happy to merge Martin T's.

David: yes let's start this conversation in TLS, pick it up in v2. interop should test for this. OK with merging this.

Martin T: putting tight requirements on the implementation is not the right thing to do in the spec, but Martin D is right that this is the right place to implement. Don't want to mandate implementation structure.

Roberto Peon: not possible to ensure an conformant implementation will not have this defect. is it possible to ensure the remote can probe? (yes)


#### [2863](https://github.com/quicwg/base-drafts/issues/2863) QUIC Discard Handshake Keys

Slides: https://github.com/quicwg/wg-materials/blob/master/ietf106/QUIC_Discard_Handshake_Keys_IETF_106.pdf
    **NOTE** no slides available in meeting materials; please keep these synced from github!

David: we have a solution (see slides), DT can live with it.

ekr: i'm fine with this. note that this will not work if we want to do server-side migration.

Brian: Should I file an issue for this problem with server-side, and tag it QUICv2?

Roberto Peon: of course, server side migration is much bigger than just this.
    
Jana: To Brian's point, we have great analysis from ekr. Let's not lose that.


#### [3197](https://github.com/quicwg/base-drafts/issues/3197) Active connection ID limit defaults to 0

Eric Kinneear: PR [3201](https://github.com/quicwg/base-drafts/pull/3201) also covers [3193](). default needs to become 2, because [reasons]

Jana: earlier we were thinking differently, but this model makes sense. i have comments on the PR, can be resolved, not fundamental.

Martin Duke: why is 1 invalid if not supporting migration?

Mike Bishop: if you're not supporting migration, why would you need a second CID?

Eric Kinnear: you can change without migrating. you need two so the server can give you the preferred address TP. 

Mark: it sounds like there;s more discussion to happen here. work it out and finish the PR, we can CfC in the next batch.

#### [2602](https://github.com/quicwg/base-drafts/issues/2602)

Jana: needs no discussion. has a PR, close to done.


#### [2143](https://github.com/quicwg/base-drafts/issues/2143) more conservative about migration

Eric Kinnear: last status in Cupertino, went through the text, should be in good shape 

Martin T: I regard this as editorial, but the size and scope is such that we need to look at it. Relatively happy with direction last I looked. Fairly big project, strange that it is late in the process. Please to read this. Will review, lot of text.

ekr: +1 please read this, if it does not accurately characterize your expectations then please raise that.

Christian [missing, attack based on unauthenticated IP addresses]

Eric Kinnear: I believe the current text highlights the attack and that it lists capabilities of that attacker. Please take a look


### Triage Issues

#### [3189](https://github.com/quicwg/base-drafts/issues/3189) Add loss bits to unencrypted header

Mark: We've discussed this before, we had a separate issue that we wouldn't do this in QUICv1. Issue was locked, since we need to triage. Personal take is that making it an extension will be most productive. We would need a big privacy and security review if we were to take this.

Igor Lubashev: There's discussion in TSVWG. Spin bit gets delay but not loss to the path, and many operators want to see this. There was a lot of discussion already for spin bit, and we adopted that. There wasn't a proposal at that time for a loss bit. However, now we have code implemented for a loss bit. I think there's a lot of interest in the community. We want WG engagement to do a review of the new draft. We can do a QUIC extension draft by the interim.

Roberto Peon: I would like to ask what the layer of the protocol is. We're smooshing layers a lot in QUIC, but we're stepping a layer
too deep to add these things. It seems sad to solve this in QUIC and not solve for other protocols. This should be a lower layer.

Mark: Our options are:
    - This is in scope
    - This is out of scope
    - We ask for an extension draft

Brian Trammell: It sounds like Roberto wants a new IP version =) This sounds like PLUS! More seriously, there are two questions here: do we want to replace the fact that we had implicit signals with explicit signals; and do we want *this* proposal. It's REALLY late to have this conversation. While it's nice that Igor is eager to do this fast, but it's late. I'm concerned that this as an extension mechanism is very different from a lot of other extension mechanisms, and is a lot bigger. Maybe we discuss how many bits are laid aside in v1 for extensibility. The answer is less clear than the spin bit, but if we do end up deciding that we want to do this, it would be a shame to realize the bits are not available.
    
DKG: (Jabber scribe) 

Ian Swett: If there is some small change we can make to v1 to make it possible to experiment here, I am amenable to that. QUICv2 would be mch better.

David Schinazi: The decision to add one bit for latency we reached took a very long time and a lot of energy. Research takes time. I didn't see anything that warranted revisiting consensus. I think this can work as an extension. Can't commit to security and privacy review, but would be open to participating. 

ekr: Certainly, this should be possible in an extension mechanism. If there is some reason we can't do this, then we should fix that now! I'm not in favor of having this in QUICv1, it opens a can of worms. We don't have the resources as a group to do the right review on this work right now.

Chris Box: My day job is running mobile networks. Reiterate the need to understand packet loss. Without that, network deteriorates. How it's done, don't care. Now or later? Don't want to wait too long. We don't block QUIC, we have no intention of blocking QUIC, p

Gorry Fairhurst: I think the use of bytes we call transport is what we do in TSV. IPPM is here. We need to stop going on about the later. It's part of the area, we should do this. Is this proposal right? Don't know. Spent so much time not talking about this. 
        
Igor Lubashev: There was opinion that we should do nothing here. I disagree. Google deployed QUIC on UDP. Pragmatism is in the spirit of QUIC. Meanwhile TSVWG is talking about how to do measurability the right way.
    
Ted Hardie: Clearly we must do this or people might deploy ECN, and we must prevent that. I am happy to work on this if it is not gating for V1. Do not set aside bits now. We need a real design process. 
    
Martin Thomson: This is going to take longer than I'm willing to tolerate. Want to be done this month. Want a little deployment experience. Can also participate in analyzing these sorts of things.
    
DKG: Please do not make this required for QUIC v1.
    
Kazuho: Let's do it in V2 as an extension. Setting aside bits for experiments also interesting. Needs to be agreement between client and server to run experiments, because both need to know what the risks are. Need a transport parameter for this.
    
Christian: This is really important when the vast majority of traffic is QUIC. Not there in V1. Happy to work on it. Later.
    
Jana: Not part of v1. Separately. We probably don't want to design optional bit-signals until we have experiments that show that the first signal will actually work.

Tommy: Not appropriate for V1. Very useful to look into. It will be a much better mechanism if we wait. Moving implicit signals to explicit is not something we have done before, we need experimentation with this.

Brian: How many people are willing to look at the privacy analysis *after* v1?

_(About a dozen or more hands, about the same as the spin bit)_

Mark: I'd suggest proposing an extension. Not clear whether this is on the agenda for Zurich or for Vancouver.

Gorry Fairhurst: As TSVWG chair, try and make sure there is a home for this. If there are central mechanisms, we should do this in TSVWG. If there is energy here, do it here. Make sure we have only one home. 


### QUICv2 For HTTP/3?

Slides: https://github.com/quicwg/wg-materials/blob/master/ietf106/ALPN.pdf

Mike Bishop: What do we do for the alpn interface? Has implications on Version Negotiation. You currently can't get to alpn before version. There are ways to do them simultaneously, though.
The list of Alt-Svc combinations can be very complicated.
H3 can't define how it will interact with future versions.

Martin Thomson: We need it to be the case that implementations of these combinations will be understood by the other side. A server should not be able to pick H3 on Q2 when the client does not know what that is.

ekr: Why is that a big problem? TLS does this. Seems theoretical.

Mike Bishop: What do we do with non-HTTP? If you negotiate transport, then negotiate the app layer, you might end up with weird inversions. This is just a tradeoff: is the token for the full stack, then it's inflexible but simple. If you just negotiate by layer, it's cleaner but more complicated. TLS says applications can restrict which transports. 

martin: since 7301 everyone assumes different things about how alpn operates. philosophical Q. dont have to decide now. we can accept the ambiguity.

tommy: Definitely update the h3 document. We shouldn't say either "needs TLS" or "needs QUICv1". Rather, describe the transport services required by the QUIC protocol, and point to the transport document to indicate the features. We shouldn't decide our future path until later. We can have philosophical discussions in TAPS if you want =)

mark: we are now a tsv group talking about a security group's idea of what an app is

??: ??

david: conceptual intf from tls to app is a bytestream. The layering model of QUIC partly causes these problems. However, I think that we can't predict the future. We should focus on what we have today. The idea of defining all of the properties is hard. We shouldn't be confused about what fits on what. Contain it to what we know today. We can add a 1 page RFC later to say that things work with v2, and use a new alpn.

Brian: agree with david. you might think you can layer these things but the interface is complicated, the details will always pick it up. TLS used ALPN to abstract away application, should have been called ASPN ("application stack"). I think the bigger discussion lands on identifying stacks, not composing layers, but it's more complicated that that. let us defer this: H3 -> Q1, let Q2 fix this.

ekr: Perfectly fine to say h3 is QUICv1, and we can address that later. Also, QUIC can't define the meaning of ALPN—that's TLS. Also, note that DTLS is another thing with ALPN that you can't just run other protocols on.

Jana: I don't think we need to parse this here. ALPN says what sits on top of TLS. In this case, QUIC AND HTTP sit on top of TLS, so the combination form makes sense conceptually. We'll come up with new versions very soon, and we don't necessarily want to tie their revision lifetime. The problem that shows up in scaling, and we can punt that problem.

Mike: Some support for H3 = Q1, some support for H3 = Q1.get_abstract_properties()

Kazuho: What does feature mean?

Mike: We have been careful to design away from complicated feature combinations.

Jana: Can we actually specify H3Q1? _peanut gallery: that's just spelling_ no i'm speaking in favor of stack.

Tommy: as one of the people who brought up the mapping, i almost want to see a minmal PR because I don't think we want to open that wormcan. it'll be fun to work on mapping, but in taps.

Kyle: _missing_

ekr: the minimal thing here is h3 -> Q1. one thing we did in TLS. _too fast_

dkg: just say H3 -> Q1. The idea that the working group can describe Q1 as properties in reasonable lifetime 

nick: can we also H3 -> Q2 in the future?

mike: yep, we can do that in the future, but we need to figure out rules for mismatch.

jana: clarification point. agree that h3 -> Q1

mark: two hums. first hum: close issue with h3 -> q2. second hum: try and describe properties of Q1 for h3. 

first hum: loud as hell

second hum: crickets


## Wednesday November 20, 2019

### Planning

Mnot:  there is some discussion of extensions and other documents later today, and the chairs and ADs have been talking about how things go from there.   We're hoping that the drafts will settle down and that the editors will take that time to ensure readability (so editorial-only PRs).  At the same time, we're looking for more implementation and deployment experience, so that we use that to inform the RFCs.  We're going to hold them for publication for about six months after they have been WG last called.  Because of that pause, the wg capacity can turn to extensions, new applications, and potentially new versions. Those extension discussions should be limited, not a flood, and work on other applications will go into BoF or other WG processes. There is an interim in Zurich, mostly focused on closing out v1, but there may be some time for extensions there.

Christian:  I like the idea of pausing before the publication, but if you are not doing the IETF Last Call, you are not getting the feedback from other areas or participants.  I am concerned.  I think that might extend the later IETF Last Call people.  

Praveen: I like the idea of doing an IETF call as well is a good idea.

MT:  Based on this week, the next version of the drafts may be the one we are looking to take Last Call.  I think we are in pretty good shape for that one.  For Christian's concern, we can go to each of the directorates now, and get cross-area review that way.  That will happen during the period running up to the interim.  The directorate feedback can be folded into drafts prepared just before the interim. 

Christian:  At the same time, you cannot expect review from multiple directorates to change nothing.

Brian:  Expanding slightly what Martin Thomson said:  press the button for the directorate review, that's simple and we should do it.  If there is concern that is broad enough, we can send an early pointer to either ietf@ietf.org or last-call@ietf.org.  Pipelining this is a good idea.

Sean Turner:  We have some running code form TLS 1.3, you can send a bunch of calls (twitter!) that warn people it is coming, and that tends to work.

Ekr:  Basically what Sean said, plus a couple of other things.  Seems like a solid plan.  Bike-shed is that issues not raised in last call or out of order later, but that would not be the case here, since we're still looking at making changes based on implementation and deployment.  

David Schinazi:  Good plan, like it; from our implementation kind of thing, as this quiet period will mean we're not chasing a moving target, and we can actually get it into production.

Jana: Clarification question: are we talking about all the documents or some of them.  

Mnot:  I think we have been assuming all four documents.

Jana:  We have not yet moved all of the documents to the same internal state.  

Mnot:  We also have not talked about ops and management document.

MT: This quiet period gets them a chance to catch up, because they have the same chasing a moving target.

Mnot:  If you do think you have an extension which is generic enough,we will reserve time for it during the quiet for disucssion on the list. For this, we will need a charter change for that, but we've been talking to the ADs about that, and we'll put a proposal out for comment.


### Issues

#### David Schinazi:  #3014 (Corrupt retry packets)

David summarizes the issue Kazuho raised.  Retry packets are more fragile to accidental bit flips during connection establishment, because they are relying on UDP checksum, which is optional.  The proposal from Cupertino was to add an integrity tag to retry packets/ See related PR #3120.  Last question: what hash to use, and they propose GMAC, in order not to introduce a new dependency.  Martin suggested using the initial salt as the initial secret.

Ekr: two point: re-using the initial salt is not good cryptographic.  Aside from that the question is whether the retry token should be encrypted.  Costs AEAS operation or two, but really XOR over a fixed mask.  There are two ways you go here; one is the way the PR describes, the other way is to an AEAS operation but use on the connection IDs as a none.  

David Schinazi:  I get that you have really good instincts about cryptography, and that re-use is generally bad.  But since this in the spec, this looks more like a beauty context issue.  From my perspective, this is a bike shed, and I'm totally in favor of flipping a coin to decide.  

Praveen:  Are we trying to get protection beyond what a UDP or IP checksum would have provided?

David:  You do not know what IP version you are using.  With a checksum at the IPlayer some boxes (v4/v6), the checksum would be cleared.

Ekr: It's true that the ciphertext is not distinguishable from random, but in one of these, it is less clear that the header is similarly indistinguishable.

Chris Wood: (Missed comment) 
    
Martin Thomson: Does anyone seen this as a hill worth dieing on?  (No).  We are clear we don't want to do HKDF, since it is expensive, but the other three points on the spectrum:  integrity tag; fixed key; use something from the original message as a nonce. I suggest we just do a beauty context on those? 

Ekr: Do people understand them?

MT: Repeats to the mic.

Kazuho:  I think of the two first options, just doing GMAC is preferrable to XOR, because then you have to manage the possibility that there are different salts for different versions. 

Martin Duke:  You had a use case where Nick's experiments looked to expensive.

Martin Thomson:  That was based on the HKDF operation being expensive, where the AEAS opertions are cheap.  There is a cost, but it is very hard to measure it.

Jana:  Does this effectively mean that the Cupertino agreement remains? (Yes)

Mnot:  We're going to hum on the three options:  no encrytion(in the PR), fixed encryption(an integrity check +fixed key), changing encryption (integrity check which uses a fixed key and a diversifying nonce).

Christian:  I have the impression that the second option brings nothing, let's hum first on eliminating option 2.

Mnot:  If you believe we should have no encryption, humm now (some)
If you believe we should have integrity protection with a fixed key and a diversifying nonce.

Jana: I'm going to suggest we just shift this responsibility over to the PR authors to work out. 

Ian Swett:  We should circle back with Nick Banks about the chance that the more encrypted version is a blocker.  

Mnot: if we just say no to encryption, is anyone going to lie in the road? 

Mt:  That assumption is based on a presumption of expense.

Mnot: Take the discussion to the issue then. 

David Schinazi:  Some people assume that something is cheap and some people assuming it is expensive.  If we take it to the list, this is just going to drag on, can we just do a coin flip. If we get more data, we can re-open. But we are mostly getting new opinions, not new data.  

Jana:  I don't think you can find a solution in list discussion, given the disucssion on the issue and in the room.  He supports either merge it or do a coin flip.

Roberto:  We did a hum for what people like and we can also do a hum for what people don't like.  That might be elucidating.

Mnot: Does this change your mind, ekr?

Ekr: No.

Mike Bishop:  Does anyone care to give us data on the cost?  

Ekr: Christian just gave us data.

Christian:  The data is very simple.  That operation runs at 20 gigs at a windows stack.

Praveen:  (inaudible)

Moving on to the other documents:  Recovery is up first.

Six open issues.  


#### [3094](https://github.com/quicwg/base-drafts/issues/3094)

Ian Swett: We need input on #3094.  He would prefer not to merge, but he wants to know whether the guidance from the WG is that the pseudocode should cover MAYs as well as shoulds. 

Vidhi (lost meetecho connection to her when she started speaking)

Jana: The pseudocode is merely a guidance to understand the text.  The text is normative.  The extent to which we want to add guidance for this, it should be in the text. 

Vidhi again got lost by meetecho 

Eric Kinnear:  It does say that we SHOULD be pacing, so it seems like the pseudocode should have a  copy of what you might do to meet the need. There would be alternates, but having this would be nice.  

Gorry: Let's keep the main path really clean.

Andrew McGregor:  
    
Roberto:  (Old habits caused him to say he came from Google, which gave laughter).  

MNot:  heard general support for having something.

Reviewed other issues on the list, to see if there were ones that had not been assigned editorial but not otherwise marked urgent.

#### Refs in Recovery

Jana:  We have references to the TCP RFCs, but Gorry has pointed that we don't have any linkage to the constants we use aside from those.  Proposal is to make the references normative. 

Gorry: I think it would be useful for it to be normative.

Jana:  This might be a downref. 

Martin Duke: why not copy the MUSTs into this document and make an information reference to the existing docs?

Ekr: That seems like a great solution.  The purpose of the text to explain, and pointing it to that is a informative reference. 

Martin: Should have a normative reference or not?

Ekr:  What a normative reference means if you have to read the specification to understand what to do. There are lots of security docs which are full of references that explain why we made choices.  But we don't need to understand it to implement it. You can just take the number and go.

Jana: There is a slightly different question on the reference to RFC 8085. The question is whether we should have a normative reference to it. There is a PR #3248 that addresses.  

Ian Swett:  I think this is a reasonable choice (Christian chimes in yes).

MT:  This PR is fine, but the issue is badly worded.  RFC 8085 provides the requirement to have a congestion control algorithn, and that's why it is normative here.

Ian Swett:  If you care about the headshake deadlock, please check that issue and the linked PR.

Praveen:  (again could not hear, sorry)

Over to HTTP: What issues do we want to discuss.


#### [3265](https://github.com/quicwg/base-drafts/issues/3265)

Mike Bishop:  The most thorny issue we already discussed. #3265 is probably next in line.  This is requesting some that is new to HTTP and kind of not.  This is a request that we can send bodies at any point after the body has started.  I don't what this might break.

Kazuho:  I don't have a sense that this is a problem, but this might be better in HTTP.

Mnot: With various chair hats on, will coordintes with HTTP since some are not in both.

Patrick McManus:  Looks okay, but the commitment of the group was to port over functionality from HTTP and this got dropped from HTTP/2 for lack of use.

MT:  Looks kind of cool, but this should come from HTTP.

Lucas:  Is this push-specific?

Roy: I don't think there is any connection to push responses that would connect to trailers.  I don't have a lot experience with those  stretching across.  But I believe this is in scope, because this is taking over the HTTP/2 version 2 work, and this is a change to the previous version.  I think this is within charter now.

David Schinazi:  If there was a use for this, someone would have built this as an extension to HTTP/2.  Maybe not universally true, but this is trivially implemented as an extension, and this is not popular enough to get into the current version.  If this gets widely used, we can bring into the next version.  

Martin Duke:  No technical merit issues, but I'd rather see this come from HTTP and then we'd try to get it in based on schedule.  

Mnot: If the semantics are clarified in HTTP core, we can try to bubble into HTTP/3.  As an individual, I think it is pretty cool, in particular because it is backwards compatible.  

Roy will open an issue in HTTP for HTTP core. 

Mike Bishop:  most of the others have a pending resolution.  We might be better served by the other presentations.

Now moving to presentations, Datagrams first.  


### Datagrams

Eric Kinnear:  Unreliable datagram extension. (See slides).  Basic use case is reliable signalling stream/control stream and unreliable data.  We want this in QUIC, rather than DTLS, because we want to share handshake with existing reliable data. The design has simplified greatly, thanks for the comments. Flow control limits do not take Datagram frames into account. Feedback from implementors has been positive, and there were some at the Hackathon.

Question about adoption of basic datagram document (not H3 binding)

Mike Bishop:  Notice you reserved two adjacent values, where we are now at random allocation.  Can we ask for randomly allocation of two?  Good question, probably can make it work.

Roberto: I'm certain we're going to adopt this but it is scary for me as it is interesting for proxies, especially in flow control.  It might be good to insert something about intermediaries with no flow control are going to have a bad time.

Chris:  I think this is good direction, but this is a change to the security posture, because which packets get retransmitted turns out to leak.

_Some dispute_

David: Can you file an issue on the draft?  (yes)

Mo:  I'm in favor and it needs to be sooner rather than later because there are a lot of other groups who will need to weigh in on this.

Martin Duke:  I'm in favor, but worried about bandwidth.  This is a bit beyond walk and chew gum at the same time.

Colin: As a minimal base for the functionality, this is reasonable.  But before we finalize it, I think we need more experience about this to figure out what the functionality needed looks like (e.g. does everyone use FLOW ID).

Ian Swett: appreciate all the simplifications. Makes it much easier to reason about. 

Brian:  Mo and Lucas are right: do it, do it now.

Jana: I think this is useful in another way, because it exercises our extension function.

Mnot: We'll talk among chairs and ADs and move from there.


### Version Negotiation

David Schinazi: Version Negotiation. (See slides).  Downgrade prevention of original invariant version and load-balancing issues have a hairy interaction.  The discussion was blocking v1, so it has move to an extension.  Two goals:  downgrade prevention and no use of an RTT.  Compatible versions are defined. Goes through the transport parameter.  

MT:  Client and server have to check that these match?

David Schinazi: Yes.

Document needs an editorial pass...

Mark: Does the working group need this extension, is this a reasonable starting point, now or wait?

Ted: Could we use ALPN with a full stack as opposed to just an app, would that obviate the use of this?

David: No. This is for the transport layer. Without knowing client version there, you can't get ALPN.

Roberto: What happens in the 0RTT case? Yes, we need this.

David: 0RTT is per-version-specific, but work to figure that out, esp with versions with 0RTT

Kazuho: Important work, but, only need version number change when the handshake exchange changes. We need a different kind of version for [...?]. This one doesn't address all downgrade cases. 

Martin Thomson: We need .... a lot better ... work ... incompatible versus compatible upgrades is important. don't block v1 on this, treat it like the other extensions, because we will need a story for v2. 

ekr: author, should adopt this, have misgivings about incompatible negotiation. 

ian: we should adopt this. editorial work ... 

roy: http/1.1?

david: no minor versions in QUIC yet. please put that out to the list.


### QUIC Load Balancers

Mostly about servers and load balancers implemented by different folks to work together.

This turned about to be a useful vehicle for several other problems. This also turns out to be useful for syncookie offload. Changes value statement from "QUIC tolerates no L7 middlebox" to "QUIC tolerates only explicitly trusted L7 middleboxes".  

Martin goes through the linkability problem, and then shows common configuration schema. Then next bit is "how do you get the configuration around".  You can ship it around using anything you want, but there is also a simple in-band method described.  Feedback on this has been "varied" (from "We should never to use this" to "a few tweaks" to "just pick something that already exists").

Other discussion points: linkability server decisions affect the client.  Retry services are version specific but CID parts are not.  Is OCID actually easier than crypto versions?  Engagement with cloud load balancer vendors?  The low-state vendors have been hard to engage with, but they should give us feedback.

Mnot: please focus on whether this is the right working group, right time, etc.

MT:  I like the model, like the framing, don't like the protocol, and I think it should be separate.  This looks a lot like some ops and nm work, so YANG models will probably enter in here at some point.

Martin: I cracked open the YANG spec, then hoped I could get someone to to the YANG model for me

Praveen:  This ... important ... [missed it]
    
Mirja: I think Martin mostly said what I wanted to say.  It is easier to rip off the new protocol, and the algorithm is also separable, and I wanted to add to more work on manageability.  
        
Tommy: We should adopt it now, and split out the protocol work.
    
Eric Kinnear: People trying to deploy things at scale on the server side will need guidance in this area, and I think that will make the difference between a QUIC that many people can deploy versus a small number can deploy

Speaker from Verizon: the syntax doesn't matter much; some will express this as YANG, some in other ways, but we are definitely ready for adoption.

Manasi:  Ready for adoption

Manasi: adopt it

Roberto: +4

Mark: we expect a revised, pared-down draft. I have no uniform feedback on a lot of issues, do some coordination and bring it back for adoption.

### Interop Runner

Jana: Marten Seeman and I have been working on QUIC Interop Runner; introduced in Cupertino, had a couple of implementations then, now we have 6-7. We have managed to get most of the tests in the interop suite. Value of this is you can run interop at any time. You get logs. If you don't have your implementation in, then please do so. [slides are here]() but were not shown