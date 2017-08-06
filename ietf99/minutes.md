# QUIC Working Group Minutes - IETF99

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

  - [Session I](#session-i)
    - [Hackathon / Interop Report](#hackathon--interop-report)
    - [First Implementation Draft Status](#first-implementation-draft-status)
    - [Second Implementation Draft](#second-implementation-draft)
    - [Issue Discussion](#issue-discussion)
      - [Passive RTT measurement in QUIC - Ian Swett](#passive-rtt-measurement-in-quic---ian-swett)
  - [Session II](#session-ii)
    - [Second Implementation Draft](#second-implementation-draft-1)
    - [Quic Invariants](#quic-invariants)
    - [Unidirectional Streams](#unidirectional-streams)
    - [ECN support in QUIC](#ecn-support-in-quic)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Session I

Thursday 15:50 - 16:xx, Grand Ballroom

Notetakers: Brian Trammell and Ted Hardie

Note Well and pointer to Ombudsteam given.

Blue sheets are being circulated.

Mark notes the Interim coming up in Seattle; there is a deadline for registration.  Please see details at https://quicwg.github.io .

Agenda bash: add hackathon and first implementation draft.

### Hackathon / Interop Report

Mark: Five implementations. Outcome pretty good.

Patrick: Yep five. None had achieved interop of -05 before. Issues: settling on ALPN/TLS versions. See the [compatibility matrix](https://docs.google.com/spreadsheets/d/1cvg5WNGNtoGzoEZTo7NZ-D2nrGXnBox-4sKqVFYN7Bs/edit#gid=0).
No fundamental problems found. Editorial nits. A couple open to consideration. What the WG meant to write down is what was understood...

Mark: Important milestone; we can start discussion on running code.

Patrick: Good thing to do right before each meeting. Hackathon at interims and IETF meetings are good ideas.

Mark: Interim in Seattle will be one day of interop plus two days of meeting. No need to show up for first day if you're not interop testing.

No questions about the hackathon.



### First Implementation Draft Status

-04 was designated, but everyone implemented -05 instead. 

What did we learn from that implementation experience?  Moved to -05.  Possibly time for a second implementation draft now, according to Martin Duke.  He clarifies that the 2nd draft would be a feature set that comes yet, rather than a single successor draft (there might be multiple drafts in this round of iterations).  


### Second Implementation Draft

Martin Duke: want to clarify what the second draft is and isn’t. It’s a feature set that comes after what we’re doing today. Continuous iterative process with multiple features, centered around the handshake. We want to focus on the stream. Key updates, post-handshake CID, and PMTU go into a subsequent draft. See https://github.com/quicwg/base-drafts/wiki/Second-Implementation-Draft 

Strategy 1: settle the wire image. 

Strategy 2: focus on performance testing.

Strategy 3: Mix, “deployable at scale”, Ian’s suggestion. Transport parameters, address validation, stateless reset, and a basic H2 application.

Open this up for comments:

Patrick: Will not stand in a TSV group and talk about scale without talking about congestion control. Let’s focus on handshake items, then get to core features of what we want to do here. 0RTT and things it needs. Transport parameters. This weekend we were butting up against the edge of TLS1.3 deployments. Variety of TLS was almost as wide; 5 different libraries. Sometimes tls18, sometimes 20, sometimes 21. Forcing function on TLS things. 

Martin Thomson: in H2 we discovered that our single dep on TLS was a burden. Including TPE and stateless retry is critical. Don’t think we want 0RTT in 2ndI. Need to get to bottom of 0RTT, because in TLS, there be dragons. Handshake interactions frighteningly difficult. Strategy 1 is the best for what we have. Can scale back LR and CC, but they absolutely need to be there. No firehoses. 

ekr: agree that good to get everything in TLS intf done. not sure about locking down wire image. Open questions: should we encrypt sequence numbers, what about data structures with varlen stuff…? Unless we want to throw away the rest of the meeting agenda now. CC obvs important, orthogonal. We’re a little far away from having plausible implementations of basic things. ACK timestamps, ranges unbaked. Good target would be convergence on… [unint]... maybe instead of phrasing like this, implementations must be stable under various network conditions. Turn it on, send data, have it lose and not freak out. Target I have: good enough to build a plausible simple echo app. Not at scale. Run in small env.

Ian: Largely agree with everything ekr said, except I’d really like to have a multistreamed application, H2 with static HPACK. Otherwise streams aren’t interesting. Happy with 1 but with real data. 

ekr: i can live with that. Obvs focusing on H2 first, but this is a generic system. Though it is a diversion, we could do H1

Jana: Unmodified H2 single stream works just as well. We should specify what app we’re talking about, not just echo. I propose H2. Don’t understand what deployed ad scale needs to do, nobody will do this. Loss recovery quite useful. If written down, we should be able to do it. Nailing down the wireformat: we know it’s not done but it also shouldn’t mean that we’re going to leave it undone for two years. Useful to start thinking about actual deployment. GUIC wire format already a bit ossified. 

Martin T: raised point of flow control, would say that it’s a little tricky, and we should take it out. Put it in carefully, should respect, don’t need to manage. No, don’t lock down wire image, no deployed ad 
Brian Trammell: agree with ekr, Jana, and MT.  What makes me afraid when we talk about a second implementation is getting stuck there with people outside this room.  We should probably hold off running full-blown H2 over this, in other words, as some people might just do that.  I like the idea of going this direction, without lockdown.

Christian: Agree with strategy 1, don’t want to implement H2 just for test. I care about DNS over QUIC. Why should I have to do HPACK?

Jörg Ott: Same comment as Christian on H2. Don’t want to be forced into an API that I can hook up to an H2 library.

ekr: important to nail down wire image relatively soon. prioritize these for the Seattle interim. On Christian’s issue, Implementation impacts your viewpoint here. I don’t care about H2 because it’s easy to link to in Go.. Want to make sure we get generic implementations, not fully integrated muck. Not sure who. 

Jana: Agree on wireimage, should absolutely prioritize for interim. Agree testing flow control is not in 2nd impl, interaction between CC and flow control are very tricky. Application itself: I assumed you could just take an H2 impl on top of a single stream. I’d like to do something simpler. Could implement just GET and response. 

Patrick (off mike): An amplification service. 

Ian: Whilst I recommended H2 with static hpack; I wanted to exercise the stack.

Victor: I want echo, share concern with Christian (/ekr) re http specific.

Kazuo: H1 easiest for us to implement.

Erik Nygren: We may look at whether we want things in the unencrypted wire image for PMTUd. Also need to consider load balancer implementation.

Martin: Consensus in the room seems like a heavily modified Strategy 1. Pushback on “lockdown”. Want to converge close to final wire image in strategy 1. Let’s iterate on the mailing list.

Mark: Can you take a go at modifying the wiki tonight, to discuss tomorrow.

Ted via Jabber: Let’s implement Gopher.

### Issue Discussion

https://github.com/quicwg/base-drafts/issues

#### Passive RTT measurement in QUIC - Ian Swett

https://www.ietf.org/proceedings/99/slides/slides-99-quic-sessa-quic-passive-rtt-measurements-00.pdf

https://github.com/quicwg/base-drafts/issues/631


Emile: On option 2: how can we make passive measurements if it’s encrypted?

Ian: It’s not a sequence number anymore, it’s a token, and you look at the token echo.

MT: other trivial comment: does allow packets to be correlated. 

Ian: It’s an explicit packet correlator.

Brian: on how much memory this takes:  if you need a flight of tokens, you need to save the full flight.  I know of other implementations that do simply implement inequality.  

ekr: what happens if you encrypt the packet numbers?

Ian: We reflect said gobbeldygook in the other direction.

Jana: What happens if you ack every two packets?

Ian: Current proposal is must echo once per RTT.

Mirja: Complexity of measurement can be traded off against how often you reflect. It’s also a confirmation signal.

Ian: Good point, and it has a lot more entropy than we otherwise have.

On option 3: What is “downstream”?
RTT between the observation point and the receiver.

Jana: also, note that approximate congestion window exposure might be a con.

On option 3a: Martin Thomson adds that packet numbers can be used to deal with some reordering as long as they are not encrypted. 

Chris Seal: “filtered out to account for reordered spin bits?” You can always tell when you have a bad signal?

Ian: May need a smoothing filter. You can throw away bad results. Exposing packet number makes it much easier to throw away bad result. 3a is strictly superior to 3.

Jana: I like option 3a if this is something that we want to do. Middleboxes have to fix up reordering for TCP anyway. Nobody uses raw RTT signals anyway.

Andrew McGregor: Found four different spectral methods for RTT measurement on self-clocked CC. So you can’t hide this information, 

Jana: BBR is rate driven. Self-clocking not a requirement

Al Morton: How do you set the length

Ian: CLient starts sending ones, then a one comes back, then it flips to zero. 

Al: Could you keep the lengths of 1-runs and 0-runs constant? It helps (for loss measurement).

Patrick: I think the tradeoffs are well described but exposing not in line with what we know about traffic analysis.

Chris: This is really useful for us in managing our network. RTT is a good early warning sign for tr

Ian: How many people will use this information if it is exposed?

Mark and Lars: Good portion of the room. More than 20.

Gorry: One point about 3/3a is that it is processed data. I want to see these numbers are when things are going wrong, I don’t quite know how well 3a works when that’s the state and I want see jitter in the RTT etc.

Ian: Yeah, if there is heavy ACK aggregation, or etc, this is noisy.

Martin: What’s the MUST/SHOULD/MAY here?

Ian: up to the WG. How can a middlebox tell when a endpoint is doing it? We can specify that, e.g. 

Christian: Not in PR609 yet, but one good way is you only use the value 1, then you’re doing it otherwise not.

dkg: I think I agree with Patrick, we don’t really know what the consequences are. Number of people who do it not relevant. Concerned given what net does with signals now, this gives me pause.

Lars: The tussle here is with network management that can expose enough to help them run the network.

dkg: appreciate the effort to scope it, but [port numbers argument]... We don’t know what the 

Marcus: I build stuff that uses this info. 3a is the only option and I would like it mandatory. I would be super happy with packet numbers, 

[unknown, mumbled]: how to force / measure sender being honest. 

Ian: Peer could enforce that. Requires more state tracking. Possible. 

Christian: This also allows for one-way observation on the RTT. Transition cycle is 1RTT.

Jana: Valuable to have a long discussion right now, but we do have an existence proof of something that might work, does not mean this is something we will do.

Colin Perkins: Two points. If likely to be problematic, we should have heard that the technique is problematic (1-3), then we would know that. Some people have said that there are hypothetical problems  - we should document these problems if they are real.

Measuring once per RTT is an issue. A lot of why you want to measure is during times where there is a problem. RTT clocked signals are dynamic.

Ted: Having done network planning on lots of networks, RTT change is a pretty basic form of analysis. While I certainly have a concern, I have a related concern that this may make networks less easy to operate and that may have impacts on how this is finally used.

Brian: What Ted said. 

Ekr:..........The privacy properties of TCP are horrific, so I am concerned with Colin’s argument.  There are plenty of attacks on TCP that we could be referencing here.  They are not active in TCP, because there are so many other more horrific leaks there.

Colin: There was a claim that there were specific comments that this mechanism introduces a new set of risks and that these have been known, but I did not see these documented.

Ian: I do think you are correct. It is hard to see retransmission in QUIC.

Andrew McGregor: I should clarify what I was saying before about the spectrum efforts.  they don’t actually require a self clock.  The mere fact that a response comes after a query (or a retransmission after the loss), there is almost no way to hide this from a middlebox.  Unless you are willing to add long term delays, you just can’t hide it.  

Tommy Pauly:  I like three a, if we have something.  If you see uniform behavior, ideally, it wouldn’t be giving me any information about what they are doing other than this quic.  I’d like to understand why this is more of a port-style privacy issue.

Brian Trammell: I do think this is important to be easy measurable. If it’s input to an AQM then this is important to get right - we want people to use quic.  We have a big red switch for turning off QUIC, by blocking UDP 443.  We don’t want people to use it.    I’d like a citation to a measurement hiding paper that looks at something like this, rather than timestamps.  I’m really interested in concrete examples of why this is risky and then look at the risk/utility tradeoff.  

Dkg:  I want to make a couple of observations.  I believe Andrew’s point is about a network under one domain of control (No: the paper demonstrates).  Privacy risk:  location can be circumscribed by the RTT.  Privacy risks for geography are well known.  Information about battery life, information about implementation. We need to have a precautionary approach here. IETF has a bad history here. Don’t want to have to fix this later. Don’t want to find out people are colluding to keep people off the network because of their RTT.

Ian: Followup: I think the concern slide would have been . 3a is simple enough to make it turn-offable. We can do that in the next few years. Would have to correlate to turn it off. We could turn it off quickly. 

Mirja: I agree we should consider privacy. We are considering it. I think the negative impacts on not providing this information are much clearer . We have learned some things so far: TCP not designed to expose information. We have experience with where this leads. This information is useful. 

ekr: Our loyalty here is to end-users. If I have to inconvenience the operators to make the user’s life better, then that’s okay. We are trying to be better than TCP. Remove as much signal as we possibly can. The whole reason you remove signal is that is meaningful

How to do an RTT attack: timing of packet decryption. Manipulate packets to create error on receiver, do immediate response. Now you can immediately packets respond to which other packets. Nonconstant timing -> you can extract decryption keys  [fill me in]

Ian: I can do this today by twiddling packets.

Dan Druta: I think what brought us to this discussion is a set of requirements. Are people arguing about what is needed, in terms of RTT on path… we need a solution, period. Of the solutions we’ve seen, 3a seems a good balance between privacy and manageability. Are there clear requirements, and if so why are they not accepted? RTTs necessary for operators as well as enterprises. Unmanageable

Lars: For the WG, the question is do we want to address them.

Jana: The burden of proof for privacy is not on [mumble]. Important that we consider this question now, and not wait for there to be a problem. One of the [mumble] AQM. BBR works toward the same end as AQM. Personal opinion is AQM might get deployed, but endpoints have to do something anyway, can’t rely on AQM. Ultimately bufferbloat affects endpoints. Exposing information to AQM may not be necessary if BBR makes AQM useless [? not sure I got this]

Ian: You mean using this as AQM input may be less 

Joao: I support Option 1, do nothing, which is my default position in life. Risk is we increase surface area in the protocol. What are the risks of HBH options and flow label? If middleboxes can hack around it, then let them do it. Feels like a niche use case. This isn’t even on the right layer. 

Philipp Tiesel: Very much in favor of 3a, first if you don’t give this information it might start an arms race on RTT, and the machinery used for this is useful for other stuff which we’re less comfortable with. If you want more privacy, you could add a small RTT delta (delaying bit flip), still usable but removing some privacy issues. Can also default to zero or completely randomize. 

Lars: We have 25 minutes, do we want to burn to the end?

Spencer: Could I ask some show of hands questions. How many people understand the issue that they can explain this as their job and not starve to death?

Martin: With this much competition, I would starve.

*How many hands?*

Spencer: How many people would like to know more about this?

*Fewer hands than experts*

Spencer: At the retreat in Montreal, the IAB and IESG talked about this. Then the IESG talked about this again. Then the IESG talked about this again. ekr gave an excellent presentation helping the IESG understanding these issues better. It seems to me that if that got a broader audience, that might be helpful. 

Lars: Could ekr do a version of this presentation tomorrow or in Singapore?

Mark: It’s apparent to us we’re not going to make a decision about this today. 

Ian: Is it possible to kill all options except 3a?

chairs: (And one)

Gorry: All transport protocols to date have sequence numbers. And the aim there is not to annoy operators. Let’s talk about how transport protocols work, and interwork with the network. AQM is simply a strawman - there are other network layer mechansisms that transport has to interact with. Being able to measure these things is one of the ways you can do research to keep the network evolving.

Colin: Gorry and Mirja said a lot of what I wanted to say. dkg raised a lot of important privacy issues. I tend to believe that those are not solvable unless you take active counter measures to stop them. I think we need to consider whether are trying to solve a problem which is not solvable. If not, management issues should have some weight.

Ted: Spencer made a parallel between this proposal and PLUS. PLUS was considerably different in scope. This is drawn as minimally as a the tight mind of Christian Huitema can make it. Would like to volunteer the slide deck at the retreat to the WG, which is about getting rid of inference. I would never say that 3a should be imposed on the protocol. This is an explicit signal, and can be explicitly removed. Don’t want to prejudge the outcome. We should be open to the importance of this information to management as we are to the importance to suppressing it to privacy.

Jana: Example of past transports is a poor way to discuss this. QUIC deliberately not TCP. The fact that operators have used TCP headers in the past was because TCP didn’t know better. Now we know better. We know that GUIC has already been ossified. We try to change TCP and we can’t. That’s not good. Second, on soluable privacy concerns… We are in a position to say what information we expose and what we do not. Ian and I have spoken to operators over the past two years about what they might need, and the answers have been vague and lukewarm to yeah we’d like it but we don’t need it. Not sure we can make this 

Dirk: We agree that RTT is useful for network planning and performance management. Mixing up utility and requirements. Given the demonstrated privacy risks, I don’t think we can decide on adding info for RTT measurements without evidence that it is actually required. I don’t think we can decide on this without understanding more.

Sanjay: There certainly is a need for network management for level of accountability on how QUIC is performing. This solution  Let’s go back and look at the charter.

Lars: Group should consider current practices. Need not be defined to enable each of these abilities. 

Sanjay: … want to make sure that QUIC is deployable and that we can measure how well it is performing. Google has been able to demonstrate QUIC’s improvement over TCP. This allows us the tool to do the measurements.

Mirja: Want to come back to Jana’s example, it makes Ted’s point. Information that was ossified was not meant to be shared with the network. When we share something with the network, it should not depend on the internals of the protocol. It must be separated, that’s what we learned. There are ways to infer this information from traffic characteristics, but it doesn’t scale. With this mechanism you get RTT all the time, so you have the same privacy risk but more utility.

Lars as individual: dkg would say...

dkg: You said my name three times and I appeared at the mic. What Mirja said is that one gives you pervasive passive RTT surveillance and one gives you targeted RTT surveillance.

Mirja: No, what I said was… it's a different signal if you have RTT (changes) over time or just some samples.

Andrew: Whether or not you do this, you still have to take active measures to hide your RTT. 

Ted: Please send information about this attack to the list.

Andrew: I’m leaning toward let’s not do this if it could be used to expose information about crypto. I don’t need the RTT as an AQM developer, I can measure the traffic directly.

Mark: Two questions: should a concrete privacy/security violation be identified to preclude adoption, and should concrete network management issues be identified to adopt?

Ted: I present two postulates: 1 there is no chance we’re doing this for the next implementation draft, and we already know that people want to share information about this issue, we have already established that the WG has less information than it wants. 

## Session II

Friday 9:30-11:30

*Bad Note Taker: Wes Hardaker*

Agenda discussion, including related work such as Multipath


### Second Implementation Draft

Martin updated it overnight
- tried to synthesize the comments and getting wire and handshake right
- Converge closer to a final solution and prevents a middlebox from oscifying
- Did not address 5 things (key updates, post handshake, loss recovery, congestion control, http/2 mapping)
- Changed a lot of things based on consensus

*missed something due to conflicts*

Suggested we do http 0.9, simpliest thing is to do string matching on get.  otherwise i think this is pretty reasonable and let's leave the debatable stuff out; if you do more than what we agree to then that's cool

We should just do http.9 and we don't need to support all the primatives.  We already have 2 streams, so maybe it's already multistream and I'd be fine with not including multiple streams
you can multiplex multiple requests

what is stateless reset?

Martin: I thought we changed the term.  

Brian: http 0.9 get multiple seems perfect

?: support removing go away and http.9 get

DKG: if you want to do a multi-stream protocol you could just do ftp (there was a boo)

ekr: agrees further -- resumption and 0rtt

martin will do a few more tweaks and then take it to the list; we're converging 


### Quic Invariants

*Martin Thomson*

issue 645

constraints on the handshake

One point of clarification: what's the scope of handshake?  until version is complete? until 0rtt is done?

no, until handshake is complete. Maybe we share clarify that to not include the client's second flight.  the point at which you start packet protcecting is the point at which the handshake is done

That was true in the previous point of the draft; we could now allow the ip address to change after that (src).

I'm suggesting a change of language: until a server is available from the client, client can't change src addr

there are other things that require the handshake be complete

martin duke: is that a security limitation?

it's connection id arrangement to get a connection ID

if the client hand multiple IP addresses, and maintained connection then you need to associate the connection id as the server

martin: we need to take some steps to simplify this

that does create a whole host of complications like off path attakers -- it's possible they're solvable but we should agree upon this now.
      
What can someone do to keep the handshake from completing?

Ian Swett: Cleartext packets should be encrypted using the connection ID plus some other constant that changes with each new QUIC version. That way, when the QUIC version changes, a middlebox cannot snoop on the new packets until it’s updated to understand the new QUIC version.

Martin Thomson asked for agreement on broad guiding principles:
- Good packets are accepted
- Redundant packets (unnecessary retransmissions) are ignored
- Bad packets cause the connection to be closed


### Unidirectional Streams

*Ian Swett*

Three basic options:
- Support bidirectional streams, with a bit to signal that the one direction is unused
- Support only unidirectional streams, and force applications to invent their own way of pairing two unidirectional streams to make a bidirectional stream
- Support only unidirectional streams, but have mechanisms at the transport layer to support associating streams in a one-to-many relationship

Thomas Pauly: Our experience shows that BYOB (Bring Your Own Bidirectionality) is a substantial burden on the application.

Kazuho Oku: I also agree that making every application invent its own bidirectionality is a problem.

Martin Thomson: There are implications here related to how we handle Cancel Request.

Eric Rescorla: I was initially attracted by the simplicity of unidirectional streams, but so many applications require bidirectional streams that we have to take the responsibility of providing bidirectional streams.

Brian Trammell: I also was initially attracted by the simplicity of unidirectional streams, but have become convinced of the need to provide bidirectional streams. By the same token, there are also applications that need unidirectional streams, and they should also not have to invent their own convention for how to use half of a bidirectional stream. QUIC should also have explicit support for the one recommended way of doing unidirectional streams.

Janardhan Iyengar: 

Kyle Rose: We should optimize for the common case, the bidirectional case.

Martin Thomson: I prefer unidirectional streams plus a transport-provided binding layer.

Kyle Rose: I like the simplicity of supporting bidirectional streams by default, plus a single bit to signal that one direction is unused

Chairs called for hum to get a sense of the opinion in the room:

1. For using unidirectional streams as the basis, with binding layer (moderate hum + 1 in Jabber)
2. For using bidirectional streams as the basis, with option to signal that one direction is unused (moderate hum, very slightly louder + 2 in Jabber)

Chairs asked if anyone is advocating the strict BYOB (Bring Your Own Bidirectionality) model. No one spoke up.


### ECN support in QUIC

*Ingemar Johansson*

Gorry Fairhurst: Let's make sure we specify the basics

Stuart Cheshire: It would be nice to make ECN mandatory, except that we have to accommodate clients on operating systems where the APIs do not allow access to the CE bits.

Janardhan Iyengar: Do we have a list of which operating systems do or do not have suitable APIs? That would be useful to include in the draft.

Eric Rescorla: The ack frame is already complicated enough. We should be hesitant about complicating it further. Perhaps ECN data can be communicated in a separate frame of its own.

Chairs called for hum on whether the group should work on ECN:
1. Strong hum in favor of spending time investigating whether it's worth adding ECN to QUIC
2. Weak hum opposed to considering ECN

