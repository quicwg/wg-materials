# IETF-116 QUIC WG Agenda

* [Agenda](https://github.com/quicwg/wg-materials/blob/main/ietf116/agenda.md)
* [Meetecho](https://meetings.conf.meetecho.com/ietf116/?group=quic) remote participation
* [Minutes](https://codimd.ietf.org/notes-ietf-116-quic)
* [Meeting chat](xmpp:quic@jabber.ietf.org?join) ([Slack](https://quicdev.slack.com/) users can join the #jabber Slack channel)
* [Slides](https://github.com/quicwg/wg-materials/tree/main/ietf116)

## Thursday, March 30, 2023
10:00-12:00 Thursday, Session I

### Administrivia
* Blue sheets
* Scribe selection
  * notes: Robin Marx, Momoka Yamamoto
  * Scribe: Chairs
* [NOTE WELL](https://www.ietf.org/about/note-well.html)
* [Code of Conduct](https://www.rfc-editor.org/rfc/rfc7154.html)
* Agenda bashing (unbashed)

## Chair Updates

[Slides](https://github.com/quicwg/wg-materials/blob/main/ietf116/chairs.pdf)

## Multipath

[Slides](https://github.com/quicwg/wg-materials/blob/main/ietf116/multipath.pdf)
presented by Yanmei Liu & Yunfei Ma

**Yanmei**: Main changes since last time (see slides). Main thing: removal of single packet number space support, as a conclusion we draw from the last ietf meeting. 2 technical reports on comparing the two options with experimental results. Both reports point out that multiple packet number spaces have better experience than the single pns. As we removed the support for zero-length CID support in multipath, the current version requires that people must use non-zero Connection IDs when using multipath.

**Yunfei**: 1st main issue. Removed Path ID and only use CID sequence number. 2 options: stable path ID vs loose path ID. Any opinions?

**Alessandro Ghedini**: change makes sense from spec pov. Implementations still need SOME id and using the CID seqnr makes sense. Don't know whether this proposal makes it easier to implement, but doesn't seem complicated, so fine by me.

**Kazuho Oku** : Still pref for loose. Stable: people can have that concept if they want, not sure if we want to expose that as a concept in the protocol design.

**Mirja Kühlewind**: loose model was in the draft before, just not very clearly explained. And indeed, in implementation can just have the stable as implementation detail. But have had a lot of questions on what to do, so writing this out helped clarify a lot of these aspects; was the main reason.

**Yunfei**: 2nd main issue. Error code for missing CID during handshake. Just use transport parameter error or not?

**Martin Thomson**: Lots of error codes still available: Just make a new one. Transport parameter error is too generic, and no TPs involved in this error. Oh, except you're saying the multipath TP is wrong? But isn't the fact that the CID is 0-length is what's wrong here?

**Alessandro Ghedini**: Can have 0-length CIDs, but can't have them in combination with multipath. Matter of perspective. Shouldn't set TP at the same time as using zero-length CID. Agree we have enough error code points left; make new one.

**Lucas Pardue**: (as individual) I like specific error codes.

**Mirja Kühlewind**: doesn't make big difference. Can put additional information in the error packet (reason phrase). Not sure if implementations want to treat the error differently, which is what matters.

**Lucas Pardue**: Code is simpler.

**Mirja Kühlewind**: in the end, it's connection error and need to tear down. Will you do anything else?

**Lucas Pardue**: We can call somebody to fix it. Easier to track spike in specific error code.

**Alessandro Ghedini**: From operational position, easier to aggregate by error code.

**Lucas Pardue** (as chair): strong preference for error code in the room.

**Yunfei**: Third issue. More values than 2 for PATH_STATUS (standby vs available). Alternative status values in PATH STATUS #186

**Alessandro Ghedini**: is the question to add them now or in the future? If in the draft: I don't think so. But would be nice to have option open so we can do that later.

**Mirja Kühlewind**: Real questions is 2nd: What to do with value that you don't know.

**Alessandro Ghedini**: Probably sort of depends on what meaning of the new value would be. For now, I'd say ignore it. If later one actually needs to be defined and it's critical, then ...

**Christian Huitema**: Good afternoon. No point in defining the value ... . We do this in QUIC using extension mechanism. If people want to have new var that says "pause this path for 5 seconds". Then write a new draft, send ACK/TP that understands it, but if you see new PATH-STATUS that comes out without you supporting it, then it's protocol error.

**Martin Thomson**: Doc published a while ago that talks about extension points etc. This is a good example of how it's important to have a clear idea of a use case before defining extension point. I propose: remove this extension point completely. If needed later, use new frame type later (basically what Christian proposed). Then don't have the problem that this extension point becomes unusable later.

**Mike Bishop**: I agree with MT. Part of design philosophy of core protocol was to make it impossible to send something invalid as much as possible. Using a new frame type is better from that perspective.

**Mirja Kühlewind**: Agree and that makes sense. *some details on current design*.

**Alessandro Ghedini**: Doing 2 frames is fine. What MIke was saying. IF you send value that's not supported, it's not invalid per se, it's just not supported (e.g., unknown HTTP/3 frame).

**Matt Joras**: don't have that in QUIC. Feel most support for multiple frames as extension point, so best to do that.

**Yunfei**: Main issue 3. ACK_MP on any path or not? ACK MP can be received on any path #190. Should we encourage it or not, and if yes: what is simplest mechanism for RTT measurement then?

**Christian Huitema**: Part of issue is that we use single estimate to estimate many things. Path discovery and congestion control. It only gets complex if you rely on the RTT estimate for CC. IF you only use it for path discovery, only thing you need is to estimate RTO. Naive implementation: whenever receive ACK, I use it in RTO estimate for that path. INcorporate in statistics both network status and algorithmic implementation on the other side. As long as peer follows predictable strategy, RTO will be influenced by both the path evolution and strategy used by peer; perfectly fine to use it to trigger PTO or something. IF people want to do CC based on delays, needs separate specification.

**Ian Swett**: Agree with Christian. If everything is consistent, should work. Some problems with asymmetric paths though; would introduce interesting challenges. Makes sense to prefer lower RTT path for ACKs because faster feedback.

**Mirja Kühlewind**: Will still have discussion in draft on options. Real question is : should we remove the SHOULD here?

**Ian Swett**: Ok to remove the SHOULD on the same path, but would keep the SHOULD to use a *consistent* path.

**Mirja Kühlewind**: Why does it have to be normative?

**Ian Swett**: Otherwise peer's job to do what Christian said more difficult?

**Mirja Kühlewind**: Another proposal. Use PING frame to get RTT measurements on a per-path basis instead of ACKs?

**Christian Huitema**: Can discuss later, but seems I'm in agreement with Ian. IF you keep ACK path stable, if you have a ... . Similar to what happens if you have routing change in network. Most PTOs can deal with that; just fire a bit too soon and you get ACK of PTO. Encouraging consistency is good. If you really want accurate RTT measurement (E.g., for CC) need to explain how to do that in the CC specification.

**Mirja Kühlewind**: That makes sense but that doesn't make sense to make the normative reference?

**Christian Huitema**: If send ACK sometimes after 5th of second, sometimes 10th of second. If you use ACK path, should keep that stable, otherwise strong change in conditions.

**Matt**: People seem to agree on problem, just debate about normative language. Maybe not most important part to discuss here, but good to follow up offline.

**Yunfei**: Fourth issue #200. What if path_status needs to be resent and CID has changed? How to incorporate multiple/future CIDs?

*crickets*

**Alessandro Ghedini**: think PATH frame should hold info about multiple CIDs is what Mirja was talking about earlier. From an implementation perspective that would be useful. Don't know if there are situations where we want to update multiple updates at once. Just sending multiple frames is probably fine; keep it simple. It's not that frequent, so can just send multiple.

**Mirja Kühlewind**: Might send update for e.g., privacy reasons. Does incur many updates on all the paths. Not a huge issue, but does happen. No clear preference. From model discussed earlier, no reasons to not say in advance: I'll give you bunch of CID and you can define in advance if they can be used for standby paths or not. Is about giving semantics about CIDs whether they're in use yet or not.

**Alessandro Ghedini**: Sort of limits how you can use certain CIDs. Might change mind later?

**Mirja Kühlewind**:  but you can send a new one

**Alessandro Ghedini**: Unless there are limits?

**Mirja Kühlewind**: Both works, will bring it to github for more discussion there.

**Yunfei**: Fifth and final issue #180. Separate path_setup frame instead of using QUIC v1 mechanisms to setup new path (current)?

**Christian Huitema**: My advice: just leave that for further extension later.

**Alessandro Ghedini**: Agree with Christian.

**Yunfei**: Next steps. Couple of implementations currently, but more would be nice.

**Lucas Pardue**: 20 open issue, made good progress today. As chair, would like to re-start hackathon efforts to get more multipath implementation experience. If people are interested in this (e.g., getting interop matrices setup etc.) would be good.

**Markus Amend**: ongoing discussion in tsvwg on multipath. Main discussion is on concurrent path usage. Discussion is if this is marked as Experimental or Proposed Standard. Would be good if people engaged in MPQUIC also add to that discussion to get consensus there.

**Yanmei**: Will organize interop testing after this meeting. Will be good to get more input from implementers.

## ACK Frequency

[Slides](https://github.com/quicwg/wg-materials/blob/main/ietf116/ack-frequency.pdf)
presented by Ian Swett

**Ian Swett**: Lots of progress since last IETF (see slides). Some resolved issues: a) change Ignore Order to Reordering Threshold. Should be clearer now (was confusion before).

**Martin Thomson**: This is an 8-bit field, why is that not a varint.

**Matt**: Discussed in London. I was under impression that we agreed to varint it, because that's what we do in this WG.

**Ian Swett**: Can somebody check the draft? Might have updated it and forgot to change slides. Agree it should be a varint ;

**Ian Swett**: b) number of MUSTs changed to SHOULDs to keep consistent with RFC9000. c) one normative change: seq nr doesn't need to start at 0 anymore, but MUST still be monotonically increasing. d) some smaller issues.

**Ian Swett**: Main remaining open issue: Is One ACK per RTT enough? (#168). Let's assume datacenter use cases are out of scope here.

**Matt Joras**: (as individual). Shouldn't have normative language around this. Having recommendations is ok, but anticipating future use cases (e.g., datacenter thing you mentioned) is not easy. Mildly supportive of some "colour" in the text for recommendations, but don't be normative on this.

**Ian**: Keep or drop existing SHOULD?

**Matt Joras**: Prefer to drop it.

**Mirja Kühlewind**: I'm fine with anything but, think we *should* keep the normative SHOULD. ... . Slightly more strong opinion than before the meeting; have tcpm documents that use this barrier, but don't always use normative language there.

**Ian**: indeed, similar docs in tcpm. Whatever we decide here might reflect there as well.

**Kazuho Oku**: No strong opinion on keeping SHOULD or not. Lowest frequency we know to work fine is 4. Can come up with cases where it's 1 per RTT. IF we can provide (Weak) recommendation referring to the safe value is a good idea there, rather than discussing if 1 is adequate or not.

**Gorry Fairhurst**: The lowest number that works reliably with any return path with lots of traffic and loss is actually 2 instead of 1. 1/RTT is at least mostly known behaviour up to the point where congestion causes ACK loss/delay: Regarding 1 ACK per RTT. A better way to explain this is that, unless you have absolutely perfect pacing of data and ACKS, half the RTTs will exhibit <1 ACK and the other half >1 ACK, that’s a performance impact, because you'll be stalling half the time. If the return channel Changing the ACK frequency does impact the CC behaviour: This can synchronise congestion in the return direction to the pattern of transmission in the forward direction, and strong CC synchronisation is worrying. ... . Quite a big change in a transport protocol direction; need more analysis for stability if we recommend 1. Maybe we can say "if you're in a datacenter, might change". We can advise that 3 or 4 is helpful (lower case) advice. Would motivate using normative language for the Internet case and make it 2.

**Mirja Kühlewind**: About Datacenter case: this is why it's a SHOULD and not a MUST. Also don't fully agree with Gorry about 1 vs 2. Won't loss all ACKs, only occasionally.

**Matt Joras**: (as individual) Agree with Mirja. Transport won't break if we don't ACK every RTT. Additionally, shouldn't take for granted that standards documents only talk about what runs on the current day internet and forget other use cases (e.g., datacenter). Doc should be general mechanism, not for specific use case.

**Martin Thomson**: Made a comment in chat with my opinion. Don't think we need recommendations here due to vastly different implementations / use cases. Can put out some facts: if you manipulate ACKs, performance can degrade. If sending fewer than 1 ACK per RTT can have perf impact. If you have extremely low RTT and stable delay, might get away with fewer.

**Martin Thomson**: (copy-pasted from the chat): Agree with @Matt Joras I would prefer to have this be something like "performance might suffer if fewer ACK frames are sent, with worse performance as ACKs are sent less often relative to the RTT. sending fewer than one ACK per RTT can have serious consequences for performance. sending at least several ACKs on each RTT (2-4) is likely to be necessary for adequate performance. connections with extremely low RTT and stable path delay might be able to use fewer acknowledgments"

**Mirja Kühlewind**: Current SHOULD is because there's a SHOULD in RFC9000.

**Ian Swett**: Might be argument to remove this from this document. Aren't in habit to have duplicate SHOULDs across documents

**Mirja Kühlewind**: Careful not to override normative language from RFC9000 either though.

**Ian Swett**: would like to have -some- guidance in the text myself. What are next steps once this is resolved?

**Lucas Pardue**: Forgot to mention Mirja joined editor's team. I think we're getting ready for WG last call. Give people opportunity to review and get deep dive into the text.

**Ian Swett**: Indeed thanks Mirja. Without you, this wouldn't have progressed at this fast pace.


## qlog

[Slides](https://github.com/quicwg/wg-materials/blob/main/ietf116/qlog.pdf)
presented by Lucas Pardue

**Lucas Pardue**: Updates since IETF 115 overview.

**Lucas Pardue**: 1st main issue #283. Versioning of qlog and protocol-specific schema. No clear immediate feedback from room except for 1 thumbs up, so probably just go for that.

**Martin Thomson**: (in chat) why not use JSON-LD for the additional-schema? (later clarification: Martin was being facetious here)

**Lucas Pardue**: 2nd main issue #286. Naming categories. Breaking change for implementations, but right time to do this if we ever want to do that. No direct feedback from the room; if you have opinion, take it to the list.

**Lucas Pardue**: 3rd issue #134. Multipath basic support; is path_id field enough?

**Christian Huitema**: General feedback is that we should probably wait a little bit before committing. Already waiting 2 years since issue open, so can wait some more. Currently have open issue about path_ids tied to CID seq nrs. Whatever we do in qlog should reflect that instead of theories from 2 years ago, so best to wait a bit.

**Mirja Kühlewind**: Need a bit more experience indeed. However, we kind of obsoleted that path_id here, so bit weird ; IF only use CID, kind of hard events that belong to both sides. Need to think of how to do that in an easy way.

**Christian Huitema**: Another issue is matching of events. If multiple number spaces with current version of qlog, graphs look like shit. Really need this notion of multiple spaces inside qlog model (i.e., ACK of nr 25 is within a specific number space, not for the entire connection).

**Lucas Pardue**: we have other fields in qlog that's not literally stuff on the wire. So we could keep something like path_id. Don't think we want something

**Robin Marx**: We decided that we will do stuff that was there at the end of 2022, Multipath support is an exception to this. It shouldn't block qlog docs from making progress (not there yet, but if that ever happens). Imo this should be separate document.

**Lucas Pardue**: Agreed.

**Mirja Kühlewind**: shouldn't block doc and be in separate, but SHOULD have some mechanism to add it in later so it's still possible later.

**Lucas Pardue**: 4th issue. QPACK events.

**Alan Frindell**: (as intense QPACK enthusiast) I was viewing it more as a replacement. Having lowest level of events is qlog replacing tcpdump. Header fields often have sensitive info etc, not what you want, so this helps you tune that as well. I'm sort of interested in implementing this in our implementation. We've seen the dynamic table making a difference, so want to explore. But not sure if people would be interested in doing even the high-level events.

**Lucas Pardue**: I'd personally like to have both low- and high-level options myself. Agree there are security/privacy considerations here that should be included in the PR.

**Lucas Pardue**: 5th issue. Clocks and timestamps.

**Victor Vasiliev**: Not entirely clear to me: do you intend to use ISO 8601 for each event or just once and then use it as reference?

**Lucas Pardue**: define once and then encode stuff relative to that indeed.

**Martin Thomson**: (in chat) RFC 3339 should do to indicate baseline and also indicating the use of monotonic is fine

**Victor Vasiliev**: we had success with always having 1 timestamp in the beginning and everything is relative to that. Using varints mean that compresses extremely well. Also solves the anchor problem.

**Andrew McGregor**: +1 to the relative timestamp suggestion. Precedent on how to represent times. Do use that, because just opaque for something like clock monotonic doesn't even begin to cover all problems you might encounter. We have precedent for this; use it instead of doing something random.

**Andrew** (later in chat): My comment about timestamps and timescales seems to mostly relate to rfc8877 and the history of the PTP alternate timescale field. I haven't right now found a naming scheme for epochs and timescales, but 8877 has some discussion.

**Martin Thomson**: Like the idea of having something like "here is where we started, here is the epoch for following events". We use monotonic in our implementation, and we just say "might drift a bit over time, not ideal for actual time keeping". Would be interesting if we could periodically drop an update to the epoch inside of a qlog (e.g., after machine wakes back up from sleep).

**Martin Thomson**: (in chat) There will be small discrepancies if people use monotonic clocks that jump around a little, but they don't jump around that much; a periodical checkpoint (for NTP updates say) can correct for that in cases where precision matters

**Ira McDonald**: (in chat) from IETF RATS with CBOR details https://datatracker.ietf.org/doc/draft-birkholz-rats-epoch-markers/. See also: https://datatracker.ietf.org/doc/slides-116-rats-epoch-markers/

**Martin Thomson**: (in chat) RATS works is maybe a bit too complex for qlog

**Lucas Pardue**: 6th issue: ECN logging.

**Mirja Kühlewind**:: no issues with L4S, just uses ECT code points. L4S specific events need to be in separate document.

## As Time Permits

### Reliable QUIC Stream Resets

[Slides](https://datatracker.ietf.org/meeting/116/materials/slides-116-quic-closing-streams)
presented by Marten Seemann

**Marten Seemann**: New proposal from WebTransport use cases. 1st proposal: RESET_STREAM_WITH_PAYLOAD. 2nd proposal: RELIABLE_RESET_STREAM. Reset_stream is probably not the correct semantics though? Sometimes it is a reset, sometimes it's more like a FIN. *Lots of detailed discussion. See recording and slides for details. Also good comments in the chat*. Maybe call it STREAM_CLOSED instead?

**Marten Seemann**: Already implemented this in several stacks, only few LOC needed. Is this ready for adoption?

**Matt Joras** (as chair): Reminder: focus should be adoption of existing draft as starting point, not as final solution. Take it this is a dependency for other working groups in the IETF that need this, so please keep that in mind too.

**Mike Bishop**: Overall problem is one that's good to solve and I like this approach. Not sure about STREAM_CLOSED, but can bikeshed this.

**Christian Huitema**: One concern: see a lot that people get confused between RESET and FIN. Application sends short message on stream. Want to cancel that with RESET to intend "forget that I did this". Different to what you described Marten, but wonder if you have this issue: discrepancy between actual FIN and "short FIN".

**Alan Frindell**: When first developing QUIC, said we're not doing partial reliability. But kind of lying, because RESET_STREAM is "stream is unreliable starting at offset 0". This is dividing a stream into a reliable and unreliable half, and RESET_STREAM is just a special case where offset is 0. Not sure this solution is what we want to provide as partial reliability service. If we DO add this, we need to surface this in the WebTransport API as well.

**Marten Seemann**: different notions of partial reliability. Struggle to call this that. Didn't want to open up this discussion (e.g., allowing to have gaps in the middle of the stream is not covered here). We don't need full partial reliability for WebTransport, but do concede this is a step towards partial reliability.

**David Schinazi** (as bikeshed enthusiast and WebTransport wg chair): wonder if W3C will publish WT API before we publish the actual transport. I feel this is critical to WT, so need this done before that can ship. Please adopt this. If people have questions, save them until after adoption so we can move this forward. Don't care about the naming.

**Alessandro Ghedini**: Reasonable solution for the problem. Great to see we already have implementations. Definitely adopt this. Use next 5 years to decide what to call it.

**Kazuho Oku**: Agree with adoption.

**Victor Vasiliev**: For naming, it's RESET_STREAM_AT_OFFSET for me; easiest way to understand. Fine with either approach provided that they work.

**Martin Duke**: Yes adopt. Like this better than the payload option because more general while payload option is more limited. Think we might also need update to STOP_SENDING as well: please send me first 50 bytes of the stream and not the rest.

**Matt Joras**: let's not talk about that now Martin ;) but it is a good point. Let's run a poll for adoption now.

Adoption call results: 38 in favor. 0 against. 38 participants. (people are humming because they want to)

**Matt**: will make adoption call on the list.

## QUIC Handshake Challenges

[Slides](https://github.com/quicwg/wg-materials/blob/main/ietf116/quic-handshake-challenges.pdf)
presented by Marcin Nawrocki

**Marcin**: based on research paper + maprg presentation, see also that. Want to get input from wg on issues identified.

**David Schinazi**: did you take into account the address validation token to bypass amplification limit?

**Marcin**: No, we always used completely new QUIC connection.

**someone**: can solve this by having the client send more data in its first flight (e.g., additional packet with padding)

**Marten Seemann**: Value of 3 was chosen completely arbitrarily when writing this spec. Could have been 2, 4, 5. I don't really care, as long as there's some limit that's not 50x or 100x, we probably shouldn't care.

**Kazuho Oku**: we don't have a limit on the client side. Way of tricking clients to send packets to certain locations you want to attack.


