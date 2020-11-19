# QUIC Working Group - IETF 109

Scribes: Dmitri Tikhonov, Robin Marx, Dan York

## Administrivia - 5 min total

* Blue sheets
  * Meetecho does the bluesheets
* NOTE WELL
* Agenda bashing
  * Lars: I moved MP discussion down

**Lucas**: use Meetecho tool to put yourself in the queue

## Hackathon / Interop Report
5 min - Recap of interpo at hackathon (interop sheet) - Lars Eggert

**Lars**: Nothing special to report.  Interop Runner continously testing.  That will go on for foreseeable future.
**Lars**: congrats: we're past IETF Last Call

## Base Drafts Discussion
30 min - Placeholder for any needed discussion on issues raised during IETF Last Call

[Slides](https://github.com/quicwg/wg-materials/blob/master/ietf109/quic-issues-status.pdf)

**Jana**: We had 129 issues during last call. Most from area reviews, just a few from wg participants. Closed 74 of them as they were minor/editorial/no action issues. Left 55 open, but many are very trivial (26 are proposal ready). 25 in the last 2 days, so no proposals yet (mostly IANA+area review). Only 4 that are older than 2 days that don't have proposals.

**Jana**: of open issues only 2 marked as design, have proposal. 3 issues left with active discussion on GitHub. Does anyone want to discuss these?

**Magnus**: Can we spend a little more time on issues regarding  IANA registry?

**Lars**: raised by stewart and genart reveiew. For vnums no registrty defined, just question of which document they should be in. Ideally in invariants, but there is a bunch of text about policies we define for registries, and that text is in transport. Question if we need to move/replicate that. 

**Jana**: Discussion probably hasn't moved too far on that. Feel this is discussion with ADs/chairs. Seems it's not a discussion to have with entire wg.

**Magnus**: This is something all people specifying future extensions will have to deal with, so wg should pay attention to this.

**Martin Thomson**: I put in a PR for this in the Transport doc, because that's easier to do. Don't see much added value in putting it in invariants. 

**Magnus**: I'm fine with that

**Martin**: Saw number of comments but none of them are particularly troubling. Questions of where to put notes (my pref = nothing). Rules around the first value (my pref= follow your suggestion). Can we look at the issue?  #4378 (from memory) - IANA review of -transport, question 3. Provisional assignment or early allocation. PR saying first value in any space follows standards-action space: follow RFC7120. Please check.

**Jana**: I haven't had a chance to look at this yet

**Lars**: What makes sense?  We'll settle it one way or the other, none of them will be terrible

**Jana**: Wanted to support what you said on the other issue about having vnum descriptions in v1 in transport instead of invariants. Invar is focused on protocol specific things, this is about process, doesn't belong in invariants. 

**Martin**: I've done review of all open issues. Aside from h3 or qpack, I'm satisfied we've got PRs for most, other questions can be answered via email. 

**Lars**: That's it in terms of issues.

**Lucas**: Wrt HTTP issue I raised, I think that'll probably be closed without action, but maybe small editorial tweak we want to make. Probably not more to say there. Can Mike Bishop maybe comment? 

**Lars**: Intent going forward is, IETF last call is closed, do another revision of the draft set that rolls in all of the changes. Hopefully that'll give us a clean slate. Then go to IESG review sometime in December. Probably in 2 steps: taking invariants transport TLS recovery on 1 telechat and H3 qpack on a 2nd telechat to make easier for IESG to review. Question is what would happen then. Ideally then to RFC Editor queue, or might have to do new round of revisions. We'll know in December. Hopefully in the new year we'll have drafs in RFC Editor queue and hopefully be finished later in Q1. 

**Lars**: Have been asked by implementers that want to ship quicv1, what should they do? My take is that once the drafts are in the RFC editor queue (after IESG approval), I would consider it safe to call yourself v1. Only editorial changes would happen in RFC editing. It's your call though.

**David Schinazi**: strongly disagree with that. Fundamentally we need bakin' time. We need to deploy this and know it works. For TLS 1.3, found out it was broken. Luckily we found it and fixed before fixed. This -can- happen while it's in the RFC queue. Probably not huge changes, but still changes. Our goal is to make a good standard, let's not rush.

**Lars**: Don't remember timeline for TLS. Don't know if that came up during RFC editing. One point: this question came from implementation that has some release windows. Question is if they can make that window or have to wait. 

**Martin Thomson**: Two things to say.  First, David is too cautious.  If we have to burn v1, then we are OK to use another version.  No emergency, can add antoher version.  The salts will have to change between last draft and final release. Hoped to do it later.  If IESG approves it, we can do it in AUTH48.

**Lars**: We could do it in RFC editor; we can figure it out later.

**EKR**: When TLS interop problems were found, that was before IESG review. I'm between Martin and David. True that there's nothing special about codepoint 1. However, problem is if we don't know when people are deploying with cp 1. If substantial portion does, and we need to make change in RFC editing, and continue with cp 1 because we don't know about broad deployment. We need to discourage people from using cp 1 until RFC is shipped. Just continue to use the -29 cp. Not like it's a large change. We don't have perfect knowledge. 

**Matt Mathis**: As example of where too early commitment an fail: language ambiguity found in an earlier document. Releasing the version before the document is fully done is dangerous.

**Martin Thomson**: We can interpret my suggestion here that is if we want to revise the document, we also need to move to a new vnum. Bit confused by what EKR was suggesting. 

**EKR**: Right now, if people deploy... If we're prepared to commit to v1...  People should wait.  That's why we have things like RFCs.

**Jana Iyengar**: Want to remind people we're already deploying quic -29. So v1 should be just another revision. I don't think v1 is any special in this regard. We will have change in salt though. Customer aspect: they ask: "is v1 ready?" Doesn't make sense to wait for RFC editor to fix semicolons in the text to call v1 done. I see no reason to wait for RFC editing before minting v1.

**EKR** There are not just colons and semicolons. Found many non-trivial changes in TLS 1.3 from looking at it with fresh eyes

**Ian Swett**: We deployed h3-29 quite widely, in Chrome and Google servers. Performance seems quite good. Don't have overly large concerns about technical aspects of the draft. 

**Spencer Dawkins**: We've had conversations about not having a QUIC v2 anytime in the foreseeable future but just using extension mechanism a lot and not rolling new vnums. Seems like that's going to be an important part of this answer. I agree vnum shouldn't be special, you just need to support them. 

**Lars** Queue emtpy, we're pretty much just on time. Will eventually also go into a late  stage process of the ops drafts. Jana will discuss this with editors in the coming weeks. 

## QUIC-LB: Generating Routable QUIC Connection IDs
10+10 min - Discussion of the QUIC-LB draft - Martin Duke
[Draft](https://tools.ietf.org/html/draft-duke-quic-load-balancers-06)
[Slides](https://github.com/quicwg/wg-materials/blob/master/ietf109/QUIC-LB-IETF109.pdf)

(Martin Duke presents)

**MD**: I presented similar slides at 108.  Got feedback, deleted some algorithms that were satisfying to delete.  Ian and ? gave good feedback.  I was able to open-source some impls. encode and decode.  nginx is a load balancer.  That's available, just waiting for a server impl, let me know when you have that, we'll interop.

**MD**: next slide.  Addressed Ant critiques.  Request for UDP proxy protocol.  Ops does not have right people to get feedback.  No feedback from big cloud providers on L4 balancers. One last appeal for some guidance here. 

**MD**: (next slide) First two bits for every CID are for config rotation. If you're rotating your keys, take a time for servers to catch up. Proposal to make it into 3 bits to deal with SNI switching. 

**MD**: (next slide) MegaCloudCorp with one huge shared config where all clients could change would lead to security issues. In practice, need to run different configs. If it's in the ClientHello you're going to need something that is in every packet. 2 options: a) multiple configs separared by these config bits. Solves problem of having mutually mistrustful customers able to reach each other's mappings. But is still globally visible (circumvents things like ECHO). b) alternative is to share configs manually. More difficult for attackers to position themselves. Tradeoff, my pref is towards b. 

**MD**: (next slide) in violation of QUIC transport.  Keep this in thbe draft (plaintext CID).  INtroduce TP "hey, I'm doing this, but if you're concerned, don't migrate."

**Ian**: Any time you have one domain name to one IP, you have immediate linkability.  I don't know what to do about that -- this is best effort, the world is not perfect.

**MD**: Agree. One lesson I learned from LB is that there are no guarantees. But ECHO exists for valid use cases and don't want to break them with this.

**MT**: Two things. 1) this is the same server we're talking to, then it's indeed just one IP. But this text is about services. You're creating smaller anonymity sets for diff customers. Analogous to having separate IP for servers in the backend. At that point you're back to what Ian says. Depends on how many people are using these servers.

**MD**: I am glad to hear you're comfortable.  I am.  Do you think the TP is worth having?

**MT**: No probably not worth it. We'll find out in time, but wouldn't start with something like that .Don't know what we would do with that information.

**MD**: OK, there is PR on GH.  Put comments there.

**Ian**: I agree with MT.  It's not worth it.  We can have 10,000 conn or more going to same machine.

**MD**: (skipping 4 slides) #35 was resolved recently. (next slide) There's a list of the things you need to configure to make this work, but no really config mechanism. Haven't really had any feedback from people on what to do, so would appreciate some input. 

**Eric Kinnear**: We are chatting with our CDN folks.  Hey there is this QUIC thing, can we make it work?  They are involved in early renditions of ? stuff.  They are happy with later things.  Thank you for putting so much effort into this.  We have peolple who care a lot about what's going on.

**MD**: Will wrap up after this meeting.

## Manageability/Applicability of the QUIC Transport Protocol
5+5 min - Final steps on the Applicability and Manageability drafts - Mirja Kühlewind & Brian Trammell

[Draft applicability](https://tools.ietf.org/html/draft-ietf-quic-applicability-08)
[Draft manageability](https://tools.ietf.org/html/draft-ietf-quic-manageability-08)
No slides, see [github issues page](https://github.com/quicwg/ops-drafts/issues)

**Brian Trammell**: 3 open issues. 1 has PR, 1 does require some discussion (normative language or not), 1 has bit of text to add. Had some discussion on these docs in hallways and mailing lists and issues. Are getting more participation than last year. I'm here to say that the train is leaving the station. After these 3 issues we're planning to submit another revision draft and have that go to WGLC before next IETF. If you have anything that you'd like to ask/say, you're running out of time. 

**Mirja Kuehlewind**: Think we did address #115, just didn't close it. 

**BT** By end of week, we'll have docs ready to rev.

**Lars**: That makes sense. Want to have people take a look at this. Going to WGLC is a good trigger for that. 

**BT**: Look at issue 100, was waiting for base drafts to stabilize, to make sure section numbers are correct etc. Think we're ready to go now. Thanks to everyone 

**Lars**: Did a show of hands to see who read some version of these drafts this year. (Results are 16 read and 28 not read). Argues for longer WGLC of 2-3 weeks to let people take a look. Don't have to wait for this though, can already send feedback now!

**MK**: We've been reading other docs and try to reflect.  Figure out whether anything needs to be added or removed, not just agree or disagree.

**BT**: WE've cut some things over the time we've been editing.


## As Time Permits
Subject to reordering

* 5+5 min - Discussion of the QUIC Version Aliasing draft - Martin Duke
[Draft](https://tools.ietf.org/html/draft-duke-quic-version-aliasing-04)
[Slides](https://github.com/quicwg/wg-materials/blob/master/ietf109/Version%20Aliasing%20IETF109.pdf)

**MD**: improve greasing and privacy of QUIC. Basic idea is that you start with v1 and server gives you TP with various random numbers. (next slide) Client takes all that data and in a subsequent connection uses the random vnum/salt/token/length offset. Server can then compute salt and offset from that. For connections after the first, initials are fully protected and cannot be decrypted by outsiders.

**MD**: (next slide): didn't touch QUIC bit yet, also some issues with doing this for packet type. (next slide). Makes initial packets entirely private and immune to ossification (prevents TLS ossification on initials). Deals with injection attacks. However, doesn't cover first connection, which is a main concern. Also, if no large deployments are interested on this, probably not useful to move on. Maybe steal some things from ECHO/use ECHO to apply to the first connection. Wanted to know if there is any interest in continuing to invest in this idea.

**Christian Huitema**: It's interesting to find something that makes conn more robust.  if we want to, add additional checksum to make sure things are not messed with in transit.  Prevent 3rd party to mess with packets and make packets not observable by anybody.  The latter is a bridge too far.  To sum: I'd like to look along those lines, but goes for auth rather than encryption.

**MD**: I'm trying to combine things to maximal results. Some people in chat are saying this is more about greasing and not about privacy. If that's the main thing, we can go back to Marten Seemann's original proposal of just having 3 versions per server that are used. 

**Lars**:  It'd be intersting to hear what direction people think this should go towards.

**David**: This is useful. Helps reduce ossification risk, but only slight privacy improvements (think we're overselling these atm). Just need to do some evaluation of priv/sec aspects. We should spend some time on this. I'd like for Google to implement this. 

**Lars**: Increase greasing, then?  Is that what you're interested in?

**David**: Mainly interested in making ossification harder. Privacy is secondary, as it makes observability slightly more limited.

**EKR**: The question to ask... Is this ECH and should it just be QUIC ECH? Differences I can tell is that it only works from second connection. We looked at this type of design for ECHO using the PSK mechanism as the seed and wouldn't need SNI. Same problem: if you lose state, no way to recover. In your proposal, there is a way to recover _(didn't quite follow this)_. 

**MD**: I'm trying to bring in some ECH concepts, but not ready for prime time. Does have some different properties than ECH. e.g., server initial is also entirely protected, but not sure this matters. 

**EKR**: THe idea would be you'd hoist some of this info into QUIC.  Can you do that?  I don't know.  This is reasonablty complicated already.  If we don't have to solve it twice, would be good. I am with David, let's take a look and see what the options are.

**Eric Kinnear**: I would second David's comment. Interested in greasing. Worth spending time to see if we can get security and privacy wins. Even if it takes us v2 to deliver this, it would still be very interesting. 

**Christian Huitema**: Just a comment on EKR reuse of ECH or other TLS things.  I worry if TLS message grows larger than one packet then TLS solution won't be adequate.  We have to take that into consideration: is it worth it to increase size of TLS packet?

**Lars**: Let's take it to the list.

**MD**: Cautious enthusiasm.  Please comment on GH or mailing list.


* 5+5 min - Discussion of the Network Address Translation Support for QUIC draft - Martin Duke
[Draft](https://tools.ietf.org/html/draft-duke-quic-natsupp-03)
[Slides](https://github.com/quicwg/wg-materials/blob/master/ietf109/quic-natsupp-ietf109.pdf)

(Martin Duke presents again) (he's on fire today)

**MD**: NAT can lead to black hole when migration happens or you can end up breaking QUIC security model. So this draft just says: please don't do this. (next slide) Not exited about adding PROXY protocol myself. (next slide). Don't really care where we put this. Currently in separate draft. Could put this in ops draft or reference it there, etc. Want to hear thoughts from people here.

**Lars**: If we decide we need text along these lines, prefer it in the Ops drafts.

**MD**: Everyone's indifference is as great as mine

**Gorry Fairhurst**: Having separate draft is good if people just implementing NAT have something small to look at. 

**Lars**: People who build NATs don't look at RFCs.

**MK**: I wouldn't want to ref an expired draft from ops to prefer separate document. I think we can have a shorter version in ops draft or merge the whole thing. No real pref. 

**Spencer**: Back to Lars' thing about reading RFCs.  However people who buy NATs might.  Maybe put ? in the abstract.  _(did not get that last part)_

**MD**: I'll send a PR, that's what people would prefer me to do.


* 5+5 min - Discussion of the 0-RTT-BDP draft - Nicolas Kuhn
[Draft](https://tools.ietf.org/html/draft-kuhn-quic-0rtt-bdp-07)
[Slides](https://github.com/quicwg/wg-materials/blob/master/ietf109/draft-0rtt-bdp-vf.pdf)

**Nicholas Kuhn**: Idea is to add new TPs when re-connecting with 0-RTT. Bandwidth estimations based on in-flight data or RTT estimates. Could be used to share past parameters so clients could adapt their request or improve 0-RTT performance. Has been implemented in picoquic with TLS 1.3 and Matt Joras using BDP_TOKEN. Would like input from the wg. 

**NK**: Have some early evaluations using picoquic PR. go from 4.3s (no 0-RTT) to 3.4s (0-RTT) to 2.9s (0-RTT with this extension). 

**NK**: Unclear on the precise mechanism: BDP_TOKEN vs NEW_TOKEN.

**Matt Joras**: Some context:  We're developing something for FB broadly similar.  But server informs the client about network characterstics.  Use QUIC frame to do it.  Makes sense for server (for us) to do this stuff.  Ours and this idea are compatible.  Perhaps send this frame as part of 0-RTT.  either peer can contain this frame.  I am a proponent of frames for this sort of thing.  They're easy to add and use.

**CH**: Two parts: There are a bunch of things that come from idea of ... _(missed this, sorry)_  The other part is remembering what peer did before.  The consensus it need not be standardzied as it's specific to implementation.  They can use some sort of cache or token.  They'd do it with NEW_TOKEN as it's a much better fit because it can be sent at any time in the connection.

**Lars**: Kazuho is agreeing with CH in chat

**Ian Swett**: Doing it in the NEW_TOKEN is relatively safe. Is more of a tsvarea thing to figure out guidelines. But I don't see why we need to do anything in QUIC for this. I feel we already provide good mechanisms in QUIC to accomplish this and think NEW_TOKEN is a good example. Think it's more dangerous than it's worth to further specify this for QUIC. 

**Lars**: A whole bunch of agreement in chat (Praveen, Christian, Dragana) with what Ian said

**Jana**: Agree with Ian. Why does this need to be explicit? If this is just going back to the server, we can just make this opaque to the client. 

**NK**: Discussion on the list -- clients can adapt their session preference depeding on what they have.

**NK**: Last slides: next steps might not be what we envisioned before (NK is disconnected)


* 5+5 min - Discussion of how to progress qlog (main schema, QUIC and HTTP/3 events) - Robin Marx
[Draft main schema](https://tools.ietf.org/html/draft-marx-qlog-main-schema-02)
[Draft QUIC H3 events](https://tools.ietf.org/html/draft-marx-qlog-event-definitions-quic-h3-02)
[Slides](https://github.com/quicwg/wg-materials/blob/master/ietf109/qlog_IETF109.pdf)

Robin Marx presents

**RM**: (slide 2): structured logging review, useful for debugging and analysis.  Cong windows, good for privacy, log just what you care about.  easy to build tooling.

(slide 3): >70% adoption, notable FB in production -- it can scale and work in practice.  IMplementation that don't use qlog use something similar.  General concept is solid.

(slide 4): still  just personal draft.  Few people dealing with day-to-day work.  Time for addl discussion how to progress it.  Who is going to do it and where to do it?

(slide 5): four options - nothing - interim/DT - adopt in QUIC WG - adopt in another WG.  Enventually I think we'll go with (4).  It's useful beyond QUIC.  Would take too long to do something generic.

**Lars**: I think the use case is very much QUIC and specifically TCP-based workloads already has tooling.  It fills the need for QUIC.  I think (3) is reasonable.  It does not preclude doing (4) at soem point.

**Martin Duke** Want to see QLOG draft adopted by QUIC WG.  It's the general tol for this.  As far as core QLOG, conceptutally, not the right place, but practically, why not just do it here?

**Eric Kinnear**: QLOG is great, we've adopted it.  Nice privacy win.  Being able to visualize is very nice, esp. with HTTP/3 priotization.  Both useful and in helping conceptualize impact of changes.  It's useful for WG and implementations and deployment. I disagree with Lars.  I want to bring it to TCP.  Yes, there are tools, but QLOG is already as good as most of those tools.  Quicly becoming apparent that QUIC elicits "oh this is cool!" response.  Value of having all of that in one place.  Let's make it really robust.

**Robin Marx**: It's not so much TCP, it's more new app-layer protocols.  Lots of potential there.  BGP and that kind of stuff.

**Ian Swett**: I support this work.  Having it for H2 would be amazing.  Expanding it to more transport would be hugely helpful.  More CC information in there.  I hope to work wityo7u on ethat.

**Jana**: Thank you for this work Robin.  QLOG becomign defacto standard.  Many impl. support it and continue to support it.  Let's include it as part of QUIC WG.  We need to have tooling.  Seriosly good tooling, QLOG is.  Tooling is that people love, QLOG is what people read.   We're adopting QLOG the format not QVIZ the tool.  Let's not expand QLOG scope, then, to include TCP.  Let's not cast too wide a net.  Let's have QLOG be specific to QUIC.

**Lars**: This distinction is interesting.  What's the model for jointly developing qviz or similar tools?  Strong deps between format and tools.  Nee dto have discussion about it.

**Matt Joras**: Thank you.  QLOG is first thing I go to.  I support WG adoption.  Defacto standard.  QUIC WG is the logical place for it.  It's reasonable path fwd.  Another WG not much sense: it would be same epeople.

**Lucas Pardue**: I hoped this would come up: it's taken us a year from -01 to -02.  Large burden on Robin.  Not a criticism.  Hopefully people can contribute if we have more governance over this text.  As individual, I support adopting it somewhere.

**Lars**: Robin is doing by himself other that doing his thesis.  If we're adopting it, we would encourage people to chip in and help out.  Both spec and developing and visualization tool as well.  Everyone would benefit.  Will continue discussion on the list.  Leaning toward (3) and (4).

## Planning & Wrap up

**Lars**: Let's see what else we can adopt.  MP is what's left.  We'll try to recharter now that base drafts are done.  Taliking to ADs about new text in Charter.  Extensions?  There will be draft versions of charger.  Not planninng any more interims.  No topic requires an interim.

## QUIC Multipath
30 min - Placeholder for any needed discussion based on the status of the mailing list discussion min - Future meetings, implementation drafts, etc.

**LE**: It's been freeflowing.  There has been some directions that became clearer.  SDome people belive that what we have in draft is enough.  It's not TCP-MP, but some say what we have it's enough.  Other say we need concurrent MP use.  Let's see if we can come on agreement.  Please be brief and get into queue.

**Ted Hardie**: Exegesis is not important (?).  Things changed since charter was written.  QUIC has changed as well.  My take is that MP in QUIC now don't work without multiple connections.  If you want it within single transport, you would make it a first-class element of some verion of QUIC.  Decide isn't MP, but whether it's apps doing MP using QUIC.  Will it be a baseline version of QUIC or a parallel version of QUIC.  All are on the table.  I'd prefer concurrent MP as a version of QUIC.

**IS**: Want deployment experience.  New version of QUIC is sensible.  We've been deploying QUIC for six years.  You can widely deploy something and then come back to IETF.

**Spencer**: I think one of the Qs to ask was: we're talking QUIC do all the scheduling for MP or having app do that.  At least 2 people mentioned on list of coming up with common layer on top of QUIC.  Im curious: how many more other people thought of that.  Second: agree about experimenting and getting back to WG.  I thank WG for talking about MP.  I try to do some analysis in draft I sent to QUIC list today to understand what diff. people mean by MP and how they hope to use MP.
 
**Eric Kinnear**: I want people to experiment deploy and get back with comments.  No need for RFC to get that experience.  Demonstrate benefit.
 
**Jana**: At high level I don't think MP should be in transport.  Useful in long term, but long term.  Now, however, we spent a lot of time building conn migration.  One of two design issues we caught was around migration.  Gift that keeps on giving.  I expect more dragons be there. If people want to experiment I encourage them strongly  Consider mechanisms already in place.  Even if we replace those mechanisms, replace them meaningfully.  There is a distinction between use and design of protocol that accomplishes MP.  Because MP can be used with QUIC.  I want to see how it gets used.

**CH**: Question that: should MP be new version of QUIC?  In practice, we can do a lot with extensions.  Datagrams, delayed acks -- same kind of complexity as MP.  We can experiment with MP building on extensivility of QUIC protocol.  See recent discussion with Kazuho on the list.  We're *almost* there.  Let's experiment.
 
**Dmitri Tikhonov**: Want to point out that we just had a presentation about Multipath use of QUIC. Why is that not valid? Didn't you guys like it? I liked it. 

**Lucas Pardue**: (chair hat off, literally). Similar to Jana and Christian: we're still trying to take this transport layer and map H3 on top as a fully flexible app layer protocol that mainly uses QUIC for its primary goal of removing HOLblocking. This will be a good test of implementations to see how they use congestion and flow control. Too much focus on using MP to solve performance problems of QUIC impls right now probably throws away bandwidth on trying to do that by other means (e.g., extensions like delayed ACK). Let's be careful in applying solutions to problems that are unique _(didn't quite catch this)
  
**Erik Kinnear**: I agree with that a lot.  Let's not throw MP at problem.  We deployed MP.  The problem is not technical, but policy.  And cost.  If we want industry change, if we want to see a change in cost structure, then more people would be interested to deploy MP.  If we advocate that it won't be a big policy problem, we'd be wrong.

**Jana**: Completely agree with Eric. Want to re-emphasize what Lucas pointed out. One of the thinks that made MPTCP slightly easier was that it was operating under a single byte-stream. So the constraints on it were pretty clear on what the receiver needed to do. QUIC has multiple streams and need priorities. Takes scheduling problem of multiple paths to multiple streams over mutiple paths. This is a performance problem; Mark Handley did some early work on this. He found that it was critical to pin some streams on some paths to get perf benefits for HTTP. For other use cases it might be different, but for something QUIC generic, we need to consider the basic streams building blocks. 

**Spencer Dawkins**: At least one per  IETF meeting I point out that there is a conv in Jabber to take note of.  One point in slack during virutal interim (I think it was Matt) that the difference between use cases were that some people  use H3 versus those who would not.  We hear people say remove path restriction for connection migrtation.  What's the diff betwen that and MP support?  I suspect the difference is between those who use H3 vs those who would not be.  Again, thanks for doing this.

**Mirja Kuehlewind**: Disagree somewhat with Jana. Scheduling is indeed complex, streams make this slightly worse. But it's not a problem we need to solve completely now. It's like congestion control; can't optimize fully. Just looking for basic scheduling schemes that support basic use cases to start with for now. Also looking into getting signalling into the protocol so experimentation can start. Signalling itself isn't that difficult, can be quickly agreed upon, which would be useful for sparking experimentation.
  
**Lars**: Desire for more experience and experimentation. Questions is if the WG needs to do anything here. Can just use a private version (e.g., see Alibaba who's done that). I don't see a need for the WG to do something MP-related to further enable something. It's very clear we won't change v1 for this, definitely only future version/extension. 
  
**Ted Hardie**: Example that Martin Duke gave for LB is what I am looking for.  Share experience, compare implementation notes.  The support does not nee d to be more than that in the beginning.  Having the context -- MD came to WG to say there is this thing in the transport Draft I have to relax -- is that OK?
  
**Lars**: so be a forum for discussion of results and if there are needs to change the basic specs. 

**Mirja**: We don't need experimentation on e.g., if we need multiple PN spaces. We need experimentation on if and how people would use MP. But that only happens if people have a ref protocol they can use. Not all applications that are interested would want to implement their own thing. 

**Lars**: there are already impls. that do one version of MP.

**MK**: why have multiple flavors of MP?

**Lars**: I don't see why we need to do any spec work to enable further experimentation.

**MK**: design question, not experimentation question.

**Lars**: I disagree. 

(We are running really short on time now)

**Jana Iyengar**: I agree with Lars. This is 100% question of experimentation. People can do that today. Just because we specify doesn't mean people show up and start experimenting. It should be the other way around. So we should do what Ted proposes: let people present experiences but not protocol design. 
  
**Lars** See you on the mailing list and on the Slack.  Bye!
  
  