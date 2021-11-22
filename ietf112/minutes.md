
# IETF-112 QUIC WG Agenda

* [Meetecho](https://meetings.conf.meetecho.com/ietf112/?group=quic) remote participation
* [Minutes](https://codimd.ietf.org/notes-ietf-112-quic)
* [Meeting chat](xmpp:quic@jabber.ietf.org?join) ([Slack](https://quicdev.slack.com/) users can join the #jabber Slack channel)

## Administrivia

* Blue sheets
* Scribe selection
* [NOTE WELL](https://www.ietf.org/about/note-well.html)
* [Code of Conduct](https://www.rfc-editor.org/rfc/rfc7154.html)
* Agenda bashing

Note takers: Robin Marx (RM), Jonathan Hoyland (JGH)
Jabber Scribe: Watson Ladd (WL)

## Chair Updates

[slides](https://github.com/quicwg/wg-materials/blob/main/ietf112/chair-slides.pdf)

Martin Thomson (MT): GREASE Bit WG draft update inbound.
(MT): Update posted

Vidhi Goel (VG): MoQ is on Friday (not Thursday)

(RM): Side meeting today about OpenSSL support for QUIC.

Christian Huitema (CH): DoQ will be discussed in dprive wg on Thursday.

## WG Items

### ACK Frequency
[ack frequency](https://github.com/quicwg/ack-frequency).
[slides](https://github.com/quicwg/wg-materials/blob/main/ietf112/ack-frequency.pdf) - *Ian Swett*

_Ian has a bit of stage fright_

Ian Swett (IS) presenting: looking to wrap-up in near future. Just one main issue open. Let's start with overview.

IS: main open issue is #96 (latency to detect packet loss). There's a lot of situations where sending second ACK after threshold will slow down loss detection. Especially for data senders.
IS: proposal for resolution in PR #100. Main negative is: increases implementation cost by a slight margin, because you have to implement this new algorithm.

Christian Huitema (CH): You're suggesting we add a reordering threshold based on packet counts. I don't think this is the right tool. Re-ordering happens a lot in multiplexing scenarios, esp. equal cost multiplexing (ECMP). Makes more sense to use delays rather than packet counts
IS: agree. There are circumstances this doesn't work. It depends on the circumstance. 2 main mechanisms for declaring loss in RFC9002. This gives sender max number of tools to express those two mechanisms. But you're right, this is not always optimal.
CH: You're think of the ACK delay as two functions,
  1. pacing of acks,
  2. please fire quickly if something seems wrong.

CH: What you're looking at here is secondary mechanism to say "fire quickly if something seems wrong". This can be expressed as a) I'm observing holes in PNs or b) there is some other mechanism. In case a), this is hard to use in practice, because the size of the loss in PN varies with cwnd size, and also depends on number skipping by the sender. You have primary ACK delay and might also want an "ack reordering delay"
IS: you're right we're conflating the two; possible they are not sufficiently similar.


Jana Iyengar (JI): I don't understand the issue of CH. The problem with ACK delay is we don't have packet threshold loss any more.
This proposal brings back packet threshold, which we lost in RFC 9002. Probably have to discuss more on the issue.
CH: indeed, should take this to github.

MT: Think I understand what you're doing, but I would like a picture to make it clearer. Suspect this is along the lines of a right solution though. Bring this to the list and provide better explanatory material maybe, makes it easier to discuss in-depth.
JI: Issue already has some discussion, but fair to bring more context to list. Especially since it's the last design issue; should be able to solve if people look at it.
IS: thought I sent it to the list, but apparently forgot

VG: This gives you a lot of more options. I think I agree with CH, if there's a reordering threshold it can be in time or in packets. If there are two fields we can define in time or packets. If you have the threshold someone can set it very high, which puts us back to where we were. No guidance on how to set this in the draft?
JI: no explicit guidance I think, but probably we should add. PR 100 isn't fully fleshed out yet, probably should include that there as well. Having a fallback will be good, but it would be good to state that explicitly.

Gorry Fairhurst (GF): 2 questions.
  1) already touched on: some element of safety in here: if you get numbers wildly wrong, there's a congestion control implication. So want to see safety considerations/recommended maximum somewhere.

IS: We can discuss it on this issue or some other issue.
GF: It should be a separate issue.

  2) Not convinced that ignore CE is in any way what people that are designing L4S are imagining. Wondering what the impact of deploying this without strong guidance would be on L4S.
VG: +1

IS: we could add some notes on this for them
JI: ignore CE isn't really designed to handle L4S, more an escape hatch for them, in the sense that if no ACKs coming back, you don't get accurate CE feedback. Not designed as -solution- for L4S.
GF: let's take it to the list

### qlog

[Main schema](https://datatracker.ietf.org/doc/html/draft-ietf-quic-qlog-main-schema), [QUIC event schema](https://datatracker.ietf.org/doc/html/draft-ietf-quic-qlog-quic-events), [HTTP/3 and QPACK event schema](https://quicwg.github.io/qlog/#go.draft-ietf-quic-qlog-h3-events.html).
[slides](https://github.com/quicwg/wg-materials/blob/main/ietf112/qlog.pdf) - *Robin Marx*

RM presenting:
In the last few months not much changed, but we changed to a new format. RFC7464.
Use \<RS> as record separator.
Tried to get some practical experience, in general works well, and is well supported.
Will support JSON and this.

For IETF 113 mainly editorial work. Move from TypeScript to CDDL.

KO: We should only support one format so it's easier to implement. With two formats I have to write a convertor.
RM: I understand what you mean. Will need a separate issue for this to discuss pro's/cons of each approach and if we can drop one.

Omer Shapira (OS): Regarding RS separated qlog, are the semantics of merging separate logs going to be understood by the tools.
RM: With normal JSON you can append multiple traces, with RFC 7464 you can't. That's one reason to support both JSON and RFC 7464. However, we do have support for the "group_id" field, where for each event you explicitly log the trace it belongs to so you can demultiplex traces later. So it's possible, but at a small cost. qvis currently does support this.

CH: Multipath support?
Lucas Pardue (LP): It's possible to define everything. It's what you can persuade people to support.
RM: I was waiting for multipath proposal to settle down before going down that route. Once that's done, it should be easy to get some (preliminary) qlog (and qvis) multipath support.

### Version Negotiation

[version negotiation](https://datatracker.ietf.org/doc/draft-ietf-quic-version-negotiation/).
[slides](https://github.com/quicwg/wg-materials/blob/main/ietf112/version-negotiation.pdf) - *David Schinazi*

David Schinazi (DS) presenting: mostly minor issues, most people like the general setup.
DS: want more feedback on whether to publish soon or not. If yes: worth it for editors to speed up editorial stuff.
**crickets**
DS: Please interop with my server, I put it in the slack.
DS: Given limited excitement let's kick the can down the road.

MJ: There doesn't seem to be a lot of implementation appetite. For everyone keep in mind if this is something you want in the future please implement.
JI: Would be good to get some implementation performance experience. QUIC version too plays into this as well, see later?
DS: If we have a v
we're going to have to implement it. Maybe it should be a cluster with version too.

### Load Balancing

[QUIC-LB](https://datatracker.ietf.org/doc/draft-ietf-quic-load-balancers).
[slides](https://github.com/quicwg/wg-materials/blob/main/ietf112/quic-lb.pdf) - *Martin Duke*

MT: I think that your Stream Cipher Algorithm is budget FPE, which is a little worrying. Maybe Chris Patton (CP) can suggest a STPRP that can be used.
CH: We've gone to the CFRG for review.
MD: missed the mail maybe because we didn't go directly to the CFRG, but on advice of Security ADs via backchannel-ish mechanisms.

IS:  now that we have worked through backlog we're excited to help take this further. Still some details to figure out who on our side will do the work, but we're planning to do this. This is mainly for the stream ciphers etc., key rotation stuff is probably more than a year out on our side. We will deploy at least one of these options soon though.

MD: Are you talking about the retry service vs. the load balancing? I anticipate the implementations of one vs. the other being very asymmetric, so don't want to block one for the other.
LP: Has anyone said they _wouldn't_ like the split?
MD: brought it up a long time ago and got some negative pushback. Becoming more convinced it's the right way to go, so bringing it up again now. Need to bring it up more on the list.

LP: If splitting them is going to make some progress on implementing one of them then I'm in favour, but are they truly independent?
MD: together because of a common thread of middlebox coordination.

MJ: From a chair perspective, what is your opinion on the necessity of interop. Seems like there haven't been a lot of design issues recently. Do we wait on interop? Do we have to interop everything?
MD: two concerns on maturity.
  1) document is written in way that is implementable.
  2) We are making many decisions about what use cases are the most important, and what tradeoffs to make. Some actual requirements from people interested in deploying this would be very helpful for these decisions. My co-author, Nick Banks, has been working with Azure, but has had trouble getting feedback from them.


## Unifying the Multipath extensions

[draft-lmbdhk-quic-multipath](https://datatracker.ietf.org/doc/draft-lmbdhk-quic-multipath/).
[slides](https://github.com/quicwg/wg-materials/blob/main/ietf112/multipath.pdf) - *Mirja Kuehlewind*

Mirja Kühlewind (MK) presenting: combined draft from all the authors of three previous drafts; already discussed in side meeting.

MK: enable_multipath TP negotiation mainly for the drafts: not intended to stick around like this for final setup; mainly to make experimenting with different options easier. Goal is to evolve towards just one of both PN-space options.
JI: I want to push back against more implementation experience.

KO: By saying that path is defined by 4-tuple (bidirectional), is the receiver required to send ACKs only on the path on which it received the packets being acked?
MK: no. Just that you can receive on that path. How you ack packets, it's currently left to the implementation. No requirement to send ACKs on the path that the packets were received on.
CH: Actually, we do specify very clearly that ACKs can be sent on any path.
KO: The reason I asked is because you can only ACK packets on different paths when you retain per-path ACK queues. Single PN space means ACK on only one path.

Xiaobo Yu (XY): potentially put this in the introduction to say how you can use mpquic. Currently ATSSS/3GPP has strong support to add mpquic support and ((...)). Perhaps we can complete mpquic work just before the release 18 (at 3GPP) and then try to adopt this (mpquic) RFC into release 18.
LP: Let's keep this to clarifying questions only due to limited time.
MK: very important use case. We should probably have more discussion on this in the future, but not in this meeting. Right now, focus on basics of the draft.

JI: You said the decision between single PN and multiple PNs requires more implementation experience. but MJ said in chat "Yes, to reiterate, we anticipate this to be the first major design issue if the WG has consensus to adopt.". Which one is it?

MK: personally, people deciding to only implement one or the other is good input to this group. If everyone in the end only implemented 1 approach, then we don't need further discussion. However, depending on your stack your mileage may vary, so it depends. For now, we think single PN space is easier, but didn't yet evaluate some of the logic you need to implement, that's probably more work
MJ: agree with Jana that's a design issue. Understand you want input from developers which design works with their implementation.

Spencer Dawkins (SD): thank you all for doing this work. One of the path selection strategies people have been talking about in QUIC is sending ACKs and data on different paths. Clarifying question: does that work with 1 PN-space, multiple, both or neither?
MK: that is completely independent, works with both. ACK_MP defines which PN space is related to.

Markus Amend (MA): does mpquic also cover DATAGRAM extension?
MK: yes, extensions are independent and you can use both together.
MA: wrt PN spaces. We're developing MPDCCP which has similar characteristics, especially when thinking about DGRAM with unreliability which has challenges to mpquic. We explicitly chose to use different PN spaces for MPDCCP because it helps to distinguish on receiver side lost packets and delayed packets. That becomes important if packets need to be reordered.
MK: I'm not too familiar with the detalis of MPDCCP but it seems like it's not the same as (MP-)QUIC because there it is known if packets get lost on sender side and can be re-transmitted.
MA: It's the same in MP-DCCP, packet loss can be detected, however if re-transmission is not in scope, this is a challenge for a reordering process which can be mitigated by multiple PN spaces.
LP: Take it to the list.

LP: let's focus discussion on adoption for now

JI: at high level, document lays out all possible designs. This is not really a good option.
MK: We're not just listing all possibilities. We were trying to stick to the things we agree on. Already a redacted set.
CH: More like an intersection.
JI: PN space is a very fundamental issue?
MK: It's really a detailed implementation thing, it doesn't really affect the core of the draft.
JI: that's good feedback to me. However, protocol standard is about the details. It should make a difference in how the protocol is designed in my opinion. Haven't read the draft though, so no very strong opinion on this yet.
MK: Point taken, what we have right now is two specifications that can work together. In the future we can remove one or the other without having to change anything else because they're separated nicely.
Ted Hardie (TH) (in chat): But this is draft adoption, not working group last call. The biggest thing it does is move change control. Why resolve all the issues before taking the topic on? (got lots of +1's)
LP: let's get an idea of who has actually read the draft, do a show of hands.
Results:

| Raise Hand  | Do not raise hand | Participants | People in room |
| -------- | -------- | -------- | ---- |
|   20  | 46   | 60 |  168   |



KO: is there a design principle regarding efficiency of the protocol? E.g., mpquic should perform -at least- as well? We should clarify this, because it will drive some design choices.
MK: not currently. Listed design principles state mainly what led the authors to choose current options., not necessarily a comprehensive list. Please open issue for that.
KO: before adopting this, I hope we agree on design goals/requirements that we want to meet. It's harder to agree on possible choices if we don't have that.
MK: needs more discussion. Don't understand what such a requirement would mean in practice. don't think it's that easy; fundamentally differences between mpquic and single-path
KO: example for loss recovery, might have clear feedback on ack delay (notetaker: this might be wrongly interpreted), hard to accomplish with single PN space

MD: read the draft, support this work, support adoption, probably won't implement. Don't need to resolve PN space issue before adoption. Of all transports we have, QUIC is best to get open internet experience. Argue it should be experimental, but don't have to settle that now.

Tommy Pauly (TP): unified proposal is better than individual drafts. Focused and minimal, exactly what we want to use as a starting place for our work. I think this is the time to start to work on multipath. Implementations are mature enough to start doing this (at least ours (Apple) is). It would be best to figure out the PN space question soon, but it should be done in the WG in public, not just amongst the authors.

IS: I support the last two statetments. I feel like now is right time. I really would like the packet NS to be resolved, but I don't think that should block adoption. Maybe a one hour meeting dedicated to multipath? I think the packet NS could be bashed out fairly quickly.

CH: definitely support adoption. We want discussion to happen in public in wg, not in confines of authors. If we get adoption, we'll move the current github repo to the quic wg repo where everyone sees it and we'll have change control etc. Making the discussions public is big reason for adoption.

JI: I made the point about not adopting this. The spirit of the q is whether we should work on MP, and I think the answer is yes. I would like to change my position from earlier to "let's adopt it", now is the right time to solve this issue.

LP: will run two polls now. 1) do you think quic wg should work on multipath extension?
| Raise Hand  | Do not raise hand | Participants | People in room |
| -------- | -------- | -------- | ---- |
| 53     | 3   | 56  | 168     |

LP: 2) Should the current draft be adopted?
| Raise Hand  | Do not raise hand | Participants | People in room |
| -------- | -------- | -------- | ---- |
|   46  | 2   | 48 |  167   |

LP: Not hand-raisers would you like to come to the microphone?
** crickets **

General: discussion on the chat about number of authors being too high on the draft and whether that should be fixed before or after adoption (or at all)

## Other (aka "As Time Permits")

### Version too

[draft-duke-quic-v2](https://datatracker.ietf.org/doc/draft-duke-quic-v2/).
[slides](https://github.com/quicwg/wg-materials/blob/main/ietf112/quic-version-too.pdf) - *Martin Duke*

Eric Kinnear (EK) : Any reason we'd want to include the bikesheds? Let's just rev the version.
MD: in my view these are fundamental questions about what happens when you roll a new version that we didn't answer with RFC 9000. How do we number things and what do we do with ALPNs. We have to settle one way or the other.

DS: I think it's not a given that we want to ship a Qv2 with minor changes. That will break a lot of things. Adding Qv2 support to my codebase is trivial, but if I do that then all of our tests will have to run another version. That has a big CO₂ cost for example, because running all tests for all versions. If we deploy these things to our server we have to support them. It's going to cause problems for middleboxes, etc. So, non-zero cost to deploying v2, especially if it doesn't actually change anything substantial. It's not free to do a version with few changes.
MD: Good point. that's kind of the nature of GREASEing; breaking middleboxes that make improper assumptions. Definitely risk of breakage if people adopt this.
DS: In this specific case I don't think the middleboxes are parsing this and assume they only understand the original version I don't think they are doing anything "wrong".

Eric Rescorla (Ekr): in favor of this. Not as worried about middleboxes as others maybe. Would be against making any categorical changes at all. We should just publish this tomorrow, more or less as it is. ((...))

MD: I am also not in favour of putting any fixes in here. I was just thinking of security problems we might discover, etc.
EKR: agree. Maybe put a like 2-month limit on call for things, only include obvious problems/things that are wrong. It should be the case that modulo these constants, code/wire image should not change.
MD: Yes, thank-you.

MT: I'm a little more supportive of this. I don't see us shipping the version negotiation thing without this. You suggested before this might be a -bis version, but I don't think it's like that. I think we should keep it as is.

Brian Trammell: +1 Ekr and MT Go even further. Chairs should schedule (not necessarily start) WGLC immediately at adoption. Reduce temptation to stuff new things into this. Agree a bit with DS. But right way to discover cost is to publish the document and experiment.
MD: I'm very sympathetic to the view that we should ship it immediately, but there are _some_ things that need to be done (e.g., ALPN issue).

TP: +1 MT and BT. I want to answer DS's point to this being expensive.
We just need enough people deploying this so that the internet sees the new version coming by. E.g., YouTube doesn't need to use this. Apple is using QUIC for a ton of traffic on private relay. We don't care about SNI there; so we could deploy this first where it's safer than e.g., Google's main stack.

LP: Will send adoption call to the list.


### ACK_RECEIVE_TIMESTAMP

[draft-smith-quic-receive-ts](https://datatracker.ietf.org/doc/draft-smith-quic-receive-ts/).
[slides](https://github.com/quicwg/wg-materials/blob/main/ietf112/receive-timestamp.pdf) - *Connor Smith + Ian Swett*

Connor Smith (CS) presenting: receiver of packet tells sender exactly when each packet was received. Provide richer signals for congestion control algorithms.

CS: we have a paper in the queue that details this; hope to share details soon.

CH: I looked at the design and it's a logical design if you want to do fine-grained. The reason my current proposal doesn't do that is that I got the feedback in the WG is that we want extensions to be composable. One of the subtle differences is that the CH version is composable.
Chat: Eric Kinnear and Lucas Pardue also echo concerns about composability of ACK extensions.
IS: We talked about this a long time ago, we can consume all of the ACK info simultaneously. There may be places where this is less usable because it's not composable. It depends on the use case probably.
CH: example of composition is using this as part of the path challenges.
IS: could also use this to get the same information
CH: it's not quite the same, because not supposed to ACK the path challenges

VG:  Clarification. If there is an ACK timestamp frame is it going to follow the same schedule as the ACK freq frame? Or less frequently?  If there are compressed acks (e.g., once per RTT), probably won't really work for real-time transport.
IS: RT CC would have to decide which ACK frequency would be needed. Would want to use a canonical value (like 1/4 RTT or less). Feel like this is a tool a CC can use to give more info, but CC needs to decide if it needs it or not.
VG: ((...))
IS: packet loss and other signals are used, but not for bandwidth estimation per se. This was sent out to the list, so would you mind following up there?

JI: strongly argue for composability. Difference between ACK and timestamp. If peer does not receive timestamp it's fine, not so with ACK. having separate frame for this information would thus be best. Secondly, reasons that ACK ranges exist in ACK frame is that we can express a list of acks. Doesn't make sense to express a timestamp range... not even sure what that is. Would love to see a timestamp per packet that is ACKed.
IS: That's what the format actually does. It's that packets are not delivered in order.
JI: what is a range of timestamps though?
IS: you get timestamps for the next seven packets for example.
LP: let's discuss on the list

### 0-RTT BDP

[draft-kuhn-quic-0rtt-bdp](https://datatracker.ietf.org/doc/draft-kuhn-quic-0rtt-bdp/).
[slides](https://github.com/quicwg/wg-materials/blob/main/ietf112/0rtt_bdp.pdf) - *Nicolas Kuhn*

out of time

## Planning & Wrap up

Chairs will deal with action items and will communicate with some folks over back-channels before
bringing things back to the list.
out of time


