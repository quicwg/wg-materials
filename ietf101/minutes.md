# QUIC WG Minutes - IETF101

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Monday, 19 March 2018](#monday-19-march-2018)
  - [Hackathon Update](#hackathon-update)
  - [EDITORS UPDATE](#editors-update)
  - [QUIC DTLS and Stream 0](#quic-dtls-and-stream-0)
  - [Invariants](#invariants)
- [Thursday, 22 March 2018](#thursday-22-march-2018)
  - [Invariants](#invariants-1)
  - [ECN](#ecn)
  - [Spin Bit Proposal](#spin-bit-proposal)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Monday, 19 March 2018

### Hackathon Update

7th or 9th interop.  Usually happens before each interim and at each Hackathon.

[Interop Matrix](https://docs.google.com/spreadsheets/d/1D0tW89vOoaScs3IY9RGC0UesWGAwE6xyLk0l4JtvTVg)

Yellow is good.  It's looking promising.  Hoping to go to http.9+ in Kista.
Will share doodle poll for virtual interop meeting.  Based on version 5 (draft-11).

A rust implementation exists (link) and isn't included in the Interop Matrix.

IF YOU NEEDED ACCESS TO THE SLACK CHANNEL ask the CHAIRS!

### EDITORS UPDATE

Went through all the issues (before people added new ones).  Ian explained what tagged, assigned, closed tags mean.

Fixing HTTP Priority for QUIC Request IDs discussion: Proposed mechanism didn't generate a discussion.

Connection ID Privacy discussion: Resolution close with no action ...

Prime client with connection ID for O-RTT discussion: Proposed mechanism didn't generate a discussion.

QPACK: adopted QCRAM and renamed in QPACK.  How far should we diverge from HPACK?  For discussion ...

Handshake Corder Cases: Will be discussed later.

PADDING and PING: discuss .... or the editors are going to make something up.

Christian: Surprised by padding ACKs.  Congestion control is done by sender.  If a sender congestion control strategy requires ACK padding ACK ... Prefers Option 2 - if you need it acked used a PING.

Patrick: If it's for padding for cover traffic and it's not participating ...

Jana: Adding a ping bit - there's a problem with this because it might add toward congestion control.  ACKs fly back and forth.

Mirja: Padding should not be part of congestion control.  Data rate should be low anyway.  Just use a rate limiter.
Ian: A good suggestion.

ekr:  Need padding for CH.  What is padding for here - is it just for cover traffic.  ought to just a frame - it's an application thing and not a transport thing.

Martin: Came to the same conclusion that Patrick did.  The risk is ACKs do congest the network.  Can avoid problems by just not sending them.  The value from ACK padding is pretty low.

Subodh: Agrees with Patrick too.  Hiding the difference between ACKs and real data is dubious.  Suggest 2a (what Ian said)

Jana: Seems reasonable to not ACKs towards bytes in flight.  Allow the sender to set it.
Ian: This is pretty complex.  But, we don't need to specify it.

Christian: We have other frames that not acked.  Like path challenge (it is now acked).

Resolution: Three options (two on slide third from the room): Will get a slide on Thursday...


### QUIC DTLS and Stream 0

Ted: Is slide 9 what would if stayed the current structure?

ekr: Yes.

Ted: These crypto streams are now reliable.  This has application beyond crypto.

ekr: The other property is that they have exemption from other rules (e.g., congestion control).

Ted: You are creating a marriage of convenience ...

Ian joins the stage ... thinks we can do better.  Swallowing all of DTLS is a lot.  we might beat DTLS into whatever we were going to do.

PHB: Likes it.  Seems to solve my problem (aka web services).

Brian: Stream 0 is icky.  It's going to look like this.  Is there a way that we can get there if want to do it later?  

Ian: we'd have to work that out.  

Q: does this make co-existance with gQUIC easier or harder.  

Ian: more thought required.

Mike: Part of version negotiation includes that crypto protocol and now it's pinned to TLS.  If we move to DTLS we're pinning it to all versions.  

ekr: we'd just move invariants be DTLS invariants.  

ekr: There's lots of flexibility wrt wire image.  

Mike: special cases stream ID 0 vs byte this or that is kind of the same thing. 

ekr: only once change would be to get ride of stream 0.

Spencer (as AD): 1. chair picked for a reason. 2. expect WG to make informed decision. 3. coming off TLS1.3 is a recharter. 4. (as Spencer) don't have a good feeling about version negotiating and how much we might roll them.  

mnot: not going to wait 5 years for v2.

Chris: Echoing Spencers #2 comment.  It would be good if we had time to experiment with it.  We should definitely consider it despite scheduling concerns.

Jana: 1. this is devil we have. Packetization if it's going to sit in DTLS - loosing ... 2. shame spiral starts a little earlier - qQUIC had tight integration and we decided to give that up on purpose.  3. I don't if this is the right architecture - not sure this is solved by thinking about this a a layer - having a reliable transport on top of UDP is valuable.

Christian: Would prefer an incremental approach.

Victor: handshake, transport, and layer.  Decided to do just layer and thinks that the way to do it.  Don't want to duplicate the transport.

Ted: Identified a problem and with a solution.  If we have to impose changes on DTLS it will take more time.  keep the work here.

Patrick: From a code point of view: surprised how much of an impact it made - removed 4 times as much dode.  Hacked it up.  Core question is do we want wide or narrow API ... We should talk about the wide of the API.

Subodh: Who controls the bytes on the wire is important.  Having transport own the bits is valuable.  It's fixable.

Colin: Seems like this might be better conceptualization.

Andrei: Thanks for bringin this up.  Better to have better API.  A lot of people are not happy with DTLS services.

Kazuho: Concerned about congestion control.

Gabrial: Concerned switching horses would adversely impact interop.  Issues with stream 0, but we shouldn't go crazy because of that.

Tommy: Concerns about DTLS reliance.  What would happen if we just did QUIC running it's handshake.

ekr: Did talk an alternative where DLTS Packets = QUIC packets.

Martin: For some people this is a feature and for some it's a bug.  There's some duplication.  When you duplicate the functions you don't necessarily have to duplicate the code.

ekr: Next step is to explore.

mnot: Not hearing this is crazy talk.

Ted: Would prefer a single proposal so we have a way forward.

Martin: If we look at two proposals neither change the invariants.

Ted: Is there anybody interested in determining slide 9 and the coalition of the willing.

mnot: 20+ people interested.  Email chairs if you're interested.

Lars: This is going to move the milestones ...


### Invariants

Only one thing left if we're not changing packet layer.

Connection ID is what's left.  

Colin: short header packets don't allow demux. mt: correct we do not guarantee that.  Colin: if we could that would be good.

ekr: As a practical mater there's a way to figure it out.  Need to make that the version negotiation doesn't affect invariants.

?: Is version 32 bits set?  It would look better if it was 16bits.

mnot: the intent is to do the WGLC and then park it.

Jana: why would we park it?

mnot: we don't know the future.

Martin: there's really no upside to publishing.


In the WILD!

https://quic.netray.io





## Thursday, 22 March 2018


### Invariants

The version negotiation packet is a list of versions. No length, no anything else. This was semi-intentional, but that's not discussed. 
Is the rest of the packet non-extensible? How should these be specified as invariants?

Ekr: Is this proposal like TLS, with a bunch of bytes at the end?

Martin: No specific proposal here.

Ekr: I’m reluctant to just have a length.

Martin: Purpose is to agree, between client and server, on (1) the way to obfuscate handshake packets and (2) the handshake protocol itself. We could have another layer of negotiation inside that. I think we're actually okay with what we have, as long as we are aware of this limitation.

mnot: Do you want a hum?

Martin: Not sure, we may want more time as a group. It should just be another last call comment.

mnot: Could we do a hum to see what people feel though, without a decision?

Mirja: The length might be on the safe side to be future-proof, but I don't have hard feelings about it.

ekr: Is there a length in the long header? (NO) We could do things if we are desperate like add some magic value that means there is an extension bit

Ted: Very similar to ekr's point. The interpretation of what comes after the versions is either uninterpretable or will get very crufty.
    
Jana: We have a lot of extensibility in other parts of the protocol; if we need this in the future, we can solve that in the future.

mnot: We have a sense at the mic that we don't need a change here. Add to issue status.

### ECN

Lars: In the room in Melbourne, the consensus was that we wanted to add the full version of ECN to QUIC v1. This is an overview of the PR.

Ingemar: Proposed additions to QUIC transport and recovery are up on the Github. No major changes since Melbourne, main discussion was around connection migration. Worked with Gorry to clarify those parts. There was an email discussion around ACK_ECN feedback format. Rough consensus that counting packets was good enough.

Way forward is to create the Pull Request into the draft based on the issues to add the text.

Mirja: Remind me, is there an indication in the handshake that ECN is supported?

Ingemar: If you receive an ECT-packet, you should use ACK_ECN to feed back that information.

Mirja: So you probe the connection at the start, rather than explicit signalling?

Ingemar: That's right.

Mirja: The sender may not know if the receiver can receive ECN bits until trying and failing; why not signal explicitly.

Ingemar: We wanted to make things as simple as possible and not modify the packet much.

Mirja: Testing is more complex than just telling; you may have to test anyway if the path doesn't support it, but at least you could know it's not supported.

Magnus: It's not testing, it's just trying to use it and seeing if it works.

Lars: There's a page on the wiki that covers the design from the team; review. Do we want to see this in -11 or -12? Let’s do -12.
Fifth implementation draft will be based on -11 and TLS -28.

Ekr: I don’t know what the other plans for TLS 1.3 are, but we’re planning on staying on -28 until the RFC ships.

Mirja: The testing is not QUIC specific, but an approach that could be used by other protocols.

Martin: Let’s spend more time polishing the ECN text in the Wiki before the pull request. PRs will take time. I think this will take weeks not months.
People won't be implementing this even once it's in the document, so it's not a huge rush. Not hard, but some work.

Jana: Seconding Martin's opinion; this is useful, and let's make the Wiki solid, no rush to get this in immediately—it will get in.

Lars: Okay, please take a look at what's in the wiki, everyone! Let's get it ready for PR in June timeframe.

### Spin Bit Proposal

25min - Spin Bit overview + clarifying questions ONLY, Brian Trammell

mnot: Brian will give the presentation on Spin Bit first, with clarifying questions; and then afterwards only will we have discussions.

Brian: I have backup slides that we may use during discussion.

mnot/Lars: Our intent as chairs is to get something decided and discussed on list today. We want the whole IETF group here to discuss and review this, and we need to close on this soon.

Brian: 

    What is the spin bit? It's in PR 46, and we want to take one bit of the
    QUIC short header and make it spin. The server sends the last bit it saw
    from the client; the client sends the inverse of the last bit it saw from
    the server. It creates a square wave.

    Why? We are preparing for a post-TCP world; we see measurements for QUIC
    rising globally, and we have a loss of latency visibility as TCP gets
    replaced. Many use cases are enumerated in the spin bit draft. Lots of
    troubleshooting, buffer bloat mitigation in routers, etc. In hackathon, we
    built a proof that the spin bit can reduce buffer bloat significantly! The
    period of the pulse between the 0s and 1s is based on the RTT, so a passive
    observer in the middle can observer the flow round trip time. If you can
    observe both sides of the flow, you can separate out where the RTT is spent.

    Three separate implementations of spin bit at hackathon, very easy to
    implement and get working. Due to ack timing in QUIC, the information from
    the spin bit is more accurate RTT than checking after the decryption. Does
    this work in non-perfect networks? In heavy loss, you'll estimate too high
    of an RTT slightly.
    
ekr: What is the graph? (slide 7)

Brian: The spiky area at the beginning of the graph is the spin bit information available at the sender side, with a moving minimum (smoothed RTT). The lower graph is the server's view of the same thing. We induce a latency from 40 ms to 80 ms part way through the graph.

ekr: And anyone can see this?

Brian: Yes

ekr: Why are the client and server different?

Mirja: You only have acks in one way, so one direction is less accurate.

Brian:

    Currently, packet numbers are still in the clear in -10. So it's easy to
    detect loss, etc.
    
    In conclusion, we've talked about this for a year, and we've done
    implementations to get experience with it. This gets you pretty good RTT
    information, to all the points where the transport flow is viable. Explicit
    signalling that replaces implicit, and based on last summer's work, doesn't
    create a large privacy issue.
    
Dave Oran: Does this change at all when we do multipath?

Brian: This would need to be kept on a per-subflow basis (depends on multipath approach).

Ian Swett: Do you have numbers for how things degrade at 5%, 10%, etc loss?

Brian: Random loss or burst?

Ian: Usually a packet policer.

Brian: With burst loss, you get what you see in the blue line on slide 14. Vanilla on this slide is without looking at packet number at all; if things are running well, you don't need packet numbers at all, you just need spin edges.

Ignacio: When you say it overestimates upon loss?

Brian: It's because the edge gets delayed, and so your visible RTT goes up.

Colin: Have you run into issues with reordering on low RTT?

Brian: Yeah, looks like slide 13. With lower RTT, less absolute error. With 40ms RTT, and you have reordering, you get thrown off with values too low. A heuristic can be done to reject impossibly low values.

Colin: What is unrealistically short?

Brian: If less than one tenth of expected RTT, generally.

Colin: This is only for short header packets, right?

Brian: Yes, you can get the RTT from the handshake. You don't have many long header packets. It's not worth the complexity to add to the long header.

Christian: I have a fear looking at the numbers that the spin bit is very good when things work well, but will degrade when the network has problems. This behavior goes against the notion of a measurement tool.

Brian: Thanks for leading into the backup slides =) We looked into a mechanism called the edge-valid signal. When you have heavy loss and heavy reordering, the edges get lost, and you have fewer samples. We never drop all the samples, we just lose some. The number of valid samples lets you know how bad the network is. If we don't have packet numbers, you have two bits going up from 0-1-2-3 to indicate when there is a valid edge. What we saw here was that even when we disable flow and congestion control, with very high jitter and delay (the transport falls over) this still works.

Christian: To summarize: if we have a visible packet number, we only need 1 bit spinning; if we don't have packet numbers, we need 2 bits spinning. Martin pointed out we only need three values (1-2-3) and lets 0 be invalid/no signal.

Igor: We're discussing RTT measurements, but can we characterize loss patterns with the spin bit?

mnot: Out of scope

Brian: Yes, but we think the edges will let you know there is loss OR reordering, but not which. More work needs to be done.

ekr: Please never again say three-bit-spin-bit

Brian: It would be a spin bit and an edge vector

Markku Kojo: Does this assume a continuous flow of packets to work?

Brian: If the sender is application limited, you'll get overestimates. The sender can expose whether or not an edge is valid.

Mirja: The second bit helps you, but even if you just have one bit, just don't spin and mark this as not valid for measuring (no edges)

Eric Nygren: If you're switching what paths you're sending on, how do we handle that?
Brian: That's a good research question.

Subodh: There's some map between the flow and the packets, what is that?

Brian: That's the five-tuple

Colin: To clarify, this is limited to middleboxes observing the traffic on path - the bit(s) is/are authenticated ened-to-end.
    
5min - Scope of discussion - chairs

mnot: To give context, we've been discussing this for a long time with a lot of controversy. We had a design team to identify privacy issues with a one-bit spin bit. We had concerns about if the data was usable or not. Do we want to add the spin bit to the specification or not? We are not talking about loss, etc, just talking about latency measurement for the spin bit.

Brian: Yes, let's add this.

Ted: I didn't hear the question, so I can't just say yes or no! Having gone through the work with the design team, I'm confident that this is a good bang-for-the-buck tradeoff. Extraordinarily small risk for privacy, with good benefits. The sender is in full control of this, and the server only does reflection. The sender can control if things are on; and so can the server decide not to reflect. Another good piece is that as we move into multipath, we can use this on a per-path basis, without trying to be too complicated. Definitely in favor.

mnot: What is "this"?

Ted: I've mainly looked at the one bit spin bit, with the packet numbers. My intuition is that this is very similar in properties to the vector and no packet number; that may be an overall privacy win.

DKG: I appreciate how this has been whittled down. I want this as small as possible; 0 is great; I appreciate the work for 1. The discussion earlier was about bursty traffic. There may be other traffic patterns for which this doesn't work, also. For non-reliable streams that don't use acks, are we designing ourselves into a hole? Are we hard-coding reliable streams into the network operator model? Let's keep those in mind, if we want to use this for non-reliable streams.

Jana: I agree with what DKG just said. What happens if the ack rate goes down. But I have a broader point—I've spent the last year listening to the arguments on all sides. I've considered all the benefits and costs carefully. My informed opinion is that we should NOT include this bit in the core specifications for v1. I am happy for it to be an experiment, even Internet-wide, but there are a lot of open issues that challenge this mechanism. I don't think this needs to be or should be in the core spec.

Kevin: We've measured very high deployments of QUIC on cellular networks. We would definitely see high benefits from a way to measure latency, specifically the vec.

Emile (from orange): Implemented the spin bit, and it did provide us with enough information to do troubleshooting to detect where problems are in the network. We don't need any more information than the one spin bit.

Colin: I think it's fairly clear that there's no meaningful information leak from this bit. I think from that angle it's worth including. If anything, there is too little information here, and we won't have enough when the network misbehaves. I don't think it will solve all the problems, but I think it is worth doing. We should consider arranging the bits in a way such that if they are useful, they can become invariants.

Praveen: We have a general use case in the cloud to measure what happens with tenant traffic; we do that with TCP today, and we'd need the same thing from QUIC. The good thing about this proposal is that it is not compute or implementation intensive. We should put this in v1 to unblock the experiment, doesn't need to be in invariants.

Aaron: Channelling from jabber: are there ways to use QUIC version to experiment with this bit?

Patrick: I will take issue that this does not leak interesting information—it leaks the RTT. HTTP often does request-reply, and this can help detect the RTT as a signal pattern. I think this is not obviously harmless. Doing this is ossifying around the behavior of the TCP ecosystem, from accidents that TCP made to expose the RTT. I'm opposed to any bits being exposed here. We would not participate in this.

Thomas: We have compelling evidence that this does work, and I think it should be part of the invariants in order to rely on this to do measurements. On mobile networks, we see high variance, and this bit is very useful to extract the signal.

Brian: While stating my skepticism to resisting traffic analysis in the network, there were issues raised for unreliable streams, or when the ACKs are not done like TCP. I think they're valid points, but they are not a problem. Your sample rate goes down, but you always have some sample as long as you have some network interaction. To Patrick's point, as long as you have a five-tuple flow identified, all you need is a low delay between two packets to detect patterns; the samples for location are there—the point of the spin bit is to get better fidelity information about the performance of the network. For the cases we're looking at for network health, I don't see a world in which that concern goes away for QUIC. Yes, of course it leaks the RTT, but we want to communicate that. As far as the information leaked between streams; if you're doing multiple streams together, you're obscuring the timing of the data on the streams, but you still have this edge pattern on the full flow.

mnot: In your proposal, this is always opt-in for both parties, right? It's not a guarantee even if it is in the invariants.

Brian: Yes. On the point of greasing, individual flows can choose to opt in or out on a probabilistic basis. And if everyone chooses to not opt in, then there just are no signals.

Gabriel: I wanted to emphasize the nature of opt-in. We would definitely opt-in (Microsoft), not necessarily 100% of the time, but we would participate. The reason I'm confident for support is that we have done privacy analysis; I'd like to see the same done for the vec.

Zahed: Now that we've implemented this in the hackathon, I'm more convinced this is useful. I've worked with service providers, and they see the point of measuring RTT. This is useful. But, I also think we should discuss a bit more about the unreliable mode. We are seeing QUIC as a general purpose protocol, and I don't see this bit as a big issue. If this is not an invariant, in v1, then we won't get the testing we want to do. Since it is opt-in, then it's safe to have. I think it is fine!

Ian: I wanted to reiterate that sending fewer acks can induce about a 25% level of noise to the RTT estimate. If we do this, I want it to be good enough to be a useful signal. I'd rather have this be useful—so have the packet number in the clear, or have two bits in the packet. Speaking with implementors and operators, there are mixed opinions. Lots of yeses, noes, and maybes. If this is v1, it will be a pain in the future. We should go in the direction Jana was indicating. I want an experimental draft from Brian that uses many bits to make this more useful, and see what happens. Use all 5 bits. This seems like server push—a cool idea we think could be useful, but we shouldn't have added to v1. We shouldn't build anything we don't think is absolutely useful. Those who want to do this, do experiments.

Marcus: We took QUIC stacks at the hackathon and got really nice measurement results, and clear benefits. Based on the probabilistic opt-in, the operators will have to be flexible from the beginning.

Manasi: I understand this from the point of view of a client endpoint, but there are other ways to understand the RTT. I suggest we spend more time understanding the value of this.

ekr: My understanding is that if we encrypt the packet number, we do need a vec.

Brian: Yes, to get good signal when the network degrades.

ekr: And that's presumably when you want it.

Brian: There are other scenarios, but yes.

ekr: If I were given only two choices, between one spin bit and two, but with encrypted packet numbers, I would choose the latter! I took a little look at where this would go.. we have five fixed bits in the short header; adding the vec does cut into the flexibility of the bits we have left. If we need more bits, we're not in a great situation. We better be sure that it works before we add it. The vec seems un-baked to me right now. If it turns out that it sucks, then we'll be sad we used the space for it. Sorry to kick the can down the road, but I find it hard to decide now.

Spencer: As AD, I've been mostly hands-off. I have a couple questions.
Please hum if you think this is research, or engineering.

Brian: Putting a signal on packets in engineering; the basic measurement is engineering; the possible field of things to do with the measurements is research.

Ted: The choice between explicit and implicit signals is architecture.

mnot: Please return to the queue...

Spencer: Please hum if you think this is engineering (strong hum, mainly on one side); research (definitely less, but not trivial, other side of the room).

Marten: QUIC is not the only UDP based protocol out there. The only thing to identify a QUIC short header is a 0 in the first bit, so a middle box will have to guess based on one bit. What does this mean for other protocols on UDP?

Sanjay (Verizon): That's to the work in the hackathon. As far as the deployability, we've already seen increased traffic from QUIC. What we're really missing is the ability to help measure the success of QUIC in the next three years, and we need it in the first version to start gathering data from day one. More or less, the privacy issues are outweighed by the benefits of spin bit. Vec for v2.

Mirja: Yes, this is an experiment. As a university, we tried to look into this as much as we could. We simulated many different traffic conditions. But it does work, that's no longer a research question. Whether people will deploy it, we need operators. We need more that just a few sides to experiment—we need clients and servers. If we find it's not useful in version 1, remove it in version 2! That's the whole point of our extensibility story! We should put it in v1. There's not a limitation from the ack feedback. You need at least one signal per round trip time. I can tell you QUIC will not get through the IESG without congestion control.

Kazuho: While I find a use of measurement, I favor taking this out of the core protocol; you can participate in the experiment or not. Why not make it an experiment.

Andrew: I've been looking at various distributions, and I think there's a lot more information you can get out of the vec than is immediately obvious. The same estimators work even without the spin bit, it's just more expensive. The privacy argument is not there as long as the attacker is willing to spend the resource. The only people we hurt are systems in the network for diagnostics.

Lars: What should the WG do? This goes to everyone in the line.

mnot: Options:
    1. Spin Bit(s) in Invariant
    2. Spin Bit(s) in QUICv1
    3. Spin Bit(s) in negotiated extension
    4. No Spin Bit
    
Emile: We deployed this in Orange, and it helped detect issues before there was a fallback to TCP. 

Ted: When will we know about encrypted packet numbers (to the chairs)? 

To Patrick's point, the design team did not find issues with privacy that could be leaked.

I think the ossification is not what people are thinking of.

Chairs: We were about to announce the design team for the packet number encryption, and we should land this within the next four weeks (probably won't affect the invariants).

Ted: I vote for option (2)

DKG: I prefer (4), and also (3) is fine. This is the right group for the experiment, so (3) is fine. I actually got in line to respond to Brian, saying that traffic analysis was inevitable. I share his fear, but do not share his nihilism. I want us to keep fighting that through your research, Brian.

mnot: To recent comments about v1 and rolling back in v2; that's possible we can roll back, but since v1 is aimed at HTTP, it's not clear that v2 would be adopted by HTTP.

Spencer: My decision to charter QUIC was at the same time that we didn't charter PLUS. We didn't want to wander around with that in the IETF. We don't want the PLUS WG here in the QUIC WG. I don't want to continue to have that discussion.

Brian: I apologize to DKG for encouraging nihilism! I'm pretty firmly on option (2). I've heard lots of people volunteering me to do work. If there is an indication that the work will help for signalling at scale, I'm okay with that. I agree with ekr that encrypted packet number plus Spin plus Vec is the way to go. The explicit signal is a big win.

Roni: My preference is option (2), of course depending on the encryption of the packet number. There was a point about not all network operators need to use this, of course not all of them will want that! Many operators have different layers. But other operators work at the TCP layer today, and want to measure this. It depends who you ask. There was another point about the first bit being checked for QUIC—that's a point about multiplexing that was brought up in the other discussions.

Al Morton: To Ian and others, yes—at NANOG, the operators won't care about this. That doesn't mean that that is universal. With regards to patterns changing, you're describing a day in the life of passive measurement designers. This is what we do, and we can handle it. For those who want more study, the slides didn't cover the entire draft. Please read the full document! Andrew, it's really hard to make measurement of inter packet times work, especially with QUIC. My choice is option (2). I want it in v1 to be a large scale deployment.

Martin: Ian's comment resonated with me quite a bit. We've been sold a lemon before, and we don't know what we will get. Slight preference for (3).

Guiseppe Fiocolla: I support option (2) to allow network operators to measure performance, etc.

Praveen: Clarify a comment that Mirja made, we do have large deployments end to end, so we will be able to experiment with this at scale. For options, I prefer (2), and can live with (3).

Subodh: The version is not in the short header, and since the five tuple is the way to tell the flow, it's not based on the version. I don't see how option (3) would work. I'm concerned about differentiated service based on the use of spin bit or not. I don't think this meets the engineering bar for v1 (option 2). I would like to see it tested in the real world with HTTP/2 transports. I think we have privacy implications because it prevents us from doing other things in QUIC by complicating the middle box view of the traffic.

Erik Nygren: It's worth thinking about adversarial scenarios here, used for controlling flows not just passive measurement. It can turn this from an experiment into something detrimental. I lean towards option (3).

ekr: Christian sent an email to list that we should reserve the bits in the spec for v1. Having to re-arrange the bits is a cost, the potential privacy loss is a cost, etc. This entire project is to some degree an experiment. Checking if some parts work well or not by deploying in the protocol is what we're doing everywhere else. One thing I want to hear from Brian is that if clients participate, he can detect that, and if they're not detectable then and only then you need an extension.

Mike Bishop: The signal that it's QUIC is not just a 0 bit, but it does have a pattern for QUICv1 (but those may be greased, so we'll lose some). Currently the only things we communicate with type is the type of packet number, so we actually do get more bits. Let's do a (3a) and reserve the bits in v1, and use them in v2.

Dan Druta (AT&T): One point on architecture principles, with opt-in and explicit signalling, this is the right protocol approach. For process, between experimentation and the privacy analysis, we do have confidence. We should put it in v1, not v2. Options (2).

Jana: My opinion is option (3) at most, or (4). With an editor hat on, since we're shooting for November, there are corner cases that will explode the issues list. Repeating that exercise will not be a lot of fun. For the negotiated extension, we don't have a specified mechanism, but we don't know if it will be encrypted or not, and what it will be in future versions. If we do (3), I am concerned that we will disturb other work we need to do. 

mnot: How feasible is reserving the bits?

Jana: I don't think that will be an issue to reserve.

Brian: To ekr's point, if one endpoint opts out, it's really obvious. There's no need to negotiate this value. If we go to encrypted packet numbers, we get bits back. We could spin or grease these bits. I continue to believe that option (2) is the right choice here. (3)/(3a) wouldn't need to be negotiated; and if we do that, the core doc should refer to the experiment to let people know that it exists. We'd also want through the list or the wiki, a sense of how many people would actually do this.

mnot: I keep hearing people say we need this in QUICv1. I don't think that leads to deployment.

Brian: QUICv1 doesn't guarantee deployment; experimental extensions guarantee less deployment. One has more deployment than the others.

Mirja: Adding onto that, there is more deployment if it is QUICv1, but beyond that we need to have devices know what the bits mean. If we define it and reserve the bits, and call them experimental, I don't see the difference. What I want to say is that the server MUST support it and give the choice to the client.

Chris Seal: I support option (2) since if we become blind as operators, we won't be able to do just-in-time upgrades, and customers will be harmed.

Joerg Ott: A point on what we can gain from TCP seq numbers, you are inferring from an implicit signal. The spin bit as an explicit signal can be tweaked. We seem to be assuming well-behaved clients that aren't gaming the networks to take advantage of the behavior of the network (by artificially lengthening the RTT). We're making too many positive assumptions here. I go for option number (3)/(3a). I don't know if reserving the bits is future-proof.

Ian: Commenting on the negotiation for (3), I was referring to doing version negotiation by using an experimental version number that's reserved for QUICv1+SPIN.

Ted: You mentioned HTTP running over QUIC—are we assuming that they'll run over all versions of a type? It makes a difference from a deployment stanpoint.

Mike Bishop: It says it uses "a" version of QUIC, which may be multiple ones supporting HTTP.

Ian: If we do this in QUICv1, just reserve the bits in transport draft, and have another draft.

Brad Lassey: Agree with Mike's point on the version not mattering. 

Brian: Reiterating the fact that the bits are integrity protected, so the space of manipulation is way smaller.

mnot: Mirja's and Ian's comments were quite illuminating. We could put them in QUICv1 for now, and maybe pull them out; or do what Ian suggested, and have two differentiated versions that we can see how they go. That would make our AD happier.

Mirja: The difference is that if you use the version number, it allows the server to negotiate whether the server supports it or not based on version negotiation.

Brian: It's cute we are pretending that QUICv1 is not an experiment. I really like Ian's proposal. QUICv1 scares me that we have version negotiation experience, but we're not deployment. The spin version let's us test the version negotiation.

mnot: Does this set up a marketplace that can block non-spin QUIC.

Brian: The risk of blocking QUICv1 in favor of spin, is way less than going to TCP.

Jana: Question to the chairs: are we changing our goals of version 1 in November?

(all): No,

Jana: I want it to be after v1 in time,

(crowd): Slightly after.

ekr: If this is in v1, it's already optional to execute. You just would or wouldn't send it. The version is an explicit signal to negotiate the spin bit. To make the versions viable, we need to reserve the bits anyway. If we do think it's important to have explicit feature lists, we don't want separate versions.

Roni: Separate version (3) is still experimental RFC, right? Either (2) or (3) is okay. Other bodies define the protocols they support in their network, they just need a document to reference. I'm assuming these are going to proceed in parallel.

Subodh: I think there a lot of dragons in the version negotiation approach. Anything we do, even for a separate version, will effectively become an invariant. We shouldn't mark this as experimental.

Ian: Addressing Mirja's comment for the extra round trip of version negotiation, since most things learn about this through ALTSERV, that won't be a problem in practice. I also want version extensions to be encrypted. Those extensions should be for interior changes, but the path signalling is outside the encryption, so it should be an unencrypted version.

Emile: More support for option (2).

Sanjay (Verizon): If we're looking to standardize QUIC, we need it to be stable. I don't like the version negotiation (3b) option. We should add this into the current release. There's a big divide between the designers and the users/operators.

How many implementers would implement this? (half a dozen, some overlap)

mnot: Is the PR clean to get this in and try it in the implementation interop?

Brian: I'd be happy to do that.

Roni: The network will specifically ask or block based on what they need to see.

Jana: This will make life difficult both in text and mechanisms. I want to land solutions, not resolving anything. Once the PR is landed, the document needs to be consistent.

mnot: We can't make editorial convenience a factor.

Martin: I agree with Jana. This is another pole in the tent. I don't see a problem with a separate document.

Ted: I thought your poll was interesting. Also ask how many would use the bit.

Most operators hands stay up for wanting to use this.

Lars: We don't land PRs and then un-land them. That makes it harder. I object to changing the process.

mnot: We could reserve the bits and have a separate document, and could include the doc in the spec at the end of the process.

Marcus: As a measurement device implementor, I'd be happy to contribute to this work.

mnot: Two paths forward:
    1. Leave out of v1
    2. Have separate document, which may folded into QUICv1 down the road

Lars: Those are certainly options. I'm not any clearer than when we started. We're not concluding on this today. Spencer?

Spencer: This is the most positive conversation I've seen on this for a while—thank you to the WG and chairs for that. 

Can we close on this by the interim? (Chairs)
    
Lars: It's clear that there is enough interest to use the spin bit and understand what it is good for. Option (4), no spin bit is out. Option (1) invariants is out. We're left with either being in v1 or just an experimental version to do the same. Don't delay QUICv1, but allow spinning.

Hum:
    a) No spin bits in v1
    b) Reserve bits, seperate doc (soon) that may be incorporated in later consensus
    c) Don't know yet
    
    Hum for (a): Moderate, but low
    Hum for (b): Strong hum (+6 on jabber)
    Hum for (c): Crickets
    
Thanks everyone! More spinning to come...
