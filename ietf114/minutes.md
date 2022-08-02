# IETF-114 QUIC WG Agenda

* [Agenda](https://github.com/quicwg/wg-materials/blob/main/ietf114/agenda.md)
* [Meetecho](https://meetings.conf.meetecho.com/ietf114/?group=quic) remote participation
* [Minutes](https://codimd.ietf.org/notes-ietf-114-quic)
* [Meeting chat](xmpp:quic@jabber.ietf.org?join) ([Slack](https://quicdev.slack.com/) users can join the #jabber Slack channel)

## Thursday, July 28, 2022
10:00-12:00 Thursday Session I

### Administrivia

5 min total

* Blue sheets
* Scribe selection
  * notes: Robin Marx + Brian Trammell + Momoka Yamamoto
  * Scribe: Jonathan Morton
* [NOTE WELL](https://www.ietf.org/about/note-well.html)
* [Code of Conduct](https://www.rfc-editor.org/rfc/rfc7154.html)
* Agenda bashing

### Chair Updates

5 min - General updates about the WG [slides](https://github.com/quicwg/wg-materials/blob/main/ietf114/chair-slides.pdf)

HTTP/3 is an RFC, yay! **applause**

**Martin Duke (MD)**: Agenda bash. Lucas and MD have draft about putting QUIC in alt-svc records. Will be discussed in HTTPBIS today (strip down alt-svc to not have parameters). Upshot for this WG: probably strip down to just service B and the place where service B stuff lives will be in the QUIC wg. So look for that and call for adoption relatively early.

## WG Items

### Multipath

40 min - Open issues, updates to [multipath QUIC](https://datatracker.ietf.org/doc/html/draft-ietf-quic-multipath). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf114/multipath.pdf) - *Mirja Kühlewind*

**Mirja Kühlewind (MK)**: Biggest change: unified proposal on packet number spaces (see slide 7). Biggest open challenge: issue [#125](https://github.com/quicwg/multipath/issues/125) (ack delays and calculating accurate RTTs with single packet number space).

**Ian Swett (Ian)**: hardware offload: is there available hardware offload for QUIC today? Have looked for it haven't found it. Or are we anticipating future HW offload?

**MD**: #25 (hardware offload) was my issue, filed speculatively based on conversations with hardware vendors in the past. But no, offload doesn't exist yet. Just concerned that messing with crypto algo means we have another mode for multipath that might not be viable. Not a show-stopper at this point, but we don't want to have special hardware just for multipath.

**MK**: Nothing deployed. But have done some research to see how this would work, and we found that multiple PN space would make this easier.

**Matt Joras (MJ)**: chairhat off. No HW offload yet, but vendors that we've been working with would be unhappy with multipath anyway. Multiple packet number spaces are simpler, but different vendors will have different opinions on what's easier or harder, based on architecture.

**MK**: is issue in GitHub and needs more discussion.

**Christian Huitema (CH)**: We can't have multiple number spaces without injecting more than packet sequence number into the offload stack -- needs to know CID and sequence number. If people can actually do hardware offload and extract CID, additional step to support MPSN is not that high. Does change API, doesn't change complexity, because need the CID anyhow, or won't be able to find context of connection/needed keys.

**Jana Iyengar (JI)**: One of the things with hardware offload, people use the TCP model to think about it, which is why sequence numbers seem useful to offload. They aren't in QUIC. Don't expect seq nrs to be sequential. WE want to have gaps, is part of QUIC philosophy and design. PNs are not stream seq nrs! Echo CH: something explicit needs to be handed down to offload engine. Not something you can simply offload as task to offload engine. Hardware offload should not play a role in this decision between Single and Multiple PN spaces.

**MK**: How you decrypt the packet number depends on the space

**MD**: at the risk of going down the rabbithole: enc and dec problems are quite different. On decryption side, must expand from the truncated packet number, which is a harder problem. Question is whether vendors will find it worthwhile to implement.

**JI (jabber)**: One more thing - multipath likely implies different NICs, and hardware offload likely also means that different NICs are handling parts of the connection anyway. This means no single NIC will have a view of the entire connection.

**MK**: end of this partial discussion. Next slide (nr 9)

**Eric Kinnear (EK)**: path abandon stuff. What if old path receives both challenge and abandon at the same time?

**MK**: _replied, TODO fill in / see video_. If you have multiple PN spaces: can send ABANDON as explicit signal you won't answer on that path. _further discussion here between EK and MK_. Abandon only works if you have path identifiers.

**Alessandro Ghedini (AG)**: Starting work on multipath now. Single PN space doesn't give us much benefit. Implementing both is kind of annoying, so might just do multiple PN spaces. Might reconsider later on implementing both. Not super clear what benefits of implementing both are. QUIC impl needs to support the non-zero-length-CID case anyway and you end up implementing multiple spaces anyway, so adding single space is more complexity for little benefit.

**MK**: If you don't need zero-length CID. Some use cases might need to save bytes. Two options: try to keep multiple PN space for zero CID in one direction, some additional complexity. Other option: put zero-length-CID in extension, but not clear yet.

**AG** zero CID mostly client, supporting on only one side might be OK. Need more comments from someone considering those use cases (MK: agreed)

**Lucas Pardue (LP)**: (covid mask policy reminder)

**Ian**: More of a single space fan as individual, but requiring both seems worse than just requiring multiple. wrt zero-length: cases where Chrome will open two different ephemeral ports at the same time, so two sockets, and so use different ports to identify paths. But I have to go back to the original discussions to make sure I fully understand.

**EK**: +1 -- I was originally someone who was into single PN space. But two is strictly worse than one, and multiple PN spaces is more attractive now.

**MD**: I'm not implementing this, but attraction of single space is get simpler code and "cheap" Multipath. But if we require multiple spaces, you have to pay the entry cost, and the point of keeping single space around is not that useful for me.

**MK**: wrong assumption that single space would be easier. Looks easier at first, but delay calculation is complicated (etc.) -- so this ends up being a lot more code. Not only optimizing, just delay calculation doesn't work correctly. Doing the right thing is hard.

**MD**: If coding simplicity is an illusion, that kills single PN space for me entirely.

**MK**: Multiple PN spaces don't support zero-length CIDs in both directions. If we need that use case, we need something! Really questions is what do we do with zero-length CID. Do we want to support this or not.

**Omer Shapira (OS)**: like many other implementors, leaning toward multiple PN space. Not finding evidence that single spaces are needed today. Can emulate zero CID using a known constant, which fixes the problem simply.\

**Luke Curley (LC)**: Noticing in some wg's: adding context/pn space ID to distinguish between sessions (E.g., capsules in MASQUE). Wonder if overloading CID Is the correct approach. Makes LB more difficult? Or do we want to put PN space as a field in the header explicitly? Might benefit a lot of different working groups.

**MK**: open to this discussion but want to keep changes to the base spec minimal.

**LC**: IF we start making copies of all QUIC frames (e.g., adding context to all), it just screams a bit to me that the base might need changing.

**CH**: on this discussion... started experimenting with (unint) very early, did implementation of both to measure complexity. Complexity of Multiple PN space: add bunch of statements in code to check whether this is Multipath or Singlepath case. and more checks for MP space. Complexity of single PN space, you need a lot of structure in the code to handle that. Single space was 5% less efficient. Took that as a challenge, can I make these equal? Yes, did in the prototypes, but I needed to add a lot of code in the ack scheduler and add structure in storage of packets to make sure they didn't just carry PN but also path and retrieve which packets were sent before/after. Overall complexity is much more than the multiple number space. Reason behind unified proposal. The reason for additional complexity is the zero CID case. Is this actually needed with multipath?

**MK** Agreed this is the main question. If people have a use case for this, would be good to hear about that.

**Ian**: Not understanding the problem, if I can distinguish the path on the receiver then I can zero CID. If not, I have to use nonzero len CID. Why does multipath make this different?

**MK**: does work, but just makes your scheduling and ACK code more complex to get it right. Have to decide which PNs to use on which path and that impacts a lot how your ACKs will look like. ACK size + you don't know what the other side is doing (ack frequency). Ambiguity about ECN markings and to which path they belong etc. Need to reduce congestion window on both paths. Same is true for ACK delay calc, can only calc on longest path. Need logic for all of that. If you only send a few packets it doesn't matter.

**Ian**: Completely agree. Was mainly asking why we can't have zero-length CIDs with multiple packet number spaces.

**MK**: same packet number on both paths, don't know how to distinguish.

**MK and CH**: can't encrypt same PN twice! Packets arriving with same number on two paths, need path ID in crypto to understand which key to use. without that crypto breaks.

**JI**: assume fair amount of agreement on multiple PN spaces. possibility to consider what else we can do for bandwidth optimization. Don't hear anyone saying they need zero-length CID support; rather the opposite. At a high-level, it might be over-optimizing before we come to a complete design. Have a fork in the road now. Trying to saddle it and do both things at the same time. Argue against that. Is this a moment to ask for consensus on multiple PN space, to move forward? My opinion is we can.

**MK**: Question is not doing one or the other. We think multiple PN is the way to go. Question is do we want to support zero CID. Can also wait for implementation experience.

**Lucas Pardue**: chairhat. thanks! will discuss and follow up on the list. Mirja's question about implementation experience -- can we spend some time on this at the next hackathon in November?

**Lars Eggert (LE)**: not super closely following. MPTCP research tried to to single space, quickly found out you can't because middleboxes. But that was the original intent. Then we went to one space per path. QUIC gives you the option of a single space. Maybe now we have more experience that we didn't see way back when. NOt followed in detail though. Wonder if single space wouldn't be the way to go.

**MK**: think you're thinking about the different PN spaces. That's not what we're talking about here though. Similar, but different. _some discussion between LE and MK_. **LE**: problem was with middleboxes not liking that, but we don't have that with QUIC.

**JI**: Difference with MPTCP/SCTP. I used single space in SCTP multipath. There were reasons that we did that, but those exactly don't apply to QUIC. Both had assumptions about linear sequencing of packet numbers. Middleboxes. We don't have that in QUIC. My conclusion was that seaprate seq spaces would actually have made things far simpler. A lot of the things that transport does is recovery/cong control. All things that happen on a path and general assumption about sequencing on path-basis. IF we move to multiple PN spaces, those things just work.  With a single packet number space, you need to revisit a lot of assumptions. Not necessarily true that every path will have a perfect order, we tend to have okay ordering, don't want to use same reordering ideas in multipath. You know you have multiple paths. Multiple seq nrs actually make sense. Only reason for single nrs are a problem you cannot solve with multiple. For MPTCP it was NATs, in SCTP was backwards compatibility. QUIC allows for multiple spaces by design and by philosophy. Only if things are falling apart badly should we consider not doing multiple PN spaces.

**LP**: at time, locked the queue, last chance. This has been very helpful, thanks for your inputs.

### Acknowledgement Frequency

20 min - Open issues, updates to [Acknowledgement frequency](https://datatracker.ietf.org/doc/html/draft-ietf-quic-ack-frequency). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf114/ack-frequency.pdf) - *Ian Swett*

**Ian**: Want to use a 1-byte frame type for IMMEDIATE_ACK? (Slide 3) Saw a thumbs up and a thumbs down. Talk about it?

**MK**: depends on how often you expect to send this. If you send it often, should be 1.

**David Schinazi (DS)**: we have like 60 short type packets. extensions might need 1-2. 1-2 extensions per year. Not going to run out any time soon. If the majority will implement, get a one-byte codepoint.

**Martin Thomson (MT)**: Implemented this and number of times is sent is vanishingly small (have stats). We also only send very few PTOs in practice (no PTO on 80%+ of connections). So I don't think an extra byte is a problem here; leave as it is. Though I also understand David's argument. We have space. But we don't have to use it.

**JI**: Wonder if this is premature optimization. We can go with one, or two, doesn't matter much. Suggest we leave it as is. Getting it into people's hands is more useful at this point. Don't expect to send frequently, if you're doing this all the time you have other problems.

**MD**: We're bikeshedding this. Probably no strong opinions. Just let the editors make a decision.

**DS**: (still doesn't work at a proper company. QUIC enthusiast). Beautiful bikeshed. Have the editor's pick.

**Marten Seemann (MS)**: opened this issue because draft says you might want to send the frame at least once per RTT. Not sure why. If you only send it on PTO, I don't care. Once per RTT, needs to be short.


**Ian**: we can probably have some more text then on how often/when you should be sending this.

**Ian**: Next issue ([#118](https://github.com/quicwg/ack-frequency/issues/118)), Slide 4. Is Ignore CE worth keeping?

**MT**: won't be using this in the foreseeable future. understand why some people might want to. QUestion for L4S: Would a transport parameter suffice instead?

**MK**: Think the answer to MT is no. Main concern: this shouldn't be part of this spec. Depends on Congestion control and ECN mechanism on what is the best thing to do. No need to signal that... congestion control should do the right thing, not depend on other end telling you what to do.

**Gorry Fairhurst (GF)**: DOn't currently have an ECN method in the transport area that allows you to ignore CE without dropping. Agree with MK: we should not keep it.

**MK**: if you want to do ignore CE right, it's more complicated -- can never ignore first CE, maybe followups, but... complicated.

**Ian**: inclined to remove it. Can always add back if we find compelling use case / someone willing to implement.

**JI**: I agree. We can use a transport parameter later. We weren't certain how much traction it would get. We have ignore reordering. If no strong push, we shouldn't add the feature.

**Ian**: Next issue is somewhat difficult ([#53](https://github.com/quicwg/ack-frequency/issues/53)), slide 5. How much text/guidance on Congestion Control usage should be in here?

**MS**: Given that RFC 9002 specifies a congestion control alg that is safe and performant on the Internet, this extension should do the same.

**Ian**: Follow-up question. Doesn't anyone have a set of constants they're using with reno/cubic with the ack-freq extension that they've found to work well? Or do we need to run some experiments to get data? We (Google) run BBR by default, no reno/cubic data.


**Matt Joras (MJ)**: no chairhat: have experimented with an internet-wide deployment. Don't think we should have recommendations, it would block the document indefinitely given lack of experience with a variety of congestion controllers at scale. Personal opinion: document is to define mechanism. Concrete strategies people want to use, those can be follow-up documents that specify how to use this extension to achieve a certain result. Currently not yet sure which strategies will be used in practice.

**GF**: IW=10 gives us a fairly strong basis that for Internet Paths, 10 is not a bad number to start with. In DC's the design might need to be different, but for Internet paths this seems reasonable benefit for little risk. Of course a value larger than the RTT isn't safe.  Can't we just see what we come up with for starting values we consider safe before the ID is completed? 2 is very conservative. 2RTT worth is controversial.

**Ian**: some boundaries to getting an ACK every RTT. Can work on this over time. Will keep this open for now. Don't need to fix today.

**Ian**: Next issue ([#96](https://github.com/quicwg/ack-frequency/issues/96)), slide 6. Large number of reordering on real internet (16%), so this might make sense to do.

**MK**: To me, this seems more useful than ignore order.

**JI via Jonathan Morton**: If anyone thinks differently, please say something now about retaining ignore order, else reordering threshold is likely the direction we'll go.

**MK**: if someone wants to keep Ignore Order, speak up now *(nobody does)*

**Ian**:thank you

### QUIC Load Balancing

10 min - Open issues, updates to [QUIC-LB](https://datatracker.ietf.org/doc/draft-ietf-quic-load-balancers). (no slides) - *Martin Duke*

**MD**: All issues are currently closed. only one worth discussion in crypto review. Simple fix suggested. Another suggestion to make it a 12-pass algo, declined for probably obvious reasons. CH submitted PR to explain reasoning for dismissal in security considerations; look at this if you have a concern.

**MD**: Future path of this document. Have reached end of editorial process. 1 option is to go to WGLC. 2nd option is to wait for more code. Currently 2 LB-side implementations. 1 is mine at nginx, 2nd from Ant Financial. Because both are LB-side and none server-side, can't interop... current focus day job is to implement QUIC-LB on server side in Google QUICHE. Will have this soon at Google (within 12 months). So option 2 would be to wait for implementation/deployment experience with the Google implementation. Option 3, wait for more people who aren't me to implement this. What does the community want to see before WGLC?

**MK**: Don't have concern to go to WGLC but if there's no good reason, then why don't we wait for the implementation?

**MD**: Seeing thumbs up with that sentiment. So I'll do another bump once our implementation is more mature. Retry offload is in a similar state but no implementation going on.

**Ian**: question for the group. Is anyone else working on a QUIC-LB implementation?

**EK**: don't think we have plans to immediately deploy anything. Have been looking at it and trying to provide feedback. We need something with a very similar set of attributes, so Martin: I wouldn't give up hope ;)

**MD**: appeal to server implementors. use case is cloud L4 balancers. long-term plan is to do this for Google Cloud. This might be an interesting opportunity for server implementors.

## Other (aka "As Time Permits")

### QUIC Timestamps

15 min - Quic Timestamps For Measuring One-Way Delays [draft-huitema-quic-ts](https://datatracker.ietf.org/doc/draft-huitema-quic-ts/). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf114/timestamps.pdf) - *Christian Huitema*

**CH**: (_is finding out why presentation tools should allow multiple presenters to prepare stuff while others are presenting... Maybe during the next pandemic_)

**CH**: Does the WG want to adopt the draft? Does the WG want to discuss it? Or something else?

**Chuan Ma**: Our academic group is also working on adding Timestamps to QUIC... need to have a discussion, more details. Is it mandatory for sender/receiver to do clock sync if they need to generate TS, or are TS only generated by server itself.

or is the timestamps only generated by sender itself, so it cannot be used by the client to tell something about the information about the timeliness. Do we only measure the OWD from the sender side? More specification may be included in the draft. Also: Is it necessary for the all the packets to contain a TS frame, or only the acknowledgements? Need to specify these details in the draft.

**CH**: We should have a discussion inside the wg about what's needed and get some feedback. This is why I want adoption to get some feedback. On the issue of clock sync. WE had debate about structure of the frame. Had feedback years ago that frame should be simple; doc should only specify mechanism.

**Ian**: Was coauthor on one of those docs. Not being actively pursued at Google, though it is implemented for an internal project that has a nonstandard CC. We published on this, but it's not actively used. Lot more convenient to curry in the timestamp when you receive ACK. Just from code structure perspective, having timestamp available when you process the ACK is convenient. Don't know what to do next.

**CH** agree... picoquic always sends TS on ACKs.

**MD**: Believe understand the case for multipath, but don't really understand single path benefit. Just make ACK congestion worse if send more aggressive?

**CH**: tune ack frequency. or, understand that you can avoid spurious retransmissions and in HyStart avoid exiting HyStart too early because of interference on the ACK pass.

**LP**: _without chair hat on_ some talk about time synchronization, that sounds super-complicated. starting simple wouldn't preclude more complicated things later. _physically puts chair hat on_, we should make a decision at to whether to adopt this, it's been kicking around for some time now.

**Jake HOlland (JH)**: are some good use cases for this. E.g., apply chirping and use bandwidth protection techniques. But do we need it... I could use it I think. So probably supportive, but like to see some development on the use cases maybe to get a better handle on other ways people anticipate using it.

**Jonathan Lennox**: Would be useful for lot of the real time media cases. E.g., congestion controller in WebRTC uses timestamps.

**Yoshifumi Nishida**: wondering about measuring one-way delay for HyStart. congestion on ack path, are there other use cases.

**Spencer Dawkins (SD)**: is the ask about adoption in the WG?

**CH** yep. .Don't want to continue to push draft that gets feedback every 2 years.

**SD**: Can chairs help me understand what the bar is? Close enough to call and say who's interested?

**LP**: as chair: discussion in this session is good. Some of it is if author is still seeking adoption (clearly). I'm seeing generally positive comments that this could be useful. Need more follow-up discussion on the mailing list.

**SD**: heading same place as Jonathan Lennox: AVTCORE has just adopted an RTP over QUIC draft and we had a Media-over-QUIC BOF that wasn't as much of a train wreck as it could have been. Especially if that second chunk of work gets chartered, I would like to see an adoption call go out in the future.

**LP**: Also some discussion in the jabber chat. Chairs will have a discussion.

**JI**: (via jabber): So, first, I think this ought to be not OWD (one-way delay), but OWD-delta, since that is what the algorithm is capable of measuring. Second, there's a question of use -- and as it stands, only the receiver can use it. The value of ts in TCP is that it can be used to unambiguously tell RTT changes, where with QUIC we don't have that problem to begin with, because of unique PNs. That said, this can be an experimental draft that people can play with and see if it needs to be standardized. I don't see the value of adopting and standardizing something that doesn't have people wanting to implement and experiment with, else we end up in theoretical design land through getting this to RFC. Specifically, I think there's value in having the draft, but I don't think we need to have adoption unless people want to use this work.

**CH** Happy to work with someone as co-author

**JI**: Think draft is useful because then people have mechanism to experiment with. But without having a lot of people asking for usage of this thing, would be difficult to design mechanism that's worth standardizing. Need people with use cases first.

**LP**: at time for this item. Will do some discussion afterwards.

### QUIC Multicast

10 min - Multicast Extension for QUIC [draft-jholland-quic-multicast](https://datatracker.ietf.org/doc/draft-jholland-quic-multicast/). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf114/multicast.pdf) - *Jake Holland*

**JH**: (_is employed at the same place as DS: Enthusiasts Inc._) Wants mainly to introduce main concepts of Multicast over QUIC. See also additional discussion in MBONED

**Alex Chernyakhovsky**: Observation: you're proposing something that could be built on top of TCP or QUIC? Is this wg the correct place to do this?

**JH**: Looking for some frames in the IANA registries for QUIC. Does it have to be QUIC? No, you can have different MC protocols. But we would like to aim towards an eventual thing that can be included in browsers, and QUIC seems logical there.

**Lars Eggert**: I liked this since LP proposed it years ago. Glad to see it's progressing. We have this gap in transport between unicast and multicast, and have had trouble getting the strengths of both. How general a mechanism can this be? First time we have approach that mixes uni and multicast. Would be good if it's usable for lots of stuff.

**JH**: the *missing* proposals we think we can just do as-is, that's the demo we want to run. don't have to change the application at all. server-push, dash, could be the same thing.

**Mike Bishop (MB)**: Surprised you're putting QUIC frames on the MC stream, would have expected that just to be raw data delivery.

**JH**: one of the nice design choices, works well to put the frames on the MC stream, can use same crypto, can use same framing. These can be combined using that framing, across unicast and multicast. You can see multicast as an alternate network path. Packet processing is actually the same.

**LP**: over time now. Got some good feedback here. Would encourage hallway discussion. One more talk from Emile which we don't have time for. Understanding this is this relates to QUIC observability. Definitely related to QUIC, so encourage to keep this in the QUIC wg and add to next IETF meeting agenda.
